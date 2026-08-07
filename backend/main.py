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
    """Parse Whitaker's DICTLINE.GEN format - fixed column version"""
    if not line.strip() or line.startswith('#'):
        return None

    line = line.rstrip()
    if not line:
        return None

    parts = line.split()
    if len(parts) < 5:
        return None

    lemma = parts[0].lower()

    # The format is:
    # LEMMA STEM PERF PARTICIPLE POS DECL/CONJ GENDER FLAGS GLOSS
    #
    # After the lemma, there are optional stem/perfect/participle fields,
    # then POS type (N, V, ADJ, PREP, etc.), then declension info,
    # then single-char flag columns, then the gloss.
    #
    # The flag columns are single characters (X, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, Y, Z, .)
    # They appear as: X X X A O (5 single-char flags with spaces between)

    # Find where the flag columns end and the gloss begins
    # Strategy: scan for a pattern of 3-6 single-char tokens in a row
    gloss_start = None

    for i in range(1, len(parts)):
        # Check if current position starts a sequence of single-char flags
        if len(parts[i]) == 1 and parts[i].isalpha() or parts[i] in ['.', 'X']:
            # Count consecutive single-char tokens
            flag_count = 0
            j = i
            while j < len(parts) and (len(parts[j]) == 1 or parts[j] == '.'):
                flag_count += 1
                j += 1

            # If we found 3 or more consecutive single chars, we've found the flag block
            if flag_count >= 3:
                gloss_start = j
                break

    if gloss_start is None or gloss_start >= len(parts):
        return None

    # Everything from gloss_start onwards is the definition
    gloss = ' '.join(parts[gloss_start:])

    # Clean up
    # Remove bracket notes first (they clutter the inline gloss)
    gloss = re.sub(r'\[.*?\]', '', gloss)
    # Take first definition before semicolon
    gloss = gloss.split(';')[0].strip()
    # Remove parenthetical notes
    gloss = re.sub(r'\([^)]*\)', '', gloss).strip()
    # Remove leading pipe (alternate definition marker)
    gloss = gloss.lstrip('|').strip()

    if len(gloss) < 2:
        return None

    return {
        "lemma": lemma,
        "gloss": gloss
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

@app.route("/break-it-down", methods=["POST"])
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
    """Get clean single gloss for interlinear display"""
    lemma_lower = lemma.lower()

    if lemma_lower in GLOSS_DICT:
        return GLOSS_DICT[lemma_lower]

    if lemma_lower in FULL_DICT:
        glosses = FULL_DICT[lemma_lower]
        if glosses and isinstance(glosses, list) and len(glosses) > 0:
            # Clean first gloss
            first = glosses[0]
            if isinstance(first, str):
                return first.split(';')[0].strip()

    return lemma  # fallback to showing the lemma itself

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
    """Get array of definitions for popup display"""
    lemma_lower = lemma.lower()
    definitions = []

    # Try Whitaker's first (cleaner definitions)
    if lemma_lower in GLOSS_DICT:
        gloss = GLOSS_DICT[lemma_lower]
        if gloss and gloss != lemma:
            # Split on common separators for multiple definitions
            parts = [g.strip() for g in gloss.split(';') if g.strip()]
            definitions.extend(parts[:3])  # Max 3 from Whitaker's

    # Add Lewis & Short definitions if we need more
    if lemma_lower in FULL_DICT and len(definitions) < 3:
        full_defs = FULL_DICT[lemma_lower]
        if isinstance(full_defs, list):
            for d in full_defs:
                if isinstance(d, str) and d not in definitions:
                    definitions.append(d.split(';')[0].strip())
                if len(definitions) >= 3:
                    break

    # Fallback
    if not definitions:
        definitions = [lemma]

    return definitions


'''
with open("dict2/DICTLINE.GEN", 'r') as f:
    for i, line in enumerate(f):
        if i < 20 and line.strip():
            print(f"LINE {i}: {line.strip()[:200]}")
'''

if __name__ == '__main__':
    app.run(debug=True, port=6767)
    # print(analyzeText("inter lineas"))
