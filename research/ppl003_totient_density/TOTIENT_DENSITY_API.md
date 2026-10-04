# Exact finite-prime bounds for the totient-ratio distribution

The public `totient_density_index.cjs` API constructs weighted prime-subset atoms, retains every basis version, and produces exact rational bounds for the asymptotic distribution of $\varphi(n)/n$. Saved indexes support fresh queries and incremental prime appends without another sieve, reconstruction of old atoms, enumeration of a primorial period or an integer-prefix totient scan.

One actual consumer at **2026-10-04 17:09:52.352 UTC** constructed the first ten primes, reopened the saved index, appended prime 31, and reopened again for an interval and atom-page query. With the first eleven primes and sieve cutoff 4096, the result is

$$
0.5103142093\ \le f(1/2)\ \le 0.5243209606,
$$

where

$$
f(c)=\lim_{X\to\infty}\frac1X
\#\{1\le n\le X:\varphi(n)/n<c\}.
$$

The displayed decimals are rounded outward from the exact fractions retained below. The same index bounds the density of $1/2\le\varphi(n)/n<3/4$ between **0.1629740801 and 0.1951750149**. These are bounds for the limiting distribution over all positive integers. They are not measured proportions of a sampled or scanned finite prefix.

The complete calculation, 4,095 retained atom rows, 1,115 upper-bound contributions, prime-tail records and five queries are in [finite_prime_density_bounds.json](finite_prime_density_bounds.json). This work supplies a bounded reusable numerical method; it does not resolve the positive-derivative question, assert novelty, or make a prize or acceptance claim.

## Problem and source status

The [retrieved Formal Conjectures statement](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/50.lean), Git blob `bc1ea50a170839b20f3c8b69ea4dc94180c22d3e`, defines the strict density on $[0,1]$ and asks whether a positive derivative within that interval can exist at any point. The retrieved file labels that question research-open. It labels existence and singularity results solved, but its theorem bodies contain `sorry` placeholders. Those annotations are source metadata, not completed formal proofs.

For an accessible primary research account of the classical distribution, Banerjee, Chahal, Chaubey and Khurana, [*Distribution of values of general Euler totient function*, arXiv:2304.02540v1](https://arxiv.org/pdf/2304.02540), introduction equation (1.1), credits Schoenberg with existence of a continuous monotone distribution and endpoints 0 and 1. Their displayed convention uses $\le$; continuity gives the same limiting function for the strict convention used here.

A bounded primary-literature check supplied no resolution of the positive-derivative question. This is a limited no-finding, not an independent confirmation that the problem remains open. The canonical problem page returned an access error once and was not retried. The present guide relies on the retrieved statement for the target and the cited primary paper for its explicit existence/continuity attribution. It does not claim an independent literature verification of singularity.

The enclosure proof below first bounds the liminf and limsup of the finite proportions. It therefore stands independently of the source file's placeholder theorem bodies. The classical existence result identifies the two middle limits with $f(c)$.

## 1. Exact CRT atoms

Fix the first $m$ primes $P_y=\{p:p\le y\}$ and

$$
Q=\prod_{p\le y}p,\qquad
R_y(n)=\prod_{\substack{p\le y\\p\mid n}}\left(1-\frac1p\right).
$$

For $S\subseteq P_y$, define the divisibility class

$$
A_S=\{n:p\mid n\iff p\in S,\ \text{for every }p\le y\}.
$$

The Chinese remainder theorem gives exactly

$$
w_S=\prod_{p\in P_y\setminus S}(p-1)
$$

residue classes modulo $Q$ in $A_S$. Its density is $\alpha_S=w_S/Q$, and $R_y(n)$ has the constant value

$$
r_S=\prod_{p\in S}\frac{p-1}{p}
$$

on that class. The weights are **integer residue counts**; they are not normalized probabilities. Their total is

$$
\sum_S w_S=\prod_{p\le y}((p-1)+1)=Q.
$$

This constructs $2^m$ weighted atoms without iterating through the $Q$ residue classes.

### Distinct ratios and ordered incremental construction

The ratios $r_S$ are distinct. If two were equal, cancel the common prime subsets and choose the largest prime $\ell$ in their symmetric difference. Cross-multiplication puts a factor $\ell$ on one side. Every factor on the other side is either a smaller prime or one less than a prime no larger than $\ell$. None is divisible by $\ell$, contradicting equality.

Appending the next prime $p$ transforms each old atom as follows:

| New divisibility condition | New ratio | New integer weight | New common denominator |
|---|---|---|---|
| $p\nmid n$ | $r$ | $w(p-1)$ | $Qp$ |
| $p\mid n$ | $r(p-1)/p$ | $w$ | $Qp$ |

For normalized masses these are instead $\alpha(p-1)/p$ and $\alpha/p$. Both child streams preserve the previous ratio order: one is unchanged and the other is multiplied by the same positive constant. An exact rational merge creates the new sorted table in linear row work. The old basis versions remain retained. Cross-stream ties cannot occur by the distinctness proof.

The implementation reduces new ratios with BigInt gcd, merges with exact cross-products and accumulates integer prefix weights. A binary search then finds the number of atoms with $r_S\le c$.

## 2. A computable prime-tail bound

Set

$$
U_y(n)=\frac{\varphi(n)/n}{R_y(n)}
=\prod_{\substack{p>y\\p\mid n}}\left(1-\frac1p\right).
$$

The elementary product inequality gives

$$
0\le1-U_y(n)\le\sum_{\substack{p>y\\p\mid n}}\frac1p.
$$

For every positive integer $X$,

$$
\frac1X\sum_{n\le X}(1-U_y(n))
\le
\sum_{p>y}\frac{\lfloor X/p\rfloor}{Xp}
\le
\sum_{p>y}\frac1{p^2}.
$$

The last series converges. For an integer $z\ge y$,

$$
B_y^{\rm exact}:=\sum_{p>y}\frac1{p^2}
\le
T_{y,z}:=\sum_{y<p\le z}\frac1{p^2}+\frac1z,
$$

because

$$
\sum_{p>z}\frac1{p^2}
\le\sum_{k=z+1}^{\infty}\frac1{k^2}
\le\sum_{k=z+1}^{\infty}\frac1{k(k-1)}
=\frac1z.
$$

The implementation's ordinary sieve constructs every prime through $z$. It uses the fixed integer $D=10^{12}$ and retains

$$
\beta_y=\left\lceil\frac D z\right\rceil+
\sum_{y<p\le z}\left\lceil\frac D{p^2}\right\rceil,\qquad
\widehat B_y=\frac{\beta_y}{D}.
$$

Thus $B_y^{\rm exact}\le T_{y,z}\le\widehat B_y$. If $K$ primes occur in that finite tail, the extra rounding satisfies

$$
0\le\widehat B_y-T_{y,z}<\frac{K+1}{D}.
$$

The artifact retains every individual ceiling term and the complete suffix sums. Appending a basis prime selects the next saved suffix; it does not rerun the sieve or re-create the tail terms.

For the actual sieve $z=4096$, there are 564 prime records. The actual tail numerators are:

| Prime basis | Cutoff $y$ | $\beta_y$ | $\widehat B_y$ |
|---|---:|---:|---:|
| First 10 primes | 29 | 7,454,749,851 | 0.007454749851 |
| First 11 primes | 31 | 6,414,167,124 | 0.006414167124 |

The unrounded bound improves with a larger integer cutoff. Per-term ceiling effects mean the rounded numerator need not improve monotonically if the sieve cutoff changes. No such monotonicity is promised by the API.

## 3. Conditional tail estimate

The bound needed for an individual CRT class is asymptotic. Define

$$
M_X(S)=\frac1X\sum_{n\le X}\mathbf1_{A_S}(n)(1-U_y(n)).
$$

For a fixed integer $Z\ge y$, split the prime sum at $Z$. The tail is uniformly bounded without conditioning, giving

$$
M_X(S)\le
\sum_{y<p\le Z}\frac1p
\frac{\#\{n\le X:n\in A_S,\ p\mid n\}}X
+\frac1Z.
$$

For each fixed $p>y$, CRT modulo $Qp$ gives

$$
\lim_{X\to\infty}
\frac{\#\{n\le X:n\in A_S,\ p\mid n\}}X
=\frac{\alpha_S}{p}.
$$

First take $\limsup$ in $X$ with $Z$ fixed, then let $Z\to\infty$:

$$
\limsup_{X\to\infty}M_X(S)
\le\alpha_S\sum_{p>y}\frac1{p^2}
\le\alpha_S\widehat B_y.
$$

The unconditioned remainder $1/Z$ vanishes in this order of limits. This argument does **not** assert the bound $\alpha_S\widehat B_y$ for every finite $X$; finite residue-count discrepancies remain.

## 4. Strict distribution with a closed-atom lower bound

Let

$$
H_X(c)=\frac1X\#\{n\le X:\varphi(n)/n<c\},\qquad
F_y^{\le}(c)=\sum_{r_S\le c}\alpha_S.
$$

If $R_y(n)<c$, then $\varphi(n)/n<c$. If $R_y(n)=c>0$, the strict inequality still holds unless $U_y(n)=1$. Such exceptions have no prime factor greater than $y$: they are $y$-smooth. For fixed $m$, their count is at most

$$
\prod_{p\le y}\left(1+\frac{\log X}{\log p}\right)
\le(1+\log_2 X)^m=o(X).
$$

Consequently the whole atom at $r_S=c$ may be included in the limiting lower bound:

$$
F_y^{\le}(c)\le\liminf_{X\to\infty}H_X(c).
$$

For an atom with $r_S>c$, the strict event forces

$$
1-U_y(n)>\frac{r_S-c}{r_S}.
$$

The conditional estimate and the trivial atom-mass bound give

$$
\limsup_{X\to\infty}
\frac{\#\{n\le X:n\in A_S,\ \varphi(n)/n<c\}}X
\le
\alpha_S\min\left(1,\widehat B_y\frac{r_S}{r_S-c}\right).
$$

There are finitely many atoms, so

$$
\boxed{
F_y^{\le}(c)
\le\liminf H_X(c)
\le\limsup H_X(c)
\le
F_y^{\le}(c)+
\sum_{r_S>c}
\alpha_S\min\left(1,\widehat B_y\frac{r_S}{r_S-c}\right).
}
$$

Where the classical distribution limit is used, replace the middle two quantities by $f(c)$. At $c=0$, positivity gives $f(0)=0$. At $c=1$, every positive integer except 1 has $\varphi(n)/n<1$, giving $f(1)=1$. Atoms equal to the threshold enter the lower sum and never enter a zero-denominator tail formula.

## 5. Exact common-denominator implementation

Write an above-threshold atom as $r=u/v$, its weight as $w$, and the threshold as $c=a/b$. Then $g=ub-av>0$. With $\widehat B_y=\beta_y/D$, the exact desired tail contribution is

$$
\frac wQ\min\left(1,\frac{\beta_y ub}{Dg}\right).
$$

Multiplication by $QD$ gives $\min(wD,w\beta_y ub/g)$. Since $wD$ is an integer, an outward integer contribution is exactly

$$
k_S=\min\left(wD,\left\lceil\frac{w\beta_y ub}{ub-av}\right\rceil\right).
$$

There is no additional factor of $D$ in that numerator. The recorded bounds are

$$
L=\frac{W_{\le c}}Q,\qquad
U=\frac{DW_{\le c}+\sum_{r_S>c}k_S}{QD},
\quad
W_{\le c}=\sum_{r_S\le c}w_S.
$$

All comparisons, gcds, products, divisions and ceilings use integers. Each uncapped contribution introduces less than $1/(QD)$ probability rounding. If $k$ atoms lie above the threshold, their total extra rounding is less than $k/(QD)$, separately from the earlier rounding of $\widehat B_y$. Since $k_S\le w_SD$ and $\sum_Sw_S=Q$, the upper bound is at most 1.

For $0\le a<b\le1$, subtracting the pointwise enclosures gives

$$
\max(0,L_b-U_a)
\le f(b)-f(a)
\le\min(1,U_b-L_a).
$$

This is the density of $a\le\varphi(n)/n<b$. It is an interval-mass enclosure, with no derivative or finite-$X$ rate inferred from it.

## 6. API and saved-state use

The module has no imports, file access, network access or process operations. It exports `createTotientDensityIndex`, `openTotientDensityIndex`, `SCHEMA`, the decimal-string `SCALE` and frozen `LIMITS`. The schema is `commons.ppl003.totient_density_index/v1`.

The following is the sequence already performed in the actual consumer:

```js
const {
  createTotientDensityIndex,
  openTotientDensityIndex,
} = require('./totient_density_index.cjs');

const initial = createTotientDensityIndex({
  primeCount: 10,
  sieveLimit: 4096,
});
const initialHalf = initial.bound({numerator: 1n, denominator: 2n});

const extension = openTotientDensityIndex(initial.snapshot());
const added = extension.appendNextPrime(); // adds 31
const refinedHalf = extension.bound({numerator: '1', denominator: '2'});

const fresh = openTotientDensityIndex(extension.snapshot());
const interval = fresh.interval({
  lower: {numerator: 1n, denominator: 2n},
  upper: {numerator: 3n, denominator: 4n},
});
const page = fresh.atomPage({offset: 100, limit: 6});
const recorded = fresh.snapshot();
```


For fresh work from the publication, a caller can load the adjacent JSON and pass its `index` member directly to `openTotientDensityIndex`. That saved state already includes the eleven-prime basis and all three computed point bounds. Reading the JSON alone retrieves all recorded results.

### Construction

`createTotientDensityIndex({primeCount = 10, sieveLimit = 4096})` accepts only these two optional fields. Prime count is an integer from 1 through 15; sieve limit is an integer from 53 through 100,000. The minimum cutoff supplies enough primes for every permitted future append.

The constructor performs one complete sieve, computes the individual outward prime-tail terms and suffix sums, and builds each successive basis from the initial singleton empty-subset atom. All versions are retained. Prime selection is always the first primes in order; this constructor does not accept arbitrary subsets, supplied primality claims or a partial prime list.

### Rational arguments

A threshold is an object with exactly `numerator` and `denominator`. Values are nonnegative BigInts or canonical nonnegative decimal strings, each with at most 128 digits. The denominator must be positive and the ratio must lie in $[0,1]$. Numbers, signs, exponent notation, whitespace and leading zeroes except `'0'` are rejected.

The ratio is reduced with an exact gcd before it forms a cache key. Returned probability fractions are exact but are not promised to be reduced. Numeric masks, counts, offsets and prime bounds are safe integers; probability and ratio components are decimal strings.

### `bound({numerator, denominator})`

The method returns a pointwise density enclosure for the **active** prime basis. Its cache key combines basis count and reduced threshold, such as `11:1/2`. A cached ten-prime bound is not silently substituted for the eleven-prime bound.

On a cache miss, a binary search obtains the closed-atom prefix weight. The method then evaluates each above-threshold conditional contribution and retains every pair `[source_row, scaled_units]`. A zero threshold uses the exact zero endpoint. At one, all atoms enter the prefix and the contribution list is empty.

The returned object contains:

| Field | Meaning |
|---|---|
| `key`, `basis_count`, `cutoff_prime` | Cache/source version and largest basis prime |
| `threshold` | Reduced rational threshold |
| `kind` | `conditional_tail` or `exact_zero_endpoint` |
| `lower`, `upper` | Exact rational density bounds |
| `tail_bound` | The saved $\beta_y/D$ |
| `at_or_below_rows`, `above_rows` | Closed-CDF row boundary and remaining atom count |
| `capped_terms`, `rounded_terms` | Counts from the exact upper-unit evaluation |
| `upper_contributions` | Every above-threshold source row and its integer upper units |

On a cache hit, the saved contribution record is reused. Normalizing a newly supplied rational still involves a gcd; it does not recompute the CDF search or tail contributions.

### `interval({lower, upper})`

Both endpoints use the rational format above, with $0\le\text{lower}<\text{upper}\le1$. The result gives exact lower and upper bounds for the event

`lower <= phi(n)/n < upper`.

The method obtains the two active-basis point bounds through the same cache and subtracts their rational enclosures as proved above. It returns both bound keys. A fresh endpoint is computed once; an already recorded endpoint is reused. The actual final interval reused `11:1/2` and computed only `11:3/4`.

The interval result is an asymptotic density bound. It is not a finite-prefix count, an estimate of a derivative, or a rate of convergence in $X$.

### `atomPage({offset = 0, limit = 16})`

Both fields are optional; unknown fields are rejected. Offset is an integer from zero through the active row count, inclusive. Limit is an integer from 1 through 64. Explicit null values are invalid.

The result returns sorted source rows, total row count and the next offset, or null at the end. Each row includes the zero-based source row, subset mask, selected basis primes, reduced ratio, integer weight, cumulative weight and common probability denominator. An offset equal to the total row count yields an empty terminal page.

Pagination derives the selected-prime display from each row's mask. It does not construct atoms or evaluate pointwise density bounds.

### `appendNextPrime()`

This method accepts no arguments. It adds exactly the next prime from the retained complete table and applies the two-stream construction from Section 1.

It returns the old and new basis sizes, appended prime, old and new row counts and common denominators, plus the number of retained old versions. Existing versions and bound records remain unchanged. Subsequent point queries use the new active version and its saved tail suffix.

The actual append transformed the 1,024 rows for primes through 29 into 2,048 new rows for primes through 31. The old 2,047 cumulative rows, including all earlier versions and the singleton starting version, remained retained. The denominator changed from 6,469,693,230 to 200,560,490,130. This does not enumerate either period.

### Summary and snapshot

`summary()` returns the active basis, period, row counts, number of retained versions, sieve size, bound/contribution/query counts, local operation counters and any imported summary. It marks an index as either `constructed` or `restored_structural_only`.

`snapshot()` returns the complete prime table, every retained basis version, all cached bound records, the query history, limits and summary. Outputs are cloned. The public object is frozen, while its closure owns the active state.

Each new public bound, interval, page or append call reserves a sequential query record. The history is retained across saved opens, including its query-cap usage. Each query records its operation, canonical input, source version and result references. Successful calls have `status: 'complete'`. A failure after reservation retains `status: 'incomplete'` and an error before throwing.

Argument validation and the query-cap check occur before a query record is reserved. Earlier completed state remains available after later failures. A new atom version is installed only after the full merge and cumulative mass check succeed; a new bound is cached only after its contribution evaluation completes. An interval may retain a successfully computed first endpoint if its second endpoint fails.

### Saved-state restoration and provenance

`openTotientDensityIndex(snapshot)` makes a bounded defensive copy of the input, then loads its prime table, atom versions, cached bounds and query history. Subsequent caller mutation of the input or returned records does not alter the index's retained state.

Restoration checks schema/scale, array sizes, ordered prime tokens, version headers, mask uniqueness, positive rational/weight bounds, strict ratio order, increasing cumulative weights and final cumulative denominators. It checks bound keys, contribution row ranges, probability bounds, tail references and supported query headers. Its own sieve, atom-construction, CDF-bound and gcd counters start at zero; source copy counts are recorded separately.

These are structural checks. Restoration does **not** authenticate the source, establish primality/completeness of the supplied prime list, recompute ceiling terms or suffix arithmetic, prove that each subset mask yields its stored ratio and weight, reconstruct cumulative weight sums, or recompute cached density contributions. It does not re-prove the mathematical claim that a saved table was correctly constructed. It also does not certify every historical query result beyond the documented structural checks.

Use a source with established provenance, such as the complete adjacent artifact and its recorded implementation identity. A structurally valid forged table is not made mathematically trustworthy by opening it. Fresh calculations from an imported table inherit that provenance requirement.

## 7. Complete data format

The publication retains one full final index. It contains all source versions needed to follow earlier results, so it does not require repeating three full snapshots of the same tables.

| Top-level record | Contents |
|---|---|
| `operation`, `executed_at`, `source_blob` | Original operation, actual-use timestamp and implementation identity |
| `statement_source` | Exact retrieved formal-source blob and qualified scope |
| `input` | Constructor arguments and subsequent query/append inputs |
| `constructed_summary` | State immediately after the one construction |
| `initial_half`, `refined_half` | Complete point responses, including every upper contribution |
| `first_open_summary`, `second_open_summary` | Fresh local counters and exact copied-source counts |
| `append`, `interval`, `page` | Complete actual results |
| `index` | Complete final snapshot, including every prior atom version and cache record |
| `execution` | Actual call counts and one elapsed-time observation |

In `index.prime_table`, `primes` contains all sieve primes in increasing order. `ceiling_terms[i]` is $\lceil D/p_i^2\rceil$. `suffix_units[m]` is the tail numerator for a basis of the first $m$ primes; the last suffix is $\lceil D/z\rceil$.

In `index.versions`, the array index equals the basis count. Version zero is the singleton empty-prime starting state. Every row has exactly five columns:

```text
[subset_mask, ratio_numerator, ratio_denominator, integer_weight, cumulative_weight]
```


All except the mask are decimal strings. The version's `denominator` is the common $Q$. The mask bit at position $i$ selects prime $p_i$. Source row order is strictly increasing rational ratio.

In `index.bounds`, `lower_weight` is $W_{\le c}$, `upper_scaled_weight` is $DW_{\le c}+\sum k_S$, and `tail_scaled` is $\beta_y$. Each `upper_contributions` row is `[atom_row, scaled_units]`. Its basis count identifies the correct source atom table, including older versions. The entire numerator can therefore be interpreted directly from the published records and the proved formula.

## 8. Actual results

The three cached point records are:

| Bound key | At/below atoms | Above atoms | Capped terms | Rounded terms |
|---|---:|---:|---:|---:|
| `10:1/2` | 693 | 331 | 5 | 301 |
| `11:1/2` | 1,405 | 643 | 8 | 603 |
| `11:3/4` | 1,907 | 141 | 6 | 114 |

The complete first and refined half-threshold bounds are:

$$
\frac{3300708170}{6469693230}
\le f(1/2)\le
\frac{3404205514831811218600}{6469693230000000000000}
\qquad(m=10),
$$

$$
\frac{102348867954}{200560490130}
\le f(1/2)\le
\frac{105158068832643563974579}{200560490130000000000000}
\qquad(m=11).
$$

Their outward decimal displays are:

| Basis | Lower display | Upper display |
|---|---:|---:|
| First 10 primes | 0.5101800120 | 0.5261772690 |
| First 11 primes | 0.5103142093 | 0.5243209606 |

The interval result uses denominator $200560490130000000000000$ and exact lower/upper numerators

$$
32686161393356436025421,\qquad
39144396639147637418940.
$$

The final page returned source rows 100–105 with next offset 106.

### Work performed and reused

| Actual phase | Sieve runs | New atom rows | New point bounds | Upper terms evaluated | Bound cache hits | Source atom rows copied |
|---|---:|---:|---:|---:|---:|---:|
| Construct through 29 and query $1/2$ | 1 | 2,047 | 1 | 331 | 0 | 0 |
| Open, append 31 and query $1/2$ | 0 | 2,048 | 1 | 643 | 0 | 2,047 |
| Open, query interval and page | 0 | 0 | 1 | 141 | 1 | 4,095 |

The first phase retains versions zero through ten; the append supplies version eleven. There are 12 versions, 4,095 total atom rows, 3 cached point bounds, 1,115 contribution rows and 5 query records. The active basis contains 2,048 atoms.

The complete sieve made 6,531 marking visits and retained 564 prime-tail terms. The initial ordered constructions used 2,036 comparisons; the one append used 2,047 comparisons. The final fresh reader performed no sieve, atom generation, merge or prefix-weight accumulation. It used 11 CDF comparisons for the new three-quarter threshold and five gcd steps to normalize its two rational endpoints.

Across the entire actual use, integer totients evaluated and primorial residues enumerated were both zero. Accepted source computations were not replayed. The full CommonJS source was evaluated in the connected JavaScript environment; no native executor or substitute donor was requested.

The elapsed observation was **45 ms** for this one actual consumer. It is not a benchmark series, throughput guarantee or timing claim about another runtime.

## 9. Caps, complexity and limitations

| Item | Bound |
|---|---:|
| Basis primes | 1–15 |
| Sieve cutoff | 53–100,000 |
| Retained sieve prime records | 10,000 |
| Atoms in one basis | 32,768 |
| Atom rows across all retained versions | 65,535 |
| Retained public query records, including imported history | 32 |
| Cached point-bound records | 64 |
| Retained upper-contribution rows | 131,072 |
| Rows per atom page | 64 |
| Digits in each validated decimal component | 128 |
| Visited snapshot values during defensive copying | 1,500,000 |
| Snapshot nesting depth | 24 |
| Total snapshot string/key characters | 32,000,000 |

The fixed $D=10^{12}$ is part of the schema and is not a tuning parameter. Sieve work is bounded by its explicit cutoff. Atom storage and construction grow as $2^m$; retaining all versions uses $2^{m+1}-1$ rows. A prime append creates and merges two ordered streams in linear row work. A new point bound uses a logarithmic CDF search and one pass over the above-threshold atoms. Saved cache hits avoid that search and pass. BigInt operand costs remain relevant; these descriptions do not promise constant-time arithmetic.

The conditional Markov bound can be loose, especially for ratios just above the threshold, where terms reach their full atom-mass cap. More precise point enclosures would require additional mathematical or computational work; this implementation does not turn its fixed finite basis into a derivative conclusion or an arbitrary precision guarantee.

Only the specified construction, two saved opens, one append, two explicit point queries, interval and page were executed. The source's other valid inputs, zero/one endpoints, invalid/malformed inputs, cap failures and error branches were inspected in source only. No separate tests, fixtures, source-calculation replay, finite-prefix scan or formal proof execution was added.

## Provenance and delivery scope

| Item | Identity |
|---|---|
| Operation | `ERDOS50-TOTIENT-DENSITY-20261004-7CA6` |
| Actual module Git blob | `3969a8d6f92c53e05c4b42cfbfebb7f4be61f810` |
| Complete data Git blob | `e056035b46910fc37911418ed12ca622329ccecd` |
| Retrieved formal statement Git blob | `bc1ea50a170839b20f3c8b69ea4dc94180c22d3e` |
| Actual execution | 2026-10-04 17:09:52.352 UTC |

The module and actual data remained unchanged after the consumer. The JSON formatting places primitive rows on individual lines while preserving the complete recorded object. Independent reasoning review checked the conditional limit, closed-atom endpoint treatment, integer/probability weight distinction and exact $D$ cancellation; it did not rerun the calculation.

[Original claim in the long-tail source thread](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1791133410709209).
