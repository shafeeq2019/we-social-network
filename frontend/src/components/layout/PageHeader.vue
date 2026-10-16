<template>
  <header class="flex items-end justify-between gap-4 px-1 pb-1">
    <div class="min-w-0">
      <p v-if="eyebrow" class="eyebrow mb-1">{{ eyebrow }}</p>
      <h1 class="truncate text-[28px] font-extrabold leading-tight sm:text-[32px]">{{ title }}</h1>
      <p v-if="description" class="mt-1 text-sm text-muted-foreground">{{ description }}</p>
    </div>
    <div v-if="$slots.actions" class="shrink-0">
      <slot name="actions" />
    </div>
  </header>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title: string;
  eyebrow?: string;
  description?: string;
}>(), {
  eyebrow: '',
  description: '',
});
</script>
