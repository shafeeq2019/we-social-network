<template lang="">
  <div class="mb-4 flex items-center justify-between text-xs">
    <router-link :to="{ name: 'profile', params: { 'id': comment.created_by.id } }">
      <div class="flex items-center space-x-3">
        <img :src="comment.created_by.avatar_link" class="w-[40px] h-[39px] rounded-full">
        <p><strong>{{comment.created_by.name}}</strong></p>
      </div>
    </router-link>

    <p class="text-secondary">{{ /^0\s+minutes$/.test(comment.created_ago) ? 'Just now' : comment.created_ago}}</p>
  </div>
  <div class="flex justify-between text-sm">
    <p> {{ comment.comment}} </p>
    <div class="flex items-end">
      <DropdownMenu>
        <DropdownMenuTrigger>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
               stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z">
            </path>
          </svg>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="bg-background">
          <DropdownMenuItem class="cursor-pointer flex space-x-2 items-center" @click="deleteComment"
                            v-if="userStore.user.id === comment.created_by.id">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                 stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
            </svg>
            <p>Delete comment</p>
          </DropdownMenuItem>
          <!-- <DropdownMenuSeparator /> -->
          <DropdownMenuItem v-if="userStore.user.id != comment.created_by.id"
                            class="cursor-pointer flex space-x-2 items-center" @click="openReportModal = true">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                 stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
            </svg>
            <p>Report</p>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>

  </div>

</template>

<script lang="ts">
import { Comment } from '../interfaces';
import {
  PropType,
} from 'vue';
import {
  useToastStore
} from '@/stores/toast';
import {
  useUserStore
} from '@/stores/user';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

import axios from 'axios';
export default {
  emits: ['deleteComment'],
  props: {
    comment: {
      type: Object as PropType<Comment>,
      required: true
    },
  },
  components: {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return {
      userStore,
      toastStore
    };
  },
  methods: {
    deleteComment() {
      axios.delete(`/api/post/${this.$route.params.id}/comment/${this.comment?.id}/`).then(
        () => {
          this.$emit('deleteComment', this.comment.id);
        }
      ).catch(error => {
        console.log(error);
      });
    },
    openReportModal() {

    }
  },
  created() {
  }
};
</script>

<style></style>
