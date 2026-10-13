# Plan: faster product pages

Goal: product pages render in under 100 ms. Today they take 350 ms, and `get_price` is 250 ms of it.

1. Wrap `prices.get_price(sku)` in `functools.lru_cache(maxsize=10_000)`.
2. Prices never change after a product is created, so the cache needs no invalidation.
3. Add a test that a second call for the same SKU does not query the database.
