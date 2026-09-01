---
id: habits-014
category: reasoning_habits
subcategory: communication
difficulty: medium
source_model: fable-5
skills:
  - self-explanation
  - verification
title: Explaining a solution to a skeptical friend
approx_words: 620
---

# Explaining a Solution to a Skeptical Friend

Programmers keep a rubber duck on the desk for a reason: explaining a bug aloud to the duck, line by line, routinely reveals the bug before the sentence finishes. The mathematical version of this habit is stronger, because the duck gets upgraded. Don't merely explain your solution to an imaginary listener — explain it to an imaginary *skeptic*: a sharp friend who wants you to be right but refuses to nod at anything they don't actually follow.

The habit works because private reasoning and communicable reasoning are held to different standards, and the private standard is dangerously lax. Inside your own head, a step can be "obvious" because it's familiar, because it's what worked last time, or because you *want* the argument to go through. Ideas connect by vibes. The moment you must say the step aloud in full sentences, the vibes have to become logic. "And then clearly the maximum is at the endpoint—" *Why* clearly? The skeptical friend interrupts, and now you must either produce the reason or discover that you never had one. An enormous fraction of proof errors live exactly in the steps labeled *clearly*, *obviously*, and *it follows that*: these words are where authors put the steps they didn't check.

Run the explanation as an actual protocol, not a mood:

**Speak in full sentences, aloud or in writing.** Muttering symbol-strings doesn't trigger the effect. The friend doesn't read notation from your scratch work; every step must be *said*: "Since the function is continuous on a closed interval, it attains a maximum somewhere." Verbalizing forces serialization — one claim at a time, each supported by the previous ones — which is precisely the structure a proof must have and a hunch lacks.

**Give the friend three standing questions.** First: *"How do you know that?"* — deployed at every step, this flushes out unjustified leaps. Second: *"Where did you use the assumptions?"* — a proof of a theorem about odd integers that never uses oddness is almost surely proving something false or something weaker; unused hypotheses are a classic sign of a broken argument. Third: *"What if...?"* — the friend proposes edge cases: zero, negatives, the empty set, equality instead of strict inequality. Many "proofs" are true arguments about the typical case and false about the boundary.

**Let the friend be ignorant, not just skeptical.** They know the definitions but none of your context. This forces you to state what each symbol means and what the question was — and, as with restating any problem, the recap alone sometimes reveals that your solution answers a subtly different question.

The habit has a constructive mode too, not only a destructive one. Explanations that survive tend to *improve* the solution: to make a step sayable, you often find a cleaner reason than the one you used, and the friend's "wait, couldn't you just—" moments (which are your own, wearing a costume) shorten proofs. Teaching is famously the fastest way to learn a subject; self-explanation captures a real share of that effect without needing a student. The empirical literature on learning agrees: students prompted to explain worked examples to themselves outperform students who reread them, because explanation forces the gaps into view.

Two failure modes to avoid. Don't let the friend become a heckler who doubts everything equally — infinite skepticism is as useless as none; the friend accepts standard facts and honest arithmetic, and presses only where inference happens. And don't perform the explanation *after* you've decided you're right, as a victory lap. Its power comes from running while the verdict is genuinely open.

A solution you cannot explain to this friend is not yet a solution; it is a private feeling of correctness. The friend costs nothing, is available at 2 a.m., and holds you to the only standard that ultimately counts: an argument that convinces someone who won't pretend.
