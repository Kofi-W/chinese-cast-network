"""
快速开始脚本
Quick Start Script
"""

from src import CastNetwork

def quick_demo():
    """快速演示华语影视演员合作网络分析功能"""
    
    print("🎬 华语影视演员合作网络数据分析工具")
    print("=" * 50)
    
    # 初始化
    print("📊 正在初始化分析器...")
    network = CastNetwork()
    
    # 加载数据
    print("📁 正在加载数据...")
    try:
        network.load_data()
        print("✅ 数据加载成功!")
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return
    
    # 演员搜索演示
    print("\n🔍 演员搜索演示")
    print("-" * 30)
    search_keyword = "周星驰"
    results = network.search_actors(search_keyword, limit=5)
    
    if not results.empty:
        print(f"搜索关键词: {search_keyword}")
        for idx, row in results.iterrows():
            print(f"  • {row['cast_name']} (ID: {row['cast_id']})")
            print(f"    代表作: {row['main_works']}")
    else:
        print(f"未找到包含 '{search_keyword}' 的演员")
    
    # 重名处理演示
    print(f"\n🎭 重名处理演示")
    print("-" * 30)
    
    # 选择演员进行演示
    if not results.empty:
        demo_actor = results.iloc[0]['cast_name']
    else:
        demo_actor = network.cast_data_df.iloc[0]['cast_name']
    
    print(f"演示演员: {demo_actor}")
    
    # 检查是否存在重名
    all_matches = network.get_actors_by_name_with_selection(demo_actor)
    
    if len(all_matches) > 1:
        print(f"⚠️  发现 {len(all_matches)} 个同名演员:")
        for idx, row in all_matches.iterrows():
            print(f"  {idx + 1}. ID: {row['cast_id']} - 代表作: {row['main_works']}")
        
        # 使用第一个演员的ID进行演示
        selected_cast_id = all_matches.iloc[0]['cast_id']
        print(f"🤖 自动选择第一个演员 (ID: {selected_cast_id}) 进行演示")
        
        # 使用ID构建网络
        actor_network = network.build_actor_network_by_id(selected_cast_id)
        
        # 获取合作频率统计
        collaborations = network.get_collaboration_frequency_by_id(selected_cast_id, top_n=5)
        
    else:
        print(f"✅ {demo_actor} 无重名，直接构建网络")
        actor_network = network.build_actor_network(demo_actor)
        collaborations = network.get_collaboration_frequency(demo_actor, top_n=5)
    
    # 网络构建演示
    print(f"\n🕸️  网络构建演示")
    print("-" * 30)
    
    try:
        # 显示网络统计
        stats = network.get_network_stats(actor_network)
        print(f"✅ 网络构建成功!")
        print(f"  节点数 (演员数): {stats['nodes']}")
        print(f"  边数 (合作关系): {stats['edges']}")
        print(f"  网络密度: {stats['density']:.4f}")
        print(f"  平均聚类系数: {stats.get('average_clustering', 'N/A'):.4f}")
        
        # 显示主要合作伙伴
        print(f"\n👥 主要合作伙伴:")
        
        for i, collab in enumerate(collaborations, 1):
            print(f"  {i}. {collab['collaborator']} - 合作 {collab['frequency']} 次")
            if collab['works']:
                works_sample = collab['works'][:2]  # 显示前2部作品
                works_str = ', '.join(works_sample)
                if len(collab['works']) > 2:
                    works_str += f" 等{len(collab['works'])}部作品"
                print(f"     作品: {works_str}")
        
        # 可视化网络
        print(f"\n📈 生成网络可视化...")
        try:
            network.visualize_network(actor_network, 
                                     figsize=(12, 8),
                                     save_path=f"{demo_actor}_network_demo.png")
            print(f"✅ 网络图已保存为: {demo_actor}_network_demo.png")
        except Exception as e:
            print(f"⚠️  可视化生成失败 (可能是缺少matplotlib): {e}")
        
        # 导出网络数据
        print(f"\n💾 导出网络数据...")
        try:
            network.export_network(actor_network, 
                                 f"{demo_actor}_network_demo.gexf", 
                                 format='gexf')
            print(f"✅ 网络数据已导出为: {demo_actor}_network_demo.gexf")
        except Exception as e:
            print(f"⚠️  数据导出失败: {e}")
            
    except Exception as e:
        print(f"❌ 网络构建失败: {e}")
    
    # 多演员网络演示
    print(f"\n🎭 多演员网络演示")
    print("-" * 30)
    
    # 选择几个知名演员
    multi_actors = ["周星驰", "刘德华", "张学友"]
    available_actors = []
    
    # 检查哪些演员在数据中存在
    for actor in multi_actors:
        if not network.search_actors(actor, limit=1).empty:
            available_actors.append(actor)
    
    if len(available_actors) >= 2:
        print(f"构建多演员网络: {', '.join(available_actors)}")
        try:
            multi_network = network.build_multi_actor_network(available_actors)
            multi_stats = network.get_network_stats(multi_network)
            
            print(f"✅ 多演员网络构建成功!")
            print(f"  节点数: {multi_stats['nodes']}")
            print(f"  边数: {multi_stats['edges']}")
            print(f"  连通分量数: {multi_stats.get('connected_components', 1)}")
            
        except Exception as e:
            print(f"❌ 多演员网络构建失败: {e}")
    else:
        print("⚠️  数据中可用的知名演员不足，跳过多演员演示")
    
    print(f"\n🎉 快速演示完成!")
    print("=" * 50)
    print("💡 更多功能请查看 examples/ 目录中的详细示例")
    print("📖 完整文档请参考 README.md")

if __name__ == "__main__":
    quick_demo()
