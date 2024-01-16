<template lang="">
    <div
        class="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-4 xl:grid-cols-4 gap-4  gap-4">
        <div class="main-center col-span-1 lg:col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                <form class="p-4 flex space-x-4" @submit.prevent="submitForm">
                    <input type="search" class="p-4 w-full bg-gray-100 rounded-lg" v-model="query"
                        placeholder="What are you looking for?">
                    <button href="#" class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg" type="submit">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
                        </svg>
                    </button>
                </form>
            </div>

            <div v-if="users.length > 0"
                class="bg-white border border-gray-200 rounded-lg p-4 grid grid-cols-1 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-4 gap-4">
                <router-link :to="{ name: 'profile', params: { 'id': user.id } }" v-for="user in users">
                    <div class="p-4 text-center bg-gray-100 rounded-lg hover:bg-gray-200">
                        <img :src="user.avatar_link" class="mb-6 rounded-full w-44 h-44 mx-auto">
                        <p><strong>{{user.name}}</strong></p>
                        <div class="mt-6 flex space-x-8 justify-around">
                            <p class="text-xs text-gray-500">{{user.friends_count}} friends</p>
                            <p class="text-xs text-gray-500">{{user.posts_count}} posts</p>
                        </div>
                    </div>
                </router-link>
            </div>
            <FeedItem v-for="post in posts" :post="post" />
        </div>

        <!-- People you may know -->
        <div class="main-right col-span-1 lg:col-span-1 space-y-4">
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
import FeedItem from '../components/FeedItem.vue';

export default defineComponent({
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem
    },
    data() {
        return {
            query: '',
            users: [],
            posts: []
        }
    },
    methods: {
        submitForm() {
            axios.post('api/search/', {
                query: this.query
            }).then(response => {
                this.users = response.data.users;
                this.posts = response.data.posts
            }).catch(e => {
                console.log("error", e);
            })
        }
    }
})
</script>
<style lang="">

</style>