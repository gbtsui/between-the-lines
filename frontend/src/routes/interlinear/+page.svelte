<script lang="ts">
    type MODE = "editing" | "reading"
    type LOADSTATE = null | "sending_request" | "decoding"
    let mode = $state<MODE>("editing")
    let rawInput = $state<string>("")
    let loading = $state<boolean>(false)
    let currentLoadState = $state<LOADSTATE>(null)
    let helpOpen = $state<boolean>(false)
    const loremIpsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, " +
        "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " +
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris " +
        "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in " +
        "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " +
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia " +
        "deserunt mollit anim id est laborum." // stolen STRAIGHT from wikipedia
    const defaultText = "Lorem ipsum dolor sit amet..."

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
                //boiiiiiii ts boutta be so tuff
            }
        )
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
            <div class="w-[60vw]">

            </div>

            <!--dsahkjlhkjsafdhlkjahfdla this is where the word breakdown lives-->
            <div class="w-[30vw]">

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
            <div class="absolute bottom-[3rem] right-[3rem] w-[10rem] h-[5rem] bg-stone-300 rounded-lg flex flex-col text-center items-center justify-center hover:text-xl text-lg transition-all cursor-pointer hover:w-[10.5rem] hover:right-[2.75rem] hover:h-[5.5rem] hover:bottom-[2.75rem]">
                <!--add a handler here eventually adshflkjhsalkjfa-->
                Parse!
            </div>
        </div>
    {/if}

    {#if (helpOpen)}
        <div class="absolute w-[100vw] h-[100vh] top-0 left-0 bg-stone-950/30 flex flex-col items-center justify-center shadow-lg">
            <div class="absolute w-[30rem] h-[70vh] bg-stone-700 rounded-lg flex flex-col items-center justify-between p-[2rem] shadow-lg">
                <div class="text-xl font-semibold text-stone-200 tracking-wide">
                    Help
                </div>
                <div class="text-md text-stone-300 flex flex-col gap-[1rem]">
                    <div>Art thou stricken by confusion and perplexity at the complexity of this fusional bewildering display of Lorem and Ipsum?</div>
                    <div>Well, look no further, my dear friend!</div>
                    <div>Perchance, the editing tab is quite simple.</div>
                    <div>I believe it was myself who said, and I quote, "Typeth thy Latin into yonder textbox, whereupon the sacred Parse Button may, should Fortune smile upon thee, bestow philological and computationally linguistic value and whimsy". End quote.</div>
                    <div>But I'm no expert in Latinology, so don't take my word for it.</div>
                    <div>Perchance.</div>
                    <div>If, perhaps, you need guidance, runneth thy finger upon
                        <button class="text-stone-500 cursor-pointer" onclick={appendLoremIpsum}>this</button>
                        word and Lorem Ipsum shall perchance be appended upon thy text to grant thee an example.</div>
                </div>
                <button class="text-lg text-stone-800 bg-stone-300 p-[0.75rem] m-[0.25rem] hover:m-[0rem] hover:bg-stone-400 transition-all hover:p-[1rem] cursor-pointer rounded-lg" onclick={() => helpOpen = false}>
                    I have been enlightened
                </button>
            </div>
        </div>
    {/if}

</div>