---
id: logic-006
category: logic
subcategory: statistical-reasoning
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - counterexample
title: Survivorship bias and the airplane armor story
approx_words: 600
---

# Survivorship bias and the airplane armor story

A simplified story, worn smooth by retelling but still the cleanest teacher of its lesson. During a long air war, engineers examined bombers returning from missions and mapped every bullet hole. The holes clustered on the wings, the tail, and the middle of the fuselage. The engine housings and cockpit area came back almost clean. Armor is heavy, so it must be rationed. Where should it go?

## The tempting argument

1. Returning planes show dense damage on wings, tail, and fuselage.
2. Those are evidently the areas that get shot the most.
3. Therefore, armor the wings, tail, and fuselage.

This feels like textbook empiricism — go where the data are. And the data are real: those holes exist, honestly counted. Yet the recommendation is close to exactly backwards.

## The flaw, made explicit

The planes examined were not a sample of *planes that got shot*. They were a sample of *planes that got shot and made it home*. Every aircraft that took hits to the engine or cockpit is missing from the dataset — it is at the bottom of the sea. The bullet-hole map is not a map of where planes get hit; enemy fire sprays roughly evenly. It is a map of where a plane can *absorb* a hit and keep flying.

Read correctly, the clean patches are the scream in the data. Engines and cockpits look untouched among survivors precisely because hits there are fatal. The armor belongs on the places with the *fewest* holes.

**Counterexample to the tempting argument.** Imagine 100 bombers fly out and enemy fire distributes hits evenly: 50 planes take wing hits, 50 take engine hits. Wing hits are survivable, so all 50 wing-hit planes return, holes on display. Engine hits are fatal, so all 50 engine-hit planes crash. The engineers inspect 50 returned planes and find 100% wing damage, 0% engine damage. Premises 1 and 2's evidence looks overwhelming, yet armoring wings saves nobody, while armoring engines would have saved 50 crews. The premises are fully consistent with a world where the conclusion is maximally wrong.

## The valid form of the inference

The repaired reasoning runs:

1. Our sample contains only survivors; the selection filter was "made it home."
2. Any damage pattern common among survivors marks damage that is *compatible with surviving*.
3. Damage absent among survivors, on parts that enemy fire should hit as often as any other, marks damage that *prevents* survival.
4. Therefore, reinforce the areas where survivors show no damage.

Step 3 carries an assumption worth stating aloud — that fire lands roughly uniformly — and the argument is honest about needing it. Good statistical reasoning is often exactly this: asking *what process decided which cases I get to see?* before asking what the visible cases show.

## The same ghost elsewhere

- **Business advice.** "Every great founder I studied dropped out and persisted through ridicule." The founders who did the same and failed wrote no memoirs. The shelf of success books is a formation of returned bombers.
- **Old buildings.** "They built things to last back then." The flimsy structures from that era were demolished long ago; only the sturdy remain to be admired.
- **Investment funds.** Fund families quietly close their losers, so the average performance of *currently listed* funds overstates what an investor in a random fund actually earned.

The transferable rule: before drawing conclusions from any dataset, name the filter that produced it. If the filter is correlated with the outcome you care about — surviving, succeeding, still standing — the silent, missing cases usually hold the real lesson.
