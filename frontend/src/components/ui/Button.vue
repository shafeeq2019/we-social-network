<template>
  <button
    :class="cn(buttonVariants({ variant, size }))"
    :disabled="disabled || loading"
    :aria-busy="loading || undefined"
    >
    <Loader2 v-if="loading" class="h-4 w-4 animate-spin" aria-hidden="true" />
    <slot>Button</slot>
  </button>
</template>

<script setup lang="ts">
import { cva, type VariantProps } from 'class-variance-authority';
import { Loader2 } from 'lucide-vue-next';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  [
    'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-full font-semibold',
    'transition-[background-color,color,box-shadow,transform] duration-150 ease-out',
    'active:scale-[0.97] disabled:pointer-events-none disabled:opacity-50',
  ],
  {
    variants: {
      variant: {
        primary: ['bg-primary text-primary-foreground shadow-glow hover:brightness-110'],
        secondary: ['bg-muted text-foreground hover:bg-foreground/10'],
        soft: ['bg-primary-soft text-primary-soft-foreground hover:bg-primary/15'],
        outline: ['border border-border bg-card text-foreground hover:bg-muted'],
        ghost: ['text-muted-foreground hover:bg-muted hover:text-foreground'],
        destructive: ['bg-destructive text-destructive-foreground hover:brightness-110'],
        ink: ['bg-foreground text-background hover:bg-foreground/85'],
      },
      size: {
        default: ['h-10 px-4 text-sm'],
        sm: ['h-9 px-3.5 text-[13px]'],
        lg: ['h-12 px-6 text-[15px]'],
        icon: ['h-10 w-10 p-0'],
        // legacy aliases
        small: ['h-9 px-3.5 text-[13px]'],
        big: ['h-12 px-6 text-[15px]'],
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
    loading?: boolean;
  }>(),
  {
    variant: 'primary',
    size: 'default',
    disabled: false,
    loading: false,
  },
);
</script>
