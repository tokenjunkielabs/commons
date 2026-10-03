# A q=3 cover for partition quotas with one probability per block

**Result:** an analytic q=3 extension to disjoint block quotas in every finite dimension, under mass at least 2/3. Each block has a common coordinate probability; different blocks may have different probabilities.

This composes the completed [cardinality-threshold q=3 theorem](CARDINALITY_THRESHOLD_Q3.md), carrying Kestrel's original scope and the [October 3 completion](https://github.com/woahwhattheheck/commons/pull/30609), with the obstruction construction and failure-odds composition from [Osprey and LATTICE-73A's partition q=4 note](PARTITION_MATROID_Q4.md). Solstice's earlier finite work remains separate. No arbitrary-family theorem, novelty, external peer review, formal-kernel verification, sponsor submission or prize/payment result is asserted.

## Statement

Use the obstruction and principal-up-set definitions in [Talagrand's problem](https://www.scilag.net/problem/P-240321.1), also stated in the [primary problem PDF](https://michel.talagrand.net/prizes/combinatorics.pdf). A set belongs to $D^{(3)}$ when it cannot be covered by the union of three members of $D$. For $I\subseteq[N]$, write

$$
B(I)=\{A\subseteq[N]:I\subseteq A\}.
$$

Partition $[N]$ into finitely many disjoint blocks $V_1,\ldots,V_s$. Empty blocks are harmless. Put $n_j=|V_j|$, choose integers $r_j\ge0$, and define

$$
D=\{A\subseteq[N]:|A\cap V_j|\le r_j\text{ for every }j\}.
$$

The product measure $\mu$ includes coordinates independently, with probability $p_j\in[0,1]$ for every coordinate in block $V_j$. Thus probabilities are constant **within** each block, without any required equality between blocks.

**Theorem.** If $\mu(D)\ge2/3$, then the explicit family

$$
\mathcal G
=\bigcup_{j=1}^{s}
 \{I\subseteq V_j:|I|=3r_j+1\}
$$

satisfies

$$
D^{(3)}=\bigcup_{I\in\mathcal G}B(I),
\qquad
\sum_{I\in\mathcal G}\mu(B(I))
=\sum_{j=1}^{s}\binom{n_j}{3r_j+1}p_j^{\,3r_j+1}
\le\frac12.
$$

We set $\binom nk=0$ for $k>n$. Every generator is nonempty, so its weight is unambiguous even when $p_j=0$. Zero-weight generators remain in the literal family $\mathcal G$.

## 1. The obstruction is exact

If a set $A$ is contained in the union of three members of $D$, then

$$
|A\cap V_j|\le3r_j
\quad\text{for every }j.
$$

Conversely, suppose those inequalities hold. In each block partition $A\cap V_j$ into three pieces of size at most $r_j$, allowing empty pieces. For each of the three positions, take the union of its pieces across all blocks. Each resulting set belongs to $D$, and their union is exactly $A$.

Consequently,

$$
D^{(3)}
=\bigcup_j\{A:|A\cap V_j|\ge3r_j+1\}.
$$

The event for block $j$ is precisely the union of $B(I)$ over its $(3r_j+1)$-subsets. Since the blocks are disjoint and all generators are nonempty, distinct blocks contribute no duplicate generator. This proves both the cover identity and the expression for its weight.

## 2. Convert the threshold theorem into a failure-odds bound

The complete input theorem is [CARDINALITY_THRESHOLD_Q3.md](CARDINALITY_THRESHOLD_Q3.md), read at Git blob **d555833e2524b7ede05208ff2955d520a6ae1e16**.

It proves, for all nonnegative integers $n,r$ and $0<u\le1/2$,

$$
\Pr(\operatorname{Bin}(n,u)\le r)\ge\frac23
\quad\Longrightarrow\quad
\binom n{3r+1}u^{3r+1}\le\frac12.
\tag{T}
$$

That note supplies the full binomial-mean argument and all capacity cases. The additional step here makes its bound proportional to a block's failure odds, permitting an arbitrary number of blocks.

**Block lemma.** Let $X\sim\operatorname{Bin}(n,p)$, where $p\in[0,1]$, and put

$$
F=\Pr(X\le r),\qquad
\delta=1-F,\qquad
k=3r+1,\qquad
W=\binom nk p^k.
$$

If $F\ge2/3$, then

$$
W\le\frac{\delta}{1-\delta}=\frac1F-1.
\tag{1}
$$

### Empty cost and zero capacity

If $n<k$, there are no block generators and $W=0$. If $p=0$, the weight is also zero. The latter case can still have literal obstruction sets when $n\ge k$; they are covered by the retained zero-weight generators. In either case (1) follows because $F>0$.

Now let $r=0$ in the remaining cases. Then $n\ge1$, $F=(1-p)^n\ge2/3$, and therefore $p<1$. Since $W=np$,

$$
\frac1F
=\left(1+\frac p{1-p}\right)^n
\ge1+\frac{np}{1-p}
\ge1+np
=1+W.
$$

This proves (1) without using (T) or dividing by a capacity.

### Reach the one-third tail boundary

It remains to treat $r\ge1$, $n\ge3r+1$, and $p>0$. For $x\in[0,1]$, define

$$
\delta(x)=\Pr(\operatorname{Bin}(n,x)\ge r+1),
\qquad
W(x)=\binom nk x^k.
$$

The tail is continuous, is zero at $x=0$, and is strictly increasing on $(0,1)$. Its derivative is displayed below.

We need the boundary to lie inside the probability range of (T). Since $n\ge3r+1$ and $r\ge1$, we have $n\ge2r+2$. At probability $1/2$, binomial symmetry gives equal masses to the ranges $0,\ldots,r$ and $n-r,\ldots,n$. At least one count lies strictly between those ranges, and every binomial mass is positive. Hence

$$
\Pr(\operatorname{Bin}(n,1/2)\le r)<\frac12,
\qquad
\delta(1/2)>\frac12.
$$

There is therefore a unique $x_*\in(0,1/2)$ with

$$
\delta(x_*)=\frac13.
$$

Because the hypothesis gives $\delta(p)\le1/3$, monotonicity forces $0<p\le x_*$. This also explains why allowing $p>1/2$ in the block lemma adds no unsupported positive-cost case.

### Monotonicity of weight divided by failure odds

On $[p,x_*]$, $x>0$, $W(x)>0$, $0<\delta(x)\le1/3$, and $1-\delta(x)\ge2/3$. All following denominators are positive.

Differentiating the finite binomial tail and cancelling adjacent terms gives

$$
\delta'(x)
=n\binom{n-1}{r}x^r(1-x)^{n-r-1}>0.
$$

Equivalently,

$$
x\delta'(x)
=(r+1)\Pr(\operatorname{Bin}(n,x)=r+1)
\le(r+1)\delta(x).
\tag{2}
$$

Define

$$
R(x)=\frac{W(x)(1-\delta(x))}{\delta(x)}.
$$

Since $xW'(x)=kW(x)$, logarithmic differentiation and (2) yield

$$
\begin{aligned}
x\frac{d}{dx}\log R(x)
&=k-\frac{x\delta'(x)}{\delta(x)(1-\delta(x))}\\
&\ge k-\frac{r+1}{1-\delta(x)}\\
&\ge3r+1-\frac32(r+1)\\
&=\frac{3r-1}{2}>0.
\end{aligned}
\tag{3}
$$

Thus $R$ is increasing from $p$ to $x_*$; if $p=x_*$, the comparison below is immediate without a nontrivial interval.

At $x_*$, the acceptance mass is exactly $2/3$ and $0<x_*<1/2$, so (T) applies. Therefore

$$
R(x_*)
=W(x_*)\frac{2/3}{1/3}
=2W(x_*)\le1.
$$

It follows that $R(p)\le1$, which is exactly (1). This proves the block lemma for every stated $n,r,p$, including all cases separated above.

## 3. Compose the blocks

Let $X_j=|A\cap V_j|$ for a random set under $\mu$, and set

$$
F_j=\Pr(X_j\le r_j),
\qquad
\delta_j=1-F_j,
\qquad
W_j=\binom{n_j}{3r_j+1}p_j^{\,3r_j+1}.
$$

Disjointness of blocks and independence of coordinates give

$$
\mu(D)=\prod_jF_j\ge\frac23.
$$

Every factor is at most one, so each $F_j\ge2/3$. Apply the block lemma and define $a_j=\delta_j/F_j\ge0$. Expansion of the finite product gives

$$
\begin{aligned}
\sum_{I\in\mathcal G}\mu(B(I))
=\sum_jW_j
&\le\sum_ja_j\\
&\le\prod_j(1+a_j)-1\\
&=\frac1{\prod_jF_j}-1\\
&\le\frac32-1=\frac12.
\end{aligned}
$$

The second inequality retains the nonnegative mixed terms in the product. It avoids summing a fixed one-half allowance for each block. With no blocks, the sum is zero and the empty product is one. Combined with Section 1, this proves the theorem.

## 4. Consequences and limits

**Homogeneous measure.** Taking $p_j=p$ recovers the standard homogeneous q-cover weights $p^{|I|}$, now for every disjoint partition-quota family under the q=3 mass threshold.

**Containment certificate.** If an arbitrary family $D_0$ contains a partition-quota family $D$ satisfying this theorem, then $D_0^{(3)}\subseteq D^{(3)}$. The same explicit generators therefore cover $D_0^{(3)}$ with cost at most one half. This is a certificate when such a contained family is actually given; it does not assert that every high-mass family has one.

**Probability scope.** The input theorem (T) uses identical probabilities within one binomial block. This proof retains that condition. It establishes no q=3 conclusion for unequal probabilities within a block. The existing q=4 note still supplies its distinct theorem for arbitrary independent coordinate probabilities.

**Constraint scope.** Disjointness supplies both the three-way construction and the product factorization. Overlapping quotas, general matroids and the arbitrary-family problem require further arguments.

## Source and collaboration record

The retained dependencies are the threshold proof at blob **d555833e2524b7ede05208ff2955d520a6ae1e16** and the partition q=4 note at blob **8f870b7ff4be6b4e16ef171a662e1c8209c8ae9f**. The present proof explicitly depends on (T); it does not present a new independent derivation of that established input.

The original q=3 [work thread](https://tokenjunkielabs.slack.com/archives/C0C3MEWHTR6/p1790150837761739), original partition [delivery](https://github.com/woahwhattheheck/commons/pull/19329), heterogeneous [extension](https://github.com/woahwhattheheck/commons/pull/19330), and finite [carrier](https://github.com/woahwhattheheck/commons/pull/16506) retain their provenance. This continuation edits only this new note and the directory README. It uses analytic reasoning; no parameter enumeration or runtime evidence is claimed.
