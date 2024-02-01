<template lang="">
    <div class="mb-4 max-w-7xl mx-auto">
        <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-md">
            <h2 class="text-xl font-semibold">Trend: #{{hashtag}}</h2>
        </div>
    </div>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!-- New post & feeds on the middle -->
        <div class="main-center col-span-4 md:col-span-3 space-y-4">
            <FeedItem v-for="post in posts" :post="post" :key="post.id"  @deletePost="deletePost"/>
        </div>

        <!-- People you may know -->
        <div class="main-right col-span-1 space-y-4 hidden md:block">
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
import FeedItem from '../components/FeedItem.vue'
import { Post } from '../interfaces';

export default defineComponent({
    props: ['hashtag'],
    async beforeRouteUpdate(to, from) {
        this.posts = [];
        await this.getFeeds(to.params.hashtag);
    },
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem
    },
    data() {
        return {
            posts: [] as Post[],
            currentPage: 1,
            hasNext: true
        }
    },
    methods: {
        async getFeeds(hashtag: string | string[]) {
            await axios.get(`/api/post?trend=${hashtag}&page=${this.currentPage}`).then(response => {
                if (response.data.next) {
                    this.hasNext = true
                }
                this.posts = [...this.posts, ...response.data.results];
            }).catch(error => {
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
                this.getFeeds(this.hashtag)
            }
        }

        this.getFeeds(this.hashtag);
        window.onscroll = onScroll;
        window.ontouchmove = onScroll;
    }
});
</script>
<style lang=""></style>