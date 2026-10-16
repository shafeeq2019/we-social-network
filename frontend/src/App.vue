<template>
  <a href="#main-content"
     class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[100] focus:rounded-full focus:bg-foreground focus:px-4 focus:py-2 focus:text-background">
    Skip to content
  </a>

  <div v-if="isAuthed" class="min-h-screen md:flex">
    <!-- Desktop / tablet rail -->
    <aside class="sticky top-0 hidden h-screen shrink-0 border-r border-border/70 md:flex md:w-[84px] xl:w-[264px]"
           aria-label="Primary">
      <div class="flex w-full flex-col px-3 py-5 xl:px-5">
        <RouterLink :to="{ name: 'feed' }" class="mb-8 flex items-center justify-center rounded-2xl p-1 xl:justify-start"
                    aria-label="We home">
          <BrandMark class="xl:hidden" compact />
          <BrandMark class="hidden xl:inline-flex" />
        </RouterLink>

        <nav class="flex flex-1 flex-col gap-1">
          <RouterLink v-for="item in navItems" :key="item.key" :to="item.to"
                      :aria-current="isActive(item) ? 'page' : undefined"
                      :title="item.label"
                      :class="cn(
                        'group relative flex h-12 items-center justify-center gap-3.5 rounded-2xl px-3 text-[15px] font-medium transition-colors xl:justify-start',
                        isActive(item) ? 'bg-card text-foreground shadow-soft ring-1 ring-border/70' : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                      )">
            <span class="relative">
              <component :is="item.icon" :class="cn('h-[22px] w-[22px] transition-transform group-active:scale-90', isActive(item) && 'text-primary')"
                         :stroke-width="isActive(item) ? 2.4 : 1.9" aria-hidden="true" />
              <NavBadge v-if="item.badge && notificationStore.unread" :count="notificationStore.unread" />
            </span>
            <span class="hidden xl:inline">{{ item.label }}</span>
          </RouterLink>

          <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }"
                      :aria-current="isProfileActive ? 'page' : undefined"
                      title="Profile"
                      :class="cn(
                        'group flex h-12 items-center justify-center gap-3.5 rounded-2xl px-3 text-[15px] font-medium transition-colors xl:justify-start',
                        isProfileActive ? 'bg-card text-foreground shadow-soft ring-1 ring-border/70' : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                      )">
            <Avatar :src="userStore.user.avatar_link" :name="userStore.user.name" size="xs"
                    :class="isProfileActive ? 'ring-2 ring-primary ring-offset-2 ring-offset-card' : ''" />
            <span class="hidden xl:inline">Profile</span>
          </RouterLink>
        </nav>

        <div class="mt-4 flex flex-col items-center gap-2 xl:items-stretch">
          <button type="button" class="icon-btn xl:hidden" :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
                  @click="changeColorTheme">
            <Sun v-if="theme === 'dark'" class="h-5 w-5" aria-hidden="true" />
            <Moon v-else class="h-5 w-5" aria-hidden="true" />
          </button>
          <UserMenu :theme="theme" side="top" align="start" trigger-class="w-full" @toggle-theme="changeColorTheme" @logout="logout">
            <span class="flex w-full items-center justify-center gap-3 rounded-2xl p-1.5 text-left transition-colors hover:bg-muted xl:justify-start xl:p-2">
              <Avatar :src="userStore.user.avatar_link" :name="userStore.user.name" size="sm" />
              <span class="hidden min-w-0 flex-1 xl:block">
                <span class="block truncate text-sm font-semibold">{{ userStore.user.name }}</span>
                <span class="block truncate text-xs text-muted-foreground">Account &amp; settings</span>
              </span>
              <MoreHorizontal class="hidden h-4 w-4 text-muted-foreground xl:block" aria-hidden="true" />
            </span>
          </UserMenu>
        </div>
      </div>
    </aside>

    <!-- Mobile top bar -->
    <header class="sticky top-0 z-40 flex h-14 items-center justify-between border-b border-border/60 bg-background/80 px-4 backdrop-blur-xl md:hidden">
      <RouterLink :to="{ name: 'feed' }" aria-label="We home">
        <BrandMark />
      </RouterLink>
      <div class="flex items-center gap-1">
        <button type="button" class="icon-btn" :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
                @click="changeColorTheme">
          <Sun v-if="theme === 'dark'" class="h-5 w-5" aria-hidden="true" />
          <Moon v-else class="h-5 w-5" aria-hidden="true" />
        </button>
        <UserMenu :theme="theme" @toggle-theme="changeColorTheme" @logout="logout" />
      </div>
    </header>

    <main id="main-content" class="min-w-0 flex-1 px-4 pb-28 pt-5 sm:px-6 md:pb-12 md:pt-8 lg:px-10">
      <RouterView v-slot="{ Component, route }">
        <component :is="Component" :key="route.name === 'messages' ? 'messages' : route.fullPath" />
      </RouterView>
    </main>

    <!-- Mobile tab bar -->
    <nav class="fixed inset-x-0 bottom-0 z-40 border-t border-border/60 bg-background/85 pb-[env(safe-area-inset-bottom)] backdrop-blur-xl md:hidden"
         aria-label="Primary">
      <ul class="mx-auto flex max-w-md items-stretch justify-around px-2">
        <li v-for="item in mobileItems" :key="item.key" class="flex-1">
          <RouterLink :to="item.to" :aria-current="isActive(item) ? 'page' : undefined"
                      :class="cn('flex h-16 flex-col items-center justify-center gap-1 text-[11px] font-medium transition-colors active:scale-95',
                                 isActive(item) ? 'text-foreground' : 'text-muted-foreground')">
            <span class="relative">
              <component :is="item.icon" :class="cn('h-6 w-6', isActive(item) && 'text-primary')"
                         :stroke-width="isActive(item) ? 2.4 : 1.9" aria-hidden="true" />
              <NavBadge v-if="item.badge && notificationStore.unread" :count="notificationStore.unread" />
            </span>
            {{ item.label }}
          </RouterLink>
        </li>
        <li class="flex-1">
          <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }"
                      :aria-current="isProfileActive ? 'page' : undefined"
                      :class="cn('flex h-16 flex-col items-center justify-center gap-1 text-[11px] font-medium', isProfileActive ? 'text-foreground' : 'text-muted-foreground')">
            <Avatar :src="userStore.user.avatar_link" :name="userStore.user.name" size="xs"
                    :class="cn('!h-6 !w-6', isProfileActive && 'ring-2 ring-primary ring-offset-2 ring-offset-background')" />
            Profile
          </RouterLink>
        </li>
      </ul>
    </nav>
  </div>

  <main v-else id="main-content" class="min-h-screen">
    <RouterView />
  </main>

  <Toast />
</template>

<script lang="ts">
import { defineComponent, h } from 'vue';
import axios from 'axios';
import { MoreHorizontal, Moon, Sun } from 'lucide-vue-next';
import Toast from '@/components/Toast.vue';
import Avatar from '@/components/ui/Avatar.vue';
import BrandMark from '@/components/layout/BrandMark.vue';
import UserMenu from '@/components/layout/UserMenu.vue';
import { getNavItems, type NavItem } from '@/components/layout/navigation';
import { useUserStore } from '@/stores/user';
import { useNotificationStore } from '@/stores/notifications';
import { cn, getCurrentThem, toggleTheme } from './lib/utils';

const NavBadge = defineComponent({
  props: { count: { type: Number, required: true } },
  setup(props) {
    return () => h('span', {
      class: 'absolute -right-2 -top-1.5 flex h-[18px] min-w-[18px] items-center justify-center rounded-full bg-like px-1 text-[10px] font-bold text-white ring-2 ring-background animate-in zoom-in-50',
      'aria-label': `${props.count} unread`,
    }, props.count > 9 ? '9+' : String(props.count));
  }
});

export default defineComponent({
  components: {
    Toast,
    Avatar,
    BrandMark,
    UserMenu,
    NavBadge,
    MoreHorizontal,
    Moon,
    Sun,
  },
  setup() {
    const userStore = useUserStore();
    const notificationStore = useNotificationStore();
    return {
      userStore,
      notificationStore,
      cn,
    };
  },
  data() {
    return {
      theme: ''
    };
  },
  computed: {
    isAuthed(): boolean {
      return this.userStore.user.isAuthenticated && !!this.userStore.user.id;
    },
    navItems(): NavItem[] {
      return getNavItems(this.userStore.user.id);
    },
    mobileItems(): NavItem[] {
      return this.navItems.filter(item => item.key !== 'friends');
    },
    isProfileActive(): boolean {
      return this.$route.name === 'profile' && this.$route.params.id === this.userStore.user.id;
    }
  },
  watch: {
    isAuthed: {
      handler(value: boolean) {
        if (value) {
          this.notificationStore.fetchUnread();
        }
      },
      immediate: true
    },
    '$route.name'() {
      if (this.isAuthed) {
        this.notificationStore.fetchUnread();
      }
    }
  },
  methods: {
    isActive(item: NavItem): boolean {
      if (item.key === 'friends') {
        return this.$route.name === 'friends' && this.$route.params.id === this.userStore.user.id;
      }
      return item.match.includes(String(this.$route.name));
    },
    logout() {
      this.userStore.removeToken();
      this.$router.push('/login');
    },
    changeColorTheme() {
      this.theme = toggleTheme();
    },
  },
  created() {
    this.theme = getCurrentThem();
    this.userStore.initStore();
    const token = this.userStore.user.access;
    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
    } else {
      axios.defaults.headers.common['Authorization'] = '';
    }
  }
});
</script>
