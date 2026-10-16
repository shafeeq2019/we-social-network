<template>
  <div class="pointer-events-none fixed inset-x-0 bottom-24 z-[60] flex justify-center px-4 md:bottom-auto md:left-auto md:right-6 md:top-6 md:justify-end"
       role="status" aria-live="polite">
    <Transition enter-active-class="transition duration-300 ease-out" enter-from-class="translate-y-3 opacity-0 scale-95"
                leave-active-class="transition duration-200 ease-in" leave-to-class="translate-y-2 opacity-0">
      <div v-if="store.isVisible"
           class="pointer-events-auto flex w-full max-w-sm items-start gap-3 rounded-2xl border border-border/70 bg-popover p-4 text-popover-foreground shadow-lift">
        <span :class="['mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full',
                       store.variant === 'error' ? 'bg-destructive/15 text-destructive' : 'bg-success/15 text-success']">
          <AlertCircle v-if="store.variant === 'error'" class="h-4 w-4" aria-hidden="true" />
          <Check v-else class="h-4 w-4" :stroke-width="3" aria-hidden="true" />
        </span>
        <p class="flex-1 text-sm font-medium leading-snug">{{ store.message }}</p>
        <button type="button" class="-m-1 rounded-full p-1 text-muted-foreground hover:bg-muted hover:text-foreground"
                aria-label="Dismiss notification" @click="store.hide()">
          <X class="h-4 w-4" aria-hidden="true" />
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
// This is a composition API Component
import { AlertCircle, Check, X } from 'lucide-vue-next';
import { useToastStore } from '@/stores/toast';
const store = useToastStore();
</script>
