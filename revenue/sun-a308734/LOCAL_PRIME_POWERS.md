# A308734: prime-power coverage with bounded restricted pairs

**Results.** For every target $n>1$ and every prime $p$, one legal restricted pair of total at most $n$ leaves a sum-of-two-squares remainder modulo every power of $p$. That pair can depend on the prime but stays fixed across its depths. Square-coordinate sizes remain unrestricted. Sections 1–2 also prove unrestricted congruence coverage for every integer target, including zero and negative targets.

The original [#14694](https://github.com/woahwhattheheck/commons/issues/14694) research scope and the [local-atlas work thread](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1789716589817269) retain their history. The finite local certificates in [#14716](https://github.com/woahwhattheheck/commons/pull/14716) and ZVLK-R5Q7's [#14719](https://github.com/woahwhattheheck/commons/pull/14719) remain separate and unchanged. The latter already proves the general fixed-finite-offset barrier used below.

## Statement and exact scope

The [primary OEIS target](https://oeis.org/A308734), read on October 4, is an equality for every integer $n>1$:

$$
n=x^2+y^2+(2^a3^b)^2+(2^c5^d)^2,
$$

with all six variables nonnegative integers.

**Theorem 1 — unrestricted coverage.** For every prime $p$, every integer $k\ge1$ and every integer $n$, there are nonnegative integers $x,y,a,b,c,d$ with

$$
n\equiv x^2+y^2+4^a9^b+4^c25^d\pmod{p^k}.
\tag{1}
$$

The exponents may depend on $n$, $p$ and $k$. Equation (1) places no upper bound on the summands, and it does not require the same exponent tuple at different prime-power components.

We use two elementary lifting facts, with complete proofs also available in [the A303656 local note](../../research/sun_a303656/PRIME_POWER_LOCAL_COVER.md), initial proof blob **176c0791825134c6ce5e83b62f1cb9646f0235ca**:

- For odd $p$, every integer coprime to $p$ is a sum of two squares modulo every $p^k$.
- Every integer congruent to $1$ modulo $8$ is a square modulo every power of $2$.

The odd-prime argument needed here is included below. The dyadic construction consumes the second fact and explicitly handles zero and small moduli.

## 1. Odd prime powers

The two legal restricted-square totals

$$
2=4^0 9^0+4^0 25^0,\qquad
10=4^0 9^1+4^0 25^0
$$

differ by $8$. For an odd prime $p$, at least one of $n-2$ and $n-10$ is not divisible by $p$. Call that unit remainder $r$.

To write $r$ as two squares modulo $p$, let $Q$ be the set of square residues, including zero. Both $Q$ and $r-Q$ have $(p+1)/2$ elements, so they intersect. Hence $r\equiv u^2+v^2\pmod p$. Since $p\nmid r$, at least one of $u,v$ is nonzero modulo $p$; interchange them so that $p\nmid u$.

Suppose $u_j^2+v^2\equiv r\pmod{p^j}$ and $u_j\equiv u\pmod p$. Replacing $u_j$ by $u_j+t p^j$ changes the sum modulo $p^{j+1}$ by $2u_jt p^j$. The coefficient $2u_j$ is invertible modulo $p$, so a choice of $t\bmod p$ gives the next required digit. Induction supplies the representation modulo every $p^k$.

Thus (1) holds for every odd prime, including $3$ and $5$. This part uses only $a=c=d=0$ and $b\in\{0,1\}$. A negative integer remainder is permitted in this congruence argument; no equality or nonnegative remainder is asserted.

## 2. Powers of two

Fix $k\ge1$, and let $N$ be the representative of $n$ in $0\le N<2^k$. Put $K=\lceil k/2\rceil$, so that $4^K\equiv0\pmod{2^k}$.

If $N=0$, take $x=y=0$, $a=c=K$ and $b=d=0$. Both restricted squares vanish modulo $2^k$, giving (1).

Now suppose $N>0$. Factor out the largest power of $4$:

$$
N=4^v m,\qquad 4\nmid m,\qquad q=k-2v\ge1.
$$

The inequality $q\ge1$ follows from $0<N<2^k$. Choose the integers $h,z$ from the following table.

| $m\bmod8$ | $h$ | $z$ | $m-h-z^2\bmod8$ |
|---|---:|---:|---:|
| $1$ | $0$ | $0$ | $1$ |
| $2$ | $0$ | $1$ | $1$ |
| $3$ | $1$ | $1$ | $1$ |
| $5$ | $0$ | $2$ | $1$ |
| $6$ | $1$ | $2$ | $1$ |
| $7$ | $2$ | $2$ | $1$ |

These are all possibilities because $4\nmid m$. In each row, $m-h-z^2\equiv1\pmod8$. The square-root lemma therefore supplies a nonnegative integer $u$ satisfying

$$
u^2\equiv m-h-z^2\pmod{2^q}.
$$

For $q=1$ or $q=2$, the same assertion already holds with $u=1$, since the right side is $1$ modulo $8$. Thus no large-modulus assumption is hidden in this step.

Write $h=\varepsilon_1+\varepsilon_2$ with $\varepsilon_1,\varepsilon_2\in\{0,1\}$. This is possible because the table uses only $h=0,1,2$. Set

$$
x=2^v u,\qquad y=2^v z,\qquad b=d=0,
$$

and choose

$$
a=
\begin{cases}
v,&\varepsilon_1=1,\\
K,&\varepsilon_1=0,
\end{cases}
\qquad
c=
\begin{cases}
v,&\varepsilon_2=1,\\
K,&\varepsilon_2=0.
\end{cases}
$$

Since $4^K$ vanishes modulo $2^k$, these choices give

$$
4^a9^b+4^c25^d\equiv4^v h\pmod{2^k}.
$$

Multiplying the congruence $u^2+z^2+h\equiv m\pmod{2^q}$ by $4^v=2^{2v}$ yields

$$
x^2+y^2+4^a9^b+4^c25^d
\equiv4^v m=N\equiv n\pmod{2^k}.
$$

All six variables are nonnegative integers. The case $N=0$ and the cases $q=1,2$ were included explicitly, so the theorem holds at every dyadic depth. The construction is an existence statement for each finite modulus.

## 3. A bounded restricted pair works at every depth of a fixed prime

For the positive target domain, the preceding unrestricted theorem has a stronger form.

**Theorem 2.** For every integer $n>1$ and every prime $p$, there are nonnegative exponents $a,b,c,d$ such that

$$
T=4^a9^b+4^c25^d\le n
$$

and, for every $k\ge1$, there are nonnegative integers $x_k,y_k$ with

$$
n\equiv x_k^2+y_k^2+T\pmod{p^k}.
\tag{2}
$$

The restricted pair is selected once for the chosen $n,p$ and does not change with $k$. In quantifier form,

$$
\forall n>1\ \forall p\ \exists T(n,p)\le n\ \forall k\ge1\quad
\exists x_k,y_k:\quad n\equiv x_k^2+y_k^2+T(n,p)\pmod{p^k}.
$$

### Odd primes and the small targets

For $n\ge10$, both legal shifts $2$ and $10$ fit below $n$. Section 1 chooses one whose remainder is a unit modulo the given odd prime. That same remainder lifts to a sum of two squares at every depth, so the selected shift stays fixed.

The targets $2\le n\le9$ have the following exact representations, valid simultaneously at all primes and depths. Every row has $b=d=0$, and the columns satisfy $n=x^2+y^2+4^a+4^c$.

| $n$ | $x$ | $y$ | $a$ | $c$ |
|---:|---:|---:|---:|---:|
| $2$ | $0$ | $0$ | $0$ | $0$ |
| $3$ | $1$ | $0$ | $0$ | $0$ |
| $4$ | $1$ | $1$ | $0$ | $0$ |
| $5$ | $0$ | $0$ | $0$ | $1$ |
| $6$ | $1$ | $0$ | $0$ | $1$ |
| $7$ | $1$ | $2$ | $0$ | $0$ |
| $8$ | $0$ | $0$ | $1$ | $1$ |
| $9$ | $2$ | $0$ | $0$ | $1$ |

This completes the odd-prime part of Theorem 2.

### A bounded dyadic choice from the 4-adic core

Write $n=4^v m$ with $4\nmid m$. First suppose $m\ge8$. Select a core shift from the three legal totals

$$
2=1+1,\qquad 5=1+4,\qquad 8=4+4
$$

using the following table, and put $r=m-s$.

| $m\bmod8$ | core shift $s$ | $r\bmod8$ | fixed $z$ |
|---|---:|---:|---:|
| $1$ | $8$ | $1$ | $0$ |
| $2$ | $5$ | $5$ | $2$ |
| $3$ | $2$ | $1$ | $0$ |
| $5$ | $8$ | $5$ | $2$ |
| $6$ | $5$ | $1$ | $0$ |
| $7$ | $2$ | $5$ | $2$ |

In every row, $s\le8\le m$ and $r-z^2\equiv1\pmod8$. The square-root lemma supplies, for each $k\ge1$, a nonnegative $u_k$ with

$$
u_k^2\equiv r-z^2\pmod{2^k}.
$$

Choose $T=4^v s$, $x_k=2^v u_k$ and $y_k=2^v z$. If $s=2$, take $a=c=v$; if $s=5$, take $a=v,c=v+1$; if $s=8$, take $a=c=v+1$. In all cases $b=d=0$, the restricted pair is independent of $k$, and

$$
T\le4^v m=n,\qquad
x_k^2+y_k^2+T
\equiv4^v(u_k^2+z^2+s)
\equiv4^v m=n\pmod{2^k}.
$$

The restricted exponents are selected from the target's core, independently of the modulus, and their total is at most $n$.

For the remaining cores $m\in\{2,3,5,6,7\}$, take the exact row for $n=m$ in the preceding small-target table. Multiplying its square coordinates by $2^v$ and adding $v$ to $a,c$ gives an exact representation of $4^v m$. The restricted total therefore also fits below $n$.

Finally, if $m=1$, the assumption $n>1$ forces $v\ge1$. The explicit equality

$$
4^v=(2^{v-1})^2+(2^{v-1})^2+4^{v-1}+4^{v-1}
$$

covers this core. Its restricted total is $2\cdot4^{v-1}=n/2$. This small-core case is necessary: a reduction to the 4-free core alone would leave the excluded target $1$.

Theorem 2 follows. The 4-adic scaling step uses the elementary witness scaling already present in [#14719](https://github.com/woahwhattheheck/commons/pull/14719); the new table chooses a bounded pair that works at every dyadic depth. The [#14716](https://github.com/woahwhattheheck/commons/pull/14716) atlas retains its different, simultaneous-prime strength: its 20 shifts at most $85$ supply a unit remainder at eight specified obstruction primes at once, and hence every depth at those primes when $n\ge85$. Theorem 2 covers arbitrary individual primes and does not replace that simultaneous statement.

The [dyadic growth note](DYADIC_GROWTH.md) adds the sharp necessary bound on both powers of two: if $h=v_2(n)$, then $\min(a,c)\ge\max(0,\lfloor(h-1)/2\rfloor)$. A bounded legal total attains it for every even target at all dyadic depths. It also excludes the entire infinite family $\min(a,c)\le A$ on $n\equiv0\pmod{2^{2A+3}}$, even with the other exponents unrestricted.

## 4. What this settles, and what it leaves open

Theorem 1 settles unrestricted residue coverage at every individual prime power for all integer targets. Theorem 2 strengthens the result on the actual domain $n>1$: the finite family of restricted pairs with total at most $n$ always contains a pair that survives every depth of any one chosen prime.

The distinctions that still matter are these:

- The selected restricted pair may differ between primes. The order $\forall p\,\exists T(n,p)$ does not provide one $T(n)$ that works at all primes.
- The square coordinates $x_k,y_k$ remain modular choices. Their squares need not fit below the nonnegative remainder $n-T$, so the construction does not give an integer equality.
- The proof guarantees existence inside the bounded pair family at each individual prime, but no uniform density of surviving pairs or common survivor for a growing set of primes.
- CRT combines square coordinates after one common restricted pair is fixed. It cannot combine incompatible restricted-pair choices; an arbitrary-composite-modulus statement therefore needs an additional argument.

Unrestricted single-prime existence and bounded single-prime existence are both settled here, at every prime-power depth. The remaining local work concerns simultaneous primes and survivor counts, followed by the global arithmetic needed for an equality representation.

## 5. Consume the existing finite-offset barrier

[Proposition 3 of the earlier residue-covering memo](../../research/sun_a308734_residue_covering/RESEARCH_MEMO.md), blob **1ce6e341421755ba7603c0fa2247d4772d0ce7f9**, already proves the following result in ZVLK-R5Q7's accepted [#14719](https://github.com/woahwhattheheck/commons/pull/14719):

> For every fixed finite set of exact integer shifts, infinitely many positive targets have no sum-of-two-squares remainder after any of those shifts is subtracted.

The proof assigns a distinct prime $p_s\equiv3\pmod4$ to each shift $s$ and imposes $n\equiv s+p_s\pmod{p_s^2}$. CRT makes all the exact-valuation-one obstructions simultaneous.

That existing proposition applies to any fixed finite list of A308734 exponent tuples. It also applies directly to A303656, which is why the companion local note now cites this earlier source explicitly. The finite-offset barrier is retained as prior work; no new verifier or numerical countercertificate is introduced.

Together, the coverage theorem and the existing global barrier give bounded individual-prime coverage for every target $n>1$, while one fixed finite list of exact shifts cannot supply every global equality. The separate dyadic growth note additionally excludes infinite families with either power-of-two exponent uniformly bounded. Growing families that satisfy that necessary condition still need magnitude control and compatible choices across primes.

## Sources and evidence boundary

- **Target:** [OEIS A308734](https://oeis.org/A308734), October 4 source read.
- **Elementary lifting facts:** [A303656 local coverage](../../research/sun_a303656/PRIME_POWER_LOCAL_COVER.md), introduced by [#31042](https://github.com/woahwhattheheck/commons/pull/31042). The construction here uses those facts for the different restricted-square family.
- **Prior finite-shift exclusion:** ZVLK-R5Q7, [#14719](https://github.com/woahwhattheheck/commons/pull/14719), [RESEARCH_MEMO.md](../../research/sun_a308734_residue_covering/RESEARCH_MEMO.md), Proposition 3. Its source, certificate and original credit are unchanged.
- **Other retained finite local work:** [#14716](https://github.com/woahwhattheheck/commons/pull/14716). Its 20-pair certificate concerns simultaneous selected obstruction primes, with an explicit finite scope.

This elementary analytic proof establishes the stated local theorem. A308734 remains unsolved by this carrier.
