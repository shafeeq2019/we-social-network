<template>
  <PageLayout>
    <EmptyState :icon="MapPinOff" title="Page not found"
                description="The page you are looking for doesn't exist or was moved.">
      <RouterLink :to="{ name: 'feed' }" class="text-sm font-semibold text-primary-soft-foreground hover:underline dark:text-primary">
        Back to your feed
      </RouterLink>
    </EmptyState>
  </PageLayout>
</template>

<script setup lang="ts">
import { MapPinOff } from 'lucide-vue-next';
import PageLayout from '@/components/layout/PageLayout.vue';
import EmptyState from '@/components/ui/EmptyState.vue';
</script>
