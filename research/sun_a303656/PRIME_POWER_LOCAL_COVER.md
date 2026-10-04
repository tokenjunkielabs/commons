# A303656: prime-power coverage and the finite-offset limit

**Analytic result.** For every prime power $p^k$, every residue is represented by
$x^2+y^2+3^c+5^d$ even with $c,d\in\{0,1\}$. This local statement cannot be combined across prime powers by choosing the exponents independently. In fact, every fixed finite set of exact exponent pairs fails for infinitely many positive integers.

These are elementary local-coverage and route-exclusion lemmas. They neither prove nor disprove Sun's original conjecture, which permits arbitrary nonnegative exponents. No novelty claim is made.

This October 4 continuation belongs to [#14608](https://github.com/woahwhattheheck/commons/issues/14608). ZOL-C4N9 retains the original research scope; the exact harness, finite evidence and review/transport credit from [#14639](https://github.com/woahwhattheheck/commons/pull/14639) are preserved. No source or recorded computation from that carrier is changed or replayed.

## 1. Statement and quantifiers

The [primary OEIS statement](https://oeis.org/A303656), read on October 4, asks whether every integer $n>1$ has an equality

$$
n=x^2+y^2+3^c+5^d
$$

with $x,y,c,d$ nonnegative integers. The results below concern congruences or restricted exact-offset strategies, with different quantifiers.

**Theorem 1 — every individual prime power is covered.** For every prime $p$, every integer $k\ge1$ and every integer $n$, there are nonnegative integers $x,y$ and exponents $c,d\in\{0,1\}$ such that

$$
n\equiv x^2+y^2+3^c+5^d\pmod{p^k}.
\tag{1}
$$

The four possible offsets are

$$
S=\{3^c+5^d:c,d\in\{0,1\}\}=\{2,4,6,8\}.
\tag{2}
$$

The choice of $(c,d)$ in (1) may depend on the prime power. There is no claim here that one choice works simultaneously for every prime power dividing a composite modulus. There is also no magnitude bound on the nonnegative representatives $x,y$, so (1) is not an equality representation of $n$.

## 2. Odd prime powers

We first prove a standard elementary fact in the needed form.

**Unit lemma.** If $p$ is odd and $p\nmid u$, then $u$ is a sum of two squares modulo $p^k$ for every $k\ge1$.

Let $Q$ be the set of square residues modulo $p$, including zero. It has $(p+1)/2$ elements. The sets $Q$ and $u-Q$ therefore have total size $p+1$ inside a field with $p$ elements, so they intersect. Thus

$$
u\equiv a^2+b^2\pmod p.
$$

Because $u$ is nonzero modulo $p$, at least one of $a,b$ is nonzero. Interchange them if necessary to have $p\nmid a$.

Suppose $a_j^2+b^2\equiv u\pmod{p^j}$, with $a_j\equiv a\pmod p$. Replacing $a_j$ by $a_j+t p^j$ changes the sum of squares modulo $p^{j+1}$ by

$$
2a_jt p^j.
$$

The coefficient $2a_j$ is invertible modulo $p$, so exactly one residue $t\bmod p$ supplies the next required digit. Induction lifts the representation to every $p^k$. Choosing residue representatives gives nonnegative coordinates. This proves the lemma without a restriction on $p\bmod4$.

Now the two available offsets

$$
2=3^0+5^0,\qquad 4=3^1+5^0
$$

differ by $2$. An odd prime cannot divide both $n-2$ and $n-4$. At least one of these remainders is a unit modulo $p$, and the unit lemma applies. This proves Theorem 1 for every odd prime, including $p=3$ and $p=5$.

## 3. Powers of two

We use the following elementary lifting fact.

**Square-root lemma.** Every integer $u\equiv1\pmod8$ is a square modulo $2^k$ for every $k\ge1$.

For $k\le3$, the square $1$ suffices. If odd $a$ satisfies $a^2\equiv u\pmod{2^j}$ with $j\ge3$, put

$$
a'=a+\varepsilon2^{j-1},\qquad \varepsilon\in\{0,1\}.
$$

Then

$$
(a')^2\equiv a^2+\varepsilon a2^j\pmod{2^{j+1}},
$$

because $2j-2\ge j+1$. As $a$ is odd, the two choices of $\varepsilon$ select the two possible next square digits. One gives $(a')^2\equiv u\pmod{2^{j+1}}$. Induction proves the finite-modulus assertion.

The following table chooses an offset from (2). The last column fixes a small second square so that the remaining quantity is $1$ modulo $8$.

| $n\bmod8$ | $(c,d)$ | Offset $s=3^c+5^d$ | $(n-s)\bmod8$ | Choose $y$ |
|---:|:---:|---:|---:|---:|
| 0 | $(0,1)$ | 6 | 2 | 1 |
| 1 | $(1,0)$ | 4 | 5 | 2 |
| 2 | $(1,1)$ | 8 | 2 | 1 |
| 3 | $(0,0)$ | 2 | 1 | 0 |
| 4 | $(0,0)$ | 2 | 2 | 1 |
| 5 | $(1,0)$ | 4 | 1 | 0 |
| 6 | $(1,0)$ | 4 | 2 | 1 |
| 7 | $(0,0)$ | 2 | 5 | 2 |

In every row, $n-s-y^2\equiv1\pmod8$. The square-root lemma supplies $x$ modulo every $2^k$. Hence

$$
n\equiv x^2+y^2+s\pmod{2^k},
$$

which completes Theorem 1. Negative intermediate integers cause no problem in a congruence; the result does not assert a nonnegative equality remainder.

## 4. A composite obstruction for the same four offsets

The local theorem uses only $S=\{2,4,6,8\}$, but that same finite palette is not universal modulo a suitable composite.

Choose $n$ to satisfy

| Offset $s$ | Assigned prime $p_s$ | Required congruence |
|---:|---:|:---|
| 2 | 3 | $n\equiv5\pmod9$ |
| 4 | 7 | $n\equiv11\pmod{49}$ |
| 6 | 11 | $n\equiv17\pmod{121}$ |
| 8 | 19 | $n\equiv27\pmod{361}$ |

The moduli are pairwise coprime, so the Chinese remainder theorem gives one nonempty residue class modulo

$$
M=9\cdot49\cdot121\cdot361=19\,263\,321.
\tag{3}
$$

An explicit choice of the residue class is

$$
n=17\,692\,637+19\,263\,321t,\qquad t\ge0.
$$

Indeed, the initial value has remainders $5,11,17,27$ modulo $9,49,121,361$, respectively. Every displayed member is positive and greater than $8$.

For every row,

$$
n-s\equiv p_s\pmod{p_s^2}.
\tag{4}
$$

A prime $p\equiv3\pmod4$ has no square root of $-1$ modulo $p$: such a root would have multiplicative order $4$, which cannot divide $p-1$. Consequently,

$$
p\mid x^2+y^2\quad\Longrightarrow\quad p\mid x\ \text{and}\ p\mid y.
\tag{5}
$$

Indeed, if $y$ were nonzero modulo $p$, dividing by $y^2$ would produce a square root of $-1$; if $y$ is zero, so is $x$.

If $x^2+y^2\equiv p\pmod{p^2}$, equation (5) forces the left side to be zero modulo $p^2$, a contradiction. Thus (4) prevents $n-s$ from being a sum of two squares modulo its assigned $p_s^2$.

Every one of the four offsets is excluded by a row. Therefore this entire residue class modulo $M$ has no representation

$$
n\equiv x^2+y^2+3^c+5^d\pmod M
\quad\text{with }c,d\in\{0,1\}.
\tag{6}
$$

It contains infinitely many positive integers greater than $8$, none of which has an equality representation using that finite palette. The obstruction concerns the four offsets only. Larger exponents may supply different offsets, so these integers are not counterexamples to A303656.

## 5. No fixed finite list of exact exponent pairs can suffice

The preceding construction is not special to four offsets.

**Theorem 2 — finite-offset exclusion.** For every nonempty finite set of integer offsets $S$, there is an arithmetic progression of infinitely many positive integers $n$ such that $n-s$ is not a sum of two integer squares for any $s\in S$.

Assign a distinct prime $p_s\equiv3\pmod4$ to each $s\in S$ and impose

$$
n\equiv s+p_s\pmod{p_s^2}
\qquad(s\in S).
\tag{7}
$$

There are arbitrarily many such primes. For completeness, if $q_1,\ldots,q_t$ were a complete finite list, the integer $4q_1\cdots q_t-1$ would be $3$ modulo $4$ and divisible by none of the $q_i$. Its prime factorization must contain a prime that is $3$ modulo $4$, since a product consisting only of primes $1$ modulo $4$ and even multiplicities of primes $3$ modulo $4$ would be $1$ modulo $4$. This supplies a new prime, a contradiction.

The moduli in (7) are pairwise coprime. CRT supplies one residue class modulo $\prod_{s\in S}p_s^2$. For every member of that class and every $s$, equation (4) and the argument following (5) exclude the offset. The class has infinitely many positive members exceeding $\max S$, so negative equality remainders are not the reason for the failure. This proves Theorem 2.

In particular, for any fixed nonnegative integers $C,D$, apply the theorem to the distinct offsets in

$$
S_{C,D}=\{3^c+5^d:0\le c\le C,\ 0\le d\le D\}.
$$

There are infinitely many positive integers with no representation inside that exponent rectangle. More generally, any fixed finite list of exact exponent pairs fails. If A303656 is true, representations cannot be supplied for all $n$ by one finite list independent of $n$.

This does not exclude a finite description of infinitely many exponent pairs, a period-class argument, or an identity whose chosen exponents grow with $n$. Those are different strategies.

## 6. Consequences for the existing research program

The original receipt covers 1,151 specified moduli and a bounded greedy exponent-grid experiment. Those recorded calculations remain unchanged and are not re-executed here. The present proof adds two unbounded analytic conclusions:

- Searching individual prime powers for an A303656 residue obstruction cannot succeed, regardless of their size. Theorem 1 already covers all of them.
- A fixed finite set of exact exponent choices cannot prove the universal equality statement. Theorem 2 gives infinitely many failures for every such set.

A composite-modulus search must retain the same exponent pair across all prime-power components. CRT can combine the square coordinates after that compatibility is established; it cannot independently choose incompatible exponents at different components. Section 4 demonstrates this failure of the naive combination argument on the very palette that proves Theorem 1.

The original unrestricted composite-modulus question remains open in this note. The finite greedy cover remains necessary evidence only: divisibility without a forced odd valuation is insufficient, and a bounded exponent rectangle does not cover all exponents.

The proof is elementary and written out in full. No parameter census, new verifier, test, native execution, formal-kernel verification, external review or prize claim supplies a step. The original conjecture remains unsolved by this carrier.

## References and retained artifacts

- **Primary target:** [OEIS A303656](https://oeis.org/A303656), October 4 source read. The conjecture permits arbitrary nonnegative exponents; its finite verification record is not a proof.
- **Original research scope:** [#14608](https://github.com/woahwhattheheck/commons/issues/14608), ZOL-C4N9, and the [original work thread](https://tokenjunkielabs.slack.com/archives/C0BV7KHRGF7/p1789442649697189).
- **Accepted harness and finite evidence:** [#14639](https://github.com/woahwhattheheck/commons/pull/14639), exact source head 11d643d224cc815949603ebeb03e7e25fd017656. Scree-Zeta's original arithmetic review and the transport/finalization contributors retain their credit in that history.
- **Unchanged local search source:** [modular.py](modular.py), blob be024b43adab61a0c6d0ad51449ffbe6a937c5c5.
- **Unchanged finite receipt:** [negative_evidence_v1.json](evidence/negative_evidence_v1.json), blob 7861023c7d0143ff34d0bfdae2bd98ab50ac7616.
