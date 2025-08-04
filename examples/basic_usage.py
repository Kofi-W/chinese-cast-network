"""
基础使用示例
Basic Usage Example
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import CastNetwork

def main():
    """基础使用示例"""
    
    # 初始化网络分析器
    print("初始化华语影视演员合作网络分析器...")
    network = CastNetwork()
    
    # 加载数据
    print("加载数据...")
    network.load_data()
    
    # 搜索演员
    print("\n=== 搜索演员示例 ===")
    search_results = network.search_actors("周星驰")
    print("搜索结果:")
    print(search_results[['cast_name', 'cast_id', 'main_works']].head())
    
    # 构建单个演员的合作网络
    print("\n=== 构建单个演员合作网络 ===")
    actor_name = "周星驰"
    
    try:
        print(f"构建 {actor_name} 的合作网络...")
        actor_network = network.build_actor_network(actor_name)
        
        # 获取网络统计信息
        stats = network.get_network_stats(actor_network)
        print(f"\n网络统计信息:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # 获取合作频率统计
        print(f"\n=== {actor_name} 的主要合作伙伴 ===")
        collaborations = network.get_collaboration_frequency(actor_name, top_n=10)
        
        for i, collab in enumerate(collaborations, 1):
            print(f"{i}. {collab['collaborator']}")
            print(f"   合作次数: {collab['frequency']}")
            print(f"   合作作品: {', '.join(collab['works'][:3])}" + 
                  ("..." if len(collab['works']) > 3 else ""))
            print(f"   作品类型: {', '.join(collab['work_types'])}")
            print()
        
        # 可视化网络（静态图）
        print("生成网络可视化图...")
        network.visualize_network(actor_network, 
                                 figsize=(15, 10), 
                                 save_path=f"examples/{actor_name}_network.png")
        
        # 导出网络数据
        print("导出网络数据...")
        network.export_network(actor_network, 
                             f"examples/{actor_name}_network.gexf", 
                             format='gexf')
        
    except ValueError as e:
        print(f"错误: {e}")
    
    # 构建多演员合作网络
    print("\n=== 构建多演员合作网络 ===")
    multi_actors = ["周星驰", "刘德华", "张学友"]
    
    try:
        print(f"构建多演员合作网络: {', '.join(multi_actors)}")
        multi_network = network.build_multi_actor_network(multi_actors)
        
        # 获取网络统计
        multi_stats = network.get_network_stats(multi_network)
        print(f"\n多演员网络统计:")
        for key, value in multi_stats.items():
            print(f"  {key}: {value}")
        
        # 可视化多演员网络
        network.visualize_network(multi_network,
                                 figsize=(16, 12),
                                 save_path="examples/multi_actor_network.png")
        
    except Exception as e:
        print(f"构建多演员网络时出错: {e}")

if __name__ == "__main__":
    main()
