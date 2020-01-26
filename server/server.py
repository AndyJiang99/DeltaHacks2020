import os
import pandas as pd
import json

from flask import Flask
from flask_ngrok import run_with_ngrok
from flask import request

from google.cloud import language_v1
from google.cloud.language_v1 import enums


app = Flask(__name__)
run_with_ngrok(app)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/scheduleTasks', methods=['POST'])
def schedule():
    stringload = json.loads(request.form["values"])
    allEvents = stringload['events']['schedulable']
    # scheduler = Scheduler()
    # scheduler


    return(str(allEvents))


@app.route('/testSentiments', methods=['POST'])
def test():
    text_content = request.form["concatString"]
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\AndyJiang\Github\deltahacks2020-266223-a84fb8895002.json"

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful. I hate my life.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_sentiment(document, encoding_type=encoding_type)
    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(
        response.document_sentiment.score))
    print(
            u"Document sentiment magnitude: {}".format(
                    response.document_sentiment.magnitude
            )
    )
    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(u"Sentence sentiment magnitude: {}".format(
            sentence.sentiment.magnitude))

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    return(u"Language of the text: {}".format(response.language))


if __name__ == "__main__":
    app.run()
