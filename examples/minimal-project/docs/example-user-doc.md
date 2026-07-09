# Configuring the widget cache

Example Project can cache widgets to speed up repeated lookups. This page
explains how to turn caching on and choose a cache size.

## Enable caching

Set `cache.enabled` to `true` in your configuration file:

```yaml
cache:
  enabled: true
  max_items: 500
```

When caching is enabled, Example Project keeps recently used widgets in memory.
Subsequent lookups for the same widget return faster.

## Choose a cache size

The `max_items` option controls how many widgets are kept in the cache. When the
cache is full, the least recently used widget is removed to make room.

A larger cache uses more memory but improves hit rates for workloads that reuse
many widgets. Start with the default and adjust based on your workload.

## When caching does not help

Caching provides little benefit when each lookup is for a different widget,
because entries are evicted before they are reused.
