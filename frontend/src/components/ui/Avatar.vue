<template>
  <span :class="cn('relative inline-flex shrink-0 select-none items-center justify-center overflow-hidden rounded-full bg-primary-soft font-display font-bold text-primary-soft-foreground', sizes[size], ring && 'ring-4 ring-card', props.class)">
    <img v-if="src && !failed" :src="src" :alt="alt ?? ''" class="h-full w-full object-cover"
         loading="lazy" @error="failed = true">
    <span v-else aria-hidden="true">{{ initials(name) }}</span>
  </span>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { cn, initials } from '@/lib/utils';

type Size = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';

const props = withDefaults(defineProps<{
  src?: string;
  name?: string;
  alt?: string;
  size?: Size;
  ring?: boolean;
  class?: string;
}>(), {
  size: 'md',
  ring: false,
});

const sizes: Record<Size, string> = {
  xs: 'h-7 w-7 text-[10px]',
  sm: 'h-9 w-9 text-xs',
  md: 'h-11 w-11 text-sm',
  lg: 'h-14 w-14 text-base',
  xl: 'h-24 w-24 text-2xl',
  '2xl': 'h-28 w-28 sm:h-36 sm:w-36 text-4xl',
};

const failed = ref(false);
watch(() => props.src, () => {
  failed.value = false;
});
</script>
