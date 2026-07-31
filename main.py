import spacy
import sys
import json 
import flask

nlp = spacy.load("la_core_web_lg")
doc = nlp("haec narrantur a poetis de perseo")

for word in doc:
    print(f'{word.text}, {word.norm_}, {word.lemma_}, {word.pos_}')
