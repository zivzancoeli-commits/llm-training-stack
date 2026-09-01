---
id: code-005
category: code
subcategory: data-structures
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - debugging
title: Matching parentheses with a stack, and a case that fails
approx_words: 600
---

Checking whether brackets are balanced is the canonical stack problem, because the structure of the problem *is* a stack: the most recently opened bracket must be the first one closed. Last in, first out.

```python
PAIRS = {")": "(", "]": "[", "}": "{"}

def balanced(s):
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != PAIRS[ch]:
                return False
            stack.pop()
    return not stack
```

Three ways to fail, and the code checks all three: a closer arrives with nothing open (`not stack`), a closer arrives that doesn't match the most recent opener (`stack[-1] != PAIRS[ch]`), or the string ends with openers still waiting (`return not stack`).

## Trace on a passing case: "{[]()}"

| step | char | action              | stack after |
|------|------|---------------------|-------------|
| 1    | `{`  | push                | `{`         |
| 2    | `[`  | push                | `{ [`       |
| 3    | `]`  | top is `[`, pop     | `{`         |
| 4    | `(`  | push                | `{ (`       |
| 5    | `)`  | top is `(`, pop     | `{`         |
| 6    | `}`  | top is `{`, pop     | (empty)     |

End of string, empty stack: balanced. Notice how the stack height at any moment equals the current nesting depth — after step 2 we are two levels deep, and the stack has two entries.

## Trace on a failing case: "([)]"

This is the instructive one, because every bracket individually has a partner — there is one `(` for the `)` and one `[` for the `]` — yet the string is invalid because the partners *interleave* instead of nesting.

| step | char | action                                  | stack after |
|------|------|-----------------------------------------|-------------|
| 1    | `(`  | push                                    | `(`         |
| 2    | `[`  | push                                    | `( [`       |
| 3    | `)`  | top is `[`, but `)` needs `(` — **fail** | —           |

The stack rejects it at step 3: the most recent unclosed bracket is `[`, and a `)` cannot close it. A naive counter-based checker — increment on open, decrement on close, per bracket type — would happily accept `"([)]"` because all three counters end at zero. That is precisely the bug the stack prevents: counters track *quantity*, the stack tracks *order*.

## Bug note: the empty-stack check must come first

A tempting compression is:

```python
elif ch in ")]}":
    if stack.pop() != PAIRS[ch]:   # BUG on input ")"
        return False
```

On input `")"`, `stack` is empty and `pop()` raises `IndexError` instead of returning `False`. The original code's `if not stack or ...` short-circuits before touching the top. Crashing on malformed input is a worse behavior than reporting it, and closers-before-openers is exactly the kind of malformed input a validator exists to handle.

## Complexity

One pass over the string with \(O(1)\) work per character gives \(O(n)\) time. Space is \(O(n)\) in the worst case — the input `"((((("` pushes every character — but it is proportional to maximum nesting depth, not string length, so realistic inputs (source code, JSON) stay shallow.

## Why this pattern generalizes

The same skeleton — push on open, check-and-pop on close, demand emptiness at the end — validates HTML tag nesting, checks indentation blocks, and underlies how parsers handle nested expressions. Whenever a problem says "the most recent unfinished thing must finish first," reach for a stack; whenever a proposed solution only counts things, test it against an interleaved case like `"([)]"` before trusting it.
