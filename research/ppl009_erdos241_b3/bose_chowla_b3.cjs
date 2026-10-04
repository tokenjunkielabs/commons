"use strict";

// Classical Bose-Chowla construction, specialized to prime fields and order 3.
// Source attribution and exact certificate contracts: BOSE_CHOWLA_B3_API.md.
const BOSE_CHOWLA_B3_LIMITS = Object.freeze({
  min_prime: 2,
  max_prime: 43,
  max_field_elements: 79507,
  max_primitive_candidates: 4096,
  max_field_multiplications: 2000000
});

function constructBoseChowlaB3(options) {
  if (!options || typeof options !== "object" || Array.isArray(options)) {
    throw new TypeError("options must be an object");
  }
  const p = options.prime;
  if (!Number.isSafeInteger(p) || p < BOSE_CHOWLA_B3_LIMITS.min_prime ||
      p > BOSE_CHOWLA_B3_LIMITS.max_prime) {
    throw new RangeError("prime must be an integer from 2 through 43");
  }
  const primeTests = [];
  for (let divisor = 2; divisor * divisor <= p; divisor++) {
    const remainder = p % divisor;
    primeTests.push({ divisor, remainder });
    if (remainder === 0) throw new RangeError("prime is composite");
  }
  if (!Array.isArray(options.cubic_coefficients) ||
      options.cubic_coefficients.length !== 3) {
    throw new TypeError("cubic_coefficients must be [constant, linear, quadratic]");
  }
  const polynomial = Array.from(options.cubic_coefficients, value => {
    if (!Number.isSafeInteger(value) || value < 0 || value >= p) {
      throw new RangeError("cubic coefficients must be canonical residues modulo prime");
    }
    return value === 0 ? 0 : value;
  });
  const mod = value => ((value % p) + p) % p;
  const work = {
    prime_trial_divisors: primeTests.length,
    polynomial_root_evaluations: 0,
    primitive_candidates_tested: 0,
    field_power_calls: 0,
    power_result_multiplications: 0,
    power_squarings: 0,
    field_multiplications: 0,
    degree_certificate_products: 0,
    cycle_steps: 0,
    discrete_log_lookups: 0,
    cyclic_gaps_examined: 0,
    triple_sums_enumerated: 0,
    subsets_enumerated: 0
  };
  const rootValues = [];
  for (let value = 0; value < p; value++) {
    const result = mod(mod(mod(value + polynomial[2]) * value + polynomial[1]) *
      value + polynomial[0]);
    work.polynomial_root_evaluations++;
    rootValues.push({ argument: value, value: result });
    if (result === 0) {
      const error = new Error("the monic cubic has a base-field root");
      error.name = "ReduciblePolynomialError";
      error.root_witness = { prime: p, cubic_coefficients: polynomial.slice(), root: value };
      throw error;
    }
  }

  const fieldSize = p * p * p, order = fieldSize - 1, p2 = p * p;
  if (fieldSize > BOSE_CHOWLA_B3_LIMITS.max_field_elements) {
    throw new RangeError("field exceeds the complete-table limit");
  }
  const decode = code => [code % p, Math.floor(code / p) % p, Math.floor(code / p2)];
  const encode = values => values[0] + p * values[1] + p2 * values[2];
  function multiply(left, right) {
    if (work.field_multiplications >= BOSE_CHOWLA_B3_LIMITS.max_field_multiplications) {
      const error = new RangeError("field multiplication budget exhausted");
      error.work = { ...work };
      throw error;
    }
    work.field_multiplications++;
    const a = decode(left), b = decode(right), coefficients = Array(5).fill(0);
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) coefficients[i + j] += a[i] * b[j];
    }
    for (let i = 0; i < 5; i++) coefficients[i] = mod(coefficients[i]);
    for (let degree = 4; degree >= 3; degree--) {
      const leading = coefficients[degree];
      coefficients[degree] = 0;
      for (let i = 0; i < 3; i++) {
        coefficients[degree - 3 + i] =
          mod(coefficients[degree - 3 + i] - leading * polynomial[i]);
      }
    }
    return encode(coefficients);
  }
  function power(base, exponent) {
    work.field_power_calls++;
    let result = 1, factor = base, remaining = exponent;
    while (remaining > 0) {
      if (remaining % 2 === 1) {
        result = multiply(result, factor);
        work.power_result_multiplications++;
      }
      remaining = Math.floor(remaining / 2);
      if (remaining > 0) {
        factor = multiply(factor, factor);
        work.power_squarings++;
      }
    }
    return result;
  }

  const orderFactorization = [];
  let remainingOrder = order;
  for (let prime = 2; prime * prime <= remainingOrder; prime++) {
    if (remainingOrder % prime !== 0) continue;
    let exponent = 0;
    while (remainingOrder % prime === 0) {
      remainingOrder /= prime;
      exponent++;
    }
    orderFactorization.push({ prime, exponent });
  }
  if (remainingOrder > 1) orderFactorization.push({ prime: remainingOrder, exponent: 1 });
  const candidateRecords = [];
  function assessGenerator(candidate) {
    work.primitive_candidates_tested++;
    const record = {
      candidate_code: candidate,
      candidate_coefficients: decode(candidate),
      prime_factor_tests: [],
      full_order_power_code: null,
      primitive: false
    };
    for (const factor of orderFactorization) {
      const exponent = order / factor.prime;
      const value = power(candidate, exponent);
      record.prime_factor_tests.push({
        order_prime_factor: factor.prime,
        exponent,
        power_code: value,
        power_coefficients: decode(value)
      });
      if (value === 1) {
        candidateRecords.push(record);
        return null;
      }
    }
    record.full_order_power_code = power(candidate, order);
    if (record.full_order_power_code !== 1) {
      throw new Error("finite-field multiplicative-order invariant failed");
    }
    record.primitive = true;
    candidateRecords.push(record);
    return record;
  }

  let selected = null;
  const automatic = options.generator_code === undefined;
  if (!automatic) {
    const candidate = options.generator_code;
    if (!Number.isSafeInteger(candidate) || candidate < 1 || candidate >= fieldSize) {
      throw new RangeError("generator_code must be a nonzero encoded field element");
    }
    selected = assessGenerator(candidate);
    if (selected === null) {
      const error = new Error("the supplied field element is not primitive");
      error.name = "NonPrimitiveElementError";
      error.order_witness = candidateRecords[0];
      throw error;
    }
  } else {
    for (let candidate = p; candidate < fieldSize && selected === null; candidate++) {
      if (work.primitive_candidates_tested >= BOSE_CHOWLA_B3_LIMITS.max_primitive_candidates) {
        const error = new RangeError("primitive-element candidate limit exhausted");
        error.candidate_records = candidateRecords;
        error.work = { ...work };
        throw error;
      }
      selected = assessGenerator(candidate);
    }
    if (selected === null) throw new Error("no primitive element found in the complete field");
  }
  const theta = selected.candidate_code, thetaCoordinates = decode(theta);
  const thetaSquared = multiply(theta, theta);
  work.degree_certificate_products++;
  const squareCoordinates = decode(thetaSquared);
  const determinant = mod(thetaCoordinates[1] * squareCoordinates[2] -
    thetaCoordinates[2] * squareCoordinates[1]);
  if (determinant === 0) throw new Error("degree-three basis certificate failed");

  const logs = new Int32Array(fieldSize);
  logs.fill(-1);
  const powers = [];
  let current = 1;
  for (let exponent = 0; exponent < order; exponent++) {
    if (current <= 0 || current >= fieldSize || logs[current] !== -1) {
      throw new Error("complete primitive power cycle invariant failed");
    }
    logs[current] = exponent;
    powers.push(current);
    current = multiply(current, theta);
    work.cycle_steps++;
  }
  if (current !== 1) throw new Error("primitive power cycle did not close at its order");

  const offsets = [];
  for (let offset = 0; offset < p; offset++) {
    const coordinates = thetaCoordinates.slice();
    coordinates[0] = mod(coordinates[0] + offset);
    const code = encode(coordinates), exponent = logs[code];
    work.discrete_log_lookups++;
    if (exponent < 1 || exponent >= order) {
      throw new Error("Bose-Chowla affine-line exponent invariant failed");
    }
    offsets.push({
      offset,
      target_code: code,
      target_coefficients: coordinates,
      canonical_exponent: exponent
    });
  }
  const residues = offsets.map(row => row.canonical_exponent).sort((a, b) => a - b);
  if (new Set(residues).size !== p) throw new Error("affine offsets did not produce distinct exponents");

  const gaps = [];
  let largestGap = null;
  for (let index = 0; index < residues.length; index++) {
    const from = residues[index], to = residues[(index + 1) % residues.length];
    const distance = index + 1 < residues.length ? to - from : order + to - from;
    const record = { from, to, distance, wraps_zero: index + 1 === residues.length };
    gaps.push(record);
    work.cyclic_gaps_examined++;
    if (largestGap === null || distance > largestGap.distance ||
        (distance === largestGap.distance && to < largestGap.to)) {
      largestGap = record;
    }
  }
  const start = largestGap.to;
  const residueMod = value => ((value % order) + order) % order;
  const mapped = offsets.map(row => ({
    offset: row.offset,
    canonical_exponent: row.canonical_exponent,
    positive_integer: residueMod(row.canonical_exponent - start) + 1
  })).sort((a, b) => a.positive_integer - b.positive_integer);
  const values = mapped.map(row => row.positive_integer);
  const bound = order - largestGap.distance + 1;
  if (values[0] !== 1 || values[values.length - 1] !== bound) {
    throw new Error("largest-gap positive interval invariant failed");
  }

  return {
    schema: "erdos241.bose_chowla_b3/v1",
    status: "EXACT_CONSTRUCTED_B3_SET",
    prime: p,
    order_of_sums: 3,
    cubic_coefficients: polynomial,
    field_size: fieldSize,
    cyclic_modulus: order,
    prime_certificate: {
      trial_divisor_limit: Math.floor(Math.sqrt(p)),
      trial_remainders: primeTests
    },
    irreducibility_certificate: {
      degree: 3,
      monic: true,
      base_field_root_values: rootValues,
      reason: "a reducible cubic over a field has a linear factor"
    },
    field_encoding: {
      basis: ["1", "alpha", "alpha^2"],
      code: "c0 + prime*c1 + prime^2*c2",
      coefficient_order: "constant, linear, quadratic",
      reduction: "alpha^3 = -f0 - f1*alpha - f2*alpha^2 modulo prime"
    },
    multiplicative_order_factorization: orderFactorization,
    generator_search: {
      mode: automatic ? "increasing_codes_outside_base_field" : "supplied_code",
      automatic_first_code: automatic ? p : null,
      candidate_records: candidateRecords,
      selected_code: theta,
      selected_coefficients: thetaCoordinates
    },
    degree_three_certificate: {
      basis_columns: [[1, 0, 0], thetaCoordinates, squareCoordinates],
      theta_squared_code: thetaSquared,
      determinant_mod_prime: determinant,
      determinant_nonzero: true
    },
    power_cycle: {
      exponent_start: 0,
      exponent_end_inclusive: order - 1,
      codes: powers,
      unique_nonzero_codes: powers.length,
      next_code_after_cycle: current,
      interpretation: "codes[e] is theta^e; the complete table is invertible to discrete logs"
    },
    affine_offset_exponents: offsets,
    canonical_residues: residues,
    interval_lift: {
      largest_gap: largestGap,
      all_cyclic_gaps: gaps,
      tied_largest_gaps: gaps.filter(gap => gap.distance === largestGap.distance),
      start_residue: start,
      residue_translation: residueMod(1 - start),
      mapping: "b(a) = ((a - start_residue) mod cyclic_modulus) + 1",
      values,
      mapped_elements: mapped,
      minimum: 1,
      maximum: bound,
      optimal_among_cyclic_cuts_of_this_set: true,
      optimized_over_field_choices_or_unit_multipliers: false
    },
    theorem_consequences: {
      cardinality: p,
      repetitions_in_triples_allowed: true,
      equal_sums_identify_multisets: true,
      modular_B3: true,
      positive_integer_B3: true,
      unordered_triples_with_repetition: p * (p + 1) * (p + 2) / 6,
      distinct_triple_sum_residues: p * (p + 1) * (p + 2) / 6,
      triple_sums_enumerated: false,
      finite_lower_bound: { notation: "f(N)", N: bound, at_least: p },
      extremal_equality_claimed: false,
      asymptotic_improvement_claimed: false,
      external_frontier_claimed: false
    },
    limits: { ...BOSE_CHOWLA_B3_LIMITS },
    work
  };
}

module.exports = { constructBoseChowlaB3, BOSE_CHOWLA_B3_LIMITS };
