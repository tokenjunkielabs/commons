# Erdős 588 — exact finite line incidence

Status: **PUBLIC EXACT INTEGER-PLANE API AND COMPLETE FINITE DATA / NO EXTREMAL OR ASYMPTOTIC CLAIM**.

The [original Erdős problem](https://www.renyi.hu/~p_erdos/1984-18.pdf), Problem 36 in *Research problems* (1984), asks about the maximal number of $k$-point lines in an $n$-point real-plane set with no line containing more than $k$ points, for fixed $k>3$.

This directory delivers a connected-V8/CommonJS API for exact integer coordinates. It enumerates each unordered point pair once, stores unique primitive line equations and all incident point IDs, checks the required maximum-collinearity condition, and supports subset views from the retained line records. A snapshot restorer certifies complete saved incidence without reconstructing the original pairs.

| File | Purpose |
|---|---|
| [integer_line_incidence.cjs](integer_line_incidence.cjs) | Public constructor, snapshot restoration, multiplicity profiles, $P_k$ assessments, subset views and paged exports. |
| [INTEGER_LINE_INCIDENCE_API.md](INTEGER_LINE_INCIDENCE_API.md) | Source conventions, completeness arguments, API contract, bounds and actual results. |
| [sidon_grid_and_cyclic_subset.json](sidon_grid_and_cyclic_subset.json) | Complete 100-point source geometry, 40-point subset, every line/point incidence, assessments and execution evidence. |

The actual input uses the retained ten-element set from Commons #31157, carried unchanged by #31177. The 100-point Cartesian product has 3,970 distinct lines: 3,921 ordinary lines, 28 three-point lines and 21 ten-point lines.

A new 40-point cyclic-offset subset has exactly 642 ordinary lines, six three-point lines and 20 four-point lines, with no five collinear points. It therefore supplies the finite lower bound

$$
f_4(40)\ge20.
$$

All 668 subset line records are retained. The API formed the subset in a fresh connected V8 call after restoring the complete saved source snapshot; it repeated no point-pair construction.

The guide credits Erdős and the prior Solymosi–Stojaković construction, and preserves the original finite-set provenance. The earlier Sidon search and ordered-representation computations were not rerun. No optimality, external-frontier, novelty, native-execution or sponsor claim is made.
