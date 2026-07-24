import numpy as np
import matplotlib.pyplot as plt

# 避免中文乱码；如果系统没有这些字体，可以删除这两行
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
    "Arial Unicode MS",
    "DejaVu Sans"
]
plt.rcParams["axes.unicode_minus"] = False


def f(x):
    """原函数 1 / (1 - x)"""
    return 1.0 / (1.0 - x)


def partial_sum(x, N):
    """
    几何级数的 N 阶部分和：
    S_N(x) = 1 + x + ... + x^N
    """
    result = np.ones_like(x, dtype=float)
    term = np.ones_like(x, dtype=float)

    for _ in range(N):
        term *= x
        result += term

    return result


# 不同的展开阶数
orders = [0, 1, 2, 5, 10, 20]

# 用于左图的范围：包括部分收敛域外区域
x = np.linspace(-1.5, 1.5, 4000)

fig, axes = plt.subplots(
    1, 2,
    figsize=(14, 6),
    constrained_layout=True
)

# ============================================================
# 左图：原函数与不同阶数的部分和
# ============================================================

ax = axes[0]

# 标记收敛域
ax.axvspan(
    -1, 1,
    color="green",
    alpha=0.10,
    label=r"收敛域 $|x|<1$"
)

# 绘制原函数，避开 x=1 的奇点，防止曲线跨越渐近线
mask_left = x < 0.995
mask_right = x > 1.005

ax.plot(
    x[mask_left],
    f(x[mask_left]),
    color="black",
    linewidth=3,
    label=r"$f(x)=\frac{1}{1-x}$"
)

ax.plot(
    x[mask_right],
    f(x[mask_right]),
    color="black",
    linewidth=3
)

# 绘制不同阶数的部分和
colors = plt.cm.plasma(np.linspace(0.05, 0.9, len(orders)))

for N, color in zip(orders, colors):
    y = partial_sum(x, N)

    ax.plot(
        x,
        y,
        color=color,
        linewidth=1.7,
        label=fr"$S_{{{N}}}(x)$"
    )

# 收敛域边界
ax.axvline(-1, color="gray", linestyle="--", linewidth=1.5)
ax.axvline(1, color="red", linestyle="--", linewidth=1.5)

ax.text(
    -0.98, 9.2,
    r"$x=-1$",
    color="gray",
    ha="left",
    va="top"
)

ax.text(
    0.98, 9.2,
    r"$x=1$",
    color="red",
    ha="right",
    va="top"
)

ax.set_xlim(-1.5, 1.5)

# 收敛域外的高阶多项式可能增长很快，因此限制纵轴便于观察
ax.set_ylim(-10, 10)

ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_title("几何级数不同阶数的部分和")
ax.grid(alpha=0.25)
ax.legend(loc="upper left", fontsize=9, ncol=2)


# ============================================================
# 右图：收敛域内的绝对误差
# ============================================================

ax = axes[1]

# 不取 ±1，避免边界行为影响图像
x_inner = np.linspace(-0.99, 0.99, 3000)
y_exact = f(x_inner)

for N, color in zip(orders, colors):
    error = np.abs(partial_sum(x_inner, N) - y_exact)

    # 对数坐标不能显示 0，设置一个很小的下限
    error = np.maximum(error, 1e-16)

    ax.semilogy(
        x_inner,
        error,
        color=color,
        linewidth=1.7,
        label=fr"$N={N}$"
    )

ax.axvspan(
    -1, 1,
    color="green",
    alpha=0.10,
    label=r"$|x|<1$"
)

ax.axvline(-1, color="gray", linestyle="--", linewidth=1.5)
ax.axvline(1, color="red", linestyle="--", linewidth=1.5)

ax.set_xlim(-1.05, 1.05)
ax.set_ylim(1e-16, 1e3)

ax.set_xlabel("$x$")
ax.set_ylabel(r"绝对误差 $|S_N(x)-f(x)|$")
ax.set_title("收敛域内的近似误差（对数坐标）")
ax.grid(alpha=0.25, which="both")
ax.legend(fontsize=9, ncol=2)

plt.suptitle(
    r"$\frac{1}{1-x}"
    r"=\sum_{n=0}^{\infty}x^n,\qquad |x|<1$",
    fontsize=16
)

# 如需保存图片，取消下一行注释
# plt.savefig("geometric_series.png", dpi=200, bbox_inches="tight")

plt.show()