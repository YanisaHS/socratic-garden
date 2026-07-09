# Internal note: reproducing widget cache behavior

This note captures how to reproduce and inspect widget cache behavior during
development. It is internal and not intended for public users.

## Reproduce a cache hit

1. Start Example Project with caching enabled and `max_items: 2`.
2. Look up widget `A`. This is a cache miss and populates the cache.
3. Look up widget `A` again. This should be a cache hit.

## Reproduce an eviction

1. With `max_items: 2`, look up widgets `A`, then `B`.
2. Look up widget `C`. The least recently used entry (`A`) is evicted.
3. Look up widget `A` again. This is a miss, confirming eviction.

## Notes for maintainers

- The cache is in-memory only and is cleared on restart.
- There is currently no metric exposed for hit/miss ratio; this is tracked as an
  open question in the design note.
