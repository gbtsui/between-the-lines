const CASE_ABBR: Record<string, string> = {
    Nom: "NOM",
    Acc: "ACC",
    Gen: "GEN",
    Dat: "DAT",
    Abl: "ABL",
    Voc: "VOC",
    Loc: "LOC"
}

const GENDER_ABBR: Record<string, string> = {
    Masc: "M", Fem: "F", Neut: "N"
}

const NUMBER_ABBR: Record<string, string> = {
    Sing: 'SG', Plur: 'PL'
};
const PERSON_ABBR: Record<string, string> = {
    '1': '1', '2': '2', '3': '3'
};
const TENSE_ABBR: Record<string, string> = {
    Pres: 'PRES', Imp: 'IMP', Fut: 'FUT', Perf: 'PERF', Pqp: 'PLUP', FutP: 'FUTP'
};
const MOOD_ABBR: Record<string, string> = {
    Ind: 'IND', Sub: 'SUB', Imp: 'IMP' // imperative mood, not imperfect tense
};
const VOICE_ABBR: Record<string, string> = {
    Act: 'ACT', Pass: 'PASS'
};

function parseMorph(morph: string): Record<string, string> {
    if (!morph) return {};
    const features: Record<string, string> = {};
    morph.split('|').forEach(pair => {
        const [key, value] = pair.split('=');
        if (key && value) features[key] = value;
    });
    return features;
}

export const formatMorphology =
({morph, pos}: { morph: string, pos: string }) => {
    if (!morph) {
        if (pos === "ADP") return "+?"
        return ""
    }

    const f = parseMorph(morph);
    const parts: string[] = []

    //nouns, adj, pronoun
    if (pos !== "ADP" && f.Case) {
        if (f.Gender) parts.push(GENDER_ABBR[f.Gender] || f.Gender);
        parts.push(CASE_ABBR[f.Case] || f.Case);
        if (f.Number) parts.push(NUMBER_ABBR[f.Number] || f.Number);
    }

    //verb
    else if (f.Tense || f.VerbForm) {
        if (f.Person) parts.push(PERSON_ABBR[f.Person]);
        if (f.Number) parts.push(NUMBER_ABBR[f.Number]);
        if (f.Tense) parts.push(TENSE_ABBR[f.Tense] || f.Tense);
        if (f.Mood) parts.push(MOOD_ABBR[f.Mood] || f.Mood);
        if (f.Voice) parts.push(VOICE_ABBR[f.Voice] || f.Voice);
    }

    //preposition if morph includes case (show +Case)
    else if (pos === 'ADP' && f.Case) {
        return '+' + (CASE_ABBR[f.Case] || f.Case);
    }

    else {
        for (const [k, v] of Object.entries(f)) {
            parts.push(`${k}=${v}`);
        }
    }
}

