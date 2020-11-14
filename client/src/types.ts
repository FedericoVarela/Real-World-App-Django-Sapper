
// Utilities
export type Result<T> = { result: T | Error }
export type Response<T> = Promise<Result<T>>

export interface Paginated<T> {
  count: number,
  next: URL | null,
  previous: URL | null,
  results: T[]
}

// Models
export interface Author {
  id: number
  username: string
}

export type Tag = {
  name: string
}

export interface Post {
  id: number,
  title: string,
  content: string,
  author: Author
  tags?: Tag[]
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
}

