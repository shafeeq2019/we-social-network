<template lang="">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!-- New post & feeds on the middle -->
        <div class="main-center col-span-3 space-y-4">
            <FeedForm :user="null" :posts="posts"/>
            <FeedItem v-for="post in posts" :post="post" :key="post.id" />
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
import FeedItem from '../components/FeedItem.vue'
import FeedForm from '@/components/FeedForm.vue';
import { Post } from '../interfaces.ts'
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
            hasNext: true
        }
    },
    methods: {
        async getFeeds() {
            await axios.get(`/api/post/?page=${this.currentPage}`).then(response => {
                if (!response.data.next) {
                    this.hasNext = false
                }
                this.posts = [...this.posts, ...response.data.results]
            }).catch(error => {
                console.log(error);
            })
        }
    },
    mounted() {
        this.getFeeds();
        window.onscroll = () => {
            let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight
            if (bottomOfWindow && this.hasNext) {
                console.log(this.currentPage)
                this.currentPage += 1;
                this.getFeeds()
            }
        }
    }
});
</script>
<style lang=""></style>