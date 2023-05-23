from datetime import datetime
import googletrans
import gtts
import os
import pandas as pd
import streamlit as st
import zipfile


AVAILABLE_LANGUAGES_DICT = googletrans.LANGUAGES

AVAILABLE_LANGUAGES_DISTINCT_SET = set(val for dic in [googletrans.LANGUAGES] for val in googletrans.LANGUAGES.values())

AVAILABLE_SPEECH_LANGUAGES_DICT = gtts.lang.tts_langs()

LOCAL_ACCENTS_DICT = {'No Preference': 'com',
                      'English (Australia)': 'com.au',
                      'English (United Kingdom)': 'co.uk',
                      'English (United States)': 'us',
                      'English (Canada)': 'ca',
                      'English (India)': 'co.in',
                      'English (Ireland)': 'ie',
                      'English (South Africa)': 'co.za',
                      'French (Canada)': 'ca',
                      'French (France)': 'fr',
                      'Portuguese (Brazil)': 'com.br',
                      'Portuguese (Portugal)': 'pt',
                      'Spanish (Mexico)': 'com.mx',
                      'Spanish (Spain)': 'es',
                      'Spanish (United States)': 'us'
                      }


def get_language_code(value, d=AVAILABLE_LANGUAGES_DICT):
    """Find the appropriate two-letter code for Google to properly translate text.
    If multiple options exist, let user decide which is appropriate"""

    lang_code_list = [k for k, v in d.items() if v == value]

    if len(lang_code_list) > 1:
        selected_dialect = st.selectbox('Multiple dialects are available.  Which would you like?', lang_code_list)
    else:
        selected_dialect = lang_code_list[0]

    return selected_dialect


def return_translated_text(raw_text, source, destination='en'):
    # create a translator object for text translations
    translator = googletrans.Translator()

    # return object with translations
    result = translator.translate(raw_text, src=source, dest=destination)

    return result


def read_and_record(raw_word, file_location, spoken_language, localization):
    """Read each word out loud and save the mp3 file in the correct location.
    Full localized accents can be found here:
    https://gtts.readthedocs.io/en/latest/module.html#playing-sound-directly"""

    tts = gtts.gTTS(raw_word, lang=spoken_language, tld=localization)

    # replace special characters in the provided word.   Use cleaned version as file name
    cleaned_word = ''.join(filter(str.isalnum, raw_word))

    new_filename = cleaned_word + '.mp3'

    path_to_file = file_location + '/' + new_filename
    tts.save(path_to_file)

    with zipfile.ZipFile(file_location + '/audio_files.zip', 'a') as myzip:
        myzip.write(path_to_file, os.path.basename(path_to_file))

    return new_filename


def create_save_directory(filetime):
    file_dir = 'generated_notecard_files/' + filetime
    directory_exists = os.path.exists(file_dir)

    if not directory_exists:
        os.makedirs(file_dir)

    return file_dir


def transform_uploaded_file_to_dataframe(f):
    if '.csv' in uploaded_file.name:
        df = pd.read_csv(uploaded_file)
    elif '.xls' in uploaded_file.name:
        df = pd.read_excel(uploaded_file)

    df.columns = map(str.lower, df.columns)
    return df


def iterate_through_uploaded_dataframe(df, path):
    """For each row on the spreadsheet.   Read the text, save the audio file.   Update the dataframe."""
    for index, row in df.iterrows():

        if df.loc[index, 'source'] == 'x':
            # st.write(f'I am translating from {dest_lang} to {source_language}.')
            translation = return_translated_text(df.loc[index, 'destination'],
                                                 source=native_lang,
                                                 destination=learning_lang)
            df.loc[index, 'source'] = str(translation.text)

        if df.loc[index, 'destination'] == 'x':
            # st.write(f'I am translating from {source_language} to {dest_lang}.')
            translation = return_translated_text(df.loc[index, 'source'],
                                                 source=learning_lang,
                                                 destination=native_lang)
            df.loc[index, 'destination'] = str(translation.text)

        # Check if language is available for speech-to-text, if not, don't record audio
        if AVAILABLE_SPEECH_LANGUAGES_DICT.get(learning_lang):
            file_name = read_and_record(raw_word=df.loc[index, 'source'],
                                        file_location=path,
                                        spoken_language=learning_lang,
                                        localization=selected_localization)

            df.loc[index, 'audio'] = f"[sound:{file_name}]"

            path_to_file = path + '/' + file_name

            with zipfile.ZipFile(path + '/audio_files.zip', 'a') as myzip:
                myzip.write(path_to_file, os.path.basename(path_to_file))

    return df


def write_results_to_csv_file(df, time):
    """save the final results to file"""

    csv_file = df.to_csv(index=False)

    st.download_button(
        label="Download Summary CSV",
        data=csv_file,
        file_name=f'FlashCard_Summary_{time}.csv',
        mime='text/csv',
    )
    return


def download_audio_files(path, time):
    """download a zip file of all audio"""

    with open(path + "/audio_files.zip", "rb") as fp:
        btn = st.download_button(
            label="Download Zipped Audio Files",
            data=fp,
            file_name=f"Flashcard_Audio_Files_{time}.zip",
            mime="application/zip"
        )

    return


######################
# DISPLAY DETAILS
######################

st.title('Anki Language Notecard Generator')
st.write('_:grey[A small tool to create language flashcards.]_')
st.write("""
---
__Instructions:__

1. Select a language to study. (_If multiple dialects of that language exist, select the appropriate localization._)


2. Select your native language.


3. Insert a file (`.csv`, `.xls`, or `.xlsx`) with the following column names:
    * `Source`  (_This is the language you are studying_)
    * `Destination` (_This is the language you already know_)
    * `Tags` (_No spaces allowed, write "common_phrases" not "common phrases"_)  



4. To auto-translate your text, just write "x" in that column and the tool will translate for you.
    * For example, if you don't know the Spanish word for "Hello", write "Hello" under `Destination` and _x_ under `Source`.


5. The tool will automatically translate the phrases, record the correct pronunciation and save an `.mp3` file.  It will also create a single .csv file to import into Anki.

6.  After completing this process:
    * Bulk import the new audio files into Anki's library.
    * Bulk import the newly created .csv file to Anki, and Anki will generate a new notecard deck complete with audio files.
    
---    

""")
########

st.write('<br>', unsafe_allow_html=True)

# Find language to study
source_language = st.selectbox('_Which language are you studying?_', sorted(AVAILABLE_LANGUAGES_DISTINCT_SET))
st.write('You selected:', source_language)
learning_lang = get_language_code(source_language)

if not AVAILABLE_SPEECH_LANGUAGES_DICT.get(learning_lang):
    st.write(':red[**No text-to-speech available for this language.  No audio files will be created.]')

# which accent would you like pronunciation in?
if learning_lang in ['en', 'fr', 'ca', 'pt', 'es']:
    local_accent = st.selectbox('_Which local dialect?_', sorted(LOCAL_ACCENTS_DICT))
    st.write('You selected:', local_accent)
    selected_localization = LOCAL_ACCENTS_DICT.get(local_accent)
else:
    selected_localization = LOCAL_ACCENTS_DICT.get('No Preference')

# Find language to translate to
dest_lang = st.selectbox('_What is your native language?_', sorted(AVAILABLE_LANGUAGES_DISTINCT_SET))
st.write('You selected:', dest_lang)
native_lang = get_language_code(dest_lang)

# Read and process uploaded file
st.write('<br>', unsafe_allow_html=True)
uploaded_file = st.file_uploader('_Please upload a file_')

if uploaded_file is not None:
    CURRENT_TIMESTAMP = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")

    filepath = create_save_directory(CURRENT_TIMESTAMP)
    raw_df = transform_uploaded_file_to_dataframe(uploaded_file)

    final_df = iterate_through_uploaded_dataframe(df=raw_df, path=filepath)

    # display results to user
    st.write("""---""")
    st.subheader('Results')
    st.write(final_df)
    st.write("Saved to filepath: " + filepath)

    write_results_to_csv_file(df=final_df, time=CURRENT_TIMESTAMP)
    download_audio_files(filepath, CURRENT_TIMESTAMP)

