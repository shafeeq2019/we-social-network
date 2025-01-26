<template>
  <nav class="py-3 px-4 border-b border-border bg-foreground text-primary fixed w-full top-0">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between">
        <div class="menu-left">
          <a href="#" class="text-xl font-medium">We</a>
        </div>
        <div class="menu-center flex space-x-9" v-if="userStore.user.isAuthenticated">
          <RouterLink to="/feed" active-class="text-purple-700">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                 stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
            </svg>
          </RouterLink>
          <RouterLink :to="{ name: 'messages', params: { id: null } }" active-class="text-purple-700">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                 stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M8.625 9.75a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 01.778-.332 48.294 48.294 0 005.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z">
              </path>
            </svg>
          </RouterLink>
          <RouterLink to="/notifications" active-class="text-purple-700">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                 stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0">
              </path>
            </svg>
          </RouterLink>
          <RouterLink to="/search" active-class="text-purple-700">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                 stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
            </svg>
          </RouterLink>
        </div>
        <template v-if="userStore.user.isAuthenticated && userStore.user.id">
          <div class="menu-right">
            <DropdownMenu>
              <DropdownMenuTrigger>
                <img :src="userStore.user.avatar_link" class="rounded-full w-10 h-10" />
              </DropdownMenuTrigger>
              <DropdownMenuContent class="font-medium bg-background rounded-md">
                <DropdownMenuItem class="cursor-pointer">
                  <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }"
                              class="flex space-x-2 items-center">
                    <img :src="userStore.user.avatar_link" class="rounded-full w-8 h-8" />
                    <span class="px-2">{{ userStore.user.name }}</span>
                  </RouterLink>
                </DropdownMenuItem>
                <DropdownMenuItem class="cursor-pointer">
                  <div class="flex space-x-2 items-center" @click="changeColorTheme()">
                    <svg v-if="theme === 'dark'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                         stroke="currentColor" class="h-8 w-8 text-secondary">
                      <path stroke-linecap="round" stroke-linejoin="round"
                            d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
                    </svg>
                    <svg v-if="theme === 'light'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                         stroke="currentColor" class="h-8 w-8 text-secondary">
                      <path stroke-linecap="round" stroke-linejoin="round"
                            d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z" />
                    </svg>
                    <span class="px-2">{{ theme == "dark" ? "Light" : "Dark" }} Mode </span>
                  </div>
                </DropdownMenuItem>
                <DropdownMenuItem class="cursor-pointer" @click="logout">
                  <div class="flex space-x-2 items-center">
                    <svg class="h-8 w-8 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    <span class="px-2">Logout</span>
                  </div>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </template>
        <template v-else>
          <div class="menu-right">
            <RouterLink class="py-2 px-4 bg-gray-500 text-white rounded-md mr-4 text-sm" to="/login">Log in</RouterLink>
            <RouterLink class="py-2 px-4 bg-button-primary text-white rounded-md text-sm" to="/signup">Sign up
            </RouterLink>
          </div>
        </template>
      </div>
    </div>
  </nav>
  <main class="px-4 py-6 mt-14 bg-background max-w-7xl mx-auto">
    <RouterView />
  </main>
  <Toast />
</template>

<script lang="ts">
import Toast from '@/components/Toast.vue';
import {
  useUserStore
} from '@/stores/user';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import axios from 'axios';
import {
  defineComponent
} from 'vue';
import { getCurrentThem } from './lib/utils';
export default defineComponent({
  setup() {
    const userStore = useUserStore();
    return {
      userStore,
      userId: '',
      theme: ''
    };
  },
  components: {
    Toast,
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
  },
  methods: {
    logout() {
      this.userStore.removeToken();
      this.$router.push('/login');
    },
    changeColorTheme() {
      let theme = getCurrentThem();
      if (theme === 'dark') {
        theme = 'light';
      } else {
        theme = 'dark';
      }
      localStorage.setItem('we.theme', theme);
      this.theme = getCurrentThem();
      if (theme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    },
  },
  created() {
    this.theme = getCurrentThem();
    console.log(this.theme);
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

<style scoped></style>
