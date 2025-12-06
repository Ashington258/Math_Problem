# 叉积简化三维的Gram-Shcmidt正交化过程

## 0 核心论述和原理

1. $\ker(A) = \mathrm{Row}(A)^\perp.$ 
2. 叉积得到垂直矢量


**核心论述**：对于三阶实对称矩阵，必定可以相似对角化，有如下情况
1. 三个不同的特征值(此时特征向量本身相互正交，无需正交化)
2. 二重根(重根的特征子空间为二维平面，需要正交化)
3. 三重根(特征子空间为整个空间，任意正交基底就行)
因此我们重点讨论二重根情形，此时我们为了找到三个相互正交的特征向量我们可以考虑先从重根的特征子空间挑选出任意矢量，然后使用改平面的法向量做叉积，得到该特征子空间的另一个正交矢量，而这个法向量就是该特征子空间对应的行空间的任意向量(正交补)，并且，该向量恰好正是非重根特征值的特征向量，至此完成了整个正交特征向量的求解。

## 1 方法原理

在二重特征值的情形下，为了构造三条互相正交的特征向量，可按如下规范步骤描述：首先取重根 $\lambda$ 对应的特征子空间

$$
E_\lambda=\ker(A-\lambda I)
$$

中的任一非零向量 $v_1$ 。记 $A-\lambda I$ 的行空间为 $\mathrm{Row}(A-\lambda I)$ 。由于

$$
E_\lambda=\ker(A-\lambda I)=\bigl(\mathrm{Row}(A-\lambda I)\bigr)^\perp,
$$

任取 $n\in\mathrm{Row}(A-\lambda I)$ （即任一非零行向量），则 $n$ 与 $E_\lambda$ 中的所有向量正交。对于实对称矩阵 $A$ 而言， $\mathrm{Row}(A-\lambda I)=E_\lambda^\perp$ 恰好等于对应单重特征值 $\mu$ 的特征子空间 $E_\mu$ ，因此该 $n$ 可以取为非重根 $\mu$ 的特征向量。随后令

$$
v_2 := n \times v_1,
$$
故而正交基为:
$$\{v_1,v_2,n\}$$
$v_2$ 非零、与 $v_1$ 正交，且由维数与正交性可知 $v_2\in E_\lambda$ 。归一化后 $\{\,q_1,q_2,q_3\}=\{\;v_1/\|v_1\|,\;v_2/\|v_2\|,\;n/\|n\|\;\}$ 是一组正交特征向量，从而得到正交矩阵 $Q$ 使得

$$
Q^T A Q=\operatorname{diag}(\lambda,\lambda,\mu).
$$


## 2 例子 

$$
A = \begin{pmatrix} 
2 & 2 & -2
\\ 2 & 5 & -4
\\ -2 & -4 & 5
\end{pmatrix} 
$$

### **1. 特征值**

计算特征多项式：
$$
\det(A-\lambda I) = \lambda^3 - 12\lambda^2 + 21\lambda - 10.
$$

因式分解：
$$
(\lambda-10)(\lambda-1)^2=0.
$$

所以特征值为：
$$
\lambda = 10 \ (\text{单重}),\quad \lambda = 1 \ (\text{二重}).
$$



### **2. 特征子空间**

- 对 $\lambda=1$ ：
$$
A-I=\begin{pmatrix}
1&2&-2\\
2&4&-4\\
-2&-4&4
\end{pmatrix},\quad 
E_1 = \ker(A-I) = \mathrm{span}\{(-2,1,0),(2,0,1)\}.
$$

- 对 $\lambda=10$ ：
特征向量 $n=(1,2,-2)$直接对应行向量即可，无需再求 。



### **3. 构造正交基**

1. 取 $v_1=(-2,1,0)\in E_1$ 。
2. $n=(1,2,-2)$ 是 $\lambda=10$ 的特征向量。
3. 作叉积：
 $$
 v_2=n\times v_1=(2,4,5).
 $$
 可知 $v_2\in E_1$ ，且与 $v_1$ 正交。



### **4. 归一化**

$$
q_1=\frac{v_1}{\|v_1\|}=\left(-\tfrac{2}{\sqrt{5}},\tfrac{1}{\sqrt{5}},0\right),
$$

$$
q_2=\frac{v_2}{\|v_2\|}=\left(\tfrac{2}{3\sqrt{5}},\tfrac{4}{3\sqrt{5}},\tfrac{5}{3\sqrt{5}}\right),
$$

$$
q_3=\frac{n}{\|n\|}=\left(\tfrac{1}{3},\tfrac{2}{3},-\tfrac{2}{3}\right).
$$



### **5. 正交相似对角化**

$$
Q=\begin{pmatrix}
-\tfrac{2}{\sqrt{5}} & \tfrac{2}{3\sqrt{5}} & \tfrac{1}{3}\\[6pt]
\tfrac{1}{\sqrt{5}}  & \tfrac{4}{3\sqrt{5}} & \tfrac{2}{3}\\[6pt]
0 & \tfrac{5}{3\sqrt{5}} & -\tfrac{2}{3}
\end{pmatrix},
$$

则
$$
Q^\top A Q = \operatorname{diag}(1,1,10).
$$

