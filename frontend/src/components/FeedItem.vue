<template lang="">
    <div class="p-4 bg-foreground border border-border rounded-lg text-primary">

        <div class="mb-6 flex items-center justify-between">
            <router-link :to="{ name: 'profile', params: { 'id': post.created_by.id } }">
                <div class="flex items-center space-x-3">
                    <img :src="post.created_by.avatar_link" class="w-9 h-9 rounded-full object-cover object-center">

                    <p><strong>{{post.created_by.name }}</strong></p>
                </div>
            </router-link>

            <p class="text-gray-600 text-secondary">{{ /^0\s+minutes$/.test(post.created_ago) ? 'Just now' : post.created_ago}}</p>
        </div>

        <p v-html="formatHashtags(post.body)"> </p>

        <img :src="post.post_attachments[0].image_link" :key="post.post_attachments[0].id"
            class="w-full rounded-lg mt-4 h-auto max-w-xl mx-auto" v-if="post.post_attachments.length > 0">

        <div class="mt-6 mb-1 flex justify-between">
            <div class="flex space-x-6">
                <div class="flex items-center space-x-2">
                    <svg xmlns="http://www.w3.org/2000/svg" :fill="post.post_liked ? 'red' : 'none'" viewBox="0 0 24 24"
                        stroke-width="1.5" @click="likePost" :stroke="post.post_liked ? 'red' : 'currentColor'"
                        class="w-6 h-6 cursor-pointer">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z">
                        </path>
                    </svg>

                    <span class="text-desc text-xs">{{post.likes_count}}</span>
                </div>

                <RouterLink :to="{name: 'postview', params: {id: post.id}}"
                    class="flex items-center space-x-2 cursor-pointer">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z">
                        </path>
                    </svg>

                    <span class="text-desc text-xs">
                        {{ post.comments_count }} comments</span>
                </RouterLink>

                <div class="flex items-center space-x-2 text-desc"  v-if="post.is_private">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>

                    <span class="text-desc text-xs">private</span>
                </div>
                <div class="flex items-center space-x-2 cursor-pointer" @click="share()">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M7.217 10.907a2.25 2.25 0 1 0 0 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186 9.566-5.314m-9.566 7.5 9.566 5.314m0 0a2.25 2.25 0 1 0 3.935 2.186 2.25 2.25 0 0 0-3.935-2.186Zm0-12.814a2.25 2.25 0 1 0 3.933-2.185 2.25 2.25 0 0 0-3.933 2.185Z" />
                    </svg>

                    <span class="text-desc text-xs">Share</span>
                </div>

            </div>

            <div>
                <DropdownMenu>
                    <DropdownMenuTrigger>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z">
                            </path>
                        </svg>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent class="bg-background">
                        <DropdownMenuItem class="cursor-pointer flex space-x-2 items-center" @click="deletePost"
                            v-if="userStore.user.id === post.created_by.id">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                            </svg>
                            <p>Delete post</p>
                        </DropdownMenuItem>
                        <!-- <DropdownMenuSeparator /> -->
                        <DropdownMenuItem v-if="userStore.user.id != post.created_by.id"
                            class="cursor-pointer flex gap-2 items-center" @click="openReportModal = true">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
                            </svg>
                            <p>Report</p>
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
        </div>

        <Dialog v-model:open="openReportModal" @update:open="reportText = ''">
            <DialogContent class="sm:max-w-[425px] text-primary">
                <DialogHeader>
                    <DialogTitle class="text-primary">Report a post</DialogTitle>
                    <DialogDescription class="text-secondary">
                      Please tell us why you want to report this post
                    </DialogDescription>
                </DialogHeader>
                <div class="p-2 text-primary">
                    <textarea class="p-4 w-full bg-foreground rounded-lg" placeholder="Why should we delete this post?"
                        v-model="reportText"></textarea>
                </div>
                <DialogFooter>
                    <button @click="reportPost">
                        Send
                    </button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script lang="ts">
import {
  defineComponent
} from 'vue';
import axios from 'axios';
import {
  Post
} from '../interfaces.ts';
import type {
  PropType
} from 'vue';
import {
  useToastStore
} from '@/stores/toast';
import {
  useUserStore
} from '@/stores/user';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
export default defineComponent({
  components: {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return {
      userStore,
      toastStore
    };
  },
  props: {
    post: {
      type: Object as PropType<Post>,
      required: true
    }
  },
  data() {
    return {
      openReportModal: false,
      reportText: ''
    };
  },
  methods: {
    likePost() {
      axios.post(`/api/post/${this.post.id}/like/`).then(response => {
        if (response.data.message == 'post liked successfully') {
          this.post.likes_count += 1;
          this.post.post_liked = true;
        } else {
          this.post.likes_count -= 1;
          this.post.post_liked = false;
        }
      }).catch(e => {
        console.log(e);
      });
    },
    formatHashtags(text: string): string {
      const escapeHTML = (text: string) => text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
      const escapedText = escapeHTML(text);
      return escapedText.replace(/\B#(\w+)/g,
        '<a class="text-hashtag" href="/trends/$1">#$1</a>');
    },
    async deletePost() {
      axios.delete(`/api/post/${this.post.id}`).then(
        () => {
          this.$emit('deletePost', this.post.id);
          this.toastStore.showToast(5000, 'The post was deleted', 'bg-emerald-500');
          if (this.$route.name == 'postview') {
            this.$router.go(-1);
          }
        }
      ).catch(e => {
        console.log(e);
      });
    },
    async reportPost() {
      axios.post(`/api/post/${this.post.id}/report/`, {
        reportText: this.reportText
      }).then(response => {
        this.openReportModal = false;
        console.log(response);
        this.toastStore.showToast(5000, 'The post was reported', 'bg-emerald-500');
      }).catch(e => {
        console.log(e);
      });
    },
    share() {
      const route = this.$router.resolve({ name: 'postview', params: { id: this.post.id } });
      const absoluteURL = new URL(route.href, window.location.origin).href;

      navigator.share({
        title: 'Post from We',
        text: this.post.body,
        url: absoluteURL,
      });
    }
  },
  created() { }
});
</script>