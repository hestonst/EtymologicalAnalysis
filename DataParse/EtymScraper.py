import urllib.request

def scrapeEtymology(word):
        """
            This function scrapes the entry for a word from the American
            heritage dictionary and uses regex to isolate the etymology
            information. 
        """
    beginning = "https://ahdictionary.com/word/search.html?q="
    end = "&submit.x=0&submit.y=0"
    request = urllib.request.Request(beginning+word+end)
    try:
        response = urllib.request.urlopen(request)
        thePage = response.read()
        # convert from bytes to utf-8
        theText = thePage.decode(errors="replace")
        # replaced with ?-esque char
    except:
        print("Error: Connection to Server Cannot Be Established")
    blockNdx = theText.find('<div class="etyseg">[')
    etymInfo = theText[blockNdx:blockNdx+400]
    print(etymInfo)

scrapeEtymology('sdafs')
