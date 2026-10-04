# PPL036: Hankel determinants at every shift

For the fixed point of $1\mapsto12$, $2\mapsto23$, $3\mapsto14$,
$4\mapsto32$, the complete retained calculation establishes

$$
\det(a_{k+i+j})_{0\le i,j<n}\ne0
\quad\text{for every }k\ge0\text{ and }1\le n\le32.
$$

The 6,949 exact determinant records cover every shift through a proved complete
factor language. Matrix order remains bounded by 32; this does not solve the
all-order nonvanishing question.

| File | Contents |
|---|---|
| [morphic_hankel_index.cjs](morphic_hankel_index.cjs) | Bounded BigInt compiler, large-shift lookup and factor pagination |
| [HANKEL_INDEX_API.md](HANKEL_INDEX_API.md) | Complete coverage proof, determinant identity, API contract and provenance |
| [order32_all_shifts.json](order32_all_shifts.json) | All factor carriers, pair coverage, 6,949 determinant rows, minor references and actual queries |
| [morphic_hankel_reader.cjs](morphic_hankel_reader.cjs) | Separate reader for saved tables, lazy order maps and reusable shift windows |
| [RETAINED_READER_API.md](RETAINED_READER_API.md) | Saved-reader contract, exact source identity and actual-use evidence |
| [retained_reader_queries.json](retained_reader_queries.json) | Three fresh large-shift results, a six-row page and all accessed source records |

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
witnesses, and construction would stop. Other orders and error/limit paths were
inspected in source only.

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
