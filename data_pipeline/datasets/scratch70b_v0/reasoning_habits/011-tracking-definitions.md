---
id: habits-011
category: reasoning_habits
subcategory: precision
difficulty: medium
source_model: fable-5
skills:
  - definitions
  - precision
title: "Tracking definitions: don't swap meanings mid-problem"
approx_words: 610
---

# Tracking Definitions: Don't Swap "Average" Meanings Mid-Problem

Some of the most stubborn errors in reasoning involve no bad arithmetic at all. Every calculation is correct; the problem is that a word quietly changed meaning between step two and step five. "Average" is the classic offender, and it deserves a close look, because the cure — pinning definitions at the start and refusing to let them drift — is a habit that transfers everywhere.

Here is the trap in its purest form. A cyclist rides 60 km to a town at 30 km/h and returns at 20 km/h. What is her average speed? The reflex answer is (30 + 20)/2 = 25 km/h — the *mean of the two speeds*. But "average speed" has a fixed definition: total distance over total time. The trip out takes 2 hours; the return takes 3. Total: 120 km in 5 hours, which is 24 km/h. The reflex answer wasn't a computational slip; it was a definition swap. The solver was asked for one kind of average and silently computed another. And note the swap is seductive precisely because in the special case of equal *times* the two definitions agree — so the habit learned on easy problems betrays you on this one.

The word "average" alone shelters at least four distinct concepts: the arithmetic mean, the median, the mode, and various weighted or rate-based averages like the one above. A news claim that "the average family" has some income means wildly different things under mean versus median, since high incomes drag the mean upward while leaving the median put. None of these definitions is *the* right one. The error is never in the choice; it is in the *unmarked switch* — computing with one meaning, interpreting with another, or letting a problem's two "averages" (average speed, average of speeds) collapse into one word.

The habit that prevents this has three parts:

**Pin the definition at first use, in writing.** The moment a shifty word appears — average, growth, error, or, most, likely — write a one-line contract: "here, 'average speed' = total distance / total time." Ten seconds. The act of writing forces the choice to happen consciously, which is exactly where an unconscious swap gets intercepted.

**Give different concepts different names.** If a problem involves both the mean of the speeds and the average speed of the trip, the word "average" is no longer safe to use at all. Rename: call one m and the other v̄, or "leg-mean" and "trip-rate." Notation is anti-drift technology — a symbol defined once cannot quietly become its cousin, whereas a natural-language word does so without leaving marks.

**At the final answer, re-check the contract.** Before boxing the result, ask: the thing I computed — does it match the definition I pinned at the start, and does *that* match what the question meant? This closes the loop where many otherwise-careful solutions fail: correct machinery, applied to the wrong sense of the word, reported as if it answered the question.

The discipline extends far beyond "average." A "50% chance of rain Saturday and 50% Sunday" does not make rain certain on the weekend — the swap there is between per-day and per-weekend probabilities. "Interest rate" may be monthly or annual, nominal or effective. In a debate, "freedom" or "efficiency" can shift meaning between premise and conclusion, making an invalid argument feel airtight; logicians call this *equivocation*, and it is the same bug in prose clothing.

A useful self-test: if you cannot state, in one sentence and without the contested word, what your symbol or term means *in this specific problem*, you do not yet control it — the word controls you. Definitions are the load-bearing joints of an argument. Most people inspect their calculations. The stronger habit is inspecting the joints.
