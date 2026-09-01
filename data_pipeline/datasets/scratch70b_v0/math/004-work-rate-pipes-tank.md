---
id: math-004
category: math
subcategory: word-problems
difficulty: medium
source_model: fable-5
skills:
  - worked-solution
  - check-your-work
title: "Work-rate problem: two pipes filling a tank, one leaking"
approx_words: 590
---

Work-rate problems look like they're about pipes and tanks, but they are really about one idea: rates add, times don't. Once you convert every actor in the story into "fraction of the job per hour," the problem becomes bookkeeping.

Problem: Pipe A can fill a tank in 4 hours. Pipe B can fill the same tank in 6 hours. A drain at the bottom, left open, can empty a full tank in 12 hours. If both pipes are opened while the drain is accidentally left open, how long does it take to fill the tank from empty?

The wrong instinct is to average or add the times: "4 hours and 6 hours, so together maybe 5 hours, minus something for the leak." Times don't combine that way. A pipe that fills the tank in 4 hours is doing 1/4 of a tank per hour; that per-hour rate is the thing you're allowed to add.

Set up the rates, taking "one full tank" as the unit of work:

- Pipe A: +1/4 tank per hour
- Pipe B: +1/6 tank per hour
- Drain: -1/12 tank per hour (negative, because it undoes work)

Combined rate = 1/4 + 1/6 - 1/12. Put everything over 12: 3/12 + 2/12 - 1/12 = 4/12 = 1/3 tank per hour.

If the tank fills at 1/3 per hour, filling one whole tank takes 1 / (1/3) = 3 hours.

Verify by simulating hour by hour, which is the tree-check of work problems. In one hour: A adds 1/4, B adds 1/6, drain removes 1/12. After hour one the tank holds 1/3. After hour two, 2/3. After hour three, 3/3 = full. The simulation agrees with the algebra, and it also confirms nothing weird happens along the way (the level never exceeds 1 or goes negative, which would signal a modeling error).

Also sanity-check the direction of the answer. With no leak, A and B together run at 1/4 + 1/6 = 5/12 per hour, filling the tank in 12/5 = 2.4 hours. The leak should make things slower than 2.4 hours but should not stop the job, since the leak's rate (1/12) is smaller than the pipes' combined rate (5/12). Three hours sits exactly where it should: slower than 2.4, but finite. If your computed answer had come out faster than the no-leak time, or negative, the sign on the drain's rate is the first place to look.

The common mistake is adding times instead of rates, and it has a subtle cousin: subtracting the drain's time instead of its rate, e.g., computing "4 + 6 - 12" somewhere. Any arithmetic performed directly on 4, 6, and 12 as raw numbers is suspect. The safe habit is mechanical: the moment you read "X does the job in T hours," write down "X's rate = 1/T job per hour" before doing anything else, with a minus sign if X works against the job.

One extension worth thinking through, because it tests real understanding: what if the drain could empty the tank in 2 hours instead of 12? Then the combined rate is 1/4 + 1/6 - 1/2 = 3/12 + 2/12 - 6/12 = -1/12 per hour. The rate is negative: the tank never fills, and if it started with water it would slowly empty. A time of "negative 12 hours" from the formula is the algebra telling you the story has no ending, not an answer to report. Reading the sign of a rate is part of solving the problem.
