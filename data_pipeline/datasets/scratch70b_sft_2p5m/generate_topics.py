"""Build ~1,056 writer assignments for a 1M-token from-scratch mix (2.5M hard cap)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOPICS_PATH = ROOT / "topics.jsonl"
BATCH_DIR = ROOT / "batches"
DOCS_PER_BATCH = 12

# 370+211+127+106+85+74+53+30 = 1056 → ~1.0M heuristic tokens at ~720 words.
QUOTAS = {
    "chat": 370,
    "code": 211,
    "math": 127,
    "science": 106,
    "logic": 85,
    "reasoning_habits": 74,
    "world": 53,
    "how_things_work": 30,
}

CHAT_SITUATIONS = [
    "a late bus on a rainy weeknight",
    "a first day in a shared kitchen",
    "a neighbor's smoke alarm that will not stop",
    "returning a shirt that shrank",
    "booking a dentist after three years",
    "a group project where one person vanished",
    "explaining a parking ticket to a roommate",
    "a job interview after a career gap",
    "asking a librarian for a quiet corner",
    "a family dinner where politics comes up",
    "teaching a parent how to use a password manager",
    "a barista getting a complicated order wrong twice",
    "waiting rooms and a delayed appointment",
    "a hiking friend who wants to turn back",
    "negotiating chores after a messy weekend",
    "a small-town hardware store for a broken latch",
    "a teacher conference about one missing assignment",
    "comforting someone after a failed driving test",
    "planning a cheap birthday without making it sad",
    "a noisy upstairs neighbor at 1 a.m.",
    "splitting a restaurant bill when someone ordered extra",
    "a lost wallet at a train station",
    "telling a friend their joke landed badly",
    "a first call with a new doctor",
    "declining a weekend trip without lying",
    "a coworker who replies-all to everything",
    "helping a teen set up a bank account",
    "a landlord visit that was supposed to be ten minutes",
    "buying a used bike from a stranger",
    "a wedding RSVP when money is tight",
    "explaining jet lag to a toddler",
    "a gym induction with a nervous beginner",
    "asking for a deadline extension without sounding flaky",
    "a power cut during remote work",
    "returning a library book that is two weeks late",
    "a potluck where two people brought the same dish",
    "talking through a scary medical leaflet",
    "a tourist asking for directions you are unsure of",
    "a sibling borrowing the car again",
    "an online seller who shipped the wrong size",
    "a first meeting with a new roommate's partner",
    "calming someone who thinks they locked the keys inside",
    "a community garden plot that got overwatered",
    "telling a coach you need a rest day",
    "a noisy cafe used as an office",
    "a delayed flight and one shared charger",
    "asking a neighbor to watch a package",
    "a school play costume that fell apart",
    "explaining a credit card fee to a parent",
    "a first therapy session small talk",
    "a volunteer shift that ran long",
    "a friend who keeps 'just dropping by'",
    "a messy breakup of a group chat",
    "buying flowers when you do not know the names",
    "a night bus conversation that got too personal",
    "a new employee learning the coffee machine politics",
    "a parent-teacher email that sounds harsher than meant",
    "a camping trip with one person who hates bugs",
    "asking for gluten-free options without making a scene",
    "a noisy construction week and a baby next door",
    "a first date that is going awkwardly well",
    "returning to a hobby after years away",
    "a coworker taking credit in a meeting",
    "a broken washing machine on laundry day",
    "explaining a meme to a grandparent",
    "a sports team that keeps losing politely",
    "a surprise visit from relatives",
    "a quiet argument in a supermarket aisle",
    "teaching someone to ride a bike again",
    "a hospital waiting-room update",
    "a missed birthday and how to recover",
    "a noisy open-plan office phone call",
    "asking a stranger to take a photo",
    "a DIY shelf that is not level",
    "a book club that did not read the book",
    "a teen wanting a later curfew",
    "a colleague who microwaves fish",
    "planning a move across town on a budget",
    "a pet that ate something it should not",
    "a first snow for someone from a warm city",
    "a festival crowd and a lost child protocol",
    "a slow computer at a public library",
    "a friend who only talks about work",
    "a leak under the kitchen sink",
    "a community meeting about a new bike lane",
    "an apology after snapping in traffic",
    "a first time cooking for in-laws",
    "a delayed paycheck conversation with a landlord",
    "a museum guard and a no-photo rule",
    "a haircut that went shorter than asked",
    "a night of studying with a noisy housemate",
    "a farmer-market vendor and a card reader that fails",
    "a first standup meeting at a new job",
    "a friend asking to borrow money",
    "a heatwave without air conditioning",
    "a school pickup mix-up",
    "a concert where someone is too tall in front",
    "a first time voting and a confusing ballot",
    "a broken zipper ten minutes before leaving",
    "a neighbor's cat that moved in",
]

CHAT_GOALS = [
    "keep the tone kind and specific",
    "say no without inventing an excuse",
    "ask one clarifying question before advising",
    "narrate what you would do in the next ten minutes",
    "translate jargon into plain speech",
    "offer two options and a recommendation",
    "admit uncertainty instead of bluffing",
    "de-escalate without being fake-cheerful",
    "make a plan that fits a tight budget",
    "check that the other person still wants help",
]

CODE_TASKS = [
    "off-by-one in a binary search",
    "a hash map vs scanning a list",
    "mutable default arguments in Python",
    "why this nested loop is quadratic",
    "BFS versus DFS on a grid",
    "matching parentheses with a stack",
    "prefix sums for range queries",
    "two pointers reversing words in a sentence",
    "a race on a shared counter",
    "retrying PUT vs POST",
    "stable versus unstable sorts",
    "memoized Fibonacci call counts",
    "greedy coin change that fails",
    "topological sort of courses",
    "XOR to find an unpaired number",
    "sliding window with two distinct characters",
    "hash collisions and equality",
    "recursion vs iteration for factorial",
    "a leaking file handle",
    "SQL N+1 queries",
    "0-based vs 1-based page offsets",
    "UTF-8 vs code-unit length",
    "a cache that never expires",
    "boolean flags that mean three states",
    "copy-paste of a regex that is too greedy",
    "integer division truncating a rate",
    "timezone-naive datetime subtraction",
    "a CSV with commas inside quotes",
    "JSON keys that look like numbers",
    "a linked list cycle",
    "binary heap vs sorted array",
    "an idempotent webhook handler",
    "pagination that skips rows on insert",
    "a deadlocked pair of locks",
    "floating point money",
    "off-by-one in slice end indices",
    "a generator that cannot be reused",
    "closure over a loop variable",
    "string concatenation in a hot loop",
    "an API that returns 200 on failure",
    "null vs empty list",
    "a bitmask for feature flags",
    "shortest path vs spanning tree",
    "a trie for autocomplete",
    "modulo for wrapping indices",
    "a bloom filter false positive",
    "consistent hashing at a glance",
    "a debounce versus throttle",
    "UTF-16 surrogate pairs",
    "an off-heap cache eviction bug",
    "comparing floats with epsilon",
    "a circular buffer overwrite",
    "endianness in a binary file",
    "a CORS preflight that fails",
    "SQL injection via string format",
    "a TOCTOU file replace",
    "reference vs copy of a dict",
    "a Python GIL misunderstanding",
    "tail recursion that is not optimized",
    "an off-by-one in a window size",
]

MATH_TASKS = [
    "completing the square on a non-monic quadratic",
    "Bayes on a rare medical test",
    "percent change vs percentage points",
    "expected value of a simple dice game",
    "work-rate two pipes filling a tank",
    "similar triangles and a shadow",
    "mean vs median on skewed incomes",
    "modular arithmetic on a clock",
    "combinations vs permutations of a team",
    "logs undoing exponents",
    "arithmetic vs geometric sequences",
    "unit-circle sine at special angles",
    "dimensional analysis of a road trip",
    "inclusion-exclusion of two clubs",
    "inverse of a linear function",
    "Fermi estimate of piano tuners",
    "a linear system by elimination",
    "compound interest for three years",
    "a false 'average speed' of a round trip",
    "units of a density calculation",
    "slope as a rate with real units",
    "a 3-4-5 triangle scaled by 2.5",
    "probability of at least one six in n rolls",
    "converting a repeating decimal",
    "the area of a ring (annulus)",
    "weighted averages of class grades",
    "exponential doubling time",
    "a proportion that is not linear",
    "degrees vs radians in a small program",
    "variance of two-point data by hand",
    "a mixture of 2% and 5% solutions",
    "Pythagorean distance on a city grid vs straight line",
    "log-scale reading of a chart",
    "the pigeonhole idea with remainders",
    "a recursive sequence first five terms",
    "percent error vs absolute error",
    "solving for time in d = vt + 1/2 at^2 with numbers",
    "a 2x2 determinant as area",
    "conditional probability with a two-way table",
    "the harmonic mean of two speeds",
    "floor division vs rounding",
    "a piecewise function at the join",
    "base-10 vs base-2 length of a number",
    "a confidence interval spoken carefully",
    "Simpson's paradox in two hospitals",
    "expected waits vs typical waits",
    "a unit conversion that cubes",
    "the binomial coefficient C(10,3) by hand",
    "an arithmetic series sum",
    "a geometric series that should not be infinite",
    "radians of a 40-degree slice",
    "a ratio table that stays consistent",
    "solving |x-3| = 5",
    "a function and its inverse swap",
]

SCIENCE_TASKS = [
    "why seasons happen",
    "photosynthesis as a mass balance",
    "Newton's third law on a skateboard",
    "why ice floats",
    "a bouncing ball losing energy",
    "pH as a log scale",
    "DNA vs RNA in one cell story",
    "Ohm's law in a series circuit",
    "natural selection in a beetle color",
    "why the sky is blue",
    "plate tectonics vs the crust you walk on",
    "half-life with 16 atoms",
    "greenhouse gases vs the ozone hole",
    "osmosis in a raisin",
    "a feedback loop in a thermostat",
    "experimental controls in a fertilizer test",
    "why a metal spoon feels colder",
    "surface tension and a water strider",
    "a closed vs open circulatory sketch",
    "the difference between mass and weight",
    "why mountains are colder",
    "a simple food web with one shock",
    "evaporation cooling your skin",
    "why we see lightning before thunder",
    "a magnet and a coil inducing current",
    "the carbon cycle in a backyard",
    "why blood is red and veins look blue",
    "a catalyst that is not used up",
    "density stacking oil and water",
    "the greenhouse of a parked car",
    "why salt melts ice",
    "a nerve impulse as a chain of gates",
    "the difference between weather and climate",
    "why the moon has phases",
    "a plant bending toward a window",
    "why stainless steel rusts slowly",
    "the Doppler idea with a siren",
    "a calorie as energy not a nutrient",
    "why a vacuum flask works",
    "mitosis vs meiosis in one contrast",
    "the inverse-square idea for light",
    "why ears pop in an elevator",
    "a battery as a chemistry trick",
    "the water table after a dry month",
    "why high voltage for long wires",
]

LOGIC_TASKS = [
    "if-then vs only-if",
    "affirming the consequent",
    "necessary vs sufficient",
    "correlation is not causation",
    "base-rate neglect with taxis",
    "survivorship bias on airplanes",
    "Simpson's paradox hospitals",
    "expected value vs what usually happens",
    "quantifier scope: every vs some",
    "proof by contradiction that sqrt(2) is irrational, sketched",
    "pigeonhole with hairs",
    "a false dichotomy",
    "a leaky analogy about atoms",
    "calibration when you say 70 percent",
    "post hoc ergo propter hoc",
    "a motte-and-bailey move",
    "equivocation on the word 'theory'",
    "an anecdotal N=1",
    "moving the goalposts",
    "a straw man of a climate claim",
    "burden of proof reversal",
    "a No True Scotsman",
    "circular definition of 'natural'",
    "slippery slope that skips steps",
    "appeal to nature",
    "appeal to popularity",
    "the Texas sharpshooter",
    "cherry-picking a time window",
    "a hidden confounder",
    "the prosecutor's fallacy",
    "denying the antecedent",
    "a composition fallacy",
    "an ecological fallacy",
    "a just-world story",
    "the gambler's fallacy",
    "a false precision of 3.141592",
    "whataboutery",
    "a euphemism treadmill",
    "reification of an average",
    "a category error",
    "begging the question in a short argument",
    "an undistributed middle",
    "a hasty generalization from three examples",
    "the streetlight effect",
    "a tautology dressed as news",
    "moral luck in a driving story",
    "a double standard on anecdotes",
    "the sharpshooter on a scatterplot",
]

HABIT_TASKS = [
    "units as a bug detector",
    "working a special case first",
    "bounding an answer before computing",
    "restating the question in one sentence",
    "working backwards from a candidate",
    "drawing a table",
    "sanity-checking a percentage",
    "naming what you do not know",
    "given-want-bridge",
    "independent-method cross-check",
    "tracking definitions",
    "time-boxing a stuck proof",
    "Fermi estimates as a prior",
    "explaining to a skeptical friend",
    "checking extreme values",
    "replacing a word with a number",
    "drawing the axes before the curve",
    "writing the opposite claim",
    "a one-line invariant",
    "counting degrees of freedom",
    "asking what would falsify this",
    "separating 'can't' from 'don't know'",
    "doing the units last as a check",
    "a rubber-duck restatement",
    "comparing to a known analog",
    "splitting a hard thing into two easier ones",
    "refusing to multiply incompatible units",
    "writing a tiny example before the formula",
    "checking symmetry",
    "the 'off by a factor of two' hunt",
    "naming the audience of a proof",
    "keeping an error budget",
    "a pre-mortem of a calculation",
    "switching representation (picture vs algebra)",
    "asking who measured this",
    "a checklist before submitting",
    "not averaging ratios blindly",
    "labeling every column",
    "sleeping on a stuck bug",
    "the 'what is the output type' question",
    "reducing to a previously solved problem",
    "writing the negation carefully",
    "a Fermi check against a receipt",
    "keeping a running estimate",
    "drawing the system boundary",
]

WORLD_TASKS = [
    "why time zones exist",
    "continents vs tectonic plates",
    "the water cycle as a budget",
    "how vaccines train immunity at a high level",
    "supply and demand at a street stall",
    "inflation vs a scarcity spike",
    "how a bill becomes a law, roughly",
    "why coastal cities are not destiny",
    "leap years and February",
    "latitude, longitude, GPS",
    "language families vs writing systems",
    "what different energy sources convert",
    "macronutrient basics",
    "interest as the price of borrowing",
    "public goods vs private goods",
    "why the equator is hot",
    "Mercator distortion",
    "writing systems: sound vs meaning",
    "why some countries drive on the left",
    "what a census is for",
    "how a central bank is not a shop",
    "why passports exist",
    "the idea of a time-use survey",
    "what GDP leaves out",
    "how a union local differs from a company",
    "why daylight saving is argued",
    "a tariff vs a quota in one stall story",
    "what 'real' vs 'nominal' means for a paycheck",
    "how a primary election is not the general",
    "why river mouths get cities",
    "what a reserve currency is in plain speech",
    "how a coop grocery is owned",
    "why some maps use equal-area projections",
    "a literacy rate is not a reading test",
    "what a patent is supposed to trade",
    "how a drought becomes a food-price story",
    "why radio spectrum is allocated",
    "what a municipal bond is for",
    "how a jury is not a poll",
    "why some languages have official status",
    "a trade deficit in one shipping story",
    "what zoning is trying to do",
    "how a public library is funded, roughly",
    "why earthquakes cluster at plate edges",
    "what 'median household' hides",
]

HOW_TASKS = [
    "a refrigerator moving heat",
    "a toilet fill valve",
    "bicycle gear ratios",
    "a three-way light switch",
    "a pin-tumbler lock",
    "a microwave heating water",
    "LED vs incandescent",
    "a lithium-ion cell at high-school chemistry",
    "septic vs sewer",
    "a GPS position fix",
    "chip vs magstripe",
    "a heat pump colder than inside",
    "tension and compression in a truss",
    "parity error correction",
    "compiler vs interpreter",
    "a DNS lookup chain",
    "a smoke detector ionization vs photoelectric",
    "how a zipper meshes",
    "a ballcock vs a modern fill valve",
    "how a transformer steps voltage",
    "a clutch on a bicycle hub",
    "how a key fob rolling code thinks",
    "a septic leach field",
    "how a speaker makes sound",
    "a fridge capillary tube",
    "how a NAND flash page is written, roughly",
    "a GFCI outlet",
    "how a carburetor vs fuel injection, one idea",
    "a lock washer",
    "how a quartz watch ticks",
    "a heat exchanger in a furnace",
    "how a barcode is just a number",
    "a diode as a one-way street",
    "how a thermostat deadband works",
    "a centrifugal pump",
    "how a ball bearing takes load",
    "a PWM LED dimmer",
    "how a search index is not grep",
    "a pressure cooker seal",
    "how a differential on a car, one sentence then expand",
    "a fuse vs a breaker",
    "how a capacitor filters a supply",
    "a worm gear",
    "how HTTPS names a certificate, roughly",
    "a float switch",
]

AUDIENCES = [
    "a sharp 14-year-old",
    "a tired coworker on a break",
    "someone who almost has it",
    "a skeptical uncle",
    "a new intern",
    "yourself last year",
]


def _skills(category: str) -> list[str]:
    if category == "chat":
        return ["conversational", "instruction-following"]
    if category == "code":
        return ["worked-solution", "check-your-work"]
    if category in {"math", "science", "logic"}:
        return ["worked-solution", "causal-explanation"]
    if category == "reasoning_habits":
        return ["check-your-work", "metacognition"]
    return ["causal-explanation", "general-knowledge"]


def _subcategory(category: str) -> str:
    return {
        "chat": "everyday-dialogue",
        "code": "programming",
        "math": "school-math",
        "science": "physical-and-life",
        "logic": "argument",
        "reasoning_habits": "method",
        "world": "civics-and-earth",
        "how_things_work": "mechanism",
    }[category]


def _difficulty(i: int) -> str:
    return ("easy", "medium", "hard")[i % 3]


def _prefix(category: str) -> str:
    return {
        "chat": "chat",
        "code": "code",
        "math": "math",
        "science": "science",
        "logic": "logic",
        "reasoning_habits": "habits",
        "world": "world",
        "how_things_work": "how",
    }[category]


def _expand(tasks: list[str], n: int, kind: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    i = 0
    while len(out) < n:
        task = tasks[i % len(tasks)]
        aud = AUDIENCES[i % len(AUDIENCES)]
        if kind == "chat":
            goal = CHAT_GOALS[i % len(CHAT_GOALS)]
            title = f"Talk through {task}"
            angle = f"Write a spoken dialogue. Goal: {goal}. Audience feel: {aud}."
        else:
            title = task[0].upper() + task[1:]
            angle = (
                f"Teach {task} to {aud}. Use a concrete number or tiny example. "
                f"Close with a limiting case or a check."
            )
        out.append({"title": title, "angle": angle, "seed": task})
        i += 1
        if i > n * 8:
            raise RuntimeError(f"could not expand {kind} to {n}")
    return out[:n]


def build_topics() -> list[dict[str, object]]:
    banks = {
        "chat": _expand(CHAT_SITUATIONS, QUOTAS["chat"], "chat"),
        "code": _expand(CODE_TASKS, QUOTAS["code"], "code"),
        "math": _expand(MATH_TASKS, QUOTAS["math"], "math"),
        "science": _expand(SCIENCE_TASKS, QUOTAS["science"], "science"),
        "logic": _expand(LOGIC_TASKS, QUOTAS["logic"], "logic"),
        "reasoning_habits": _expand(HABIT_TASKS, QUOTAS["reasoning_habits"], "habits"),
        "world": _expand(WORLD_TASKS, QUOTAS["world"], "world"),
        "how_things_work": _expand(HOW_TASKS, QUOTAS["how_things_work"], "how"),
    }
    topics: list[dict[str, object]] = []
    for category, items in banks.items():
        prefix = _prefix(category)
        for i, item in enumerate(items, start=1):
            doc_id = f"{prefix}-{i:04d}"
            # Keep titles unique when the seed list repeats.
            title = item["title"]
            if i > len(
                {
                    "chat": CHAT_SITUATIONS,
                    "code": CODE_TASKS,
                    "math": MATH_TASKS,
                    "science": SCIENCE_TASKS,
                    "logic": LOGIC_TASKS,
                    "reasoning_habits": HABIT_TASKS,
                    "world": WORLD_TASKS,
                    "how_things_work": HOW_TASKS,
                }[category]
            ):
                title = f"{title} (pass {((i - 1) // 50) + 1})"
            topics.append(
                {
                    "id": doc_id,
                    "category": category,
                    "subcategory": _subcategory(category),
                    "difficulty": _difficulty(i),
                    "title": title,
                    "angle": item["angle"],
                    "skills": _skills(category),
                    "filename": f"{doc_id}.md",
                }
            )
    topics.sort(key=lambda t: t["id"])
    return topics


def _slug(title: str) -> str:
    keep = []
    for ch in title.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in " -_/":
            keep.append("-")
    slug = "".join(keep).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:60] or "topic"


def write_batches(topics: list[dict[str, object]]) -> list[Path]:
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    for old in BATCH_DIR.glob("batch-*.json"):
        old.unlink()
    paths: list[Path] = []
    for start in range(0, len(topics), DOCS_PER_BATCH):
        chunk = topics[start : start + DOCS_PER_BATCH]
        n = start // DOCS_PER_BATCH + 1
        path = BATCH_DIR / f"batch-{n:03d}.json"
        path.write_text(json.dumps({"batch": n, "topics": chunk}, indent=2) + "\n")
        paths.append(path)
    return paths


def main() -> None:
    topics = build_topics()
    TOPICS_PATH.write_text("".join(json.dumps(t) + "\n" for t in topics))
    batches = write_batches(topics)
    print(f"wrote {len(topics)} topics -> {TOPICS_PATH}")
    print(f"wrote {len(batches)} batches of {DOCS_PER_BATCH} -> {BATCH_DIR}")


if __name__ == "__main__":
    main()
