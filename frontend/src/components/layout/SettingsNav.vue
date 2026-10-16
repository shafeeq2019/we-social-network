<template>
  <nav aria-label="Settings" class="flex gap-1 rounded-full bg-muted p-1">
    <RouterLink v-for="item in items" :key="item.name" :to="{ name: item.name }"
                :aria-current="$route.name === item.name ? 'page' : undefined"
                :class="['flex flex-1 items-center justify-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition-all',
                         $route.name === item.name ? 'bg-card text-foreground shadow-soft' : 'text-muted-foreground hover:text-foreground']">
      <component :is="item.icon" class="h-4 w-4" aria-hidden="true" />
      {{ item.label }}
    </RouterLink>
  </nav>
</template>

<script setup lang="ts">
import { KeyRound, UserCog } from 'lucide-vue-next';

const items = [
  { name: 'editprofile', label: 'Profile', icon: UserCog },
  { name: 'editpassword', label: 'Password', icon: KeyRound },
];
</script>
