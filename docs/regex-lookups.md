---
title: Regex lookups - AMSDAL Glue
description: How the regex and iregex lookups run on SQLite and PostgreSQL, and how to write a pattern that gives the same rows on both.
amsdal_docs:
  target: glue/regex-lookups.md
  nav_title: Regex lookups
  nav_section: Glue (ETL)
  nav_order: 5
---

# Regex lookups

`FieldLookup.REGEX` and `FieldLookup.IREGEX` (`regex` / `iregex` in the AMSDAL ORM) match a value against a
regular expression. The pattern is a string and reaches the database unchanged, as in Django:

```python
Entry.objects.filter(title__regex=r'^(An?|The) +')
Entry.objects.filter(title__iregex=r'^(an?|the) +')
Entry.objects.filter(title__regex=r'(?i)^(an?|the) +')  # the same as iregex
```

| Backend | `regex` | `iregex` | Engine |
| -- | -- | -- | -- |
| SQLite | `value REGEXP pattern` | `value REGEXP '(?i)' \|\| pattern` | Python `re`, through the `REGEXP` function every glue SQLite connection registers |
| PostgreSQL | `value ~ pattern` | `value ~* pattern` | PostgreSQL's own engine (ARE) |
| Cross-database (Polars) executor | not supported | not supported | raises `NotImplementedError` |

A NULL value or a NULL pattern matches nothing. A column that is not text is matched as text. An invalid pattern
fails the query: on SQLite with `ConnectionError` (`user-defined function raised exception`).

## Portable syntax

glue does not translate or validate patterns. The portable syntax is **Python `re`**, kept within the
differences below: written that way, a pattern gives the same rows on SQLite and PostgreSQL. `(?i)` is accepted at
the very start of a pattern only.

A project that runs only on PostgreSQL may also write PostgreSQL's native syntax (`\y`, `\m`, `\M`,
`[[:alpha:]]`, embedded options): it works there, but fails or gives other rows on SQLite, the default backend of
local development and of tests.

## Known differences

Checked on PostgreSQL 17 with a UTF-8 locale against Python 3.13 `re`. Every row is pinned by a test case in
`libs/connections/tests/sql/regex_cases.py`.

| Construct | Python `re` (SQLite) | PostgreSQL | Portable form |
| -- | -- | -- | -- |
| `\s` | includes non-breaking spaces (U+00A0, U+2007, U+202F), U+0085 and U+001C–U+001F | does not | `[\s\u00a0\u2007\u202f]` |
| `\d` | any Unicode decimal digit (`٣`, `３`) | `0-9` only | `[0-9]` |
| `.` | does not match a newline | matches a newline | `[^\n]`, or `[\s\S]` for any character |
| `$` | the end, or before a final newline | the end only | `\Z` (the very end on both) |
| `\b`, `\B` | word boundary | `\b` is a backspace character: no error, just no match | `(?<!\w)john(?!\w)` instead of `\bjohn\b` |
| `\w` | Unicode word characters | differs on rare characters (`²`, `½`, combining marks) | accepted difference |
| case-insensitive | Python's case mapping | differs on rare letters (Greek final sigma, `ß`, Turkish `İ`) | accepted difference |
| backreference to a group inside a repetition, e.g. `^(?:(a)\|b)*\1$` on `aba` | keeps the capture of an earlier iteration: match | resets it: no match | avoid |
| groups inside lookaround | capture | do not capture, later group numbers shift | avoid |
| `a{,3}` | 0 to 3 | the literal text `a{,3}` | `a{0,3}` |
| `\x41B` | `\x41` then `B` | `\x` takes every following hex digit | `\u0041B` |
| `{m,n}` above 255 | accepted | error | 255 or below |
| named groups `(?P<n>…)`, scoped flags `(?i:…)`, inline flags other than a leading `(?i)`, atomic groups, possessive quantifiers, `\N{…}` | accepted | error | plain groups, one leading `(?i)` |
| `[[:alpha:]]`, `\y`, `\m`, `\M` | not `re` syntax: `\y` is an error, `[[:alpha:]]` silently means another set | accepted | PostgreSQL only |

The locale is a deployment requirement: PostgreSQL must run with a UTF-8 locale and collation (not `C`).
Otherwise case-insensitive matching and `\w` outside ASCII do not work there.
