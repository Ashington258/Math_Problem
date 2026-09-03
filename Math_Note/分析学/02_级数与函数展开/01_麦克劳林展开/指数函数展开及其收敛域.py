import mpmath as mp
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


def partial_sum(x, N):
    """
    指数函数麦克劳林级数的 N 阶部分和：
    S_N(x) = 1 + x + x^2 / 2! + ... + x^N / N!
    """
    result = np.ones_like(x, dtype=float)
    term = np.ones_like(x, dtype=float)

    for n in range(1, N + 1):
        term *= x / n
        result += term

    return result


def high_precision_errors(x, max_order):
    """高精度计算固定点处各阶部分和的绝对误差。"""
    x_mp = mp.mpf(x)
    exact = mp.exp(x_mp)
    result = mp.mpf(1)
    term = mp.mpf(1)
    errors = [abs(result - exact)]

    for n in range(1, max_order + 1):
        term *= x_mp / n
        result += term
        errors.append(abs(result - exact))

    return np.array([float(error) for error in errors])


# 左图展示有限区间上的函数逼近；收敛域本身是全体实数
orders = [0, 1, 2, 5, 10, 20, 40]
x = np.linspace(-5, 5, 4000)

fig, axes = plt.subplots(
    1, 2,
    figsize=(14, 6),
    constrained_layout=True
)

# ============================================================
# 左图：原函数与不同阶数的部分和
# ============================================================

ax = axes[0]
ax.plot(
    x,
    np.exp(x),
    color="black",
    linewidth=3,
    label=r"$f(x)=e^x$"
)

colors = plt.cm.plasma(np.linspace(0.05, 0.9, len(orders)))

for N, color in zip(orders, colors):
    ax.plot(
        x,
        partial_sum(x, N),
        color=color,
        linewidth=1.7,
        label=fr"$S_{{{N}}}(x)$"
    )

ax.set_xlim(-5, 5)
ax.set_ylim(-25, 160)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_title(r"有限区间上的逼近（收敛域为 $\mathbb{R}$）")
ax.grid(alpha=0.25)
ax.legend(loc="upper left", fontsize=9, ncol=2)


# ============================================================
# 右图：固定实数点处，误差随阶数的变化
# ============================================================

ax = axes[1]
max_order = 60
order_values = np.arange(max_order + 1)
test_points = [-5.0, -2.0, 1.0, 5.0]
point_colors = ["#2166ac", "#67a9cf", "#ef8a62", "#b2182b"]

# 提高精度，避免浮点舍入误差掩盖趋于 0 的理论趋势
mp.mp.dps = 100

for point, color in zip(test_points, point_colors):
    errors = high_precision_errors(point, max_order)
    errors = np.maximum(errors, 1e-100)

    ax.semilogy(
        order_values,
        errors,
        marker="o",
        markersize=3,
        markevery=4,
        color=color,
        linewidth=1.8,
        label=fr"$x={point:g}$"
    )

# x=-5 的误差在低阶阶段先增加，在 N=4 附近达到峰值
negative_five_errors = high_precision_errors(-5, max_order)
peak_order = int(np.argmax(negative_five_errors))
ax.scatter(
    peak_order,
    negative_five_errors[peak_order],
    color="#2166ac",
    edgecolor="white",
    linewidth=0.8,
    s=55,
    zorder=5
)
ax.annotate(
    "负数点的误差可先增大",
    xy=(peak_order, negative_five_errors[peak_order]),
    xytext=(12, 3e1),
    arrowprops={"arrowstyle": "->", "color": "#2166ac"},
    color="#2166ac"
)

ax.set_xlim(0, max_order)
ax.set_ylim(1e-90, 1e3)
ax.set_xlabel("展开阶数 $N$")
ax.set_ylabel(r"绝对误差 $|S_N(x)-e^x|$")
ax.set_title("每个固定实数点处的误差最终趋于 0")
ax.grid(alpha=0.25, which="both")
ax.legend(fontsize=9)

plt.suptitle(
    r"$e^x=\sum_{n=0}^{\infty}\frac{x^n}{n!},"
    r"\qquad x\in\mathbb{R}$",
    fontsize=16
)

# 如需保存图片，取消下一行注释
# plt.savefig("exponential_series.png", dpi=200, bbox_inches="tight")

plt.show()