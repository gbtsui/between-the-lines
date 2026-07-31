<script lang="ts">
    console.log("Vos saluto qui veriora quaesistis")

    let testWord = $state("")
    function handleTestWordInput(event) {
        // Remove all whitespace (spaces, tabs, newlines)
        testWord = event.currentTarget.value.replace(/\s+/g, '');
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
                            <line x1="0" y1="1" x2="17.5rem" y2="1" stroke="#a8a29e" stroke-width="1.5" stroke-dasharray="4,2"/>
                        </svg>
                        <div class="absolute right-[20rem] -top-4 bg-stone-800 text-stone-200 px-[2rem] py-[1rem] shadow-lg min-w-[180px]">
                            <div class="space-y-1">
                                <div class="flex justify-between gap-[1rem]">
                                    <span class="text-stone-400 text-sm">lemma</span>
                                    <span class="text-stone-200 text-sm font-mono">inter</span>
                                </div>
                                <div class="flex justify-between gap-[1rem]">
                                    <span class="text-stone-400 text-sm">part of speech</span>
                                    <span class="text-emerald-300 text-sm font-mono">PREP</span>
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
                    <!-- Arrow and breakdown panel -->
                    <div class="absolute top-1/2 left-full">
                        <svg width="20rem" height="2" class="absolute top-0 left-0">
                            <line x1="0.5rem" y1="1" x2="20rem" y2="1" stroke="#a8a29e" stroke-width="1.5" stroke-dasharray="4,2"/>
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
    <div class="w-[90vw] mx-[5vw] h-[50rem] mt-[3rem] text-stone-200 flex flex-col items-center justify-center shadow-lg">
        <div class="w-[75vw] flex flex-row items-center justify-around">
            <div class="w-[30vw] text-lg">
                yet another tool for interlinear Latin analysis.
                the difference is that this one is kinda pretty. or at least i'm trying to make it pretty.
            </div>
            <div class="w-[30vw] h-[40rem] bg-stone-700 flex flex-col justify-start gap-[1rem] p-[1rem]">
                <div class="text-lg text-center">try it out with word lookup.</div>
                <input type="text" bind:value={testWord} oninput={handleTestWordInput} class="bg-stone-300 text-stone-800 text-center outline-color-stone-800 focus:ring-stone-200 focus:ring-2 focus:border-stone-200"/>
            </div>
        </div>
    </div>
</div>