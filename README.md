# between the lines
get it? cuz like. interlinear. from the words "inter" (between) and "linear" (pertaining to lines). between the lines. please laugh.

intended to be a web wrapper for a latin natural language processor! take a phrase in latin then it breaks it down word-by-word to create an interlinear translation. planning to expand to Ancient Greek!

It's kind of broken right now. The grammatical analysis is working perfectly fine, it's just that I'm working with two of the WORST fricking digital dictionaries of all time and parsing and finding glosses is hell. 
I'm planning to actually run both dictionaries through a local LLM to sort everything into its lemmas, strict one/two word definitions and occasional expansions. 
No hate to Lewis and Short or Mr. Whitaker, but Lewis and Short is encyclopaedic when I need glosses and Whitaker's formatting is too weird for me to be able to do in the 3 hours I spent on parsing.

It does what it needs to do, though -- the "translation" part is really scuffed at the moment and you could probably get quicker (literal) results from Google Translate, 
but my intended value is in the actual grammatical analysis tool given by the NLP. Useful for finding nuances and grammatical gooberies in texts quickly without having to 
memorize declension and stuff.

Gladius inter lineas est

## framework
polyglot (heh). 

Backend:
- Python
- spaCy
- LatinCy la_core_web_lg
- Flask

Frontend:
- SvelteKit
- TailwindCSS

AI disclosure:
- Frontend components and TypeScript logic done by me, debugged via LLMs
- Python backend... I tried really hard, wrote most of the early versions myself, eventually got super pressed for time and had to debug the JSON/GEN parsers really really quick
- I do wish I could have used less, but it is what it is