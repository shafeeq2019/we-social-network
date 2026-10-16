<template>
  <span class="inline-flex items-center gap-2.5">
    <span class="relative flex h-9 w-9 shrink-0 items-center justify-center rounded-[14px] bg-foreground text-background" aria-hidden="true">
      <span class="font-display text-[19px] font-extrabold leading-none tracking-tighter">w</span>
      <span class="absolute right-[7px] top-[7px] h-[7px] w-[7px] rounded-full bg-primary ring-2 ring-foreground" />
    </span>
    <span v-if="!compact" class="font-display text-[22px] font-extrabold leading-none tracking-tight">
      we<span class="text-primary">.</span>
    </span>
    <span class="sr-only">We</span>
  </span>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ compact?: boolean }>(), { compact: false });
</script>
