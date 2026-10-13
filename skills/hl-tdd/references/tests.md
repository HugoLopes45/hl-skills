# Good and bad tests

A good test calls the public interface, asserts what a caller can observe, and survives a rewrite of the internals.

## Implementation-coupled

Breaks on a refactor that keeps behavior.

```python
# Bad: asserts which collaborator was called
def test_invoice_uses_tax_service(mocker):
    tax = mocker.patch("billing.tax_service.rate", return_value=0.2)
    make_invoice(order)
    tax.assert_called_once()

# Good: asserts the result a caller sees
def test_invoice_total_includes_tax():
    assert make_invoice(order_of(100)).total == 120
```

Other tells: testing private functions, asserting call order or counts, checking state through a side channel (querying the table instead of reading through the interface).

```python
# Bad: verifies through the database
def test_register_saves_user(db):
    register("ada@example.com")
    assert db.execute("select 1 from users where email = ?", ["ada@example.com"]).fetchone()

# Good: verifies through the interface
def test_registered_user_can_log_in():
    register("ada@example.com", password="pw")
    assert log_in("ada@example.com", "pw").ok
```

## Tautological

The expected value is computed the way the code computes it, so the test cannot disagree with the code.

```python
# Bad
def test_total():
    items = [10, 5]
    assert total(items) == sum(items)

# Good: an independent literal
def test_total():
    assert total([10, 5]) == 15
```

Expected values come from a known-good literal, a worked example, or the spec.

## Horizontal

All tests first, then all code. The tests describe imagined behavior and lock in a structure before the code teaches anything. Write one test, make it pass, then write the next.

## Mocks

Mock only what the project does not control: external APIs, clocks, randomness, sometimes the filesystem or database. Never mock the module under test or its internal collaborators. Code that is hard to test without mocking internals usually needs its dependency passed in.
