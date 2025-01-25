export default function throttle(fn, delay) {
  let timer = null
  return function () {
    if (timer !== null) return
    fn.apply(this, arguments)
    timer = setTimeout(() => {
      timer = null
    }, delay)
  }
}
