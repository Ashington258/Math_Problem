# Jordan 引理与围道设计

上一节给出了三种标准积分，但真正的技术难点都在“补充段为什么为零”和“极点落在围道上怎么办”。本篇把这两件事讲透，并完整推出目标例题

$$
\int_{-\infty}^{\infty}\frac{\cos x}{1+x^{2}}\,dx=\frac{\pi}{e}.
$$

> **必须掌握的输出**：会用 Jordan 引理处理带 $e^{iaz}$ 的大圆弧；会为实轴上的极点设计缩进围道。

## 1. 大圆弧的两条判据

### 1.1 大圆弧引理（ML 型）

若在圆弧 $C_R:\lvert z\rvert=R,\ \theta\in[\alpha,\beta]$ 上 $\lvert f(z)\rvert\le\dfrac{C}{R^{k}}$（$k>1$），则

$$
\left\lvert\int_{C_R}f\,dz\right\rvert\le\frac{C}{R^{k}}(\beta-\alpha)R
=\frac{C(\beta-\alpha)}{R^{k-1}}\xrightarrow[R\to\infty]{}0 .
$$

这是第 4 章 ML 估计的直接应用，也是有理函数型的通行证。**条件是分母比分子至少高一阶。**

### 1.2 Jordan 引理

$$
\text{若 }f\ \text{在} \operatorname{Im}z\ge0 \text{上满足} \lvert f(z)\rvert\to0\ (\lvert z\rvert\to\infty),
\text{ 则 } \int_{C_R}f(z)e^{iaz}dz\xrightarrow[R\to\infty]{}0\quad(a>0).
$$

**为什么需要它**：$e^{iaz}$ 在 $\operatorname{Im}z>0$ 时模为 $e^{-a\operatorname{Im}z}$，**指数衰减**；但衰减最快的区域是正虚轴附近，靠近实轴的部分几乎不衰减，因此**不能**用 ML 引理直接卡（那会得到“$L=O(R)$，被积函数 $\approx1$”的无效估计）。Jordan 的做法是分片估计。

**证明要点**：写 $z=Re^{i\theta}$，$\operatorname{Im}z=R\sin\theta$，于是

$$
\left\lvert\int_{C_R}f e^{iaz}dz\right\rvert
\le\max\lvert f\rvert\cdot R\int_0^{\pi}e^{-aR\sin\theta}d\theta .
$$

用 $\sin\theta\ge\dfrac{2\theta}{\pi}$（$0\le\theta\le\frac\pi2$）并对 $[0,\pi]$ 用对称性：

$$
R\int_0^{\pi}e^{-aR\sin\theta}d\theta
=2R\int_0^{\pi/2}e^{-aR\sin\theta}d\theta
\le2R\int_0^{\pi/2}e^{-2aR\theta/\pi}d\theta
\le\frac{\pi}{a}.
$$

于是积分的模被 $\dfrac{\pi}{a}\max_{\lvert z\rvert=R}\lvert f(z)\rvert$ 控制，由 $\lvert f\rvert\to0$ 得极限为 $0$。

**结论**：Jordan 引理把“衰减”这件事从被积函数 $f$ 转移到了指数因子 $e^{iaz}$ 上；只要 $a>0$ 且 $f\to0$，大弧就贡献为零。

## 2. 围道选型对照表

| 积分类型 | 选哪个半平面 | 关键条件 | 补充段为零的理由 |
| --- | --- | --- | --- |
| 有理函数 $\int P/Q$ | 上半 | $\deg Q\ge\deg P+2$ | ML 引理 |
| $\int f(x)\cos ax$（$a>0$） | 上半，乘 $e^{iaz}$ | $f\to0$ | Jordan 引理 |
| $\int f(x)\cos ax$（$a<0$） | **下半**，乘 $e^{iaz}$ | $f\to0$ | Jordan 引理（下半取 $e^{-iaz}$） |
| 三角有理式 | 单位圆 | 极点不在圆上 | 无补充段 |
| 含 $x^{a}$ / $\ln x$ | keyhole | $0<a<1$ 等指数条件 | 大小两圆各用 ML |

符号提醒：$e^{iaz}$ 在**上半**平面衰减需 $a>0$；$a<0$ 时必须改用下半平面，此时围道取顺时针，最终整体符号为负。

## 3. 缩进围道

### 3.1 问题

若极点恰好落在实轴上（如 $\dfrac{\sin x}{x}$ 在 $x=0$、$\dfrac{1}{x^{2}-a^{2}}$ 在 $x=\pm a$），围道直接穿过极点，积分无定义。补救办法是把围道在极点附近**挖一个小半圆**绕过去。

### 3.2 小半圆的贡献

设 $z_0$ 是 $f$ 的一阶极点，用小半圆 $z=z_0+\varepsilon e^{i\theta}$ 绕过。由于

$$
f(z)=\frac{\operatorname{Res}_{z_0}f}{z-z_0}+O(1),
$$

小半圆上的积分趋于 $\operatorname{Res}_{z_0}f\cdot i(\theta_{\text{终}}-\theta_{\text{始}})$，即**一个 $i\pi$ 乘留数**。具体符号由绕行方向决定。在常用的“上半平面逆时针围道 + 小半圆凸向上方”设置下：

$$
\int_{\text{小半圆}}f\,dz\longrightarrow-\pi i\operatorname{Res}_{z_0}f .
$$

### 3.3 主值公式

在上半平面围道、且两个补充段都趋于零的前提下（即大弧用 ML 或 Jordan 说明为 $0$，小弧如上取值）：

$$
\boxed{\;
\operatorname{PV}\int_{-\infty}^{\infty}f(x)\,dx
=2\pi i\!\!\sum_{\operatorname{Im}z_k>0}\!\!\operatorname{Res}_{z_k}f
+\pi i\!\!\sum_{\text{实轴上一阶极点}}\!\!\operatorname{Res}f\;}
$$

**注意**：实轴极点贡献的是 $\pi i$（半个 $2\pi i$），这正是“只绕了一半”的几何后果。

### 3.4 例：Dirichlet 积分

$$
\int_{-\infty}^{\infty}\frac{\sin x}{x}\,dx=\pi .
$$

取 $f(z)=\dfrac{e^{iz}}{z}$，围道为上半平面取缩进版（在 $0$ 处凸向上方）。围道内无极点，故 $\oint=0$；大弧由 Jordan 引理为零；小弧贡献 $-\pi i\cdot1=-\pi i$。于是

$$
\operatorname{PV}\int_{-\infty}^{\infty}\frac{e^{ix}}{x}dx-\pi i=0
\ \Longrightarrow\
\operatorname{PV}\int_{-\infty}^{\infty}\frac{e^{ix}}{x}dx=\pi i .
$$

取虚部（被积函数的虚部是偶函数，主值即普通积分）：

$$
\int_{-\infty}^{\infty}\frac{\sin x}{x}dx=\operatorname{Im}(\pi i)=\pi .
$$

这个积分在信号处理中给出理想低通滤波器的冲激响应，是 sinc 函数的归一化常数。

## 4. 目标例题：$\displaystyle\int_{-\infty}^{\infty}\frac{\cos x}{1+x^{2}}dx=\frac{\pi}{e}$

### 4.1 改为复积分

$\cos x$ 在实轴上无界（复平面中会指数增长），故不能直接对 $\dfrac{\cos z}{1+z^{2}}$ 积分。标准做法是用 Euler 公式取实部：

$$
\int_{-\infty}^{\infty}\frac{\cos x}{1+x^{2}}dx
=\operatorname{Re}\int_{-\infty}^{\infty}\frac{e^{ix}}{1+x^{2}}dx .
$$

令

$$
f(z)=\frac{e^{iz}}{1+z^{2}}=\frac{e^{iz}}{(z-i)(z+i)} .
$$

### 4.2 选围道

取上半平面半圆围道 $\gamma_R=[-R,R]\cup C_R$，其中 $C_R$ 为上半圆（逆时针）。选择上半平面的理由：$e^{iz}=e^{ix}e^{-y}$ 要衰减，必须 $y>0$。

### 4.3 大弧为零

在 $\lvert z\rvert=R$ 上 $\left\lvert\dfrac{1}{1+z^{2}}\right\rvert\le\dfrac{1}{R^{2}-1}\to0$，且 $a=1>0$，满足 Jordan 引理条件：

$$
\int_{C_R}f\,dz\xrightarrow[R\to\infty]{}0 .
$$

### 4.4 求留数

$f$ 的极点 $z=\pm i$，只有 $z=i$ 在上半平面，且为一阶。用 $\dfrac{g}{h}$ 公式：$g=e^{iz}$，$h=1+z^{2}$，$h'(z)=2z$，

$$
\operatorname{Res}_{z=i}f=\frac{e^{i\cdot i}}{2i}=\frac{e^{-1}}{2i}=-\frac{i}{2e}.
$$

### 4.5 求围道积分

$$
\oint_{\gamma_R}f\,dz=2\pi i\cdot\Bigl(-\frac{i}{2e}\Bigr)
=\frac{2\pi i\cdot(-i)}{2e}=\frac{\pi}{e} .
$$

### 4.6 收官

由 $R\to\infty$ 时大弧为零，

$$
\int_{-\infty}^{\infty}\frac{e^{ix}}{1+x^{2}}dx=\frac{\pi}{e},
$$

取实部即得

$$
\boxed{\;\int_{-\infty}^{\infty}\frac{\cos x}{1+x^{2}}dx=\frac{\pi}{e}\;}
$$

顺便得到两个副产品：虚部为零，说明

$$
\int_{-\infty}^{\infty}\frac{\sin x}{1+x^{2}}dx=0
$$

（被积函数是奇函数，与对称性一致）；以及由偶函数性

$$
\int_{0}^{\infty}\frac{\cos x}{1+x^{2}}dx=\frac{\pi}{2e}\approx0.5779 .
$$

### 4.7 复盘：这道题用到了本区几乎全部内容

| 步骤 | 依赖章节 |
| --- | --- |
| 用 $e^{iz}$ 换 $\cos z$ | 第 3 章（指数函数无界，三角函数无界） |
| 选上半平面 | 第 3 章（$e^{iz}$ 的衰减方向） |
| 大弧为零 | 第 4 章 ML + 本篇 Jordan 引理 |
| 定阶与留数 | 第 7 章 |
| 围道求和 | 第 8 章留数定理 |

因此这道题可以当作本区的“总测验”。

## 5. 自检清单

做任何围道积分前，依次确认：

> **Step1:** 被积函数的实/虚部与奇偶性，是否可以先化简 $[0,\infty)$ 上的积分？
> **Step2:** 奇点在哪？有几个落在所选半平面内？是否落在围道上（需缩进）？
> **Step3:** 大弧用什么理由为零（ML 还是 Jordan）？$a$ 的符号与半平面是否匹配？
> **Step4:** 小弧贡献写对符号没有（$\pm\pi i\operatorname{Res}$）？
> **Step5:** 最后一步是否把 $e^{iz}$ 的实部/虚部正确取回？

**必须掌握的输出（本阶段）**：能独立、无提示地写出 §4 的六个步骤，并解释每一步的依据。

[返回本节索引](./README.md)
