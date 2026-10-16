<template>
  <div v-if="errors.length > 0" role="alert"
       class="flex gap-3 rounded-2xl border border-destructive/25 bg-destructive/10 p-4 text-sm text-destructive animate-in fade-in slide-in-from-top-1">
    <AlertCircle class="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
    <ul class="space-y-1">
      <li v-for="error in errors" :key="error">{{ error }}</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { AlertCircle } from 'lucide-vue-next';

defineProps<{ errors: string[] }>();
</script>
