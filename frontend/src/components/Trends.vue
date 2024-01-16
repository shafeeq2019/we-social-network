/**
 TODO:
  - update the posts count when adding a new post to a trend
*/ 

<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-md" v-if="trends && trends.length > 0">
        <h3 class="mb-6 text-xl">Trends</h3>
        <div class="space-y-4">
            <div class="flex items-center justify-between" v-for="trend in trends">
                <p class="text-xs">
                    <strong>#{{ trend.hashtag }}</strong><br>
                    <span class="text-gray-500">{{ trend.occurences }} posts</span>
                </p>
                <router-link :to="{ name: 'trendsview', params: { 'hashtag': trend.hashtag } }"
                    class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Explore</router-link>
            </div>
        </div>
    </div>
</template>
<script  lang="ts">
import { defineComponent } from 'vue'
import { Trend } from '../interfaces'
import axios from 'axios';

export default defineComponent({
    data() {
        return {
            trends: [] as Trend[]
        }
    },
    methods: {
        getTrends() {
            axios.get('/api/post/trends/')
                .then(response => {
                    this.trends = response.data
                }).catch(error => {
                    console.log(error)
                })
        }
    },
    created() {
        this.getTrends()
    }
}) 
</script>
