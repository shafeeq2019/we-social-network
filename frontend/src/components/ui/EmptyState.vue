<template>
  <div :class="cn('flex flex-col items-center px-6 py-12 text-center animate-fade-up', bare ? '' : 'surface')">
    <div class="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-soft text-primary-soft-foreground">
      <component :is="icon" class="h-6 w-6" aria-hidden="true" />
    </div>
    <h2 class="text-lg font-bold">{{ title }}</h2>
    <p v-if="description" class="mt-1.5 max-w-sm text-sm text-muted-foreground">{{ description }}</p>
    <div v-if="$slots.default" class="mt-6">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Component } from 'vue';
import { cn } from '@/lib/utils';

withDefaults(defineProps<{
  icon: Component;
  title: string;
  description?: string;
  bare?: boolean;
}>(), {
  description: '',
  bare: false,
});
</script>
