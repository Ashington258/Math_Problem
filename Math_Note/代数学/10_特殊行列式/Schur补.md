## 1. Schur 补的原理与推导

设分块矩阵

\[
M=
\begin{pmatrix}
A&B\\
C&D
\end{pmatrix},
\]

其中各块尺寸相容。

### 1.1 原理：分块高斯消元

普通高斯消元利用某个非零元素消去其他元素；Schur 补则是利用一个可逆矩阵块，消去另一个矩阵块。

假设 \(D\) 可逆。左乘分块初等矩阵

\[
L=
\begin{pmatrix}
I&-BD^{-1}\\
0&I
\end{pmatrix}.
\]

因为 \(L\) 是分块三角矩阵，

\[
\det L=1.
\]

计算：

\[
\begin{aligned}
LM
&=
\begin{pmatrix}
I&-BD^{-1}\\
0&I
\end{pmatrix}
\begin{pmatrix}
A&B\\
C&D
\end{pmatrix}\\[4pt]
&=
\begin{pmatrix}
A-BD^{-1}C&B-BD^{-1}D\\
C&D
\end{pmatrix}\\[4pt]
&=
\begin{pmatrix}
A-BD^{-1}C&0\\
C&D
\end{pmatrix}.
\end{aligned}
\]

这就把右上角的 \(B\) 消掉了。

其中

\[
\boxed{S_D=A-BD^{-1}C}
\]

称为 \(D\) 在 \(M\) 中的 Schur 补。

由于 \(\det L=1\)，所以

\[
\det M=\det(LM).
\]

而 \(LM\) 是分块下三角矩阵，因此

\[
\det(LM)
=
\det(A-BD^{-1}C)\det D.
\]

最终得到

\[
\boxed{
\det
\begin{pmatrix}
A&B\\
C&D
\end{pmatrix}
=
\det D\,
\det(A-BD^{-1}C)
}
\]

前提是 \(D\) 可逆。



### 1.2 如果 \(A\) 可逆

同理，左乘

\[
\begin{pmatrix}
I&0\\
-CA^{-1}&I
\end{pmatrix},
\]

得到

\[
\begin{aligned}
&
\begin{pmatrix}
I&0\\
-CA^{-1}&I
\end{pmatrix}
\begin{pmatrix}
A&B\\
C&D
\end{pmatrix}\\[4pt]
&=
\begin{pmatrix}
A&B\\
0&D-CA^{-1}B
\end{pmatrix}.
\end{aligned}
\]

所以

\[
\boxed{
S_A=D-CA^{-1}B
}
\]

是 \(A\) 在 \(M\) 中的 Schur 补，并且

\[
\boxed{
\det M
=
\det A\,
\det(D-CA^{-1}B)
}.
\]



### 1.3 从方程组理解 Schur 补

考虑分块方程组

\[
\begin{pmatrix}
A&B\\
C&D
\end{pmatrix}
\begin{pmatrix}
x\\
y
\end{pmatrix}
=
\begin{pmatrix}
f\\
g
\end{pmatrix}.
\]

它等价于

\[
\begin{cases}
Ax+By=f,\\
Cx+Dy=g.
\end{cases}
\]

如果 \(D\) 可逆，由第二个方程得到

\[
y=D^{-1}(g-Cx).
\]

代入第一个方程：

\[
Ax+BD^{-1}(g-Cx)=f,
\]

整理得

\[
\boxed{
(A-BD^{-1}C)x=f-BD^{-1}g
}.
\]

因此，消去变量 \(y\) 后，变量 \(x\) 的有效系数矩阵正是

\[
A-BD^{-1}C.
\]

这就是 Schur 补的本质：

\[
\boxed{\text{消去一组变量后，剩余变量所对应的有效矩阵}}
\]



## 2. 低秩修正行列式公式的推导

设

\[
A\in\mathbb F^{n\times n}
\]

可逆，并且

\[
U,V\in\mathbb F^{n\times r}.
\]

于是

\[
UV^{\mathsf T}\in\mathbb F^{n\times n},
\qquad
V^{\mathsf T} A^{-1}U\in\mathbb F^{r\times r}.
\]

我们要证明

\[
\boxed{
\det(A+UV^{\mathsf T})
=
\det A\,
\det(I_r+V^{\mathsf T} A^{-1}U)
}.
\]

### 2.1 构造分块矩阵

考虑

\[
K=
\begin{pmatrix}
A&U\\
-V^{\mathsf T}&I_r
\end{pmatrix}.
\]

对同一个 \(K\)，分别使用两个方向的 Schur 补。



### 2.2 对 \(I_r\) 做 Schur 补

因为 \(I_r\) 可逆，

\[
\begin{aligned}
\det K
&=
\det(I_r)
\det\left(
A-U I_r^{-1}(-V^{\mathsf T})
\right)\\
&=
\det(A+UV^{\mathsf T}).
\end{aligned}
\]

所以

\[
\boxed{\det K=\det(A+UV^{\mathsf T})}.
\]



### 2.3 对 \(A\) 做 Schur 补

因为 \(A\) 可逆，

\[
\begin{aligned}
\det K
&=
\det A\,
\det\left(
I_r-(-V^{\mathsf T})A^{-1}U
\right)\\
&=
\det A\,
\det\left(
I_r+V^{\mathsf T} A^{-1}U
\right).
\end{aligned}
\]

所以

\[
\boxed{
\det K
=
\det A\,
\det(I_r+V^{\mathsf T} A^{-1}U)
}.
\]



### 2.4 比较两个结果

两个式子计算的是同一个 \(\det K\)，因此

\[
\boxed{
\det(A+UV^{\mathsf T})
=
\det(I_r+V^{\mathsf T} A^{-1}U)\det A
}.
\]

这说明矩阵行列式引理就是：

\[
\boxed{\text{对同一个分块矩阵，从两个方向计算 Schur 补}}
\]

## 3. 秩一情形

当 \(r=1\) 时，令

\[
U=u,\qquad V=v,
\]

其中 \(u,v\in\mathbb F^n\)。

这时

\[
V^{\mathsf T} A^{-1}U=v^{\mathsf T} A^{-1}u
\]

是一个标量，因此

\[
\det(I_1+v^{\mathsf T} A^{-1}u)
=
1+v^{\mathsf T} A^{-1}u.
\]

于是得到

\[
\boxed{
\det(A+uv^{\mathsf T})
=
\det A\left(1+v^{\mathsf T} A^{-1}u\right)
}.
\]

## 4. 公式的降维意义

左边是一个 \(n\) 阶行列式：

\[
\det(A+UV^{\mathsf T}),
\]

右边新增的行列式只有 \(r\) 阶：

\[
\det(I_r+V^{\mathsf T} A^{-1}U).
\]

当 \(r\ll n\) 时，

\[
\boxed{
n\text{ 阶行列式}
\longrightarrow
r\text{ 阶行列式}
}
\]

这就是低秩修正公式的核心价值，也是 Schur 补“消元并降维”思想的直接体现。