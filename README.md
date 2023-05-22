# portuguese_flash_card_generator
A small tool to create audio files for portuguese flashcards.  Easily import these files into Anki notcards.

__Instructions:__

1. Select a language to study. (_If multiple dialects of that language exist, select the appropriate localization._)


2. Select a language to translate the text to.


3. Insert a file (`.csv`, `.xls`, or `.xlsx`) with the following column names:
    * `Source`  (_This is the language you are studying_)
    * `Destination` (_This is the language you already know_)
    * `Tags` (_No spaces allowed, write "common_phrases" not "common phrases"_)  



4. To auto-translate your text, just write "x" in that column and the tool will translate for you.
    * For example, if I don't know the Spanish word for "Hello", I would write, "Hello" under `Destination` and _x_ under `Source`.


5. The tool will automatically translate the phrases, record the correct pronunciation and save an `.mp3` file for each phrase in the output folder.  It will also create a single .csv file to import into Anki.
The tool will automatically translate the phrases, record the correct pronunciation and save an .mp3 file for each phrase in the output folder.  It will also create a single .csv file to import into Anki.

6. After completing this process:
    * Bulk import the new audio files into Anki's library.
    * Bulk import the newly created .csv file to Anki, and Anki will generate a new notecard deck complete with audio files.


TODO:
* Improve download support
* Create automated method to import Anki data
