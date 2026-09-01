---
id: math-018
category: math
subcategory: estimation
difficulty: hard
source_model: fable-5
skills:
  - worked-solution
  - estimation
  - check-your-work
title: "A Fermi estimate: how many piano tuners, with bounds not a fake precise number"
approx_words: 720
---

How many piano tuners work in Chicago? The point of this classic question is not pianos. It's a method: break an unknowable-sounding quantity into factors you can bound, estimate each factor honestly, multiply, and report a range instead of a fraudulent single number.

Structure first. The number of tuners is set by supply meeting demand: total tunings needed per year, divided by tunings one tuner can perform per year.

tuners = (pianos * tunings per piano per year) / (tunings per tuner per year)

Now estimate each factor, carrying a low and a high value rather than one number, because the honesty lives in the ranges.

Pianos in Chicago. Chicago has roughly 2.7 million people; call it about 1 million households (2-3 people per household). What fraction of households have a piano? Not 1 in 2, not 1 in 500. Somewhere around 1 in 20 to 1 in 50 feels defensible: pianos are common but far from universal. That gives 20,000 to 50,000 household pianos. Add institutions — schools, churches, venues, studios — which push the total up somewhat; say 25,000 to 60,000 pianos overall.

Tunings per piano per year. Serious players tune once or twice a year; most household pianos sit untouched for years. A blended rate of one tuning every 1 to 2 years, i.e., 0.5 to 1 tunings per piano per year, brackets it. Demand: 25,000 * 0.5 = 12,500 tunings/year on the low end, and 60,000 * 1 = 60,000 on the high end.

Tunings per tuner per year. A tuning takes about 2 hours, plus travel; call it 2 to 4 jobs per working day. At roughly 250 working days a year, that's 500 to 1,000 tunings per year for a full-time tuner.

Divide, pairing extremes carefully. Lowest tuner count: low demand / high productivity = 12,500 / 1,000 ≈ 13. Highest: high demand / low productivity = 60,000 / 500 = 120. So the estimate is roughly 15 to 120 piano tuners, centered somewhere near 40 to 60.

Notice what we did not do: report "there are 47 piano tuners in Chicago." Every input was uncertain by a factor of 2 or so, and those uncertainties compound. A single precise-sounding number would be a costume, dressing up a rough calculation as knowledge it doesn't contain. The interval is the honest product. The right way to state the conclusion: almost certainly more than 10, almost certainly fewer than 200, best guess a few dozen. That's genuinely useful — it tells you piano tuning is a niche trade of dozens, not a corner store on every block and not one lonely specialist.

Check the estimate against independent angles, because a Fermi answer you can't cross-check is a guess with extra steps. Angle one, employment share: a few dozen tuners among roughly 1.4 million Chicago workers means about 1 worker in 30,000 tunes pianos. Rare-but-real specialist trades (organ repair, watchmaking) live at about that frequency; plumbing, by contrast, is hundreds of times more common. Plausible. Angle two, market size: 40 tuners * 750 tunings * maybe $150 each is about $4.5 million a year of piano tuning in a metro of millions — a viable micro-industry, not an absurd one. Angle three, historical folklore: phone directories of large cities in the late 20th century listed piano tuners in the dozens, consistent with our band. Three independent angles, no contradictions; the estimate stands.

The common mistake, beyond fake precision, is letting one factor silently carry all the risk. Our answer is most sensitive to the piano-ownership fraction — the 1-in-20 versus 1-in-50 choice alone moves the result by 2.5x, more than any other input. Good practice is to identify that dominant uncertainty explicitly, because it tells you what to look up first if the estimate ever needs tightening. One real datum (say, actual piano sales figures) collapses more uncertainty than polishing all the other factors combined. A related trap: multiplying five estimates that each lean optimistic. Biases multiply too; five factors each inflated by 50% compound to a 7.6x overshoot. The discipline is to let your ranges straddle — make each interval one you'd bet either side of — so errors have a chance to cancel instead of stack.

The transferable lesson: decompose, bound each piece, multiply the extremes, sanity-check from an independent direction, and name your dominant uncertainty. The final number matters less than knowing how wrong it could be, and why.
