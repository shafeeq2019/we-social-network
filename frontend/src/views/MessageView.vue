<template>
  <div class="mx-auto w-full max-w-[1040px]">
    <div v-if="loading" class="surface flex h-[calc(100dvh-12rem)] items-center justify-center md:h-[calc(100dvh-5rem)]" role="status">
      <Loader2 class="h-6 w-6 animate-spin text-muted-foreground" aria-hidden="true" />
      <span class="sr-only">Loading conversations</span>
    </div>

    <div v-else-if="conversations.length > 0"
         class="surface flex h-[calc(100dvh-12rem)] overflow-hidden md:h-[calc(100dvh-5rem)]">
      <!-- Conversation list -->
      <aside :class="['w-full shrink-0 flex-col border-r border-border/60 md:flex md:w-[300px]', user_id ? 'hidden' : 'flex']"
             aria-label="Conversations">
        <div class="px-5 pb-3 pt-5">
          <h1 class="text-2xl font-extrabold">Messages</h1>
          <p class="text-sm text-muted-foreground">{{ conversations.length }} {{ conversations.length === 1 ? 'conversation' : 'conversations' }}</p>
        </div>
        <ul class="flex-1 space-y-0.5 overflow-y-auto px-2 pb-3">
          <li v-for="conversation in conversations" :key="conversation.id">
            <button type="button" @click="openConversation(conversation)"
                    :aria-current="isActive(conversation) ? 'true' : undefined"
                    :class="['flex w-full items-center gap-3 rounded-2xl p-2.5 text-left transition-colors',
                             isActive(conversation) ? 'bg-primary-soft' : 'hover:bg-muted']">
              <Avatar :src="conversation.users[0].avatar_link" :name="conversation.users[0].name" />
              <span class="min-w-0 flex-1">
                <span :class="['block truncate text-sm font-semibold', isActive(conversation) && 'text-primary-soft-foreground']">
                  {{ conversation.users[0].name }}
                </span>
                <span class="block truncate text-xs text-muted-foreground">Active {{ formatAgo(conversation.modified_ago) }}</span>
              </span>
            </button>
          </li>
        </ul>
      </aside>

      <!-- Chat pane -->
      <section :class="['min-w-0 flex-1 flex-col md:flex', user_id ? 'flex' : 'hidden']" aria-label="Conversation">
        <template v-if="partner">
          <header class="flex items-center gap-3 border-b border-border/60 px-3 py-3 sm:px-5">
            <button type="button" class="icon-btn md:hidden" aria-label="Back to conversations" @click="$router.push({ name: 'messages' })">
              <ArrowLeft class="h-5 w-5" aria-hidden="true" />
            </button>
            <RouterLink :to="{ name: 'profile', params: { id: partner.id } }" class="flex min-w-0 flex-1 items-center gap-3 rounded-2xl">
              <Avatar :src="partner.avatar_link" :name="partner.name" size="sm" />
              <span class="min-w-0">
                <span class="block truncate font-semibold leading-tight">{{ partner.name }}</span>
                <span class="block text-xs text-muted-foreground">View profile</span>
              </span>
            </RouterLink>
            <DropdownMenu>
              <DropdownMenuTrigger class="icon-btn" aria-label="Conversation options">
                <MoreHorizontal class="h-5 w-5" aria-hidden="true" />
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" class="w-52 rounded-2xl p-1.5 shadow-lift">
                <DropdownMenuItem class="cursor-pointer gap-3 rounded-xl px-2.5 py-2"
                                  @select="$router.push({ name: 'profile', params: { id: partner.id } })">
                  <UserRound class="h-4 w-4 text-muted-foreground" aria-hidden="true" /> Show profile
                </DropdownMenuItem>
                <DropdownMenuItem class="menu-item-danger cursor-pointer gap-3 rounded-xl px-2.5 py-2" @select="deleteConversation">
                  <Trash2 class="h-4 w-4" aria-hidden="true" /> Delete conversation
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </header>

          <div id="conversation" class="flex flex-1 flex-col gap-1.5 overflow-y-auto px-4 py-5 sm:px-6" aria-live="polite">
            <p v-if="!activeConversation.messages || activeConversation.messages.length === 0"
               class="m-auto max-w-xs text-center text-sm text-muted-foreground">
              Say hi to {{ partner.name }} — this is the beginning of your conversation.
            </p>
            <template v-for="(message, index) in activeConversation.messages" :key="message.id">
              <div :class="['flex w-full items-end gap-2', isMine(message) ? 'justify-end' : 'justify-start',
                            startsGroup(index) ? 'mt-3' : '']">
                <Avatar v-if="!isMine(message)" :src="message.created_by.avatar_link" :name="message.created_by.name" size="xs"
                        :class="endsGroup(index) ? '' : 'invisible'" />
                <div :class="['flex max-w-[78%] flex-col sm:max-w-[65%]', isMine(message) ? 'items-end' : 'items-start']">
                  <div :class="['whitespace-pre-line break-words px-4 py-2.5 text-[15px] leading-snug',
                                isMine(message)
                                  ? 'rounded-[22px] rounded-br-md bg-primary text-primary-foreground'
                                  : 'rounded-[22px] rounded-bl-md bg-muted text-foreground']">
                    {{ message.message }}
                  </div>
                  <span v-if="endsGroup(index)" class="mt-1 px-1 text-[11px] text-muted-foreground">{{ formatAgo(message.created_ago) }}</span>
                </div>
              </div>
            </template>
          </div>

          <form class="flex items-center gap-2 border-t border-border/60 p-3 sm:p-4" @submit.prevent="submitForm">
            <label for="message-input" class="sr-only">Message {{ partner.name }}</label>
            <input id="message-input" type="text" class="field h-12 flex-1 rounded-full bg-muted/60" v-model="messageText"
                   autocomplete="off" :placeholder="`Message ${partner.name.split(' ')[0]}…`">
            <btn type="submit" size="icon" class="h-12 w-12 shrink-0" :loading="sending" :disabled="!messageText.trim()"
                 aria-label="Send message">
              <SendHorizontal v-if="!sending" class="h-5 w-5" aria-hidden="true" />
            </btn>
          </form>
        </template>

        <div v-else class="m-auto max-w-xs p-6 text-center">
          <MessagesSquare class="mx-auto h-8 w-8 text-muted-foreground" aria-hidden="true" />
          <p class="mt-3 text-sm text-muted-foreground">Select a conversation to start chatting.</p>
        </div>
      </section>
    </div>

    <EmptyState v-else :icon="MessagesSquare" title="No messages yet"
                description="Open someone's profile and tap “Message” to start a conversation.">
      <RouterLink :to="{ name: 'search' }"
                  class="inline-flex h-10 items-center gap-2 rounded-full bg-foreground px-5 text-sm font-semibold text-background transition hover:bg-foreground/85">
        Find people
      </RouterLink>
    </EmptyState>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import {
  ArrowLeft, Loader2, MessagesSquare, MoreHorizontal, SendHorizontal, Trash2, UserRound
} from 'lucide-vue-next';
import {
  useUserStore
} from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Conversation, Message, User } from '../interfaces';
import btn from '@/components/ui/Button.vue';
import Avatar from '@/components/ui/Avatar.vue';
import EmptyState from '@/components/ui/EmptyState.vue';
import { formatAgo } from '@/lib/utils';

export default defineComponent({
  components: {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
    btn,
    Avatar,
    EmptyState,
    ArrowLeft,
    Loader2,
    MoreHorizontal,
    SendHorizontal,
    Trash2,
    UserRound,
    MessagesSquare,
  },
  props: ['user_id'],
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return {
      userStore,
      toastStore,
      formatAgo,
      MessagesSquare
    };
  },
  data() {
    return {
      conversations: [] as Conversation[],
      activeConversation: {} as Conversation,
      messageText: '',
      loading: true,
      sending: false
    };
  },
  computed: {
    partner(): User | undefined {
      if (!this.user_id) {
        return undefined;
      }
      return this.activeConversation.users?.find(user => user.id === this.user_id)
        ?? this.conversations.find(c => c.users[0]?.id === this.user_id)?.users[0];
    }
  },
  methods: {
    isActive(conversation: Conversation): boolean {
      return !!this.user_id && conversation.users[0]?.id === this.user_id;
    },
    isMine(message: Message): boolean {
      return message.created_by.id == this.userStore.user.id;
    },
    startsGroup(index: number): boolean {
      const messages = this.activeConversation.messages ?? [];
      return index > 0 && messages[index - 1].created_by.id !== messages[index].created_by.id;
    },
    endsGroup(index: number): boolean {
      const messages = this.activeConversation.messages ?? [];
      return index === messages.length - 1 || messages[index + 1].created_by.id !== messages[index].created_by.id;
    },
    async getConversationsList() {
      axios.get('/api/chat/').then(async response => {
        this.conversations = response.data.conversations;
        const isWide = window.matchMedia('(min-width: 768px)').matches;
        if (this.conversations.length > 0 && this.user_id) {
          await this.getMessages(this.user_id);
          this.scrollToBottom();
        } else if (this.conversations.length > 0 && !this.user_id && isWide) {
          // on wide screens open the latest conversation; on phones show the list first
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
      if (this.messageText.replace(/\s/g, '').length > 0 && !this.sending) {
        this.sending = true;
        axios.post(`/api/chat/${this.user_id}/messages/`, {
          message: this.messageText
        }).then(async () => {
          this.messageText = '';
          await this.getMessages(this.user_id);
          this.scrollToBottom();
        }).catch(error => {
          console.log(error);
          this.toastStore.showToast(4000, 'Your message could not be sent.', 'bg-red-300');
        }).finally(() => {
          this.sending = false;
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
        await this.$router.push({
          name: 'messages',
        });
        await this.getConversationsList();
        this.toastStore.showToast(3000, 'Conversation deleted', 'bg-emerald-500');
      }).catch(error => {
        console.log(error);
        this.toastStore.showToast(4000, 'The conversation could not be deleted.', 'bg-red-300');
      });
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = document.getElementById('conversation');
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    }
  },
  created() {
    this.getConversationsList();
  }
});
</script>
