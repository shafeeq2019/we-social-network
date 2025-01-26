<template>
  <button
    :class="cn(buttonVariants({ variant, size }))"
    :disabled="disabled"
    >
    <slot>Button</slot>
  </button>
</template>

<script setup lang="ts">
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  ['inline-block text-white rounded-lg items-center'],
  {
    variants: {
      variant: {
        primary: ['bg-button-primary text-white'],
        secondary: ['bg-button-secondary text-white'],
      },
      size: {
        default: ['px-3 py-1'],
        small: ['p-2 sm:p-1 text-xs'],
        big: ['p-2 sm:py-2 sm:px-6 text-sm sm:text-base'],
      }
    },
    defaultVariants: {
      variant: 'primary',
      size: 'default'
    }
  }
);

type ButtonProps = VariantProps<typeof buttonVariants>;

withDefaults(
  defineProps<{
    variant?: ButtonProps['variant'];
    size?: ButtonProps['size'];
    disabled?: boolean;
  }>(),
  {
    variant: 'primary',
    size: 'default',
    disabled: false,
  },
);
</script>
