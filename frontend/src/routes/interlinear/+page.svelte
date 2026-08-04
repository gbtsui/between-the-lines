<script lang="ts">
    type MODE = "editing" | "reading"
    let mode = $state<MODE>("editing")
    let rawInput = $state<string>("")
    let loading = $state<boolean>(false)
    const loremIpsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, " +
        "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " +
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris " +
        "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in " +
        "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " +
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia " +
        "deserunt mollit anim id est laborum." // stolen STRAIGHT from wikipedia
    const defaultText = "Lorem ipsum dolor sit amet..."
</script>


<!--why the hell does it not want to work properly sadfdsajflsahfdlkjsahflkjsh-->
<div class="w-[100vw] h-[100vh] flex flex-col bg-stone-800">
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
            </div>
        </div>    </div>

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
            <textarea bind:value={rawInput} class="w-full h-full p-[3rem] bg-stone-800 shadow-inner resize-none focus:outline-none focus:ring-2 focus:ring-stone-500 text-stone-100 text-lg leading-[2.5] overflow-y-auto whitespace-pre-wrap break-words transition-all duration-200, border-2 border-transparent"
                      placeholder={defaultText}
                        style="line-height: 2.5rem"
            ></textarea>
            <div class="absolute bottom-[3rem] right-[3rem] w-[10rem] h-[5rem] bg-stone-300 rounded-lg flex flex-col text-center items-center justify-center hover:text-xl text-lg transition-all cursor-pointer hover:w-[10.5rem] hover:right-[2.75rem] hover:h-[5.5rem] hover:bottom-[2.75rem]">
                <!--add a handler here eventually adshflkjhsalkjfa-->
                Parse!
            </div>
        </div>
    {/if}


</div>