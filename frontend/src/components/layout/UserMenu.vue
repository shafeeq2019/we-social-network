<template>
  <DropdownMenu>
    <DropdownMenuTrigger :class="cn('group rounded-full', triggerClass)" aria-label="Open account menu">
      <slot>
        <Avatar :src="userStore.user.avatar_link" :name="userStore.user.name" size="sm" />
      </slot>
    </DropdownMenuTrigger>
    <DropdownMenuContent :align="align" :side="side" class="w-64 rounded-2xl p-1.5 shadow-lift">
      <DropdownMenuItem class="cursor-pointer gap-3 rounded-xl p-2" @select="go({ name: 'profile', params: { id: userStore.user.id } })">
        <Avatar :src="userStore.user.avatar_link" :name="userStore.user.name" size="sm" />
        <span class="min-w-0">
          <span class="block truncate font-semibold">{{ userStore.user.name }}</span>
          <span class="block truncate text-xs text-muted-foreground">View your profile</span>
        </span>
      </DropdownMenuItem>
      <DropdownMenuSeparator class="my-1.5" />
      <DropdownMenuItem class="cursor-pointer gap-3 rounded-xl px-2.5 py-2" @select="go({ name: 'editprofile' })">
        <UserCog class="h-4 w-4 text-muted-foreground" aria-hidden="true" /> Edit profile
      </DropdownMenuItem>
      <DropdownMenuItem class="cursor-pointer gap-3 rounded-xl px-2.5 py-2" @select="go({ name: 'editpassword' })">
        <KeyRound class="h-4 w-4 text-muted-foreground" aria-hidden="true" /> Change password
      </DropdownMenuItem>
      <DropdownMenuItem class="cursor-pointer gap-3 rounded-xl px-2.5 py-2" @select.prevent="$emit('toggleTheme')">
        <Sun v-if="theme === 'dark'" class="h-4 w-4 text-muted-foreground" aria-hidden="true" />
        <Moon v-else class="h-4 w-4 text-muted-foreground" aria-hidden="true" />
        {{ theme === 'dark' ? 'Light' : 'Dark' }} mode
      </DropdownMenuItem>
      <DropdownMenuSeparator class="my-1.5" />
      <DropdownMenuItem class="menu-item-danger cursor-pointer gap-3 rounded-xl px-2.5 py-2" @select="$emit('logout')">
        <LogOut class="h-4 w-4" aria-hidden="true" /> Log out
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

<script setup lang="ts">
import { useRouter, type RouteLocationRaw } from 'vue-router';
import { KeyRound, LogOut, Moon, Sun, UserCog } from 'lucide-vue-next';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import Avatar from '@/components/ui/Avatar.vue';
import { useUserStore } from '@/stores/user';
import { cn } from '@/lib/utils';

withDefaults(defineProps<{
  theme: string;
  align?: 'start' | 'center' | 'end';
  side?: 'top' | 'bottom' | 'left' | 'right';
  triggerClass?: string;
}>(), {
  align: 'end',
  side: 'bottom',
  triggerClass: '',
});

defineEmits<{
  (e: 'toggleTheme'): void;
  (e: 'logout'): void;
}>();

const userStore = useUserStore();
const router = useRouter();

function go(to: RouteLocationRaw) {
  router.push(to);
}
</script>
