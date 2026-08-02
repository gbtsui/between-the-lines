import spacy
import sys
import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import hmac
from dotenv import load_dotenv


nlp = spacy.load("la_core_web_lg")


#doc = nlp("haec narrantur a poetis de perseo")

#for token in doc:
#    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#            token.shape_, token.is_alpha, token.is_stop)

app = Flask(__name__)
CORS(app)


def verify_secret(incoming_secret: str) -> bool:
    expected_secret = os.getenv("SILLYMAXXED_INTERNAL_SERVER_SECRET")

    if not expected_secret:
        raise ValueError("CLIENT_SECRET environment variable is missing!")
    return hmac.compare_digest(incoming_secret, expected_secret)


@app.route('/testWord', methods=['POST'])

def testWord():
    #print("testWord called")
    #text = request.json["text"]
    #print("text:", text)

    silly_secret: str = request.headers.get("Secret")
    print("silly_secret: ", silly_secret)
    if not silly_secret:
        return jsonify({"error": "Unauthorized, No Secret"}), 401


    verified = verify_secret(silly_secret)
    if not verified:
        return jsonify({"error": "Unauthorized"}), 401

    if not request.is_json:
            print("Request is not JSON!")
            return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    #print("parsed data: ", data)

    if "text" not in data:
        print("No 'text' field in request!")
        return jsonify({"error": "Missing 'text' field"}), 400

    text = data["text"]
    #print("text: ", text)
    return analyzeText(text)

def ping():
    return jsonify({
        "result":"pong"
    })

def analyzeText(text):
    print("running AnalyzeText")
    doc = nlp(text)
    words = []

    for token in doc:
        words.append({
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "morph": str(token.morph),
            "shape": token.shape_,
            "head": token.head.i,  # index of parent word
            "definition": get_definition(token.lemma_)
        })

    #print(words)

    return jsonify({
        "words": words,
        "sentence": text
    })

def get_definition(lemma):
    #add dictionary lookup later astaghfirullah
    return None

if __name__ == '__main__':
    app.run(debug=True, port=6767)
    # print(analyzeText("inter lineas"))
