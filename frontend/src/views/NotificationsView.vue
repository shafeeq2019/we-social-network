<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4 text-primary">
    <div class="main-center col-span-4 md:col-span-3">
      <div v-if="notifications.length" class="flex flex-col gap-2">
        <div class="p-3 bg-foreground border border-border rounded-lg flex justify-start items-center"
             v-for="notification in notifications" v-bind:key="notification.id">
          <router-link :to="{ name: 'profile', params: { id: notification.created_by.id } }">
            <div class="flex items-center space-x-3">
              <img :src="notification.created_by.avatar_link" class="w-[40px] h-[39px] rounded-full" />
            </div>
          </router-link>
          <p class="ml-3">{{ notification.body }}</p>
          <button class="ml-2 underline" @click="readNotification(notification)">
            Read more
          </button>
        </div>
      </div>
      <div v-else class="p-4 bg-foreground border border-border rounded-lg">
        You don't have any unread notifications!
      </div>
    </div>
    <!-- People you may know -->
    <div class="main-right col-span-1 space-y-4 hidden md:block">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import PeopleYouMayKnow from "@/components/PeopleYouMayKnow.vue";
import Trends from "@/components/Trends.vue";
import { Notification } from "../interfaces.ts";
import axios from "axios";

export default defineComponent({
  components: {
    Trends,
    PeopleYouMayKnow,
  },
  data() {
    return {
      notifications: [] as Notification[],
    };
  },
  methods: {
    async getNotifications() {
      axios
        .get("/api/notification/")
        .then((response) => {
          this.notifications = response.data.results;
          console.log(response);
        })
        .catch((error) => console.log(error));
    },
    async readNotification(notification: Notification) {
      axios
        .get(`/api/notification/read/${notification.id}/`)
        .then(() => {
          if (
            notification.type_of_notification == "post_like" ||
                        notification.type_of_notification == "post_comment"
          ) {
            this.$router.push({ name: "postview", params: { id: notification.post_id } });
          } else if (
            notification.type_of_notification == "accepted_friendrequest" ||
                        notification.type_of_notification == "rejected_friendrequest"
          ) {
            this.$router.push({
              name: "profile",
              params: { id: notification.created_by.id },
            });
          } else {
            this.$router.push({
              name: "friends",
              params: { id: notification.created_for_id },
            });
          }
        })
        .catch((error) => console.log(error));
    },
  },
  created() {
    this.getNotifications();
  },
});
</script>
