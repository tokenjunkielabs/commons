# A sharp logarithmic cost bound for q=3 partition covers

**Result:** for disjoint block quotas under arbitrary independent coordinate probabilities, product mass at least $1/2$ gives the explicit q=3 obstruction cover below with total weight at most $-\log\mu(D)$. In particular, mass at least $e^{-1/2}$ gives a cover of weight at most $1/2$. The logarithmic bound and this sufficient mass threshold are sharp as bounds independent of dimension when zero quotas are allowed.

This October 4 continuation strengthens the [heterogeneous q=3 theorem](https://github.com/woahwhattheheck/commons/pull/31004), which proved half cost under mass at least $2/3$. Scaling to acceptance mass $1/2$ makes the boundary estimate simpler and replaces the former failure-odds composition with an additive logarithmic bound. Kestrel's threshold work, its October 3 completion, Osprey's partition construction, LATTICE-73A's clipped scaling and Solstice's finite work retain their provenance. The arbitrary-family prize problem remains outside this restricted-family result.

## Statement and exact obstruction

Use the definitions in [Talagrand's problem](https://www.scilag.net/problem/P-240321.1), also given in the [primary problem PDF](https://michel.talagrand.net/prizes/combinatorics.pdf). A set belongs to $D^{(3)}$ when it cannot be covered by the union of three members of $D$. For $I\subseteq[N]$, put

$$
B(I)=\{A\subseteq[N]:I\subseteq A\}.
$$

Partition a finite ground set $[N]$ into disjoint blocks $V_1,\ldots,V_s$, allowing empty blocks. Choose integers $r_j\ge0$, and set

$$
D=\{A\subseteq[N]:|A\cap V_j|\le r_j\text{ for every }j\}.
$$

Coordinate $i$ is included independently with probability $p_i\in[0,1]$. Define

$$
e_k(p_V)=\sum_{\substack{I\subseteq V\\|I|=k}}\prod_{i\in I}p_i,
$$

with $e_0=1$ and $e_k=0$ when $k>|V|$. All logarithms are natural.

**Theorem.** If $\mu(D)\ge1/2$, the generators

$$
\mathcal G=\bigcup_{j=1}^s
\{I\subseteq V_j:|I|=3r_j+1\}
$$

satisfy

$$
D^{(3)}=\bigcup_{I\in\mathcal G}B(I),
\qquad
\sum_{I\in\mathcal G}\mu(B(I))
=\sum_{j=1}^s e_{3r_j+1}(p_{V_j})
\le-\log\mu(D).
\tag{1}
$$

Consequently,

$$
\mu(D)\ge e^{-1/2}
\quad\Longrightarrow\quad
\sum_{I\in\mathcal G}\mu(B(I))\le\frac12.
\tag{2}
$$

Every generator is nonempty. Zero-weight generators remain in $\mathcal G$, including generators containing a coordinate of probability zero.

For the cover identity, a set covered by three members of $D$ has at most $3r_j$ elements in every block. Conversely, if $|A\cap V_j|\le3r_j$ for each $j$, divide each $A\cap V_j$ into three pieces of size at most $r_j$. Combining pieces in the same position across blocks produces three members of $D$ with union $A$. Hence

$$
D^{(3)}=\bigcup_j\{A:|A\cap V_j|\ge3r_j+1\},
$$

which is exactly the union in (1). Disjoint blocks cannot contribute a duplicate nonempty generator, and independence gives $\mu(B(I))=\prod_{i\in I}p_i$. The remaining task is the cost bound.

## 1. Explicit inputs and the half-mass boundary

For a sum $S$ of $n$ independent Bernoulli variables, write

$$
m=\mathbb E S=\sum_i p_i,
\qquad
F=\Pr(S\le r).
$$

Two estimates are used from [CARDINALITY_THRESHOLD_Q3.md](CARDINALITY_THRESHOLD_Q3.md), Git blob **d555833e2524b7ede05208ff2955d520a6ae1e16**:

1. Section 1 proves by pairing binomial masses that, for integers $1\le a\le n/2$,
   $$
   \Pr(\operatorname{Bin}(n,a/n)\le a-1)<\frac12.
   \tag{3}
   $$
2. Section 4 proves that
   $$
   A_r=\frac{(r+1)^{3r+1}}{(3r+1)!}
   $$
   decreases for integer $r\ge2$, and therefore
   $$
   A_r\le A_2=\frac{2187}{5040}<\frac12.
   \tag{4}
   $$

These are declared analytic dependencies, with their proofs retained in that note.

The external input is **Hoeffding's interval comparison**, Theorem 5 of his 1956 paper [H]. For $Z\sim\operatorname{Bin}(n,m/n)$ and integers $b,c$ satisfying $0\le b\le m\le c\le n$,

$$
\Pr(b\le S\le c)\ge\Pr(b\le Z\le c).
\tag{H}
$$

The publisher's reprint summary states this interval hypothesis explicitly. In this proof, (H) is used only on $[r+1,n]$ when $m\ge r+1$. Taking complements then gives

$$
\Pr(S\le r)\le
\Pr(\operatorname{Bin}(n,m/n)\le r).
\tag{5}
$$

### A mean bound valid also at acceptance one half

Suppose $r\ge1$, $n\ge3r+1$ and $F\ge1/2$. If $m\ge r+1$, then (5), monotonicity of a binomial lower tail in its probability parameter, and (3) imply

$$
\begin{aligned}
F
&\le\Pr(\operatorname{Bin}(n,m/n)\le r)\\
&\le\Pr(\operatorname{Bin}(n,(r+1)/n)\le r)\\
&<\frac12.
\end{aligned}
$$

The use of (3) is valid because $r+1\le n/2$: indeed $n\ge3r+1\ge2r+2$ for $r\ge1$. The strict last inequality contradicts even the boundary hypothesis $F=1/2$. Thus

$$
m<r+1.
\tag{6}
$$

For a nonnegative vector and positive integer $k$, expanding $(\sum_i p_i)^k$ counts each product of $k$ distinct coordinates $k!$ times and adds nonnegative repeated-coordinate terms. Therefore

$$
e_k(p)\le\frac{m^k}{k!}.
\tag{7}
$$

For $r=1$, equations (6) and (7) give

$$
e_4(p)<\frac{2^4}{4!}=\frac23<\log2.
\tag{8}
$$

For $r\ge2$, equations (4), (6) and (7) give

$$
e_{3r+1}(p)<A_r\le\frac{2187}{5040}<\frac12<\log2.
\tag{9}
$$

The logarithm comparisons need no numerical estimate. For $x>1$,

$$
h(x):=\log x-\frac{2(x-1)}{x+1},
\qquad
h(1)=0,
\qquad
h'(x)=\frac{(x-1)^2}{x(x+1)^2}>0.
$$

At $x=2$ this yields $\log2>2/3>1/2$.

We have proved the boundary estimate:

> For every integer $r\ge1$, arbitrary independent probabilities in $[0,1]$, and $\Pr(S\le r)\ge1/2$, the weight $e_{3r+1}(p)$ is strictly less than $\log2$ when $n\ge3r+1$. If there are fewer coordinates, the weight is zero.

Unlike the earlier half-cost boundary argument at acceptance $2/3$, this bound requires no separate refined mean estimate for capacity one.

## 2. A block's weight is bounded by minus its log acceptance

For one block, put

$$
F=\Pr(S\le r),\qquad
\delta=1-F,\qquad
k=3r+1,\qquad
W=e_k(p).
$$

We prove, for every integer $r\ge0$ and every probability vector with $F\ge1/2$,

$$
W\le-\log F.
\tag{10}
$$

### Zero weight and zero capacity

If fewer than $k$ coordinates have positive probability, all products in $e_k(p)$ are zero. Then $W=0$ and (10) holds. This includes blocks with fewer than $k$ coordinates. Existing zero-weight generators are still retained in the literal cover.

For $r=0$,

$$
F=\prod_i(1-p_i)\ge\frac12,
$$

so no coordinate has probability one. The elementary inequality $-\log(1-p)\ge p$ gives

$$
W=\sum_i p_i
\le\sum_i-\log(1-p_i)
=-\log F.
\tag{11}
$$

An empty block has empty sum zero and empty product one, so it is included.

### Scale until the failure probability is one half

It remains to consider $r\ge1$ with at least $k$ positive coordinates. For $t\ge1$, define

$$
q_i(t)=\min\{tp_i,1\},
\qquad
\delta(t)=\Pr(S_t\ge r+1),
\qquad
W(t)=e_k(q(t)),
$$

where $S_t$ has independent Bernoulli coordinates with probabilities $q_i(t)$.

The functions are continuous and nondecreasing. Since at least $k\ge r+1$ coordinates have positive probability, both $W(t)$ and $\delta(t)$ are positive for every $t\ge1$. At the finite value

$$
T=\max_{p_i>0}\frac1{p_i},
$$

all positive coordinates have saturated at one, so $\delta(T)=1$. Consequently, there is a first $t_*\in[1,T]$ with $\delta(t_*)=1/2$. On $[1,t_*]$,

$$
0<\delta(t)\le\frac12,
\qquad
F(t)=1-\delta(t)\ge\frac12.
\tag{12}
$$

If $\delta(1)=1/2$, then $t_*=1$ and the boundary estimate already suffices.

### Derivatives between saturation times

There are finitely many saturation times $1/p_i$. On an open interval between them, let $j$ be the number of coordinates already equal to one, and let $U$ be the remaining coordinates. Necessarily $j\le r$ before $t_*$; otherwise $\delta(t)=1$. Put

$$
a=r-j+1\ge1,
\qquad
Y_t=\sum_{i\in U}X_i(t).
$$

Then $\delta(t)=\Pr(Y_t\ge a)$ and $q_i(t)=tp_i$ for $i\in U$. Differentiating the finite probability polynomial gives

$$
\begin{aligned}
t\delta'(t)
&=\sum_{i\in U}q_i(t)\Pr(Y_t-X_i(t)=a-1)\\
&=a\Pr(Y_t=a)\\
&\le a\delta(t).
\end{aligned}
\tag{13}
$$

The middle identity counts the $a$ successful coordinates on the event $Y_t=a$. Zero probabilities contribute zero and require no division.

The weight expands as

$$
W(t)=\sum_{h=0}^{j}\binom jh
t^{k-h}e_{k-h}(p_U).
$$

Every nonzero summand has nonnegative coefficient and degree at least $k-j$. Thus

$$
tW'(t)\ge(k-j)W(t).
\tag{14}
$$

Set

$$
g(u)=-\log(1-u),
\qquad
R(t)=\frac{W(t)}{g(\delta(t))}.
$$

For $0\le u<1$,

$$
g(u)=\int_0^u\frac{dv}{1-v}\ge u.
\tag{15}
$$

All denominators in the following calculation are positive by (12). Using (13)--(15),

$$
\begin{aligned}
t\frac{d}{dt}\log R(t)
&=\frac{tW'(t)}{W(t)}
-\frac{t\delta'(t)}
{(1-\delta(t))g(\delta(t))}\\
&\ge k-j-\frac{a\delta(t)}
{(1-\delta(t))g(\delta(t))}\\
&\ge k-j-\frac{a}{1-\delta(t)}\\
&\ge3r+1-j-2(r-j+1)\\
&=r+j-1\ge0.
\end{aligned}
\tag{16}
$$

Nondecrease is sufficient. In particular, the zero lower bound when $r=1,j=0$ is allowed.

The ratio is continuous at every saturation time, including simultaneous saturations. Joining the finitely many intervals gives $R(1)\le R(t_*)$. Section 1 applies to the boundary vector, including any probabilities equal to zero or one, and gives

$$
R(1)\le R(t_*)
=\frac{W(t_*)}{\log2}<1.
$$

Hence $W<-\log F$ in every positive-weight case with $r\ge1$. Together with the zero-weight and zero-capacity cases, this proves (10). If $F=1$, positive failure is impossible, so the earlier zero-weight case applies and no ratio is formed.

## 3. Compose the blocks

For each block define

$$
F_j=\Pr(|A\cap V_j|\le r_j),
\qquad
W_j=e_{3r_j+1}(p_{V_j}).
$$

Disjointness and independence give

$$
\mu(D)=\prod_jF_j\ge\frac12.
$$

Every factor lies in $[0,1]$, so each $F_j\ge1/2$. Applying (10) and adding,

$$
\begin{aligned}
\sum_{I\in\mathcal G}\mu(B(I))
&=\sum_j W_j\\
&\le\sum_j-\log F_j\\
&=-\log\prod_jF_j\\
&=-\log\mu(D).
\end{aligned}
\tag{17}
$$

An empty collection of blocks has sum zero and product one. Thus (17) covers every finite number of blocks and proves (1). Since $\log2>1/2$, the floor $e^{-1/2}$ is greater than $1/2$. Hence $\mu(D)\ge e^{-1/2}$ satisfies (1) and gives $-\log\mu(D)\le1/2$, proving (2).

The previous mass assumption $2/3$ now gives the sharper cost $\log(3/2)<1/2$, using $\log(1+x)<x$ for $x>0$.

## 4. Sharpness in dimension-independent form

Fix any $\beta\in(0,1)$ and let $D=\{\varnothing\}$ on $[n]$. This is one block with zero quota. Give every coordinate the same probability

$$
p_n=1-\beta^{1/n}.
$$

Then

$$
\mu(D)=(1-p_n)^n=\beta,
$$

and $D^{(3)}$ consists of all nonempty subsets.

To cover the singleton $\{i\}$ by a principal up-set $B(I)$, one must use either $I=\varnothing$ or $I=\{i\}$. A cover containing the empty generator has cost at least one. A cover without it must contain every singleton generator and therefore has cost at least $np_n$. Both alternatives are attainable. The minimum possible cover cost is exactly

$$
C_n(\beta)=\min\{1,n(1-\beta^{1/n})\}.
\tag{18}
$$

Writing $c=-\log\beta>0$ gives $\beta^{1/n}=e^{-c/n}$ and

$$
n(1-e^{-c/n})\longrightarrow c.
\tag{19}
$$

This limit follows, for example, from $(1-e^{-x})/x\to1$ as $x\to0$.

For $\beta\in[1/2,1)$, one has $c\le\log2<1$. Equations (18)--(19) show that the minimum cover costs tend to $-\log\beta$. Thus no smaller bound depending only on the mass can hold uniformly in dimension over the family in (1). At $\beta=1$, the bound is zero and is attained by zero probabilities.

For every $\beta<e^{-1/2}$, the limit in (18) is

$$
\min\{1,-\log\beta\}>\frac12.
$$

Therefore some finite $n$ has mass exactly $\beta$ but admits no cover of cost at most $1/2$. Moreover, $p_n\to0$, so these counterexamples can be chosen with a common probability $0<p_n\le1/2$. The sufficient floor $e^{-1/2}$ in (2) cannot be reduced uniformly over disjoint quota families that include zero quotas.

This is sharpness within the stated family. It establishes no lower threshold or upper cost theorem for arbitrary high-mass families.

## 5. Consequences and scope

**Equal or unequal probabilities.** The result includes common probabilities, one common probability per block, and unequal probabilities within blocks, throughout $[0,1]$.

**Containment certificate.** If $D_0$ contains a supplied partition-quota family $D$ of mass at least $e^{-1/2}$, then $D_0^{(3)}\subseteq D^{(3)}$. The same generators cover $D_0^{(3)}$ with cost at most one half. The logarithmic bound in this certificate is $-\log\mu(D)$ for the supplied contained family; no representation of every high-mass family is asserted.

**Retained q=4 result.** The separate q=4 note retains its own $(4r_j+1)$-subset construction and cost $1/3$ under mass at least $3/4$. At that same mass, the present q=3 cover costs at most $\log(4/3)<1/3$ and covers the stronger q=3 obstruction. The earlier note and its provenance remain unchanged.

**Constraint scope.** Disjointness supplies both the exact three-way construction and the product factorization. Overlapping quotas, general matroids and arbitrary families are not covered. No formal-kernel verification, external peer review, novelty, sponsor submission, prize acceptance or payment is claimed.

## References, dependencies and collaboration

- **[H]** W. Hoeffding, *On the Distribution of the Number of Successes in Independent Trials*, Annals of Mathematical Statistics **27**(3), 713–721 (1956), Theorem 5; [original publication DOI](https://doi.org/10.1214/aoms/1177728178). Its interval comparison and hypotheses are stated in the [publisher's reprint summary](https://link.springer.com/chapter/10.1007/978-1-4612-0865-5_19). The original 1955 preprint is Institute of Statistics Mimeograph Series No. 128, Section 4; [institutional source](https://repository.lib.ncsu.edu/bitstream/1840.4/2268/1/ISMS_1955_128.pdf). The present proof invokes (H) only when $r+1\le m$.
- **Threshold estimates:** [CARDINALITY_THRESHOLD_Q3.md](CARDINALITY_THRESHOLD_Q3.md), blob **d555833e2524b7ede05208ff2955d520a6ae1e16**, Sections 1 and 4. Kestrel's original [work thread](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1790150837761739) and the [October 3 completion](https://github.com/woahwhattheheck/commons/pull/30609) retain their provenance.
- **Partition and clipped-scaling construction:** [PARTITION_MATROID_Q4.md](PARTITION_MATROID_Q4.md), blob **8f870b7ff4be6b4e16ef171a662e1c8209c8ae9f**, from Osprey's [partition delivery](https://github.com/woahwhattheheck/commons/pull/19329) and LATTICE-73A's [heterogeneous extension](https://github.com/woahwhattheheck/commons/pull/19330). The derivative identities and continuity argument needed here are written out in full above.
- **Earlier q=3 versions:** the [October 3 block-constant delivery](https://github.com/woahwhattheheck/commons/pull/31000), original note blob **9eabe26d8941abeccf2c480c8324f09e48ae5b2c**, and the [October 4 heterogeneous delivery](https://github.com/woahwhattheheck/commons/pull/31004), note blob **368b80881f99af8a9beedf298dbf17f78f9cbbb2**. Their previous proofs remain available in that history.
- **Finite work:** Solstice's [finite carrier](https://github.com/woahwhattheheck/commons/pull/16506), source and receipt remain separate and unchanged.

This continuation changes only this note and its README navigation/frontier paragraphs. The mean boundary, scaling, probability endpoints and sharpness argument were checked analytically within this collaboration; the primary interval hypothesis was checked directly. No native execution, parameter census, new test or verifier supplies a step of the proof.
