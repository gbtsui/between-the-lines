<script lang="ts">
    import type {WordData} from "$lib/types";
    import WordBlock from "$lib/components/WordBlock.svelte";
    import {formatMorphology} from "$lib/utils/morphology";

    type MODE = "editing" | "reading"
    type LOADSTATE = null | "sending_request" | "decoding"
    let mode = $state<MODE>("editing")
    let rawInput = $state<string>("")
    let loading = $state<boolean>(false)
    let currentLoadState = $state<LOADSTATE>(null)
    let error = $state<null | string>(null)
    let helpOpen = $state<boolean>(false)

    //let selectedWordIndex = $state<null | string>(null) //idk if there's a more robust way to do ts
    let selectedWordData = $state<null | WordData>(null)
    let wordslop = $state<WordData[]>([])

    const loremIpsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, " +
        "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " +
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris " +
        "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in " +
        "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " +
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia " +
        "deserunt mollit anim id est laborum." // stolen STRAIGHT from wikipedia
    const defaultText = "Lorem ipsum dolor sit amet..."

    const selectNewWordData = (wordData: WordData) => selectedWordData = wordData

    const appendLoremIpsum = () => {
        rawInput += loremIpsum
        helpOpen = false
    }

    const parse = async () => {
        loading = true
        currentLoadState = "sending_request"
        await fetch("/api/break-it-down", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                text: rawInput,
            })
        }).then(
            res => res.json()
        ).then(
            data => {
                if (data.type === "failure" || data.error) {
                    console.error("error!", JSON.stringify(data));
                    error = data.error || "request failed :("
                } else {
                    console.log(JSON.stringify(data));
                    wordslop = data.words
                }
            }
        ).catch(err => {
            error = err
            loading = false
        }).finally(() => {
            loading = false
        })
    }
</script>

<style>
    .custom-scrollbar::-webkit-scrollbar {
        width: 12px;
    }

    .custom-scrollbar::-webkit-scrollbar-track {
        background: #44403c; /* stone-700 */
        border-radius: 0; /* Square edges */
    }

    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: #78716c; /* stone-500 */
        border-radius: 0; /* Square edges */
        border: 2px solid #44403c; /* Creates padding effect */
    }

    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
        background: #a8a29e; /* stone-400 */
    }

    /* Firefox */
    .custom-scrollbar {
        scrollbar-width: thin;
        scrollbar-color: #78716c #44403c; /* thumb track */
    }
</style>

<!--why the hell does it not want to work properly sadfdsajflsahfdlkjsahflkjsh-->
<div class="w-[100vw] h-[100vh] flex flex-col bg-stone-800 custom-scrollbar">
    <!--top bar idk what to put here yet lowk idk-->
    <div class="sticky top-0 left-0 right-0 z-50 bg-stone-900/95 backdrop-blur-sm border-b border-stone-700 shadow-lg">
        <div class="max-w-[95vw] mx-auto h-[4rem] flex items-center justify-between px-[2rem]">
            <div class="text-xl font-semibold text-stone-200 tracking-wide">Interlinear Editor</div>

            <!-- Mode toggle for future use -->
            <div class="flex gap-[1rem]">
                <button
                        class="px-[1.5rem] py-[0.5rem] rounded-lg text-sm font-medium transition-colors {mode === 'editing' ? 'bg-stone-700 text-stone-100' : 'text-stone-400 hover:text-stone-200'}"
                        onclick={() => mode = 'editing'}>
                    Edit
                </button>
                <button
                        class="px-[1.5rem] py-[0.5rem] rounded-lg text-sm font-medium transition-colors {mode === 'reading' ? 'bg-stone-700 text-stone-100' : 'text-stone-400 hover:text-stone-200'}"
                        onclick={() => mode = 'reading'}>
                    Read
                </button>
                <button
                        class="p-[1rem] h-[3rem] w-[3rem] rounded-full bg-stone-700 flex flex-col items-center justify-center shadow-lg text-2xl cursor-pointer text-stone-400"
                        onclick={() => helpOpen = true}
                >
                    ?
                </button>
            </div>
        </div>
    </div>

    {#if (mode === "reading")}
        <!--split this jawn notionstyle-->
        <div class="h-full w-full flex flex-row justify-center gap-[2rem]">
            <!--word by word-->
            <div class="w-[65vw] h-full flex flex-row flex-wrap items-start grow-0 justify-start gap-[1rem] p-[3rem]">
                {#if !wordslop || wordslop.length === 0}
                    <div class="text-xl text-stone-300 p-[2rem] text-center select-none">Parse a text to see its breakdown here.</div>
                {/if}

                {#each wordslop as slopslopslopsahur (slopslopslopsahur)}
                    <WordBlock selectFunction={selectNewWordData} word_data={slopslopslopsahur}/>
                {/each}
            </div>

            <!--dsahkjlhkjsafdhlkjahfdla this is where the word breakdown lives-->

            <div class="w-[35vw] flex flex-col items-center bg-stone-900">
                {#if selectedWordData === null}
                    <div class="text-xl text-stone-300 p-[2rem] text-center select-none">
                        Select a word to view its grammatical breakdown
                    </div>
                {:else}
                    <div class="h-full flex p-[2rem] flex-col w-full">
                        <div class="text-xl text-stone-300">{selectedWordData.text}</div>
                        <div class="flex-col flex">
                            <div class="flex justify-between gap-4">
                                <span class="text-stone-400 text-sm">lemma</span>
                                <span class="text-stone-200 text-sm font-mono">{selectedWordData?.lemma ?? "Lemmatized form"}</span>
                            </div>
                            <div class="flex justify-between gap-4">
                                <span class="text-stone-400 text-sm">part of speech</span>
                                <span class="text-emerald-300 text-sm font-mono">{selectedWordData?.pos ?? "Part of Speech"}</span>
                            </div>
                            <!--not sure if i want to show the full tag, will show for now-->
                            <div class="flex justify-between gap-4">
                                <span class="text-stone-400 text-sm">tag</span>
                                <span class="text-teal-300 text-sm font-mono">{selectedWordData?.tag ?? "Tag"}</span>
                            </div>
                            <div class="flex justify-between gap-4">
                                <span class="text-stone-400 text-sm">morphology</span>
                                <span class="text-amber-300 text-sm font-mono">{selectedWordData && formatMorphology({
                                    morph: selectedWordData.morph,
                                    pos: selectedWordData.pos
                                })}</span>
                            </div>
                            <div class="flex justify-between gap-4">
                                <span class="text-stone-400 text-sm">syntactic dependency</span>
                                <span class="text-sky-300 text-sm font-mono">{selectedWordData?.dep ?? "Syntactic Dependency"}</span>
                            </div>
                        </div>
                        <div class="flex flex-col gap-4">
                            <span class="text-stone-400">definitions</span>
                            <ul>
                                {#each selectedWordData?.definition as def (def)}
                                    <li class="text-stone-500 text-xs">{def}</li>
                                {/each}
                            </ul>
                        </div>
                    </div>
                {/if}
            </div>
        </div>
    {:else}
        <div class="h-full overflow-x-hidden">
            <!--insert a big ass text box here idk gng-->
            <textarea bind:value={rawInput}
                      class="w-full h-full p-[3rem] bg-stone-800 shadow-inner resize-none focus:outline-none focus:ring-2 focus:ring-stone-800 text-stone-100 text-lg leading-[2.5] overflow-y-auto whitespace-pre-wrap break-words transition-all duration-200, border-2 border-transparent"
                      placeholder={defaultText}
                      style="line-height: 2.5rem"
            ></textarea>
            <button onclick={parse}
                    class="absolute bottom-[3rem] right-[3rem] w-[10rem] h-[5rem] bg-stone-300 rounded-lg flex flex-col text-center items-center justify-center hover:text-xl text-lg transition-all cursor-pointer hover:w-[10.5rem] hover:right-[2.75rem] hover:h-[5.5rem] hover:bottom-[2.75rem]">
                <!--add a handler here eventually adshflkjhsalkjfa-->
                Parse!
            </button>
        </div>
    {/if}

    {#if (helpOpen)}
        {#if (mode === "editing")}
            <div class="absolute w-[100vw] h-[100vh] top-0 left-0 bg-stone-950/30 flex flex-col items-center justify-center shadow-lg">
                <div class="absolute w-[30rem] h-[70vh] bg-stone-700 rounded-lg flex flex-col items-center justify-between p-[2rem] shadow-lg">
                    <div class="text-xl font-semibold text-stone-200 tracking-wide">
                        Help
                    </div>
                    <div class="text-md text-stone-300 flex flex-col gap-[1rem]">
                        <div>Art thou stricken by confusion and perplexity at the complexity of this fusional
                            bewildering
                            display of Lorem and Ipsum?
                        </div>
                        <div>Well, look no further, my dear friend!</div>
                        <div>Perchance, the editing tab is quite simple.</div>
                        <div>I believe it was myself who said, and I quote, "Typeth thy Latin into yonder textbox,
                            whereupon
                            the sacred Parse Button may, should Fortune smile upon thee, bestow philological and
                            computationally linguistic value and whimsy". End quote.
                        </div>
                        <div>But I'm no expert in Latinology, so don't take my word for it.</div>
                        <div>Perchance.</div>
                        <div>If, perhaps, you need guidance, runneth thy finger upon
                            <button class="text-stone-500 cursor-pointer" onclick={appendLoremIpsum}>this</button>
                            word and Lorem Ipsum shall perchance be appended upon thy text to grant thee an example.
                        </div>
                    </div>
                    <button class="text-lg text-stone-800 bg-stone-300 p-[0.75rem] m-[0.25rem] hover:m-[0rem] hover:bg-stone-400 transition-all hover:p-[1rem] cursor-pointer rounded-lg"
                            onclick={() => helpOpen = false}>
                        I have been enlightened
                    </button>
                </div>
            </div>
        {:else if (mode === "reading")}
            <div class="absolute w-[100vw] h-[100vh] top-0 left-0 bg-stone-950/30 flex flex-col items-center justify-center shadow-lg">
                <div class="absolute w-[30rem] h-[70vh] bg-stone-700 rounded-lg flex flex-col items-center justify-between p-[2rem] shadow-lg">
                    <div class="text-xl font-semibold text-stone-200 tracking-wide">
                        Help
                    </div>
                    <div class="text-md text-stone-300 flex flex-col gap-[1rem]">
                        <div>This is the reading section.</div>
                        <div>im so fricking tired ive been wrestling with bad dictionaries and my laptop getting liquid
                            damage i think it's pretty self-explanatory
                        </div>
                    </div>
                    <button class="text-lg text-stone-800 bg-stone-300 p-[0.75rem] m-[0.25rem] hover:m-[0rem] hover:bg-stone-400 transition-all hover:p-[1rem] cursor-pointer rounded-lg"
                            onclick={() => helpOpen = false}>
                        oh
                    </button>
                </div>
            </div>
        {/if}
    {/if}

</div>