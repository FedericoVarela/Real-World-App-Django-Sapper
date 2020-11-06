import type { Result } from "./types"

export function match<T>(item: Result<T>, ok: Function, err: Function): any {
  if (item.result instanceof Error) {
    return err(item.result)
  } else {
    return ok(item.result)
  }
}