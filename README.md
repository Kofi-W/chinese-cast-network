# 华语影视演员合作网络数据 | Chinese Cast Network

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)

[English](#english) | [中文](#中文)

---

## 中文

本项目提供华语影视演员合作网络数据和相关分析工具，可用于研究华语影视行业的合作关系和网络结构。

### 项目简介

本项目包含：
- 华语影视演员基础数据（85,000+ 演员）
- 演员作品关系数据（590,000+ 记录）
- 作品基础数据（92,000+ 作品）
- 基于NetworkX的合作网络分析工具
- 数据可视化功能

### 数据结构

#### 1. 演员表 (cast_data.csv)
- `cast_id`: 演员唯一标识
- `cast_name`: 演员姓名
- `main_works`: 主要代表作品

#### 2. 演员作品关系表 (cast_works_data.csv)
- `work_id`: 作品唯一标识
- `work_title`: 作品名称
- `cast_id`: 演员ID（对应演员表）
- `cast_name`: 演员姓名
- `cast_role`: 职责类型（演员/导演等）
- `cast_order`: 演员表序号
- `work_year`: 作品年份
- `work_type`: 作品类型（电影/电视剧）
- `work_genres`: 作品类型

#### 3. 作品表 (works_data.csv)
- `work_id`: 作品唯一标识
- `work_title`: 作品名称
- `work_year`: 作品年份
- `work_type`: 作品类型

### 功能特性

- 🎭 演员数据查询和筛选
- 📊 合作网络构建和分析
- 📈 网络可视化
- 🔍 演员合作关系查询
- 📋 统计分析报告生成
- 🎯 **职能筛选分析**（新功能）：支持按演员、导演、编剧等职能类型进行合作网络分析
- 🆔 重名演员处理：通过ID精确识别同名演员

### 安装使用

#### 1. 环境要求
```bash
Python 3.8+
```

#### 2. 安装依赖
```bash
pip install -r requirements.txt
```

#### 3. 基本使用
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

#### 4. 高级功能

##### 4.1 职能筛选分析（新功能）
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

##### 4.2 其他高级功能
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

### 项目结构

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

### 数据统计

- **演员数量**: 85,165 位
- **作品数量**: 92,161 部
- **合作关系**: 596,281 条记录
- **时间跨度**: 1932年 - 2024年
- **作品类型**: 电影、电视剧等

### 示例分析

#### 获取演员合作网络
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

### 贡献指南

欢迎提交Issue和Pull Request！

### 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

### 致谢

感谢所有为华语影视行业数据整理和分析做出贡献的开发者们。

---

## English

This project provides Chinese film and television actor collaboration network data and related analysis tools for studying collaboration relationships and network structures in the Chinese entertainment industry.

### Project Overview

This project includes:
- Chinese film and television actor basic data (85,000+ actors)
- Actor-work relationship data (590,000+ records)
- Work basic data (92,000+ works)
- NetworkX-based collaboration network analysis tools
- Data visualization capabilities

### Data Structure

#### 1. Actor Table (cast_data.csv)
- `cast_id`: Unique actor identifier
- `cast_name`: Actor name
- `main_works`: Main representative works

#### 2. Actor-Work Relationship Table (cast_works_data.csv)
- `work_id`: Unique work identifier
- `work_title`: Work title
- `cast_id`: Actor ID (corresponding to actor table)
- `cast_name`: Actor name
- `cast_role`: Role type (actor/director, etc.)
- `cast_order`: Actor order number
- `work_year`: Work year
- `work_type`: Work type (movie/TV series)
- `work_genres`: Work genres

#### 3. Work Table (works_data.csv)
- `work_id`: Unique work identifier
- `work_title`: Work title
- `work_year`: Work year
- `work_type`: Work type

### Features

- 🎭 Actor data query and filtering
- 📊 Collaboration network construction and analysis
- 📈 Network visualization
- 🔍 Actor collaboration relationship queries
- 📋 Statistical analysis report generation
- 🎯 **Role filtering analysis** (New feature): Support filtering collaboration networks by role types (actor, director, screenwriter, etc.)
- 🆔 Duplicate name handling: Precise identification of actors with same names through ID

### Installation and Usage

#### 1. Requirements
```bash
Python 3.8+
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Basic Usage
```python
from src import CastNetwork

# Initialize network analyzer
network = CastNetwork()

# Load data
network.load_data()

# Build collaboration network for specified actor
actor_network = network.build_actor_network("周星驰")

# Visualize network
network.visualize_network(actor_network)

# Get network statistics
stats = network.get_network_stats(actor_network)
print(stats)
```

#### 4. Advanced Features

##### 4.1 Role Filtering Analysis (New Feature)
```python
# View all available roles in data
roles = network.get_available_roles()
print(f"Data contains {len(roles)} role types")

# Get role statistics
role_stats = network.get_role_statistics()
print(role_stats.head())

# Build network with only actor roles
actor_only_network = network.build_actor_network_by_id(cast_id, include_roles=['演员'])

# Build network with actor and director roles
actor_director_network = network.build_actor_network_by_id(
    cast_id, include_roles=['演员', '导演']
)

# Compare network sizes under different role filters
print(f"Full role network: {full_network.number_of_nodes()} nodes")
print(f"Actor only network: {actor_only_network.number_of_nodes()} nodes")
print(f"Actor+Director network: {actor_director_network.number_of_nodes()} nodes")
```

##### 4.2 Other Advanced Features
```python
# Build multi-actor collaboration network
multi_network = network.build_multi_actor_network(["周星驰", "刘德华", "张学友"])

# Analyze actor collaboration frequency
collaborations = network.get_collaboration_frequency("周星驰")

# Handle duplicate names
actors = network.get_actors_by_name_with_selection("张伟")
if len(actors) > 1:
    # User selection then use ID
    selected_id = actors.iloc[0]['cast_id']
    collaborations = network.get_collaboration_frequency_by_id(selected_id)

# Export network data
network.export_network(actor_network, "zhou_xingchi_network.gexf")
```

### Project Structure

```
chinese-cast-network/
├── data/                          # Data files
│   ├── cast_data.csv             # Actor table (85K+ records)
│   ├── cast_works_data.csv       # Actor-work relationship table (590K+ records)
│   └── works_data.csv            # Work table (92K+ records)
├── src/                          # Source code
│   ├── __init__.py              # Main entry
│   ├── data_loader.py           # Data loading module
│   ├── network_builder.py       # Network building module
│   └── visualizer.py            # Visualization module
├── examples/                     # Example code
│   ├── basic_usage.py           # Basic usage examples
│   ├── network_analysis.py      # Network analysis examples
│   └── visualization_demo.py    # Visualization examples
├── tests/                        # Test files
├── requirements.txt              # Dependencies
├── LICENSE                       # License
└── README.md                     # Project documentation
```

### Data Statistics

- **Number of Actors**: 85,165
- **Number of Works**: 92,161
- **Collaboration Records**: 596,281
- **Time Span**: 1932 - 2024
- **Work Types**: Movies, TV series, etc.

### Example Analysis

#### Getting Actor Collaboration Network
```python
# Using Stephen Chow as example
network = CastNetwork()
network.load_data()

# Build collaboration network
zhou_network = network.build_actor_network("周星驰")
print(f"Stephen Chow's network: {zhou_network.number_of_nodes()} nodes, {zhou_network.number_of_edges()} edges")

# Get top frequent collaborators
top_collaborators = network.get_top_collaborators("周星驰", top_n=10)
```

### Contributing

Issues and Pull Requests are welcome!

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgements

Thanks to all developers who contributed to Chinese film and television industry data organization and analysis.
