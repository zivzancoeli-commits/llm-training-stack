---
id: logic-009
category: logic
subcategory: deduction
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - counterexample
title: Scope of quantifiers, two readings of one sentence
approx_words: 600
---

# Scope of quantifiers: "every student read a book"

The sentence "every student read a book" is two claims wearing one coat. Which claim you heard determines what follows from it — and arguments that slide between the readings can smuggle in conclusions nobody agreed to.

## The two readings

**Reading 1 (every…some):** For every student, there is some book — possibly a different one per student — that the student read.

> For all students s, there exists a book b such that s read b.

**Reading 2 (some…every):** There is one particular book that every student read.

> There exists a book b such that for all students s, s read b.

The difference is which quantifier sits inside the other's scope. In Reading 1, the choice of book is allowed to *depend on* the student; in Reading 2, one book must be chosen first and then work for everyone.

Concretely: a class of three where Ana read *Dune*, Ben read *Beloved*, and Cy read *Dracula* makes Reading 1 true and Reading 2 false. A class where all three read *Frankenstein* makes both true.

## The valid direction

1. There is one book that every student read. (Reading 2)
2. Therefore, every student read at least one book. (Reading 1)

This inference is airtight. If a single book b serves all students, then each student, asked to name a book they read, can name b. The shared witness works as everyone's personal witness. In general, "some-for-all" always entails "for-all-some."

From Reading 2 you may validly conclude more: a book club discussion is possible, the teacher can quiz the whole class on one plot, two students can be assumed to share reading material.

## The tempting invalid cousin

1. Every student read a book. (asserted, and true on Reading 1)
2. Therefore, there is a book that the class shares — let's discuss *it* on Friday.

The argument runs the entailment backwards, upgrading "for-all-some" to "some-for-all."

**Counterexample.** The Dune/Beloved/Dracula class above. Premise 1 is true — each student genuinely read a book. The conclusion is false — no title is common to all three. Friday's discussion collapses. The premises permit the witnesses to vary; the conclusion demands a uniform one, and nothing paid for that upgrade.

This backwards slide has serious real-world costumes:

- "Everyone in this country is represented by a senator" (each person, some senator) does not yield "some senator represents everyone."
- "Every event has a cause" (each event, some cause) does not yield "there is one cause behind every event" — a scope slide that has propped up more than one grand metaphysical argument.
- "Each patient responds to some treatment" does not yield "some treatment works for all patients." Pharmaceutical marketing lives in this gap.
- "Every process ends eventually" does not yield "eventually, every process has ended" — there may be no single moment by which all are done, if ever-longer processes keep starting.

## How to hear the difference

When a sentence mixes "every/all/each" with "a/some/there is," force yourself to ask: **can the witness vary, or must it be fixed first?** Try to build the spread-out scenario — different book per student, different senator per citizen. If that scenario satisfies the speaker's sentence, they have only claimed the weak reading, and any conclusion requiring a shared witness is unearned.

The one-way street is the whole lesson: a fixed witness gives you varying witnesses for free; varying witnesses never assemble themselves into a fixed one without a further argument.
