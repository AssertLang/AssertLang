export function find_first_even(numbers: Array<number>): number {
  for (const num of numbers) {
    if (((num % 2) === 0)) {
      return num;
    }
  }
  return -1;
}
