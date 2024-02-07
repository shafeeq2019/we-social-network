/**
TODO:
- scroll to the end of the chat automatically when open it
- delete message Button
- dont show empty conversation
- real time messaging
*/

<template lang="">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4" v-if="conversations.length > 0">
        <div class="main-left col-span-1">
            <div class="bg-white border border-gray-200 rounded-lg text-center shadow-md">
                <div class="flex items-center justify-between cursor-pointer pl-4 py-2 group"
                    v-for="conversation in conversations" @click="openConversation(conversation)" :key="conversation.id"
                    :class="{ 'bg-gray-300 rounded-lg': activeConversation.id == conversation.id, 
                        ' shadow-md' : conversation.id == conversations[conversations.length-1].id  ,
                        'hover:bg-gray-200 hover:rounded-lg':activeConversation.id != conversation.id}">
                    <div class="flex items-center space-x-2">
                        <img :src="conversation.users[0].avatar_link"
                            class="mx-auto w-12 h-12 rounded-full object-cover object-center">
                        <p class="text-xs font-bold hidden sm:block"> {{conversation.users[0].name}} </p>
                    </div>
                    <div>
                        <DropdownMenu>
                            <DropdownMenuTrigger class="sm:invisible group-hover:visible hover:bg-gray-400 hover:rounded-xl">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="" viewBox="0 0 24 24" stroke-width="1.5"
                                    stroke="currentColor" class="w-8 h-8 block">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z">
                                    </path>
                                </svg>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent>
                                <DropdownMenuItem class="cursor-pointer" @click="deleteConversation">Delete Conversation
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                    </div>

                </div>
            </div>
        </div>
        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                <div class="flex flex-col flex-grow p-4 h-[calc(100vh-339px)] overflow-auto">
                    <template v-for="message in activeConversation.messages" :key="message.id">
                        <!--sent messages-->
                        <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
                            v-if="message.created_by.id == userStore.user.id">
                            <div>
                                <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                    <p class="text-sm"> {{message.message}}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{message.created_ago}}</span>
                            </div>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img :src="message.created_by.avatar_link"
                                    class="mx-auto w-11 h-11 rounded-full object-cover object-center">
                            </div>
                        </div>
                        <!--received messages-->
                        <div class="flex w-full mt-2 space-x-3 max-w-md"
                            v-if="message.created_by.id != userStore.user.id">
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img :src="message.created_by.avatar_link"
                                    class="mx-auto w-11 h-11 rounded-full object-cover object-center">
                            </div>
                            <div>
                                <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                                    <p class="text-sm"> {{message.message}}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{message.created_ago}}</span>
                            </div>
                        </div>
                    </template>
                </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg">
                <form @submit.prevent="submitForm">
                    <div class="p-4">
                        <textarea class="w-full bg-gray-100 rounded-lg p-4 resize-none" v-model="messageText"
                            @keydown.enter.prevent="submitForm" placeholder="What do you want to say?" rows=""
                            cols=""></textarea>
                    </div>
                    <div class="mb-2 border-t border-gray-100 p-4 flex justify-between">
                        <button href="#"
                            class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Send</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <div v-else-if="!loading" class="max-w-lg mx-auto bg-white shadow-md sm:rounded-lg p-6">
        <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
                stroke="currentColor" class="h-40 w-40 text-purple-600 mx-auto ">
                <path strokeLinecap="round" strokeLinejoin="round"
                    d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
            </svg>
            <p class="mt-2 text-xl font-semibold text-gray-700">You don't have any messages</p>
        </div>
    </div>

</template>
<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios';
import {
    useUserStore
} from '@/stores/user';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Conversation, User } from '../interfaces';

export default defineComponent({
    components: {
        DropdownMenu,
        DropdownMenuContent,
        DropdownMenuItem,
        DropdownMenuLabel,
        DropdownMenuSeparator,
        DropdownMenuTrigger,
    },
    props: ['user_id'],
    setup() {
        const userStore = useUserStore()
        return {
            userStore,
            loading: true
        }
    },
    data() {
        return {
            conversations: [] as Conversation[],
            activeConversation: {} as Conversation,
            messageText: ''
        }
    },
    methods: {
        async getConversationsList() {
            axios.get('/api/chat/').then(async response => {
                this.conversations = response.data.conversations;
                if (this.conversations.length > 0 && this.user_id) {
                    await this.getMessages(this.user_id)
                } else if (this.conversations.length > 0 && !this.user_id) {
                    this.activeConversation = this.conversations[0]
                    await this.openConversation(this.conversations[0])
                }
                this.loading = false;
            }).catch(error => {
                this.loading = false;
                console.log(error);
            })
        },
        async getMessages(user_id: string) {
            axios.get(`/api/chat/${user_id}/`).then(response => {
                this.activeConversation = response.data.conversation
            }).catch(error => {
                console.log(error)
            })
        },
        async submitForm() {
            if (this.messageText.replace(/\s/g, '').length > 0) {
                axios.post(`/api/chat/${this.user_id}/messages/`, {
                    message: this.messageText
                }).then(async response => {
                    this.messageText = ''
                    //this.activeConversation.messages.push(response.data.message)
                    await this.getMessages(this.user_id)
                }).catch(error => {
                    console.log(error)
                })
            }
        },
        async openConversation(conversation: Conversation) {
            await this.$router.push({
                name: 'messages',
                params: {
                    user_id: conversation.users[0].id
                }
            });
            await this.getMessages(this.user_id);
        },
        async deleteConversation() {
            axios.delete(`/api/chat/${this.user_id}/`).then(async response => {
                this.activeConversation = {} as Conversation;
                await this.getConversationsList();
                await this.$router.push({
                    name: 'messages',
                });
            })
        }
    },
    created() {
        this.getConversationsList()
    }
})
</script>