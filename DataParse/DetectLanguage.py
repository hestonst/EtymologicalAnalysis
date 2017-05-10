# Author: Alejandro Nolla - z0mbiehunt3r
# Source: http://blog.alejandronolla.com/2013/05/15/detecting-text-language-with-python-and-nltk/
# Purpose: Example for detecting language using a stopwords based approach
# Created: 15/05/13

from nltk import wordpunct_tokenize
from nltk.corpus import stopwords


#----------------------------------------------------------------------
def _calculate_languages_ratios(text):
    """
    Calculate probability of given text to be written in several languages and
    return a dictionary that looks like {'french': 2, 'spanish': 4, 'english': 0}

    @param text: Text whose language want to be detected
    @type text: str

    @return: Dictionary with languages and unique stopwords seen in analyzed text
    @rtype: dict
    """

    languages_ratios = {}

    '''
    nltk.wordpunct_tokenize() splits all punctuations into separate tokens

    >>> wordpunct_tokenize("That's thirty minutes away. I'll be there in ten.")
    ['That', "'", 's', 'thirty', 'minutes', 'away', '.', 'I', "'", 'll', 'be', 'there', 'in', 'ten', '.']
    '''

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements) # language "score"

    return languages_ratios


#----------------------------------------------------------------------
def detect_language(text):
    """
    Calculate probability of given text to be written in several languages and
    return the highest scored.

    It uses a stopwords based approach, counting how many unique stopwords
    are seen in analyzed text.

    @param text: Text of language we want to be detected
    @type text: str

    @return: Most scored language guessed
    @rtype: str
    """

    ratios = _calculate_languages_ratios(text)

    most_rated_language = max(ratios, key=ratios.get)

    return most_rated_language



def unit_test_detect_language():
    """
    unit test to text funtionality over 6 languages.
    author: Thomas Heston
    """

    russian = '''
    Вот пример какого-то русского текста.
    '''
    french = '''
    Voici un example d'un texte en français.
    '''
    portuguese = '''
    Aqui está um exemplo dum texto em português.
    '''
    german = '''
    Hier ist ein Beispiel für einen Text auf Deutsch.
    '''
    spanish = '''
    Aquí hay un ejemplo de texto en castellano.
    '''
    english = '''
    Here is an example of text in English.
    '''

    print(detect_language(russian) + " text is Russian")
    print(detect_language(french) + " text is French")
    print(detect_language(portuguese) + " text is Portuguese")
    print(detect_language(spanish) + " text is Spanish")
    print(detect_language(german) + " text is German")
    print(detect_language(english) + " text is English")
