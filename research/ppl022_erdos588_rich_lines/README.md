# Erdős 588 — exact finite line incidence

Status: **PUBLIC EXACT INTEGER-PLANE API / COMPLETE FINITE DATA / EXACT FIXED-HOST OPTIMUM**.

The [original Erdős problem](https://www.renyi.hu/~p_erdos/1984-18.pdf), Problem 36 in *Research problems* (1984), asks about the maximal number of $k$-point lines in an $n$-point real-plane set with no line containing more than $k$ points, for fixed $k>3$.

This directory delivers a connected-V8/CommonJS API for exact integer coordinates. It enumerates each unordered point pair once, stores unique primitive line equations and all incident point IDs, checks the required maximum-collinearity condition, and supports subset views from the retained line records. A snapshot restorer certifies complete saved incidence without reconstructing the original pairs.

| File | Purpose |
|---|---|
| [integer_line_incidence.cjs](integer_line_incidence.cjs) | Public constructor, snapshot restoration, multiplicity profiles, $P_k$ assessments, subset views and paged exports. |
| [INTEGER_LINE_INCIDENCE_API.md](INTEGER_LINE_INCIDENCE_API.md) | Source conventions, completeness arguments, API contract, bounds and original actual results. |
| [sidon_grid_and_cyclic_subset.json](sidon_grid_and_cyclic_subset.json) | Complete 100-point source geometry and original 40-point subset, every line/point incidence, assessments and execution evidence. |
| [CYCLE_SWITCH_TEMPLATE_OPTIMUM.md](CYCLE_SWITCH_TEMPLATE_OPTIMUM.md) | Explicit four-cycle switch, complete fixed-host upper-bound argument and new finite result. |
| [cycle_switch_template_optimum.json](cycle_switch_template_optimum.json) | Complete new 40-point subset, all 663 lines, the switch, assessments, paged outputs and retained upper-bound input. |
| [integer_plane_projection.cjs](integer_plane_projection.cjs) | Explicit bounded integer projection preserving distinct points and all collinear/noncollinear triples. |
| [INTEGER_PLANE_PROJECTION_API.md](INTEGER_PLANE_PROJECTION_API.md) | Projection theorem, input/output contract, hard bounds and actual cube result. |
| [projected_cube_64.json](projected_cube_64.json) | All 64 source/projected cube points, both ID maps, 1,492 lines, incidence assessments and paged exports. |
| [grid_line_histogram.cjs](grid_line_histogram.cjs) | Exact full grid histograms from Möbius-factorized segment counts, without geometric enumeration. |
| [GRID_LINE_HISTOGRAM_API.md](GRID_LINE_HISTOGRAM_API.md) | Published attribution, full derivation, integer limits and theorem-derived planar interpretation. |
| [grid5_dim12_histogram.json](grid5_dim12_histogram.json) | Complete actual histogram for 244,140,625 points, all shared powers, Möbius terms and pair-accounting evidence. |
| [rectangular_5pow12_7pow3_histogram.json](rectangular_5pow12_7pow3_histogram.json) | Exact rectangular composition using the accepted 5^12 factor and one new 7^3 factor, with complete source/product witnesses. |

## The retained host and the fixed-host optimum

The actual host is $H=S\times S$, with the retained ten-element set from Commons #31157, carried unchanged by #31177. The accepted #31227 ledger has 100 points and 3,970 distinct lines: 3,921 ordinary lines, 28 three-point lines and 21 ten-point lines. Thus $T_4(H)=21$.

The original 40-point cyclic-offset subset has 642 ordinary lines, six three-point lines and 20 four-point lines, with no five collinear points. Its complete 668-line certificate remains unchanged.

A four-cycle switch preserves all row/column counts and adds four main-diagonal points. The new 40-point subset has 636 ordinary lines, six three-point lines and **21 four-point lines**, again with no five collinear points. Every line containing four selected points must be one of the host's 21 at-least-four-point lines. The new subset attains all 21.

Consequently, the maximum among 40-point $P_4$ subsets of this fixed host is exactly 21. The construction also gives

$$
f_4(40)\ge21.
$$

This does not identify the global extremal value over arbitrary planar configurations.

Both subset consumers reuse the persisted host incidence; the new switch repeats no host point-pair construction or old-subset computation. The public module, original guide and original data remain unchanged by the continuation.


## Explicit projection from higher dimensions

The new projection API translates a finite integer set coordinatewise, chooses the exact base $t=\max(2,2D^2+1)$ from its largest coordinate span $D$, and uses separated exponents in two integer linear forms. A direct leading-coefficient bound preserves distinct points and every collinear/noncollinear triple. The projection enumerates no pairs or triples.

The same derivation gives a finite family: for integers $k\ge4$ and $d\ge1$, projection of $\{0,\ldots,k-1\}^d$ preserves exactly $((k+2)^d-k^d)/2$ $k$-point lines and no larger collinear subset. Hence $f_k(k^d)\ge((k+2)^d-k^d)/2$. The theorem's finite-family scope is separate from the executable API's size limits.

The actual new input $\{0,1,2,3\}^3$ projects at base 19 to 64 planar points. It has 1,344 two-point lines, 72 three-point lines and 76 four-point lines, with no five collinear points. This supplies the finite lower bound

$
f_4(64)\ge76.
$

Every projected point, source/planar ID correspondence and all 1,492 line records are retained. The public projection accepts dimensions 1 through 8 and uses explicit integer/digit limits. The unchanged incidence module consumed this new configuration once; no earlier host or subset was recomputed.

The projection guide credits the prior generic-projection construction and makes no claim of global optimality or priority.


## Full histograms without enumerating a grid

The histogram API counts consecutive primitive-step segments with Möbius inversion and obtains exact line counts by second differences. The guide credits Haukkanen–Merikoski's published general-grid segment/line identities. Shared integer powers are cached, and all arithmetic uses bounded BigInt operations.

The new actual input $\{0,1,2,3,4\}^{12}$ has 244,140,625 points. Its complete histogram is:

| Multiplicity | Exact lines |
|---:|---:|
| 2 | 29,767,389,101,298,792 |
| 3 | 11,366,735,095,072 |
| 4 | 127,495,551,352 |
| 5 | 6,798,573,288 |

Every count is theorem-derived; no points, pairs, projected coordinates or individual lines were enumerated. The existing finite projection theorem gives the planar lower bound $f_5(244140625)\ge6798573288$. The projection API's separate dimension/digit limits remain unchanged.

The saved record contains every Möbius coefficient, all five shared powers, all eight contribution terms and both exact pair-accounting sums. No accepted configuration was recomputed.


## Rectangular composition from saved power tables

The same grid module now composes source-identified uniform power-basis results for rectangular Cartesian products. It requires complete scale and Möbius premises, checks their structure and algebraic fields, and preserves their source identities. Stored powers are reused without re-exponentiation; source validity remains an explicit premise.

The actual product $\{0,\ldots,4\}^{12}\times\{0,\ldots,6\}^3$ has 83,740,234,375 points and 47,119,140,625 seven-point lines, with no longer line. All six line-multiplicity counts and every factor/product contribution are retained. The accepted $5^{12}$ result was not rerun; only the new $7^3$ factor and the composition were computed.

The finite projection theorem gives $f_7(83740234375)\ge47119140625$. No coordinates, pairs or individual incidences were enumerated, and the projection API's runtime caps remain unchanged.

The guides credit Erdős and the prior Solymosi–Stojaković construction, and preserve the original finite-set provenance. Earlier Sidon/representation computations were not rerun. No global optimality, external-frontier, novelty, asymptotic, native-execution or sponsor claim is made.
