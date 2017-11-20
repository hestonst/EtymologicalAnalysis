import EtymTagger
import pickle
from nltk import pos_tag, word_tokenize


def readNPSChat(filePathOut):
    """
    Reads from the corpus of text developped by the US government
    for online monitoring, available through the nltk library
    Parameters:
        filePathOut - the location to write output
    """
    from nltk.corpus import nps_chat
    chatroom = nps_chat.posts()
    wordList = []
    for l in chatroom[1:4256]:
        wordList += l
    for l in chatroom[4259:]:
        wordList += l
    # los miembros 4257 y 4258 continen caracteres inválidos
    messages = [" ".join(wordList)]
    parseEtymologies(messages, filePathOut)

def readFromNLTKCorpusNPSChat(category, filePathOut):
    """
    Reads from the corpus of text developped by the US government
    for online monitoring, available through the nltk library
    Parameters:
        category - for example, "news", "learned"
        see http://www.nltk.org/book/ch02.html
        filePathOut - the location to write output
    """
    from nltk.corpus import brown
    wordList = brown.words(categories=category)[1:5000]
    parseEtymologies(wordList, filePathOut)



def readFromFacebook(namesArray, filepathIn, filePathOut):
    """
    Reads from the htm output by facebook specified. Returns a list of strings
    corresponding to different messages sent by the facebook users in
    namesArray.
    Parameters:
        namesArray - names of FB users
        filepath - the location of the facebook message .htm
    """
    import ReadFacebookDOM
    allMessages = ReadFacebookDOM.readInfo(namesArray, filepathIn)
    with open(filePathOut+".bin", "wb") as f:
        pickle.dump(allMessages, f, pickle.HIGHEST_PROTOCOL)
        f.close()


def parseWordsFromFacebook(fileOfAllMessages,filePathOut):
    with open(fileOfAllMessages, "rb") as f:
        allMessages = pickle.load(f)
        parseEtymologies(allMessages, filePathOut)

def readFromTXT(filepathIn, filePathOut):
    """
    Reads from a txt file. Returns a list of strings
    corresponding to lines in the .txt
    Parameters:
        filepath - the location of the facebook message .htm
    """
    fileIn = open(filepathIn,'r')
    allMessages = []
    for line in fileIn:
        allMessages += [line]
    parseEtymologies(allMessages,filePathOut)

def parseEtymologies(listOfMessages, filePathOut):
    """
    Produces a count of different etymologies in the given messages.
    Prints and saves output to output.txt
    Parameters:
        listOfMessages - the location of the facebook message .htm
    """
    outFile = open(filePathOut, 'w')
    
    print("Tagging and filtering unique relevent words from messages.")

    releventWordClasses = ["JJ", "NN", "NNS", "RB", "VB", "VBP"]
    # nltk.help.upenn_tagset():
    # FW -foreign word
    # JJ: adjective or numeral, ordinal
    # JJR: adjective, comparative #not in etymology database
    # JJS: adjective, superlative #not in etymology database
    # NNP: noun, proper, singular #no proper nouns
    # NN: noun, common, singular or mass
    # NNS: noun, common, plural
    # RB: adverb
    # RBR: adverb, comparative
    # RBS: adverb, superlative
    # RP: particle
    # POS: genitive marker
    # VB: verb, base form
    # VBD: verb, past tense # present, but would give false negatives
    # VBG: verb, present participle or gerund # """"
    # VBN: verb, past participle # not in database
    # VBP: verb, present tense, not 3rd person singular
    # VBZ: verb, present tense, 3rd person singular  # not in database

    setOfWords = set({})
    wordCountInOriginalDocument = 0
    for message in listOfMessages:
        for word in word_tokenize(message):
            wordCountInOriginalDocument += 1
            if str(pos_tag([word])[0][1]) in releventWordClasses:
                setOfWords.add(word)
    print("Webscraping Etymologies")
    etymologyDict = EtymTagger.produceReport(setOfWords)

    for category in etymologyDict.keys():
        out = str(category) + "\t" + str(etymologyDict[category])
        outFile.write(str(out) + "\n")
    outFile.write("word_count_with_redundancies" + "\t" \
        + str(wordCountInOriginalDocument))
