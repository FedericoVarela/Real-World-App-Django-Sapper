import type { Result, Session } from "./types"

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

export function matchSession(item: Session, some: Function, none: Function): any {
	if (item === undefined) {
		return none()
	} else {
		return some(item)
	}
}