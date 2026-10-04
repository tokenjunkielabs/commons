"use strict";

// Exact point counts using the attributed shared A304081 offset catalog.
const MAX_N = 1000000000000n;

function exactInteger(value, name) {
  let result;
  if (typeof value === "bigint") result = value;
  else if (typeof value === "number" && Number.isSafeInteger(value)) result = BigInt(value);
  else if (typeof value === "string" && /^(?:0|[1-9][0-9]*)$/.test(value)) {
    if (value.length > 13) throw new RangeError(name + " exceeds 1000000000000");
    result = BigInt(value);
  } else throw new TypeError(name + " must be a nonnegative exact integer");
  if (result < 0n || result > MAX_N) {
    throw new RangeError(name + " must be between 0 and 1000000000000");
  }
  return result;
}

function squareRoot(value) {
  let low = 0n, high = value + 1n;
  while (high - low > 1n) {
    const middle = (low + high) / 2n;
    if (middle * middle <= value) low = middle;
    else high = middle;
  }
  return low;
}

function sievePrimes(limit) {
  const composite = new Uint8Array(limit + 1);
  const primes = [];
  for (let value = 2; value <= limit; value++) {
    if (composite[value]) continue;
    primes.push(BigInt(value));
    if (value * value <= limit) {
      for (let multiple = value * value; multiple <= limit; multiple += value) {
        composite[multiple] = 1;
      }
    }
  }
  return primes;
}

/**
 * Prepare one bounded counter. In CommonJS, the local catalog is loaded
 * automatically; a connected runtime passes its complete catalog export.
 * Each count call returns all candidate pairs and distinct classifications.
 */
function createRepresentationCounter(max_n, catalogFactory) {
  const maximum = exactInteger(max_n, "max_n");
  if (catalogFactory === undefined) {
    if (typeof require !== "function") {
      throw new TypeError("pass createOffsetCatalog as the second argument in a connected runtime");
    }
    catalogFactory = require("./offset_catalog.cjs").createOffsetCatalog;
  }
  if (typeof catalogFactory !== "function") {
    throw new TypeError("catalogFactory must be the createOffsetCatalog export");
  }
  const catalog = catalogFactory(maximum);
  if (!catalog || catalog.schema !== "commons.a304081.offset_catalog/v1" ||
      catalog.max_n !== maximum.toString() || typeof catalog.candidatesFor !== "function") {
    throw new TypeError("catalogFactory returned an incompatible offset catalog");
  }
  const sieveLimit = Number(squareRoot(maximum));
  const primes = sievePrimes(sieveLimit);
  const preparation = Object.freeze({
    max_n: maximum.toString(),
    catalog_schema: catalog.schema,
    catalog_base_bound: catalog.base_bound,
    catalog_statistics: catalog.statistics,
    prime_sieve_limit: sieveLimit,
    prime_sieve_count: primes.length,
    method: "exact_trial_division",
    division_bound: "floor(sqrt(prime_candidate))"
  });

  function classify(value) {
    let divisions = 0;
    for (const prime of primes) {
      if (prime * prime > value) break;
      divisions++;
      if (value % prime === 0n) {
        return {prime_candidate: value.toString(), is_prime: false,
          least_divisor: prime.toString(), cofactor: (value / prime).toString(),
          trial_divisions: divisions};
      }
    }
    return {prime_candidate: value.toString(), is_prime: true,
      least_divisor: null, cofactor: null, trial_divisions: divisions};
  }

  function count(n) {
    const target = exactInteger(n, "n");
    if (target > maximum) throw new RangeError("n exceeds this counter's inclusive max_n");
    const view = catalog.candidatesFor(target);
    if (!view || view.schema !== "commons.a304081.prime_candidates/v1" ||
        view.n !== target.toString() || !Array.isArray(view.candidates) ||
        view.exponent_pair_count !== view.candidates.length) {
      throw new TypeError("offset catalog returned an incompatible candidate view");
    }
    const byValue = new Map();
    const classifications = [];
    const candidatePairs = [];
    const representations = [];
    let trialDivisions = 0;
    let distinctPrimes = 0;
    for (const row of view.candidates) {
      const value = exactInteger(row.prime_candidate, "prime_candidate");
      if (value < 3n || value > target || value % 2n !== 1n) {
        throw new RangeError("offset catalog returned an out-of-domain prime candidate");
      }
      let index = byValue.get(row.prime_candidate);
      if (index === undefined) {
        const result = classify(value);
        index = classifications.length;
        byValue.set(row.prime_candidate, index);
        classifications.push(result);
        trialDivisions += result.trial_divisions;
        if (result.is_prime) distinctPrimes++;
      }
      candidatePairs.push({...row, classification_index: index});
      if (classifications[index].is_prime) {
        representations.push({p: row.prime_candidate, k: row.k, m: row.m,
          offset: row.offset, base_offset: row.base_offset, j: row.j});
      }
    }
    return {
      schema: "commons.a304081.representation_count/v1",
      n: target.toString(),
      coefficient: view.coefficient,
      prime_status: "evaluated_exactly",
      preparation,
      coverage: {
        complete_offsets_for_n: view.coverage.complete_offsets_for_n,
        all_distinct_candidates_classified: true,
        minimum_prime_candidate: "3",
        scope: "single_n"
      },
      candidate_pair_count: candidatePairs.length,
      distinct_candidate_count: classifications.length,
      representation_count: representations.length,
      distinct_prime_candidate_count: distinctPrimes,
      composite_pair_count: candidatePairs.length - representations.length,
      trial_divisions: trialDivisions,
      representations,
      candidate_pairs: candidatePairs,
      classifications
    };
  }

  return Object.freeze({
    schema: "commons.a304081.representation_counter/v1",
    max_n: maximum.toString(), preparation, count
  });
}

module.exports = {createRepresentationCounter};
