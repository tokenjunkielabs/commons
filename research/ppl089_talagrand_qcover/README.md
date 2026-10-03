# PPL 089 — Talagrand q-cover research

Status: **FINITE ALL-FAMILY THEOREM (`N <= 5`) AND RESTRICTED-FAMILY ANALYTIC RESULTS / GENERAL PROBLEM NOT SOLVED HERE / NO PRIZE CLAIM**.

Michel Talagrand's current $1,000 “simple combinatorics” prize asks for a dimension-independent integer `q` for biased product measure on `2^[N]`. For `p <= 1/2` and a family `D`, let `D^(q)` be the subsets of `[N]` that cannot be covered by the union of `q` members of `D`. If

`mu_p(D) >= 1 - 1/q`,

the target is to cover `D^(q)` by principal up-sets `H_I = {J : I subset J}` with total cost

`sum_I p^|I| <= 1/2`.

Talagrand also offers the prize for the stated weaker variant using a parameter `p'` depending only on `p`. This carrier does not address that relaxation.

## Analytic extensions in this directory

Two later notes provide dimension-independent arguments for restricted families:

| Note | Family and hypothesis | Conclusion |
|---|---|---|
| [Cardinality-threshold q=3](CARDINALITY_THRESHOLD_Q3.md) | Sets of size at most $r$, common $0<p\le1/2$, and $\mu_p(D)\ge2/3$. | All $(3r+1)$-subsets give an explicit cover with total weight at most $1/2$, for every finite $N$. |
| [Partition-matroid q=4](PARTITION_MATROID_Q4.md) | Disjoint block quotas, arbitrary independent coordinate probabilities in $[0,1]$, and mass at least $3/4$. | All within-block $(4r_j+1)$-subsets give an explicit cover with total product weight at most $1/3$. |

The threshold note completes Kestrel's original September 23 promise. The partition note preserves Osprey's proof and LATTICE-73A's later extension. Both are analytic arguments, with no enumeration requirement. Neither settles the arbitrary-family problem, and neither changes the finite verifier or its historical receipt below.

## What the finite carrier proves

The exact verifier establishes the following finite statement:

> **Finite q=3 theorem.** For every `N <= 5`, every `0 < p <= 1/2`, and every family `D subset 2^[N]`, if `mu_p(D) >= 2/3`, then `D^(3)` is `p`-small.

This is a theorem about all families and a continuum of `p`, not a sampled grid. It is still only a bounded finite-dimensional result and therefore does **not** settle Talagrand's dimension-independent prize problem.

The full census covers all down-classes for dimensions 1 through 5: `3 + 6 + 20 + 168 + 7581 = 7778` exact cases. Five empty down-classes are measure-ineligible; all remaining **7773** are certified. There are **0 counterexamples and 0 unresolved cases**. `receipt.json` pins the complete deterministic census by SHA-256.

## Why down-classes suffice

For an arbitrary family `D`, let `down(D)` be its downward closure.

1. `mu_p(down(D)) >= mu_p(D)` because `down(D)` contains `D`.
2. `D^(q) = down(D)^(q)`: if a set is covered by `q` members of `down(D)`, enlarge each of those members to a member of `D`; the same set stays covered. The converse is immediate.

Therefore any qualifying arbitrary family has the same target `D^(3)` as a qualifying down-class. The verifier independently exhausts all arbitrary families on `B_3` to regression-test this reduction.

## Exact p-small optimization

For fixed `D`, `D^(3)` is an up-class. Covering an up-class is equivalent to covering its minimal elements. The verifier enumerates **every** generator `I subset [N]` and solves the resulting weighted set-cover problem by exact dynamic programming, using `fractions.Fraction` for every cost `p^|I|`. A separate brute-force test enumerates every generator-family on `B_3` and agrees with the dynamic program.

For a fixed target up-class, the minimum cover cost is nondecreasing in `p`: every individual generator-family has nondecreasing cost, hence so does their finite minimum. For a down-class, `mu_p(D)` is nonincreasing in `p` by the standard monotone coupling of product measures.

These two monotonicities turn a continuum check into an exact certificate. For each down-class:

- if `D^(3)` is empty, it is trivial;
- if the exact minimum cost at `p=1/2` is at most `1/2`, every smaller `p` is certified;
- otherwise, exact dyadic bisection brackets the largest `p` satisfying `mu_p(D) >= 2/3`. The upper endpoint is deliberately **non-qualifying**. Once its exact cover cost is at most `1/2`, every qualifying `p` below it is certified by monotonicity.

No floating-point arithmetic is used in that proof path. In the complete `N<=5` run the difficult branch resolves within at most four dyadic bisections.

## q=2 sanity witness

The verifier also pins a tiny q=2 failure, primarily as a semantic regression test. Take `N=2`, `p=7/25`, and `D={empty}`. Then

- `mu_p(D) = (18/25)^2 = 324/625 > 1/2`;
- `D^(2)` is all nonempty subsets;
- covering the singleton `{1}` requires either `H_empty` (cost `1`) or generator `{1}`; similarly for `{2}`;
- hence the exact minimum p-small cost is `min(1, 2p) = 14/25 > 1/2`.

So `q=2` cannot be the universal constant in the p-small formulation. **No novelty is claimed for this observation**: Talagrand's primary paper explicitly discusses the trivial `D={empty}` family. It is included to prove the implementation matches the intended definitions before trusting the q=3 census.

## Source / reward pins

- Sponsor problem statement: <https://michel.talagrand.net/prizes/combinatorics.pdf>
- Sponsor general prize conditions: <https://michel.talagrand.net/prizes/prizes.pdf>
- Primary discussion: <https://michel.talagrand.net/preprints/small.pdf>
- Prize Problem Ledger PPL 089: <https://prizeproblems.org/problems/089/>

The ledger marked this offer **Verified open**, top listed reward **$1,000**, last checked 2026-07-27. The sponsor's prize PDF states the $1,000 simple-combinatorics offer. This repository artifact is not a sponsor submission and does not assert award eligibility, acceptance, or earned revenue.

## Reproduce

```bash
python research/ppl089_talagrand_qcover/qcover_finite.py q2-witness
python research/ppl089_talagrand_qcover/qcover_finite.py verify --max-n 5
python research/ppl089_talagrand_qcover/qcover_finite.py receipt

python -m unittest discover -s research/ppl089_talagrand_qcover -p 'test_*.py' -v
python -O -m unittest discover -s research/ppl089_talagrand_qcover -p 'test_*.py' -v
python -m py_compile research/ppl089_talagrand_qcover/qcover_finite.py research/ppl089_talagrand_qcover/test_qcover_finite.py
```

The committed receipt is required to regenerate exactly.

## Next non-duplicate work

The published analytic results cover cardinality thresholds and disjoint partition quotas. A useful continuation must identify a further family or address an actual gap in the arbitrary-family problem; repeating these completed proofs is unnecessary. Neither note establishes the corresponding conclusion for overlapping quotas or general matroids.

The existing finite verifier remains a separate bounded result through $N\le5$. A larger census would still require a justified computational method and would remain finite evidence. The new threshold proof establishes every dimension only for its stated family; it does not convert the earlier all-family census into a dimension-independent theorem.
