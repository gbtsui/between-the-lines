<script lang="ts">
    import type {WordData} from "$lib/types";

    type PropsTypeGuacThinksImAnAlcoholic = {
        word_data: WordData,
        selectFunction: (wordData: WordData) => void
    }

    const {word_data, selectFunction}: PropsTypeGuacThinksImAnAlcoholic = $props()


</script>

<div class="flex flex-col items-start">
    <button onclick={() => selectFunction(word_data)} class="text-stone-200 cursor-pointer">
        {word_data.text}
    </button>
    <div class="text-stone-500 text-sm">
        {word_data.definition[0].split(",")[0]} <!--ensure single sense cuz some of these entries have multiple senses-->
    </div>
</div>
