# benchmark-spring-ai

Public Spring AI Maven benchmark runner for BoringCache vs GitHub Actions cache.

This repo exists separately from [`boringcache/benchmarks`](https://github.com/boringcache/benchmarks) so the benchmark keeps:

- one pinned upstream source commit
- isolated GitHub Actions cache usage
- one shared BoringCache workspace name: `boringcache/benchmarks`
- independent workflow history and nightly runs

## Source Model

- Upstream source lives in the pinned `upstream/` submodule.
- `scenarios/stale-low.patch`, `scenarios/stale-mid.patch`, and `scenarios/stale-high.patch` are the only source mutations applied during scenario runs.

The current pinned upstream source is:

- `spring-projects/spring-ai@e6ec123574c263094dd3bc866d67c1390f190f82`

## What It Measures

Each backend runs the same scenario set:

- `cold`
- `warm1`
- `warm2`
- `stale-low`: one leaf/advisor Java source change
- `stale-mid`: one model or starter Java source change
- `stale-high`: one shared core Java source change

The story this benchmark is meant to show is:

- speed on cold, warm, and stale paths
- storage footprint in each backend
- cache reuse through native Maven remote-cache behavior

## Token Model

This repo uses split BoringCache tokens as the standard CI shape:

- `BORINGCACHE_RESTORE_TOKEN` for read-only restore and proxy access
- `BORINGCACHE_SAVE_TOKEN` for trusted write paths
- `BORINGCACHE_API_TOKEN` only where a single bearer variable is still required for compatibility
