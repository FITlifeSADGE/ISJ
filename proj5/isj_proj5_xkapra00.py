#!/usr/bin/env python3


# Definujte funkci gen_quiz, která bude moci být volána se 4 parametry:
# qpool - seznam dvojic otázka a seznam odpovědí
# libovolný počet indexů do seznamu qpool
# altcodes - sekvence, přes kterou lze projít konstrukcí for a která vrací řetězce, jež se mají ve výsledku předřadit (spolu s ': ') před každou z odpovědí 
# quiz - vstupní podoba kvízu ve formě seznamu dvojic otázka a seznam formátovaných odpovědí.

# Pokud bude některý z indexů do seznamu qpool mimo rozsah, nebo nastane jiná chyba při zpracování konkrétního indexu, má se vypsat:
# Ignoring index <číslo> - <text výjimky>
# (poněkud nesmyslně na standardní výstup, nikoliv na standardní chybový výstup, aby fungoval doctest)

# Pokud bude sekvence altcodes kratší než seznam možných odpovědí v některém ze seznamů, dá se do výsledného kvízu pouze daný počet (lze využít konstrukci zip(altcodes, answers)). Defaultně jsou odpovědi označovány písmeny a je maximálně 6 možných odpovědí, tedy altcodes = 'ABCDEF')

# Pokud není zadána vstupní podoba kvízu, vytvoří se nový kvíz s položkami podle definovaných indexů. Defaultní hodnota je tedy prázdný kvíz.

# Cvičné hodnocení můžete vyzkoušet v systému http://isj.fit.vutbr.cz/upload, ale pro získání bodů za projekt musíte výsledný skript (se správným názvem) odevzdat prostřednictví WIS.

#Do kódu si můžete přidat testy (pro dokumentační komentář funkce):
from fnmatch import fnmatch
from hashlib import new


def gen_quiz(qpool, *index, altcodes='ABCDEF', quiz=None):
    """
    >>> test_qpool1 = [('Question1', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question2', ['Answer1', 'Answer2', 'Answer3']), ('Question3', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question4', ['Answer1', 'Answer2'])]
    >>> existing_quiz1 = [('ExistingQuestion1', ['1: Answer1', '2: Answer2', '3: Answer3']), ('ExistingQuestion2', ['1: Answer1', '2: Answer2'])]
    >>> gen_quiz(test_qpool1, -2, 0, altcodes = ('10', '20', '30'), quiz = existing_quiz1)
    [('ExistingQuestion1', ['1: Answer1', '2: Answer2', '3: Answer3']), ('ExistingQuestion2', ['1: Answer1', '2: Answer2']), ('Question3', ['10: Answer1', '20: Answer2', '30: Answer3']), ('Question1', ['10: Answer1', '20: Answer2', '30: Answer3'])]

    >>> test_qpool2 = [('Question1', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question2', ['Answer1', 'Answer2', 'Answer3']), ('Question3', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question4', ['Answer1', 'Answer2'])]
    >>> existing_quiz2 = [('ExistingQuestion1', ['1: Answer1', '2: Answer2', '3: Answer3']), ('ExistingQuestion2', ['1: Answer1', '2: Answer2'])]
    >>> not_used = gen_quiz(test_qpool2, -2, 0, altcodes = ('1', '2', '3'), quiz = existing_quiz2)
    >>> existing_quiz2
    [('ExistingQuestion1', ['1: Answer1', '2: Answer2', '3: Answer3']), ('ExistingQuestion2', ['1: Answer1', '2: Answer2']), ('Question3', ['1: Answer1', '2: Answer2', '3: Answer3']), ('Question1', ['1: Answer1', '2: Answer2', '3: Answer3'])]

    >>> test_qpool3 = [('Question1', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question2', ['Answer1', 'Answer2', 'Answer3']), ('Question3', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question4', ['Answer1', 'Answer2'])]
    >>> existing_quiz3 = [('ExistingQuestion1', ['1: Answer1', '2: Answer2', '3: Answer3']), ('ExistingQuestion2', ['1: Answer1', '2: Answer2'])]
    >>> not_used1 = gen_quiz(test_qpool3, 0, 2, altcodes = ('i', 'ii', 'iii'), quiz = existing_quiz3)
    >>> not_used2 = gen_quiz(test_qpool3, 1, altcodes = ('i', 'ii', 'iii'), quiz = existing_quiz3)
    >>> existing_quiz3
    [('ExistingQuestion1', ['1: Answer1', '2: Answer2', '3: Answer3']), ('ExistingQuestion2', ['1: Answer1', '2: Answer2']), ('Question1', ['i: Answer1', 'ii: Answer2', 'iii: Answer3']), ('Question3', ['i: Answer1', 'ii: Answer2', 'iii: Answer3']), ('Question2', ['i: Answer1', 'ii: Answer2', 'iii: Answer3'])]

    >>> test_qpool4 = [('Question1', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question2', ['Answer1', 'Answer2', 'Answer3']), ('Question3', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question4', ['Answer1', 'Answer2'])]
    >>> gen_quiz(test_qpool4, 0, 1, -1)
    [('Question1', ['A: Answer1', 'B: Answer2', 'C: Answer3', 'D: Answer4']), ('Question2', ['A: Answer1', 'B: Answer2', 'C: Answer3']), ('Question4', ['A: Answer1', 'B: Answer2'])]

    >>> test_qpool5 = [('Question1', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question2', ['Answer1', 'Answer2', 'Answer3']), ('Question3', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question4', ['Answer1', 'Answer2'])]
    >>> not_used = gen_quiz(test_qpool5, 0, altcodes = '123456')
    >>> gen_quiz(test_qpool5, 0, altcodes = '123456')
    [('Question1', ['1: Answer1', '2: Answer2', '3: Answer3', '4: Answer4'])]
    
    >>> test_qpool6 = [('Question1', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question2', ['Answer1', 'Answer2', 'Answer3']), ('Question3', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question4', ['Answer1', 'Answer2'])]
    >>> existing_quiz6 = [('ExistingQuestion1', ['1: Answer1', '2: Answer2', '3: Answer3']), ('ExistingQuestion2', ['1: Answer1', '2: Answer2'])]
    >>> gen_quiz(test_qpool6, quiz = existing_quiz6)
    [('ExistingQuestion1', ['1: Answer1', '2: Answer2', '3: Answer3']), ('ExistingQuestion2', ['1: Answer1', '2: Answer2'])]

    >>> test_qpool7 = [('Question1', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question2', ['Answer1', 'Answer2', 'Answer3']), ('Question3', ['Answer1', 'Answer2', 'Answer3', 'Answer4']), ('Question4', ['Answer1', 'Answer2'])]
    >>> gen_quiz(test_qpool7, 0, 4, 2, altcodes = ['101','201']) 
    Ignoring index 4 - list index out of range
    [('Question1', ['101: Answer1', '201: Answer2']), ('Question3', ['101: Answer1', '201: Answer2'])]
    """
    # Pokud bude některý z indexů do seznamu qpool mimo rozsah, nebo nastane jiná chyba při zpracování konkrétního indexu, má se vypsat:
    # Ignoring index <číslo> - <text výjimky>
    # (poněkud nesmyslně na standardní výstup, nikoliv na standardní chybový výstup, aby fungoval doctest)

    # Pokud bude sekvence altcodes kratší než seznam možných odpovědí v některém ze seznamů, dá se do výsledného kvízu pouze daný počet (lze využít konstrukci zip(altcodes, answers)). Defaultně jsou odpovědi označovány písmeny a je maximálně 6 možných odpovědí, tedy altcodes = 'ABCDEF')

    # Pokud není zadána vstupní podoba kvízu, vytvoří se nový kvíz s položkami podle definovaných indexů. Defaultní hodnota je tedy prázdný kvíz.
    
    if not quiz:
        quiz = []
    for ind in index:
        try:
            answers = qpool[ind]
        except IndexError as err:
            print('Ignoring index ' + str(ind) + ' - ' + str(err))
        else:
            answer_value = []
            values = answers[1] #answers
            questions = answers[0] #questions
            zipped = zip(altcodes, values)
            for altcode_answer in zipped:
                answer_value.append(altcode_answer[0] + ': ' + altcode_answer[1])
            new_quiz = (questions, answer_value)
            quiz.append(new_quiz)
        #finally:
    return quiz

if __name__ == "__main__":
    import doctest
    doctest.testmod()   
