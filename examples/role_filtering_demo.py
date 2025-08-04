#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
角色筛选功能演示
演示如何使用职能筛选功能来分析特定职能的合作网络
"""

import os
import sys
import pandas as pd

# 添加项目根目录到路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src import CastNetwork

def main():
    # 初始化分析工具
    network = CastNetwork()
    
    # 加载数据
    data_dir = os.path.join(project_root, 'data')
    network.load_data(data_dir)
    
    print("=" * 60)
    print("角色筛选功能演示")
    print("=" * 60)
    
    # 1. 查看所有可用的职能
    print("\n1. 查看所有可用的职能：")
    available_roles = network.get_available_roles()
    print(f"数据中包含 {len(available_roles)} 种职能：")
    for i, role in enumerate(available_roles[:20], 1):  # 显示前20个
        print(f"  {i:2d}. {role}")
    if len(available_roles) > 20:
        print(f"  ... 以及其他 {len(available_roles) - 20} 种职能")
    
    # 2. 查看职能统计信息
    print("\n2. 职能统计信息（前10位）：")
    role_stats = network.get_role_statistics()
    print(role_stats.head(10))
    
    # 3. 演示重名处理和职能筛选
    print("\n" + "=" * 60)
    print("演示：处理重名演员和职能筛选")
    print("=" * 60)
    
    # 搜索一个常见的名字（可能有重名）
    test_name = "张伟"  # 这是一个很常见的名字，可能有重名
    print(f"\n搜索演员：{test_name}")
    
    # 获取同名演员列表
    actors = network.get_actors_by_name_with_selection(test_name)
    
    if actors.empty:
        print(f"未找到名为 {test_name} 的演员，尝试其他名字...")
        # 从数据中随机选择一个演员
        sample_actors = network.search_actors("", limit=5)
        if not sample_actors.empty:
            test_actor = sample_actors.iloc[0]
            cast_id = test_actor['cast_id']
            cast_name = test_actor['cast_name']
            print(f"使用示例演员：{cast_name} (ID: {cast_id})")
        else:
            print("无法找到示例演员，退出演示")
            return
    else:
        print(f"找到 {len(actors)} 个同名演员：")
        for idx, actor in actors.iterrows():
            print(f"  ID: {actor['cast_id']}, 姓名: {actor['cast_name']}, 代表作: {actor['main_works']}")
        
        # 选择第一个演员进行演示
        cast_id = actors.iloc[0]['cast_id']
        cast_name = actors.iloc[0]['cast_name']
        print(f"\n选择第一个演员进行演示：{cast_name} (ID: {cast_id})")
    
    # 4. 构建不同职能的合作网络
    print(f"\n4. 为演员 {cast_name} 构建不同职能的合作网络：")
    
    # 4.1 所有职能的网络
    print(f"\n4.1 构建包含所有职能的合作网络：")
    full_network = network.build_actor_network_by_id(cast_id)
    print(f"全职能网络：{full_network.number_of_nodes()} 个节点，{full_network.number_of_edges()} 条边")
    
    # 4.2 只包含演员职能的网络
    print(f"\n4.2 构建只包含'演员'职能的合作网络：")
    actor_network = network.build_actor_network_by_id(cast_id, include_roles=['演员'])
    print(f"演员职能网络：{actor_network.number_of_nodes()} 个节点，{actor_network.number_of_edges()} 条边")
    
    # 4.3 包含演员和导演职能的网络
    print(f"\n4.3 构建包含'演员'和'导演'职能的合作网络：")
    actor_director_network = network.build_actor_network_by_id(cast_id, include_roles=['演员', '导演'])
    print(f"演员+导演职能网络：{actor_director_network.number_of_nodes()} 个节点，{actor_director_network.number_of_edges()} 条边")
    
    # 5. 分析网络差异
    print(f"\n5. 网络规模对比：")
    print(f"  所有职能:    {full_network.number_of_nodes():4d} 节点, {full_network.number_of_edges():4d} 边")
    print(f"  仅演员:      {actor_network.number_of_nodes():4d} 节点, {actor_network.number_of_edges():4d} 边")
    print(f"  演员+导演:   {actor_director_network.number_of_nodes():4d} 节点, {actor_director_network.number_of_edges():4d} 边")
    
    # 6. 展示职能筛选对合作关系的影响
    if full_network.number_of_nodes() > 1:
        print(f"\n6. 职能筛选对合作关系的影响：")
        
        # 获取目标演员的邻居（合作者）
        neighbors_all = list(full_network.neighbors(cast_name))
        if actor_network.number_of_nodes() > 1:
            neighbors_actor = list(actor_network.neighbors(cast_name))
        else:
            neighbors_actor = []
        
        print(f"  所有职能合作者数量: {len(neighbors_all)}")
        print(f"  仅演员职能合作者数量: {len(neighbors_actor)}")
        
        if neighbors_all and neighbors_actor:
            # 展示前5个合作者的职能信息
            print(f"\n  前5位合作者的职能差异：")
            for i, neighbor in enumerate(neighbors_all[:5], 1):
                if full_network.has_node(neighbor):
                    edge_data = full_network[cast_name][neighbor]
                    collaborator_roles = edge_data.get('collaborator_roles', ['未知'])
                    in_actor_network = neighbor in neighbors_actor
                    print(f"    {i}. {neighbor} - 职能: {', '.join(collaborator_roles)} - 在演员网络中: {'是' if in_actor_network else '否'}")
    
    print(f"\n" + "=" * 60)
    print("角色筛选功能演示完成！")
    print("=" * 60)
    print("\n使用建议：")
    print("1. 使用 get_available_roles() 查看数据中所有可用的职能")
    print("2. 使用 get_role_statistics() 了解各职能的分布情况")
    print("3. 在构建网络时使用 include_roles 参数筛选特定职能")
    print("4. 对比不同职能筛选条件下的网络差异")

if __name__ == "__main__":
    main()
