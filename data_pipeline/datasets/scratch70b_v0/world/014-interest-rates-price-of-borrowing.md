---
id: world-014
category: world
subcategory: economics
difficulty: medium
source_model: opus-5
skills:
  - general-knowledge
  - worked-example
title: Interest rates as the price of borrowing, with a small loan example
approx_words: 735
---

An interest rate is a **rent on money over time**. You hand someone
purchasing power now; they hand back more later. The rate is the price
of that service, quoted as a percentage per period.

## Why the price is positive

Four separate components, which are worth being able to name apart:

1. **Time preference.** People prefer things sooner. To postpone
   consumption they want compensation.
2. **Opportunity cost.** Money lent to you cannot be lent to someone
   else or invested in a productive project.
3. **Expected inflation.** If prices rise 3% over the year, money repaid
   next year buys less, and lenders will ask for that back.
4. **Risk.** Some borrowers do not repay. A lender who loses 2% of loans
   must charge roughly 2% more, on top of everything else, just to break
   even.

Component 3 gives the most useful distinction in the topic. The
**nominal** rate is the number on the contract; the **real** rate is
what you actually gain in purchasing power. Approximately:

```
real rate = nominal rate - inflation rate
```

At 5% nominal with 5% inflation, the lender earns nothing in real terms.
Real rates can be negative, and often have been — a fact that makes no
sense until you separate the two ideas.

## Worked example: a small loan

Borrow **$1,200** for one year at **1% per month**.

**Case A: repay everything at the end.** With monthly compounding, the
balance grows by a factor of 1.01 each month:

```
1.01^12 = 1.12683 (approximately)
1200 * 1.12683 = $1,352.19
interest = $152.19
```

Note that the quoted 12% per year (12 × 1%) produced 12.68% of actual
growth. That gap is compounding — interest earning interest. The 12%
figure is an APR; the 12.68% figure is the effective annual rate. When
comparing offers, compare effective rates, or you are comparing
different things.

**Case B: repay in twelve equal monthly instalments.** This is how most
real consumer loans work, and the answer surprises people. The standard
amortising payment formula is:

```
payment = P * i / (1 - (1 + i)^-n)
```

with P = 1200, i = 0.01, n = 12.

```
(1.01)^-12 = 1 / 1.12683 = 0.88745
1 - 0.88745 = 0.11255
1200 * 0.01 = 12
payment = 12 / 0.11255 = $106.62 per month
```

Total paid: 12 × 106.62 = **$1,279.44**, so interest is about **$79.44**
— roughly half of Case A's $152.19.

Why? Because interest accrues on the *outstanding balance*, and in Case
B you are paying the balance down all year. You start owing $1,200 and
end owing nothing, so your average balance is around $600, and $600 at
about 12.7% for a year is close to $76. The rough estimate lands very
near the exact answer, which is a good sanity check to keep in your
head.

Inside a single payment, the split shifts. Month 1: interest is
1% × 1,200 = $12.00, so $94.62 reduces principal. Month 12: the balance
is about $105.56, interest is about $1.06, and nearly all of the payment
is principal. Early payments are mostly interest; late payments are
mostly principal. This is why paying extra early on a long loan saves
disproportionately, and why refinancing late in a mortgage saves less
than people expect.

## Scaling up: what rates do to the economy

The same price shows up everywhere. Central banks set a very short-term
policy rate, which propagates — imperfectly — into mortgage rates,
business loans, and bond yields. Raising it makes borrowing dearer,
which cools investment, housing, and spending; lowering it does the
opposite.

Rates also work backwards, as a **discount rate** for valuing future
money. A payment of $100 in five years is worth 100 / 1.05^5 ≈ $78 today
at 5%, but only 100 / 1.10^5 ≈ $62 at 10%. Because long-dated assets
have most of their value far in the future, their prices are highly
sensitive to rates — a large part of why bond prices fall when rates
rise, and why long-lived investments get hit hardest by tightening.

Finally, rates differ across borrowers and across time horizons. The
gap between a risky borrower's rate and a safe government's rate is the
**risk premium**. The pattern of rates across maturities is the **yield
curve**, which usually slopes upward and occasionally inverts —
something watched closely as a recession signal, though its reliability
is debated rather than settled.
