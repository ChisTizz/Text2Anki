from config import *
import csv, sys, re, genanki, docx
import translators as ts
from langdetect import detect


def main():
    # check user input arguments
    validate('csv', 'txt', 'docx') # if error: sys.exit with error message
    input_file_name = inputfile_path + sys.argv[1]
    if not file_exists(input_file_name):
        sys.exit(f'Could not find {filename}')

    # set vars for file format
    file_extension = input_file_name.rsplit('.',1)[-1].lower()
    global deck_name #required to aviod error when assigning deck_name a new value
    global lang

    # set deck name based on config setting
    if len(sys.argv) == 3:
        deck_name = sys.argv[2]

    # open file and read content (dictReader)
    # create dict with translations and tags
    # different func for each file ext
    if file_extension == 'csv':
        notes = readout_csv(input_file_name)
    elif file_extension == 'txt':
        notes = readout_txt(input_file_name, card_mode)
    elif file_extension == 'docx':
        notes = readout_docx(input_file_name, card_mode)

    # add translation based on config setting for dest and translation service
    add_translations(notes, translator)

    # add tags to notes based on config setting
    if tag_propagation:
        add_tag_propagation(notes)

    # print notes for user feedback
    print(notes)
    if len(notes) == 0:
        sys.exit('Error: Input did not create any notes!')

    # creat str for language detection
    text = ""
    for note in notes:
        text = text + note['Front']

    # create anki model with card layout depending on detected language
    if not lang:
        try:
            lang = detect(text)
        except:
            print('Language could not be detected by langdetect modul!')
        else: print(f'detected language code: {lang}')
    print(f'using {lang} for TTS selection')
    print(f'translated to language code: {dest}')
    if not audio_off:
        if lang not in ["en","es","fr","it","de","ja","zh-cn"]:
            print(f'TTS audio is not implemented for {lang}')
            my_model = create_anki_model()
        else:
            match lang:
                # matching implemented card templates to include correct TTS tag
                case 'en': my_model = create_anki_model_en()
                case 'es': my_model = create_anki_model_es()
                case 'fr': my_model = create_anki_model_fr()
                case 'it': my_model = create_anki_model_it()
                case 'de': my_model = create_anki_model_de()
                case 'ja': my_model = create_anki_model_ja()
                case 'zh-cn': my_model = create_anki_model_zh()
    else: my_model = create_anki_model()


    anki_deck = create_anki_deck(deck_name, deck_id, notes, my_model)
    print(f'created {len(notes)} note/s with card mode={card_mode}')

    # export anki deck as APKG file
    genanki.Package(anki_deck).write_to_file(f'{outputfile_path}{deck_name}.apkg')
    print(f'created output: {outputfile_path}{deck_name}.apkg')


# opens input file and reads content (dictReader)
# returns list of dicts with 'Front', 'Back' and 'Tags' as keys
def readout_csv(file):
    notes = []
    with open(file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            notes.append({'Front':row['Front'],'Back':row['Back'], 'Tags':row['Tags'].split()})
    return notes


def readout_docx(file, mode):
    notes = []
    reader = docx.Document(file)
    match mode:
        case 0:
            for row in reader.paragraphs:
                text = row.text.split('#',maxsplit=1)[0].strip()
                if len(row.text.split('#',maxsplit=1)) > 1: tags = row.text.split('#',maxsplit=1)[-1].strip()
                else: tags = ''
                notes.append({'Front':text,'Back':'', 'Tags':tags.split()})
        case 1:
            tags = input('Tags (separated by space): ')
            for p in reader.paragraphs:
                notes.append(p.text)
            notes = '\n'.join(notes)

            #match all sentences in text
            sentence_pattern = re.compile(r'[^。！？.!?|\n]*[。！？.!?|\n]')
            matches = sentence_pattern.findall(notes)

            notes = []
            for match in matches:
                if not match.strip() in ['','\n',',']:
                    notes.append({'Front':match.strip(),'Back':'', 'Tags':tags.split()})
        case 2:
            tags = input('Tags (separated by space): ')
            for p in reader.paragraphs:
                notes.append(p.text)
            notes = '\n'.join(notes)

            #match all words in text
            matches = re.findall(r'\b[a-zA-Z0-9]+\b', notes)   # matches single words in western languages
            notes = []
            word_set = set()
            for match in matches:
                if not match.strip() in word_set:   # to avoid word dulicates
                    word_set.add(match.strip())
                    if not match.strip() in ['','\n',',']:  # to avoid empty cards
                        notes.append({'Front':match.strip(),'Back':'', 'Tags':tags.split()})
    return notes


def readout_txt(file, mode):
    notes = []
    match mode:
        case 0:
            with open(file, encoding='utf-8') as f:
                reader = f.readlines()
                for row in reader:
                    text = row.split('#',maxsplit=1)[0].strip()
                    if len(row.split('#',maxsplit=1)) > 1: tags = row.split('#',maxsplit=1)[-1].strip()
                    else: tags = ''
                    notes.append({'Front':text,'Back':'', 'Tags':tags.split()})
        case 1:
            tags = input('Tags (separated by space): ')
            with open(file, encoding='utf-8') as f:
                reader = f.read()

                #split text into sentences
                sentence_pattern = re.compile(r'[^。！？.!?|\n]*[。！？.!?|\n]')
                matches = sentence_pattern.findall(reader)

                notes = []
                for match in matches:
                    if not match.strip() in ['','\n',',']:
                        notes.append({'Front':match.strip(),'Back':'', 'Tags':tags.split()})
        case 2:
            tags = input('Tags (separated by space): ')
            with open(file, encoding='utf-8') as f:
                reader = f.read()

                #match all words in text
                matches = re.findall(r'\b[a-zA-Z0-9]+\b', reader)   # matches single words in western languages
                notes = []
                word_set = set()
                for match in matches:
                    if not match.strip() in word_set:    # to avoid word dulicates
                        word_set.add(match.strip())
                        if not match.strip() in ['','\n',',']:  # to avoid empty cards
                            notes.append({'Front':match.strip(),'Back':'', 'Tags':tags.split()})
    return notes


# adds translations to 'Back' of notes if no values is present using translators module
def add_translations(notes, translator):
    for note in notes:
        if not note['Back']:
            note['Back'] = ts.translate_text(note['Front'], translator, to_language=dest)


#if one or more tags are found in note['Tags'], they will be applied to all following notes until another tag or only "#" is found, which is earsed
def add_tag_propagation(notes):
    prop = ''
    for note in notes:
        if '#' in note['Tags']: prop, note['Tags']  = '', []
        elif note['Tags']: prop = note['Tags']
        else:
            if prop: note['Tags'] = prop
    return notes


def create_anki_model():
    # define model with fields and template based on config
    my_model = genanki.Model(
  2104038997,
  'Simple Model',
  fields=[
    {'name': 'Front'},
    {'name': 'Back'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Back}}<br><br><br>{{Tags}}',
    },
  ],
  css= """
.card {
 font-family: times;
 font-size: 30px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color:Lavender }
""")
    return my_model


def create_anki_model_en():
    # define model with regular fields and add template based on config.py
    my_model = genanki.Model(
  2104138997,
  'Simple Model',
  fields=[
    {'name': 'Front'},
    {'name': 'Back'},
  ],
  templates=[
    {
      'name': '{{en TTS Card',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Back}}<br>{{tts en_US voices=AwesomeTTS:Front}}<br><br>{{Tags}}',
    },
  ],
  css= """
.card {
 font-family: times;
 font-size: 30px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color:Lavender }
""")
    return my_model


def create_anki_model_es():
    # define model with fields and template based on config
    my_model = genanki.Model(
  2104238997,
  'Simple Model',
  fields=[
    {'name': 'Front'},
    {'name': 'Back'},
  ],
  templates=[
    {
      'name': 'es TTS Card',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Back}}<br>{{tts es_ES voices=AwesomeTTS:Front}}<br><br>{{Tags}}',
    },
  ],
  css= """
.card {
 font-family: times;
 font-size: 30px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color:Lavender }
""")
    return my_model


def create_anki_model_fr():
    # define model with fields and template based on config
    my_model = genanki.Model(
  2104338997,
  'Simple Model',
  fields=[
    {'name': 'Front'},
    {'name': 'Back'},
  ],
  templates=[
    {
      'name': 'fr TTS Card',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Back}}<br>{{tts fr_Fr voices=AwesomeTTS:Front}}<br><br>{{Tags}}',
    },
  ],
  css= """
.card {
 font-family: times;
 font-size: 30px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color:Lavender }
""")
    return my_model


def create_anki_model_it():
    # define model with fields and template based on config
    my_model = genanki.Model(
  2104438997,
  'Simple Model',
  fields=[
    {'name': 'Front'},
    {'name': 'Back'},
  ],
  templates=[
    {
      'name': 'it TTS Card',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Back}}<br>{{tts it_IT voices=AwesomeTTS:Front}}<br><br>{{Tags}}',
    },
  ],
  css= """
.card {
 font-family: times;
 font-size: 30px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color:Lavender }
""")
    return my_model


def create_anki_model_de():
    # define model with fields and template based on config
    my_model = genanki.Model(
  2104538997,
  'Simple Model',
  fields=[
    {'name': 'Front'},
    {'name': 'Back'},
  ],
  templates=[
    {
      'name': 'de TTS Card',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Back}}<br>{{tts de_DE voices=AwesomeTTS:Front}}<br><br>{{Tags}}',
    },
  ],
  css= """
.card {
 font-family: times;
 font-size: 30px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color:Lavender }
""")
    return my_model


def create_anki_model_ja():
    # define model with fields and template based on config
    my_model = genanki.Model(
  2104638997,
  'Simple Model',
  fields=[
    {'name': 'Front'},
    {'name': 'Back'},
  ],
  templates=[
    {
      'name': 'ja TTS Card',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Back}}<br>{{tts ja_JP voices=AwesomeTTS:Front}}<br><br>{{Tags}}',
    },
  ],
  css= """
.card {
 font-family: times;
 font-size: 30px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color:Lavender }
"""
  )
    return my_model


def create_anki_model_zh():
    # define model with fields and template based on config
    my_model = genanki.Model(
  2104738997,
  'Simple Model',
  fields=[
    {'name': 'Front'},
    {'name': 'Back'},
  ],
  templates=[
    {
      'name': 'zh TTS Card',
      'qfmt': '{{Front}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Back}}<br>{{tts zh-CN voices=AwesomeTTS:Front}}<br><br>{{Tags}}',
    },
  ],
  css= """
.card {
 font-family: times;
 font-size: 30px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color:Lavender }
""")
    return my_model


def create_anki_deck(deck_name, deck_id, notes, my_model):
    # for each note in notes create a anki_note and add to anki_deck
    anki_deck = genanki.Deck(deck_id, deck_name)
    for note in notes:
        anki_note = genanki.Note(model=my_model, fields=[note['Front'], note['Back']], tags = note['Tags'])
        anki_deck.add_note(anki_note)
    return anki_deck


def validate(*ext):
    # 1 to 2 inline commands
    # argv[1] ends with allowed file-extensions
    # argv[1] file can be opened
    if prompt := bad_args([2,3], ext):
        sys.exit(prompt)


# validates if number of inline commands is in list n
# validates if argv[1] ends with str in *ext
# returns False if no error
# returns Error message as prompt, if error
def bad_args(n, ext):
    prompt = ''
    if len(sys.argv) < n[0]:
        prompt = 'no file name specified'
    elif len(sys.argv) > n[-1]:
        prompt = 'Too many command-line arguments'
    elif not sys.argv[1].rsplit('.',1)[-1].lower() in ext:
       prompt = f"First argument not a {','.join(ext[0:-1])} or {ext[-1]} file"
    else:
        return False
    return prompt


# validates if inputfile exists by opening and closing
# returns True if file can be opened
# returns False if file not found
def file_exists(filename):
    try:
        file = open(filename)
    except FileNotFoundError:
        return False
    else:
        file.close()
        return True


if __name__=="__main__":
    main()
