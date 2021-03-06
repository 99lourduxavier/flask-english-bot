import re
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import requests
import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from word_forms.word_forms import get_word_forms
import string
import argparse


#usage message
def msg():
    message='''You failed to provide required files.\nYou must provide it as input on command line'''
    return message

#argparse object
parser = argparse.ArgumentParser(usage=msg())
parser.add_argument("file",metavar="english.csv",nargs=1)
args = parser.parse_args()




# to add all sentences
all_common_english_sentence = set()

count = 0
# 2
# 4
# function to extract sentence


def extract_sentence(url):
    # parsing html and getting clear text from it
    words_set = set()
    req = Request(str(url), headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urlopen(req).read()
    #html = urllib.request.urlopen(str(url))
        soup = BeautifulSoup(html, features="lxml")
        data = soup.findAll(text=True)

        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                return False
            return True
        result = filter(visible, data)
        list_to_str = ' '.join([str(element) for element in list(result)])

    # sentence tokenizing the clear text
        sent = nltk.sent_tokenize(list_to_str)
     # operations to extract words
        for item in sent:
            tokens = nltk.word_tokenize(item)
        # removing punctuation
            table = str.maketrans('', '', string.punctuation)
            stripped = [word.translate(table) for word in tokens]
        # taking only alphabet
            words = [word for word in stripped if word.isalpha()]
            for word in words:
                word = ''.join([char for char in word if not char.isdigit()])
                # removing hexadecimal
                word = re.sub(r'[^\x00-\x7f]', r'', word)
                if len(word) >= 1:
                    words_set.add(str(word.casefold()))
                # to get different form of a word
                    word_form = get_word_forms(word)
                    for item in word_form.values():
                        for inner_item in item:
                            words_set.add(str(inner_item.casefold()))
        return words_set

    except:
        with open('unavailable_url.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([count])
            writer.writerow([url])
        return set("page " + str(count) + " not available")


# 1
# for getting url from csv file

fname = args.file[0]
with open(fname, 'rt')as urls:
    url = csv.reader(urls)
    for item in url:
        for data in item:
            count += 1
            print("parsing link "+str(count))
            # passing one url at a time from link.csv file
            all_common_english_sentence.update(extract_sentence(data))

#dump into json object
json_object = json.dumps(list(all_common_english_sentence))
with open("extract_word.json", "w") as outfile: 
    outfile.write(json_object) 

print("extract_word.json created successfully..!")