---
id: world-017
category: world
subcategory: cartography
difficulty: medium
source_model: opus-5
skills:
  - general-knowledge
  - tradeoff-analysis
title: Maps lie — Mercator size distortion, and what the projection is for
approx_words: 740
---

## Every flat map is wrong, and this is provable

This is not a matter of cartographers being careless. A sphere cannot be
flattened onto a plane without distortion, and the reason is a theorem.
Gauss's *Theorema Egregium* says that Gaussian curvature is intrinsic to
a surface — it can be measured from within the surface, without
reference to any surrounding space. A sphere has positive curvature; a
flat plane has zero. So no mapping between them can preserve all
distances. You can confirm the intuition with an orange peel: flatten it
and it tears or crumples.

Since you cannot preserve everything, every projection is a decision
about **what to sacrifice**. Distances, areas, angles, and shapes cannot
all survive. A projection is a trade, and the honest question is not
"which map is correct" but "which distortion is acceptable for this
task."

## What Mercator preserves

Gerardus Mercator published his in 1569 for a specific job:
**navigation under sail**.

A sailor steering a fixed compass bearing traces a curve called a rhumb
line, which on a globe spirals slowly toward a pole. Mercator's
construction has the property that **every rhumb line is a straight
line on the map**. So a navigator can lay a ruler between two points,
read the angle, and hold that bearing. That is an extraordinarily
valuable property when your instruments are a compass and a straightedge.

To get it, the projection must be **conformal**: angles are correct
locally, and small shapes are preserved. Achieving that requires
stretching the map north–south by exactly as much as the cylinder
already stretches it east–west. Since the meridians on a cylinder are
forced apart by a factor of sec(latitude) — 1/cos — the vertical spacing
must be stretched by sec(latitude) too.

## The price: areas grow as sec²

Stretch both directions by sec(φ) and area is exaggerated by **sec²(φ)**.

| Latitude | Linear factor | Area factor |
| ---: | ---: | ---: |
| 0° | 1.0 | 1.0 |
| 30° | 1.15 | 1.33 |
| 45° | 1.41 | 2.0 |
| 60° | 2.0 | 4.0 |
| 75° | 3.86 | 14.9 |

At the poles, sec is infinite, so the poles cannot be drawn at all. Web
maps typically cut off near ±85°, which conveniently makes the world a
square.

The consequences are famous. Greenland (about 2.2 million km²) appears
roughly the size of Africa (about 30 million km²), which is nearly
fourteen times larger. Greenland is in fact about the same size as the
Democratic Republic of the Congo. Alaska looks comparable to Brazil and
is roughly a fifth of it. Because most high-latitude land is in the
northern hemisphere, this systematically inflates Europe, Russia,
Canada, and the United States relative to Africa, South Asia, and South
America — which is why the projection has drawn political criticism, and
why some institutions have switched their reference maps.

## Why online maps still use it

Nearly all web mapping services use a variant called Web Mercator, and
the reason is not inertia.

Conformality means **shapes and angles are locally correct at every
zoom level**. When you are zoomed into a city, streets meet at the right
angles, roundabouts are round, and a north-up bearing means what you
expect. Since the distortion is uniform in all directions at any given
point, no local view looks stretched. The projection is also cheap to
compute and tiles neatly into square images at powers-of-two zoom
levels. For a street map, whose users are almost always looking at a
small area, these are exactly the right priorities — and the global
view, where the distortion is glaring, is the view people use least for
measurement.

## Choosing by purpose

- **Equal-area projections** (Gall–Peters, Mollweide, Eckert IV,
  Equal Earth) preserve relative area and distort shape. Correct choice
  for anything where quantity per region matters: population,
  deforestation, disease burden.
- **Compromise projections** (Robinson, Winkel Tripel — the latter
  adopted by the National Geographic Society in 1998) minimise no single
  error but keep all of them moderate. Good general reference maps.
- **Azimuthal projections** centred on a point preserve directions and
  often distances from that point. Used for flight range diagrams,
  radio coverage, and polar views.

The habit to build: when you see a world map, ask what it was made to
do. Then treat every measurement it suggests as suspect unless the
projection was chosen to preserve that particular quantity.
