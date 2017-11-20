import urllib.request

germanicLanguages = {'Old English', 'Eastphalian', 'Limburgian',
'Lausitzisch-Neumärkisch', 'Brabantine', 'Alsatian', 'Germanic', 'Norwegian',
'Austro-bavarian', 'Stadsfries', 'Landsmål', 'Tirolean', 'German', 'Norse',
'Danish', 'Palatine', 'Swedish', 'Hessian', 'Hindeloopers',
'Afrikaans', 'Schiermonnikoogs', 'Proto-norse', 'Gutnish', 'Flemish',
'Prussian', 'Nynorsk', 'Riksmål', 'Frisian', 'Plautdietsch', 'Vandalic',
'Pomeranian', 'Vestlandsk', 'Aasters', 'Scandinavian',
'Trøndersk', 'Mócheno', 'Brandenburgisch', 'Saxon', 'Thuringian', 'Zeelandic',
'Dutch', 'Faroese', 'Scots', 'Westphalian', 'Wymysorys', 'Alemannic',
'Burgundian', 'Hollandic', 'Luxemburgish', 'Icelandic', 'Anglo-frisian',
'Fering', 'Gothic', 'Öömrang', 'Anglic', 'Cimbrian', 'Yiddish', 'Heligolandic',
'Franconian'}

latinateLanguages = {'Romanian', 'Latin', 'Proto-romanian', 'Proto-italian',
'Sardinian', 'Romance', 'Spanish', 'African romance', 'Balkan Romance',
'French', 'Portuguese', 'Eastern Romance', 'Italo-western', 'Occitano-Romance',
'Aromanian', 'Dalmatian', 'Gallo-Romance', 'Catalan', 'Italian',
'Ibero-Romance', 'Continental Romance', 'Occitan'}

otherLanguages = {'Tunisian', 'Gujarati', 'Deccan', 'Sanaani', 'Algerian',
'Polish', 'Pashto', 'Vietnamese', 'Farsi', 'Marathi', 'Haitian', 'Cebuano',
'Sinhala', 'Maithili', 'Belarusan', 'Mesopotamian', 'Malay', 'Sudanese',
'Madura', 'Hiligaynon', 'Egyptian', 'Yoruba', 'Levantine',
'Burmese', 'Hungarian', 'Chhattisgarhi', 'Ilocano', 'Xiang', 'Oriya',
'Indonesian', 'Nepali', 'Haryanvi', 'Somali', 'Mandarin',
'Calabrese', 'Chittagonian', 'Saraiki', 'Amharic', 'Croatian',
'Jinyu', 'Arabic', 'Tatar', 'Kurmanji', 'Thai', 'Malayalam', 'Creole',
'Nigerian', 'Bhojpuri', 'Malagasy', 'Kannada', 'Awadhi', 'Tagalog', 'Lombard',
'Hausa', 'Zhuang', 'Central', 'Czech', 'Uzbek', 'Russian', 'Khmer', 'Nan',
'Shona', 'Javanese', 'Panjabi', 'Sindhi', 'Bulgarian', 'Zulu', 'Wu',
'Chinese', 'Tamil', 'Bengali', 'Azerbaijani', 'Urdu', 'Magahi', 'Japanese',
'Kazakh', 'Hindi', 'Serbo', 'Igbo', 'Napoletano', 'Rwanda', 'Greek', 'Korean',
'Oromo', 'Moroccan', 'Ukrainian', 'Turkish', 'Persian'}

def scrapeEtymology(word):
    """
    Scrapes Etymology Information from the American Heritage Dictionary
    Returns snippet of HTML dom
    Example Output:
    <div class="etyseg">[Middle English, from<span> </span>Old French<span>
    </span><i>romans</i>, romance, work written in French, from<span>
    </span>Vulgar Latin<span> </span><i>*r<font face="Minion New">ō</font>m
    <font face="Minion New">ā</font>nic<font face="Minion New">ē</font>
    (scr<font face="Minion New">ī</font>bere)</i>, (to write) in the
    vernacular, from<span> </span>Latin<span> </span><i>R<font
    """
    etymInfo = ""
    beginning = "https://ahdictionary.com/word/search.html?q="
    request = urllib.request.Request(beginning+word)
    try:
        response = urllib.request.urlopen(request)
        thePage = response.read()
        # convert from bytes to utf-8
        theText = thePage.decode(errors="replace")
        # replaced with ?-esque char
        blockNdx = theText.find('<div class="etyseg">[')
        etymInfo = theText[blockNdx:blockNdx+400]
    except:
        print("Error: Connection to Server Cannot Be Established" \
              + " Scrapping Word: " + word)
    return etymInfo

def testLanguageGroup(etym, languageGroup):
    """
    Returns a set of the languages that are both in the provided etymology and
    the sets of languages defined above.
    etym -- etymology as snippet of HTML dom, typically produced by
    scrapeEtymology
    """
    retVal = set({})
    for language in languageGroup:
        if language in etym:
            retVal.add(language)
    return retVal

def resolveEtymology(word):
    """
    Example output:
    {'romance': {'Latin', 'French'}, 'germanic': {'Old English'},
        'other': set()}
    Corresponds to a word that has influence from two Romance languages,
    1 germanic, and no others
    """
    word = word.lower()
    etym = scrapeEtymology(word)
    dictionary = {'romance':testLanguageGroup(etym, latinateLanguages),
        'germanic':testLanguageGroup(etym, germanicLanguages),
        'other':testLanguageGroup(etym, otherLanguages)}
    return dictionary



def produceReport(setOfWords):
    """
    Scrapes each word in the setOfWords and returns a count of languages
    related to the sets' etymologies
    Parameters:
        setOfWords
    Sample Output for set({'help','butter','romance'}):
        {'germanic_Count': 2, 'total_Count': 5, 'germanic': {'Old English': 2},
        'romance': {'French': 1, 'Latin': 2}, 'romance_Count': 2,
        'other_Count': 1, 'other': {'Greek': 1}}
    """
    cumulativeEtymologyCountDict = {'germanic': {}, 'romance':{}, 'other':{},
        'germanic_Count': 0, 'romance_Count':0, 'other_Count': 0}

    def countLanguages(languageGroup, word, individualEtymologyCountDict):
        if len(individualEtymologyCountDict[languageGroup]) > 0:
            cumulativeEtymologyCountDict[languageGroup + "_Count"] += 1
            for language in individualEtymologyCountDict[languageGroup]:
                if language in cumulativeEtymologyCountDict[languageGroup]:
                    cumulativeEtymologyCountDict[languageGroup][language] += 1
                else:
                    cumulativeEtymologyCountDict[languageGroup][language] = 1

    for word in setOfWords:
        individualEtymologyCountDict = resolveEtymology(word)
        countLanguages('germanic', word, individualEtymologyCountDict)
        countLanguages('romance', word, individualEtymologyCountDict)
        countLanguages('other', word, individualEtymologyCountDict)

    cumulativeEtymologyCountDict['total_Count'] = \
        cumulativeEtymologyCountDict['germanic_Count'] \
        + cumulativeEtymologyCountDict['other_Count'] \
        + cumulativeEtymologyCountDict['romance_Count']
    return cumulativeEtymologyCountDict
