---
id: habits-005
category: reasoning_habits
subcategory: checking
difficulty: medium
source_model: fable-5
skills:
  - verification
  - check-your-work
title: Working backwards from a candidate answer
approx_words: 600
---

# Working Backwards from a Candidate Answer

Solving and checking are not the same skill, and the second is usually easier. Finding x such that 7x + 13 = 104 requires algebraic maneuvering; checking whether x = 13 works requires only multiplication and addition: 7 × 13 + 13 = 91 + 13 = 104. Yes. The asymmetry — verification is cheaper than search — is one of the most exploitable facts in problem solving, and the habit that exploits it is simple: once you have a candidate answer, run it backwards through the original conditions.

The crucial phrase is *original conditions*. A common failure is to check the candidate against your own derived equation — the one you wrote three steps into the solution. If your error happened while setting up that equation, the check will pass and the answer will still be wrong. You'll have verified your mistake with great care. Always return to the problem statement itself, the words on the page, and ask: does this candidate make every sentence true?

Consider a word problem: "A mother is three times as old as her daughter. In 12 years, she will be twice as old. How old is each now?" Suppose your algebra produced daughter = 12, mother = 36. Now interrogate the candidate against the story, sentence by sentence. Three times as old now? 36 = 3 × 12. Yes. In twelve years: daughter 24, mother 48. Twice as old? 48 = 2 × 24. Yes. Both sentences hold, so the answer stands — and notice the check never touched your algebra. It is an independent path to confidence, which is exactly what makes it evidence rather than repetition.

Working backwards has a second life as a *solving* method, not just a checking one. When the answer is known to be one of a few possibilities — a multiple-choice question, a small integer, "one of these five suspects" — it can be faster to test candidates than to construct the answer. If a problem asks which whole number of hours makes two rental plans cost the same, and the structure suggests the answer is small, testing 3, 4, 5 directly may finish before the algebraic setup would. This is not cheating; it is choosing the cheaper direction through the same logical tunnel. The equation "solve for x" and the procedure "find the x that survives checking" define the same x.

Three refinements make the habit sharp:

**Check every condition, not just the memorable one.** Problems often carry two or three constraints, and a wrong candidate typically satisfies most of them — that's what made it seductive. The candidate that passes four checks and fails the fifth is wrong, period. Partial credit belongs to exams, not to answers.

**Prefer checks that use different operations than the solution did.** If you solved by dividing, check by multiplying. If you found a root by formula, substitute it into the polynomial by direct evaluation. Errors tend to be sticky within an operation — a person who mis-divides will often mis-divide the same way twice — so crossing to the inverse operation breaks the correlation.

**When the check fails, treat it as a gift.** A failed check localizes nothing by itself, but it converts "I think I'm done" into "there is a specific bug to find," which is a far better epistemic position than false confidence. Re-derive with the failed condition in view; it often points at the exact step where the story and the algebra parted ways.

The habit's deepest lesson is about the direction of trust. Your solution is a construction, and constructions inherit every weakness of their longest chain. The backward check is short, independent, and anchored to the problem's own words. When the two agree, you haven't just done the problem — you've caught it from both ends.
