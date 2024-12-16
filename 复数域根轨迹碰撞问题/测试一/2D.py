import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap

# 定义 K1 的范围，从 0 到 K_max，分成 num_points 个点
K_max = 1000
num_points = 10000
K1_values = np.linspace(0, K_max, num_points)

# 初始化一个列表来存储所有根
# 每个元素是一个长度为3的复数数组，代表一个 K1 下的三个根
all_roots = []

for K1 in K1_values:
    # 定义多项式系数，从高次到低次
    # s^3 + 8s^2 + K1*s + K1 = 0
    coeffs = [1, 8, K1, K1]
    # 计算多项式的根
    roots = np.roots(coeffs)
    all_roots.append(roots)

# 转换为 NumPy 数组，形状为 (num_points, 3)
all_roots = np.array(all_roots)

# 为了跟踪每个根的轨迹，通常需要对根进行排序
# 这里我们按实部排序，这样同一根在不同 K1 下的大致位置会保持一致
sorted_roots = np.sort_complex(all_roots)

# 分别提取三个根的实部和虚部
root1 = sorted_roots[:, 0]
root2 = sorted_roots[:, 1]
root3 = sorted_roots[:, 2]

# 创建绘图
plt.figure(figsize=(10, 8))

# 绘制每个根的轨迹，使用不同颜色
plt.plot(root1.real, root1.imag, label='Root 1', color='red')
plt.plot(root2.real, root2.imag, label='Root 2', color='green')
plt.plot(root3.real, root3.imag, label='Root 3', color='blue')

# 添加起始点和终点
plt.scatter(root1.real[0], root1.imag[0], color='red', marker='o')  # Root1 起点
plt.scatter(root1.real[-1], root1.imag[-1], color='red', marker='x')  # Root1 终点

plt.scatter(root2.real[0], root2.imag[0], color='green', marker='o')  # Root2 起点
plt.scatter(root2.real[-1], root2.imag[-1], color='green', marker='x')  # Root2 终点

plt.scatter(root3.real[0], root3.imag[0], color='blue', marker='o')  # Root3 起点
plt.scatter(root3.real[-1], root3.imag[-1], color='blue', marker='x')  # Root3 终点

# 设置图形标题和标签
plt.title(r'Trajectories of Roots in the Complex Plane for $s^2(s + 8) + K_1(s + 1) = 0$')
plt.xlabel('Real Part')
plt.ylabel('Imaginary Part')

# 添加网格
plt.grid(True)

# 添加图例
plt.legend()

# 设置相同的比例，以便复平面不失真
plt.axis('equal')

# 显示图形
plt.show()
