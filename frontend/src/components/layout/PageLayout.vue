<template>
  <div class="mx-auto flex w-full max-w-[1040px] gap-8 xl:gap-10">
    <div class="min-w-0 flex-1">
      <div class="mx-auto w-full max-w-[640px] space-y-4">
        <slot />
      </div>
    </div>
    <aside v-if="!noAside" class="hidden w-[320px] shrink-0 xl:block" aria-label="Suggestions">
      <div class="sticky top-8 space-y-4">
        <slot name="aside">
          <PeopleYouMayKnow />
          <Trends />
        </slot>
        <p class="px-2 text-xs text-muted-foreground">
          We · a place for the people you care about
        </p>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';

withDefaults(defineProps<{ noAside?: boolean }>(), { noAside: false });
</script>
