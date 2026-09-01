---
id: how-015
category: how_things_work
subcategory: computing
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How a compiler differs from an interpreter, using a 5-line program story
approx_words: 800
---

# How a compiler differs from an interpreter, using a 5-line program story

Both a compiler and an interpreter make a machine do what the source
describes. The difference is *when* the translation happens and *what
survives afterwards*. Follow one tiny program through both paths:

```
x = 5
y = 0
while x > 0:
    y = y + x
    x = x - 1
```

It sums 5 + 4 + 3 + 2 + 1 and leaves 15 in y. One loop, and that loop is
where the whole argument lives.

## The interpreter's story

An interpreter reads the source, usually parses it once into a tree or
bytecode, then walks that structure executing as it goes. Nothing durable
is produced; when the process exits, the translation effort is gone.

Trace the loop body. On each iteration the interpreter must:

1. Fetch the instruction for `y = y + x`.
2. Decode it: an assignment whose right side is a binary addition.
3. Look up `y` in an environment, typically a hash table keyed by name.
4. Look up `x` the same way.
5. Check the runtime types of both values. Integers? Floats? Strings, in
   which case `+` means concatenation? Objects with custom addition?
6. Dispatch to the right addition routine.
7. Possibly allocate a new object to hold the result.
8. Store it back into the environment.

Then it repeats the same eight-step ceremony on the next iteration, and
again. The loop runs five times here, but if `x` started at five million,
the interpreter would redo that decoding and type-checking five million
times. That overhead — not the addition itself, which is one machine
instruction — is the dominant cost.

## The compiler's story

A compiler reads the whole program before running any of it and emits
machine code the CPU executes directly. Because it sees everything and is
allowed to spend time, it settles questions once, at compile time, that
the interpreter must re-settle on every pass.

For this program a compiler for a statically typed language would work
out that `x` and `y` are integers, keep both in CPU registers rather than
a hash table, and emit a loop roughly like:

```
    mov  eax, 5        ; x in a register
    xor  ebx, ebx      ; y = 0
loop:
    test eax, eax
    jle  done
    add  ebx, eax      ; y = y + x
    dec  eax           ; x = x - 1
    jmp  loop
done:
```

No name lookups, because names were resolved to registers at compile
time. No type checks, because types were proven at compile time. No
decoding, because these *are* the machine's instructions.

An optimising compiler may go further. Since `x` starts at a known
constant and nothing external can observe the loop, it can unroll or even
evaluate the whole thing at compile time and emit `mov ebx, 15`. Constant
folding like that is only available to something that examines the
program as a whole before executing any of it.

## What each side buys

The compiler's advantages: fast execution, errors caught before shipping,
and a distributable artifact that runs without the toolchain present.

The interpreter's advantages: no build step, so edit-run cycles are
instant; portability, since the same source runs anywhere the interpreter
exists; and genuine expressive power — `eval`, monkey-patching, runtime
type changes, and inspecting the program while it runs are easy for an
interpreter and awkward once code is frozen into machine instructions.

Real systems blur the line. Most "interpreted" languages compile to
bytecode for a virtual machine first, a compilation step even if the user
never sees it. A JIT compiler interprets at first, watches which loops
are hot, and compiles those at runtime using observed types as
assumptions — with a guard that falls back to the interpreter if an
assumption breaks. That is how modern JavaScript engines make a
dynamically typed language run within a small factor of C. The useful
mental model is a spectrum of *how much is decided before execution*, not
two boxes.

## Limiting case: what if line 5 has a typo?

Change the last line to `x = x - "1"`, subtracting a string.

The compiled path never runs. The compiler reaches that line during type
checking, sees an integer minus a string, and refuses to produce a
binary. You get an error with a line number, at build time, before anyone
else sees the program. Nothing executed, so nothing partial happened.

The interpreted path behaves completely differently. Lines 1 and 2 run
fine. The loop starts. `y = y + x` executes and y becomes 5. Then the
interpreter reaches the bad subtraction and raises a type error —
*during the first iteration*, after state has already changed. If those
first lines had written a file or sent a network request, that side
effect has already happened and will not be undone.

Worse, if the typo sat on a rarely taken branch instead of inside the
main loop, the interpreter would not notice until that branch ran,
possibly months later in production. The compiler would have caught it
the first time anyone built the project.

That is the trade in its sharpest form: the compiler makes you answer
questions up front and rewards you with speed and early errors; the
interpreter lets you start immediately and defers every question until
the moment it genuinely cannot be avoided.
