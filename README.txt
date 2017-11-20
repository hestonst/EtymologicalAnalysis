A collection of scripts to analyze the etymological sources of text written in Python v3. 
Requires Stanford’s NLTK.

1) (Re)install the newest version of python3 from python.org

2) Integrate your system’s SSL certificates into the python environment by running the /Applications/Python 3.6/Install Certificates.command script

3) Install pip to the python3 installation on your Mac: 
sudo easy-install pip 

4) Install nltk
sudo pip3 install -U nltk


To pull the text from a Facebook user's historical data: 
EtymologyParser.readFromFacebook(namesArray, filepathIn, filePathOut)

5) Install nltk tools, which on MacOS requires accepting a SSL certificate:
python3 
Then install “stop words package from GUI”


e.g. If Facebook user Anthony Doe has formally had the name Tony Doe on Facebook, 
to collect all the text he personally wrote on 

names array : ["Tony Doe", “Anthony Doe“]
filepathIn: file path of the “messages” folder in his name
filePathOut: where to write the output file

if you want info on their friend that speaks another language: [“Alexei Nikolaievitch”, “Alex Nikolaievitch”] (all the names that that friend has ever gone by)

So in terminal, type: 

6) python3 

6a) cd to this folder 

7) import EtymologyParser

8) EtymologyParser.readFromFacebook(["Tony Doe", "Anthony Doe"], "/Users/username/Desktop/facebook-tonydoe/messages/", "output")
This step takes approx 2-5 mins.

9) EtymologyParser.parseWordsFromFacebook("output.bin", "output.txt")
Replace output.bin with whatever your third argument to EtymologyParser.readFromFacebook was, appending a .bin. 
This step takes 20-60 minutes. 



