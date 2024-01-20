from project import readout_csv
from project import add_tag_propagation
from project import readout_docx
from project import readout_txt


test_csv1 = [{'Front':'Spass haben und Spass machen sind nicht das Gleiche',
            'Back':'Having fun and having fun are not the same thing',
            'Tags':['DummerSpruch']},
            {'Front':'Unterm Fernsehturm kacken die Tauben',
            'Back':'The pigeons poop under the television tower',
            'Tags':[]},
            {'Front':'Tote Oma mit Sauerkraut ist mein Lieblingsgericht',
            'Back':'Dead grandma with sauerkraut is my favorite dish',
            'Tags':[]}]

test_csv2 = [{'Front':'Spass haben und Spass machen sind nicht das Gleiche',
            'Back':'Having fun and having fun are not the same thing',
            'Tags':['DummerSpruch']},
            {'Front':'Unterm Fernsehturm kacken die Tauben',
            'Back':'The pigeons poop under the television tower',
            'Tags':['DummerSpruch']},
            {'Front':'Tote Oma mit Sauerkraut ist mein Lieblingsgericht',
            'Back':'Dead grandma with sauerkraut is my favorite dish',
            'Tags':['DummerSpruch']}]

def test_readout_csv():
    assert readout_csv('./input/test.csv') == test_csv1


def test_add_tag_propagation():
    assert add_tag_propagation(test_csv1) == test_csv2
