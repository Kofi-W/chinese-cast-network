"""
处理重名演员示例
Handle Duplicate Names Example
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import CastNetwork
import pandas as pd

def demonstrate_duplicate_name_handling():
    """演示如何处理重名演员的情况"""
    
    print("🎭 华语影视演员合作网络 - 重名处理演示")
    print("=" * 50)
    
    # 初始化
    network = CastNetwork()
    network.load_data()
    
    # 搜索可能存在重名的演员
    print("\n🔍 搜索演员示例")
    print("-" * 30)
    
    # 尝试搜索一些常见姓名，这些可能存在重名
    test_names = ["张伟", "王伟", "李伟", "刘伟", "陈伟"]
    
    duplicate_found = False
    test_actor = None
    
    for name in test_names:
        actors = network.get_actors_by_name_with_selection(name)
        if len(actors) > 1:
            print(f"\n✅ 找到重名演员: {name}")
            print(f"共有 {len(actors)} 个同名演员:")
            for idx, row in actors.iterrows():
                print(f"  {idx + 1}. ID: {row['cast_id']} - 代表作: {row['main_works']}")
            
            test_actor = name
            duplicate_found = True
            break
        elif len(actors) == 1:
            print(f"演员 {name}: 1个结果")
        else:
            print(f"演员 {name}: 未找到")
    
    if not duplicate_found:
        print("⚠️  未找到重名演员，使用数据中的第一个演员进行演示...")
        # 随机选择一个演员
        sample_actor = network.cast_data_df.iloc[0]['cast_name']
        actors = network.get_actors_by_name_with_selection(sample_actor)
        test_actor = sample_actor
    else:
        actors = network.get_actors_by_name_with_selection(test_actor)
    
    print(f"\n🎯 演示演员: {test_actor}")
    print("-" * 30)
    
    # 场景1：直接使用演员姓名（可能失败）
    print(f"\n📍 场景1: 直接使用演员姓名构建网络")
    try:
        direct_network = network.build_actor_network(test_actor)
        print(f"✅ 直接构建成功")
        print(f"   网络规模: {direct_network.number_of_nodes()} 节点, {direct_network.number_of_edges()} 边")
    except ValueError as e:
        print(f"❌ 直接构建失败: {e}")
        
        # 场景2：处理重名情况
        print(f"\n📍 场景2: 使用演员ID构建网络")
        
        if len(actors) > 1:
            print("请选择具体的演员:")
            for idx, row in actors.iterrows():
                print(f"  选项 {idx + 1}: ID={row['cast_id']}, 代表作={row['main_works']}")
            
            # 自动选择第一个进行演示
            selected_cast_id = actors.iloc[0]['cast_id']
            selected_main_works = actors.iloc[0]['main_works']
            
            print(f"\n🤖 自动选择第一个演员进行演示:")
            print(f"   演员ID: {selected_cast_id}")
            print(f"   代表作: {selected_main_works}")
            
            try:
                # 使用cast_id构建网络
                id_network = network.build_actor_network_by_id(selected_cast_id)
                print(f"✅ 使用ID构建成功")
                print(f"   网络规模: {id_network.number_of_nodes()} 节点, {id_network.number_of_edges()} 边")
                
                # 获取合作频率统计
                print(f"\n📊 合作频率统计:")
                collaborations = network.get_collaboration_frequency_by_id(selected_cast_id, top_n=5)
                
                if collaborations:
                    for i, collab in enumerate(collaborations, 1):
                        print(f"  {i}. {collab['collaborator']}: {collab['frequency']} 次合作")
                        if collab['works']:
                            works_sample = collab['works'][:2]
                            print(f"     代表作品: {', '.join(works_sample)}")
                else:
                    print("  该演员暂无合作数据")
                
                # 获取合作数据
                print(f"\n📋 合作数据统计:")
                collab_data = network.get_cast_collaboration_data_by_id(selected_cast_id)
                
                if not collab_data.empty:
                    unique_works = collab_data['work_title'].nunique()
                    unique_collaborators = collab_data[collab_data['cast_id'] != selected_cast_id]['cast_name'].nunique()
                    
                    print(f"   参演作品数: {unique_works}")
                    print(f"   合作演员数: {unique_collaborators}")
                    print(f"   总合作记录数: {len(collab_data)}")
                    
                    # 按年份统计
                    yearly_stats = collab_data.groupby('work_year').agg({
                        'work_title': 'nunique',
                        'cast_name': 'nunique'
                    }).tail(5)  # 最近5年
                    
                    if not yearly_stats.empty:
                        print(f"\n   最近年份作品统计:")
                        for year, stats in yearly_stats.iterrows():
                            if not pd.isna(year):
                                print(f"     {int(year)}年: {stats['work_title']}部作品, {stats['cast_name']}位合作演员")
                
                # 可视化网络
                print(f"\n📈 生成网络可视化...")
                try:
                    network.visualize_network(id_network, 
                                             figsize=(12, 8),
                                             save_path=f"{test_actor}_{selected_cast_id}_network.png")
                    print(f"✅ 网络图已保存")
                except Exception as e:
                    print(f"⚠️  可视化失败: {e}")
                
            except Exception as e:
                print(f"❌ 使用ID构建网络失败: {e}")

def interactive_actor_selection():
    """交互式演员选择演示"""
    
    print(f"\n🎮 交互式演员选择演示")
    print("=" * 50)
    
    network = CastNetwork()
    network.load_data()
    
    def process_actor_selection(actor_name):
        """处理演员选择的完整流程"""
        print(f"\n🔍 搜索演员: {actor_name}")
        
        # 1. 获取所有同名演员
        actors = network.get_actors_by_name_with_selection(actor_name)
        
        if actors.empty:
            print(f"❌ 未找到演员: {actor_name}")
            return None
        
        # 2. 如果只有一个结果，直接使用
        if len(actors) == 1:
            cast_id = actors.iloc[0]['cast_id']
            main_works = actors.iloc[0]['main_works']
            print(f"✅ 找到唯一演员: ID={cast_id}, 代表作={main_works}")
            return cast_id
        
        # 3. 如果有多个结果，显示选项
        print(f"找到 {len(actors)} 个同名演员，请选择:")
        for idx, row in actors.iterrows():
            print(f"  {idx + 1}. ID: {row['cast_id']}")
            print(f"     代表作: {row['main_works']}")
            print()
        
        # 在实际使用中，这里应该接收用户输入
        # 这里我们自动选择第一个
        selected_cast_id = actors.iloc[0]['cast_id']
        print(f"🤖 自动选择: {selected_cast_id}")
        
        return selected_cast_id
    
    # 演示几个演员
    demo_actors = ["周星驰", "刘德华", "张学友"]
    
    for actor_name in demo_actors:
        cast_id = process_actor_selection(actor_name)
        
        if cast_id:
            try:
                # 构建网络
                actor_network = network.build_actor_network_by_id(cast_id)
                
                # 显示基本统计
                stats = network.get_network_stats(actor_network)
                print(f"📊 网络统计: {stats['nodes']} 节点, {stats['edges']} 边")
                
                # 显示主要合作伙伴
                collaborations = network.get_collaboration_frequency_by_id(cast_id, top_n=3)
                if collaborations:
                    print(f"🤝 主要合作伙伴:")
                    for collab in collaborations:
                        print(f"   - {collab['collaborator']} ({collab['frequency']} 次)")
                
            except Exception as e:
                print(f"❌ 处理失败: {e}")
        
        print("-" * 30)

def main():
    """主函数"""
    try:
        demonstrate_duplicate_name_handling()
        interactive_actor_selection()
        
        print(f"\n🎉 重名处理演示完成!")
        print("💡 在实际使用中，用户可以:")
        print("   1. 使用 get_actors_by_name_with_selection() 获取同名演员列表")
        print("   2. 选择正确的 cast_id")
        print("   3. 使用 build_actor_network_by_id() 构建网络")
        
    except Exception as e:
        print(f"❌ 演示过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
