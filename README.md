# Text2Anki
## Video Demo:  <https://youtu.be/t6BR9YNSrkA>
## Description:

**Automatically create effective Anki flash-cards from a varity of input files to kick-start your language studies!**

Designed for effordless creation of hundreds of cards from ***docx***, ***txt*** or ***csv*** files, containing just a list of phrases in your target language. Safe time by letting this program take care of adding translations and audio to your cards. All you need to do, is simply to upload the ***apkg*** output to Anki.

The auto-translation allows almost any language as input and output, making this script highly flexible. Audio is provided by using Anki's text-to-speech feature.

> AwesomeTTS's Text-To-Speech feature requires Anki 2.1.(see Link below). AnkiWeb and AnkiDroid do not currently support this method. Also Text2Anki itself supports TTS only for English, Spanish, French, Italian, German, Japanese and Chinese out-of-box. Fortunately, AwesomeTTS's Add-on allows to add TTS for most languages after importing a deck with Text2Anki!

## Requirements:
- Python modules:
    - [translators](https://pypi.org/project/translators/) (installation: `pip install translators`)
    - [genanki](https://pypi.org/project/genanki/) (installation: `pip install genanki`)
    - [langdetect](https://pypi.org/project/langdetect/) (installation: `pip install langdetect`)
- 3rd party applications: Anki (download: https://apps.ankiweb.net/) with Add-on [AwesomeTTS](https://ankiweb.net/shared/info/1436550454) installed
- Internet connection for translators API

## Usage:
> For ***docx*** files as input, the program will create a note from each single line, which will become the Front of the card. The auto-translation of the Front will constitute the Back of the card. Tags can be included at the end of each line by adding `# tag1 tag2 ...` (the `#` character is only required before the first tag, also no spaces are allowed within a tag).

> For ***txt*** files as input, the program will create a note from each single line, which will become the Front of the card. The auto-translation of the Front will constitute the Back of the card. Similar to above, tags can be included at the end of each line by adding `# tag1 tag2 ...` (the `#` character is only required before the first tag, also no spaces are allowed within a tag).

> For ***csv*** files as input, the first row of your table needs to be filled in with `Front`, `Back` and `Tags`, respectively, in columns A to C. When saving from an Excel workbook, use *CSV UTF-8 (Comma delimited)* .csv-format.
>
> Under `Front`, fill in the list of words or phrases of the target language, which will be shown on the front of the card.
>
> `Back` column: if left empty, the auto-translation will add a translation for each phrase. If instead you like to use your own translations, fill them in under `Back`, which will override the auto-translation.
>
> `Tags` column: one or more tags can be entered here by adding `tag1 tag2 ...` (no spaces are allowed within a tag).

#### Steps:

1. It's recommended to define at least the desired deck name in `config.py` before creating a deck, e.g.: `deck_name="Japanese Phrases"`. If left unchanged, the created deck will be named just *output*. Please check the explanations in `config.py` for further details.
2. Execute `text2anki.py` followed by the *inputfile-name* and optional *deck-name*:

    `python text2anki.py inputfile-name [opt.: deck-name]`

3. The final deck is then written to the specified output folder as `deck_name`.apk and can be simply uploaded to the anki application by double-clicking or using the import function of Anki. All imported decks will add new cards to the same deck in your Anki collection, unless the card already exits. If you want to create multiple decks, you need to change `deck_name` and `deck_id` before executing `text2anki.py`.

## Program files:
```
text2anki.py
```
- Contains main program with logic and all subfunctions.
- Subfunctions:
    - **validate(*\*ext*)**: Takes a list of supported extensions-strings and returns *True* if user input is valid.
    - **readout_*XXX*(*file_name*)**: Depending on the input file extention there is a corresponding readout function with the extension in place of *XXX*. It reads the content of the input file provided and returns a list of dicts with the keys `Front`, `Back` and `Tags`.
    - **add_translations(*list_of_dicts*)**: Takes return value of the readout function and returns a list of dicts with missing translations added to field `Back`.
    - **add_tag_propagation(*list_of_dicts*)**: Takes and returns a list of dicts which is modifyied by copying any tags in field `Tags` to subsequent list records.
    - **create_anki_model*XXX*()**: defines the Anki deck model with a card layout based on the detected language and config.py audio settings. Each setting requires it's own version.
    - **create_anki_deck(*deck_name, list_of_dicts, anki_model*)**: takes a deck name, a Anki deck model and a list of dicts to return an Anki deck.
```
config.py
```
- Contains all customizations to allow easy switch of configurations by just swapping this file (see Usage section)
- Is made up of a list of variables accompanied with explanatory comments.
- The main program loads all variables as *global* variables.
