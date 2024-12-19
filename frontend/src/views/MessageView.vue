/**
TODO:
- real time messaging
*/

<template lang="">
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4 text-primary" v-if="conversations.length > 0">
    <div class="main-left col-span-1">
      <div class="bg-primary border border-border rounded-lg text-center shadow-md">
        <div class="flex items-center justify-between cursor-pointer pl-4 py-2 group"
             v-for="conversation in conversations" @click="openConversation(conversation)" :key="conversation.id"
             :class="{ 'bg-secondary rounded-lg': activeConversation.id == conversation.id,
                       ' shadow-md' : conversation.id == conversations[conversations.length-1].id ,
                       'hover:bg-primary-hover hover:rounded-lg':activeConversation.id != conversation.id}">
          <div class="flex items-center space-x-2">
            <img :src="conversation.users[0].avatar_link"
                 class="mx-auto w-9 h-9  sm:w-12 sm:h-12 rounded-full object-cover object-center">
            <p class="text-xs font-bold hidden sm:block"> {{conversation.users[0].name}} </p>
          </div>
          <div>
            <DropdownMenu>
              <DropdownMenuTrigger
                class="sm:invisible group-hover:visible hover:bg-gray-400 hover:rounded-lg mx-1">
                <svg xmlns="http://www.w3.org/2000/svg" fill="" viewBox="0 0 24 24" stroke-width="1.5"
                     stroke="currentColor" class="w-5 h-5 sm:w-8 sm:h-8 block">
                  <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z">
                  </path>
                </svg>
              </DropdownMenuTrigger>
              <DropdownMenuContent class="bg-background">
                <DropdownMenuItem class="cursor-pointer flex space-x-2 items-center" @click="$router.push({ name: 'profile', params: { id: conversation.users[0].id } })">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                       stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                          d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                  </svg>
                  <p>Show profile</p>
                </DropdownMenuItem>
                <DropdownMenuItem class="cursor-pointer flex space-x-2 items-center"
                                  @click="deleteConversation">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                       stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                          d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                  </svg>
                  <p>Delete Conversation</p>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </div>
    </div>
    <div class="main-center col-span-3 space-y-4">
      <div class="bg-foreground border border-border rounded-lg">
        <div class="flex flex-col flex-grow p-4 h-[calc(100vh-212px)] overflow-auto" id="conversation">
          <template v-for="message in activeConversation.messages" :key="message.id">
            <!--sent messages-->
            <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
                 v-if="message.created_by.id == userStore.user.id">
              <div>
                <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                  <p class="text-sm text-right"> {{message.message}}</p>
                </div>
                <span class="text-xs text-secondary leading-none">{{message.created_ago}}</span>
              </div>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-secondary">
                <img :src="message.created_by.avatar_link"
                     class="mx-auto w-11 h-11 rounded-full object-cover object-center">
              </div>
            </div>
            <!--received messages-->
            <div class="flex w-full mt-2 space-x-3 max-w-md"
                 v-if="message.created_by.id != userStore.user.id">
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-secondary">
                <img :src="message.created_by.avatar_link"
                     class="mx-auto w-11 h-11 rounded-full object-cover object-center">
              </div>
              <div>
                <div class="bg-secondary p-3 rounded-r-lg rounded-bl-lg">
                  <p class="text-sm"> {{message.message}}</p>
                </div>
                <span class="text-xs text-secondary leading-none">{{message.created_ago}}</span>
              </div>
            </div>
          </template>
        </div>
      </div>

      <div class="bg-foreground border border-border rounded-lg">
        <form @submit.prevent="submitForm">
          <div class="p-4 flex space-x-3">
            <input type="text" name="" id="" class="w-full bg-background rounded-lg p-4 " v-model="messageText"
                   @keydown.enter.prevent="submitForm" placeholder="What do you want to say?">
            <button class="inline-block py-3 px-3 bg-button-primary text-white rounded-lg" type="submit">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                   stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
              </svg>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
  <div v-else-if="!loading" class="max-w-lg mx-auto bg-foreground shadow-md sm:rounded-lg p-6">
    <div class="text-center">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
           stroke="currentColor" class="h-40 w-40 text-purple-600 mx-auto ">
        <path strokeLinecap="round" strokeLinejoin="round"
              d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
      </svg>
      <p class="mt-2 text-xl font-semibold text-desc">You don't have any messages</p>
    </div>
  </div>

</template>
<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import {
  useUserStore
} from '@/stores/user';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Conversation } from '../interfaces';

export default defineComponent({
  components: {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
  },
  props: ['user_id'],
  setup() {
    const userStore = useUserStore();
    return {
      userStore,
      loading: true
    };
  },
  data() {
    return {
      conversations: [] as Conversation[],
      activeConversation: {} as Conversation,
      messageText: ''
    };
  },
  methods: {
    async getConversationsList() {
      axios.get('/api/chat/').then(async response => {
        this.conversations = response.data.conversations;
        if (this.conversations.length > 0 && this.user_id) {
          await this.getMessages(this.user_id);
          this.scrollToBottom();
        } else if (this.conversations.length > 0 && !this.user_id) {
          this.activeConversation = this.conversations[0];
          await this.openConversation(this.conversations[0]);
        }
        this.loading = false;
      }).catch(error => {
        this.loading = false;
        console.log(error);
      });
    },
    async getMessages(user_id: string) {
      return axios.get(`/api/chat/${user_id}/`).then(response => {
        this.activeConversation = response.data.conversation;
      }).catch(error => {
        console.log(error);
      });
    },
    async submitForm() {
      if (this.messageText.replace(/\s/g, '').length > 0) {
        axios.post(`/api/chat/${this.user_id}/messages/`, {
          message: this.messageText
        }).then(async () => {
          this.messageText = '';
          //this.activeConversation.messages.push(response.data.message)
          await this.getMessages(this.user_id);
        }).catch(error => {
          console.log(error);
        });
      }
    },
    async openConversation(conversation: Conversation) {
      this.messageText = '';
      await this.$router.push({
        name: 'messages',
        params: {
          user_id: conversation.users[0].id
        }
      });
      await this.getMessages(this.user_id);
      this.scrollToBottom();
    },
    async deleteConversation() {
      axios.delete(`/api/chat/${this.user_id}/`).then(async () => {
        this.activeConversation = {} as Conversation;
        await this.getConversationsList();
        await this.$router.push({
          name: 'messages',
        });
      });
    },
    scrollToBottom() {
      const container = document.getElementById("conversation");
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }
  },
  created() {
    this.getConversationsList();
  }
});
</script>
