# 华语影视演员合作网络数据 Chinese Cast Network

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)

本项目提供华语影视演员合作网络数据和相关分析工具，可用于研究华语影视行业的合作关系和网络结构。

## 项目简介

本项目包含：
- 华语影视演员基础数据（85,000+ 演员）
- 演员作品关系数据（590,000+ 记录）
- 作品基础数据（92,000+ 作品）
- 基于NetworkX的合作网络分析工具
- 数据可视化功能

## 数据结构

### 1. 演员表 (cast_data.csv)
- `cast_id`: 演员唯一标识
- `cast_name`: 演员姓名
- `main_works`: 主要代表作品

### 2. 演员作品关系表 (cast_works_data.csv)
- `work_id`: 作品唯一标识
- `work_title`: 作品名称
- `cast_id`: 演员ID（对应演员表）
- `cast_name`: 演员姓名
- `cast_role`: 职责类型（演员/导演等）
- `cast_order`: 演员表序号
- `work_year`: 作品年份
- `work_type`: 作品类型（电影/电视剧）
- `work_genres`: 作品类型

### 3. 作品表 (works_data.csv)
- `work_id`: 作品唯一标识
- `work_title`: 作品名称
- `work_year`: 作品年份
- `work_type`: 作品类型

## 功能特性

- 🎭 演员数据查询和筛选
- 📊 合作网络构建和分析
- 📈 网络可视化
- 🔍 演员合作关系查询
- 📋 统计分析报告生成
- 🎯 **职能筛选分析**（新功能）：支持按演员、导演、编剧等职能类型进行合作网络分析
- 🆔 重名演员处理：通过ID精确识别同名演员

## 安装使用

### 1. 环境要求
```bash
Python 3.8+
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 基本使用
```python
from src import CastNetwork

# 初始化网络分析器
network = CastNetwork()

# 加载数据
network.load_data()

# 构建指定演员的合作网络
actor_network = network.build_actor_network("周星驰")

# 可视化网络
network.visualize_network(actor_network)

# 获取网络统计信息
stats = network.get_network_stats(actor_network)
print(stats)
```

### 4. 高级功能

#### 4.1 职能筛选分析（新功能）
```python
# 查看数据中所有可用职能
roles = network.get_available_roles()
print(f"数据包含 {len(roles)} 种职能")

# 获取职能统计信息
role_stats = network.get_role_statistics()
print(role_stats.head())

# 构建只包含演员职能的合作网络
actor_only_network = network.build_actor_network_by_id(cast_id, include_roles=['演员'])

# 构建包含演员和导演职能的合作网络
actor_director_network = network.build_actor_network_by_id(
    cast_id, include_roles=['演员', '导演']
)

# 对比不同职能筛选下的网络规模
print(f"全职能网络: {full_network.number_of_nodes()} 节点")
print(f"仅演员网络: {actor_only_network.number_of_nodes()} 节点")
print(f"演员+导演网络: {actor_director_network.number_of_nodes()} 节点")
```

#### 4.2 其他高级功能
```python
# 构建多演员合作网络
multi_network = network.build_multi_actor_network(["周星驰", "刘德华", "张学友"])

# 分析演员合作频率
collaborations = network.get_collaboration_frequency("周星驰")

# 处理重名演员
actors = network.get_actors_by_name_with_selection("张伟")
if len(actors) > 1:
    # 用户选择后使用ID
    selected_id = actors.iloc[0]['cast_id']
    collaborations = network.get_collaboration_frequency_by_id(selected_id)

# 导出网络数据
network.export_network(actor_network, "zhou_xingchi_network.gexf")
```

## 项目结构

```
chinese-cast-network/
├── data/                          # 数据文件
│   ├── cast_data.csv             # 演员表 (85K+ 记录)
│   ├── cast_works_data.csv       # 演员作品关系表 (590K+ 记录)
│   └── works_data.csv            # 作品表 (92K+ 记录)
├── src/                          # 源代码
│   ├── __init__.py              # 主入口
│   ├── data_loader.py           # 数据加载模块
│   ├── network_builder.py       # 网络构建模块
│   └── visualizer.py            # 可视化模块
├── examples/                     # 示例代码
│   ├── basic_usage.py           # 基础使用示例
│   ├── network_analysis.py      # 网络分析示例
│   └── visualization_demo.py    # 可视化示例
├── tests/                        # 测试文件
├── requirements.txt              # 依赖包
├── LICENSE                       # 许可证
└── README.md                     # 项目说明
```

## 数据统计

- **演员数量**: 85,165 位
- **作品数量**: 92,161 部
- **合作关系**: 596,281 条记录
- **时间跨度**: 1932年 - 2024年
- **作品类型**: 电影、电视剧等

## 示例分析

### 获取演员合作网络
```python
# 以周星驰为例
network = CastNetwork()
network.load_data()

# 构建合作网络
zhou_network = network.build_actor_network("周星驰")
print(f"周星驰合作网络: {zhou_network.number_of_nodes()} 个节点, {zhou_network.number_of_edges()} 条边")

# 获取最frequent合作伙伴
top_collaborators = network.get_top_collaborators("周星驰", top_n=10)
```

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

感谢所有为华语影视行业数据整理和分析做出贡献的开发者们。
