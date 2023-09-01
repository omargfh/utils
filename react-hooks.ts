/* 
 * function: useReferenceBind
 * a hook to mutate object/map/tuple/set/array states in memory
 * 
 * Example usage: 
 * const [likes, refreshLikes] = useReferenceBind({ count: 0 })
 * function handleClick() {
 *    likes.count++
 *    refreshLikes()
 * }
 * 
 * */
function useReferenceBind(defaultValue: any) {
  const $ = useState<typeof defaultValue>(defaultValue);
  const _ = useState(0);
  const WRAP_AROUND_BOUND = 10_000;
  function refresh() {
    _[1]((render) => (render + 1) % WRAP_AROUND_BOUND);
  }
  return [$[0], refresh];
}

/* 
 * function: useInterface
 * a hook to wrap together the state as a property and setState as a method
 * this makes it easier to create two-way bindings
 * 
 * Example usage:
 * const count = useInterface<number>(0);
 * function handleClick() {
 *    count.assign(count => count + 5)
 * }
 * return <h3>Count: {count.value}</h3>
 * */
type Interface<T> = {
  value: T,
  assign: React.Dispatch<React.SetStateAction<T>>
}
function useInterface<T>(defaultValue: T): Interface<T> {
  const [state, setState] = useState<T>(defaultValue);
  return {
    value: state,
    assign: setState
  };
}
