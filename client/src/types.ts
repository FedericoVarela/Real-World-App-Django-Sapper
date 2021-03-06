import type { User } from "./api"

// Utilities
export type Result<T> = { result: T | Error }
export type Option<T> = T | null
export type Response<T> = Promise<Result<T>>
export type Session = User | undefined;

export interface Paginated<T> {
  count: number,
  next: Option<string>,
  previous: Option<string>,
  results: T[]
}

// Models
export interface Author {
  id: number
  username: string
  picture?: string
}

export type Tag = {
  name: string
}

export interface Post {
  id: number,
  title: string,
  content: string,
  author: Author
  tags?: Tag[],
  is_favorite?: boolean
  favorite_count: number
  created_at: Date
}

export interface Token {
  access: string,
  refresh: string
}

export interface Comment {
  id: number,
  parent_id?: number,
  post_id: number
  content: string,
  author: Author,
  created_at: Date
  reply_to: Option<number>
}

export interface Profile {
  username: string,
  created_at: Date,
  description: string,
  picture: string
  is_following?: boolean
}