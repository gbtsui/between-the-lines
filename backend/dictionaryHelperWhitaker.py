# okay so lowk im gonna whitakermax
# rest in peace, william whitaker
# 1936 - 2010
# your contributions to latin software will never be forgotten
# may your memory live as long as the language that you studied

import os
import sys
from pathlib import Path


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

whitakers_dict = {}

dict_dir = "dict2"
with open(Path(dict_dir).open('DICTLINE.GEN'), 'r') as f:
    for line in f:
        result = parse_line(line)
        if result:
            whitakers_dict[result['lemma'].lower()] = result['gloss']