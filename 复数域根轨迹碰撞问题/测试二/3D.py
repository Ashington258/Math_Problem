import numpy as np
import plotly.graph_objects as go


# 定义多项式的系数
def polynomial_coeffs(K1):
    return [1, 10, 33, 40, 16 + K1]


# 设置 K1 的范围
K1_values = np.linspace(-20, 20, 10000)  # 从 -20 到 20 的 100 个点

# 存储根的实部和虚部
roots_real = []
roots_imag = []
roots_K1 = []

# 计算每个 K1 值的根
for K1 in K1_values:
    coeffs = polynomial_coeffs(K1)
    roots = np.roots(coeffs)  # 计算根
    roots_real.append(roots.real)  # 存储实部
    roots_imag.append(roots.imag)  # 存储虚部
    roots_K1.append(np.full(roots.shape, K1))  # 存储 K1 值

# 转换为数组
roots_real = np.array(roots_real)
roots_imag = np.array(roots_imag)
roots_K1 = np.array(roots_K1)

# 创建 3D 根轨迹图
fig = go.Figure()

# 为每个根绘制轨迹
for i in range(4):  # 四次方程有四个根
    fig.add_trace(
        go.Scatter3d(
            x=roots_real[:, i],
            y=roots_imag[:, i],
            z=roots_K1[:, i],
            mode="lines+markers",
            name=f"Root {i+1}",
            line=dict(width=2),  # 设置线宽
        )
    )

# 添加图形的标题和标签
fig.update_layout(
    title="3D Root Locus of the Polynomial as K1 Varies",
    scene=dict(xaxis_title="Real Part", yaxis_title="Imaginary Part", zaxis_title="K1"),
    showlegend=True,
)

# 显示图形
fig.show()
