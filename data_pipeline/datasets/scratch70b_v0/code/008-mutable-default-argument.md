---
id: code-008
category: code
subcategory: python-pitfalls
difficulty: easy
source_model: fable-5
skills:
  - debugging
  - worked-solution
title: The mutable default argument bug in Python
approx_words: 580
---

This is probably Python's most famous foot-gun, and it looks completely innocent:

```python
def add_task(task, queue=[]):     # BUG lives here
    queue.append(task)
    return queue
```

The intent is obvious: "if the caller doesn't supply a queue, start a fresh empty one." That is not what Python does.

## Watching it go wrong

```python
>>> add_task("write tests")
['write tests']
>>> add_task("deploy")
['write tests', 'deploy']        # where did "write tests" come from?
>>> add_task("rollback")
['write tests', 'deploy', 'rollback']
```

Three independent calls, and the tasks are accumulating in one shared list. Meanwhile, callers who pass their own list are unaffected:

```python
>>> add_task("audit", [])
['audit']                        # fine, uses the caller's list
```

## Why: defaults are evaluated once, at def time

A `def` statement is executable code. When Python runs it, it evaluates each default expression *once* and stores the resulting object on the function itself. Every call that omits the argument receives that same stored object — not a fresh copy, the object.

You can literally inspect the shared list growing:

```python
>>> add_task.__defaults__
(['write tests', 'deploy', 'rollback'],)
```

The bug requires two ingredients: the default is evaluated once, **and** the object is mutable. `def f(x=0)` and `def f(s="")` are safe forever, because ints and strings can't be mutated — any "change" rebinds the local name and leaves the default untouched. `[]`, `{}`, `set()`, and mutable class instances are the dangerous defaults, and only if the function body mutates them in place.

## The fix: sentinel plus late construction

```python
def add_task(task, queue=None):
    if queue is None:
        queue = []               # fresh list on every defaulted call
    queue.append(task)
    return queue
```

Trace the fixed version through the same calls: first call sees `queue is None`, builds a new list, returns `['write tests']`. Second call builds *another* new list, returns `['deploy']`. The construction moved from def time into the call, so each defaulted call gets its own object.

If `None` is itself a meaningful value the caller might pass, use a private sentinel:

```python
_MISSING = object()

def add_task(task, queue=_MISSING):
    if queue is _MISSING:
        queue = []
    ...
```

## When the "bug" is a feature

The evaluate-once behavior is occasionally exploited deliberately as a cheap per-function cache:

```python
def expensive(x, _cache={}):
    if x not in _cache:
        _cache[x] = compute(x)
    return _cache[x]
```

This works, and you will meet it in real codebases, but `functools.lru_cache` says the same thing without relying on a pitfall your reviewer has to recognize as intentional.

## How to spot it in review

The pattern to flag is mechanical: a mutable literal (`[]`, `{}`, `set()`) or constructor call in a default, combined with any in-place mutation of that parameter in the body (`append`, `update`, `add`, item assignment). Linters catch it — flake8-bugbear's B006 and pylint's `dangerous-default-value` both fire on the buggy version above — so this bug should never survive CI in a configured project.

One last subtlety worth internalizing: the same evaluate-once rule explains why `def f(when=datetime.now())` freezes the timestamp at import time. Nothing is mutated there, yet every call sees the same stale time — the default was computed once and stored. Same mechanism, different symptom. The umbrella rule: *default expressions run at def time; if you need per-call behavior, put the construction inside the function.*
