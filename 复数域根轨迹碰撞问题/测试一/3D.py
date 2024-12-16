import numpy as np
import plotly.graph_objects as go

# 定义 K1 的范围，从 0 到 K_max，分成 num_points 个点
K_max = 100
num_points = 10000
K1_values = np.linspace(-100, K_max, num_points)

# 初始化一个列表来存储所有根
all_roots = []

for K1 in K1_values:
    # 定义多项式系数，从高次到低次
    # s^3 + 8s^2 + K1*s + K1 = 0
    coeffs = [1, 9, K1, K1]
    # 计算多项式的根
    roots = np.roots(coeffs)
    all_roots.append(roots)

# 转换为 NumPy 数组，形状为 (num_points, 3)
all_roots = np.array(all_roots)

# 为了跟踪每个根的轨迹，通常需要对根进行排序
# 这里我们按实部排序，这样同一根在不同 K1 下的大致位置会保持一致
sorted_roots = np.sort_complex(all_roots)

# 提取三个根的实部和虚部
real_parts = sorted_roots.real.T  # 转置后每行是一个根的实部轨迹
imag_parts = sorted_roots.imag.T  # 转置后每行是一个根的虚部轨迹

# 创建一个 3D 图
fig = go.Figure()

# 为每个根绘制轨迹
colors = ['red', 'green', 'blue']
labels = ['Root 1', 'Root 2', 'Root 3']

for i in range(3):
    fig.add_trace(go.Scatter3d(
        x=real_parts[i],       # 实部作为 x 轴
        y=K1_values,           # K1 作为 y 轴
        z=imag_parts[i],       # 虚部作为 z 轴
        mode='lines',
        line=dict(color=colors[i], width=4),
        name=labels[i]
    ))

# 设置图形布局
fig.update_layout(
    title="3D Trajectories of Roots in the Complex Plane",
    scene=dict(
        xaxis_title="Real Part",
        yaxis_title="K1",
        zaxis_title="Imaginary Part",
        xaxis=dict(nticks=10),
        zaxis=dict(nticks=10),
        yaxis=dict(nticks=10),
    ),
    legend=dict(x=0.8, y=0.9),
    margin=dict(l=0, r=0, b=0, t=40),
)

# 显示图形
fig.show()
