# A Hard Count: complete finite tables and an index of written cells

Operation: `KIMBERLING122-HARD-COUNT-INDEX-20261004-7CA6`  
[Original claim](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1791153794614419)

The delivered record contains **128 complete generated tables, every one of the
65,227 written cells, and all 623 distinct values that occur in those cells**.
Its positive integer coverage is exactly an initial interval through 518,
followed by the first missing value 519. The largest written value is 714.
Every occurrence position is saved. The data contains the complete tables and
index, rather than a selected list of observed values.

The new module constructs a bounded prefix, resumes that exact prefix in a
fresh session, and provides direct navigation of the saved record. The actual
continuation preserved all 54 earlier tables, all 8,039 earlier occurrence
positions, and the earlier session literally. A third session answered 19
queries without constructing a table, applying a recurrence step, or rebuilding
the occurrence index.

## Files and identities

| File | Purpose | UTF-8 bytes | Git blob SHA-1 |
|---|---|---:|---|
| `hard_count.cjs` | Public constructor, continuation and saved navigation | 41,989 | `8b58d5a5a674172ad9cf1eae2e8c89bea30dea1f` |
| `one_seed_history.json` | Entire retained history and execution receipts | 928,401 | `76fe7df3a3c4f1c5f01d0edeb5f562e150d2e3bf` |
| `HARD_COUNT_API.md` | Mathematical interpretation, API, limits and evidence | — | Published with the contribution |
| `README.md` | Entry point and principal findings | — | Published with the contribution |

The source was frozen before its first construction and remained unchanged.
The data formatting preserves every parsed value and array order. Primitive
arrays are packed across readable lines; no position, count, table or query
receipt is omitted.

## Original problem and reward boundary

Clark Kimberling's [primary page, section 4](https://faculty.evansville.edu/ck6/integer/unsolved.html)
attributes the special problem to Crux Mathematicorum Problem 2386 (1998).
Start with one written 1. Repeatedly write a table giving the cumulative count
of every value already written. The question asks whether all positive
integers eventually appear, also allowing an arbitrary initial positive
counting table with distinct bottom labels.

That page's January 2025 notice makes subsequent rewards donations to OEIS in
the solver's name. This finite computation is neither a solution submission
nor a direct cash award claim. No sponsor was contacted. The author’s
problem is credited; the bounded engine, complete occurrence data and saved
navigation are this contribution.

## What is being counted

A cell containing `156` contributes **one occurrence of the integer 156**.
It does not contribute 156 copies of another value, and the decimal digits
`1`, `5` and `6` are not separate objects.

Write `C_t(x)` for the frequency of the positive integer `x` after the seed
and `t` complete generated tables. Let

$$
D_t=\{x:C_t(x)>0\},\qquad
M_t=\sum_{x\geq1}C_t(x).
$$

The next table has one column for each member `y` of `D_t`. Its top cell is
`C_t(y)` and its bottom cell is `y`. All top cells are determined from the
same complete previous frontier. Appending one top cell must not change the
input used to determine another top cell in that same table.

For every positive integer `x`, the exact update is

$$
C_{t+1}(x)
=
C_t(x)+\mathbf1_{\{x\in D_t\}}
+\bigl|\{y\in D_t:C_t(y)=x\}\bigr|.
$$

The indicator accounts for the bottom row. The final term counts top-row
**multiplicity**: several existing labels can have equal frequencies and
therefore write the same count value several times.

Consequently,

$$
D_{t+1}=D_t\cup\{C_t(y):y\in D_t\},
\qquad
M_{t+1}=M_t+2|D_t|.
$$

Support never shrinks, and each previously present value gains at least one
occurrence in every complete round.

### The special seed and the general table

The actual input is `{kind:"one"}`: a single cell, so `C_0(1)=1` and `M_0=1`.
The first generated table has two cells. Treating that first table as the seed
would shift all subsequent round numbers and positions.

The general input has positive rows `a_1,...,a_n` and `b_1,...,b_n`, with
distinct `b_i`. This API uses the explicitly **physically written** initial
table:

$$
C_0(x)=|\{i:a_i=x\}|+|\{i:b_i=x\}|,\qquad M_0=2n.
$$

Repeated top-row values and overlaps between rows contribute separately.
A value occurring only in the top row is already in the initial support.
The API does not postulate an additional unprinted multiset containing
`a_i` copies of `b_i`. This interpretation is visible in the input and guide;
only the special one-cell seed was executed in this delivery.

## Serialization and positions

Generated columns use increasing **numerical** label order. Values are
canonical positive decimal strings. Length followed by lexicographic order
compares them exactly without converting a large initial label to a floating
point number.

The written stream is serialized as follows:

1. Include the complete seed at positions starting with zero. For a general
   seed, preserve the supplied column order and write its entire top row,
   followed by its entire bottom row.
2. For each generated table, write the entire count row in increasing label
   order, followed by the aligned entire label row.
3. Continue with the next complete table.

A generated table of width `d` starting at position `s` occupies the
half-open interval `[s,s+2d)`. Column `j` has its count at `s+j` and its
label at `s+d+j`. The serialization chooses an address convention; changing
the order of already fixed cells would not change the complete-round
frequency recurrence.

The next example is an actual saved query, not a second construction.
Table 4 has labels `[1,3,4]` and counts `[6,2,1]`. Its count cells are at
positions 9, 10 and 11, and its label cells are at 12, 13 and 14. The next
complete frontier starts at position 15.

An occurrence query can end inside a table. Such a stream prefix has a
well-defined frequency, but it is **not** a complete-round input from which
the same table should be generated again.

## An elementary infinite-process consequence

For any permitted nonempty seed, an indefinitely continued process has
unbounded support.

Suppose instead that all values ever written belonged to a finite set with
largest member `K`. Choose any value `y` in the initial support. Its bottom
label is written in every subsequent table, so

$$
C_t(y)\geq C_0(y)+t.
$$

Eventually this frequency exceeds `K`. The next count row writes that
frequency as a value, contradicting the assumed upper bound on all written
values. Thus infinitely many distinct values appear, with unbounded maximum.

This argument does not establish that every positive integer occurs.
An unbounded set of positive integers may have gaps. The delivered finite
record supplies first appearances and absences inside its explicit endpoint;
it gives no permanent-absence certificate for 519 or any other missing value.

## Actual construction and continuation

The requested work and its actual stopping points are retained separately.

| Stage | Requested additional tables | New-token allowance | Actual new tables | Total tables | Total written cells | Distinct values | Complete positive prefix |
|---|---:|---:|---:|---:|---:|---:|---:|
| Constructor | 0 | — | 0 | 0 | 1 | 1 | 1 |
| First advance | 64 | 8,192 | 54 | 54 | 8,039 | 185 | 155 |
| Fresh continuation | 202 | 65,536 | 74 | 128 | 65,227 | 623 | 518 |

The first call stopped with `new_token_budget`. After its 54 completed
tables, another table needed 370 cells, which did not fit the remaining
per-call allowance. No part of that next table was written.

The fresh continuation loaded the saved 54-table record, then appended 74 new
tables. It stopped with `total_token_limit`. The module permits at most
65,536 written cells. At the actual endpoint 309 slots remain, while the next
table needs `2*623=1,246` cells. The intended 256-table target was therefore
not reached. Tables 129 through 256 were neither constructed nor described
as completed.

Table 128 itself has 616 columns and writes 1,232 cells at
`[63995,65227)`. It introduces seven new values, leaving 623 values in the
next frontier. The last recorded token, position 65,226, is the bottom
label 705. The largest value written anywhere is 714; the current frequency
of value 1 is 720. A current frequency need not already have been printed as
a value.

### Retained continuation custody

Literal comparisons of already retained data established all of the following:

- The original input and seed-token IDs remained unchanged.
- The earlier 185 dictionary entries retained their values and first-appearance
  metadata exactly.
- All 54 earlier tables remained literally identical.
- Every one of the earlier 8,039 occurrence positions remained an identical
  prefix of its corresponding occurrence list.
- The original session and its first advance receipt remained identical.
- Table 55 used exactly the saved 54-table label order and frequency vector
  as its frozen input.
- The third session's queries left the entire 128-table core and both previous
  sessions literally unchanged.

These were comparisons of retained values. They did not construct old tables
again or recalculate the source recurrence.

## Findings available from the saved index

At table 54, value 156 was absent. The final record locates its first
appearance at position **13,567**, in table **68**, count-column **22**:
the existing label **23** had count 156. The same table also writes 156
as the count for label 25 at position 13,569. The completed record contains
89 occurrences of 156.

Value 518 first appears at position **41,152**, in table **107**, as the
count for label 2. It has 24 occurrences at the endpoint. Its early appearance
does not imply that every smaller value had already appeared then: the complete
positive prefix reaches 518 at table 125, after filling earlier gaps.

The occurrence at zero-based rank 100 in the list for value 1 is at position
**1,861**, table **30**, count-column **76**, for label **95**. A subsequent
strict-prefix rank query at position 1,861 returns 100.

Two independent saved access paths expose the 54-table boundary: `countAt`
reads 222 from the next table's stored input, while occurrence ranking before
position 8,039 also returns 222. Neither query generates a historical table.
At table 128, the final frequency for value 1 is 720.

The first four new values in the resumed table 55 are 222, 195, 179 and 170,
in discovery order. Their corresponding old labels are 1, 3, 4 and 6.
Discovery order and numerical order are distinct, and the API states which
one each page uses.


## Public API

The CommonJS exports are `SCHEMA`, `LIMITS`, `createHardCount` and
`openHardCount`. There are no package dependencies, filesystem operations,
network operations, random choices or clocks inside the module. The caller
chooses how to load and save its plain JSON snapshots.

Both factories return a frozen facade over private copied data. Returned
summaries, pages, receipts and snapshots are separate JSON copies. Modifying
a returned object cannot alter the retained record.

### Create a finite prefix

```js
const { createHardCount } = require("./hard_count.cjs");

const run = createHardCount({
  source_id: "my-hard-count-prefix",
  seed: { kind: "one" }
});

const progress = run.advance({
  tables: 64,
  max_new_tokens: 8192
});

const saved = run.snapshot();
```

`source_id` is a nonempty string of at most 512 UTF-16 code units. It is
caller provenance, not authentication.

A general initial table uses:

```js
seed: {
  kind: "written_counting",
  counts: ["3", "5"],
  labels: ["2", "7"]
}
```

This illustrates the input shape; it was not an executed second seed. It
means four physically written cells, in order `3,5,2,7`. Both arrays must
have the same width from 1 through 32, all values must be positive, and
bottom labels must be distinct. Values normalize to canonical decimal
strings without leading zeroes. Positive safe integer inputs are also
accepted and converted exactly.

### Resume a saved prefix

```js
const { openHardCount } = require("./hard_count.cjs");
const resumed = openHardCount(saved);

const progress = resumed.advance({
  tables: 202,
  max_new_tokens: 65536
});
const continued = resumed.snapshot();
```

`openHardCount` defensively copies the supplied record, checks its structure
and index bindings, and appends a new session. It does not call the
constructor or regenerate existing tables.

`advance` always requires both fields. `tables` is the maximum additional
number of complete tables for that call; `max_new_tokens` is its allowance
for newly written cells. This allowance is separate from the fixed global
limits. A table is started only if its complete two rows fit.

| `advance.status` | Meaning |
|---|---|
| `requested_tables_complete` | The requested additional tables were constructed |
| `new_token_budget` | The next whole table would exceed this call's new-token allowance |
| `total_token_limit` | The next whole table would exceed the module's global written-token limit |
| `total_table_limit` | The module's global table limit was reached |

A resource stop can return zero new tables. It is a completed, retained call
with an unchanged mathematical frontier. Raising the next call's allowance
can continue a per-call stop when global space remains. The delivered final
record has insufficient global space for another table under this source;
opening more sessions does not increase that capacity.

An advance stages a private copy of the current core, appends only new
tables to that copy, and commits the complete result and its receipt
together. It reuses the transaction's value map when committing. The
earlier core copy costs time and memory proportional to the retained
prefix; this module does not describe resumption as constant time.

### Open the delivered evidence file

```js
const evidence = require("./one_seed_history.json");
const { openHardCount } = require("./hard_count.cjs");

const reader = openHardCount(evidence.record);
const first156 = reader.firstAppearance({ value: "156" });
const positions = reader.pageOccurrences({
  value: "156",
  offset: 0,
  limit: 8
});
```

The top-level evidence envelope is separate from the public core schema.
Pass `evidence.record` to `openHardCount`.

### Saved navigation methods

Every retained method returns a reference
`{session_id,event_id}` and its `query_work`. Array offsets, ranks, columns
and written positions are zero based. Generated table numbers are one based.
The special seed is frontier/table number zero.

All page calls require explicit `offset` and `limit`. Limits range from
1 through 64; offsets range from 0 through 65,536. An offset beyond the
available records returns an empty page. `next_offset` is null at the end.

| Method and required arguments | Result and interpretation |
|---|---|
| `pageTables({offset,limit})` | Summaries of saved generated tables, in chronological order; offset 0 selects table 1 |
| `pageTable({step,offset,limit})` | Saved count/label columns and both stream positions for one existing table |
| `pageNewValues({step,offset,limit})` | Values first written by that table, in first-discovery order, with source-cell locations |
| `pageValues({offset,limit})` | Final support in increasing numerical order, with final frequencies and first/last positions |
| `countAt({value,through_table})` | Frequency after the seed and that many complete tables |
| `firstAppearance({value})` | The first written cell and total retained occurrences, or finite-prefix absence |
| `locateToken({position})` | The saved value, table, column and count/label role at one written position |
| `rankOccurrences({value,before_position})` | Number of occurrences at positions strictly less than the supplied boundary |
| `selectOccurrence({value,rank})` | The position and role of that zero-based occurrence rank, or an out-of-range result |
| `pageOccurrences({value,offset,limit})` | Consecutive occurrence ranks, positions and source-cell roles |
| `summary()` | Small current frontier, work totals and copy-budget usage; no retained event |
| `snapshot()` | Complete plain JSON record, including all sessions and events; no retained event |

`step` must name an existing generated table. `through_table` ranges from
zero through the current completed table count. A position passed to
`locateToken` must be an existing written position; a rank boundary can also
be exactly the stream length.

Every value lookup accepts a positive canonical decimal string of at most
128 digits, or a positive safe integer. A valid value absent from the record
is an ordinary finite negative answer. Zero, negative values, leading-zero
strings, unsafe numeric values and unknown argument fields are rejected.

`countAt` has two direct data paths. At the final frontier it reads
`counts_by_id`. At an earlier frontier `t`, table `t+1` already stores the
entire frequency vector used as its input; the reader binary-searches that
table's label order. There is no replay of tables 1 through `t`.

Occurrence rank uses binary search of the value's saved sorted position
list. Selection reads the requested list entry directly, then locates its
table through saved boundaries. These operations do not scan the whole
written stream.

### Exact executed navigation requests

The complete input and output of each call lives in
`record.sessions[2].events` in the data file.

| Event | Method | Actual request |
|---:|---|---|
| 0 | `pageTables` | offset 0, limit 6 |
| 1 | `pageTable` | table 4, offset 0, limit 8 |
| 2 | `pageTable` | table 128, offset 604, limit 12 |
| 3 | `countAt` | value 1, through table 54 |
| 4 | `countAt` | value 156, through table 54 |
| 5 | `firstAppearance` | value 156 |
| 6 | `firstAppearance` | value 519 |
| 7 | `firstAppearance` | value 518 |
| 8 | `rankOccurrences` | value 1, before position 8,039 |
| 9 | `selectOccurrence` | value 1, rank 100 |
| 10 | `rankOccurrences` | value 1, before the selected position 1,861 |
| 11 | `locateToken` | final position 65,226 |
| 12 | `pageOccurrences` | value 156, offset 0, limit 8 |
| 13 | `pageValues` | offset 0, limit 16 |
| 14 | `pageValues` | offset 611, limit 12 |
| 15 | `pageNewValues` | table 55, offset 0, limit 64 |
| 16 | `countAt` | value 1, through table 128 |
| 17 | `pageTables` | offset 116, limit 12 |
| 18 | `pageTable` | table 55, offset 180, limit 8 |

The dependent request in event 10 used the location returned by event 9.
These are the actual finite consumer calls, with their complete receipts.
No additional suite of sample inputs or generated fixtures was run.

## Record layout

The core schema is `commons.kimberling_hard_count/v1`.

| Field | Contents |
|---|---|
| `schema`, `source_id` | Format and caller provenance |
| `core.input` | The canonical seed |
| `core.dictionary` | Every distinct value, in first-appearance order, with first position and first table |
| `core.seed_token_ids` | Every initial cell's dictionary ID |
| `core.tables` | Every complete generated table, including its input label IDs, count cells, boundaries and support summary |
| `core.occurrences` | One complete increasing list of written positions per dictionary ID |
| `core.frontier` | Final table count, stream size, numerical value order, current frequencies and complete positive prefix |
| `core.work` | Construction operation counters |
| `sessions` | Opening records, method receipts and accumulated work for each session |

A table retains `label_ids` and `counts` with equal lengths. It also
retains `new_value_ids` in first-discovery order, `distinct_after`,
`positive_prefix_after`, and `maximum_value_id_after`.

The two-row physical stream has a compact complete representation:
count cells are the table's saved numbers, label cells are references to
the dictionary, and the seed has explicit IDs. The occurrence index stores
every position separately. Neither representation drops an occurrence.

The data file contains one complete final core, not several duplicate
copies of its growing prefix. Earlier construction requests and outcomes
remain in sessions 0 and 1. Session 2 contains the saved reader's opening
receipt and all 19 navigation receipts. The top-level envelope adds the
source blob, timing observations, endpoint and literal-custody comparisons.


## Opening checks and mathematical trust

A fresh open copies the complete record once through the bounded JSON copier,
then checks its typed structure, numerical label ordering, complete table
boundaries, active-support membership, discovery metadata and occurrence lists.
It checks every written token against its corresponding saved occurrence-list
position. Final frequencies must equal complete occurrence-list lengths.

It also checks the positive-prefix and maximum-value metadata using saved
discovery times, session/event references, known method names, work-counter
shapes and the sums of historical query work. Selected construction counters
are tied to stored cardinalities.

The opener deliberately does **not** compare a table's saved count cells with
recomputed prefix frequencies. That would regenerate the source recurrence
during a saved-data open. Historical query outcomes likewise are not
mathematically recalculated. A coherently altered history is not established
as an authentic computation merely by passing these structural checks.
Use the delivered source/data identities and provenance when relying on the
delivered result.

The actual fresh reader opened the complete two-session construction record.
Its later snapshot retains a third session with 19 query events. Reopening
that final three-session snapshot was not an additional executed action in
this delivery.

## Exact work accounting

Construction counters describe operations performed by the frozen module.
They are neither CPU instructions nor a timing model.

| Construction counter | Initial seed plus all 128 tables |
|---|---:|
| Seed tokens written | 1 |
| Complete tables constructed | 128 |
| Frozen old counts read | 32,613 |
| Value-map lookups | 32,614 |
| Occurrence positions appended | 65,227 |
| Frequency increments | 65,227 |
| Dictionary entries inserted | 623 |
| Numerical ordering comparisons | 34,151 |
| Positive-prefix membership checks | 647 |
| Generated table cells saved | 65,226 |

The two advances have separate complete work deltas in their retained
receipts. The first advance created 4,019 columns and appended 8,038 cells.
The continuation created 28,594 additional columns and appended 57,188 cells.
All these columns and positions occur in the delivered data.

Preparing the first advance copied 33 existing core JSON values and indexed
one old dictionary entry. Preparing the continuation copied 18,121 existing
core values and indexed 185 old entries. The transaction then inserted 438
new entries while constructing only its new tables, and reused that prepared
map at commit. Copying retained data is included as a cost; it is not described
as replaying the count-table computation.

### Fresh-open work

| Structural work | Open 54-table prefix | Open 128-table prefix |
|---|---:|---:|
| Dictionary entries | 185 | 623 |
| Occurrence positions inspected | 8,039 | 65,227 |
| Final frequency bindings | 185 | 623 |
| Seed cell bindings | 1 | 1 |
| Saved table records | 54 | 128 |
| Saved column pairs | 4,019 | 32,613 |
| Active-support links | 4,019 | 32,613 |
| New-value links | 184 | 622 |
| Numerical ordering comparisons | 4,333 | 33,729 |
| Positive-prefix checks | 210 | 647 |
| Forward-token/index bindings | 8,039 | 65,227 |
| Historical retained events | 1 | 2 |
| Historical query-work fields | 11 | 22 |
| JSON values in initial defensive copy | 18,192 | 136,895 |
| String/key code units in that copy | 13,174 | 36,592 |
| Recurrence replays | 0 | 0 |

Opening also measures the complete record and its core to initialize the
retention budget. Those metadata walks are separate from the initial
defensive-copy counts shown above.

### Saved-query work

The actual 19 retained queries accumulated:

| Counter | Total |
|---|---:|
| Query calls | 19 |
| Value-map lookups | 20 |
| Binary-search comparisons | 150 |
| Saved table records read | 40 |
| Column records read | 37 |
| Occurrence positions read directly | 37 |
| Origin records read | 50 |
| Returned data records | 87 |
| Table reconstructions | 0 |
| Recurrence steps | 0 |
| Occurrence-index rebuilds | 0 |

The binary-search counter covers comparisons against saved boundaries or
positions. The separate direct-occurrence-read counter covers selected/page
entries; it does not count each binary-search comparison a second time.
Returned-record counts describe items and witnesses, so a finite-absence
answer can return zero data records while still producing a response envelope.

### Cost model

Let `d_t=|D_t|`, let `a_t` be the number of values first introduced by the
next table, and let `M` be the retained written-stream length.

Generating that table reads `d_t` old counts, appends `2d_t` occurrence
positions, sorts its `a_t` new IDs and merges them with the old numerical
order. Across a run the explicit cell work is proportional to `M`; sorting
adds the comparisons for the new-value batches. Comparisons of initial
decimal labels can inspect up to the permitted 128 digits.

An advance copies its existing core once before adding tables. Opening and
snapshot export walk the complete retained data. The record stores the
complete two-row tables as well as the complete occurrence index, so storage
is linear in retained cells and metadata, with a real constant cost for both
representations.

Ordinary queries copy only their arguments, bounded result and new receipt.
They do not copy the fixed core. Table/value pages read their selected
records. A historical `countAt` performs a numerical-label binary search;
a final `countAt` uses the saved final frequency. Occurrence rank is a
binary search of one position list. Selection and first-appearance queries
locate their saved position through a table-boundary binary search.
An occurrence page performs that location work for each returned entry.

These are operation-level descriptions. No worst-case constant-time promise
is made for the JavaScript engine's map or array implementation.

## Bounds and error behavior

| Resource | Fixed limit |
|---|---:|
| General initial table width | 32 columns |
| Positive value length | 128 decimal digits |
| `source_id` length | 512 UTF-16 code units |
| Complete generated tables | 512 |
| Tables requested by one advance | 256 |
| Total written cells, including the seed | 65,536 |
| Items requested by one page | 64 |
| Retained sessions | 16 |
| Retained method events per session | 32 |
| Complete-record JSON value visits | 8,000,000 |
| Complete-record string/key code units | 40,000,000 |
| JSON nesting depth | 48 |

Labels may be much larger than the written-cell limit. They remain canonical
strings and are ordered exactly. Frequencies, ranks, positions and counters
are safe integers; the finite token bound keeps constructed frequencies
within exact Number arithmetic.

A general input table uses at most 64 physical seed cells. New values produced
by a count row are themselves bounded by the current number of written cells.
The module does not use decimal-digit splitting, floating point estimates of
large labels, BigInt serialization, or hidden external storage.

The JSON copier rejects cycles, sparse arrays, extra array properties,
accessors, symbols, non-enumerable object data, unsupported prototypes,
noninteger numbers and non-JSON values. Snapshot budgets count recursive JSON
values and string/key UTF-16 code units. They do not count the decimal digits
of Number values, punctuation or encoded UTF-8 bytes. The evidence envelope's
928,401 file bytes are therefore a different measure.

The final reader record's retained budget reports 138,120 values,
49,583 string/key code units and depth 9. These describe the public record,
excluding the outer evidence envelope.

Before computing a retained call, the implementation reserves a conservative
amount of remaining event space. An advance's reservation scales with its
requested token/table allowances. Actual complete-event and core sizes are
checked before committing. A near-capacity record can therefore reject a call
even when a smaller request would fit.

Invalid arguments, exhausted session/event capacity and export-limit errors
leave the current record unchanged. They throw `HardCountError` with a
`code`; they do not append an error event. Rejected input has no completed
mathematical result. Normal complete-table resource stops are retained
`advance` outcomes, as demonstrated by both actual advances.

## Observed timings and execution scope

| Actual operation | Single observation |
|---|---:|
| Construct the one-cell seed | 1 ms |
| First advance, 54 new tables | 13 ms |
| Open the saved 54-table prefix | 31 ms |
| Continue with 74 new tables | 89 ms |
| Open the completed 128-table prefix | 193 ms |
| All 19 saved queries | 6 ms |

These are individual wall-clock observations with millisecond resolution,
not benchmarks or comparative performance results. Advance/open observations
exclude the separate explicit snapshot exports. The query-loop observation
includes retaining local call receipts and excludes its final full snapshot
copy. Timing code belongs to the external execution record; the public
module contains no clocks.

Actual execution comprised one constructor, one first advance, one fresh
open and continuation, and one fresh saved-reader open with 19 queries.
The source remained at the recorded blob throughout. No mathematical prefix
was regenerated to produce a verification result.

The general initial-table branch, invalid-input paths, retention-limit
errors, table-limit stop and final-history reopening were not separately
executed. There were no tests, fixtures, native executor calls, workflow
dispatches or external contacts.

## Publication and qualification scope

The original public board and source statement were qualified before the
finite scope was claimed. Exact PPL122 and Hard Count Slack searches returned
the board; its original thread had no replies at that observation. The
Commons code search returned no matching carrier, and a current 90-entry
research-directory read showed no corresponding directory.

A separate PR-title search returned a GitHub secondary-rate-limit 403.
That query remained held and was not counted as an empty search or retried
through another route. The quiet interval was observed before the distinct
needed directory read. These are bounded custody observations, not an
exhaustive claim about every repository or conversation.

The publication consists of the source, this guide, the complete data and
the README. Its delivery receipt records actual commit/file readbacks.
It does not assert mode verification, whole-tree verification, hosted
workflow success, sponsor acceptance, universal coverage or an award.

The reusable result is a complete finite count-table history with exact
occurrence navigation and an explicit continuation boundary. The unbounded
support argument remains separate from the unresolved all-positive coverage
question.
