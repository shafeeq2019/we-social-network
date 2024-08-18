<template>
  <nav class="py-3 px-4 border-b border-gray-200 bg-white fixed w-full top-0">
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
              <DropdownMenuContent class="font-medium  bg-white rounded-md">
                <DropdownMenuItem class="cursor-pointer">
                  <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }"
                    class="flex space-x-2 items-center">
                    <img :src="userStore.user.avatar_link" class="rounded-full w-8 h-8" />
                    <span class="px-2">{{ userStore.user.name }}</span>
                  </RouterLink>
                </DropdownMenuItem>
                <DropdownMenuItem class="cursor-pointer" @click="logout">
                  <div class="flex space-x-2 items-center">
                    <svg class="h-8 w-8 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
            <RouterLink class="py-2 px-4 bg-purple-600 text-white rounded-md text-sm" to="/signup">Sign up</RouterLink>
          </div>
        </template>
      </div>
    </div>
  </nav>
  <main class="px-4 py-6 mt-14">
    <RouterView />
  </main>
  <Toast />
</template>

<script lang="ts">
import Toast from "@/components/Toast.vue";
import {
  useUserStore
} from "@/stores/user";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import axios from "axios";
import {
  defineComponent
} from "vue";

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    return {
      userStore,
      userId: ''
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
      this.$router.push("/login");
    }
  },
  created() {
    this.userStore.initStore();
    const token = this.userStore.user.access;
    if (token) {
      axios.defaults.headers.common["Authorization"] = "Bearer " + token;
    } else {
      axios.defaults.headers.common["Authorization"] = "";
    }
  }
});
</script>

<style scoped></style>