import re
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

'''
def load_gloss_dict(path="latin_interlinear.json"):
    if not os.path.exists(path):
        print(f"Warning!!!!!!!! {path} not found, definitions will be empty")
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
'''

def load_full_dict(path="latin_gloss.json"):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_line(line):
    if not line.strip():
        return None

    parts = line.strip().split()
    if len(parts) < 2:
        return None

    lemma = parts[0]
    in_flags = True
    gloss_start = 0

    for i, part in enumerate(parts[1:], 1):
        if in_flags and len(part) > 2 and not part.isupper():
            gloss_start = i
            in_flags = False

    clean_gloss = ""

    if gloss_start > 0:
        gloss = " ".join(parts[gloss_start:])
        # Clean up: take first definition before semicolon
        first_def = gloss.split(';')[0].strip()
        # Remove parenthetical notes for inline gloss
        clean_gloss = re.sub(r'\([^)]*\)', '', first_def).strip()
    else:
        clean_gloss = lemma

    return {
        "lemma": lemma,
        "gloss": clean_gloss
    }

#GLOSS_DICT = load_gloss_dict()
FULL_DICT = load_full_dict()

GLOSS_DICT = {}

with open("dict2/DICTLINE.GEN", 'r') as f:
    for line in f:
        result = parse_line(line)
        if result:
            GLOSS_DICT[result['lemma'].lower()] = result['gloss']

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
    #TODO: refactor to just have it return a single word afsdhflksahflksahflkahklashfdlkjahfdas

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

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "result":"pong"
    })

@app.route("/break-it-down")
def breakItDown():
    # break it down tony
    # literally just copypasted code lmao im lazy tho
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

    if "text" not in data:
        print("No 'text' field in request!")
        return jsonify({"error": "Missing 'text' field"}), 400

    text = data["text"]
    return analyzeText(text)


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

def get_gloss(lemma):
    if lemma in GLOSS_DICT:
        return GLOSS_DICT[lemma]

    if lemma in FULL_DICT:
        glosses = FULL_DICT[lemma]
        if glosses:
            return glosses[0].split(';')[0].strip()

    return lemma

'''
def get_definition(lemma):
    #add dictionary lookup later astaghfirullah
    #return None
    lemma_lower = lemma.lower()

    if lemma_lower in FULL_DICT:
        return FULL_DICT[lemma_lower]

    if lemma_lower in GLOSS_DICT:
        gloss = GLOSS_DICT[lemma_lower]
        if isinstance(gloss, list):
            return gloss
        return [gloss]

    return []
'''


def get_definition(lemma) -> list:
    lemma_lower = lemma.lower()

    definitions = [get_gloss(lemma)]
    idkwhattonamethisvariable = []
    if lemma_lower in FULL_DICT:
        idkwhattonamethisvariable = FULL_DICT[lemma_lower]
    if isinstance(idkwhattonamethisvariable, list):
        definitions.append(idkwhattonamethisvariable)
        return definitions
    return definitions

if __name__ == '__main__':
    app.run(debug=True, port=6767)
    # print(analyzeText("inter lineas"))
