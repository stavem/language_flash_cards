# Anki Language Flash Card Generator
A small tool to create audio files for portuguese flashcards.  Easily import these files into Anki notcards.

Link here:
https://anki-language-flashcard-generator.streamlit.app/

__Instructions:__

1. Select a language to study. (_If multiple dialects of that language exist, select the appropriate localization._)


2. Select your native language.


3. Insert a file (`.csv`, `.xls`, or `.xlsx`) with the following column names:
    * `Source`  (_This is the language you are studying_)
    * `Destination` (_This is the language you already know_)
    * `Tags` (_No spaces allowed, write "common_phrases" not "common phrases"_)  



4. To auto-translate your text, just write "x" in that column and the tool will translate for you.
    * For example, if you don't know the Spanish word for "Hello", write "Hello" under `Destination` and _x_ under `Source`.


5. The tool will automatically translate the phrases, record the correct pronunciation, and save an `.mp3` file.  It will also create a single .csv file to import into Anki.

6.  After completing this process:
    a. Bulk import the new audio files into Anki's library.
    b. Bulk import the newly created .csv file to Anki, and Anki will generate a new flash card deck complete with audio files.
