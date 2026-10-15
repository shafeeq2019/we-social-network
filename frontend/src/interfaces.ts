export interface User {
  id: string;
  email?: string;
  name: string;
  friends_count: number;
  posts_count: number;
  avatar_link: string;
}

export interface Message {
  id: string;
  message: string;
  created_at: string;
  created_ago: string;
  created_by: User;
  sent_to: User;
}

export interface Conversation {
  id: string;
  modified_ago: string;
  users: User[];
  messages?: Message[];
}

export interface LoginUser {
  isAuthenticated: boolean;
  id: string;
  name: string;
  email: string;
  access: string;
  refresh: string;
  avatar_link: string;
}

export interface State {
  user: LoginUser;
}

export interface Token {
  access: string;
  refresh: string;
}

export interface Post {
  id: string;
  body: string;
  created_at: string;
  created_ago: string;
  created_by: User;
  likes_count: number;
  post_liked: boolean;
  comments_count: number;
  is_private?: boolean;
  post_attachments: PostAttachment[];
  comments?: Comment[];
}

export interface PostAttachment {
  id: string;
  image_link: string;
}

export interface Notification {
  id: string;
  body: string;
  post_id: string;
  type_of_notification: string;
  created_by: User;
  created_for_id: string;
}

export interface Trend {
  id: string;
  hashtag: string;
  occurences: number;
}

export interface Comment {
  id: string;
  comment: string;
  created_by: User;
  created_at: string;
  created_ago: string;
}

export interface FriendshipRequest {
  id: string;
  created_by: User;
  status: string;
}