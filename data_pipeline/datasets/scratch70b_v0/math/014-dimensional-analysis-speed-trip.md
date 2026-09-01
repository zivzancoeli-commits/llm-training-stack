---
id: math-014
category: math
subcategory: applied-math
difficulty: easy
source_model: fable-5
skills:
  - worked-solution
  - unit-tracking
  - check-your-work
title: Dimensional analysis converting a speed into a time for a trip
approx_words: 620
---

Dimensional analysis is the practice of treating units as algebraic objects that multiply and cancel like numbers. It turns unit conversion from a memorized ritual ("do I multiply or divide by 1.6?") into a mechanical procedure that announces its own errors.

Problem: you're driving 380 kilometers. Your average speed will be 65 miles per hour. How long will the trip take, in hours and minutes? Use 1 mile = 1.609 km.

The core relation is time = distance / speed. But the distance is in kilometers and the speed is in miles per hour, and dividing them raw gives 380/65 = 5.85 of... nothing meaningful. The units don't cancel: km divided by (miles/hour) is km-hours per mile, which is not a time. Dimensional analysis makes this mismatch impossible to miss, because you carry the units through every step.

Convert the speed to km/h first. The conversion factor 1.609 km per mile is a fraction equal to 1 (since 1.609 km and 1 mile are the same length), and multiplying by 1 is always legal:

65 miles/hour * 1.609 km/mile = 104.6 km/hour

Watch the units do the work: "miles" in the numerator cancels "mile" in the denominator, leaving km/hour. If you had guessed the factor upside down — 65 * (1 mile / 1.609 km) — the units would read miles^2 per (hour*km), an obvious absurdity. That's the whole trick: write the factor in whichever orientation cancels the unit you want to kill. You never have to remember whether to multiply or divide; the cancellation decides.

Now the division has consistent units:

time = 380 km / 104.6 km/hour = 3.63 hours

Kilometers cancel, leaving hours, which is a time. Convert the fractional hour to minutes: 0.63 hours * 60 minutes/hour = 38 minutes (again, "hours" cancels). Total: about 3 hours 38 minutes.

Check the answer two independent ways. Sanity bound: at a clean 100 km/h, 380 km takes 3.8 hours; we're going slightly faster than 100, so slightly under 3.8 hours — 3.63 fits. Reverse computation: 3.63 hours * 104.6 km/hour = 379.7 km ≈ 380 km, recovering the original distance. When a chain of conversions inverts cleanly back to the input, the arithmetic and the unit logic are both confirmed.

Alternatively, convert the distance instead: 380 km * (1 mile / 1.609 km) = 236.2 miles, then 236.2 miles / (65 miles/hour) = 3.63 hours. Same answer by the other route — you may standardize either quantity, so pick whichever needs fewer steps.

The common mistake is inverting a conversion factor, and it's insidious because the wrong answer often looks plausible. Divide 65 by 1.609 instead of multiplying and you get 40.4, and "40.4 km/h" doesn't scream error the way negative time would; the trip comes out at 9.4 hours, wrong by a factor of 2.6. The unit-cancellation habit is the defense: if you write units on every quantity, the upside-down factor produces visible garbage (miles squared per hour-kilometer) instead of a silent bad number. People who skip writing units aren't saving time; they're deleting their error detector.

The reason this technique generalizes: every physical formula must be dimensionally consistent, so units are a free proofreading pass on any calculation. If you compute an energy and the units come out as kg*m/s, you've made an algebra mistake somewhere, guaranteed, before you check a single digit. Professionals in physics and engineering run this check reflexively on formulas they've just derived. For a trip-time problem the stakes are a missed dinner; the habit, though, is the same one that catches million-dollar errors, famously including a Mars probe lost to an unconverted pound-force. Write the units. Cancel them on paper. Believe them when they complain.
