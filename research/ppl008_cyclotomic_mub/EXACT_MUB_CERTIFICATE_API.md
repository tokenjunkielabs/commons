# Exact cyclotomic certificates for mutually unbiased bases

Operation: `PPL008-CYCLOTOMIC-MUB-CERTIFICATE-20261004-7CA6`.  
[Original claim](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1791139618290799).

This addition constructs the classical three product bases in dimension six
and retains an exact certificate for every norm and overlap. The public
compiler also accepts other bounded basis families in the same coefficient
ring. A separate saved-result reader returns basis coordinates, individual
overlaps in either direction, and complete pages without recomputing their
arithmetic.

The actual result contains **18 positive column squared norms, 45 zero
within-basis off-diagonal inner products, and 108 cross-basis comparisons**.
All pass. After normalization, every cross-basis squared overlap is exactly
$1/6$. The receipt preserves all 171 records and all 1,026 component terms.

## Files and source identity

| File | Purpose |
|---|---|
| [cyclotomic_mub_certificates.cjs](cyclotomic_mub_certificates.cjs) | Exact ring arithmetic, classical product recipe, generic finite compiler and saved-result reader |
| [dimension6_product_triple.json](dimension6_product_triple.json) | Complete constructed family, conjugates, norms, component products, partial sums, comparisons and seven reader responses |
| [README.md](README.md) | Entry point and concise mathematical result |

The source executed for this consumer is Git blob
`c10abc5098a368831722e804b1b11138efc5a696`, 25,058 bytes. The complete receipt
is blob `1898bdd954189f7e9d76b262f9c207aaf1652c6a`, 489,146 bytes. No matrix
calculation or reader query was rerun while formatting these artifacts.

The mathematical construction is classical. The original KCIK Problem 2 asks
for at least four mutually unbiased bases in dimension six, or a proof that
seven cannot exist. The three-basis certificate resolves neither target.
The dated primary problem statement and construction sources are identified
below; their publication dates are not a claim about the current literature
frontier.

## Coordinate and normalization conventions

### Exact coefficient ring

Set

$$
\zeta=e^{2\pi i/12}=\frac{\sqrt3+i}{2}.
$$

A coordinate is stored as four canonical integer strings

$$
[a,b,c,d]\quad\longleftrightarrow\quad a+b\zeta+c\zeta^2+d\zeta^3.
$$

All computation takes place with BigInt coefficients in

$$
\mathbb Z[T]/(T^4-T^2+1).
$$

The constant-first minimal-polynomial array is `[1,0,-1,0,1]`. The concrete
embedding is part of the contract: $i=\zeta^3$ and
$\omega=e^{2\pi i/3}=\zeta^4$.

This representation is faithful. The displayed $\zeta$ satisfies
$\zeta^4-\zeta^2+1=0$. Moreover, $i=\zeta^3$ and
$\sqrt3=2\zeta-\zeta^3$, so $\mathbb Q(\zeta)=\mathbb Q(i,\sqrt3)$.
The latter has degree four over $\mathbb Q$: $\sqrt3$ is not rational and
cannot belong to the real elements of $\mathbb Q(i)$ except as a rational.
Thus the quartic is minimal. Equality of two reduced four-coefficient arrays
is equivalent to equality of the represented complex numbers.

No approximate complex number, trigonometric evaluation, square root,
eigenvalue solver or floating-point tolerance is used by the compiler.

### Multiplication and conjugation

For a product, first form the ordinary coefficient convolution
$q_0,\ldots,q_6$. The relations

$$
\zeta^4=\zeta^2-1,\qquad
\zeta^5=\zeta^3-\zeta,\qquad
\zeta^6=-1
$$

give the reduced product

$$
[q_0-q_4-q_6,\ q_1-q_5,\ q_2+q_4,\ q_3+q_5].
$$

Conjugation follows from
$\bar\zeta=\zeta-\zeta^3$,
$\overline{\zeta^2}=1-\zeta^2$, and
$\overline{\zeta^3}=-\zeta^3$:

$$
\overline{[a,b,c,d]}=[a+c,\ b,\ -c,\ -(b+d)].
$$

The source implements these identities directly. Its twelve-entry phase table
is the same reduction of $1,\zeta,\ldots,\zeta^{11}$ and uses no approximate
phase values.

### Unnormalized columns

An input basis is a list of columns. Every entry in every column is a
four-string coefficient array. If a column $v$ has squared norm $h>0$, its
normalized vector is $v/\sqrt h$. The compiler requires $h$ to be an integer;
it does not require the Euclidean norm $\sqrt h$ to be an integer.

For two columns $v,w$ with positive squared norms $h,g$,

$$
\left|\left\langle \frac v{\sqrt h},\frac w{\sqrt g}\right\rangle\right|^2
=\frac{|\langle v,w\rangle|^2}{hg}.
$$

Consequently the dimension-$d$ cross-basis criterion is the exact identity

$$
d\,|\langle v,w\rangle|^2=hg.
$$

This removes normalization denominators from the comparison. Within a basis,
the off-diagonal inner products must be zero.

The returned `inner_product` is unnormalized. Its associated
`normalization` record stores the two squared norms, the exact ring numerator
and positive integer denominator of the normalized squared overlap, and a
reduced rational probability whenever that numerator is rational.

## The explicit dimension-six family

The local matrices are

$$
H_2=\begin{pmatrix}1&1\\1&-1\end{pmatrix},
\qquad
Y_2=\begin{pmatrix}1&1\\i&-i\end{pmatrix},
$$

$$
F_3[y,j]=\omega^{yj},\qquad D[y,y]=\omega^{y^2},
\qquad y,j\in\{0,1,2\}.
$$

The three unnormalized bases are the columns of

$$
I_6,\qquad H_2\otimes F_3,\qquad Y_2\otimes(DF_3).
$$

They have the stable API IDs `computational`, `fourier_product` and
`quadratic_product`. The standard columns have squared norm one. Each of the
other twelve columns has squared norm six.

Rows use index $3x+y$, where $x=0,1$ and $y=0,1,2$. Columns use $3b+j$ with
the analogous ranges. The two dense entry exponents are

$$
6xb+4yj\pmod {12}
$$

and

$$
3x+6xb+4(y^2+yj)\pmod {12},
$$

respectively. The receipt retains every exponent in column/row order.
For the computational basis, exponent zero denotes its nonzero entry and
null denotes a zero coordinate.

These are direct product bases: each vector factors according to the fixed
$\mathbb C^2\otimes\mathbb C^3$ decomposition. The three qubit bases are the
Pauli eigenbases. The qutrit factors are the standard basis and the
$a=0,1$ quadratic-phase bases in the cited prime-field construction.

For this small case, the usual tensor-product argument can also be seen
directly. The qubit cross sums are entries with squared magnitude one when a
standard column is involved, and $1\pm i$ with squared magnitude two between
the two dense bases. The qutrit quadratic cross sum is

$$
S_\ell=\sum_{y=0}^2\omega^{y^2+\ell y}.
$$

In $|S_\ell|^2$, write $y=z+h$. For $h\ne0$, the inner geometric sum
$\sum_z\omega^{2hz}$ is zero; the $h=0$ contribution is three.
Thus $|S_\ell|^2=3$. Tensor inner products multiply the corresponding local
inner products. This explains the classical construction; the published
certificate additionally records the actual six-dimensional arithmetic.

## What the finite certificate proves

### Complete pair coverage

For $b$ bases of $d$ columns, the compiler creates

$$
bd+\frac{bd(d-1)}2+\binom b2d^2
=\frac{bd(bd+1)}2
$$

records. These are all diagonal norms, each within-basis upper pair, and every
column pair between each pair of distinct bases. Hermitian symmetry supplies
the opposite orientation; the conjugate scalar is retained explicitly.

For $b=3,d=6$, the counts are $18+45+108=171$. This is the complete upper
triangle of the Gram matrix of all eighteen vectors, including its diagonal.
There are no sampled column pairs.

### Evidence in each record

Each record contains its canonical left/right addresses, the unnormalized
inner product, its conjugate, its absolute square and the relevant exact
comparison. For each of the six coordinates it additionally contains:

- the conjugated left entry and the right entry;
- their reduced product;
- the running partial sum after adding that product.

The compiler precomputes each coordinate conjugate once. It then accumulates
each dot product using the conjugate-left inner-product convention.

A positive scalar diagonal, represented by `[h,0,0,0]` with $h>0$, establishes
a supported nonzero column. Zero upper off-diagonal Gram entries establish
orthogonality; $d$ nonzero orthogonal columns form a basis. Dividing each by
its positive norm therefore gives an orthonormal basis. Every cross comparison
then establishes the defining normalized squared overlap $1/d$.

All coefficient comparisons are exact. A finite failure concerns the supplied
basis family, not the existence of some other family.

### Rational probabilities and general failed families

The exact normalized squared overlap is retained even if its numerator has
nonconstant cyclotomic coefficients. A reduced rational probability is present
only when all three nonconstant coefficients are zero and the constant
coefficient is nonnegative. Reduction uses the integer gcd and exact division.

Every record in the actual successful family has a rational probability.
The generic complete-failure path can retain an irrational numerator instead;
the API does not silently round it into a rational number.

## Public API

The CommonJS module performs no I/O. It exports three functions plus the
schema constants and frozen limits.

| Export | Purpose |
|---|---|
| `buildDimensionSixProductTriple({source_id})` | Construct the explicit three-basis family above |
| `certifyCyclotomicMubFamily(family)` | Compute a complete finite certificate within the coefficient/norm contract |
| `openCyclotomicMubCertificate(certificate, {source_id})` | Copy and index an identified completed certificate |
| `FAMILY_SCHEMA` | `commons.cyclotomic12_basis_family/v1` |
| `SCHEMA` | `commons.cyclotomic12_mub_certificate/v1` |
| `READER_SCHEMA` | `commons.cyclotomic12_mub_reader/v1` |
| `LIMITS` | The exact bounded-input and query contract |

### Family input

The generic compiler requires a plain JSON-like object with:

```js
{
  schema: 'commons.cyclotomic12_basis_family/v1',
  source_id: 'an explicit source identifier',
  dimension: 6,
  bases: [
    {
      id: 'a unique basis id',
      columns: [
        // Exactly dimension columns.
        // Each column contains dimension entries.
        // Each entry is [a,b,c,d], four canonical integer strings.
      ],
    },
  ],
  construction: {}, // optional, bounded metadata retained without interpretation
}
```

A coefficient such as `['0','0','0','1']` represents $i$.
`['0','0','0','0']` represents zero. Coefficient numbers are not accepted in
place of strings. Leading plus signs, whitespace, leading zeros and `'-0'` are
rejected. Both family and basis IDs must be nonempty strings within the
512-character cap, and basis IDs must be unique.

The family and basis objects reject unknown fields. Optional construction
metadata is copied within the source limits; the compiler does not interpret
it as proof. The builder supplies all required coordinates and its complete
phase recipe.

Generic inputs need not be product vectors. They are restricted to
twelfth-cyclotomic integer coordinates and positive integer squared column
norms. This is a bounded exact-input domain, not all possible complex bases.

### Compiler results

| Status | Meaning |
|---|---|
| `EXACT_MUTUALLY_UNBIASED_BASES` | Complete coverage, supported positive norms and every finite comparison passed |
| `NOT_MUTUALLY_UNBIASED` | Complete coverage with at least one failed orthogonality or unbiasedness comparison for the supplied family |
| `UNSUPPORTED_COLUMN_NORMS` | All diagonal calculations are retained, but at least one squared norm is not a positive integer; further pair calculations were not performed |

The first two results have `complete: true`. The unsupported-norm result has
`complete: false` and is not accepted by the saved reader. It must not be
reported as a completed cross-basis nonexistence result.

Malformed structure, invalid coefficient text or exceeded bounds can throw
`TypeError` or `RangeError` before compilation. Those errors are distinct from
a completed mathematical failure.

### Saved reader methods

```js
const reader = openCyclotomicMubCertificate(certificate, {
  source_id: 'the retained complete certificate identifier',
});

reader.getBasis({basis: 'quadratic_product'});

reader.getOverlap({
  left_basis: 'computational',
  left_column: 4,
  right_basis: 'quadratic_product',
  right_column: 2,
});

reader.page({kind: 'unbiasedness', offset: 96, limit: 12});
reader.summary();
reader.snapshot();
```

Columns and page offsets are zero-based. Basis arguments use the saved IDs.
The reader provides:

| Method | Result |
|---|---|
| `getBasis({basis})` | Complete saved columns, coordinate conjugates, squared norms and coordinate metadata |
| `getOverlap({left_basis,left_column,right_basis,right_column})` | Retained inner product in the requested direction, its normalization and the complete canonical source record |
| `page({kind,offset,limit})` | Complete source records, total size and `next_offset`, which is null at the end |
| `summary()` | Source IDs, source status, basis IDs, record counts, query/materialization counts and work counters |
| `snapshot()` | Summary, query history and unique returned record IDs |

Page kinds are `all`, `norm`, `orthogonality` and `unbiasedness`. An offset equal
to the selected list's length returns an empty terminal page. Unknown keys,
IDs, kinds and out-of-range indices are rejected.

The reader stores one index for every canonical address. A reversed request
selects the already-retained `conjugate_inner_product`. It does not run a
conjugation helper. The returned `source_record`, its detailed terms, and its
left/right squared-norm order remain explicitly labelled as canonical source
orientation. The requested scalar is outside that record under
`answer.inner_product`. The squared overlap is unchanged by reversal.

All returned objects are defensive copies. Changing a returned record or
basis cannot mutate the retained reader data. The outward method object is
frozen. At most 64 operational queries are retained; summaries and snapshots
do not consume that query budget.

The activity snapshot is **not** a certificate or restoration format.
Preserve the separately identified complete certificate with it.

### Minimal usage and reading the published receipt

A new caller can construct and compile a family as follows:

```js
const {
  buildDimensionSixProductTriple,
  certifyCyclotomicMubFamily,
  openCyclotomicMubCertificate,
} = require('./cyclotomic_mub_certificates.cjs');

const family = buildDimensionSixProductTriple({
  source_id: 'my-explicit-classical-product-recipe',
});
const certificate = certifyCyclotomicMubFamily(family);
const reader = openCyclotomicMubCertificate(certificate, {
  source_id: 'my-retained-complete-certificate',
});
```

The published receipt already contains the actual certificate. A consumer
using it can omit construction and compilation:

```js
const fs = require('node:fs');
const receipt = JSON.parse(
  fs.readFileSync('./dimension6_product_triple.json', 'utf8')
);
const reader = openCyclotomicMubCertificate(receipt.certificate, {
  source_id: 'gitblob:1898bdd954189f7e9d76b262f9c207aaf1652c6a:certificate',
});
```

These snippets are usage examples, not additional executions behind the
published counters.

## Source validation and bounds

The reader accepts a completed certificate with the exact emitted coordinate
metadata. Preserve that metadata object as serialized by the compiler. It
checks the source family shape, IDs, coefficient formats, positive stored
squared norms, conjugate-coordinate shapes and the required record count.

For each record it checks contiguous IDs, canonical valid addresses, unique
address coverage, expected record kind, complete component indices and
coefficient shapes. It checks normalization references against the saved norm
table and the numerator against the retained absolute square. Declared
success must agree with the retained Boolean decisions.

These are structural and selected-reference checks. They do not multiply the
saved component factors again, resummate the dot products, establish the
saved conjugates, recompute norm products or rerun gcd reduction. A fabricated
but structurally plausible receipt can still contain false mathematics. A
source-ID string, including one containing a Git blob, is not itself source
authentication. The caller must establish the certificate's provenance.

| Limit | Bound |
|---|---:|
| Dimension | 2 through 6 |
| Bases | 1 through dimension + 1, at most 7 |
| Magnitude digits in each input coefficient | 64 |
| Digits accepted for a result coefficient | 300 |
| Characters per source or basis ID | 512 |
| Operational reader queries | 64 |
| Records per page | 36 |
| Nodes copied from family input | 20,000 |
| Family string/key characters | 1,000,000 |
| Nodes copied from a certificate | 500,000 |
| Certificate string/key characters | 12,000,000 |
| Nested copy depth | 24 |

The copying routines support safe-integer metadata numbers, strings, arrays,
plain objects, Booleans and null. Unsupported values and excessive structures
are rejected. Object keys are copied through explicit own-property definitions.

For $b$ bases of dimension $d$, there are $bd(bd+1)/2$ stored dot products and
$d$ component terms per product. The compiler therefore uses
$O(b^2d^3)$ fixed-degree ring operations and retains the corresponding complete
term evidence. BigInt cost additionally depends on coefficient length.
The bounded reader copies and indexes the receipt once; individual overlap
queries copy the selected stored record without rebuilding its arithmetic.
A page copies the complete selected records, so its cost depends on the
returned evidence volume.

## Actual consumer and complete work accounting

The one new consumer began at **2026-10-04T18:55:23.527Z**. It built the
classical family once, compiled it once, opened a reader in a fresh module
instance, and issued seven operational queries.

| Observed stage | Elapsed milliseconds |
|---|---:|
| Build explicit family | 1 |
| Compile complete certificate | 7 |
| Open fresh saved reader | 18 |
| Seven reader queries | 3 |
| Total including evidence retention between stages | 33 |

These are single elapsed observations in connected V8, not a benchmark or a
claim about other hardware or inputs.

### Returned reader results

| Request | Stored result | Record |
|---|---|---:|
| Complete `quadratic_product` basis | Six columns, all squared norms six | Basis index 2 |
| Computational column 4 to quadratic column 2 | $i$, normalized squared overlap $1/6$ | 125 |
| Quadratic column 2 to computational column 4 | $-i$, normalized squared overlap $1/6$ | Same 125, reversed |
| Fourier column 0 to quadratic column 0 | `[-1,-2,2,1]`, normalized squared overlap $1/6$ | 135 |
| Fourier column 0 to Fourier column 1 | Zero, normalized squared overlap zero | 33 |
| Quadratic column 3 to itself | Six, normalized squared overlap one | 15 |
| Unbiasedness page at offset 96, limit 12 | Complete last twelve records of 108; `next_offset: null` | 159–170 |

The dense cross-basis inner product `[-1,-2,2,1]` represents
$-\sqrt3+i\sqrt3$. Its absolute square is six, while the squared-norm product
is $6\cdot6=36$, yielding $1/6$ after normalization.

The forward/reverse pair materialized record 125 twice. Its scalar changed
from the stored inner product to its stored conjugate. The complete detailed
term record retained its original canonical orientation in both responses.

### Compiler counters

| Counter | Value |
|---|---:|
| `compiler_calls` | 1 |
| `input_columns` | 18 |
| `input_coordinates` | 108 |
| `input_coefficients` | 432 |
| `precomputed_coordinate_conjugates` | 108 |
| `inner_products` | 171 |
| `retained_component_terms` | 1,026 |
| `ring_products` | 1,197 |
| `ring_additions` | 1,026 |
| `ring_conjugations` | 279 |
| `ring_scalar_products` | 108 |
| `integer_products` | 19,755 |
| `integer_additions` | 29,799 |
| `integer_negations` | 558 |
| `rational_reductions` | 171 |
| `euclidean_steps` | 279 |
| `exact_integer_divisions` | 342 |
| `norm_checks` | 18 |
| `orthogonality_checks` | 45 |
| `unbiasedness_checks` | 108 |
| `normalized_overlap_records` | 171 |
| `floating_point_decisions` | 0 |

Each of the 171 dot products has six component terms. There are 1,026 component
ring products and 171 additional products for their absolute squares, totaling
1,197. The 108 precomputed entry conjugates and 171 dot-product conjugates
give 279 conjugations.

The implementation counts all sixteen coefficient products in every
four-by-four polynomial convolution, including zero terms. Convolution
accumulation and reduction, dot-product additions, conjugation additions and
negations, cross-comparison scaling, scalar norm products and gcd reduction
are included in the appropriate counters. The builder's 36 identity entries,
72 small integer phase formulas and 72 phase-table lookups are separately
recorded in `certificate.family.construction.stats`.

### Saved reader counters

| Counter | Value |
|---|---:|
| `reader_opens` | 1 |
| `source_records_copied` | 171 |
| `source_component_terms_copied` | 1,026 |
| `indexed_records` | 171 |
| `overlap_queries` | 5 |
| `basis_queries` | 1 |
| `page_queries` | 1 |
| `source_record_materializations` | 17 |
| `basis_coordinates_returned` | 36 |
| `source_compiler_calls` | 0 |
| `new_inner_products` | 0 |
| `new_ring_products` | 0 |
| `new_rational_reductions` | 0 |
| `floating_point_decisions` | 0 |

The reader returned 17 full source-record copies representing 16 distinct
records, plus the 36 coordinates of one complete basis. It indexed all 171
source records and validated the shapes of all 1,026 retained component
terms. It computed no new dot product, ring product or rational reduction.

The full builder output and the compiler's retained family matched by JSON
identity. The complete receipt, including every query response and the final
reader activity record, was formatted and parsed back by identity only.
No second construction, compilation or saved-reader query was used as a
verification pass.

Other dimensions, other input families, failed comparisons, unsupported norms,
and bound/error branches were source-inspected only.

## Primary sources and mathematical scope

The original target is Problem 2, section II.B, of Paweł Horodecki,
Łukasz Rudnicki and Karol Życzkowski, *Five open problems in theory of quantum
information*, arXiv:2002.03233v2, December 21, 2020:
[KCIK primary PDF](https://kcik.ug.edu.pl/wp-content/uploads/2021/12/2002.03233.pdf).
It specifies the normalized overlap convention and the alternatives of
constructing four bases or excluding a complete seven-basis family. We use
that statement to identify the target, not to infer a current prize amount,
renewal or solution status.

Andreas Klappenecker and Martin Rötteler, *Constructions of Mutually Unbiased
Bases*, arXiv:quant-ph/0309120:
[primary PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/Constructions-of-Mutually-Unbiased-Bases.pdf),
Theorem 2 and Lemma 3, supplies the quadratic-phase and tensor-product
construction. The theorem credits the earlier Ivanović and Wootters–Fields
construction lineage. This consumer uses the odd-characteristic quadratic
family at $q=3$; it does not use the separate Alltop construction, whose
characteristic restriction excludes three.

Daniel McNulty and Stefan Weigert, *All Mutually Unbiased Product Bases in
Dimension Six*, arXiv:1111.3632v2, March 24, 2012:
[primary PDF](https://arxiv.org/pdf/1111.3632), Theorem 4, states that no
mutually unbiased product triple in dimension six admits even one additional
mutually unbiased vector. The additional vector may be entangled. Applied to
the displayed product triple, the source theorem excludes extending this
particular triple to a fourth basis. The statement was read; its earlier
computer-algebraic proof dependency was not independently rerun or audited.

That last source theorem does not exclude four arbitrary MUBs or establish
a global maximum of three. The finite matrix certificate proves neither an
extension obstruction nor a universal upper bound. It supplies exact,
inspectable arithmetic and a reusable bounded interface for the displayed
classical construction and for other supplied families in the stated ring.

No new construction priority, external record, asymptotic result, formal proof
assistant verification, sponsor submission, acceptance or payment is claimed.
