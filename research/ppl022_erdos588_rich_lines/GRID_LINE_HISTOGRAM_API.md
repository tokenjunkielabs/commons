# Exact grid-line histograms without point enumeration

## Delivered result

[grid_line_histogram.cjs](grid_line_histogram.cjs) computes the complete line-multiplicity histogram of
$$
G_{k,d}=\{0,\ldots,k-1\}^d
$$
from integer formulas. It counts unoriented primitive-step segments by Möbius inversion and obtains whole-line counts by second differences. It does not enumerate grid points, point pairs, individual lines or projected coordinates.

The actual new input is $k=5$, $d=12$, with
$$
n=5^{12}=244140625.
$$

Its complete nonzero histogram is:

| Points on a line $\ell$ | Exact number $t_\ell$ |
|---:|---:|
| 2 | 29,767,389,101,298,792 |
| 3 | 11,366,735,095,072 |
| 4 | 127,495,551,352 |
| 5 | 6,798,573,288 |

There are **29,778,890,130,518,504** determined lines in total and no line contains more than five grid points. The exact pair accounting is
$$
t_2+3t_3+6t_4+10t_5
=29802322265625000
={244140625\choose2}.
$$

The previously established finite integer-projection theorem carries this incidence pattern to the plane, giving the finite lower bound
$$
f_5(244140625)\ge6798573288.
$$

The result is an exact aggregate calculation. It does not provide an enumeration of those individual points or lines. [grid5_dim12_histogram.json](grid5_dim12_histogram.json) retains the complete request, all counts, Möbius coefficients, power basis, all eight contribution terms and execution evidence.

## Published attribution

Pentti Haukkanen and Jorma K. Merikoski's [*Some formulas for numbers of line segments and lines in a rectangular grid*](https://arxiv.org/pdf/1108.1041), Ars Combinatoria 104 (2012), [publisher version](https://combinatorialpress.com/article/ars/Volume%20104/volume-104-paper-30.pdf), already gives gcd-weighted segment counts in general rectangular dimensions. Theorem 1 divides by two for reversal; Corollaries 1–2 recover cumulative and exact line counts by differences. The paper credits Mustonen's planar precursors. These are prior identities, with no formula-priority claim here.

This implementation evaluates them through a factorized Möbius sum, caches the shared integer powers and retains a complete new consumer. Its dimension-one endpoint is stated separately.

The planar interpretation uses the finite projection theorem documented in [INTEGER_PLANE_PROJECTION_API.md](INTEGER_PLANE_PROJECTION_API.md), released in [Commons #31247](https://github.com/woahwhattheheck/commons/pull/31247). That guide preserves the prior Solymosi–Stojaković generic-projection attribution. The original extremal $P_k$ convention is Erdős's Problem 36 in [*Research problems* (1984)](https://www.renyi.hu/~p_erdos/1984-18.pdf).

## Segment conventions

The side length $k$, ambient dimension $d$ and segment length $\ell$ are separate parameters. A primitive integer vector $v\ne0$ satisfies
$$
\gcd(|v_1|,\ldots,|v_d|)=1.
$$

Zero coordinates are allowed; the all-zero vector is excluded. An $\ell$-point consecutive segment consists of
$$
x,\ x+v,\ \ldots,\ x+(\ell-1)v
$$
inside the grid, where $\ell\ge2$. Its two orientations describe the same segment.

Let $A_\ell$ count these **unoriented** segments. For fixed signed primitive $v$, the endpoint constraints give
$$
\prod_{i=1}^d\bigl(k-(\ell-1)|v_i|\bigr)_+
$$
starting points. Summing over both signs counts each segment twice. Thus the module retains the oriented numerator separately and divides it by two to produce $A_\ell$.

A line's grid points occur at consecutive primitive integer steps because the grid is the set of integer points in a convex box. A maximal $m$-point line contributes $\max(m-\ell+1,0)$ segments. Consequently,
$$
T_\ell=A_\ell-A_{\ell+1},\qquad
t_\ell=A_\ell-2A_{\ell+1}+A_{\ell+2}.
$$

Here $T_\ell$ counts lines with at least $\ell$ points and $t_\ell$ counts lines with exactly $\ell$ points. Every line contains at most $k$ points, so $A_\ell=0$ for $\ell>k$.

## Factorizing the primitive-direction count

For positive integers $a$, define
$$
M=\left\lfloor\frac{k-1}{a}\right\rfloor,\qquad
S(k,a)=k+2kM-aM(M+1).
$$

This is the elementary one-coordinate sum
$$
S(k,a)=\sum_{u=-M}^M(k-a|u|).
$$

The range uses $k-1$, so every included coordinate weight is positive. The $u=0$ contribution is $k$.

Let $\mu$ be the ordinary number-theoretic Möbius function: $\mu(1)=1$, a number divisible by a square has value zero, and a product of $r$ distinct primes has value $(-1)^r$. The identity
$$
\sum_{g\mid h}\mu(g)=
\begin{cases}
1,&h=1,\\
0,&h>1
\end{cases}
$$
isolates primitive nonzero direction vectors.

If all direction coordinates are divisible by $g$, write $v=gu$. For an $\ell$-point segment, put $a=(\ell-1)g$. Coordinate independence factors the unrestricted weighted direction sum as $S(k,a)^d$. The forbidden all-zero direction contributes exactly $k^d$, and must be subtracted before applying the gcd identity.

Every nonzero direction has a nonzero coordinate, which bounds its common divisor by $\lfloor(k-1)/(\ell-1)\rfloor$. Therefore
$$
A_\ell=
\frac12
\sum_{g=1}^{\left\lfloor(k-1)/(\ell-1)\right\rfloor}
\mu(g)\left(S\bigl(k,(\ell-1)g\bigr)^d-k^d\right),
\qquad 2\le\ell\le k.
$$

This is a finite sum of integers. The signed terms can have either sign, but their total is a nonnegative even oriented count. The module enforces those two conditions before division by two.

Subtracting $k^d$ only once after the whole sum would be incorrect: the zero direction occurs in every unrestricted gcd-divisor summand. The retained step-basis records make this exclusion explicit.

## Complete pair accounting

Every unordered pair of distinct grid points has a unique primitive direction and a unique number of primitive steps between its endpoints. It is therefore the endpoint pair of exactly one segment counted among $A_2,\ldots,A_k$. Hence
$$
\sum_{\ell=2}^k A_\ell={k^d\choose2}.
$$

The corresponding whole-line accounting is
$$
\sum_{\ell=2}^k{\ell\choose2}t_\ell={k^d\choose2}.
$$

The API checks both equalities exactly. They are aggregate identities, without enumerating the pairs themselves. The complete histogram also supplies all cumulative counts, the number of determined lines and total point-line incidences.

For $d=1$, the grid consists of one $k$-point line. The same formulas have $A_\ell=k-\ell+1$ for $2\le\ell\le k$, with $t_k=1$ and all lower exact line counts zero. This endpoint is included in the public contract. Side length one, dimension zero and empty grids are outside it.

## The $k=5$ family and the actual powers

For side length five, the only Möbius coefficients needed are
$$
\mu(1)=1,\quad\mu(2)=-1,\quad\mu(3)=-1,\quad\mu(4)=0.
$$

The coordinate sums are $S(5,1)=25$, $S(5,2)=13$, $S(5,3)=9$ and $S(5,4)=7$. Substitution and the second differences give
$$
\begin{aligned}
t_2&=(25^d-3\cdot13^d+2\cdot7^d)/2,\\
t_3&=(13^d-2\cdot9^d+5^d)/2,\\
t_4&=(9^d-2\cdot7^d+5^d)/2,\\
t_5&=(7^d-5^d)/2.
\end{aligned}
$$

These are symbolic simplifications of the general formula, not additional grid computations. The actual $d=12$ call used exactly the following shared powers:

| Base $b$ | $b^{12}$ |
|---:|---:|
| 5 | 244,140,625 |
| 7 | 13,841,287,201 |
| 9 | 282,429,536,481 |
| 13 | 23,298,085,122,481 |
| 25 | 59,604,644,775,390,625 |

The last value was obtained by squaring the point count. Four bounded exponentiations supply the other bases. Repeated step scales reuse these saved values.

The actual unoriented segment counts are
$$
\begin{aligned}
A_2&=29790532252436144,\\
A_3&=11642121917640,\\
A_4&=141092697928,\\
A_5&=6798573288,\qquad A_6=A_7=0.
\end{aligned}
$$

All eight divisor-sum records are retained, including the zero term at $g=4$. Seven terms contribute nonzero values.

## Public API

The module exports `countGridLineHistogram` and the immutable `GRID_HISTOGRAM_LIMITS` object. It uses CommonJS syntax, with no imports or I/O, and runs in connected V8.

```javascript
const result = countGridLineHistogram({
  side_length: 5,
  dimension: 12,
  include_terms: true
});
```

The two size parameters must be safe integer Numbers in the supported ranges. Strings and BigInt size parameters are not accepted. All potentially large counts and powers are returned as canonical decimal strings; callers should use BigInt if they need further exact arithmetic.

The optional `include_terms` flag defaults to false and must be boolean when provided. Every result always contains the complete histogram, segment counts, Möbius table and shared power basis. With `include_terms: true`, it additionally retains every considered divisor term, including zero coefficients.

| Field | Meaning |
|---|---|
| `point_count`, `maximum_collinearity` | $k^d$ and the exact maximum $k$. |
| `histogram` | Every multiplicity 2 through $k$, including zero rows, with exact and cumulative line counts. |
| `determined_line_count`, `point_line_incidences` | Complete aggregate line and incidence totals. |
| `segment_counts` | Oriented numerators and unoriented $A_\ell$, including the zero endpoints $k+1,k+2$. |
| `mobius_table` | Every coefficient through $k-1$, with its least-prime-divisor record. |
| `power_values` | Each shared integer base and its exact power; the point-count square is identified. |
| `step_basis` | $a$, $M$, $S(k,a)$, its power, and the excluded zero-direction weight. |
| `mobius_terms` | Complete signed contribution records when requested, otherwise null. |
| `accounting` | Both exact pair-accounting sums and $\binom{k^d}{2}$. |
| `finite_planar_interpretation` | The projection-theorem interpretation and, for $k\ge4$, a finite Erdős lower bound. |
| `limits`, `work` | The actual bounds and operation counters. |

There are no point IDs or individual line records in this interface. It provides aggregate counts derived from the stated complete grid, rather than incidence records for a materialized point list.

## Bounds and computational cost

| Bound | Value |
|---|---:|
| Side length | 2 through 1,024 |
| Dimension | 1 through 4,096 |
| Decimal digits in any retained integer power | 512 |
| Optional retained divisor-term records | 8,192 |

The input must also satisfy
$$
(k^2)^d\le10^{512}-1.
$$

The numeric parameter bounds alone do not guarantee this power bound. Out-of-contract inputs raise an error without returning a partial histogram.

Binary exponentiation uses checked BigInt multiplication. Since $S(k,1)=k^2$ is the largest coordinate-sum base, the squared point count bounds every required power. Products are checked by division before multiplication, so a larger power is not constructed merely to detect overflow.

The 512-digit rule concerns powers and returned counts. Signed intermediate sums may be slightly longer: each is a sum of at most $k-1$ terms of magnitude at most $10^{512}-1$. BigInt retains these intermediates exactly. There is no floating-point cancellation.

A linear sieve computes the Möbius coefficients. The number of divisor terms is
$$
\sum_{r=1}^{k-1}\left\lfloor\frac{k-1}{r}\right\rfloor=O(k\log k).
$$

Only $k-1$ distinct step scales occur. Their shared powers are cached; each power uses $O(\log d)$ bounded multiplications. The arithmetic-operation count is therefore $O(k\log k+k\log d)$, in addition to bounded sorting/output work. The integer cost depends on the digit cap. No factor proportional to $k^d$ or $\binom{k^d}{2}$ enters the enumeration loops.

The actual consumer used four exponentiations, eight exponentiation multiplications, twelve squarings and one point-count square. It considered eight divisor terms, with three step-basis cache hits. Every geometric-enumeration counter is zero. Its single-run timing is retained without a comparative benchmark claim.

## Planar interpretation and reuse

The complete grid has no line longer than five. Applying the already proved finite projection theorem with span $D=4$ gives base $t=33$ and the mathematical map
$$
(x_0,\ldots,x_{11})\longmapsto
\left(\sum_{i=0}^{11}x_i33^i,\;
      \sum_{i=0}^{11}x_i33^{12i}\right).
$$

This formula defines an integer planar configuration with the same complete histogram, proving the stated finite lower bound. The histogram consumer did not execute that projection or generate the 244,140,625 images.

The earlier projection module accepts dimensions only through eight and has its own output-digit bound. Those limits were not changed or bypassed. The algebraic finite projection theorem applies to arbitrary finite dimensions; its proof, rather than an out-of-contract API call, supplies this interpretation.

After loading the module text as `moduleText`, a connected V8 caller can evaluate a supported new input directly:

```javascript
const m = { exports: {} };
new Function("module", "exports", moduleText)(m, m.exports);

const histogram = m.exports.countGridLineHistogram({
  side_length: k,
  dimension: d,
  include_terms: true
});
```

To consume the completed result without repeating it, parse `grid5_dim12_histogram.json` and read its `result.histogram`, `result.power_values` and `result.mobius_terms`. All arithmetic inputs and contributions are already explicit there.

The computation establishes these exact finite aggregate counts and a finite planar lower bound. It makes no extremal equality, novelty, external-frontier or conjecture-resolution claim. Earlier accepted cube, host, subset and projection computations were not rerun.
