<template lang="">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!-- User on the left -->
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <div class="flex items-center justify-center">
                    <img :src="user.avatar_link" class="mb-6 rounded-full object-fit:cover h-64 w-full" />
                </div>

                <p><strong>{{user.name}}</strong></p>
                <div class="mt-6 flex space-x-8 justify-around">
                    <router-link :to="{name:'friends', params:{id: user.id}}" class="text-xs text-gray-500">
                        {{user.friends_count}} friends</router-link>
                    <p class="text-xs text-gray-500">{{user.posts_count}} posts</p>
                </div>

                <div class="mt-6 space-y-2">
                    <router-link v-if="user.id == userStore.user.id" :to="{name:'editprofile'}"
                        class="inline-block p-1 bg-purple-600 text-white rounded-md text-xs w-full">
                        Edit profile
                    </router-link>
                    <button v-if="user.id != userStore.user.id && can_send_friendship_request"
                        class="inline-block p-1 bg-purple-600 text-white rounded-md text-xs w-full"
                        @click="sendFriendshipRequest"> Send friendship request</button>
                    <button v-if="user.id != userStore.user.id"
                        class="inline-block p-1 bg-purple-600 text-white rounded-md text-xs w-full"
                        @click="sendDirectMessage"> Send direct message</button>
                    <button v-if="userStore.user.id && user.id == userStore.user.id"
                        class="inline-block p-1 bg-red-600 text-white rounded-md text-xs w-full" @click="logout">
                        Logut
                    </button>
                </div>
            </div>
        </div>
        <!-- New post & feeds on the middle -->
        <div class="main-center col-span-2 space-y-4">
            <FeedForm :user="user" v-if="userStore.user.id == user.id" :posts="posts"/>
            <FeedItem v-for="post in posts" :user="user" :post="post" :key="post.id" @deletePost="deletePost" />
        </div>

        <!-- People you may know -->
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>

    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios';
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import { useUserStore } from '@/stores/user'
import FeedItem from '../components/FeedItem.vue'
import { useToastStore } from "@/stores/toast";
import { User, Post } from '../interfaces';
import FeedForm from '@/components/FeedForm.vue';

export default defineComponent({
    async beforeRouteUpdate(to, from) {
        // react to route changes...
        await this.getFeeds(to.params.id);
    },
    setup() {
        const userStore = useUserStore();
        const toastStore = useToastStore();
        return {
            userStore,
            toastStore
        }
    },
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
        FeedForm
    },
    data() {
        return {
            posts: [] as Post[],
            user: {} as User,
            can_send_friendship_request: false,
            currentPage: 1,
            hasNext: true

        }
    },
    methods: {
        async sendDirectMessage() {
            axios.get(`/api/chat/get-or-create/${this.$route.params.id}/`).then(
                response => {
                    this.$router.push({
                        name: 'messages',
                        params: {
                            user_id: this.$route.params.id
                        }
                    });
                }
            ).catch(error => {
                console.log(error);
            })
        },
        async getFeeds(userId: string | string[]) {
            this.posts = [];
            await axios.get(`/api/post/profile/${userId}/?page=${this.currentPage}`).then(response => {
                if (!response.data.next) {
                    this.hasNext = false
                }
                this.posts = [...this.posts, ...response.data.results.posts];
                this.user = response.data.results.user
                this.can_send_friendship_request = response.data.results.can_send_friendship_request
            }).catch(error => {
                console.log(error);
            })
        },
        async sendFriendshipRequest() {
            axios.post(`/api/friends/request/${this.$route.params.id}/`).then(response => {
                if (response.data.message == "friendship request created") {
                    this.can_send_friendship_request = false
                    this.toastStore.showToast(5000, "The request was sent!", "bg-emerald-300");
                }
            }).catch(error => {
                console.log(error);
            })
        },
        deletePost(postId: string) {
            this.posts = this.posts.filter(
                post => post.id != postId
            )
        },
        logout() {
            this.userStore.removeToken();
            this.$router.push("/login")
        }
    },
    mounted() {
        this.getFeeds(this.$route.params.id);
        window.onscroll = () => {
            let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight
            if (bottomOfWindow && this.hasNext) {
                console.log(this.currentPage)
                this.currentPage += 1;
                this.getFeeds(this.$route.params.id)
            }
        }
    }
});
</script>