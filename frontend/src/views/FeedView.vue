<template lang="">
    <div class="max-w-7xl mx-auto grid-cols-4 gap-4 hidden md:grid">
        <div class="main-center col-span-3 space-y-4">
            <FeedForm :user="null" :posts="posts" />
            <FeedItem v-for="post in posts" :post="post" :key="post.id" @deletePost="deletePost"
                v-if="posts.length > 0" />
            <div v-else-if="!loading" class="bg-white shadow-md sm:rounded-lg p-6">
                <div class="text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
                        stroke="currentColor" class="h-36 w-40 text-purple-600 mx-auto ">
                        <path strokeLinecap="round" strokeLinejoin="round"
                            d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                    </svg>
                    <p class="mt-2 text-xl font-semibold text-gray-700">You don't have any posts yet and no friends
                        either. Create a new post or add friends to see new feeds</p>
                </div>
            </div>
        </div>
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>

    <div class="max-w-7xl mx-auto md:hidden space-y-4">
        <FeedForm :user="null" :posts="posts" />
        <PeopleYouMayKnow />
        <Trends />
        <FeedItem v-for="post in posts" :post="post" :key="post.id" @deletePost="deletePost" v-if="posts.length > 0" />
        <div v-else-if="!loading" class="bg-white shadow-md sm:rounded-lg p-6">
            <div class="text-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
                    stroke="currentColor" class="h-36 w-40 text-purple-600 mx-auto ">
                    <path strokeLinecap="round" strokeLinejoin="round"
                        d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                </svg>
                <p class="mt-2 text-xl font-semibold text-gray-700">You don't have any posts yet and no friends
                    either. Create a new post or add friends to see new feeds</p>
            </div>
        </div> 

    </div>
</template>
<script lang="ts">
import {
    defineComponent
} from 'vue'
import axios from 'axios';
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import FeedForm from '@/components/FeedForm.vue';
import {
    Post
} from '../interfaces.ts'
export default defineComponent({
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
        FeedForm
    },
    data() {
        return {
            posts: [] as Post[],
            body: '',
            currentPage: 1,
            hasNext: true,
            loading: true
        }
    },
    methods: {
        async getFeeds() {
            await axios.get(`/api/post/?page=${this.currentPage}`).then(response => {
                if (response.data.next) {
                    this.hasNext = true
                }
                this.loading = false;
                this.posts = [...this.posts, ...response.data.results]
            }).catch(error => {
                this.loading = false;
                console.log(error);
            })
        },
        deletePost(postId: string) {
            this.posts = this.posts.filter(
                post => post.id != postId
            )
        }
    },
    mounted() {
        const onScroll = () => {
            let bottomOfWindow = parseInt(`${document.documentElement.scrollTop + window.innerHeight}`) === document.documentElement.offsetHeight
            if (bottomOfWindow && this.hasNext) {
                this.currentPage += 1;
                this.hasNext = false;
                this.getFeeds()
            }
        }
        this.getFeeds();
        window.onscroll = onScroll;
        window.ontouchmove = onScroll;
    }
});
</script>
<style lang=""></style>