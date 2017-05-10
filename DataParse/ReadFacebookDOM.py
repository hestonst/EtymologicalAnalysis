import re
from html.entities import name2codepoint
import DetectLanguage

def readInfo(namesArray, filepath):
    """
    This function reads in the DOM created by Facebook and returns a list of
    Messages sent by any of the names in namesArray. Note: sometimes very long 
    names are shortened. Verify target name presence in DOM.
    @param namesArray The HTML (or XML) source text.
    @param filepath -- to the messages.htm provided by the facebook download.
    @return The plain text, as a Unicode string, if necessary.
    """
    file = open(filepath, "r")
    dom = file.read()
    dom = unescape(dom)
    file.close()

    regex = re.compile('<div class="message_header"><span class="user">[^<]*</span><span class="meta">[^<]*</span></div></div><p>[^<]*')
    listOfMessages = regex.findall(dom)

    regex = re.compile('<div class="message_header"><span class="user">[^<]*')
    regex2 = re.compile('<p>[^<]*')

    releventMessages = []
    for subDom in listOfMessages:
        name = regex.findall(subDom)[0][47:]
        message = regex2.findall(subDom)[0][3:]
        if (name in namesArray and DetectLanguage.detect_language(message) == "english"):
            releventMessages += [message]
    return releventMessages



def unescape(text):
    """
    Removes HTML or XML character references and entities from a text string.
    author: Fredrik Lundh
    source: http://effbot.org/zone/re-sub.htm#unescape-html
    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
