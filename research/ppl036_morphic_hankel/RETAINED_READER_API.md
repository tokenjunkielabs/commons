# Saved-table reader for PPL036

The separate `morphic_hankel_reader.cjs` module opens the published determinant table and answers new shift and factor-page queries. It never imports the compiler, reconstructs the factor language or evaluates a determinant. Opening copies the bounded source records; lookup maps are built only for requested orders, and queries at the same shift share a symbol window.

The first actual consumer, recorded at **2026-10-04 16:39:28.495 UTC**, opened the previously published order-32 table once. At the new shift $k=10^{500}+12345$, it obtained:

| Order $n$ | Stored factor row (zero based) | Stored $H_n(k)$ | Newly evaluated sequence symbols |
|---:|---:|---:|---:|
| 32 | 244 | -4,686,314,378,119 | 63 |
| 16 | 115 | 35,361,608 | 0 |
| 8 | 52 | 1,751 | 0 |

A subsequent order-32 page returned rows 120–125, with next offset 126 and 434 total factors. The complete responses, nine accessed source records, cached window and operation counts are in [retained_reader_queries.json](retained_reader_queries.json). Reading that JSON retrieves these already computed results.

## Source identity and mathematical scope

This consumer used [order32_all_shifts.json at the original merge](https://github.com/woahwhattheheck/commons/blob/ba8410152d8ef18b3aa8e96c0c08c774cb8feea6/research/ppl036_morphic_hankel/order32_all_shifts.json), published by [PR #31364](https://github.com/woahwhattheheck/commons/pull/31364).

| Source item | Exact identity |
|---|---|
| Repository | `woahwhattheheck/commons` |
| Original merge | `ba8410152d8ef18b3aa8e96c0c08c774cb8feea6` |
| Original dataset Git blob | `bee379d4292f123599fe26ca88ab6056ee8d62c0` |
| Original compiler Git blob | `fe1e7493dfe37606d0bf4c1a7ba643cb02dbeb70` |
| This reader Git blob | `0a231ad081144212eaa8a9d143398f5e7c31c3be` |
| Original calculation time | 2026-10-04 16:13:56.302 UTC |

The identity basis is the complete merged-file and literal-main readbacks retained from that publication. Those accepted source calculations were not replayed for this reader.

The source uses the fixed point $a=\mu^\infty(1)$ of

$$
\mu(1)=12,\quad \mu(2)=23,\quad \mu(3)=14,\quad \mu(4)=32
$$

and $H_n(k)=\det(a_{k+i+j})_{0\le i,j<n}$. Its [original proof and compiler contract](HANKEL_INDEX_API.md) explain the complete factor coverage and exact determinant calculation establishing $H_n(k)\ne0$ for every $k\ge0$ and $1\le n\le32$. The reader carries that bounded-order claim as source metadata; opening a table does not prove it. No all-order conclusion, novelty, prize eligibility or sponsor acceptance follows from this new reader.

The compiler module retains its original in-memory API and has no restoration/import function. This additional module provides a separate API for recorded tables. Neither the original compiler, original guide nor original dataset is changed.

## Minimal use

The following calls describe the consumer already recorded in the adjacent JSON. They do not require loading the compiler.

```js
const saved = require('./order32_all_shifts.json');
const {
  openMorphicHankelReader,
  LIMITS,
  SCHEMA,
  INPUT_SCHEMA,
} = require('./morphic_hankel_reader.cjs');

const reader = openMorphicHankelReader(saved.index);
const shift = 10n ** 500n + 12345n;

const order32 = reader.at({shift, order: 32});
const order16 = reader.at({shift, order: 16});
const order8 = reader.at({shift, order: 8});
const page = reader.factorPage({order: 32, offset: 120, limit: 6});

const state = reader.summary();
const receipt = reader.snapshot();
```


The module contains plain JavaScript, has no imports and performs no file, network or process operations. File loading in the example belongs to the caller. The retained actual consumer evaluated the CommonJS module in the connected JavaScript environment; no native executor or alternate runtime was requested.

Exports are:

| Export | Meaning |
|---|---|
| `openMorphicHankelReader(snapshot)` | Copy and structurally load a compiler snapshot; return a reader |
| `SCHEMA` | `commons.ppl036.morphic_hankel_reader/v1` |
| `INPUT_SCHEMA` | `commons.ppl036.morphic_hankel_index/v1` |
| `LIMITS` | Frozen caps shown below |

The reader object exposes `schema`, `at`, `factorPage`, `summary` and `snapshot`. It is frozen; its closure owns the mutable caches. Source arrays are copied into bounded primitive records and returned structures are cloned, so later caller mutation of those input or output records does not mutate the reader's retained tables or query history.

## Opening a saved table

Pass the original artifact's `index` member, not its outer receipt. The loader accepts the exact source schema, seed `'1'` and four literal morphism mappings.

The source must declare requested order 1–64 and a nonempty completed prefix through an order no greater than the requested order. Its nonzero bound must lie between zero and the completed bound. Accepted declared statuses are `complete`, `counterexample_found` and `incomplete`. A complete status requires requested, completed and nonzero bounds to agree; a counterexample-found status requires the declared nonzero bound to be one less than the completed bound. These checks establish consistency of declarations, not their mathematical truth.

The factor language must declare `complete: true`, maximum factor length $2N-1$, a block size equal to $2^q$, and block coverage $2^q\ge2N-2$. Substitution depth is 0–7 and block size is 1–128. The recorded pair list contains 1–16 unique two-symbol tokens over 1–4. Carrier rows contain exactly a word, decimal occurrence, pair index and offset. The loader checks fixed word length, alphabet, strict lexicographic order, canonical nonnegative occurrence decimals, pair-index bounds and offsets inside the recorded pair block.

For each order in the completed prefix, the order number, factor length and complete flag must agree. Each order has 1–carrier-count rows and each row has exactly six bounded primitive cells. All copied rows count against the total row cap. Extra source orders beyond the completed prefix are counted in metadata and ignored.

Opening does **not** index every order. On the first query for an order, its map builder checks carrier indices, canonical signed determinant strings, appropriate null/empty/prior-order minor-reference bounds, and strict lexicographic uniqueness of the factors reconstructed from carrier prefixes. Only successful maps are cached.

These checks are deliberately structural. They do not authenticate a file, verify occurrence arithmetic or pair closure, prove factor completeness, check the determinant recurrence, confirm that referenced minors represent the intended factors, or re-establish the declared nonzero bound. Even after one successful query, copied rows in other unindexed orders have not received that order-map validation. Use the pinned source and its proof when mathematical provenance matters.

## Query API

### `at({shift, order})`

Both fields are required and unknown query fields are rejected. Order is a safe integer from 1 through the source's completed prefix. Shift is either a nonnegative BigInt or a canonical decimal string with at most 1,024 digits. Number-valued shifts, a leading plus sign, leading zeroes except `'0'`, exponent notation and whitespace are rejected.

The reader indexes the requested order if necessary, obtains the factor of length $2n-1$ starting at the requested shift, and looks it up. The fixed-point navigation uses

$$
a_{2t+d}=\mu(a_t)[d],\qquad d\in\{0,1\}.
$$

Each newly needed sequence position is read as a binary integer from most significant bit to least, starting in state 1. This is the same symbol relation justified in the original proof; the reader does not expand the prefix up to the shift.

A window is keyed by the canonical decimal shift. An equal or smaller requested length reuses its prefix. A larger requested length extends only the missing tail. Different shifts have separate windows; overlapping positions across different shift keys are not shared.

A successful result has `status: 'found'`, the canonical shift, order, exact factor, zero-based factor row, determinant decimal string, `reused_determinant: true`, new-symbol count, source-record key and complete accessed source record. No determinant arithmetic occurs. In the actual three-query sequence, the first call evaluated 63 symbols and the next two needed none.

### `factorPage({order, offset = 0, limit = 16})`

Order is required. Offset is a safe integer from zero through the order's row count, inclusive; limit is a safe integer from 1 through 64. Explicit null values are not defaults. Unknown fields are rejected.

The response includes the requested bounds, all returned source records, returned count, total factor count and `next_offset`. The latter is null at the end. Offset equal to the row count yields an empty terminal page. Records follow the source's strictly lexicographic factor order and keep their source row numbers.

The first page for an order builds that order's map if needed. A page for an already indexed order reuses it. Pagination performs no sequence-symbol or determinant evaluation. The actual page reused the order-32 map.

### Source records and references

A record key is the string `order:row`. Each record contains:

| Field | Meaning |
|---|---|
| `order`, `row`, `carrier` | Source order and zero-based source indices |
| `factor`, `determinant` | Carrier prefix and exact recorded determinant decimal |
| `source_occurrence` | Recorded occurrence shift, pair index/token, block offset and substitution depth |
| `minor_rows` | Left/center/right references to order $n-1$, and inner reference to order $n-2$ |

The occurrence is a source witness for the factor, not the requested large shift and not a claim of earliest occurrence. Order-one minor references are null. For order two, the inner reference is -1 for the empty determinant. Higher-order references are zero-based rows in the indicated source order. The original table remains necessary to follow references to records not accessed by the reader.

### `summary()` and `snapshot()`

Summary returns copied source declarations, `validation: 'structural_only'`, counters, sorted indexed orders, cached-shift count and retained-query count. Source mathematical claims remain explicitly attributed to the input.

Snapshot adds limits, complete fresh query records, all distinct accessed source records, and full cached windows. It contains the new reader's activity rather than the original compiler's query history. It does not embed the entire source table and is not a replacement for that table. This module provides no function to restore a reader from its own snapshot.

Successful and failed retained query records are sequentially numbered from 1. Input validation and the query-cap check happen before a query is retained. Once reserved, a query that later fails is retained with `status: 'incomplete'` and an error string before the exception is rethrown. Earlier completed work remains available through summary and snapshot. An unsuccessful order-map build is not cached. The caller chooses any later action; the module never invokes the compiler as a fallback.

## Caps and bounded work

| Item | Cap |
|---|---:|
| Requested/source order | 64 |
| Carrier rows | 4,096 |
| Total copied determinant rows | 32,768 |
| Decimal digits in a supplied shift or source occurrence | 1,024 |
| Decimal digits in a stored determinant, excluding sign | 512 |
| Rows per factor page | 64 |
| Fresh retained queries | 32 |

All queries must also fit the loaded source's completed bound. For this input that bound is 32. At most 32 shift windows can be created; a window has at most 127 symbols under the global order cap. The query and page caps also bound record accesses. No automatic widening, hidden rebuild, background work or restart occurs when a cap is reached.

Opening is linear in copied source rows and carriers. Additional map work is proportional to the rows of each newly requested order. A fresh window of length $L$ at shift $k$ evaluates $L$ symbols with binary navigation proportional to the bit lengths of $k$ through $k+L-1$. A shorter query at the same shift avoids those new symbol evaluations. These are algorithmic descriptions, not runtime guarantees.

## Actual use and evidence limits

The one recorded consumer made one open, three shift queries and one page query. It retained the following counters:

| Measure | Actual value |
|---|---:|
| Carrier rows copied | 434 |
| Determinant rows copied | 6,949 |
| Orders/rows indexed immediately after opening | 0 / 0 |
| Final indexed orders | 8, 16, 32 |
| Final indexed rows | 742 = 98 + 210 + 434 |
| Reuses of an existing order map | 1 |
| Windows created / extended | 1 / 0 |
| Window-prefix cache hits | 2 |
| New sequence symbols | 63 |
| Binary transition steps | 104,643 |
| Record reads / distinct records | 9 / 9 |
| Compiler calls | 0 |
| Determinant evaluations | 0 |
| Factor-language expansions | 0 |
| Retained queries | 4 |

The opened summary, all three answers, full six-row page and final snapshot are saved together with the source identity and execution time. The single observed elapsed time was **16 ms**. It is one actual use, not a benchmark series or a throughput promise.

Only the specified successful input and calls were executed. Larger-window extension, alternate source statuses, invalid input, missing factors, malformed rows and cap/error paths were inspected in source only. No extra fixtures, tests, source-calculation replay or verification-only computation was added.

Operation: `MORPHIC-HANKEL-READER-20261004-7CA6`.
[Original reader claim](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1791131641067779).
