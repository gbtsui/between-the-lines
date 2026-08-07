export type WordData = {
    text: string,
    lemma: string,
    pos: string,
    tag: string,
    morph: string,
    head: string,
    dep: string,
    //definition: string | null,
    definition: string[]
}