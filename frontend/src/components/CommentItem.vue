<template lang="">
    <div class="mb-6 flex items-center justify-between">
        <router-link :to="{ name: 'profile', params: { 'id': comment.created_by.id } }">
            <div class="flex items-center space-x-3">
                <img :src="comment.created_by.avatar_link" class="w-[40px] h-[39px] rounded-full">

                <p><strong>{{comment.created_by.name}}</strong></p>
            </div>
        </router-link>

        <p class="text-gray-600">{{ /^0\s+minutes$/.test(comment.created_ago) ? 'Just now' : comment.created_ago}}</p>
    </div>
    <p> {{ comment.comment}} </p>
</template>
<script  lang="ts">
import { defineComponent } from 'vue'
    export default {
        props: {
            comment: Object
        },
        methods: {},
        created() {}
    }
</script>
<style lang="">

</style>