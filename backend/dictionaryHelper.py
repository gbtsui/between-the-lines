import sys
import os
import json
import re
from pathlib import Path

def extract_glosses(entry, max_glosses=3, max_chars=50):
    """Extract short, clean glosses suitable for interlinear display"""
    senses = entry.get("senses", [])
    results = []

    def is_good_gloss(text):
        """Only keep short, definition-like strings"""
        if not text or len(text) < 2 or len(text) > max_chars:
            return False
        # Skip cross-references
        if re.match(r'^(v\.|q\.\s*v\.|=|cf\.)', text):
            return False
        # Skip single words that are just alternate forms
        if re.match(r'^[a-zA-ZāēīōūăĕĭŏŭĀĒĪŌŪ\,\.\s]+$', text) and len(text) < 10:
            # Could be a real gloss like "a rose" - keep short phrases with spaces
            if ' ' not in text:
                return False
        # Skip pure etymological notes
        if any(word in text.lower() for word in ['sanscr', 'etym', 'deriv', 'prob', 'perhaps']):
            return False
        return True

    def collect_glosses(item):
        if isinstance(item, str):
            # Split on common separators and try each piece
            for part in re.split(r'[;,]', item):
                text = part.strip(' ,.()"')
                if is_good_gloss(text):
                    results.append(text)
                    if len(results) >= max_glosses:
                        return
        elif isinstance(item, list):
            for sub in item:
                collect_glosses(sub)
                if len(results) >= max_glosses:
                    return

    for sense in senses:
        collect_glosses(sense)
        if len(results) >= max_glosses:
            break

    # Fallback: try main_notes for very short entries
    if not results:
        note = entry.get('main_notes', '')
        if note and len(note) <= max_chars:
            # Strip parenthetical cross-references
            note = re.sub(r'\(.*?\)', '', note).strip()
            if is_good_gloss(note):
                results.append(note)

    # Last resort: part_of_speech descriptor
    if not results and entry.get('part_of_speech'):
        pos = entry['part_of_speech'].split('.')[0].strip()
        if pos in ['noun', 'verb', 'adjective', 'adverb', 'preposition']:
            results.append(f"({pos})")

    return results[:max_glosses]

# Build the compressed dictionary
minimal = {}
total = 0
good = 0

dict_dir = "dict"  # adjust this path

for letter_file in sorted(Path(dict_dir).glob("*.json")):
    with open(letter_file) as f:
        for entry in json.load(f):
            total += 1
            key = entry.get("key", "").lower()
            if not key:
                continue

            glosses = extract_glosses(entry, max_glosses=2)
            if glosses:
                minimal[key] = glosses
                good += 1

with open("latin_gloss.json", "w") as f:
    json.dump(minimal, f, indent=2)

print(f"Kept {good}/{total} entries with glosses")
print(f"File size: {os.path.getsize('latin_gloss.json') / 1024:.1f} KB")
#i tried writing this myself and gave up. sorry.


def extract_first_gloss(entry, max_chars=30):
    """Get just the best single gloss for interlinear display"""
    glosses = extract_glosses(entry, max_glosses=1, max_chars=max_chars)
    return glosses[0] if glosses else None

# Build single-gloss dictionary
interlinear = {}
for letter_file in sorted(Path(dict_dir).glob("*.json")):
    with open(letter_file) as f:
        for entry in json.load(f):
            key = entry.get("key", "").lower()
            if key:
                gloss = extract_first_gloss(entry)
                if gloss:
                    interlinear[key] = gloss

# Save both - one for inline, one for popup
with open("latin_interlinear.json", "w") as f:
    json.dump(interlinear, f)