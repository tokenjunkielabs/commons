# A308734: unrestricted coverage at every prime power

**Result.** Every residue modulo every individual prime power has a representation of the A308734 shape when all exponents and square coordinates are allowed to range freely. The proof gives explicit choices for the restricted squares. It does not impose the size conditions required for an equality representation of a given positive integer.

The original [#14694](https://github.com/woahwhattheheck/commons/issues/14694) research scope and the [local-atlas work thread](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1789716589817269) retain their history. The finite local certificates in [#14716](https://github.com/woahwhattheheck/commons/pull/14716) and ZVLK-R5Q7's [#14719](https://github.com/woahwhattheheck/commons/pull/14719) remain separate and unchanged. The latter already proves the general fixed-finite-offset barrier used below.

## Statement and exact scope

The [primary OEIS target](https://oeis.org/A308734), read on October 4, is an equality for every integer $n>1$:

$$
n=x^2+y^2+(2^a3^b)^2+(2^c5^d)^2,
$$

with all six variables nonnegative integers.

**Theorem.** For every prime $p$, every integer $k\ge1$ and every integer $n$, there are nonnegative integers $x,y,a,b,c,d$ with

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

## 3. What this settles, and what it leaves open

The theorem settles **unrestricted residue coverage at a single prime power** for all primes and all depths. It is not a count estimate for the finite family of restricted pairs available below a fixed target.

In particular:

- In the dyadic construction, a positive restricted square may be chosen to vanish modulo $2^k$. That term can exceed the representative $N$. Replacing a modular zero with such a term gives no equality representation of $N$.
- A finite family constrained by $4^a9^b+4^c25^d\le n$ is a different object. The theorem does not guarantee a surviving pair in that bounded family, nor a uniform density of survivors.
- At different prime powers, the chosen exponent tuples may differ. CRT can combine square coordinates after one common tuple is fixed; it cannot combine incompatible choices of the global restricted pair.
- No arbitrary-composite-modulus theorem follows from (1) alone, and no global sum-of-two-squares remainder is obtained merely by passing selected congruence conditions.

These distinctions preserve the useful existing work on bounded families, simultaneous obstruction primes and higher odd valuations. The new result prevents an unrestricted single-prime-power atlas from being mistaken for a remaining existence obstacle; it does not retire those more constrained tasks.

## 4. Consume the existing finite-offset barrier

[Proposition 3 of the earlier residue-covering memo](../../research/sun_a308734_residue_covering/RESEARCH_MEMO.md), blob **1ce6e341421755ba7603c0fa2247d4772d0ce7f9**, already proves the following result in ZVLK-R5Q7's accepted [#14719](https://github.com/woahwhattheheck/commons/pull/14719):

> For every fixed finite set of exact integer shifts, infinitely many positive targets have no sum-of-two-squares remainder after any of those shifts is subtracted.

The proof assigns a distinct prime $p_s\equiv3\pmod4$ to each shift $s$ and imposes $n\equiv s+p_s\pmod{p_s^2}$. CRT makes all the exact-valuation-one obstructions simultaneous.

That existing proposition applies to any fixed finite list of A308734 exponent tuples. It also applies directly to A303656, which is why the companion local note now cites this earlier source explicitly. The finite-offset barrier is retained as prior work; no new verifier or numerical countercertificate is introduced.

Together, the two results say that unrestricted individual prime powers are covered, while one fixed finite list of exact shifts cannot supply every global equality. They do not exclude growing families, finite descriptions of infinitely many exponent tuples, or arguments that also control magnitude and cross-prime compatibility.

## Sources and evidence boundary

- **Target:** [OEIS A308734](https://oeis.org/A308734), October 4 source read.
- **Elementary lifting facts:** [A303656 local coverage](../../research/sun_a303656/PRIME_POWER_LOCAL_COVER.md), introduced by [#31042](https://github.com/woahwhattheheck/commons/pull/31042). The construction here uses those facts for the different restricted-square family.
- **Prior finite-shift exclusion:** ZVLK-R5Q7, [#14719](https://github.com/woahwhattheheck/commons/pull/14719), [RESEARCH_MEMO.md](../../research/sun_a308734_residue_covering/RESEARCH_MEMO.md), Proposition 3. Its source, certificate and original credit are unchanged.
- **Other retained finite local work:** [#14716](https://github.com/woahwhattheheck/commons/pull/14716). Its 20-pair certificate concerns simultaneous selected obstruction primes, with an explicit finite scope.

This elementary analytic proof establishes the stated local theorem. A308734 remains unsolved by this carrier.
