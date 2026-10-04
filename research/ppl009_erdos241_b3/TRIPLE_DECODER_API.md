# Saved Bose–Chowla triple-sum decoder

Operation: `ERDOS241-SAVED-TRIPLE-DECODER-20261004-7CA6`.  
[Original claim](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1791137658574379).

The new API decodes fixed-length sums of three elements of an established
Bose–Chowla set using its saved finite-field data. It handles repeated summands,
returns complete polynomial quotient/remainder records and distinguishes
modular sums from ordinary integer sums. It performs no field construction,
power-cycle generation, affine-orbit search or triple census.

The recorded consumer uses the accepted affine positive set

$$
B=\{1,13,32,66,169,174,396,416,756,858,915,1016,1044\}
$$

modulo $M=2196$. This set and its finite bound $f(1044)\ge13$ were already
delivered in [PR31280](https://github.com/woahwhattheheck/commons/pull/31280).
They are source premises here. This addition supplies decoding; it claims no
new construction record, extremal equality, asymptotic improvement or novelty.

## Files and exact source custody

| File | Contents |
|---|---|
| [bose_chowla_triple_decoder.cjs](bose_chowla_triple_decoder.cjs) | Bounded saved-source loader, basis conversion, polynomial decoder and query cache |
| [prime13_saved_triple_decoding.json](prime13_saved_triple_decoding.json) | Complete calibration, six query results, four polynomial records, all divisions and execution evidence |
| [prime13_cubic_b3_construction.json](prime13_cubic_b3_construction.json) | Unchanged complete source construction, including all 2,196 power codes and 13 offset labels |
| [prime13_affine_orbit_minimum.json](prime13_affine_orbit_minimum.json) | Unchanged affine-orbit result and selected positive lift |
| [BOSE_CHOWLA_B3_API.md](BOSE_CHOWLA_B3_API.md) | Existing constructor/optimizer contract and classical source proof |
| [bose_chowla_b3.cjs](bose_chowla_b3.cjs) | Existing constructor and optimizer, unchanged |

The decoder takes the original construction's `result` member. It does not
take the outer receipt or the affine optimizer as its construction input.

| Source | Identity used |
|---|---|
| Original construction dataset | `2b77e0e8dc97c5107ab5a4e5cca162a92c12de38` |
| Original merged commit | `435db8587c0934b6f60301a132d437a6ac6f915f`, [PR31278](https://github.com/woahwhattheheck/commons/pull/31278) |
| Affine-orbit dataset | `0c31cc4c2e3e2639bb204f4b97095132134932e6` |
| Affine-orbit merged commit | `e4929586e70f694872e0867907dcd42429d35391`, [PR31280](https://github.com/woahwhattheheck/commons/pull/31280) |
| Existing constructor/optimizer module | `f5b177bfad4fa76d8a6ad37323199b0f222da6c7` |
| Existing constructor/optimizer guide | `b42119d2d55b8709a04fc01ec8625c56505dd309` |
| Executed decoder source | `cf09038fdaad042cfcc342068c1a4afb4b9c985c` |

The copied source establishes a prime $p$, a cubic extension $K/\mathbb F_p$,
a primitive element $\theta$ of order $M=p^3-1$, the independent basis
$1,\theta,\theta^2$, its complete saved powers and the plus-offset labels

$$
\theta^{a_\lambda}=\theta+\lambda,\qquad \lambda\in\mathbb F_p.
$$

These facts belong to the accepted source construction. Structural loading
checks their representation and selected cross-references. It does not
authenticate a supplied file, test primality again, prove irreducibility again,
recheck primitive-element orders or multiply around the saved cycle.

The selected affine source supplies

$$
b(a)\equiv ua+v\pmod M,\qquad u=257,\quad v=1952.
$$

The decoder uses the unique representative in $1,\ldots,M$, so residue zero
is represented by $M$. This agrees with the saved cut map
$((257a-245)\bmod2196)+1$. All 13 resulting source-to-lift mappings and the
complete sorted value list matched the saved orbit record exactly.

The source IDs retained by the API are caller-supplied strings. A string
containing a Git blob identity does not itself authenticate the input object.

## Decoder proof

### 1. Convert a saved code to the theta basis

The source encodes $x_0+x_1\alpha+x_2\alpha^2$ by

$$
x_0+px_1+p^2x_2,\qquad 0\le x_i<p.
$$

Let $C$ be the $3\times3$ matrix whose columns are the saved alpha-basis
coordinates of $1,\theta,\theta^2$. The source's degree certificate gives
$\det C\ne0$ in $\mathbb F_p$.

A new decoder open computes $C^{-1}$ by Gauss–Jordan elimination modulo
$p$. It records every swap, scaling and row subtraction, together with the
resulting augmented matrices and the inverse witnesses. For any saved code
with alpha coordinates $x$, its theta coordinates are $C^{-1}x$.

Only base-field scalar arithmetic is needed. The source already contains the
extension-field products and powers; the decoder does not regenerate them.

### 2. Recover the monic minimal cubic

Read the saved code at exponent three and express it in the retained basis:

$$
\theta^3=c_0+c_1\theta+c_2\theta^2.
$$

Then

$$
m(T)=T^3-c_2T^2-c_1T-c_0
$$

vanishes at $\theta$. The accepted degree-three property makes this its monic
minimal polynomial. No search over polynomials or new field exponentiation is
required.

For the actual saved basis,

$$
C^{-1}=
\begin{pmatrix}
1&6&10\\
0&1&12\\
0&0&1
\end{pmatrix}
\quad\text{over }\mathbb F_{13},
$$

and the new calibration gives

$$
m(T)=T^3+5T^2+4T+6.
$$

The module stores polynomial coefficients in constant-first order, hence the
array `[6,4,5,1]`. This is consistent with the source's
$\theta=7+\alpha$, $\alpha^3=2$, which gives
$m(T)=(T-7)^3-2$ over $\mathbb F_{13}$.

### 3. Obtain the unique monic cubic for one residue

For a normalized source exponent $e$, read its saved power and transform it:

$$
\theta^e=v_0+v_1\theta+v_2\theta^2.
$$

Define

$$
P_e(T)=m(T)+v_0+v_1T+v_2T^2.
$$

It is monic of degree three and satisfies $P_e(\theta)=\theta^e$. It is also
the unique monic cubic with that value: the difference of two such cubics has
degree at most two, and the independent degree-three basis prevents a nonzero
such difference from vanishing at $\theta$.

Now use the retained plus-offset convention. A triple of source labels obeys

$$
a_{\lambda_1}+a_{\lambda_2}+a_{\lambda_3}\equiv e\pmod M
$$

if and only if

$$
P_e(T)=\prod_{i=1}^{3}(T+\lambda_i).
$$

For the forward direction, evaluate the product at $\theta$ and use its saved
label identities. It is a monic cubic with the required value, so it equals
$P_e$. For the reverse direction, evaluate the factorization at $\theta$
and use the accepted order $M$ of the primitive element. Unique factorization
into monic linear factors recovers the label multiset, including multiplicity.

Thus decoding a sum becomes a degree-three splitting problem over the small
base field. No comparison against every triple of set elements is needed.

### 4. Scan roots with complete quotient/remainder evidence

Because the source uses $\theta+\lambda$, a factor $T+\lambda$ has root
$-\lambda$. The implementation scans offsets $\lambda=0,\ldots,p-1$, uses
the canonical root $-\lambda\bmod p$, and computes a synthetic division

$$
Q(T)=(T+\lambda)S(T)+r.
$$

Each attempt retains the offset, root, complete dividend, complete quotient and
remainder. A nonzero remainder leaves the current polynomial unchanged. A zero
remainder removes that linear factor and repeats the same offset on the new
quotient. This recovers repeated factors without a squarefree assumption or
derivative calculation, including in characteristics two and three.

The process stops as soon as three factors have been removed and the remaining
polynomial is $1$. Otherwise every base-field offset is visited. A label that
was a nonroot cannot become a root after removing factors with different
labels: those removed factors have nonzero values at that label. A single
increasing pass therefore suffices.

If a positive-degree residual remains after that pass, the monic cubic does
not split into three source factors. By the equivalence above, the residue has
no representing triple. An irreducible cubic, or an irreducible quadratic left after removing one
linear factor, gives a legitimate absence outcome.

The successful factor labels are mapped back to their retained source
exponents. Their exponent sum is checked against $e$; an inconsistency raises
a source error rather than returning a mathematical absence. The positive
lifts are then returned in sorted order, with explicit multiplicities.

### 5. Normalize the affine sum and check integer lifts

The decoder's affine set uses $b(a)\equiv ua+v\pmod M$, where $u$ must be a
unit. Repeated entries contribute the same translation once per summand, so a
requested three-term sum $s$ maps to

$$
e\equiv u^{-1}(s-3v)\pmod M.
$$

The factor is $3v$, including when two or three summands agree. The unit
inverse is computed by the extended Euclidean algorithm and retained with a
Bézout witness. In the actual case,

$$
u^{-1}=1145,\qquad 257\cdot1145-134\cdot2196=1.
$$

For modular queries, the unique decoded multiset is the answer even when its
actual integer sum differs from $s$ by a multiple of $M$. For an ordinary
integer query, the implementation additionally sums its actual positive
representatives and compares that exact integer with the requested value.

That final comparison is decisive. A $B_3$ modular set has at most one
candidate multiset for a residue, so a mismatch rules out an integer
representation; it cannot be repaired by selecting a second modular triple.

## API

The plain CommonJS module performs no I/O and exports:

| Export | Contract |
|---|---|
| `openBoseChowlaTripleDecoder(construction, options)` | Copy and check an identified completed source; derive decoder coordinates and the selected positive affine map |
| `DecoderSourceError` | Detectable source/reference/basis or unit-invertibility failure |
| `INPUT_SCHEMA` | `erdos241.bose_chowla_b3/v1` |
| `SCHEMA` | `erdos241.bose_chowla_triple_decoder/v1` |
| `LIMITS` | Frozen input, query and memory bounds |

The required options object has this shape:

```js
{
  source_id: 'an explicit identifier for the construction result',
  affine_source_id: 'an optional identifier for the affine parameters',
  unit: 257,          // defaults to 1
  translation: 1952, // defaults to 0
}
```

Only `source_id` is required. Both identifiers must be nonempty strings within
the 512-character cap when supplied. The unit and translation use safe-integer
numbers, with $1\le u<M$, $0\le v<M$, and $\gcd(u,M)=1$. Unknown option
fields are rejected. The default affine map selects the source's canonical
positive exponents; it does not silently select an optimized cut.

The returned object exposes:

| Method | Result |
|---|---|
| `decodeModSum({sum})` | A unique triple for the requested residue, or a complete nonsplitting record |
| `decodeIntegerSum({sum})` | The modular decoding plus exact comparison with the actual positive integer sum |
| `summary()` | Source/affine metadata, sorted positive values, work counters and cache/query counts |
| `snapshot()` | Complete calibration, offset map, every created polynomial, all division records and query history |

A sum may be a BigInt, a safe-integer number, or a canonical decimal integer
string with at most 1,024 magnitude digits. Negative sums are supported and
normalized modulo $M$ for modular decoding. Leading plus signs, extra
whitespace, leading zeros, the string `"-0"`, fractional values and unsafe
integer numbers are rejected. An integer query still compares the original
signed value, so a negative integer cannot be mistaken for a positive triple
sum.

### Minimal caller example

This example shows how a caller loads the two identified files and opens a
decoder. The published receipt already contains the actual results, so
inspecting that receipt requires no execution of this example.

```js
const fs = require('node:fs');
const {
  openBoseChowlaTripleDecoder,
} = require('./bose_chowla_triple_decoder.cjs');

const construction = JSON.parse(
  fs.readFileSync('./prime13_cubic_b3_construction.json', 'utf8')
).result;
const best = JSON.parse(
  fs.readFileSync('./prime13_affine_orbit_minimum.json', 'utf8')
).result.best;

const decoder = openBoseChowlaTripleDecoder(construction, {
  source_id: 'gitblob:2b77e0e8dc97c5107ab5a4e5cca162a92c12de38:result',
  affine_source_id: 'gitblob:0c31cc4c2e3e2639bb204f4b97095132134932e6:result.best',
  unit: best.unit,
  translation: best.residue_translation,
});

const repeatedPair = decoder.decodeIntegerSum({sum: '1042'});
// status: 'decoded'; positive_values: [13, 13, 1016]

const modularTriple = decoder.decodeModSum({sum: 936n});
// status: 'decoded'; positive_values: [1044, 1044, 1044]
// represented_integer_sum: '3132'

const ordinarySum = decoder.decodeIntegerSum({sum: '936'});
// status: 'integer_lift_mismatch'; found: false
// Reuses the modularTriple polynomial; actual positive sum is 3132.

const activity = decoder.snapshot();
```

The comments abbreviate the returned structure. The positive values are under
`answer.decoded.positive_values`. Every successful return also includes
`answer.polynomial_record` with its saved power coordinates, monic cubic,
complete division trace, residual and factors.

### Outcome fields and failures

| Query status | Meaning |
|---|---|
| `decoded` | The requested modular residue has a triple; for an integer query, its actual positive sum also equals the request |
| `no_representation` | The unique monic cubic does not split completely over the base field, and the complete scan is retained |
| `integer_lift_mismatch` | A unique modular triple exists, but its actual positive sum differs from the requested integer |
| `source_error` | A mathematical source/reference inconsistency was encountered; the query is retained and the error is thrown |
| `incomplete` | A different failure interrupted a started query; the query and error text are retained and the error is thrown |

The Boolean `found` is true only for `decoded`. In an integer lift mismatch,
`modular_representation_exists` remains true and the decoded modular triple is
returned for inspection. A nonsplitting result has `decoded: null` and
`represented_integer_sum: null`. For a decoded modular query,
`integer_sum_matches` is null because no ordinary equality was requested. For
an integer query with a modular triple, it records the exact equality result.

Malformed options, unsupported source objects, invalid numbers and exhausted
bounds can raise `TypeError` or `RangeError`. Invalid invertibility and the
explicit decoder consistency checks raise `DecoderSourceError`. Validation
that fails before a query starts does not create a query-history entry.
Opening failures return no decoder instance. Callers should handle errors as
errors, not convert them into a claim of nonrepresentation.

### Cached activity and ownership of records

The polynomial cache key is the normalized source exponent `e`. Modular
aliases, very large integer strings and ordinary queries with the same residue
therefore share the same cubic, roots, source labels and positive triple. A
cache hit still normalizes the new input and, when requested and applicable,
checks its exact ordinary integer sum. It performs no new basis transform,
saved-power read or root scan.

A polynomial entry is inserted before its arithmetic begins. If construction
fails, its partial evidence and `source_error` state remain available. Reusing
that entry rethrows the failure; the module does not retry its arithmetic
silently.

Each returned answer includes a complete copy of the associated polynomial
record, including its original `new_work` counters. Those counters describe
the work when that polynomial was first created. They are not charged again
on a cache hit. To obtain totals, use `snapshot().summary.stats` or sum the
distinct records in `snapshot().polynomials`; do not sum repeated polynomial
copies across all returned answers.

The open operation takes a defensive bounded copy of the source. Returned
summaries, query results and snapshots are also copies, so changing a caller's
returned object does not mutate the decoder cache. The outward method object
is frozen.

An activity snapshot contains calibration, the complete offset-to-positive
map, all created polynomials, their division evidence, query history and
counters. The complete source power table stays in its separately identified
artifact. An activity snapshot is **not** a constructor input or a
cache-restoration format. A caller retaining a receipt should preserve both
the snapshot and its exact source artifacts.

## Source validation and resource contract

The loader accepts bounded JSON-like data: plain objects, arrays, strings,
safe-integer numbers, Booleans and null. It rejects unsupported values and
oversized structures before decoder arithmetic. Copying object properties uses
explicit own-property definitions.

It requires the original input schema, completed construction status, and
order of sums three. The prime lies within the supported bounds; the declared
field size and modulus must equal its cube and cube minus one. It checks the
cubic coefficient representation and the exact basis/code conventions.

The retained generator's code and coefficients must agree. The degree record
must declare a nonzero determinant, and the recorded columns for
`1, theta, theta^2` must agree with the corresponding saved power codes. The
decoder's own basis inversion then has to succeed modulo the declared prime.

The saved cycle has exactly `M` entries, exponent range `0..M-1`, the expected
first codes and return-to-one metadata. Every nonzero code is checked to be in
range and to occur once. This is a **permutation and reference check**; it does
not verify the multiplication recurrence or regenerate the cycle.

There must be exactly one record for every base-field offset, with distinct
source exponents and consistent plus-offset target coordinates. Every target
must match the power code at its retained exponent. The sorted residue set
must match those labels, and the retained theorem flags must state the
expected cardinality, repetitions convention and modular `B3` property.

These checks make accidental format and cross-reference failures visible.
They do not make fabricated but structurally plausible data into a certified
field or a valid power table. Mathematical correctness remains conditional on
the caller-established construction and its provenance.

| Limit | Bound |
|---|---:|
| Declared prime | 2 through 43 |
| Retained nonzero power codes | At most 79,506 |
| Decimal magnitude digits in a sum | 1,024 |
| Retained queries per decoder | 64 |
| Distinct cached polynomials per decoder | 64 |
| Characters in each source identifier | 512 |
| Nodes copied from the source | 400,000 |
| Combined source string/key characters | 4,000,000 |
| Source nesting depth | 24 |

The prime bound is a supported input range, not a new primality certificate.
The accepted source supplies the prime-field premise. Unknown option/query
keys are rejected; the source itself retains its additional construction
evidence within the copy bounds.

The required power-table scan uses `O(p^3)` work and storage. Opening also
copies all retained source evidence within the stated caps. Calibration
inverts a fixed `3 x 3` matrix. A new residue reads one
saved code and scans at most `p` offset labels, with at most three successful
factor removals. Each synthetic division has degree at most three. Its new
base-field arithmetic and trace storage are therefore `O(p)`, independent of
the number of possible triples. A cache hit needs no such arithmetic, although copying its full returned
trace still depends on that trace's size. Parsing and reducing a large sum additionally depends on its decimal length;
this is bounded by the input contract.

## The actual saved consumer

One new decoder was opened at **2026-10-04T18:22:46.992Z**, followed by four
integer queries and two modular queries. The source module executed was blob
`cf09038fdaad042cfcc342068c1a4afb4b9c985c`. The single observed elapsed time for
that open and six-query sequence was **6 ms** in connected V8; this is one
execution observation, not a timing benchmark.

The complete receipt records the input identifiers, affine parameters, basis
calibration, every query and each distinct polynomial. Its outer schema is
`erdos241.prime13_saved_triple_decoding/v1`.

| Query in execution order | Result | Source exponent | Polynomial cache |
|---|---|---:|---|
| Integer `1042` | `13 + 13 + 1016 = 1042` | 2126 | Created |
| Modular `10^500 * 2196 + 1042` | Same triple; the request is a 504-digit integer | 2126 | Reused |
| Integer `3132` | `1044 + 1044 + 1044 = 3132` | 1536 | Created |
| Integer `936` | `integer_lift_mismatch`; the unique modular triple sums to 3132 | 1536 | Reused |
| Modular `1830` | `no_representation`; all 13 offsets have nonzero division remainder | 1830 | Created |
| Integer `1464` | `32 + 416 + 1016 = 1464` | 0 | Created |

The `936` request differs from `3132` by one modulus. Its rejection is the
integer-lift check doing necessary work, with no second factorization.

The nonrepresentation query was selected by one lookup of saved field code
`4` in the accepted power table. That lookup found exponent `1830`, and its
affine sum residue is also `1830`. It did not construct that power again. The
decoder obtained `P(T)=T^3+5T^2+4T+10` and retained all 13 unsuccessful
divisions. Those remainders are a complete base-field nonsplitting witness.

### Distinct polynomial records

All arrays below use constant-first coefficients. Work in this table is
charged once per distinct normalized exponent.

| Exponent | Monic cubic | Offset multiset | Visited offsets | Divisions | New scalar products | New scalar additions |
|---:|---|---|---:|---:|---:|---:|
| 2126 | `[0,0,5,1]` | `[0,0,5]` | 6 | 8 | 20 | 23 |
| 1536 | `[5,4,8,1]` | `[7,7,7]` | 8 | 10 | 36 | 39 |
| 1830 | `[10,4,5,1]` | `[]` | 13 | 13 | 48 | 51 |
| 0 | `[7,4,5,1]` | `[3,5,10]` | 11 | 13 | 33 | 36 |

Each of these four records uses one saved-power read and one coordinate
transform. Opening additionally uses the saved exponent-three code to obtain
the minimal cubic. Its calibration costs 45 scalar products and 27 scalar
additions. These are new decoder operations in the base field.

### Complete cumulative counters

| Counter | Value |
|---|---:|
| `source_power_codes_loaded` | 2,196 |
| `source_offset_records_loaded` | 13 |
| `source_code_permutation_entries_checked` | 2,196 |
| `source_constructor_calls` | 0 |
| `source_primitive_tests` | 0 |
| `source_cycle_steps` | 0 |
| `extension_field_multiplications` | 0 |
| `field_power_calls` | 0 |
| `affine_orbit_evaluations` | 0 |
| `triple_candidates_enumerated` | 0 |
| `modular_inverse_calls` | 4 |
| `euclidean_steps` | 13 |
| `basis_row_swaps` | 0 |
| `base_field_products` | 182 |
| `base_field_additions` | 176 |
| `coordinate_transforms` | 5 |
| `arithmetic_saved_power_reads` | 5 |
| `decoder_field_code_decodings` | 5 |
| `positive_term_maps` | 13 |
| `sum_normalizations` | 6 |
| `polynomial_cache_misses` | 4 |
| `polynomial_cache_hits` | 2 |
| `root_offsets_visited` | 38 |
| `synthetic_division_attempts` | 44 |
| `linear_factors_removed` | 9 |
| `integer_sum_comparisons` | 4 |

The source-table permutation check concerns 2,196 already retained codes.
It is distinct from extension-field arithmetic. The zero source-constructor,
primitive-test, cycle-step, extension-field multiplication, field-power,
affine-orbit and triple-candidate counters describe the actual executed
consumer, not a claim that the source construction originally cost nothing.

The final snapshot contains six queries and four polynomial records, including
every dividend, quotient and remainder for the 44 synthetic divisions. The
receipt also preserves the opened summary, so calibration can be distinguished
from query work. Two polynomial cache hits are recorded.

Identity comparisons after the consumer found the original construction and
orbit objects unchanged. The decoder's complete 13-term positive list and all
13 source-exponent-to-positive-value mappings matched the accepted affine
record. These were comparisons of retained data, not reruns of field,
construction or orbit mathematics.

## Sources and limits of the result

The mathematical premise is the classical Bose–Chowla construction, already
proved and attributed in [BOSE_CHOWLA_B3_API.md](BOSE_CHOWLA_B3_API.md).
Nathanson's primary exposition states the repeated-summand convention and the
modular construction for a prime power and a fixed sum length; its minus-offset
form is equivalent to the saved plus-offset form because the offset runs over
the whole base field. See Melvyn B. Nathanson, *The Bose–Chowla argument for
Sidon sets*, Journal of Number Theory 238 (2022), 133–146, Section 1 and
Theorem 1: [author PDF](https://www.theoryofnumbers.com/melnathanson/pdfs/nath2022-198.pdf),
[DOI](https://doi.org/10.1016/j.jnt.2021.08.005).

The inspected
[FormalConjectures statement for Erdős 241](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/241.lean),
blob `da73dfa46653a1f32f47defc09eb53e5836f4c69`, defines finite positive sets
and equality of cardinality-three multiset sums. Its displayed declarations
contain `sorry`; that file is a formal statement and source context, not a
machine-checked proof of this decoder or of the conjecture.

The five-step decoder argument above is supplied here for the saved source
contract. The new result is a reusable arithmetic consumer with complete
finite evidence. It neither proves the original source by repetition nor
establishes a new extremal value, a global optimization result, a current
literature frontier or the asymptotic conjecture. No Lean verification,
external submission, sponsorship or payment occurred.
