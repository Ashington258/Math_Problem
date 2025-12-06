以下是关于矩阵乘积 \(AB = 0\) 时子空间关系的markdown和katex格式表达：

## 📘 笔记：由 \(AB = 0\) 推出的子空间关系

### 一、已知条件

设
\[ 
A \in \mathbb{R}^{m \times n}, \quad B \in \mathbb{R}^{n \times p}, \quad AB = 0.
\]

---

### 二、三个基本关系

\[
\boxed{
\begin{aligned}
1. & \quad \mathrm{Col}(B) \subseteq \ker(A) \\
2. & \quad \mathrm{Row}(A) \subseteq \mathrm{Col}(B)^\perp \\
3. & \quad \mathrm{Col}(A) \subseteq \ker(B^T)
\end{aligned}
}
\]

---

### 三、证明思路

#### (1) \(\mathrm{Col}(B) \subseteq \ker(A)\)

任取 \(x \in \mathbb{R}^p\)，则
\[
ABx = 0 \Rightarrow Bx \in \ker(A),
\]
故列空间中每个向量都被 \(A\) 消去。

---

#### (2) \(\mathrm{Row}(A) \subseteq \mathrm{Col}(B)^\perp\)

设 \(y = z^T A \in \mathrm{Row}(A)\)，
任取 \(v = Bx \in \mathrm{Col}(B)\)，则
\[
y v = z^T A B x = z^T 0 = 0.
\]
说明行空间中的任意向量都与 \(B\) 的列空间正交。

---

#### (3) \(\mathrm{Col}(A) \subseteq \ker(B^T)\)

由 \(AB = 0\) 推得
\[
B^T A^T = 0 \Rightarrow \forall x,\, A^T x \in \ker(B^T),
\]
即 \(\mathrm{Col}(A^T) \subseteq \ker(B^T)\)，也就是
\[
\mathrm{Row}(A) \subseteq \ker(B^T).
\]

---

### 四、几何理解

- \(AB = 0\) 表示矩阵 \(B\) 的输出（即其列空间）完全落入 \(A\) 的零空间中。
- 因此 \(A\) 的行空间与 \(B\) 的列空间互相垂直。
- 同理，\(A\) 的列空间与 \(B^T\) 的核空间互相嵌套。

---

### 五、等号成立的条件（可选补充）

若维数“刚好互补”，即
\[
\dim(\ker(A)) + \dim(\mathrm{Col}(A)) = n,
\quad \dim(\mathrm{Col}(B)) + \dim(\ker(B^T)) = n,
\]
且包含关系无冗余，则可能有
\[
\mathrm{Row}(A) = \mathrm{Col}(B)^\perp, \quad
\mathrm{Col}(A) = \ker(B^T).
\]
但一般情况下仅为“\(\subseteq\)”关系。

---

## 🧩 例子（具体 \(3 \times 3\) 矩阵）

设
\[
A =
\begin{bmatrix}
1 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{bmatrix},
\quad
B =
\begin{bmatrix}
0 & 0 & 0 \\
1 & 0 & 0 \\
0 & 1 & 0
\end{bmatrix}.
\]

计算：
\[
AB =
\begin{bmatrix}
1 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{bmatrix}
\begin{bmatrix}
0 & 0 & 0 \\
1 & 0 & 0 \\
0 & 1 & 0
\end{bmatrix}=
\begin{bmatrix}
0 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{bmatrix}.
\]

---

### 验证结论：

1. **\(\mathrm{Col}(B) \subseteq \ker(A)\)**

   \[
   \mathrm{Col}(B) = \operatorname{span}\{(0,1,0)^T, (0,0,1)^T\},
   \]
   \[
   \ker(A) = \{(0,y,z)^T : y,z \in \mathbb{R}\}.
   \]
   ⟹ 完全相同，结论成立。

---

2. **\(\mathrm{Row}(A) \subseteq \mathrm{Col}(B)^\perp\)**

   \[
   \mathrm{Row}(A) = \operatorname{span}\{(1,0,0)\},
   \quad
   \mathrm{Col}(B)^\perp = \{(x,0,0)^T : x \in \mathbb{R}\}.
   \]
   ⟹ 相等，成立。

---

3. **\(\mathrm{Col}(A) \subseteq \ker(B^T)\)**

   \[
   \mathrm{Col}(A) = \operatorname{span}\{(1,0,0)^T\},
   \]
   \[
   B^T =
   \begin{bmatrix}
   0 & 1 & 0 \\
   0 & 0 & 1 \\
   0 & 0 & 0
   \end{bmatrix},
   \quad
   \ker(B^T) = \operatorname{span}\{(1,0,0)^T\}.
   \]
   ⟹ 相等，成立。

---

✅ **结论：**
此例中
\[
\mathrm{Col}(B) = \ker(A), \quad
\mathrm{Row}(A) = \mathrm{Col}(B)^\perp, \quad
\mathrm{Col}(A) = \ker(B^T).
\]
说明当维数配合恰当时，所有关系都取等号。