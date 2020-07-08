from flask import Flask,render_template,request,jsonify
import requests
import json
from logging.handlers import RotatingFileHandler
import nltk
from nltk.corpus import wordnet as wn


#Flask object

app=Flask(__name__,
template_folder="client/template",
static_folder="client/static")

#error handling object
file_handler = RotatingFileHandler("error.log", maxBytes=1024 * 1024 * 100)
app.logger.addHandler(file_handler)

#load json file here
with open("extract_word.json", "r") as read_file:
    word_in_sentence= json.load(read_file)

   

#function to print sentence
def print_sentence(word):
        if word in word_in_sentence:
            return (wn.synsets(word)[0].examples())
        else:
            msg=["cannot find example sentence for this word"]
            return msg   


#error handlers
#1
@app.errorhandler(500)
def handle_500_error(exception):
    app.logger.error(exception)
    return "Internal Server Error"
#2
@app.errorhandler(404)
def handle_404_error(exception):
    app.logger.error(exception)
    return "Not Found"


                    
#root page 
@app.route("/")
def home_html():
    print("html page printed sucessfully..!")
    return render_template("english_bot.html")

#function for api
@app.route("/api/get_sentence",methods =['GET'])
def word_present_sentence():
    word_sentence = request.args.get("word")
    print("got sentence for corresponding given word")
    word_for_sentence = print_sentence(word_sentence)
    return jsonify(word_for_sentence)


if __name__ == '__main__':
    app.run(port=5000)