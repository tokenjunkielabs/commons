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

The guides credit Erdős and the prior Solymosi–Stojaković construction, and preserve the original finite-set provenance. Earlier Sidon/representation computations were not rerun. No global optimality, external-frontier, novelty, asymptotic, native-execution or sponsor claim is made.
