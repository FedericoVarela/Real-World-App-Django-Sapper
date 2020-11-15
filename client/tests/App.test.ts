// import ErrorComponent from '../src/components/Error.svelte'
// import { render, fireEvent } from '@testing-library/svelte'
//TODO testing
import { it, expect } from "jest"

it('it works', async () => {
  // const { getByText, getByTestId } = render(ErrorComponent)
  expect(2+2).toBe(4)

  // const increment = getByText('increment')
  // const decrement = getByText('decrement')
  // const counter = getByTestId('counter-value')

  // await fireEvent.click(increment)
  // await fireEvent.click(increment)
  // await fireEvent.click(increment)
  // await fireEvent.click(decrement)

  // expect(counter.textContent).toBe('2')

  // // with jest-dom
  // expect(counter).toHaveTextContent('2')
})