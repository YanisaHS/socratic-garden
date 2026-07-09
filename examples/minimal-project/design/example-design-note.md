# Design note: widget cache

## Problem statement

Widget lookups repeat the same expensive computation for frequently used
widgets, adding latency to common workflows.

## Goals

- Reduce latency for repeated widget lookups.
- Keep memory use bounded and configurable.

## Non-goals

- Distributed or cross-process caching.
- Persisting the cache across restarts.

## Proposed solution

Add an in-memory least-recently-used (LRU) cache in front of the widget lookup
path. The cache is opt-in via `cache.enabled` and bounded by `cache.max_items`.

## Alternatives considered

- **No cache:** simplest, but does not address the latency problem.
- **Unbounded cache:** better hit rates, but unbounded memory growth is a risk.

## Trade-offs

An LRU cache adds a small amount of bookkeeping and memory overhead in exchange
for lower latency on repeated lookups. It does not help workloads with little
reuse.

## Open questions

- What default `max_items` value fits the most common workloads?
- Should cache statistics be exposed for operators?
