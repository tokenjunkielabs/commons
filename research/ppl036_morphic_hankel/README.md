# PPL036: Hankel determinants at every shift

For the fixed point of $1\mapsto12$, $2\mapsto23$, $3\mapsto14$ and
$4\mapsto32$, the complete retained calculation establishes

$$
\det(a_{k+i+j})_{0\le i,j<n}\ne0
\qquad\text{for every }k\ge0\text{ and }1\le n\le64.
$$

There are 28,229 exact determinant records. The incremental extension reused
the 6,949 accepted records through order 32 and computed 21,280 new records for
orders 33–64. Its 882 length-127 factor carriers cover all nonnegative shifts.
Matrix order remains bounded by 64; no all-order result or novelty is claimed.

| File | Contents |
|---|---|
| [morphic_hankel_index.cjs](morphic_hankel_index.cjs) | Original bounded BigInt compiler, large-shift lookup and factor pagination |
| [HANKEL_INDEX_API.md](HANKEL_INDEX_API.md) | Original complete coverage proof, determinant identity and provenance |
| [order32_all_shifts.json](order32_all_shifts.json) | Unchanged original language, 6,949 determinant rows, minor references and actual queries |
| [morphic_hankel_reader.cjs](morphic_hankel_reader.cjs) | Unchanged saved-table reader, lazy order maps and reusable shift windows |
| [RETAINED_READER_API.md](RETAINED_READER_API.md) | Saved-reader contract and its original actual-use evidence |
| [retained_reader_queries.json](retained_reader_queries.json) | Original three fresh large-shift results, page and accessed records |
| [morphic_hankel_extension.cjs](morphic_hankel_extension.cjs) | Incremental extension, order-block packing and saved assembly |
| [INCREMENTAL_EXTENSION_API.md](INCREMENTAL_EXTENSION_API.md) | Extension proof, complete API contract, limits and execution evidence |
| [order64_extension.json](order64_extension.json) | Complete longer language, remapped base, manifest, provenance and new reader queries |
| [orders33_48.json](orders33_48.json) | All 8,848 new determinant records for orders 33–48 |
| [orders49_64.json](orders49_64.json) | All 12,432 new determinant records for orders 49–64 |

## Read the completed order-64 result

Parse the outer receipt and its two order-block files. Pass the receipt's
`extension` member and the parsed blocks to
`assembleMorphicHankelExtensionArchive`, then open the returned index with
`openMorphicHankelReader`. The archive's `index` alone contains only remapped
base orders and is not the complete order-64 table. The
[incremental guide](INCREMENTAL_EXTENSION_API.md) gives a complete example.

The recorded fresh reader queried $k=10^{700}+1{,}234{,}567$:

| Order | Exact saved determinant |
|---|---|
| 64 | `20098484369344395457588731642456240` |
| 48 | `-18928918251076846287675783` |

The smaller query reused the first query's sequence window. A six-row factor
page reused the order-64 map. The reader copied all 28,229 source rows but
indexed only 1,540 rows for the two requested orders. It performed zero
compiler calls, determinant evaluations or factor-language expansions.

The extension grew the four retained length-64 letter images to length 128
with four concatenations, used the retained nine-pair closure and enumerated
1,170 windows to obtain the complete longer carrier language. It changed only
the carrier-witness index in each old row; all old determinant strings and
minor references remained exact. Its first unpublished preflight rejected the
source's existing no-zero status-record shape before any mathematical work.
The correction and both attempt records remain visible in the receipt.

Structural loading and saved assembly do not authenticate source data or
re-prove its mathematics. The complete proof, exact source identities, work
counters and full rows are retained. Reading the published data requires no
new extension or original compiler invocation.

## Original order-32 calculation and reader

The adjacent-pair closure has nine pairs. Their substitution images produce 594
windows and the complete 434-factor language of length 63. Every shorter factor
extends to one of these carriers, making the finite table applicable to all
nonnegative shifts.

After the one compiler invocation, an order-32 lookup at shift $10^{100}$ returned

$$
H_{32}(10^{100})=45\,168\,038\,832\,870.
$$

The determinant count stayed at 6,949 throughout that lookup and an eight-row
factor page. Reading the published JSON retrieves the already computed records
without running the constructor.

The separate saved-table reader opens the published `index` without loading the
compiler. Its one recorded use queried $k=10^{500}+12345$ at orders 32, 16 and 8,
returning respectively $-4{,}686{,}314{,}378{,}119$, $35{,}361{,}608$ and $1{,}751$.
It copied all 6,949 source rows but indexed only the 742 rows for those orders.
The two smaller queries reused the first query's 63-symbol window; a subsequent
six-row factor page reused the order-32 map. There were zero compiler calls,
determinant evaluations or factor-language expansions. Its validation is
structural only; the mathematical proof and original table remain the sources
for the all-shifts claim. The original compiler API and separate saved-reader
API are documented in their respective guides.

The original compiler API accepts maximum orders 1–64 with explicit carrier, row, page, query and
shift-digit caps. A complete first zero row would be retained with occurrence
witnesses, and construction would stop. At that original stage, other orders and error/limit paths were
inspected in source only. The separate retained extension above subsequently
computed orders 33–64.

The exact problem is Shallit's
[2014 Problem 9](https://cs.uwaterloo.ca/~shallit/Talks/bc4.pdf);
[current author updates](https://cs.uwaterloo.ca/~shallit/talks.html) and
[Lunnon's number-wall paper](https://cs.uwaterloo.ca/journals/JIS/VOL4/LUNNON/numbwall10.pdf)
provide context. Classical determinant methods are credited. No novelty, full
all-order result, prize eligibility or sponsor acceptance is asserted.

Operation: `MORPHIC-HANKEL-ALLSHIFTS-20261004-7CA6`.
[Original claim](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1791130082676129).

Saved-reader operation: `MORPHIC-HANKEL-READER-20261004-7CA6`.
[Reader claim](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1791131641067779).

Incremental-extension operation: `MORPHIC-HANKEL-EXTEND64-20261004-7CA6`.
[Extension claim](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1791134909002389).
