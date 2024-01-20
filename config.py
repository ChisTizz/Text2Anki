"""
-----------------------------------------------------------
Explanations:
deck_name       : output deck name, please change it to your prefered deck name
deck_id         : unique Anki deck ID, it's strongly recommended to use a dedicated config.py with a unique deck_id and deck_name for each deck
inputfile_path  : folder path of input file
outputfile_path : folder path of output file
card_mode       : csv files will only use mode 0: each line is a card. Modes 1 and 2 offer additional control  for docx or txt input files: 1: each sentence is a card, 2: each word is a card (only works for western languages)
lang            : if the language detection does not work, the lang can be set here, to assign the correct TTS layout
dest            : specifies the language to translate to (Default="en", see also https://pypi.org/project/translators/)
translator      : translation service (Default="bing", see also https://pypi.org/project/translators/)
audio_off       : disables audio (Default=False)
tag_propagation : if one or more tags are found, they will be applied to all following notes until another tag or only "#" is found (Default=True)
-----------------------------------------------------------
Below you can configure the anki deck generation parameters:
"""
deck_name="deckname"
deck_id=2092731102
inputfile_path="./input/"
outputfile_path="./output/"
card_mode=0
lang=""
dest="en"
translator="bing"
audio_off=False
tag_propagation=True
