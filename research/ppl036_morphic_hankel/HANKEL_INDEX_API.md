# An exact Hankel index covering every shift

## Result and scope

For the fixed point $a=a_0a_1a_2\cdots$ of

$$
\mu(1)=12,\qquad \mu(2)=23,\qquad \mu(3)=14,\qquad \mu(4)=32,
$$

define

$$
H_n(k)=\det(a_{k+i+j})_{0\le i,j<n}.
$$

The complete retained calculation establishes

$$
\boxed{H_n(k)\ne0\quad\text{for every }k\ge0\text{ and }1\le n\le32.}
$$

The bound applies to matrix order. Every nonnegative starting position is covered
by the finite-language argument below. No conclusion for all orders is asserted.

The calculation has 6,949 records, one for each distinct factor at each of the
32 orders. Its 434 factors of length 63 represent the complete factor language
at that length. The accompanying data retains every determinant, its minor
references, the factor coverage and concrete occurrence witnesses.

| Matrix order | Factor length | Distinct factors | Positive | Negative | Zero |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 4 | 4 | 0 | 0 |
| 2 | 3 | 15 | 8 | 7 | 0 |
| 4 | 7 | 42 | 20 | 22 | 0 |
| 8 | 15 | 98 | 58 | 40 | 0 |
| 16 | 31 | 210 | 133 | 77 | 0 |
| 32 | 63 | 434 | 265 | 169 | 0 |

The sign counts count factors. They are not counts or frequencies of their
infinitely many occurrences.

After compilation, the same index answered an order-32 query at shift $10^{100}$:

$$
H_{32}(10^{100})=45\,168\,038\,832\,870.
$$

The result references factor row 22. The number of determinant evaluations
remained 6,949 before and after the query. Eight factor records were also paged
from the same table.

## Statement, provenance and limits

Jeffrey Shallit's 2014 *Open Problems in Automata Theory: An Idiosyncratic View*,
slides 32–35, defines shifted Hankel determinants and asks the nonvanishing
question for this exact morphism as Problem 9. The slide reports a check through
prefix length 800. That historical report does not supply the complete
all-shift factor catalogue used here.

- [Primary problem slides](https://cs.uwaterloo.ca/~shallit/Talks/bc4.pdf)
- [Author's talks and problem updates](https://cs.uwaterloo.ca/~shallit/talks.html)
- W. F. Lunnon, [*The Number-Wall Algorithm: an LFSR Cookbook*](https://cs.uwaterloo.ca/journals/JIS/VOL4/LUNNON/numbwall10.pdf),
  *Journal of Integer Sequences* 4 (2001), Article 01.1.1, especially §3.

The determinant identity is classical. Lunnon provides background on number
walls, determinant recurrences and zero windows. This guide gives the precise
Hankel indexing and finite-language proof used by the implementation.

The author's current updates distinguish the related real-alphabet Problem 8
from integer-alphabet variants. The present calculation concerns exactly the
four integer symbols displayed above. A bounded literature search supplied no
exact solution or prior all-shift bound for this morphism; that is not a
comprehensive priority assessment. This artifact makes no novelty, current prize,
eligibility or sponsor-acceptance claim.

## Why finitely many factors cover every shift

### Fixed point, letters and direct navigation

The words $\mu^j(1)$ are nested prefixes because $\mu(1)$ starts with $1$.
Their lengths tend to infinity, so they define a one-sided infinite fixed point
$a=\mu(a)$, indexed from zero. The fixed-point equation gives

$$
a_{2t+d}=\mu(a_t)[d]\qquad(t\ge0,\ d\in\{0,1\}),
$$

where position $d$ is zero-based within a two-letter image.

To determine $a_k$, start in state $1$ and read the binary digits of $k$ from
most significant to least significant. A digit $d$ replaces the current letter
$c$ by $\mu(c)[d]$. Leading zero digits are harmless because $\mu(1)[0]=1$.
This evaluates a position without constructing the prefix preceding it.

The occurring letters form the least set containing $1$ and closed under taking
letters of their images. Every newly reached letter has an occurrence witness:
from $a_t=c$, the two image letters occur at $2t$ and $2t+1$. Conversely, binary
navigation reaches every position, so this closure omits no occurring letter.
The data retains the four reached letters and the parent/digit of each witness.

### Exact adjacent-pair closure

Start with the internal pair $\mu(c)$ for every reachable letter $c$. Repeatedly
apply the boundary rule

$$
cd\longmapsto \operatorname{last}(\mu(c))\operatorname{first}(\mu(d)).
$$

The least resulting set is exactly the adjacent-pair language of $a$.

For soundness, an internal pair produced from a witnessed letter at $t$ occurs
at $2t$. A boundary pair produced from a witnessed pair at $t$ occurs at $2t+1$.
Every inserted pair therefore occurs.

For completeness, a pair starting at an even position $2t$ is internal to
$\mu(a_t)$. A pair starting at $2t+1$ is the boundary image of $a_ta_{t+1}$.
Repeating the odd-position reduction strictly decreases the position until an
internal pair is reached. The closure therefore contains every actual pair.

The actual closure contains the following nine pairs. Indices are the retained
pair indices; positions are proved occurrences, with no earliest-position claim.

| Pair index | Pair | Known occurrence | Source of witness |
|---:|:---:|---:|---|
| 0 | 12 | 0 | inside μ(1) |
| 1 | 23 | 2 | inside μ(2) |
| 2 | 14 | 6 | inside μ(3) |
| 3 | 32 | 14 | inside μ(4) |
| 4 | 22 | 1 | boundary image of 12 |
| 5 | 31 | 5 | boundary image of 23 |
| 6 | 42 | 29 | boundary image of 32 |
| 7 | 41 | 11 | boundary image of 31 |
| 8 | 21 | 23 | boundary image of 41 |

Every pair's boundary image was processed once. The full witness records remain
in the data, including source-pair indices for boundary insertions.

### Two-block coverage

Fix a requested maximum order $N\ge1$, set $L=2N-1$, and choose $B=2^q$ with
$B\ge L-1$. The word $a=\mu^q(a)$ is partitioned into blocks
$\mu^q(a_t)$ of length $B$.

A length-$L$ factor starts at some $k=Bt+r$, where $0\le r<B$. It fits within
two consecutive blocks because

$$
r+L\le B-1+L\le2B.
$$

It is consequently a window of $\mu^q(a_ta_{t+1})$, and the pair $a_ta_{t+1}$
belongs to the complete adjacent-pair set.

Enumerating every length-$L$ window of $\mu^q(cd)$ for every allowed pair $cd$
therefore covers every length-$L$ factor. Conversely, if $cd$ is witnessed at
position $t$, a window at offset $r$ is witnessed at position $Bt+r$. Thus no
enumerated factor is spurious. Deduplication may retain one such occurrence;
it does not establish an earliest occurrence.

For $N=32$, the implementation uses $L=63$, $q=6$ and $B=64$. Each expanded pair
has length 128. Its 66 possible windows, at offsets 0 through 65, yield
$9\cdot66=594$ candidates and 434 distinct factors. The extra offsets beyond
$B-1$ still lie inside the expanded pair and are valid occurrences.

The data retains all four length-64 letter expansions, all 434 distinct factors
and the complete map from each expanded pair's offsets to factor indices.
This map records the full candidate coverage, including duplicates.

### Every smaller factor is a prefix of a carrier

Every occurrence of a shorter factor extends rightwards to length $L$, because
$a$ is infinite. Therefore every factor of length at most $L$ is a prefix of
some member of the complete length-$L$ catalogue. Every such prefix is also
an actual factor.

For each order $n\le N$, the implementation deduplicates and sorts prefixes of
length $2n-1$. These are exactly the factors needed for all values $H_n(k)$.
The word “carrier” in the data means one of the retained maximum-length factors
from which such a prefix is recovered. It introduces no assumption of periodicity,
recurrence or a sufficiently long sampled prefix.

## Exact determinant evaluation

Use the empty determinant convention $H_0(k)=1$. For $n\ge2$ the
Desnanot–Jacobi identity in this indexing is

$$
H_n(k)H_{n-2}(k+2)
=
H_{n-1}(k)H_{n-1}(k+2)-H_{n-1}(k+1)^2.
$$

One derivation takes the central $(n-2)\times(n-2)$ matrix of the order-$n$
Hankel matrix. When that central matrix is invertible, take its $2\times2$
Schur complement. The full determinant is the central determinant multiplied
by the determinant of this complement. The two principal minors correspond
to its diagonal entries. The two off-diagonal minors have cancelling signs
in their product; symmetry makes them equal. This yields the displayed square.
For $n=2$, the central matrix is empty and its determinant is 1.

The implementation begins with $H_1(k)=a_k$. In an order-$n$ factor of length
$2n-1$, the three order-$(n-1)$ minors use factor offsets 0, 1 and 2. The central
order-$(n-2)$ minor starts at offset 2. All of these factors belong to the already
completed smaller-factor languages.

Rows are completed in increasing order. If a row contains zero, the entire row
is retained and construction stops before beginning the next order. Thus every
denominator used is from an earlier nonzero row, or is the empty determinant 1.
This program does not cross a zero denominator.

All arithmetic uses BigInt. For orders at least 3, the numerator must have zero
remainder on division by the central determinant. The quotient is then retained
as a canonical decimal string. Internal BigInt values are also retained during
compilation, so smaller determinants do not need repeated decimal parsing.

Induction on order now proves the meaning of each stored value. The order-one
entries are the actual letters; the identity determines every subsequent entry
from proved smaller minors and a nonzero denominator. Complete factor coverage
then transfers each completed row to every nonnegative shift.

A zero in a completed row would be a counterexample at its retained occurrence.
It would have the smallest possible matrix order because all earlier rows were
complete and nonzero. Its recorded occurrence need not be the smallest shift.
An incomplete row has no complete-order conclusion.

## API contract

The module uses built-in JavaScript and BigInt, with CommonJS exports:

```javascript
const {createMorphicHankelIndex, MORPHISM, LIMITS, SCHEMA} =
  require('./morphic_hankel_index.cjs');

// These are the call shapes of the retained actual consumer.
const index = createMorphicHankelIndex({maxOrder: 32});
const answer = index.at({shift: 10n ** 100n, order: 32});
const page = index.factorPage({order: 32, offset: 0, limit: 8});
const fullRecord = index.snapshot();
```

The actual calls above have already been performed once for this delivery.
The complete saved result can be read directly:

```javascript
const recorded = require('./order32_all_shifts.json');
const answer = recorded.actual_large_shift_result;
const completeIndex = recorded.index;
const order32 = completeIndex.orders.find(row => row.order === 32);
```

Reading that JSON does not run the constructor or recompute a determinant.

### Construction

`createMorphicHankelIndex({maxOrder})` accepts exactly that field.
`maxOrder` must be a safe integer Number from 1 through 64. The morphism,
seed and integer symbol values are fixed; custom morphisms and encodings are
outside this API.

Construction first produces the complete maximum-factor language. It then
builds the determinant rows in ascending order. The returned object exposes
these outcomes through `summary()`:

| Status | Meaning |
|---|---|
| `complete` | Every requested order is complete and nonzero at every shift. |
| `counterexample_found` | A complete row contains a zero. It is the first such order; later orders were not begun. |
| `incomplete` | A resource cap or construction error stopped the work. Only rows explicitly marked complete support whole-order conclusions. |

The result distinguishes `completed_through_order` from
`all_shifts_nonzero_through_order`. These differ if the last completed order
contains zero. A partial row may retain individual evaluated entries, but its
planned factor count does not make it complete.

Invalid constructor input throws before construction. A construction error is
retained as `retained_error` with a stopping record. Previously completed
orders remain readable.

### Direct lookup

`index.at({shift, order})` evaluates the factor at the requested shift using
the four-state binary output automaton, then returns its existing determinant
row. It performs no determinant arithmetic.

- `shift` is a nonnegative BigInt or a canonical decimal string. String zero
  is allowed; signs, leading zeroes, whitespace, exponent notation and Number
  inputs are rejected. The decimal representation is limited to 1,024 digits.
- `order` must name a complete order in this index.
- The result includes the exact factor, its row index, a decimal determinant,
  the requested shift and `reused_determinant: true`.
- Positions and determinant values remain strings in returned records.
- Each lookup reserves a retained query record. A later lookup failure marks
  that record incomplete and retains its error; input validation failures occur
  before reservation.

For the actual query, the factor is

```text
122323142314123223141232122314232314123212231423122323141232231
```

and its determinant is `45168038832870`. All 63 symbols were evaluated at
their requested positions using 20,979 binary transitions.

The mathematical all-shift conclusion is independent of the API's input-digit
cap. The cap bounds the concrete representation accepted by a call.

### Factor pages and summaries

`index.factorPage({order, offset, limit})` pages the distinct factors for a
complete order in lexicographic order. The default offset is 0; the default
limit is 16. Offset may equal the factor count, producing an empty final page.
Limit must be from 1 through 64. Supplied null bounds are rejected.

Each row returns its full factor, determinant, minor references and an occurrence
witness. The page includes total factor count and a nullable next offset. The
witness refers to a catalogue occurrence, not to an earliest-occurrence search.
Pagination reserves a query record but does not recompute determinants.

`index.summary()` returns copied status, complete-order bounds, sign counts
and statistics. Reading it does not reserve a query.

`index.firstZero()` scans retained complete rows. It returns a concrete
witness at the smallest zero order, or `none_in_completed_orders` with its
explicit order bound. It does not evaluate another matrix.

`index.snapshot()` returns the complete copied JSON representation, including
partial construction records if present. Returned data cannot mutate the
index's internal tables. No snapshot restoration/import function is exposed:
a live constructed index reuses its internal table, and the published JSON
provides direct access to this already computed result.

### Fixed resource limits

| Resource | Limit |
|---|---:|
| Requested matrix order | 1–64 |
| Maximum-factor carriers | 4,096 |
| Total retained determinant rows | 32,768 |
| Decimal digits in a lookup shift | 1,024 |
| Returned factors per page | 1–64 |
| Retained lookup/page queries | 32 |

A determinant-row cap is checked before starting the next order. Reaching it
returns an incomplete index with prior complete rows. Reaching a query cap
throws without discarding prior queries. There is no continuation, automatic
restart, silent widening or zero-denominator fallback.

All modes use the same fixed four-letter integer sequence. The actual execution
in this delivery used order 32, one large-shift lookup and one factor page.
Other orders and invalid-input, cap and zero-stopping paths received source
inspection only; no separate suite or accepted calculation was replayed.

## Retained data format

`order32_all_shifts.json` contains operation and source identity, the
actual input and timestamp, the compiler summary before queries, both returned
query results and the complete index snapshot.

The source blob used for the actual calculation is
`fe1e7493dfe37606d0bf4c1a7ba643cb02dbeb70`.
Its code is shipped unchanged in this delivery.

Within `index.language`:

- `reachable_letters` records the binary-position witness derivations.
- `adjacent_pairs` records the internal or boundary origin of every pair.
- `letter_expansions` stores all four images at the chosen substitution depth.
- `carriers` contains the lexicographically sorted maximum-length factors.
- `pair_coverage` gives each expanded pair's full array of carrier indices;
  array position is its window offset.

Each carrier is a compact four-column array:

| Column | Field | Meaning |
|---:|---|---|
| 0 | factor | Complete maximum-length word over the literal digits 1–4 |
| 1 | known_shift | Decimal position of a proved occurrence |
| 2 | pair_index | Index in the adjacent-pair table |
| 3 | offset | Offset in that pair's expanded image |

For an order $n$, `index.orders[n-1]` contains its completion flag, summary
and lexicographically ordered determinant rows. Each row has six columns:

| Column | Field | Meaning |
|---:|---|---|
| 0 | carrier | Factor is this carrier's prefix of length $2n-1$ |
| 1 | determinant | Exact signed decimal integer |
| 2 | left | Order-$(n-1)$ row at factor offset 0 |
| 3 | center | Order-$(n-1)$ row at factor offset 1 |
| 4 | right | Order-$(n-1)$ row at factor offset 2 |
| 5 | inner | Order-$(n-2)$ row at factor offset 2 |

The four minor columns are null at order 1. At order 2, the inner reference is
$-1$, denoting the empty determinant 1. At larger orders, every reference is a
row index in the indicated earlier order. These references record the exact
dependency graph of the integer computation.

The factor is fully recoverable from its carrier; no factor text is omitted by
the compact representation. The data is formatted with one primitive array per
line to keep the complete records manageable. It contains no digest-only
replacement for the determinant table.

## Actual work and computational cost

The one actual consumer ran at **2026-10-04 16:13:56.302 UTC**.

| Recorded operation | Count |
|---|---:|
| Compiler invocations | 1 |
| Complete adjacent pairs | 9 |
| Expanded-pair window candidates | 594 |
| Distinct length-63 factors | 434 |
| Prefix candidates across 32 orders | 13,888 |
| Complete determinant rows | 6,949 |
| Order-one values | 4 |
| Condensation steps | 6,945 |
| Integer products in condensation | 13,890 |
| Exact division checks and quotient divisions | 6,930 each |
| Large-shift lookups | 1 |
| Factor pages | 1 |
| Determinant recomputations during queries | 0 |

The full compiler plus two queries had one observed elapsed time of 24 ms in
the available JavaScript runtime. This is a single observation, without a
benchmark series or throughput guarantee. No native process, network request,
external numerical package, floating determinant or root approximation was
used for the mathematics.

Let $D$ be the total number of factor records across completed orders. After
the factor languages are formed, each non-base determinant takes two integer
products and, after order 2, an exact quotient. This is linear in $D$ arithmetic
operations; integer bit costs and factor-string processing still grow with
order. The implementation retains BigInt values during construction and uses
table lookup during navigation.

The conclusion has two boundaries: every shift is covered, and matrix order is
bounded by 32 in the actual data. Neither a successful large-index query nor
the complete finite catalogue establishes nonvanishing for arbitrarily large
matrix order.

## Delivery identity

Operation: `MORPHIC-HANKEL-ALLSHIFTS-20261004-7CA6`.

[Original scope claim](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1791130082676129).

The NFA length-universality, Beatty, Pierce and other completed research
directories retain their own sources, computations and operation identities.
