declare module 'zustand' {
  type StoreCreator<T> = (set: (partial: Partial<T> | ((state: T) => Partial<T>)) => void, get?: () => T) => T;
  export function create<T>(creator: StoreCreator<T>): () => T;
  export function create<T>(): (creator: StoreCreator<T>) => () => T;
}
