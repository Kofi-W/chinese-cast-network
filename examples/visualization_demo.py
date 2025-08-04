"""
可视化示例
Visualization Demo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import CastNetwork
import matplotlib.pyplot as plt

def demo_basic_visualization(cast_network, actor_name):
    """基础可视化示例"""
    print(f"=== 基础可视化: {actor_name} ===")
    
    # 构建网络
    network = cast_network.build_actor_network(actor_name)
    
    # 不同布局的可视化
    layouts = ['spring', 'circular', 'kamada_kawai']
    
    for layout in layouts:
        print(f"生成 {layout} 布局的网络图...")
        cast_network.visualize_network(
            network,
            figsize=(12, 8),
            layout=layout,
            save_path=f"examples/{actor_name}_{layout}_layout.png"
        )

def demo_collaboration_visualization(cast_network, actor_name):
    """合作关系可视化示例"""
    print(f"=== 合作关系可视化: {actor_name} ===")
    
    # 获取合作频率数据
    collaborations = cast_network.get_collaboration_frequency(actor_name, top_n=20)
    
    if collaborations:
        # 合作频率热力图
        print("生成合作频率热力图...")
        cast_network.visualizer.plot_collaboration_heatmap(collaborations)
        
        # 时间线分析
        print("生成合作时间线分析...")
        cast_network.visualizer.plot_timeline_analysis(collaborations)

def demo_network_comparison(cast_network):
    """网络对比可视化示例"""
    print("=== 多演员网络对比 ===")
    
    actors = ["周星驰", "刘德华", "张学友", "梁朝伟"]
    networks = {}
    
    # 构建各个演员的网络
    for actor in actors:
        try:
            print(f"构建 {actor} 的网络...")
            networks[actor] = cast_network.build_actor_network(actor)
        except Exception as e:
            print(f"跳过 {actor}: {e}")
    
    # 比较网络规模
    print("\n网络规模对比:")
    sizes = []
    names = []
    
    for actor, network in networks.items():
        nodes = network.number_of_nodes()
        edges = network.number_of_edges()
        print(f"{actor}: {nodes} 节点, {edges} 边")
        sizes.append((nodes, edges))
        names.append(actor)
    
    # 绘制对比图
    if sizes:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 节点数对比
        nodes_count = [s[0] for s in sizes]
        ax1.bar(names, nodes_count, color='skyblue', alpha=0.7)
        ax1.set_title('演员合作网络节点数对比')
        ax1.set_ylabel('节点数')
        ax1.tick_params(axis='x', rotation=45)
        
        # 边数对比
        edges_count = [s[1] for s in sizes]
        ax2.bar(names, edges_count, color='lightcoral', alpha=0.7)
        ax2.set_title('演员合作网络边数对比')
        ax2.set_ylabel('边数')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('examples/network_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()

def demo_interactive_features(cast_network, actor_name):
    """交互式功能示例"""
    print(f"=== 交互式功能: {actor_name} ===")
    
    # 构建网络
    network = cast_network.build_actor_network(actor_name)
    
    # 创建交互式图表
    print("创建交互式网络图...")
    interactive_fig = cast_network.visualize_interactive_network(
        network, 
        title=f"{actor_name} 合作网络 - 交互式版本"
    )
    
    if interactive_fig:
        # 保存为HTML文件
        html_path = f"examples/{actor_name}_interactive.html"
        interactive_fig.write_html(html_path)
        print(f"交互式图表已保存: {html_path}")
        
        # 也可以显示图表（在Jupyter notebook中）
        # interactive_fig.show()

def demo_data_export(cast_network, actor_name):
    """数据导出示例"""
    print(f"=== 数据导出: {actor_name} ===")
    
    # 构建网络
    network = cast_network.build_actor_network(actor_name)
    
    # 导出不同格式
    formats = ['gexf', 'gml', 'graphml', 'json']
    
    for fmt in formats:
        try:
            filename = f"examples/{actor_name}_network.{fmt}"
            cast_network.export_network(network, filename, format=fmt)
            print(f"已导出 {fmt.upper()} 格式: {filename}")
        except Exception as e:
            print(f"导出 {fmt} 格式失败: {e}")

def main():
    """可视化示例主函数"""
    
    # 初始化
    print("初始化网络分析器...")
    cast_network = CastNetwork()
    cast_network.load_data()
    
    # 选择演员
    actor_name = "周星驰"
    
    try:
        # 基础可视化
        demo_basic_visualization(cast_network, actor_name)
        
        # 合作关系可视化
        demo_collaboration_visualization(cast_network, actor_name)
        
        # 网络对比
        demo_network_comparison(cast_network)
        
        # 交互式功能
        demo_interactive_features(cast_network, actor_name)
        
        # 数据导出
        demo_data_export(cast_network, actor_name)
        
        print("\n所有可视化示例已完成！")
        print("生成的文件保存在 examples/ 目录中")
        
    except Exception as e:
        print(f"示例运行中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
