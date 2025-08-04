"""
网络分析示例
Network Analysis Example
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import CastNetwork
import networkx as nx

def analyze_network_properties(network_graph, actor_name):
    """分析网络属性"""
    print(f"\n=== {actor_name} 网络深度分析 ===")
    
    # 基础统计
    nodes = network_graph.number_of_nodes()
    edges = network_graph.number_of_edges()
    density = nx.density(network_graph)
    
    print(f"网络规模: {nodes} 个节点, {edges} 条边")
    print(f"网络密度: {density:.4f}")
    
    # 度中心性分析
    degree_centrality = nx.degree_centrality(network_graph)
    print(f"\n度中心性最高的演员:")
    sorted_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
    for i, (actor, centrality) in enumerate(sorted_centrality[:5], 1):
        print(f"{i}. {actor}: {centrality:.4f}")
    
    # 中介中心性分析
    if nodes < 500:  # 避免计算时间过长
        print(f"\n计算中介中心性...")
        betweenness_centrality = nx.betweenness_centrality(network_graph)
        sorted_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)
        print(f"中介中心性最高的演员:")
        for i, (actor, centrality) in enumerate(sorted_betweenness[:5], 1):
            print(f"{i}. {actor}: {centrality:.4f}")
    
    # 聚类系数
    clustering = nx.average_clustering(network_graph)
    print(f"\n平均聚类系数: {clustering:.4f}")
    
    # 连通性分析
    if nx.is_connected(network_graph):
        diameter = nx.diameter(network_graph)
        avg_path_length = nx.average_shortest_path_length(network_graph)
        print(f"网络直径: {diameter}")
        print(f"平均路径长度: {avg_path_length:.4f}")
    else:
        components = list(nx.connected_components(network_graph))
        print(f"连通分量数: {len(components)}")
        print(f"最大连通分量大小: {len(max(components, key=len))}")

def find_important_actors(cast_network, network_graph, actor_name):
    """找出重要的演员节点"""
    print(f"\n=== 重要演员分析 ===")
    
    # 度数最高的演员
    degrees = dict(network_graph.degree())
    top_degree_actors = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print("合作最广泛的演员 (按度数):")
    for i, (actor, degree) in enumerate(top_degree_actors, 1):
        print(f"{i}. {actor}: {degree} 个合作伙伴")
    
    # 分析这些重要演员的详细信息
    print(f"\n重要演员详细分析:")
    for actor, degree in top_degree_actors[:3]:
        if actor != actor_name:  # 跳过目标演员自己
            try:
                collab_data = cast_network.get_collaboration_frequency(actor, top_n=5)
                print(f"\n{actor} (度数: {degree}):")
                print("  主要合作伙伴:")
                for collab in collab_data[:3]:
                    print(f"    - {collab['collaborator']}: {collab['frequency']} 次合作")
            except:
                continue

def analyze_collaboration_patterns(cast_network, actor_name):
    """分析合作模式"""
    print(f"\n=== {actor_name} 合作模式分析 ===")
    
    # 获取详细的合作数据
    collaboration_data = cast_network.get_cast_collaboration_data(actor_name)
    
    if collaboration_data.empty:
        print("没有找到合作数据")
        return
    
    # 按年份分析
    yearly_works = collaboration_data.groupby('work_year').agg({
        'work_title': 'nunique',
        'cast_name': 'nunique'
    }).rename(columns={'work_title': '作品数', 'cast_name': '合作演员数'})
    
    print("年度作品和合作情况:")
    print(yearly_works.tail(10))  # 显示最近10年
    
    # 按作品类型分析
    type_analysis = collaboration_data.groupby('work_type').agg({
        'work_title': 'nunique',
        'cast_name': 'nunique'
    }).rename(columns={'work_title': '作品数', 'cast_name': '合作演员数'})
    
    print(f"\n按作品类型分析:")
    print(type_analysis)
    
    # 分析角色类型
    role_analysis = collaboration_data[collaboration_data['cast_name'] == actor_name]['cast_role'].value_counts()
    print(f"\n{actor_name} 的角色类型分布:")
    print(role_analysis)

def main():
    """网络分析主函数"""
    
    # 初始化
    print("初始化网络分析器...")
    cast_network = CastNetwork()
    cast_network.load_data()
    
    # 选择要分析的演员
    actor_name = "周星驰"  # 可以修改为其他演员
    
    print(f"开始分析演员: {actor_name}")
    
    try:
        # 构建网络
        network_graph = cast_network.build_actor_network(actor_name)
        
        # 网络属性分析
        analyze_network_properties(network_graph, actor_name)
        
        # 重要演员分析
        find_important_actors(cast_network, network_graph, actor_name)
        
        # 合作模式分析
        analyze_collaboration_patterns(cast_network, actor_name)
        
        # 可视化度分布
        print(f"\n生成度分布图...")
        cast_network.visualizer.plot_degree_distribution(network_graph)
        
        # 生成交互式网络图
        print(f"生成交互式网络图...")
        interactive_fig = cast_network.visualize_interactive_network(
            network_graph, 
            title=f"{actor_name} 合作网络"
        )
        
        if interactive_fig:
            interactive_fig.write_html(f"examples/{actor_name}_interactive_network.html")
            print(f"交互式网络图已保存到: examples/{actor_name}_interactive_network.html")
        
    except Exception as e:
        print(f"分析过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
