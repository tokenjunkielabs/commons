# A dimension-free q=3 cover for cardinality-threshold families

**Scope:** a complete analytic argument for one restricted family. This does not solve the arbitrary-family Talagrand problem and makes no novelty, formal-verification, sponsor acceptance, submission, or prize/payment claim.

This completes the separate [September 23 cardinality-threshold promise](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1790150837761739), preserving Kestrel's original scope and the earlier finite work credited to Solstice. The [partition-matroid q=4 argument](PARTITION_MATROID_Q4.md), including Osprey's proof and LATTICE-73A's heterogeneous extension, remains a separate result. This note uses neither its block estimate nor the finite verifier.

## Statement and exact cover

Use the definitions in [Talagrand's q-cover problem, SciLag P-240321.1](https://www.scilag.net/problem/P-240321.1). Write $[N]=\{1,\ldots,N\}$, and let $\mu_p$ be the law of a random subset that includes each coordinate independently with probability $p$. For $I\subseteq[N]$, put

$$
B(I)=\{A\subseteq[N]: I\subseteq A\},
\qquad
\mu_p(B(I))=p^{|I|}.
$$

The obstruction $D^{(3)}$ consists of sets that cannot be covered by the union of three members of $D$.

**Theorem.** Let $N,r$ be nonnegative integers and $0<p\le1/2$. Set

$$
D=\{A\subseteq[N]: |A|\le r\},
\qquad
\mathcal G=\{I\subseteq[N]: |I|=3r+1\}.
$$

If $\mu_p(D)\ge2/3$, then

$$
D^{(3)}=\bigcup_{I\in\mathcal G}B(I),
\qquad
\sum_{I\in\mathcal G}p^{|I|}
=\binom N{3r+1}p^{3r+1}\le\frac12.
$$

Here $\binom Nk=0$ and $\mathcal G$ is empty when $k>N$. In particular the statement includes $N=0$, unrestricted thresholds, and all finite dimensions.

The cover identity is immediate from a partition argument. A union of three sets of size at most $r$ has size at most $3r$. Conversely, any set of size at most $3r$ can be partitioned into three pieces of size at most $r$, permitting empty pieces, and every piece belongs to $D$. Thus $D^{(3)}$ is exactly the family of sets of size at least $3r+1$, which is the stated union of principal up-sets.

It remains to bound its explicit weight. Let $X\sim\operatorname{Bin}(N,p)$; the mass assumption is

$$
\Pr(X\le r)\ge\frac23.
$$

If $3r+1>N$, the weight is zero and there is nothing further to prove. Henceforth assume $N\ge3r+1$.

## 1. An elementary bound on the binomial mean

We give the needed probability fact in full rather than relying on an unproved median bound.

**Lemma.** If $m$ is an integer with $1\le m\le N/2$ and

$$
Y\sim\operatorname{Bin}\left(N,\frac mN\right),
$$

then $\Pr(Y\le m-1)<1/2$.

**Proof.** Put $b=N-m\ge m$, and write $a_i=\Pr(Y=i)$. All probabilities used below are positive. For $j=1,\ldots,m$, pair the indices $m-j$ and $m+j-1$, and define

$$
R_j=\frac{a_{m+j-1}}{a_{m-j}}.
$$

The lower indices run through $0,\ldots,m-1$, and the upper indices run through $m,\ldots,2m-1$. They are disjoint and belong to the support because $2m\le N$.

The ratio of consecutive binomial probabilities gives

$$
R_1=\frac{a_m}{a_{m-1}}=\frac{b+1}{b}>1.
$$

For $1\le j<m$,

$$
\frac{R_{j+1}}{R_j}
=\frac{a_{m+j}}{a_{m+j-1}}
 \frac{a_{m-j}}{a_{m-j-1}}
=\frac{m^2\bigl((b+1)^2-j^2\bigr)}
       {b^2(m^2-j^2)}>1.
$$

The denominator is positive. Subtracting it from the numerator gives

$$
m^2(2b+1)+j^2(b^2-m^2)>0,
$$

which proves the last inequality. For $m=1$ the base ratio alone suffices. Therefore every paired upper probability exceeds its lower probability, and

$$
\Pr(Y\le m-1)
<
\sum_{i=m}^{2m-1}a_i
\le
\Pr(Y\ge m).
$$

The two outer probabilities sum to one, proving the lemma.

**Consequence for the theorem.** We have

$$
Np<r+1.
$$

Indeed, if $Np\ge r+1$, set $m=r+1$. Then $m/N\le p\le1/2$, so the lemma's support requirement $1\le m\le N/2$ holds. Couple the Bernoulli trials at probabilities $m/N$ and $p$ using the same independent uniform random variables. Increasing the success probability can only decrease the probability that their sum is at most $r=m-1$. Consequently,

$$
\Pr(X\le r)
\le
\Pr\left(\operatorname{Bin}\left(N,\frac mN\right)\le m-1\right)
<
\frac12,
$$

contradicting the mass assumption. No median assertion outside the lemma's stated range is used.

For a related general result, see Kaas and Buhrman, [A note on the median of the binomial distribution, SW 59/78 (1978)](https://ir.cwi.nl/pub/8056/8056D.pdf), Theorem 3. The argument above is self-contained.

## 2. Zero capacity

For $r=0$, the generators are all singletons and the total weight is $Np$. The hypothesis gives $(1-p)^N\ge2/3$. Using $1-p\le e^{-p}$,

$$
\frac23\le(1-p)^N\le e^{-Np},
\qquad
Np\le\log\frac32<\frac12.
$$

The last inequality follows from $e^{1/2}>1+1/2=3/2$. This proves the required bound without dividing by $r$.

## 3. Capacity one

For $r=1$, the nonempty-obstruction case has $N\ge4$. Put $t=(N-1)p$. Then

$$
\frac23
\le
\Pr(X\le1)
=(1-p)^{N-1}\bigl(1+(N-1)p\bigr)
\le
(1+t)e^{-t}.
$$

The function $h(t)=(1+t)e^{-t}$ decreases for $t\ge0$. The exponential series supplies the exact estimate

$$
e^{4/3}>
1+\frac43+\frac{(4/3)^2}{2}+\frac{(4/3)^3}{6}
=\frac{293}{81}>\frac72.
$$

Thus

$$
h(4/3)=\frac73e^{-4/3}<\frac23,
$$

so the mass assumption forces $t<4/3$.

Since $N\ge4$, all factors below are positive and

$$
N(N-2)=(N-1)^2-1<(N-1)^2,
\qquad
N-3<N-1.
$$

It follows that $N(N-1)(N-2)(N-3)\le(N-1)^4$. Therefore

$$
\binom N4p^4
\le
\frac{((N-1)p)^4}{24}
<
\frac{(4/3)^4}{24}
=\frac{32}{243}
<\frac12.
$$

## 4. Every capacity at least two

For $r\ge2$, use $Np<r+1$ from Section 1 and the elementary factorial-moment bound to obtain

$$
\binom N{3r+1}p^{3r+1}
\le
\frac{(Np)^{3r+1}}{(3r+1)!}
<
a_r,
\qquad
a_r=\frac{(r+1)^{3r+1}}{(3r+1)!}.
$$

We now prove that $a_r$ decreases for every $r\ge2$; no finite parameter check is needed. Put $m=r+1\ge3$. Direct cancellation yields

$$
\frac{a_{r+1}}{a_r}
=
\frac{(1+1/m)^{3m+1}}
     {27\left(1-\frac1{9m^2}\right)}.
$$

For $x\ge0$,

$$
\log(1+x)
=x-\int_0^x\frac{t}{1+t}\,dt
\le x-\frac{x^2}{2(1+x)},
$$

because $1+t\le1+x$ throughout the integral. With $x=1/m$, this implies

$$
(3m+1)\log\left(1+\frac1m\right)
\le
3-\frac{m-1}{2m(m+1)}
<3.
$$

Also $m\ge3$ gives

$$
27\left(1-\frac1{9m^2}\right)\ge\frac{80}{3}.
$$

Combining the estimates,

$$
\frac{a_{r+1}}{a_r}
<
\frac{3e^3}{80}
<
\frac{3(11/4)^3}{80}
=
\frac{3993}{5120}
<1.
$$

For completeness, the constant $e<11/4$ follows directly from its series:

$$
e
=\frac83+\sum_{j=0}^{\infty}\frac1{(4+j)!}
\le
\frac83+\frac1{24}\sum_{j=0}^{\infty}5^{-j}
=
\frac{87}{32}
<
\frac{11}{4}.
$$

Each successive factorial term in that tail is at most one fifth of its predecessor. Hence $a_r\le a_2$ for all $r\ge2$, and

$$
\binom N{3r+1}p^{3r+1}
<
a_2
=
\frac{3^7}{7!}
=
\frac{2187}{5040}
<
\frac12.
$$

Together with the empty-obstruction, zero-capacity, and capacity-one cases, this proves the theorem.

## What this establishes

The same fixed value $q=3$ works in every finite dimension for cardinality-threshold families, with the explicit generators specified in the theorem and the original product weights $p^{|I|}$. This is an analytic result for all admissible $p$, not a sampled parameter grid or a finite-dimensional census.

The proof uses the common coordinate probability and the cardinality-threshold form of $D$. It does not establish $q=3$ for arbitrary families, overlapping constraints, general matroids, or arbitrary heterogeneous product measures. The separate partition q=4 theorem covers a different, larger structured family under its own mass assumption.

The source recovery and algebra were checked within the current collaboration. This is not external peer review or formal-kernel verification. No code, enumerator, test suite, runtime experiment, sponsor submission, award, or payment is part of this delivery.
