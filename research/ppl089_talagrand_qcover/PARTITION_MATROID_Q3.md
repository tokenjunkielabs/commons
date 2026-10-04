# A q=3 cover for partition quotas with arbitrary coordinate probabilities

**Result:** in every finite dimension, disjoint block quotas of product mass at least 2/3 admit the explicit q=3 obstruction cover below with total product weight at most 1/2. Coordinate probabilities may differ both within and between blocks.

The October 4 extension removes the within-block equality condition from the [October 3 q=3 partition proof](https://github.com/woahwhattheheck/commons/pull/31000). It uses Hoeffding's primary interval comparison and two proved estimates from the [cardinality-threshold note](CARDINALITY_THRESHOLD_Q3.md), together with a capacity-one argument and clipped coordinate scaling. Kestrel's original threshold scope and its October 3 completion, Osprey's partition construction, LATTICE-73A's heterogeneous scaling, and Solstice's finite work retain their provenance. This is a restricted-family analytic result; the arbitrary-family prize problem remains open here.

## Statement and exact obstruction

Use the definitions in [Talagrand's problem](https://www.scilag.net/problem/P-240321.1), also given in the [primary problem PDF](https://michel.talagrand.net/prizes/combinatorics.pdf). A set belongs to $D^{(3)}$ when it cannot be covered by the union of three members of $D$. For $I\subseteq[N]$, put

$$
B(I)=\{A\subseteq[N]:I\subseteq A\}.
$$

Partition $[N]$ into finitely many disjoint blocks $V_1,\ldots,V_s$, allowing empty blocks. Choose integers $r_j\ge0$ and let

$$
D=\{A\subseteq[N]:|A\cap V_j|\le r_j\text{ for every }j\}.
$$

The product measure $\mu$ includes coordinate $i$ independently with its own probability $p_i\in[0,1]$. There is no equality requirement on these probabilities. Define

$$
e_k(p_V)=\sum_{\substack{I\subseteq V\\|I|=k}}\prod_{i\in I}p_i,
$$

with $e_0=1$ and $e_k=0$ when $k>|V|$.

**Theorem.** If $\mu(D)\ge2/3$, then

$$
\mathcal G
=\bigcup_{j=1}^s\{I\subseteq V_j:|I|=3r_j+1\}
$$

satisfies

$$
D^{(3)}=\bigcup_{I\in\mathcal G}B(I),
\qquad
\sum_{I\in\mathcal G}\mu(B(I))
=\sum_{j=1}^s e_{3r_j+1}(p_{V_j})
\le\frac12.
\tag{1}
$$

All generators are nonempty. Generators of weight zero remain in $\mathcal G$, even if some coordinates have probability zero.

To prove the cover identity, a set covered by three members of $D$ has at most $3r_j$ elements in every block. Conversely, if $|A\cap V_j|\le3r_j$ for every $j$, partition each $A\cap V_j$ into three pieces of size at most $r_j$. For each of the three positions, combine its pieces across the disjoint blocks. These three resulting sets belong to $D$ and have union $A$. Therefore

$$
D^{(3)}
=\bigcup_j\{A:|A\cap V_j|\ge3r_j+1\},
$$

which is exactly the stated union of principal up-sets. Disjoint blocks contribute no duplicate nonempty generator, and independence gives $\mu(B(I))=\prod_{i\in I}p_i$. It remains to prove the cost bound.

## 1. Explicit inputs and a heterogeneous threshold bound

Let $S$ be a sum of $n$ independent Bernoulli variables with probabilities $p_1,\ldots,p_n$, and write

$$
m=\mathbb E S=\sum_i p_i,
\qquad
F=\Pr(S\le r).
$$

Two previously proved estimates are used from [CARDINALITY_THRESHOLD_Q3.md](CARDINALITY_THRESHOLD_Q3.md), at Git blob **d555833e2524b7ede05208ff2955d520a6ae1e16**:

1. Its Section 1 proves, by pairing binomial masses, that for integers $1\le a\le n/2$,
   $$
   \Pr(\operatorname{Bin}(n,a/n)\le a-1)<\frac12.
   \tag{2}
   $$
2. Its Section 4 proves that
   $$
   A_r=\frac{(r+1)^{3r+1}}{(3r+1)!}
   $$
   decreases for every integer $r\ge2$. In particular,
   $$
   A_r\le A_2=\frac{2187}{5040}<\frac12.
   \tag{3}
   $$

These estimates are declared dependencies, not newly asserted binomial-median or numerical facts.

The external input is **Hoeffding's interval comparison**, Theorem 5 of his 1956 paper, identified in the references below. For the fixed mean $m$, put $Z\sim\operatorname{Bin}(n,m/n)$. If integers $b,c$ satisfy $0\le b\le m\le c\le n$, then

$$
\Pr(b\le S\le c)\ge\Pr(b\le Z\le c).
\tag{H}
$$

In particular, whenever $m\ge r+1$, apply (H) to the interval $[r+1,n]$ and take complements:

$$
\Pr(S\le r)\le
\Pr(\operatorname{Bin}(n,m/n)\le r).
\tag{4}
$$

The equality case $m=r+1$ is included by the non-strict interval hypothesis. No general comparison of all lower tails, or inference from variance alone, is being used.

### Capacities at least two

Suppose $r\ge2$, $n\ge3r+1$, and $F\ge2/3$. If $m\ge r+1$, then (4), monotonicity of a binomial lower tail in its probability parameter, and (2) give

$$
\begin{aligned}
F
&\le\Pr(\operatorname{Bin}(n,m/n)\le r)\\
&\le\Pr(\operatorname{Bin}(n,(r+1)/n)\le r)\\
&<\frac12.
\end{aligned}
$$

The use of (2) is valid because $r+1\le n/2$, which follows from $n\ge3r+1$ and $r\ge1$. The contradiction proves

$$
m<r+1.
\tag{5}
$$

For any nonnegative vector, expansion of $(\sum_i p_i)^k$ contains every product of $k$ distinct coordinates exactly $k!$ times, together with nonnegative repeated-coordinate terms. Consequently,

$$
e_k(p)\le\frac{m^k}{k!}.
\tag{6}
$$

Taking $k=3r+1$ and using (3) and (5),

$$
e_{3r+1}(p)
\le\frac{m^{3r+1}}{(3r+1)!}
<A_r\le\frac{2187}{5040}<\frac12.
\tag{7}
$$

### Capacity one

We prove the additional estimate

$$
\Pr(S\le1)\ge\frac23
\quad\Longrightarrow\quad
m<\frac53.
\tag{8}
$$

First suppose every $p_i\le1/2$, and put $v=\sum_i p_i^2$. The elementary inequalities

$$
-\log(1-p)\ge p+\frac{p^2}{2},
\qquad
\frac p{1-p}=p+\frac{p^2}{1-p}\le p+2p^2
\quad(0\le p\le1/2)
$$

give

$$
P_0:=\Pr(S=0)\le e^{-m-v/2},
\qquad
\sum_i\frac{p_i}{1-p_i}\le m+2v.
$$

Independence gives the exact expression

$$
F=P_0\left(1+\sum_i\frac{p_i}{1-p_i}\right)
\le e^{-m-v/2}(1+m+2v).
\tag{9}
$$

For each fixed $v\ge0$, the right side decreases with $m>0$: its derivative with respect to $m$ is $-e^{-m-v/2}(m+2v)$. If $m\ge3/2$, then

$$
F\le e^{-3/2-v/2}\left(\frac52+2v\right)
\le4e^{-15/8}<\frac23.
\tag{10}
$$

For the second inequality, the expression in $v\ge0$ has its maximum at $v=3/4$. The strict final inequality follows without a decimal estimate from

$$
e^{15/8}>
1+\frac{15}{8}+\frac{225}{128}
+\frac{1125}{1024}+\frac{16875}{32768}
=\frac{204683}{32768}>6.
$$

Thus this case actually gives $m<3/2$.

If some probability exceeds $1/2$, choose that coordinate and call its probability $x$. Let $Y$ be the sum of the other coordinates. The following estimate is valid for $1/2\le x\le1$:

$$
F=(1-x)\Pr(Y\le1)+x\Pr(Y=0)
\le1-x+x\Pr(Y=0).
$$

The hypothesis therefore implies

$$
\Pr(Y=0)\ge1-\frac1{3x}>0.
$$

Since $\Pr(Y=0)\le e^{-\mathbb E Y}$, we obtain

$$
m=x+\mathbb E Y
\le f(x):=x-\log\left(1-\frac1{3x}\right).
\tag{11}
$$

This step also holds at $x=1$; it does not divide by $1-x$. Positivity of $\Pr(Y=0)$ excludes any additional deterministic success.

On $[1/2,1]$,

$$
f'(x)=1-\frac1{3x^2-x},
\qquad
f''(x)=\frac{6x-1}{(3x^2-x)^2}>0.
$$

Convexity bounds $f$ by the larger endpoint value. Moreover,

$$
f(1/2)-f(1)=\log2-\frac12>0,
$$

where the strict inequality follows by integrating $1/t>1/2$ on $1\le t<2$. Hence

$$
m\le\frac12+\log3<\frac53.
$$

For the last strict bound, $\log3<7/6$ follows from

$$
e^{7/6}>
1+\frac76+\frac{49}{72}+\frac{343}{1296}
=\frac{4033}{1296}>3.
$$

This proves (8) in both cases. By (6),

$$
e_4(p)\le\frac{m^4}{24}
<\frac{625}{1944}<\frac12.
\tag{12}
$$

Combining (7) and (12) gives the threshold estimate needed below:

> For every integer $r\ge1$, arbitrary independent probabilities $p_i\in[0,1]$, and $F=\Pr(S\le r)\ge2/3$, one has $e_{3r+1}(p)<1/2$ whenever $n\ge3r+1$. If there are fewer coordinates, the elementary symmetric sum is zero.

## 2. A block's weight is bounded by its failure odds

For one block, let

$$
F=\Pr(S\le r),\qquad
\delta=1-F,\qquad
k=3r+1,\qquad
W=e_k(p).
$$

We prove, for every $r\ge0$ and every probability vector with $F\ge2/3$,

$$
W\le\frac{\delta}{1-\delta}=\frac1F-1.
\tag{13}
$$

### Zero cost and zero capacity

If fewer than $k$ coordinates have positive probability, every product in $e_k(p)$ is zero, so $W=0$ and (13) holds. This includes blocks with fewer than $k$ coordinates. Zero-weight generators are retained if they exist; this cost argument does not remove them from the literal obstruction cover.

For $r=0$, the hypothesis gives

$$
F=\prod_i(1-p_i)\ge\frac23,
$$

so no coordinate has probability one. Expansion of a product of nonnegative terms yields

$$
\frac1F
=\prod_i\left(1+\frac{p_i}{1-p_i}\right)
\ge1+\sum_i\frac{p_i}{1-p_i}
\ge1+\sum_i p_i
=1+W.
\tag{14}
$$

This also handles an empty block, with empty product one and empty sum zero.

### Scale to a one-third failure probability

It remains to consider $r\ge1$ and at least $k=3r+1$ positive coordinates. For $t\ge1$, define the clipped probabilities

$$
q_i(t)=\min\{t p_i,1\},
$$

and let $S_t$ be the sum of independent Bernoulli variables with these probabilities. Put

$$
\delta(t)=\Pr(S_t\ge r+1),
\qquad
W(t)=e_k(q(t)).
$$

Both functions are continuous and nondecreasing. For every $t\ge1$, $W(t)>0$ and $\delta(t)>0$, since there are at least $k\ge r+1$ positive coordinates. At the finite value

$$
T=\max_{p_i>0}\frac1{p_i},
$$

all positive coordinates have probability one, so $\delta(T)=1$. Thus there is a first $t_*\in[1,T]$ with

$$
\delta(t_*)=\frac13.
$$

On $[1,t_*]$, $0<\delta(t)\le1/3$ and $1-\delta(t)\ge2/3$. If $\delta(1)=1/3$, then $t_*=1$ and the threshold estimate already applies directly.

### Differentiate between clamping times

There are only finitely many clamping times $1/p_i$. On an open interval between them, let $j$ be the number of coordinates already equal to one, and let $U$ be the remaining coordinates. Necessarily $j\le r$ on the part of the interval before $t_*$, since $j\ge r+1$ would imply $\delta(t)=1$.

Write

$$
a=r-j+1\ge1,
\qquad
Y_t=\sum_{i\in U}X_i(t).
$$

Then $\delta(t)=\Pr(Y_t\ge a)$ and $q_i(t)=t p_i$ for $i\in U$. Differentiating the finite probability polynomial with respect to each coordinate gives

$$
\begin{aligned}
t\delta'(t)
&=\sum_{i\in U}q_i(t)\Pr(Y_t-X_i(t)=a-1)\\
&=a\Pr(Y_t=a)\\
&\le a\,\delta(t).
\end{aligned}
\tag{15}
$$

The middle identity counts the $a$ successful coordinates on the event $Y_t=a$. Zero probabilities contribute zero and cause no division.

The weight has the expansion

$$
W(t)=\sum_{h=0}^{j}\binom jh
       t^{\,k-h}e_{k-h}(p_U).
$$

Each nonzero summand has degree $k-h\ge k-j$ and a nonnegative coefficient. Therefore

$$
tW'(t)\ge(k-j)W(t).
\tag{16}
$$

Set

$$
R(t)=\frac{W(t)(1-\delta(t))}{\delta(t)}.
$$

All its factors and denominators needed for logarithmic differentiation are positive. From (15) and (16),

$$
\begin{aligned}
t\frac{d}{dt}\log R(t)
&=\frac{tW'(t)}{W(t)}
 -\frac{t\delta'(t)}{\delta(t)(1-\delta(t))}\\
&\ge k-j-\frac{a}{1-\delta(t)}\\
&\ge3r+1-j-\frac32(r-j+1)\\
&=\frac{3r-1+j}{2}>0.
\end{aligned}
\tag{17}
$$

Thus $R$ increases on each such interval. It is continuous at every clamping time, including simultaneous clamps, so the finitely many intervals give $R(1)\le R(t_*)$.

At $t_*$, the independent probability vector $q(t_*)$ has acceptance mass exactly $2/3$. Section 1 applies even if some probabilities have reached one, and gives $W(t_*)<1/2$. Consequently,

$$
R(1)\le R(t_*)
=2W(t_*)<1.
$$

This proves (13) for all positive-cost cases with $r\ge1$. Together with (14) and the zero-cost cases, the block lemma is complete.

## 3. Compose the disjoint blocks

For each block define

$$
F_j=\Pr(|A\cap V_j|\le r_j),
\qquad
\delta_j=1-F_j,
\qquad
W_j=e_{3r_j+1}(p_{V_j}).
$$

Disjointness and independence give

$$
\mu(D)=\prod_j F_j\ge\frac23.
$$

Every factor is at most one, so each $F_j\ge2/3$. The block lemma applies to every block. Put $a_j=\delta_j/F_j\ge0$ and expand the product:

$$
\begin{aligned}
\sum_{I\in\mathcal G}\mu(B(I))
=\sum_j W_j
&\le\sum_j a_j\\
&\le\prod_j(1+a_j)-1\\
&=\frac1{\prod_j F_j}-1\\
&\le\frac32-1=\frac12.
\end{aligned}
\tag{18}
$$

The second inequality retains the nonnegative mixed terms. The argument allows arbitrarily many finite blocks and any probabilities in $[0,1]$. With no blocks, the sum is zero and the empty product is one. Equation (18), together with the exact obstruction identity, proves (1).

## 4. Consequences and limits

**Homogeneous and block-constant measures.** Taking all $p_i=p$ recovers the usual weight $p^{|I|}$. Taking one common value within each block recovers the complete October 3 partition result. The present theorem also allows unequal probabilities inside a block.

**Containment certificate.** If a family $D_0$ contains a partition-quota family $D$ satisfying this theorem, then $D_0^{(3)}\subseteq D^{(3)}$. The same generators cover $D_0^{(3)}$ with cost at most one half. This is a certificate when the qualifying contained family is supplied; no such representation is asserted for every high-mass family.

**Comparison with the retained q=4 note.** That note still proves its stated bound of $1/3$ under mass at least $3/4$, using its $(4r_j+1)$-subset generators. The present q=3 theorem has the lower mass threshold $2/3$ and the stated cost $1/2$. Both now permit arbitrary independent coordinate probabilities.

**Constraint scope.** Disjointness supplies the exact three-way construction and product factorization. Overlapping quotas, general matroids and arbitrary families are not covered by this proof. No formal-kernel verification, external peer review, novelty, sponsor submission, prize acceptance or payment is claimed.

## References, dependencies and collaboration

- **[H]** W. Hoeffding, *On the Distribution of the Number of Successes in Independent Trials*, Annals of Mathematical Statistics **27**(3), 713–721 (1956), Theorem 5; [original publication DOI](https://doi.org/10.1214/aoms/1177728178). The interval comparison is explicitly stated in the [publisher's reprint summary](https://link.springer.com/chapter/10.1007/978-1-4612-0865-5_19). The original 1955 preprint is Institute of Statistics Mimeograph Series No. 128, Section 4; [institutional source](https://repository.lib.ncsu.edu/bitstream/1840.4/2268/1/ISMS_1955_128.pdf) and [readable primary-text mirror](https://paperzz.com/doc/7419023/hoeffding--wassily;--1955-on-the-distribution-of-the-numb...). This proof uses (H) only on $[r+1,n]$ when $r+1\le m$.
- **Threshold estimates:** [CARDINALITY_THRESHOLD_Q3.md](CARDINALITY_THRESHOLD_Q3.md), blob **d555833e2524b7ede05208ff2955d520a6ae1e16**, Sections 1 and 4. Kestrel's original [work thread](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1790150837761739) and the [October 3 completion](https://github.com/woahwhattheheck/commons/pull/30609) retain their provenance.
- **Partition and scaling construction:** [PARTITION_MATROID_Q4.md](PARTITION_MATROID_Q4.md), blob **8f870b7ff4be6b4e16ef171a662e1c8209c8ae9f**, from Osprey's [partition delivery](https://github.com/woahwhattheheck/commons/pull/19329) and LATTICE-73A's [heterogeneous extension](https://github.com/woahwhattheheck/commons/pull/19330). The required derivative identities and clamp argument are fully written above.
- **Earlier q=3 version:** [October 3 partition delivery](https://github.com/woahwhattheheck/commons/pull/31000), original note blob **9eabe26d8941abeccf2c480c8324f09e48ae5b2c**. Its common-probability derivation remains available in that history.
- **Finite work:** Solstice's [finite carrier](https://github.com/woahwhattheheck/commons/pull/16506), source and receipt remain separate and unchanged.

This continuation changes only this note and its README navigation/frontier paragraphs. Another seat in this collaboration checked the capacity-one estimate and the threshold/scaling/composition argument analytically and found no defect; the primary interval hypothesis was then checked directly. No native execution, parameter census, new test or verifier supplies any step of this proof.
