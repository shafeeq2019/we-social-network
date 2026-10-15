<template>
  <div class="grid min-h-screen lg:grid-cols-[1.05fr_1fr]">
    <!-- Brand panel -->
    <section class="relative hidden overflow-hidden bg-[hsl(240_12%_8%)] p-12 text-[hsl(40_20%_96%)] lg:flex lg:flex-col" aria-hidden="true">
      <BrandMark class="[&>span:first-child]:bg-[hsl(40_20%_96%)] [&>span:first-child]:text-[hsl(240_12%_8%)]" />

      <!-- Abstract orbit composition -->
      <div class="pointer-events-none absolute -right-24 top-1/2 h-[560px] w-[560px] -translate-y-1/2">
        <div class="absolute inset-0 rounded-full border border-white/10" />
        <div class="absolute inset-[70px] rounded-full border border-white/10" />
        <div class="absolute inset-[140px] rounded-full border border-white/10" />
        <div class="absolute inset-[210px] rounded-full bg-[hsl(250_80%_62%)]" />
        <div class="absolute left-[40px] top-[120px] h-14 w-14 rounded-full bg-[hsl(349_82%_62%)]" />
        <div class="absolute bottom-[90px] left-[150px] h-9 w-9 rounded-full bg-[hsl(40_90%_68%)]" />
        <div class="absolute right-[120px] top-[40px] h-6 w-6 rounded-full bg-white/80" />
      </div>

      <div class="relative mt-auto max-w-md">
        <p class="font-display text-[56px] font-extrabold leading-[0.95] tracking-tight">
          Your people.<br>Your moments.<br><span class="text-[hsl(250_95%_78%)]">Together.</span>
        </p>
        <p class="mt-6 max-w-sm text-base text-white/65">
          Share what matters, follow the conversations you care about and stay close to friends — without the noise.
        </p>
      </div>
    </section>

    <!-- Form panel -->
    <section class="flex flex-col px-5 py-8 sm:px-10">
      <div class="lg:hidden">
        <BrandMark />
      </div>
      <div class="mx-auto flex w-full max-w-[400px] flex-1 flex-col justify-center py-10 animate-fade-up">
        <h1 class="text-[34px] font-extrabold leading-tight">{{ title }}</h1>
        <p class="mt-2 text-muted-foreground">{{ subtitle }}</p>
        <div class="mt-8">
          <slot />
        </div>
        <p v-if="$slots.footer" class="mt-8 text-center text-sm text-muted-foreground">
          <slot name="footer" />
        </p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import BrandMark from './BrandMark.vue';

defineProps<{ title: string; subtitle: string }>();
</script>
