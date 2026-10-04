# Incremental Hankel extension through order 64

Operation: `MORPHIC-HANKEL-EXTEND64-20261004-7CA6`.  
[Original claim](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1791134909002389).

The retained calculation extends the complete all-shift table from order 32 to
order 64. For the fixed point beginning with $a_0=1$ of

$$
\mu(1)=12,\qquad \mu(2)=23,\qquad \mu(3)=14,\qquad \mu(4)=32,
$$

it establishes

$$
H_n(k):=\det(a_{k+i+j})_{0\le i,j<n}\ne0
\qquad(k\ge0,\;1\le n\le64).
$$

The new work consists of 21,280 exact determinant records for orders 33–64.
The 6,949 accepted records for orders 1–32 supply the base. Their determinant
strings and four minor-reference columns are retained exactly, with only the
carrier-witness column remapped to the new length-127 carrier language. All
28,229 records are available in the archive and its two complete order blocks.

This is a bounded all-shift result. It gives no conclusion for $n>64$, does
not settle the all-order nonvanishing question, and makes no claim of novelty,
formal verification, prize eligibility, payment or sponsor acceptance.

## Files and complete data layout

| File | Purpose |
|---|---|
| [morphic_hankel_extension.cjs](morphic_hankel_extension.cjs) | Incremental extension, archive packing and saved-block assembly |
| [order64_extension.json](order64_extension.json) | Provenance, rejected preflight, complete language, remapped base rows, block manifest, actual saved-reader queries and execution receipts |
| [orders33_48.json](orders33_48.json) | All 8,848 determinant records for orders 33–48 |
| [orders49_64.json](orders49_64.json) | All 12,432 determinant records for orders 49–64 |
| [morphic_hankel_reader.cjs](morphic_hankel_reader.cjs) | Previously accepted saved-table reader, unchanged by this extension |
| [order32_all_shifts.json](order32_all_shifts.json) | Previously accepted complete base calculation, unchanged |
| [HANKEL_INDEX_API.md](HANKEL_INDEX_API.md) | Original factor-coverage and determinant proof |
| [RETAINED_READER_API.md](RETAINED_READER_API.md) | Existing reader contract and its original use |

The outer receipt in `order64_extension.json` has schema
`commons.ppl036.morphic_hankel_extension_receipt/v1`. Its `extension` member is
the archive accepted by `assembleMorphicHankelExtensionArchive`. Its
`block_files` member gives filenames, exact Git blob identities, UTF-8 byte
counts and row counts for the two separately stored blocks.

The archive's `index.orders` contains only the 32 remapped base orders.
**The archive's `index` alone is not a complete order-64 input.** Assembly adds
every listed order block in manifest order. It yields a complete index using
the same input schema as the original compiler and saved reader,
`commons.ppl036.morphic_hankel_index/v1`.

No determinant row is replaced by a sample or a summary. New order records
contain the complete ordered factor rows, sign counts, zero counts and maximum
absolute determinant digit counts. A carrier stores its full word, a known
occurrence, pair index and offset. Each pair-coverage list records every
enumerated offset, including repeated carrier indices. These repetitions
preserve coverage provenance.

The serialized sizes in this particular result are 549,062 bytes for the outer
receipt, 492,609 bytes for orders 33–48 and 819,131 bytes for orders 49–64. The
16-order packing rule is a record-layout bound; it is not a universal byte-size
guarantee for arbitrary inputs.

## Source identity and what is inherited

The base is the `index` member of the original receipt, not a reconstruction.

| Source | Exact identity |
|---|---|
| Original dataset | Blob `bee379d4292f123599fe26ca88ab6056ee8d62c0` |
| Original merged commit | `ba8410152d8ef18b3aa8e96c0c08c774cb8feea6`, [PR31364](https://github.com/woahwhattheheck/commons/pull/31364) |
| Original compiler | Blob `fe1e7493dfe37606d0bf4c1a7ba643cb02dbeb70` |
| Existing saved reader | Blob `0a231ad081144212eaa8a9d143398f5e7c31c3be` |
| Reader merged commit | `b8b67bb82c98b741a15704bb7eb49e4cbcf955ec`, [PR31371](https://github.com/woahwhattheheck/commons/pull/31371) |
| Executed extension module | Blob `299a776c53ab80c62426524ac3ba7689a75374c9` |

The source table establishes a complete nine-pair language, actual occurrence
witnesses for those pairs, four saved images $\mu^6(c)$ of length 64, complete
factor tables through order 32 and their nonzero determinant values. This
extension uses those facts as premises. Structural loading checks their
representation and bounds; it does not recompute the pair closure, reconstruct
the old images, authenticate the file or re-prove the old determinant values.

The nine retained pairs, in the original insertion order, are

$$
12,\;23,\;14,\;32,\;22,\;31,\;42,\;41,\;21.
$$

Their recorded zero-based occurrences are respectively

$$
0,\;2,\;6,\;14,\;1,\;5,\;29,\;11,\;23.
$$

The pair records retain the original source-letter/source-pair provenance. An
occurrence means a proved position at which the pair appears; it is not a
claim that this is its earliest occurrence. The original guide supplies the
finite closure and occurrence proof. That accepted work was not rerun here.

## Why the longer carrier language covers every shift

### Extending saved blocks

For each letter $c$, the module concatenates the two saved images specified
by $\mu(c)$:

$$
\mu^7(c)=\mu^6(\mu(c)_0)\,\mu^6(\mu(c)_1).
$$

This uses the four retained length-64 strings directly. The actual run performs
one extension level, four concatenations and 512 newly produced block
characters. No earlier substitution level is regenerated.

Set $B=128$ and $L=127=2\cdot64-1$. The fixed-point relation gives

$$
a=\mu^7(a_0)\,\mu^7(a_1)\,\mu^7(a_2)\cdots.
$$

Every starting shift has a unique form $k=Bq+t$, with $0\le t<B$.
A factor of length $L$ starting there ends at offset

$$
t+L-1\le127+126=253<2B.
$$

It is therefore contained in $\mu^7(a_q a_{q+1})$. The complete retained pair
language includes $a_q a_{q+1}$, so enumerating the windows in its two-block
image includes that factor.

For each of the nine pair images of length 256, the implementation enumerates
offsets 0 through $256-127=129$, inclusive: 130 windows per pair and 1,170 in
total. The completeness proof only needs aligned offsets 0–127. The additional
offsets 128 and 129 are also sound, because the whole two-block word occurs in
the fixed point. They introduce no words outside the actual factor language.

If the source pair $uv$ is known to occur at shift $s$, then its expanded
two-block word occurs at shift $128s$. A window at offset $t$ consequently
has the recorded occurrence $128s+t$. The module retains the first witnessed
copy encountered for each distinct word and sorts those words lexicographically.
The actual run obtains exactly 882 distinct length-127 carriers.

This argument proves both directions: every enumerated carrier occurs, and
every factor of length 127 is enumerated. Dedupe changes neither assertion.

### Every smaller factor remains represented

Every occurrence of a shorter factor has a right extension to length 127,
because the fixed point is infinite to the right. Its extension belongs to the
complete carrier set above. Thus every factor of length $2n-1$, for every
$n\le64$, is a prefix of some retained length-127 carrier. Conversely, every
such prefix is an actual factor.

For a fixed order, scanning the sorted carriers and deduplicating adjacent
prefixes therefore gives the exact complete factor language for that order.
Determinants depend only on these $2n-1$ entries. A finite table indexed by
these factors applies to every nonnegative shift, including shifts too large
to enumerate as an initial segment of the sequence.

### Remapping the accepted base without changing its values

The original order-$n$ rows are already strictly ordered by their factor
words. For each original factor, the module finds the first new carrier with
that prefix by binary search. The preceding extension argument guarantees
that such a carrier exists.

The old order and row indices remain unchanged. The row transformation is

$$
[\text{old carrier},\,D,\,\ell,\,c,\,r,\,i]
\longmapsto
[\text{new carrier},\,D,\,\ell,\,c,\,r,\,i].
$$

The same determinant string and four minor indices therefore keep exactly the
same meaning. Their occurrence witness changes to a witnessed occurrence of
the longer carrier; its prefix is still the original factor. No earliest-shift
claim is introduced.

The actual transport-integrity check compared all five retained cells in
every one of the 6,949 old rows and found exact equality. This compares saved
records; it evaluates no determinant and replays no mathematical proof.

## Exact calculation of only the new orders

For a factor $w=a_k\cdots a_{k+2n-2}$, the four required smaller factors
are the length-$(2n-3)$ windows beginning at offsets 0, 1 and 2 and the
length-$(2n-5)$ window beginning at offset 2. Their row indices are stored
as `left`, `center`, `right` and `inner`.

The classical Desnanot–Jacobi identity, specialized to a Hankel matrix, is

$$
H_n(k)H_{n-2}(k+2)
 =H_{n-1}(k)H_{n-1}(k+2)-H_{n-1}(k+1)^2.
$$

The two off-diagonal minors agree because the matrix is Hankel. For $n=2$,
the empty determinant is $H_0=1$, represented by the inner-row sentinel
$-1$. The new run begins at $n=33$, so that special case is not exercised.

At each new order, every numerator uses already retained complete rows. Every
denominator belongs to order $n-2$, whose all-shift nonzero property has
already been established by the source prefix or a completed new order.
The implementation performs two BigInt multiplications, one subtraction, an
exact remainder check and an integer division for each new factor. A nonzero
denominator and zero remainder are required before retaining the quotient.

Induction on the order now proves that the new records are the exact Hankel
determinants of their factors. Completeness of the factor language then gives
the all-shift conclusion. None of the 21,280 new determinants is zero.

The loop begins strictly after the supplied base order. It loads old decimal
values into BigInt for the smaller minors; that parsing is not determinant
evaluation. It never calls the original compiler and never derives an old
determinant again.

### First zero and incomplete outcomes

The module retains a complete first zero-containing order before stopping.
Its `first_zero` record then has `status: "found"`, the smallest zero order,
the first zero factor row encountered, its determinant, known occurrence and
minor references. Since every earlier order is complete and nonzero, order
minimality applies across all shifts. The occurrence is a witness, not an
earliest shift.

This conservative stop is part of the API contract. It makes no claim about
later orders. A complete zero-containing row can be calculated because its
denominators are in earlier nonzero orders. The actual order-64 run did not
exercise this branch.

An exception inside the extension work returns `status: "incomplete"`, the
stage and message, the complete prefix already retained and any partial new
order. A whole next order is preflighted against the total row cap before
its construction starts. Errors within a row can leave a partial order.

Input preflight occurs before the result object is created. Invalid input or
options therefore throw to the caller rather than returning a partial
extension. The caller must retain that failure separately. The recorded
preflight rejection below demonstrates this distinction.

For a no-zero result, `first_zero` follows the original compiler's convention:

```json
{
  "status": "none_in_completed_orders",
  "completed_through_order": 64,
  "requested_max_order": 64
}
```

## API

The module is plain CommonJS and performs no I/O. Its exports are:

| Export | Contract |
|---|---|
| `extendMorphicHankelIndex(input, {maxOrder})` | Structurally loads an established complete nonzero prefix and computes only strictly larger orders, up to the configured cap |
| `packMorphicHankelExtension(result)` | Copies the retained extension into an archive containing base orders and separate consecutive new-order blocks |
| `assembleMorphicHankelExtensionArchive(archive, blocks)` | Copies and joins the listed saved blocks into the original index schema; no determinant computation |
| `SCHEMA` | `commons.ppl036.morphic_hankel_extension/v1` |
| `INPUT_SCHEMA` | `commons.ppl036.morphic_hankel_index/v1` |
| `ARCHIVE_SCHEMA` | `commons.ppl036.morphic_hankel_extension_archive/v1` |
| `BLOCK_SCHEMA` | `commons.ppl036.morphic_hankel_order_block/v1` |
| `LIMITS` | Frozen structural and work bounds |

### Read the published result

The normal way to use this completed work is to assemble the published data
and open it in the existing saved reader. This example performs no extension:

```js
const fs = require('node:fs');
const {
  assembleMorphicHankelExtensionArchive,
} = require('./morphic_hankel_extension.cjs');
const {
  openMorphicHankelReader,
} = require('./morphic_hankel_reader.cjs');

const readJSON = name => JSON.parse(fs.readFileSync(name, 'utf8'));
const receipt = readJSON('order64_extension.json');
const blocks = receipt.block_files.map(part => readJSON(part.filename));

const index = assembleMorphicHankelExtensionArchive(
  receipt.extension,
  blocks,
);
const reader = openMorphicHankelReader(index);

const answer = reader.at({
  shift: 10n ** 700n + 1234567n,
  order: 64,
});
const page = reader.factorPage({order: 64, offset: 100, limit: 6});
const activity = reader.snapshot();
```

The filesystem lines show how a repository consumer can supply parsed files;
the module itself has no filesystem dependency. The recorded use in this
receipt supplied already retained objects in connected JavaScript. No native
process or filesystem command was invoked for the calculation.

The existing reader's `at` method accepts a nonnegative BigInt or a canonical
decimal string for the shift. It creates only the required sequence window,
finds its saved factor row and returns the saved determinant. Smaller orders
at the same shift reuse the window's prefix. `factorPage` returns complete
saved records for the selected order, including their occurrence and minor
references. See [the reader guide](RETAINED_READER_API.md) for its full contract.

### Extend a new established prefix

The constructor takes the index itself, not a receipt or archive wrapper.
Its only option is the required safe integer `maxOrder`. Unknown option fields
are rejected. The target must strictly exceed the complete base order and
must not exceed 64.

For example, the mathematical call used here was
`extendMorphicHankelIndex(originalReceipt.index, {maxOrder: 64})` with the pinned
order-32 source. That calculation has already been retained; the saved-reader
example above is sufficient to consume its results.

A different eligible complete source prefix can be used for genuinely new
extension work. Its exact source identity and proof must be established by
the caller. The loader checks:

- The index schema, seed and exact four-letter morphism.
- A declared complete nonzero base, with requested, completed and nonzero
  bounds equal.
- A `none_in_completed_orders` first-zero record with matching bounds.
- A complete factor language with the correct factor length, a power-of-two
  block size, matching substitution depth and sufficient block coverage.
- Bounded distinct pair records and their canonical occurrence strings.
- Four distinct saved letter images of the declared length and alphabet.
- Strictly ordered distinct carriers, valid occurrence strings and bounded
  pair/offset references.
- Contiguous complete base orders, ordered unique factor prefixes, row
  counts, bounded nonzero determinant strings and bounded minor references.
- Structurally consistent factor/sign-count declarations and determinant-size
  summaries.

The loader does not re-count signs from the saved determinant strings, verify
minor identities, regenerate source images, check pair closure or authenticate
occurrence arithmetic. These are retained-source premises. A fabricated but
structurally plausible index can supply false mathematical assertions.

Input is defensively copied using a bounded JSON-like traversal. Supported
values are null, booleans, strings, safe integers, arrays and plain objects.
Arbitrary functions, BigInts inside the snapshot, nonintegral numbers and
non-plain objects are rejected. The shift API of the separate reader can
accept BigInts; source snapshot values remain serializable primitives.

The final index retains no old query activity. Its `queries` array starts
empty; new saved-reader activity is recorded separately in the outer receipt.
This prevents an inherited query from being misrepresented as new work.

### Pack and assemble without re-evaluation

`packMorphicHankelExtension` accepts an extension result after the longer
factor language and the retained base prefix are complete. It copies the
result, keeps the base orders in the archive and partitions the new order
records into blocks of at most 16 consecutive orders.

Each block declares its schema, filename, base order, actual first/last order
and complete stored order records. The filename's upper endpoint describes
its planned block range; an early stop can leave fewer actual orders in that
block. The manifest gives the actual order range and count. Consumers should
use the manifest and records instead of inferring completeness from a filename.

`assembleMorphicHankelExtensionArchive` requires the exact number of blocks
listed in the manifest and their stated order. It checks the schemas, common
base order, unique matching filenames, contiguous ranges and record headers.
It requires all declared completed orders and permits at most one following
partial order, within the target. A declared complete archive must contain
every requested order. Missing, reordered or mismatching block descriptions
are rejected.

These are structural transport checks. The assembler does not hash files,
validate every determinant identity, independently establish nonzero values or
prove the completeness of supplied factor rows. Caller-established source
identity still matters. The existing saved reader performs its own bounded
structural load and lazy order indexing when the assembled index is opened.

The actual pack/assembly consumer compared the complete assembled index with
the retained extension index as serialized JSON and obtained exact equality.
That comparison covers all saved fields and rows without recalculating the
mathematics. Each block's formatted JSON was also parsed and compared with its
retained object before publication; only primitive-array whitespace was
compacted.

Packing and assembly make defensive copies. They do not stream an unbounded
archive from disk, supply a database, resume an interrupted calculation or
reconstruct omitted source data. The fixed-size order blocks make the stored
result convenient to publish and read; the complete in-memory index is still
assembled for the saved reader.

An incomplete result can be packed only after the full longer language and
entire retained base have been preserved. Failure before that point leaves
the separately retained extension/error as the available checkpoint. Nothing
in this API automatically retries a failed operation.

### Resource and shape bounds

| Bound | Value |
|---|---:|
| Maximum matrix order | 64 |
| Maximum carriers | 4,096 |
| Maximum total determinant rows | 32,768 |
| Maximum occurrence/shift decimal digits | 1,024 |
| Maximum absolute determinant decimal digits | 512 |
| Saved-reader page size | 64 |
| Saved-reader retained query count | 32 |
| New orders per archive block | 16 |
| Snapshot traversal nodes | 1,000,000 |
| Snapshot string and key characters | 16,000,000 |
| Snapshot nesting depth | 24 |

These are caps, not claims that all possible values under them were exercised.
The actual source has 6,949 rows; the complete result has 28,229. Its largest
carriers have length 127, and the actual largest absolute determinant at order
64 uses 41 decimal digits. No requested cap was raised for this result.

The initial bounded traversal limits copied structure and text. Later semantic
checks narrow the accepted representation. An input with cycles eventually
exceeds the traversal/depth bound; arbitrary object graphs are not a supported
snapshot format.

For $T$ retained rows, $R$ new rows, $C$ longer carriers, maximum factor
length $L$ and $W$ pair windows, the main new work is the bounded block
concatenation, $W$ window slices, sorting $C$ words, $T$ carrier searches,
the new-order prefix scans and $R$ exact recurrence evaluations. String
comparison/slicing cost depends on $L$, and BigInt cost depends on operand
size; the counter values are not constant-time cost claims.

The loader retains old values needed as minors and constructs ordered factor
maps. The result stores complete language and determinant data. Packing,
assembly and the saved reader add copies, so their memory use should not be
described as constant or as an out-of-core computation.

## Actual execution and results

The only mathematical extension began at **2026-10-04 17:46:11.225 UTC** with
the final module identity recorded above. It completed all requested orders
with `status: "complete"`, `completed_through_order: 64` and
`all_shifts_nonzero_through_order: 64`. Its single elapsed observation was
182 ms. This is not a benchmark or a comparative performance claim.

| Recorded extension work | Count |
|---|---:|
| Retained pair records loaded | 9 |
| Source pair-closure steps | 0 |
| Retained letter images loaded | 4 |
| Retained image characters loaded | 256 |
| Source block-reconstruction steps | 0 |
| New block-extension levels | 1 |
| New block concatenations | 4 |
| New block characters | 512 |
| Candidate pair windows | 1,170 |
| Distinct length-127 carriers | 882 |
| Retained determinants loaded | 6,949 |
| Retained determinants recomputed | 0 |
| Retained rows remapped | 6,949 |
| Carrier-search comparisons | 68,409 |
| New-order prefix candidates | 28,224 |
| New determinant evaluations | 21,280 |
| Condensation products | 42,560 |
| Condensation subtractions | 21,280 |
| Exact division checks | 21,280 |
| Integer divisions | 21,280 |

The 28,224 prefix candidates are 32 new-order scans across all 882 carriers.
They are not 28,224 distinct determinant rows. Each order's duplicate prefixes
are removed before its new records are evaluated.

The complete newly calculated order summaries follow. Counts include every
factor at the indicated order; the maximum digit count is for the absolute
determinant value.

| Order | Factors | Positive | Negative | Zero | Maximum digits |
|---|---:|---:|---:|---:|---:|
| 33 | 448 | 257 | 191 | 0 | 20 |
| 34 | 462 | 164 | 298 | 0 | 20 |
| 35 | 476 | 228 | 248 | 0 | 21 |
| 36 | 490 | 313 | 177 | 0 | 21 |
| 37 | 504 | 249 | 255 | 0 | 22 |
| 38 | 518 | 208 | 310 | 0 | 23 |
| 39 | 532 | 264 | 268 | 0 | 23 |
| 40 | 546 | 304 | 242 | 0 | 24 |
| 41 | 560 | 299 | 261 | 0 | 24 |
| 42 | 574 | 251 | 323 | 0 | 25 |
| 43 | 588 | 293 | 295 | 0 | 26 |
| 44 | 602 | 339 | 263 | 0 | 26 |
| 45 | 616 | 301 | 315 | 0 | 27 |
| 46 | 630 | 254 | 376 | 0 | 28 |
| 47 | 644 | 316 | 328 | 0 | 28 |
| 48 | 658 | 381 | 277 | 0 | 29 |
| 49 | 672 | 342 | 330 | 0 | 30 |
| 50 | 686 | 266 | 420 | 0 | 30 |
| 51 | 700 | 354 | 346 | 0 | 31 |
| 52 | 714 | 458 | 256 | 0 | 32 |
| 53 | 728 | 330 | 398 | 0 | 32 |
| 54 | 742 | 294 | 448 | 0 | 33 |
| 55 | 756 | 378 | 378 | 0 | 34 |
| 56 | 770 | 402 | 368 | 0 | 35 |
| 57 | 784 | 382 | 402 | 0 | 35 |
| 58 | 798 | 349 | 449 | 0 | 36 |
| 59 | 812 | 430 | 382 | 0 | 37 |
| 60 | 826 | 460 | 366 | 0 | 37 |
| 61 | 840 | 393 | 447 | 0 | 38 |
| 62 | 854 | 386 | 468 | 0 | 39 |
| 63 | 868 | 439 | 429 | 0 | 40 |
| 64 | 882 | 520 | 362 | 0 | 41 |

### Fresh saved-reader use

A fresh JavaScript context assembled the saved archive and opened the existing
reader once at **2026-10-04 17:46:55.604 UTC**. It used

$$
k=10^{700}+1{,}234{,}567
$$

and queried the two new orders below. The 701-digit decimal shift is fully
retained in the receipt.

| Order | Saved factor row | Exact determinant | Newly evaluated sequence symbols |
|---|---:|---|---:|
| 64 | 864 | `20098484369344395457588731642456240` | 127 |
| 48 | 646 | `-18928918251076846287675783` | 0 |

The order-48 query reused the length-95 prefix of the first query's saved
length-127 window. The following page request,
`{order:64, offset:100, limit:6}`, returned rows 100–105, reported 882 total
factors and next offset 106. Its six complete records are included in the
outer receipt, as are the two query results and all eight accessed source
records.

| Recorded reader work | Count |
|---|---:|
| Source carriers copied | 882 |
| Source determinant rows copied | 28,229 |
| Orders indexed | 2: orders 48 and 64 |
| Rows indexed | 1,540 |
| Order-map cache hits | 1 |
| Sequence windows created | 1 |
| Sequence windows extended | 0 |
| Window-prefix cache hits | 1 |
| Sequence symbols evaluated | 127 |
| Binary morphism transitions | 295,402 |
| Record reads / unique source records | 8 / 8 |
| Retained queries | 3 |
| Compiler calls | 0 |
| Determinant evaluations | 0 |
| Factor-language expansions | 0 |

The one reader-use elapsed observation was 48 ms. It includes the recorded
reader activity and is not a benchmark. Assembly, formatting and identity
comparison were separate from determinant calculation.

### The rejected preflight remains visible

There were two invocations of the extension entry point across source
development, but only one mathematical extension.

At **2026-10-04 17:44:15.910 UTC**, unpublished candidate blob
`daafb439f4fcd832544516047ca5983e20ae90b5` incorrectly required
`first_zero === null`. The accepted source instead contained

```json
{
  "status": "none_in_completed_orders",
  "completed_through_order": 32,
  "requested_max_order": 32
}
```

The candidate threw `A declared complete nonzero base prefix is required`
during `loadBase`, before block construction, row remapping or determinant
evaluation. No extension-result object had been created.

The source was explicitly corrected to accept the existing status record with
matching bounds. The returned no-zero/found records and carrier-column naming
were also aligned with the accepted compiler conventions before calculation.
The mathematical recurrence and source-reuse algorithm did not change.

The subsequent successful invocation used the final source identity
`299a776c53ab80c62426524ac3ba7689a75374c9`. Its source remained unchanged after
the calculation. The receipt preserves the first attempt's timestamp, candidate
identity, exact error, observed source record and zero-work disposition. The
failed attempt is not hidden inside a claim of a single entry-point invocation.

### Verification scope

The retained evidence consists of:

- One rejected structural preflight followed by the explicit source correction.
- One successful new-order calculation and one packing call.
- One fresh assembly call, with exact complete-index transport equality.
- Exact equality of all five retained determinant/minor cells in all 6,949
  base rows.
- One saved-reader open, two new large-order lookups and one factor page.
- Complete source, data and query objects, serialized without dropped rows.

No original compiler call, accepted determinant replay, source pair-closure
recalculation or earlier substitution reconstruction occurred. No native
process, network lookup, fixture suite or workflow was used to execute the
calculation. The result is ordinary JavaScript and BigInt work using retained
input objects.

Other base sizes, target sizes, malformed-input branches, zero-finding branches
and runtime cap/error paths were inspected in source only. The recorded
preflight failure is the only exercised invalid-input path. No generic
acceptance or coverage claim is inferred from source inspection.

The theorem depends on the accepted source proof and the exact computation
described above. It is not an independent determinant implementation, a
machine-checked formal theorem or an authentication mechanism.

## Mathematical context and attribution

Shallit's [2014 talk, Problem 9](https://cs.uwaterloo.ca/~shallit/Talks/bc4.pdf)
gives the four-letter fixed point and the all-order Hankel nonvanishing
question. The [author's updates](https://cs.uwaterloo.ca/~shallit/talks.html)
supply context; statements about other numbered problems should not be
transferred to this one. The present result is stated solely for the retained
orders through 64, without asserting a complete current literature survey.

The determinant identity is classical. Dodgson condensation and number-wall
methods provide context; see Lunnon's
[The Number-Wall Algorithm: an LFSR Cookbook](https://cs.uwaterloo.ca/journals/JIS/VOL4/LUNNON/numbwall10.pdf).
The recurrence is not presented as a new discovery. The pair-coverage,
occurrence and automatic-sequence lookup arguments used by this repository
are given in [HANKEL_INDEX_API.md](HANKEL_INDEX_API.md).

The new capability is a reusable incremental extension and a complete saved
archive that existing readers can consume. Its record of what was inherited,
what was newly computed, and what failed before computation is part of the
deliverable.
