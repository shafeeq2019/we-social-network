import type { Component } from 'vue';
import type { RouteLocationRaw } from 'vue-router';
import { Bell, Home, MessageCircle, Search, Users } from 'lucide-vue-next';

export interface NavItem {
  key: string;
  label: string;
  icon: Component;
  to: RouteLocationRaw;
  // route names that mark this item as active
  match: string[];
  badge?: 'notifications';
}

export function getNavItems(userId: string): NavItem[] {
  return [
    { key: 'feed', label: 'Home', icon: Home, to: { name: 'feed' }, match: ['feed', 'home', 'postview', 'trendsview'] },
    { key: 'search', label: 'Explore', icon: Search, to: { name: 'search' }, match: ['search'] },
    { key: 'messages', label: 'Messages', icon: MessageCircle, to: { name: 'messages' }, match: ['messages'] },
    { key: 'notifications', label: 'Notifications', icon: Bell, to: { name: 'notifications' }, match: ['notifications'], badge: 'notifications' },
    { key: 'friends', label: 'Friends', icon: Users, to: { name: 'friends', params: { id: userId } }, match: ['friends'] },
  ];
}
