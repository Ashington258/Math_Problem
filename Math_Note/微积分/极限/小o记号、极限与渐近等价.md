# 小 $o$ 记号、极限与渐近等价

> 核心速记：固定趋近过程，选定比较尺度，再考察比值。

## 1. 数学本质：选定尺度，再看比值

在同一个趋近过程中，如 $x\to0$、$x\to a$、$x\to\infty$，并假设尺度函数 $f$ 在相应去心邻域内非零：

$$
\boxed{r=o(f)\iff \frac{r}{f}\to0}
$$

等价写成：

$$
\boxed{r=f\varepsilon,\qquad \varepsilon\to0}
$$

这是一切小 \(o\) 运算的核心。

> $r=o(f)$ 表示：相对于尺度 $f$，$r$ 可以忽略。
> 它不一定表示 $r\to0$。

例如 \(x\to\infty\) 时：

$$
x=o(x^2),
$$

尽管 \(x\to\infty\)，但 \(x/x^2\to0\)。

## 2. $o(f)$ 不是一个函数，而是一类函数

两个 \(o(f)\) 通常不同：

$$
o(f)+o(f)
$$

应理解为

$$
f\varepsilon_1+f\varepsilon_2,
\qquad \varepsilon_1,\varepsilon_2\to0.
$$

因此

$$
o(f)+o(f)=f(\varepsilon_1+\varepsilon_2)=o(f).
$$

不能把两个 $o(f)$ 当成同一个量随意相消。严格地说，式子中的等号表示相应的函数类关系；在具体计算中，它表示“等号两边可以分别取满足相应阶数关系的余项”，而不是两个固定函数之间的恒等式。

本文还会使用大 $O$ 记号。若存在常数 $C>0$，使得在相应趋近过程中最终有

$$
|g(x)|\le C|f(x)|,
$$

则记作

$$
g=O(f).
$$

它表示 $g$ 的量级不超过 $f$，但不要求 $g/f\to0$。

## 3. 必须先明确趋近过程

同一式子在不同趋近过程中，结果可能不同。

### \(x\to0\)

$$
x^2=o(x),
$$

所以

$$
\boxed{o(x)+o(x^2)=o(x)}.
$$

### \(x\to\infty\)

$$
x=o(x^2),
$$

所以

$$
\boxed{o(x)+o(x^2)=o(x^2)}.
$$

规则没变，变的是尺度大小。

若 \(x\to a\)，通常令

$$
h=x-a\to0
$$

并使用 \(h,h^2,h^3\) 比较阶数。

## 4. 必须掌握的运算规则

以下均针对同一个趋近过程。

### 4.1 加法：保留较大的尺度

若

$$
g=O(f),
$$

则

$$
\boxed{o(f)+o(g)=o(f)}.
$$

特别地，若 \(g=o(f)\)，也成立。

判断谁更大，只需计算比值：

$$
\frac gf\to0\quad\Longrightarrow\quad g=o(f).
$$

### 4.2 乘法：尺度相乘

$$
\boxed{o(f)o(g)=o(fg)}
$$

因为

$$
(f\varepsilon_1)(g\varepsilon_2)
=fg(\varepsilon_1\varepsilon_2),
\qquad
\varepsilon_1\varepsilon_2\to0.
$$

例如：

$$
\boxed{o(x)o(x^2)=o(x^3)}.
$$

类似地：

$$
\boxed{f\,o(g)=o(fg)},
$$

$$
\boxed{O(f)o(g)=o(fg)}.
$$

### 4.3 除以明确函数：可以

若 $g$ 在相应去心邻域内非零，则

$$
\boxed{\frac{o(f)}{g}=o\left(\frac fg\right)}.
$$

例如：

$$
\frac{o(x^3)}x=o(x^2).
$$

### 4.4 两个小 $o$ 相除：一般不能确定

$$
\boxed{\frac{o(f)}{o(g)}\text{ 通常无法化简}}
$$

因为

$$
\frac{f\varepsilon_1}{g\varepsilon_2}
=
\frac fg\frac{\varepsilon_1}{\varepsilon_2},
$$

而两个趋零量的比值

$$
\frac{\varepsilon_1}{\varepsilon_2}
$$

可能趋于 \(0\)、常数、无穷大或振荡。

因此：

$$
\boxed{\frac{o(3x)}{o(x^2)}\text{ 无确定结果}}.
$$

这与极限中的 \(0/0\) 不定式完全相同。

## 5. 小 $o$、极限与渐近等价的统一关系

### 5.1 极限为常数

以下假设 $g$ 在相应去心邻域内非零。

$$
\boxed{\frac fg\to A\iff f=Ag+o(g)}
$$

特别地：

$$
\frac fg\to0\iff f=o(g),
$$

$$
\frac fg\to1\iff f\sim g.
$$

### 5.2 渐近等价

以下仍假设有关比值在相应去心邻域内有定义。

$$
\boxed{f\sim g\iff \frac fg\to1}
$$

等价于：

$$
\boxed{f=g(1+o(1))}
$$

以及

$$
\boxed{f-g=o(g)}.
$$

因此，渐近等价表示：

> 两个函数的差，相对于主项可以忽略。

## 6. 等价替换的正确原则

若

$$
f\sim g,
$$

若有关比值均有定义，则在乘除法中通常可以替换：

$$
fh\sim gh,\qquad \frac fh\sim\frac gh.
$$

但在加减法中不能无条件替换，因为主项可能抵消。

例如：

$$
\sin x\sim x,
$$

但不能在

$$
\sin x-x
$$

中直接把 \(\sin x\) 替换为 \(x\)。必须用更高阶展开：

$$
\sin x=x-\frac{x^3}{6}+o(x^3),
$$

所以

$$
\sin x-x=-\frac{x^3}{6}+o(x^3).
$$

记忆原则：

$$
\boxed{\text{乘除可优先用等价；加减先检查主项是否抵消。}}
$$

## 7. 极限运算为什么对应这些规则？

若

$$
\varepsilon_1\to0,\qquad \varepsilon_2\to0,
$$

那么：

$$
\varepsilon_1+\varepsilon_2\to0,
$$

$$
\varepsilon_1\varepsilon_2\to0.
$$

但

$$
\frac{\varepsilon_1}{\varepsilon_2}
$$

无法确定。

因此：

$$
\boxed{o+o\text{ 通常可合并}}
$$

$$
\boxed{o\cdot o\text{ 可相乘}}
$$

$$
\boxed{o/o\text{ 通常不可化简}}
$$

## 8. 防错运算流程

遇到任何小 \(o\) 运算，依次做四步。

### 第一步：写清趋近过程

例如：

$$
x\to0,\qquad x\to\infty,\qquad x\to a.
$$

### 第二步：比较尺度

计算

$$
\frac fg.
$$

- \(f/g\to0\)：\(f=o(g)\)；
- \(f/g\to c\neq0\)：\(f,g\) 同阶；
- \(g/f\to0\)：\(g=o(f)\)。

### 第三步：将小 $o$ 展开

$$
o(f)=f\varepsilon,\qquad \varepsilon\to0.
$$

不同的 \(o\) 使用不同的 \(\varepsilon\)。

### 第四步：做普通代数并检查极限

若结果能写成

$$
F(x)\eta(x),\qquad \eta(x)\to0,
$$

则结果就是

$$
o(F).
$$

## 9. 最常见错误

### 错误一：忘记趋近过程

$$
o(x)+o(x^2)
$$

不写 \(x\to0\) 或 \(x\to\infty\)，结果不唯一。

### 错误二：把小 \(o\) 当成固定量

一般只能说：

$$
o(f)-o(f)=o(f),
$$

不能直接说等于 \(0\)。

### 错误三：认为 \(o(f)\) 本身一定趋零

小 \(o\) 表示相对尺度趋零，不是函数本身必然趋零。

### 错误四：直接计算 \(o(f)/o(g)\)

两个未知趋零因子的比值无法确定。

### 错误五：在加减法中随意使用等价替换

主项可能相消，必须使用更高阶展开。

### 错误六：把差趋零当成渐近等价

$$
f-g\to0
$$

不一定推出 \(f\sim g\)。渐近等价要求：

$$
\frac{f-g}{g}\to0.
$$

## 10. 一页公式总结

$$
\boxed{r=o(f)\iff \frac rf\to0\iff r=f\varepsilon,\ \varepsilon\to0}
$$

$$
\boxed{\frac fg\to A\iff f=Ag+o(g)}
$$

$$
\boxed{f\sim g\iff f=g(1+o(1))\iff f-g=o(g)}
$$

$$
\boxed{o(f)+o(f)=o(f)}
$$

$$
\boxed{g=O(f)\Longrightarrow o(f)+o(g)=o(f)}
$$

$$
\boxed{o(f)o(g)=o(fg)}
$$

$$
\boxed{f\,o(g)=o(fg)}
$$

$$
\boxed{\frac{o(f)}g=o\left(\frac fg\right)}
$$

$$
\boxed{\frac{o(f)}{o(g)}\text{ 一般无法确定}}
$$

最终只需牢记一句话：

$$
\boxed{\text{固定趋近过程，选择比较尺度，除以尺度，再计算极限。}}
$$

若对任何小 \(o\) 公式没有把握，就立即使用：

$$
\boxed{o(f)=f\varepsilon,\qquad \varepsilon\to0}
$$

将其还原成普通极限运算。这是最可靠、最不容易出错的方法。
