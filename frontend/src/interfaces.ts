export interface User {
    id: string;
    email: string;
    name: string;
    friends_count: number;
    posts_count: number,
    avatar_link: string
}

export interface Conversation {
    id: string;
    modifed_ago: string;
    users: User[]
}

export interface LoginUser {
    isAuthenticated: Boolean,
    id: string,
    name: string,
    email: string,
    access: string,
    refresh: string,
    avatar_link: string
}

export interface State {
    user: LoginUser
}

export interface Token {
    access: string,
    refresh: string,
}

export interface Post {
    id: string,
    body: string,
    created_at: string,
    created_ago: string,
    created_by: User,
    likes_count: number,
    post_liked: Boolean

}
export interface Notification {
    id: string,
    body: string,
    post_id: string,
    type_of_notification: string,
    created_by: User,
    created_for_id: string
}