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

The API accepts maximum orders 1–64 with explicit carrier, row, page, query and
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
