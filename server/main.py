import json

from datetime import datetime, timedelta
from flask import Flask, jsonify
from flask_ngrok import run_with_ngrok
from flask import request

from google.cloud import language_v1
from google.cloud.language import enums
from google.cloud.language import types
from transformers.scheduler import Scheduler



app = Flask(__name__)
# run_with_ngrok(app)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/schedule-tasks', methods=['POST'])
def schedule():
    task_data = json.loads(request.form["values"])
    schedulable_events = task_data['events']['schedulable']
    for event in schedulable_events:
        event['deadline'] = datetime.fromisoformat(event['deadline'][:-1])
    scheduler = Scheduler()
    ordered_events = scheduler.create_optimized_ordering(schedulable_events)
    fixed_events = task_data['events']['fixed']
    for event in ordered_events:
        event['est_duration'] = timedelta(minutes=event['est_duration'])
    for event in fixed_events:
        event['start_time'] = datetime.fromisoformat(event['start_time'][:-1])
        event['end_time'] = datetime.fromisoformat(event['end_time'][:-1])
    final_schedule, unschedulable =\
        scheduler.determine_schedule(ordered_events, fixed_events,
                                     datetime.fromisoformat(task_data['cur_time'][:-1]))
    return jsonify(schedule=final_schedule, unschedulable=unschedulable)


@app.route('/testSentiments', methods=['POST'])
def test():
    text_content = request.form["concatString"]

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
    # return(u"Language of the text: {}".format(response.language))
    return(json.dumps({"sentiment": response.document_sentiment.score}))


if __name__ == "__main__":
    app.run()
