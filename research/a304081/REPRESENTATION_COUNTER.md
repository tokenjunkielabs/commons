# Exact A304081 counts for individual inputs

`representation_counter.cjs` evaluates every prime candidate from the existing shared offset catalog and returns the exact representation count for one `n`. It preserves each `(k,m)` pair and retains both the successful representations and the complete rejected-candidate classifications.

The sequence definition and shared parity reformulation come from [OEIS A304081](https://oeis.org/A304081) and [OEIS A304122](https://oeis.org/A304122). [PARITY_CATALOG.md](PARITY_CATALOG.md) explains the credited reduction, squarefree offsets and exponent multiplicity. This counter is a portable consumer of that catalog.

## Use

With CommonJS and the two source files together:

```javascript
const {createRepresentationCounter} = require("./representation_counter.cjs");
const counter = createRepresentationCounter("20050000002");
const odd = counter.count("20050000001");
const even = counter.count("20050000002");
```

In a connected JavaScript runtime, load each complete source and pass the existing catalog export explicitly:

```javascript
const catalogBox = {exports: {}};
const counterBox = {exports: {}};
new Function("module", "exports", catalogSource)(catalogBox, catalogBox.exports);
new Function("module", "exports", counterSource)(counterBox, counterBox.exports);
const counter = counterBox.exports.createRepresentationCounter(
  "20050000002", catalogBox.exports.createOffsetCatalog
);
const result = counter.count("20050000001");
text({n: result.n, count: result.representation_count,
  representations: result.representations});
```

Here `catalogSource` is the complete `offset_catalog.cjs` source and `counterSource` is the complete `representation_counter.cjs` source. The second argument is the existing `createOffsetCatalog` export; it is a dependency injection point for runtimes without `require`. Compatibility checks do not establish the correctness or provenance of an arbitrary replacement factory.

Both `max_n` and `n` accept nonnegative BigInts, canonical decimal strings, or safe integer Numbers. The inclusive maximum is `1000000000000`; `n` must not exceed the prepared `max_n`. Unsafe Numbers, fractions and noncanonical strings raise `TypeError`; out-of-range values raise `RangeError`. Preparation validates the maximum before allocating the catalog or prime sieve.

## Exact classification

The counter prepares the shared squarefree offset catalog and a prime table once. The prime table contains every prime through `floor(sqrt(max_n))`. Its sieve limit is at most 1,000,000. For a candidate `p`, it tries the table's primes in increasing order until a divisor is found or the next prime has square greater than `p`.

A composite integer has a prime divisor at most its square root. Since all catalog candidates are odd integers at least 3 and no larger than `max_n`, exhausting this range proves primality for that candidate. Divisibility, squares, offsets, candidates and quotients use BigInt arithmetic; there is no probabilistic primality test. The sieve's bounded indexes use exact integer Numbers.

Each distinct numeric candidate is classified once within a `count` call. The classification is shared by all exponent pairs yielding that value. The per-query cache is discarded after the call; the prepared catalog and prime table remain reusable for subsequent inputs.

The API performs no provider calls, file writes, native process execution or interval scan. Trial division is intended for bounded individual queries; this implementation makes no performance claim against the existing C++ search.

## Result contract

The frozen counter has schema `commons.a304081.representation_counter/v1`, `max_n`, preparation metadata and a `count` method. Each call returns a fresh JSON-serializable object with schema `commons.a304081.representation_count/v1`.

| Field | Meaning |
| --- | --- |
| `n`, `coefficient` | Exact decimal input and its parity coefficient, 1 for even or 2 for odd |
| `prime_status` | `evaluated_exactly` |
| `preparation` | Catalog identity/statistics, inclusive bound, sieve size, exact method and division bound |
| `coverage` | Complete catalog offsets for this input, all distinct candidates classified, and `scope: single_n` |
| `candidate_pair_count` | Every eligible exponent pair, including numeric duplicates |
| `distinct_candidate_count` | Number of distinct candidate integers classified |
| `representation_count` | The sequence value `a(n)`, counting successful exponent pairs |
| `distinct_prime_candidate_count` | Distinct successful candidate integers, potentially fewer than representations |
| `composite_pair_count` | Exponent pairs whose candidate is composite |
| `trial_divisions` | Actual modulus operations across distinct candidate classifications |
| `representations` | Every successful `{p,k,m,offset,base_offset,j}` row |
| `candidate_pairs` | Every original catalog row plus its zero-based `classification_index` |
| `classifications` | Every distinct candidate's exact primality decision and divisor data |

Each classification contains `prime_candidate`, `is_prime`, `least_divisor`, `cofactor` and `trial_divisions`. Composite rows retain the least prime divisor found and the exact quotient; prime rows have null divisor and cofactor. `classification_index` links each exponent pair to that table. Inputs, offsets, candidates, divisors and quotients are returned as decimal strings; exponents, indexes and bounded counters are Numbers.

These results inherit offset completeness from the supplied original catalog implementation. Passing a different factory changes that dependency. Source compatibility and a declared coverage field are not independent provenance checks.

## Actual new point counts

One public constructor invocation of counter source `599ec2d630307c4ab1bd548ef01269b2e15cd6c5`, with catalog source `4eb31cfe376c74e9d1e3a56de15dce4e0dbcd362`, prepared the inclusive bound `20050000002`. Exactly two calls to `count` produced:

| Input `n` | Candidate pairs | Distinct candidates | `a(n)` | Composite pairs | Trial divisions |
| --- | ---: | ---: | ---: | ---: | ---: |
| 20050000001 | 381 | 378 | **27** | 354 | 377,805 |
| 20050000002 | 395 | 392 | **30** | 365 | 460,726 |

Both inputs have as many distinct successful prime candidates as successful exponent pairs. That equality is an observation for these two inputs, not a general multiplicity rule.

The shared catalog considered 509 exponent pairs across 505 distinct numeric bases, retaining 395 squarefree pairs across 392 distinct bases through `20049999999`. Its squarefree classifications were performed once per distinct base. The counter's prime table contains 13,144 primes through 141,598.

The first successful rows give:

```text
20050000001 = 20049999943 + 2^3 + 2*5^2
20050000002 = 20049999989 + 2^3 +   5^1
```

[point_counts_20261004.json](point_counts_20261004.json) retains both complete result objects: all 57 successful representations, all 776 candidate pairs and all 770 per-query classification rows. Compact row formatting changes no result field or value.

These are two individual exact point counts. The old verifier, source-example runs and historically recorded interval search were not replayed. This publication does not claim a new interval search, worldwide priority, a proof for all integers or a prize result. The original mathematical problem remains open.

## Near-cap individual counts

A new constructor invocation of the unchanged counter source `599ec2d630307c4ab1bd548ef01269b2e15cd6c5`, with catalog source `4eb31cfe376c74e9d1e3a56de15dce4e0dbcd362`, prepared the inclusive maximum `1000000000000`. Two new single-input calls produced:

| Input `n` | Candidate pairs | Distinct candidates | `a(n)` | Trial divisions |
| --- | ---: | ---: | ---: | ---: |
| 999999999999 | 508 | 505 | **26** | 2,663,718 |
| 1000000000000 | 548 | 545 | **56** | 5,186,941 |

[point_counts_near_cap_20261004.json](point_counts_near_cap_20261004.json) retains both complete result objects, including every exponent-pair row, successful representation, classification, least divisor, cofactor and operation count. Together they contain 1,056 candidate pairs, 1,050 per-query classification rows and 82 representations.

An evaluated candidate replaced the bounded primality loop's BigInt arithmetic with Number arithmetic under the same maximum. Its complete JSON results matched the retained baseline for both inputs, including all fields, counters and witnesses. The data artifact retains the complete evaluated candidate source and the original source identities. The elapsed observations were:

| Operation | Existing counter | Number candidate |
| --- | ---: | ---: |
| Preparation | 238 ms | 229 ms |
| Count `999999999999` | 201 ms | 202 ms |
| Count `1000000000000` | 362 ms | 389 ms |

These are one elapsed observation per operation and variant, not a statistical benchmark or a comparison with the C++ search. Neither count call showed an observed speedup, so the Number candidate was not adopted. The published counter remains `599ec2d630307c4ab1bd548ef01269b2e15cd6c5` and continues to use the BigInt classification described above.

These are two additional individual exact point counts, including the maximum supported input. They do not extend the historical interval search, establish worldwide priority, or prove the conjecture. The earlier point-count data, source examples and mathematical attribution remain unchanged.
