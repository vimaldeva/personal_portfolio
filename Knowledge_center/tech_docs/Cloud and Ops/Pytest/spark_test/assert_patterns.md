```
# ─── EQUALITY ─────────────────────────────────────────────────────
assert result == 5                        # equal
assert result != 5                        # not equal
assert result is None                     # is None
assert result is not None                 # is not None
assert result is True                     # exactly True
assert result is False                    # exactly False

# ─── COMPARISON ───────────────────────────────────────────────────
assert result > 0                         # greater than
assert result >= 0                        # greater than or equal
assert result < 100                       # less than
assert result <= 100                      # less than or equal

# ─── MEMBERSHIP ───────────────────────────────────────────────────
assert "tier"   in result.columns         # item in collection
assert "tier"   not in result.columns     # item not in collection
assert "Alice"  in names_list             # string in list
assert "Gold"   in ["Gold","Silver"]      # value in list

# ─── TYPE CHECKING ────────────────────────────────────────────────
assert isinstance(result, int)            # type check
assert isinstance(result, (int, float))   # multiple types
assert type(result) == str                # exact type

# ─── STRING CHECKS ────────────────────────────────────────────────
assert result.startswith("test_")         # starts with
assert result.endswith(".csv")            # ends with
assert "error" in result.lower()          # contains substring
assert len(result) > 0                    # non-empty string

# ─── COLLECTION CHECKS ────────────────────────────────────────────
assert len(my_list) == 3                  # length check
assert len(result.columns) == 5          # column count
assert my_list == [1, 2, 3]              # list equality
assert set(result) == {"a", "b", "c"}    # set equality (order ignored)
assert my_dict == {"key": "value"}        # dict equality
assert my_dict.get("key") == "value"      # dict key access

# ─── BOOLEAN ──────────────────────────────────────────────────────
assert condition                          # truthy
assert not condition                      # falsy
assert bool(result) is True              # explicit bool
```