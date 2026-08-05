<script lang="ts">
    import type {WordData} from "$lib/types";

    type PropsTypeGuacThinksImAnAlcoholic = {
        word_data: WordData,
        selectFunction: () => void
    }

    const {word_data, selectFunction}: PropsTypeGuacThinksImAnAlcoholic = $props()


</script>


<div>
    <button onclick={selectFunction}>
        {word_data.text}
    </button>
    <div>
        {word_data.definition}
    </div>
</div>