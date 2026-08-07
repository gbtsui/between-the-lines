<script lang="ts">
    import type {WordData} from "$lib/types";
    import {formatMorphology} from "$lib/utils/morphology";
    import {resolve} from "$app/paths";

    console.log("Vos saluto qui veriora quaesistis")

    let testWord = $state("lorem")
    let error = $state("")
    let testWordData = $state<WordData | null>({
        text: "lorem",
        lemma: "lor",
        pos: "NOUN",
        tag: "noun",
        dep: "ROOT",
        morph: "Case=Acc|Gender=Masc|Number=Sing",
        head: "0",
        definition: ["leather strap, thong"]
    })

    //let formattedMorphology = $derived(testWordData && formatMorphology({morph: testWordData?.morph, pos: testWordData?.pos}))

    function handleTestWordInput(event) {
        // Remove all whitespace (spaces, tabs, newlines)
        testWord = event.currentTarget.value.replace(/\s+/g, '');
    }

    const sendTestWord = async () => {
        /*const response =*/
        try {
            console.log(`Now sending testword ${testWord}`);
            await fetch("/api/testWord", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: testWord,
                })
            })/*.then(res => {
            if (!res.ok) {
                error = res.
            } else return res.json()
        })*/
                .then(res => res.json())
                .then(data => {
                    if (data.type === "failure" || data.error) {
                        console.error("error!", JSON.stringify(data));
                        error = data.error || "request failed :("
                    } else {
                        console.log(JSON.stringify(data));
                        error = ""
                        testWordData = data.words[0]
                    }
                })
            //i actually like this pattern a lot, it's very clean. i should use it more often

        } catch (err) {
            console.error(err)
            if (err instanceof Error) error = err.message;
            else error = "unknown error occurred"
        }


    }
</script>

<div class="w-max-[100vw] h-min-[100vh] bg-stone-800 flex flex-col text-stone-200 justify-start pb-[10rem]">
    <div class="w-[90vw] mx-[5vw] h-[30rem] mt-[3rem] bg-stone-700 flex flex-col items-center justify-center shadow-lg">
        <div class="flex flex-col justify-center">
            <div class="text-5xl text-stone-200">between the lines</div>
            <div class="relative flex gap-[1rem] items-start">
                <div class="relative group">
                    <div class="text-xl text-stone-400 font-serif">inter</div>
                    <div class="absolute top-1/2 left-full">
                        <!--inter-->
                        <svg width="20rem" height="2" class="absolute top-0 left-[-20rem]">
                            <line x1="0" y1="1" x2="17.5rem" y2="1" stroke="#a8a29e" stroke-width="1.5"
                                  stroke-dasharray="4,2"/>
                        </svg>
                        <div class="absolute right-[20rem] -top-4 bg-stone-800 text-stone-200 px-[2rem] py-[1rem] shadow-lg min-w-[180px]">
                            <div class="space-y-1">
                                <div class="flex justify-between gap-[1rem]">
                                    <span class="text-stone-400 text-sm">lemma</span>
                                    <span class="text-stone-200 text-sm font-mono">inter</span>
                                </div>
                                <div class="flex justify-between gap-[1rem]">
                                    <span class="text-stone-400 text-sm">part of speech</span>
                                    <span class="text-emerald-300 text-sm font-mono">ADP</span>
                                </div>
                                <div class="flex justify-between gap-[1rem]">
                                    <span class="text-stone-400 text-sm">morphology</span>
                                    <span class="text-amber-300 text-sm font-mono">+ACC</span>
                                </div>
                                <div class="flex justify-between gap-[1rem]">
                                    <span class="text-stone-400 text-sm">syntactic dependency</span>
                                    <span class="text-sky-300 text-sm font-mono">case</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="relative group">
                    <div class="text-xl text-stone-400 font-serif">lineas</div>
                    <div class="absolute top-1/2 left-full">
                        <svg width="20rem" height="2" class="absolute top-0 left-0">
                            <line x1="0.5rem" y1="1" x2="20rem" y2="1" stroke="#a8a29e" stroke-width="1.5"
                                  stroke-dasharray="4,2"/>
                        </svg>
                        <div class="absolute left-[20rem] -top-4 bg-stone-800 text-stone-200 px-[2rem] py-[1rem] shadow-lg min-w-[180px]">
                            <div class="space-y-1">
                                <div class="flex justify-between gap-4">
                                    <span class="text-stone-400 text-sm">lemma</span>
                                    <span class="text-stone-200 text-sm font-mono">linea</span>
                                </div>
                                <div class="flex justify-between gap-4">
                                    <span class="text-stone-400 text-sm">part of speech</span>
                                    <span class="text-emerald-300 text-sm font-mono">NOUN</span>
                                </div>
                                <div class="flex justify-between gap-4">
                                    <span class="text-stone-400 text-sm">morphology</span>
                                    <span class="text-amber-300 text-sm font-mono">F.ACC.PL</span>
                                </div>
                                <div class="flex justify-between gap-4">
                                    <span class="text-stone-400 text-sm">syntactic dependency</span>
                                    <span class="text-sky-300 text-sm font-mono">obj</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="mx-[5vw]  mt-[3rem] flex flex-col items-center justify-center">
        <a href={resolve("/interlinear")} class="text-lg bg-stone-300 text-stone-800 p-[2rem] hover:p-[2.1rem] hover:bg-stone-200 transition-all">
            open interlinear editor
        </a>
    </div>

    <div class="w-[90vw] mx-[5vw] h-[50rem] mt-[3rem] text-stone-200 flex flex-col items-center justify-center">
        <div class="w-[75vw] flex flex-row items-center justify-around">
            <div class="w-[30vw] text-lg">
                yet another tool for interlinear Latin analysis.
                the difference is that this one is kinda pretty. or at least i'm trying to make it pretty.
            </div>
            <div class="w-[30vw] h-[40rem] bg-stone-700 flex flex-col justify-start gap-[1rem] p-[1rem] items-center">
                <div class="text-lg text-center">try it out with word lookup.</div>
                <input type="text" bind:value={testWord} oninput={handleTestWordInput}
                       class="bg-stone-300 text-stone-800 text-center outline-color-stone-800 focus:ring-stone-200 focus:ring-2 focus:border-stone-200"/>
                <button onclick={sendTestWord}
                        class="m-[1rem] p-[0.5rem] hover:p-[1rem] hover:m-[0.5rem] cursor-pointer bg-stone-400 hover:bg-stone-300 text-stone-800 transition-all w-[7.5rem]">
                    lookup
                </button>
                <div class="bg-stone-800 text-stone-200 px-[2rem] py-[1rem] shadow-lg w-[25vw] h-[25rem]">
                    {#if error}
                        <div class="p-[1rem] m-[1rem] w-full bg-red-700">
                            <div class="font-bold">Error occurred :(</div>
                            <div>{error}</div>
                        </div>
                    {/if}
                    <div class="space-y-1">
                        <div class="flex justify-between gap-4">
                            <span class="text-stone-400 text-sm">lemma</span>
                            <span class="text-stone-200 text-sm font-mono">{testWordData?.lemma ?? "Lemmatized form"}</span>
                        </div>
                        <div class="flex justify-between gap-4">
                            <span class="text-stone-400 text-sm">part of speech</span>
                            <span class="text-emerald-300 text-sm font-mono">{testWordData?.pos ?? "Part of Speech"}</span>
                        </div>
                        <!--not sure if i want to show the full tag, will show for now-->
                        <div class="flex justify-between gap-4">
                            <span class="text-stone-400 text-sm">tag</span>
                            <span class="text-teal-300 text-sm font-mono">{testWordData?.tag ?? "Tag"}</span>
                        </div>
                        <div class="flex justify-between gap-4">
                            <span class="text-stone-400 text-sm">morphology</span>
                            <span class="text-amber-300 text-sm font-mono">{testWordData && formatMorphology({
                                morph: testWordData.morph,
                                pos: testWordData.pos
                            })}</span>
                        </div>
                        <div class="flex justify-between gap-4">
                            <span class="text-stone-400 text-sm">syntactic dependency</span>
                            <span class="text-sky-300 text-sm font-mono">{testWordData?.dep ?? "Syntactic Dependency"}</span>
                        </div>
                        <div class="flex flex-col gap-4">
                            <span class="text-stone-400">definitions</span>
                            <ul>
                                {#each testWordData?.definition as def (def)}
                                    <li class="text-stone-500 text-xs">{def}</li>
                                {/each}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>