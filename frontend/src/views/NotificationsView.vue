<template>
  <PageLayout>
    <PageHeader title="Notifications"
                :description="loading ? '' : notifications.length ? `${notifications.length} unread` : 'Nothing new'" />

    <div v-if="loading" class="surface divide-y divide-border/60" aria-hidden="true">
      <div v-for="n in 4" :key="n" class="flex items-center gap-4 p-4">
        <div class="skeleton h-11 w-11 rounded-full" />
        <div class="flex-1 space-y-2">
          <div class="skeleton h-3.5 w-3/4" />
          <div class="skeleton h-3 w-1/3" />
        </div>
      </div>
    </div>

    <ul v-else-if="notifications.length" class="surface divide-y divide-border/60 overflow-hidden">
      <li v-for="notification in notifications" :key="notification.id">
        <button type="button" @click="readNotification(notification)" :disabled="openingId === notification.id"
                class="group flex w-full items-center gap-4 px-4 py-4 text-left transition-colors hover:bg-muted/70 focus-visible:bg-muted/70 focus-visible:ring-inset focus-visible:ring-offset-0 sm:px-5">
          <span class="relative shrink-0">
            <Avatar :src="notification.created_by.avatar_link" :name="notification.created_by.name" />
            <span :class="['absolute -bottom-1 -right-1 flex h-6 w-6 items-center justify-center rounded-full ring-[3px] ring-card', meta(notification).tone]">
              <component :is="meta(notification).icon" class="h-3 w-3" :stroke-width="2.6" aria-hidden="true" />
            </span>
          </span>
          <span class="min-w-0 flex-1">
            <span class="block text-[15px] leading-snug">{{ notification.body }}</span>
            <span class="mt-0.5 block text-xs font-medium text-muted-foreground">{{ meta(notification).label }}</span>
          </span>
          <span class="h-2.5 w-2.5 shrink-0 rounded-full bg-primary" aria-label="Unread" />
          <Loader2 v-if="openingId === notification.id" class="h-4 w-4 animate-spin text-muted-foreground" aria-hidden="true" />
          <ChevronRight v-else class="h-4 w-4 shrink-0 text-muted-foreground transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
        </button>
      </li>
    </ul>

    <EmptyState v-else :icon="BellRing" title="You're all caught up"
                description="Likes, comments and friend requests will show up here." />
  </PageLayout>
</template>

<script lang="ts">
import { defineComponent, type Component } from 'vue';
import {
  BellRing, ChevronRight, Heart, Loader2, MessageCircle, UserCheck, UserPlus, UserX
} from 'lucide-vue-next';
import PageLayout from '@/components/layout/PageLayout.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import EmptyState from '@/components/ui/EmptyState.vue';
import Avatar from '@/components/ui/Avatar.vue';
import { useNotificationStore } from '@/stores/notifications';
import { Notification } from '../interfaces.ts';
import axios from 'axios';

const META: Record<string, { icon: Component; tone: string; label: string }> = {
  post_like: { icon: Heart, tone: 'bg-like text-white', label: 'Liked your post' },
  post_comment: { icon: MessageCircle, tone: 'bg-primary text-primary-foreground', label: 'Commented on your post' },
  new_friendrequest: { icon: UserPlus, tone: 'bg-foreground text-background', label: 'Friend request' },
  accepted_friendrequest: { icon: UserCheck, tone: 'bg-success text-white', label: 'Request accepted' },
  rejected_friendrequest: { icon: UserX, tone: 'bg-muted-foreground text-background', label: 'Request declined' },
};

export default defineComponent({
  components: {
    PageLayout,
    PageHeader,
    EmptyState,
    Avatar,
    ChevronRight,
    Loader2,
  },
  setup() {
    const notificationStore = useNotificationStore();
    return { notificationStore, BellRing };
  },
  data() {
    return {
      notifications: [] as Notification[],
      loading: true,
      openingId: ''
    };
  },
  methods: {
    meta(notification: Notification) {
      return META[notification.type_of_notification] ?? META.new_friendrequest;
    },
    async getNotifications() {
      axios
        .get('/api/notification/')
        .then((response) => {
          this.notifications = response.data.results;
          this.notificationStore.unread = response.data.count ?? this.notifications.length;
        })
        .catch((error) => console.log(error))
        .finally(() => {
          this.loading = false;
        });
    },
    async readNotification(notification: Notification) {
      this.openingId = notification.id;
      axios
        .get(`/api/notification/read/${notification.id}/`)
        .then(() => {
          this.notificationStore.markOneRead();
          if (
            notification.type_of_notification == 'post_like' ||
                        notification.type_of_notification == 'post_comment'
          ) {
            this.$router.push({ name: 'postview', params: { id: notification.post_id } });
          } else if (
            notification.type_of_notification == 'accepted_friendrequest' ||
                        notification.type_of_notification == 'rejected_friendrequest'
          ) {
            this.$router.push({
              name: 'profile',
              params: { id: notification.created_by.id },
            });
          } else {
            this.$router.push({
              name: 'friends',
              params: { id: notification.created_for_id },
            });
          }
        })
        .catch((error) => console.log(error))
        .finally(() => {
          this.openingId = '';
        });
    },
  },
  created() {
    this.getNotifications();
  },
});
</script>
