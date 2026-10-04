# Erdős 241 — explicit finite Bose–Chowla B3 construction

Status: **PUBLIC PRIME-FIELD CUBIC API / COMPLETE FINITE CERTIFICATE / ASYMPTOTIC QUESTION OPEN**.

Erdős 241 asks whether the largest $B_3$ subset of $\{1,\ldots,N\}$ has size asymptotic to $N^{1/3}$. A $B_3$ set permits repeated summands: equal three-term sums must have identical multisets, with reorderings treated as the same representation.

This directory makes the classical Bose–Chowla finite-field construction usable in connected V8. The API validates a monic cubic over a bounded prime field, certifies a primitive element and its degree-three basis, retains the complete power/discrete-log table, and maps its modular set to a short positive interval.

| File | Purpose |
|---|---|
| [bose_chowla_b3.cjs](bose_chowla_b3.cjs) | Public bounded constructor, exact field/order/degree evidence and largest-gap interval lift. |
| [BOSE_CHOWLA_B3_API.md](BOSE_CHOWLA_B3_API.md) | Source conventions, classical construction argument, exact mapping, input/resource limits and actual results. |
| [prime13_cubic_b3_construction.json](prime13_cubic_b3_construction.json) | Complete request, all 2,196 power-cycle entries, every candidate/offset/gap witness, output set and source identities. |

## Actual new set

For $p=13$ and $F(T)=T^3-2$, the constructor selects $\theta=7+\alpha$ in $\mathbb F_{13}[\alpha]/(\alpha^3-2)$. It gives

$$
B=\{1,75,214,574,616,724,862,963,1322,1408,1454,1527,1802\}
$$

and therefore the finite lower bound

$$
f(1802)\ge13.
$$

The set is $B_3$ modulo 2196, hence also under ordinary integer addition. The classical polynomial argument certifies all 455 unordered triples with repetition. Their sums are not enumerated. A largest cyclic gap of 395 gives interval length 1802, optimal only among cuts of this particular residue set.

The single new call used 2,368 field multiplications. Every field-cycle entry and all 13 base-field-offset/discrete-log identities are retained, so a later consumer can reuse them directly. No accepted example, earlier Sidon enumeration or asymptotic bound was rerun.

## Attribution and scope

The construction is due to **R. C. Bose and S. Chowla**, *Theorems in the additive theory of numbers*, Comment. Math. Helv. 37 (1962/63), 141–147. The guide links their original author report and Nathanson's precise author-primary restatement. It binds the positive-set/multiset convention to the inspected FormalConjectures source.

This implementation covers prime fields of degree three within explicit runtime limits. It does not claim an exact extremal value, a new external record, an asymptotic improvement, the full conjecture, or priority for the classical method. No sponsor submission or payment is involved.
