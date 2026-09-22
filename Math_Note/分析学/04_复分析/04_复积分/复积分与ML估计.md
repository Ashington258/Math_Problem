# 复积分与 ML 估计

复积分不是“复数值的实积分”这么简单：由于 $dz$ 本身带方向，积分对**围道的形状与走向**极其敏感。本篇把定义、算法、估计与路径无关性一次讲清。

> **必须掌握的输出**：能用 ML 估计证明圆弧段积分趋于 $0$；能判断何时积分与路径无关。

## 1. 定义

### 1.1 曲线与围道

**曲线**是连续映射 $\gamma:[a,b]\to\mathbb C$；称为**光滑**若 $\gamma'$ 存在且连续且 $\gamma'\ne0$；**分段光滑**指可分成有限段光滑曲线；**简单闭曲线**指不自我相交且起点等于终点，此时称**围道**（contour）。逆时针方向记为**正方向**。

### 1.2 积分定义

沿分段光滑曲线 $\gamma$ 定义

$$
\int_\gamma f(z)\,dz=\lim_{\text{分割细度}\to0}\sum_{k}f(\zeta_k)(z_k-z_{k-1}).
$$

把它拆成实数形式会更清楚：$dz=dx+i\,dy$，故

$$
\int_\gamma f\,dz
=\int_\gamma (u\,dx-v\,dy)+i\int_\gamma (v\,dx+u\,dy).
$$

**结论：复积分 = 两条实的第二类曲线积分。** 因此 `02_多元微积分` 中的路径无关性、Green 公式可以直接搬运。

## 2. 参数化算法

若 $\gamma(t)=x(t)+iy(t)$，$t\in[a,b]$，则

$$
\boxed{\;
\int_\gamma f(z)\,dz=\int_a^{b}f\bigl(\gamma(t)\bigr)\gamma'(t)\,dt\;}
$$

积分变成关于实参数 $t$ 的普通复值积分。

### 2.1 三个标准参数化

| 曲线 | 参数化 | $dz$ |
| --- | --- | --- |
| 线段 $z_0\to z_1$ | $z_0+t(z_1-z_0)$，$t\in[0,1]$ | $(z_1-z_0)\,dt$ |
| 圆弧 $z_0+re^{i\theta}$ | $\theta:\alpha\to\beta$ | $ire^{i\theta}\,d\theta$ |
| 正向圆周 $\lvert z-z_0\rvert=r$ | $\theta:0\to2\pi$ | $ire^{i\theta}\,d\theta$ |

## 3. 基本性质

1. **线性**：$\displaystyle\int_\gamma(\alpha f+\beta g)\,dz=\alpha\int_\gamma f\,dz+\beta\int_\gamma g\,dz$。
2. **反向变号**：$\displaystyle\int_{-\gamma}f\,dz=-\int_\gamma f\,dz$。
3. **分段可加**：$\displaystyle\int_{\gamma_1+\gamma_2}=\int_{\gamma_1}+\int_{\gamma_2}$。
4. **与曲线形状有关**：一般地 $\displaystyle\int_\gamma f\,dz$ 不能只看端点。

性质 4 是全课后续内容的存在理由：第 5 章要找出**什么时候它只依赖端点**。

## 4. ML 估计

### 4.1 定理

若 $f$ 在 $\gamma$ 上连续且 $\lvert f(z)\rvert\le M$，$\gamma$ 的弧长为 $L$，则

$$
\boxed{\;
\left\lvert\int_\gamma f(z)\,dz\right\rvert\le ML \;}
$$

### 4.2 证明思路

对任意分割，

$$
\left\lvert\sum_k f(\zeta_k)\Delta z_k\right\rvert
\le\sum_k\lvert f(\zeta_k)\rvert\,\lvert\Delta z_k\rvert
\le M\sum_k\lvert\Delta z_k\rvert\le ML,
$$

取极限即得。关键在于把“复数的绝对值不等式”与“折线长度”分离。

### 4.3 圆弧趋于零的标准套路

设 $\gamma_R$ 是以 $z_0$ 为心、半径 $R$、张角 $\le\pi$ 的圆弧。则 $L=\pi R$。若在 $\gamma_R$ 上 $\lvert f(z)\rvert\le\dfrac{C}{R^{2}}$（例如 $f(z)=\dfrac{1}{z^{2}+1}$ 在 $R\to\infty$ 时），就得到

$$
\left\lvert\int_{\gamma_R}f\,dz\right\rvert\le\frac{C}{R^{2}}\cdot\pi R=\frac{\pi C}{R}\longrightarrow0 .
$$

这就是第 9 章“大圆弧贡献为零”的全部机制：**分母比分子高一阶，弧长只涨一阶**。

## 5. 关键积分 $\oint z^{n}\,dz$

绕正向圆周 $\lvert z-z_0\rvert=r$ 积分 $f(z)=(z-z_0)^{n}$（$n\in\mathbb Z$）。参数化 $z=z_0+re^{i\theta}$，得

$$
\oint (z-z_0)^{n}dz
=\int_0^{2\pi}r^{n}e^{in\theta}\cdot ire^{i\theta}d\theta
=ir^{n+1}\int_0^{2\pi}e^{i(n+1)\theta}d\theta .
$$

于是

$$
\oint_{\lvert z-z_0\rvert=r}(z-z_0)^{n}dz=
\begin{cases}
2\pi i, & n=-1,\\
0, & n\ne-1.
\end{cases}
$$

这三行是留数定理的原子。特别地

$$
\boxed{\;\oint_{\lvert z-z_0\rvert=r}\frac{dz}{z-z_0}=2\pi i\;}
$$

它说明 $\dfrac1z$ 在挖去原点的区域上没有原函数，这一“异常”正是留数的来源。

## 6. 原函数与路径无关

### 6.1 定义

若存在全纯函数 $F$ 使 $F'=f$，则称 $F$ 是 $f$ 的**原函数**。

### 6.2 定理

在区域 $D$ 上，下列命题等价：

1. $f$ 在 $D$ 上有原函数；
2. 对 $D$ 内任意围道 $\gamma$ 都有 $\displaystyle\oint_\gamma f\,dz=0$；
3. 积分与路径无关，只依赖起点与终点，可写成 $\displaystyle\int_{z_0}^{z_1}f\,dz=F(z_1)-F(z_0)$。

**充分性的构造**：固定 $z_0$，定义 $F(z)=\int_{z_0}^{z}f(\zeta)d\zeta$（需先用条件 2 说明它与路径无关），再验证 $F'=f$。

### 6.3 与对称性/保守场的类比

这与 `02_多元微积分` 中“保守场 $\iff$ 环量为零 $\iff$ 存在势函数”完全同构：

$$
\text{复积分路径无关}
\ \longleftrightarrow\
\text{实二维保守场}.
$$

Cauchy 定理（第 5 章）的本质，就是断言**全纯函数的场一定是保守的**。

## 7. 例子

### 7.1 用参数化直接算

计算 $\displaystyle\int_{\gamma}\overline z\,dz$，其中 $\gamma$ 是从 $0$ 到 $1+i$ 的直线段。参数化 $z=(1+i)t$，$t\in[0,1]$，则 $\overline z=(1-i)t$，$dz=(1+i)dt$：

$$
\int_0^{1}(1-i)t(1+i)\,dt=\int_0^{1}2t\,dt=1 .
$$

若改沿折线 $0\to1\to1+i$：第一段 $\overline z=t$，$dz=dt$，得 $\frac12$；第二段 $z=1+it$，$\overline z=1-it$，$dz=i\,dt$，得 $\int_0^1(1-it)i\,dt=i+\frac12$。总计 $1+i\ne1$。

$$
\text{结论：}\overline z\ \text{的积分依赖路径，它没有原函数。}
$$

这也与 $\overline z$ 不全纯相呼应。

### 7.2 ML 估计的典型用法

证明 $\displaystyle\lim_{R\to\infty}\int_{\gamma_R}\frac{e^{iz}}{z}\,dz=0$ 需要更精细的 Jordan 引理（第 9 章），但若换成 $\dfrac{1}{z^{2}}$，直接用 ML：$\lvert f\rvert\le1/R^{2}$，$L=\pi R$，上界 $\pi/R\to0$ 即可。

### 7.3 圆周积分

$$
\oint_{\lvert z\rvert=2}\frac{dz}{z}=2\pi i,\qquad
\oint_{\lvert z\rvert=2}\frac{dz}{z^{2}}=0 .
$$

第二式可理解为：$\dfrac{1}{z^{2}}$ 在挖去原点的区域上有原函数 $-\dfrac1z$。

> **必须掌握的输出（本阶段）**：会写三种参数化；会用 ML 卡上界证明圆弧为零；记得 $\oint dz/(z-z_0)=2\pi i$ 而其余幂次为零。

## 8. 小结

- 复积分 = 两条实曲线积分，方向敏感。
- ML 估计把“复积分上界”与“弧长”解耦，是后续极限论证的主力。
- 原函数存在 / 环量为零 / 路径无关三者等价；全纯性将保证这一点（Cauchy 定理）。

[返回本节索引](./README.md)
