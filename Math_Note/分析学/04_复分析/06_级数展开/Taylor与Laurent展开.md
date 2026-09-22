# Taylor 与 Laurent 展开

全纯函数在局部“长得像多项式”，这句话的精确含义就是幂级数展开。当展开中心本身就是奇点时，多出的负幂项不但不是麻烦，反而是留数计算的直接来源。

> **必须掌握的输出**：会展开几个标准函数并判断收敛域；能说出负幂项系数与留数的关系。

## 1. 复级数

### 1.1 收敛与绝对收敛

$\sum_{n\ge0}w_n$ 收敛指部分和序列收敛。若 $\sum\lvert w_n\rvert$ 收敛则称**绝对收敛**，此时任意重排都不改变和。判敛工具基本照搬实分析：比值判别法、根值判别法、比较判别法。特别地

$$
\sum_{n\ge0}w_n\ \text{绝对收敛}\ \Longrightarrow\ \sum_{n\ge0}w_n\ \text{收敛}.
$$

### 1.2 幂级数与收敛半径

形如 $\displaystyle\sum_{n\ge0}a_n(z-z_0)^{n}$ 的级数称为**幂级数**。存在 $R\in[0,\infty]$ 使

$$
\lvert z-z_0\rvert<R\ \text{时绝对收敛},\qquad
\lvert z-z_0\rvert>R\ \text{时发散},
$$

$R$ 称为**收敛半径**，由 Cauchy–Hadamard 公式给出

$$
\frac1R=\limsup_{n\to\infty}\lvert a_n\rvert^{1/n}.
$$

在收敛圆内，幂级数定义的全纯函数满足**逐项可导、逐项可积**，且导函数仍是幂级数。这是“级数可以放心操作”的许可证。

### 1.3 收敛半径的几何含义

$$
R=\text{展开中心到最近奇点的距离}.
$$

这条经验规则极其好用：$\dfrac{1}{1+z^{2}}$ 在 $z_0=0$ 处的展开半径是 $1$（奇点 $\pm i$ 距离为 $1$），尽管函数在实轴上看不出任何异常。这是复分析“隐藏的奇点决定可见的行为”的典型例证。

## 2. Taylor 定理

### 2.1 定理

设 $f$ 在 $\lvert z-z_0\rvert<R$ 内全纯，则在该圆盘内

$$
f(z)=\sum_{n=0}^{\infty}\frac{f^{(n)}(z_0)}{n!}(z-z_0)^{n},
$$

且此展开唯一。结合第 5 章的导数公式，$n$ 阶系数有围道表示

$$
a_n=\frac{f^{(n)}(z_0)}{n!}=\frac{1}{2\pi i}\oint_{\lvert \zeta-z_0\rvert=r}\frac{f(\zeta)}{(\zeta-z_0)^{n+1}}\,d\zeta .
$$

### 2.2 为什么“全纯 = 解析”

Taylor 定理说明全纯函数在每点局部都是幂级数；反过来，幂级数在其收敛圆内显然全纯。于是

$$
\text{全纯}\iff\text{可展为幂级数（解析）}.
$$

这个等价在实分析中不成立（$e^{-1/x^{2}}$ 光滑但 Taylor 级数不收敛于自身），原因正是实函数没有第 5 章那套围道结构。

### 2.3 标准展开表

| 函数 | 展开 | 收敛域 |
| --- | --- | --- |
| $\dfrac{1}{1-z}$ | $\displaystyle\sum_{n\ge0}z^{n}$ | $\lvert z\rvert<1$ |
| $e^{z}$ | $\displaystyle\sum_{n\ge0}\frac{z^{n}}{n!}$ | 全平面 |
| $\sin z$ | $\displaystyle\sum_{n\ge0}\frac{(-1)^{n}z^{2n+1}}{(2n+1)!}$ | 全平面 |
| $\cos z$ | $\displaystyle\sum_{n\ge0}\frac{(-1)^{n}z^{2n}}{(2n)!}$ | 全平面 |
| $\operatorname{Log}(1+z)$ | $\displaystyle\sum_{n\ge1}\frac{(-1)^{n+1}z^{n}}{n}$ | $\lvert z\rvert<1$ |
| $(1+z)^{\alpha}$ | $\displaystyle\sum_{n\ge0}\binom{\alpha}{n}z^{n}$ | $\lvert z\rvert<1$ |

$\operatorname{Log}(1+z)$ 的展开对实变量同样成立，但只有在复平面里才能看清收敛半径为什么恰好是 $1$（奇点在 $z=-1$）。

## 3. Laurent 级数

### 3.1 从圆盘到圆环

在 $z_0$ 处有奇点时，Taylor 展开失效。改在**圆环**

$$
D=\{r<\lvert z-z_0\rvert<R\}
$$

上讨论：若 $f$ 在圆环内及其边界附近全纯，则

$$
\boxed{\;
f(z)=\sum_{n=-\infty}^{\infty}a_n(z-z_0)^{n},
\qquad
a_n=\frac{1}{2\pi i}\oint_{\lvert \zeta-z_0\rvert=\rho}\frac{f(\zeta)}{(\zeta-z_0)^{n+1}}\,d\zeta\;}
$$

其中 $r<\rho<R$ 任取，$R$ 可以取 $\infty$、$r$ 可以取 $0$。

### 3.2 结构分解

$$
f(z)=\underbrace{\sum_{n\ge0}a_n(z-z_0)^{n}}_{\text{解析部分（正则部分）}}
+\underbrace{\sum_{n\ge1}a_{-n}(z-z_0)^{-n}}_{\text{主部}} .
$$

主部决定奇点类型（第 7 章），而

$$
a_{-1}=\operatorname{Res}_{z=z_0}f(z)
$$

是**留数的定义式**。这就把“算留数”与“做 Laurent 展开”绑定在一起。

### 3.3 唯一性

在同一条圆环内 Laurent 展开唯一（同一函数在两条不同圆环上的展开可以不同，见下文例子）。判断展开是否合法的方法是检查**展开所用的几何级数是否在该圆环内收敛**。

## 4. 标准例子

### 4.1 单个奇点的圆环展开

把 $f(z)=\dfrac{1}{z(z-1)}$ 在 $z_0=0$ 附近展开。

在圆环 $0<\lvert z\rvert<1$ 内，利用 $\dfrac{1}{z-1}=-\dfrac{1}{1-z}=-\sum_{n\ge0}z^{n}$：

$$
f(z)=-\frac1z\sum_{n\ge0}z^{n}
=-\frac1z-1-z-z^{2}-\cdots .
$$

主部只有 $-\dfrac1z$ 一项，故 $z=0$ 是一阶极点，$\operatorname{Res}_{z=0}f=-1$。

在圆环 $\lvert z\rvert>1$ 内改为提取 $\dfrac1{z}$：$\dfrac{1}{z-1}=\dfrac1z\cdot\dfrac{1}{1-1/z}=\sum_{n\ge1}\dfrac{1}{z^{n}}$，于是

$$
f(z)=\frac{1}{z^{2}}+\frac{1}{z^{3}}+\cdots
$$

这里 $a_{-1}=0$，说明在 $z_0=0$ 处的留数必须**固定在 $0<\lvert z\rvert<1$ 的那条圆环**上读，两条圆环不能混用。

### 4.2 本质奇点的展开

$$
e^{1/z}=\sum_{n\ge0}\frac{1}{n!\,z^{n}}
=1+\frac1z+\frac{1}{2!z^{2}}+\cdots,\qquad 0<\lvert z\rvert<\infty .
$$

主部含无穷多项，故 $z=0$ 是**本质奇点**，且 $\operatorname{Res}_{z=0}e^{1/z}=a_{-1}=1$。

### 4.3 中心不是奇点的展开

把 $f(z)=\dfrac{1}{1+z^{2}}$ 在 $z_0=1$ 处展开。先写

$$
\frac{1}{1+z^{2}}=\frac{1}{(z-i)(z+i)},
$$

再用部分分式把每一项按 $\dfrac{1}{z-1}$ 的幂整理，得到以 $z=1$ 为心、半径 $R=\sqrt2$（到最近奇点 $i$ 的距离）的展开，收敛圆内有效。这个半径 $\sqrt2$ 再次说明**收敛半径由奇点位置决定**。

## 5. 例子

### 5.1 判断收敛域

$$
\frac{1}{z-3},\quad z_0=0:\qquad
\frac{1}{z-3}=-\frac13\cdot\frac{1}{1-z/3}=-\sum_{n\ge0}\frac{z^{n}}{3^{n+1}},\quad \lvert z\rvert<3 .
$$

在 $\lvert z\rvert>3$ 时改用 $\dfrac{1}{z}\cdot\dfrac{1}{1-3/z}$，得到另一条展开。

### 5.2 用展开读留数

$f(z)=\dfrac{\sin z}{z^{4}}$：$\sin z=z-\dfrac{z^{3}}{6}+\cdots$，故

$$
f(z)=\frac{1}{z^{3}}-\frac{1}{6z}+\frac{z}{120}-\cdots,
$$

$a_{-1}=-\dfrac16$，即 $\operatorname{Res}_{z=0}f=-\dfrac16$（这也与第 7 章公式 $f^{(3)}(0)/3!$ 的对应关系一致）。

> **必须掌握的输出（本阶段）**：展开前先确认圆环；用最少的几何级数把函数凑成形如 $\frac{1}{1-t}$ 或 $\frac{1}{t-1}$ 的结构；$a_{-1}$ 就是留数。

## 6. 小结

- 幂级数的收敛半径由最近奇点决定，这条“几何规则”比公式更好用。
- Taylor 定理把“全纯”与“解析”变成同一件事。
- Laurent 展开把奇点信息压缩进主部：主部长度定类型，$a_{-1}$ 定留数。

[返回本节索引](./README.md)
