/**
 TODO:
  - update posts count without refreshing the page when posting a new post
*/ 

<template lang="">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!-- User on the left -->
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <div class="flex items-center justify-center">
                    <img src="https://i.pravatar.cc/200?img=57" class="mb-6 rounded-full" />
                </div>

                <p><strong>{{user.name}}</strong></p>
                <div class="mt-6 flex space-x-8 justify-around">
                    <router-link :to="{name:'friends', params:{id: user.id} }" class="text-xs text-gray-500">
                        {{user.friends_count}} friends</router-link>
                    <p class="text-xs text-gray-500">{{user.posts_count}} posts</p>
                </div>

                <div class="mt-6 space-y-2">
                    <button v-if="user.id != userStore.user.id && can_send_friendship_request"
                        class="inline-block py-2 px-1 bg-purple-600 text-white rounded-md text-xs w-full"
                        @click="sendFriendshipRequest"> Send friendship request</button>
                    <button v-if="user.id != userStore.user.id"
                        class="inline-block py-2 px-1 bg-purple-600 text-white rounded-md text-xs w-full"
                        @click="sendDirectMessage"> Send direct message</button>
                    <button v-if="userStore.user.id && user.id == userStore.user.id"
                        class="inline-block py-2 px-1 bg-red-600 text-white rounded-md text-xs w-full" @click="logout">
                        Logut
                    </button>

                </div>
            </div>
        </div>
        <!-- New post & feeds on the middle -->
        <div class="main-center col-span-2 space-y-4">
            <form method="post" @submit.prevent="submitForm" v-if="userStore.user.id == user.id">
                <div class="bg-white border border-gray-200 rounded-lg">
                    <div class="p-4">
                        <textarea class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"
                            v-model="body"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach
                            image</button>
                        <button type="submit"
                            class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    </div>
                </div>
            </form>

            <FeedItem v-for="post in posts" :user="user" :post="post" :key="post.id" />
        </div>

        <!-- People you may know -->
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>

    </div>
</template>
<script>
import axios from 'axios';
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import {
    useUserStore
} from '@/stores/user'
import FeedItem from '../components/FeedItem.vue'
import {
    useToastStore
} from "@/stores/toast";

export default {
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
        FeedItem
    },
    data() {
        return {
            posts: [],
            user: {},
            body: '',
            can_send_friendship_request: false
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
        async getFeeds(userId) {
            await axios.get(`/api/post/profile/${userId}/`).then(response => {
                this.posts = response.data.posts;
                this.user = response.data.user
                this.can_send_friendship_request = response.data.can_send_friendship_request
            }).catch(error => {
                console.log(error);
            })
        },
        async submitForm() {
            axios.post("/api/post/create/", {
                "body": this.body
            }).then(response => {
                this.body = '';
                this.posts = [response.data, ...this.posts];
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
        logout() {
            this.userStore.removeToken();
            this.$router.push("/login")
        }
    },
    created() {
        this.getFeeds(this.$route.params.id);
    }
};
</script>
<style lang=""></style>