# PPL003 / Erdős 50: exact totient-density bounds

This directory provides a bounded reusable index for the distribution

$$
f(c)=\lim_{X\to\infty}\frac1X
\#\{1\le n\le X:\varphi(n)/n<c\}.
$$

The first eleven primes, with a complete sieve through 4096, give the outward enclosure

$$
0.5103142093\le f(1/2)\le0.5243209606.
$$

The density of $1/2\le\varphi(n)/n<3/4$ is between 0.1629740801 and
0.1951750149. Exact fractions and every source contribution are retained.

| File | Contents |
|---|---|
| [totient_density_index.cjs](totient_density_index.cjs) | Exact weighted atoms, saved-state loading, prime appends, density/interval bounds and atom pages |
| [TOTIENT_DENSITY_API.md](TOTIENT_DENSITY_API.md) | Complete CRT/tail/endpoint/rounding proof, API contract, sources and evidence limits |
| [finite_prime_density_bounds.json](finite_prime_density_bounds.json) | All 4,095 atom rows, 564 prime records, 1,115 upper contributions, five queries and actual operation counts |

CRT supplies exact finite-prime atom masses. A conditional tail estimate bounds
the contribution of omitted primes to the full limiting distribution. Fixed-basis
smooth integers have density zero, so a finite atom exactly at the threshold can
enter the lower bound even though the original distribution uses a strict inequality.

One actual consumer constructed the first ten primes, reopened the saved table,
appended prime 31, then reopened again for an interval and six-row page. The final
reader reused the half-threshold bound and computed only the new three-quarter
bound. It performed no sieve, atom construction or old bound recomputation.
No integer totients or primorial residues were enumerated in any phase.

The [retrieved formal statement](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/50.lean)
labels the positive within-derivative question open; its theorem bodies contain
placeholder proofs. A bounded primary-literature check did not independently
confirm current status. The guide cites an accessible primary research account
of existence and continuity, and proves its enclosure first for liminf/limsup.
This finite API does not resolve the derivative question or assert novelty,
formal verification, prize eligibility or acceptance.

Restoration is structural only and requires a source with established provenance.
The complete published data records the exact implementation identity and contains
every prior basis needed to follow its cached results.

Operation: `ERDOS50-TOTIENT-DENSITY-20261004-7CA6`.
[Original claim](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1791133410709209).
