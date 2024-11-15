<script setup lang="ts">
const props = defineProps({
    text: {
        type: String,
        default: 'Hello, I am a snackbar'
    },
    type: {
        type: String,
        default: 'success'
    },
    timeout: {
        type: Number,
        default: 2000
    }
});
const showSnackbar = defineModel();
</script>

<template>
    <div class="ma-2">
        <v-snackbar
        v-model="showSnackbar"
        rounded="pill"
        variant="tonal"
        location="bottom"
        :timeout="timeout"
        :color="type"
        :close-on-content-click="true"
        >
            <div class="justify-center text-center text-body-1">
                {{ text }}
            </div>
        </v-snackbar>
    </div>
</template>