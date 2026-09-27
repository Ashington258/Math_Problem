# 内积与 Gram–Schmidt 正交化

本篇在实数域上讨论有限维内积空间。内积（inner product）$\langle u,v\rangle$ 对两个变量分别线性、对称，且 $\langle v,v\rangle>0$（$v\neq0$）。它给出范数 $\lVert v\rVert=\sqrt{\langle v,v\rangle}$ 与正交关系 $u\perp v\iff\langle u,v\rangle=0$。标准欧氏内积是 $\langle u,v\rangle=u^{\mathsf T}v$。

复数域上的内积需把对称改为共轭对称，并在一个变量上使用共轭线性；相应矩阵公式使用共轭转置 $A^{H}$。

## 1. 正交补与投影

子空间 $U\subseteq V$ 的正交补（orthogonal complement）是

$$
U^\perp=\{v\in V:\langle v,u\rangle=0\text{ 对所有 }u\in U\}.
$$

有限维内积空间有正交直和 $V=U\oplus U^\perp$。若 $q_1,\dots,q_k$ 是 $U$ 的标准正交基，则 $v$ 在 $U$ 上的正交投影为

$$
\operatorname{proj}_U(v)=\sum_{i=1}^k\langle v,q_i\rangle q_i.
$$

于是 $v=\operatorname{proj}_U(v)+(v-\operatorname{proj}_U(v))$，第二项属于 $U^\perp$。对实矩阵 $A$，四个基本子空间满足 $\ker(A)=\operatorname{Row}(A)^\perp$ 和 $\ker(A^{\mathsf T})=\operatorname{Col}(A)^\perp$。

## 2. Gram–Schmidt 正交化

给定线性无关向量 $v_1,\dots,v_k$，依次构造

$$
u_1=v_1,\qquad q_1=\frac{u_1}{\lVert u_1\rVert},
$$

$$
u_j=v_j-\sum_{i=1}^{j-1}\langle v_j,q_i\rangle q_i,
\qquad q_j=\frac{u_j}{\lVert u_j\rVert}\quad(j\geq2).
$$

每个 $u_j$ 去掉了 $v_j$ 在先前方向上的投影。线性无关保证 $u_j\neq0$；所得 $q_1,\dots,q_k$ 两两正交且范数为 $1$，并与原向量组张成同一子空间。由此可将有限维内积空间的任意基正交化。

## 3. 一个计算例子

在 $\mathbb R^2$ 中取 $v_1=(1,1)^{\mathsf T}$、$v_2=(1,0)^{\mathsf T}$。先得 $q_1=(1,1)^{\mathsf T}/\sqrt2$。再减去投影：

$$
u_2=v_2-\langle v_2,q_1\rangle q_1
=(1,0)^{\mathsf T}-(1/2,1/2)^{\mathsf T}
=(1/2,-1/2)^{\mathsf T},
$$

故 $q_2=(1,-1)^{\mathsf T}/\sqrt2$。两向量组成 $\mathbb R^2$ 的标准正交基。

三维空间的特殊计算技巧见[叉积简化三维 Gram–Schmidt 正交化](./叉积简化三维Gram-Schmidt正交化.md)；一般形式及其矩阵表示见[双线性形式](./双线性形式.md)。

[返回本节索引](./README.md)
