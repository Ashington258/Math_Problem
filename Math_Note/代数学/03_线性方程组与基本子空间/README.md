# 线性方程组与基本子空间

对于 $A\in\mathbb F^{m\times n}$，方程 $Ax=b$ 是求线性映射 $T_A:\mathbb F^n\to\mathbb F^m$ 的原像。列空间决定是否有解，零空间决定解的自由度。

- [线性方程组的主线任务](./线性方程组的主线任务.md)：可解性、唯一性和通解结构，含四个典型例子。
- [列空间、零空间与解集](./列空间、零空间与解集.md)：基本定义、规范记号和求法。
- [线性映射与矩阵方程的几何结构解析](./线性映射与矩阵方程的几何结构解析.md)：四个基本子空间、正交分解与解集几何。
- [矩阵左右乘对四个基本子空间的影响](./矩阵左右乘对四个基本子空间的影响.md)：一般乘法与可逆乘法下四个子空间如何变化。
- [矩阵乘积为零时的子空间关系](./矩阵乘积为零时的子空间关系.md)：由 $AB=0$ 推出 $\operatorname{Col}(B)\subseteq\ker(A)$ 及其等价表述。

核心关系：

$$
Ax=b\text{ 有解}\iff b\in\operatorname{Col}(A),
\qquad
S_b=x_p+\ker(A),
\qquad
\operatorname{rank}(A)+\dim\ker(A)=n .
$$

解集的唯一分解 $x=x_r+x_{\text{null}}$（$x_r\in\operatorname{Row}(A)$ 唯一、$x_{\text{null}}\in\ker(A)$）见 [几何结构解析](./线性映射与矩阵方程的几何结构解析.md) §2、§5。

[返回代数学索引](../README.md)
