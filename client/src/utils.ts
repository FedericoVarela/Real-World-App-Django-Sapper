import type { Result } from "./types"

export function match<T>(item: Result<T>, ok: Function, err: Function): any {
  if (item.result instanceof Error) {
    return err(item.result)
  } else {
    return ok(item.result)
  }
}

export function unwrap<T>(item: Result<T>): any {
  if (item instanceof Error) {
    throw item.result
  } else {
    return item.result
  }
}