import numpy as np
import plotly.graph_objects as go


# 定义多项式的系数
def polynomial_coeffs(K1):
    # 计算多项式的系数
    return [1, 10, 33, 40, 16 + K1]


# 设置 K1 的范围
K1_values = np.linspace(-0, 2000, 10000)  # 从 -20 到 20 的 100 个点

# 存储根的实部和虚部
roots_real = []
roots_imag = []

# 计算每个 K1 值的根
for K1 in K1_values:
    coeffs = polynomial_coeffs(K1)
    roots = np.roots(coeffs)  # 计算根
    roots_real.append(roots.real)  # 存储实部
    roots_imag.append(roots.imag)  # 存储虚部

# 转换为数组
roots_real = np.array(roots_real)
roots_imag = np.array(roots_imag)

# 创建根轨迹图
fig = go.Figure()

# 为每个根绘制轨迹
for i in range(4):  # 四次方程有四个根
    fig.add_trace(
        go.Scatter(
            x=roots_real[:, i],
            y=roots_imag[:, i],
            mode="lines+markers",
            name=f"Root {i+1}",
            line=dict(shape="linear"),
        )
    )

# 添加图形的标题和标签
fig.update_layout(
    title="Root Locus of the Polynomial as K1 Varies",
    xaxis_title="Real Part",
    yaxis_title="Imaginary Part",
    showlegend=True,
)

# 显示图形
fig.show()
