"""
重名问题解决方案说明
Duplicate Names Solution Documentation
"""

# 华语影视演员合作网络 - 重名问题解决方案

## 🎯 问题描述
在华语影视数据中，演员姓名存在重名情况，直接使用 `cast_name` 可能选择错误的演员。

## ✅ 解决方案

### 1. 问题识别
- 原始方法：直接通过 `cast_name` 查找，可能匹配到多个演员
- 改进方法：返回所有匹配结果，由用户选择正确的 `cast_id`

### 2. 新增API方法

#### 数据查询层面
```python
# 获取所有同名演员（返回完整信息供用户选择）
actors = network.get_actors_by_name_with_selection("张伟")
# 返回格式: DataFrame with columns ['cast_name', 'cast_id', 'main_works']

# 直接使用cast_id获取合作数据
collab_data = network.get_cast_collaboration_data_by_id("2010177")
```

#### 网络构建层面
```python
# 方法1: 尝试直接构建（如果有重名会抛出异常并提示）
try:
    network_graph = network.build_actor_network("张伟")
except ValueError as e:
    print(f"存在重名: {e}")

# 方法2: 使用cast_id构建（推荐用于重名情况）
network_graph = network.build_actor_network_by_id("2010177")

# 方法3: 获取合作频率统计
collaborations = network.get_collaboration_frequency_by_id("2010177")
```

### 3. 完整工作流程

```python
from src import CastNetwork

# 1. 初始化
network = CastNetwork()
network.load_data()

# 2. 搜索演员
cast_name = "张伟"
actors = network.get_actors_by_name_with_selection(cast_name)

# 3. 处理结果
if actors.empty:
    print(f"未找到演员: {cast_name}")
elif len(actors) == 1:
    # 只有一个结果，直接使用
    cast_id = actors.iloc[0]['cast_id']
    print(f"找到唯一演员: {cast_id}")
else:
    # 多个结果，用户选择
    print(f"找到 {len(actors)} 个同名演员:")
    for idx, row in actors.iterrows():
        print(f"  {idx+1}. ID: {row['cast_id']} - 代表作: {row['main_works']}")
    
    # 用户选择（这里演示选第一个）
    user_choice = 0  # 用户实际输入
    cast_id = actors.iloc[user_choice]['cast_id']

# 4. 使用选定的cast_id进行分析
network_graph = network.build_actor_network_by_id(cast_id)
collaborations = network.get_collaboration_frequency_by_id(cast_id)
collab_data = network.get_cast_collaboration_data_by_id(cast_id)

# 5. 后续分析...
stats = network.get_network_stats(network_graph)
network.visualize_network(network_graph)
```

### 4. 错误处理机制

#### 智能检测重名
```python
def safe_build_network(network, cast_name):
    """安全的网络构建方法，自动处理重名"""
    try:
        # 先尝试直接构建
        return network.build_actor_network(cast_name)
    except ValueError as e:
        if "存在多个同名演员" in str(e):
            # 处理重名情况
            actors = network.get_actors_by_name_with_selection(cast_name)
            print(f"检测到重名，请选择正确的演员:")
            for idx, row in actors.iterrows():
                print(f"  {idx+1}. {row['cast_id']} - {row['main_works']}")
            return None  # 等待用户选择
        else:
            raise e
```

### 5. 示例代码文件
- `examples/handle_duplicate_names.py` - 完整的重名处理演示
- `examples/basic_usage.py` - 更新了重名处理逻辑
- `quick_start.py` - 包含重名检测演示

### 6. API参考

#### 新增方法
| 方法名 | 用途 | 参数 | 返回值 |
|--------|------|------|--------|
| `get_actors_by_name_with_selection()` | 获取同名演员列表 | cast_name | DataFrame |
| `build_actor_network_by_id()` | 使用ID构建网络 | cast_id | nx.Graph |
| `get_collaboration_frequency_by_id()` | 使用ID获取合作频率 | cast_id, top_n | List[Dict] |
| `get_cast_collaboration_data_by_id()` | 使用ID获取合作数据 | cast_id | DataFrame |

#### 修改的方法
| 方法名 | 变化 | 行为 |
|--------|------|------|
| `build_actor_network()` | 添加重名检测 | 如果有重名，抛出异常并提示使用ID方法 |
| `get_collaboration_frequency()` | 添加重名检测 | 如果有重名，返回空列表并提示 |
| `get_cast_collaboration_data()` | 添加重名检测 | 如果有重名，返回空DataFrame并提示 |

## 🎉 解决方案优势

1. **用户友好**: 清晰地显示所有同名演员及其代表作
2. **数据准确**: 用户可以根据代表作选择正确的演员
3. **向后兼容**: 原有API继续工作，只是增加了重名检测
4. **灵活性**: 提供多种方式处理重名情况
5. **错误提示**: 明确的错误信息指导用户使用正确的方法

## 💡 使用建议

1. **推荐流程**: 先使用 `get_actors_by_name_with_selection()` 检查是否重名
2. **生产环境**: 始终使用 `cast_id` 进行精确操作
3. **用户界面**: 在UI中显示演员的代表作帮助用户选择
4. **数据验证**: 在关键操作前验证 `cast_id` 的有效性

这个解决方案完美地解决了重名问题，确保了数据分析的准确性！
"""
