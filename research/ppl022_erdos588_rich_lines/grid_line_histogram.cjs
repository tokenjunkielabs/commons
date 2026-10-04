"use strict";

// Exact theorem-derived grid line counts; see GRID_LINE_HISTOGRAM_API.md.
const GRID_HISTOGRAM_LIMITS = Object.freeze({
  min_side_length: 2,
  max_side_length: 1024,
  min_dimension: 1,
  max_dimension: 4096,
  max_power_digits: 512,
  max_term_records: 8192
});
const POWER_LIMIT = 10n ** BigInt(GRID_HISTOGRAM_LIMITS.max_power_digits) - 1n;

function countGridLineHistogram(options) {
  if (options === null || typeof options !== "object" || Array.isArray(options)) {
    throw new TypeError("options must be an object");
  }
  const k = options.side_length;
  const dimension = options.dimension;
  if (!Number.isSafeInteger(k) ||
      k < GRID_HISTOGRAM_LIMITS.min_side_length ||
      k > GRID_HISTOGRAM_LIMITS.max_side_length) {
    throw new RangeError("side_length must be an integer from 2 through 1024");
  }
  if (!Number.isSafeInteger(dimension) ||
      dimension < GRID_HISTOGRAM_LIMITS.min_dimension ||
      dimension > GRID_HISTOGRAM_LIMITS.max_dimension) {
    throw new RangeError("dimension must be an integer from 1 through 4096");
  }
  const includeTerms = options.include_terms === undefined ? false : options.include_terms;
  if (typeof includeTerms !== "boolean") {
    throw new TypeError("include_terms must be a boolean");
  }
  const work = {
    exponentiation_calls: 0,
    exponentiation_multiplications: 0,
    exponentiation_squarings: 0,
    point_count_square_multiplications: 0,
    power_cache_hits: 0,
    step_basis_cache_hits: 0,
    sieve_composite_marks: 0,
    mobius_terms_considered: 0,
    nonzero_mobius_terms_added: 0,
    zero_mobius_terms_skipped: 0,
    retained_term_records: 0,
    points_enumerated: 0,
    point_pairs_enumerated: 0,
    individual_lines_enumerated: 0,
    projected_coordinates_enumerated: 0
  };

  function checkedProduct(left, right, label) {
    if (left !== 0n && right > POWER_LIMIT / left) {
      throw new RangeError(label + " exceeds the power digit limit");
    }
    return left * right;
  }
  function boundedPower(base) {
    work.exponentiation_calls++;
    let exponent = dimension;
    let result = 1n;
    let factor = base;
    while (exponent > 0) {
      if (exponent % 2 === 1) {
        result = checkedProduct(result, factor, "integer power");
        work.exponentiation_multiplications++;
      }
      exponent = Math.floor(exponent / 2);
      if (exponent > 0) {
        factor = checkedProduct(factor, factor, "integer power");
        work.exponentiation_squarings++;
      }
    }
    return result;
  }

  const kb = BigInt(k);
  const pointCount = boundedPower(kb);
  const maximumPower = checkedProduct(pointCount, pointCount, "squared point count");
  work.point_count_square_multiplications++;
  const powerCache = new Map([
    [kb.toString(), { base: kb, value: pointCount, construction: "bounded_exponentiation" }],
    [(kb * kb).toString(), { base: kb * kb, value: maximumPower, construction: "squared_point_count" }]
  ]);
  function cachedPower(base) {
    const key = base.toString();
    if (powerCache.has(key)) {
      work.power_cache_hits++;
      return powerCache.get(key).value;
    }
    const value = boundedPower(base);
    powerCache.set(key, { base, value, construction: "bounded_exponentiation" });
    return value;
  }

  const bound = k - 1;
  const mu = Array(bound + 1).fill(0);
  const leastPrime = Array(bound + 1).fill(0);
  const primes = [];
  mu[1] = 1;
  for (let value = 2; value <= bound; value++) {
    if (leastPrime[value] === 0) {
      leastPrime[value] = value;
      primes.push(value);
      mu[value] = -1;
    }
    for (const prime of primes) {
      const multiple = value * prime;
      if (multiple > bound) break;
      leastPrime[multiple] = prime;
      work.sieve_composite_marks++;
      if (value % prime === 0) {
        mu[multiple] = 0;
        break;
      }
      mu[multiple] = -mu[value];
    }
  }

  const basis = new Map();
  function stepBasis(scale) {
    if (basis.has(scale)) {
      work.step_basis_cache_hits++;
      return basis.get(scale);
    }
    const a = BigInt(scale);
    const maximumCoordinate = BigInt(bound) / a;
    const singleCoordinate = kb + 2n * kb * maximumCoordinate -
      a * maximumCoordinate * (maximumCoordinate + 1n);
    const power = cachedPower(singleCoordinate);
    const record = {
      scale,
      maximum_abs_direction_coordinate: Number(maximumCoordinate),
      one_coordinate_weight: singleCoordinate,
      cartesian_weight: power,
      nonzero_direction_weight: power - pointCount
    };
    basis.set(scale, record);
    return record;
  }

  const segmentCounts = Array(k + 3).fill(0n);
  const segmentRows = [];
  const terms = includeTerms ? [] : null;
  for (let length = 2; length <= k; length++) {
    const divisorLimit = Math.floor(bound / (length - 1));
    let numerator = 0n;
    for (let g = 1; g <= divisorLimit; g++) {
      const scale = (length - 1) * g;
      work.mobius_terms_considered++;
      let contribution = 0n;
      if (mu[g] === 0) {
        work.zero_mobius_terms_skipped++;
      } else {
        contribution = BigInt(mu[g]) * stepBasis(scale).nonzero_direction_weight;
        numerator += contribution;
        work.nonzero_mobius_terms_added++;
      }
      if (includeTerms) {
        if (terms.length >= GRID_HISTOGRAM_LIMITS.max_term_records) {
          throw new RangeError("too many retained Mobius term records");
        }
        terms.push({
          segment_length: length,
          divisor: g,
          mobius: mu[g],
          step_scale: scale,
          signed_contribution: contribution.toString()
        });
      }
    }
    if (numerator < 0n || numerator % 2n !== 0n) {
      throw new Error("primitive-segment orientation accounting failed");
    }
    segmentCounts[length] = numerator / 2n;
    segmentRows.push({
      segment_length: length,
      divisor_limit: divisorLimit,
      oriented_primitive_segment_count: numerator.toString(),
      unoriented_consecutive_segments: segmentCounts[length].toString()
    });
  }
  for (let length = k + 1; length <= k + 2; length++) {
    segmentRows.push({
      segment_length: length,
      divisor_limit: 0,
      oriented_primitive_segment_count: "0",
      unoriented_consecutive_segments: "0"
    });
  }

  const histogram = [];
  let cumulative = 0n;
  let representedPairs = 0n;
  let incidences = 0n;
  let segmentSum = 0n;
  for (let length = k; length >= 2; length--) {
    const exact = segmentCounts[length] - 2n * segmentCounts[length + 1] +
      segmentCounts[length + 2];
    if (exact < 0n) throw new Error("negative exact line count");
    cumulative += exact;
    representedPairs += BigInt(length * (length - 1) / 2) * exact;
    incidences += BigInt(length) * exact;
    segmentSum += segmentCounts[length];
    histogram.push({
      points_per_line: length,
      exact_lines: exact.toString(),
      at_least_lines: cumulative.toString()
    });
  }
  histogram.reverse();
  const pairCount = pointCount * (pointCount - 1n) / 2n;
  if (representedPairs !== pairCount || segmentSum !== pairCount) {
    throw new Error("complete grid pair accounting failed");
  }
  work.retained_term_records = terms === null ? 0 : terms.length;
  const topCount = segmentCounts[k];

  return {
    schema: "erdos588.grid_line_histogram/v1",
    side_length: k,
    dimension,
    point_count: pointCount.toString(),
    maximum_collinearity: k,
    determined_line_count: cumulative.toString(),
    point_line_incidences: incidences.toString(),
    histogram,
    segment_counts: segmentRows,
    mobius_table: Array.from({ length: bound }, (_, index) => {
      const g = index + 1;
      return { g, mobius: mu[g], least_prime_divisor: g === 1 ? null : leastPrime[g] };
    }),
    power_values: [...powerCache.values()].sort((a, b) =>
      a.base < b.base ? -1 : a.base > b.base ? 1 : 0).map(row => ({
      base: row.base.toString(),
      exponent: dimension,
      value: row.value.toString(),
      construction: row.construction
    })),
    step_basis: [...basis.values()].sort((a, b) => a.scale - b.scale).map(row => ({
      scale: row.scale,
      maximum_abs_direction_coordinate: row.maximum_abs_direction_coordinate,
      one_coordinate_weight: row.one_coordinate_weight.toString(),
      cartesian_weight: row.cartesian_weight.toString(),
      excluded_zero_direction_weight: pointCount.toString(),
      nonzero_direction_weight: row.nonzero_direction_weight.toString()
    })),
    terms_included: includeTerms,
    mobius_terms: terms,
    accounting: {
      unordered_point_pairs: pairCount.toString(),
      sum_line_pair_counts: representedPairs.toString(),
      sum_consecutive_segment_counts: segmentSum.toString(),
      exact: true
    },
    finite_planar_interpretation: {
      property_P_side_length: true,
      exact_side_length_lines: topCount.toString(),
      existence_basis: "the proved finite integer incidence-preserving projection",
      projected_coordinates_computed: false,
      individual_incidence_records_computed: false,
      erdos_lower_bound: k >= 4 ? {
        notation: "f_k(n)",
        k,
        n: pointCount.toString(),
        at_least: topCount.toString()
      } : null,
      extremal_equality_claimed: false,
      external_frontier_claimed: false
    },
    limits: { ...GRID_HISTOGRAM_LIMITS },
    work
  };
}

module.exports = Object.freeze({ countGridLineHistogram, GRID_HISTOGRAM_LIMITS });
