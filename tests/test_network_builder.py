"""
测试网络构建模块
Test Network Builder Module
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import DataLoader
from src.network_builder import NetworkBuilder
import networkx as nx

class TestNetworkBuilder(unittest.TestCase):
    """测试网络构建器"""
    
    def setUp(self):
        """测试前准备"""
        self.data_loader = DataLoader()
        self.network_builder = NetworkBuilder()
        
        # 加载测试数据
        try:
            self.cast_data_df, self.cast_works_df, self.works_data_df = self.data_loader.load_data()
        except Exception as e:
            self.skipTest(f"无法加载测试数据: {e}")
    
    def test_build_actor_network(self):
        """测试构建演员网络"""
        try:
            # 选择一个有数据的演员
            test_actor = self.cast_data_df.iloc[0]['cast_name']
            
            # 构建网络
            network = self.network_builder.build_actor_network(
                test_actor, self.cast_data_df, self.cast_works_df
            )
            
            # 检查网络类型
            self.assertIsInstance(network, nx.Graph)
            
            # 检查网络是否包含目标演员
            self.assertIn(test_actor, network.nodes())
            
            # 检查网络节点属性
            if network.number_of_nodes() > 0:
                target_node_data = network.nodes[test_actor]
                self.assertEqual(target_node_data.get('node_type'), 'target')
                
            print(f"演员网络构建测试通过:")
            print(f"  演员: {test_actor}")
            print(f"  节点数: {network.number_of_nodes()}")
            print(f"  边数: {network.number_of_edges()}")
            
        except Exception as e:
            self.fail(f"演员网络构建测试失败: {e}")
    
    def test_get_network_stats(self):
        """测试网络统计"""
        try:
            # 构建一个小网络进行测试
            test_actor = self.cast_data_df.iloc[0]['cast_name']
            network = self.network_builder.build_actor_network(
                test_actor, self.cast_data_df, self.cast_works_df
            )
            
            # 获取统计信息
            stats = self.network_builder.get_network_stats(network)
            
            # 检查统计信息
            self.assertIn('nodes', stats)
            self.assertIn('edges', stats)
            self.assertIn('density', stats)
            
            self.assertEqual(stats['nodes'], network.number_of_nodes())
            self.assertEqual(stats['edges'], network.number_of_edges())
            
            print(f"网络统计测试通过:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
                
        except Exception as e:
            self.fail(f"网络统计测试失败: {e}")
    
    def test_get_collaboration_frequency(self):
        """测试合作频率统计"""
        try:
            # 选择演员
            test_actor = self.cast_data_df.iloc[0]['cast_name']
            
            # 获取合作频率
            collaborations = self.network_builder.get_collaboration_frequency(
                test_actor, self.cast_data_df, self.cast_works_df, top_n=5
            )
            
            # 检查结果
            self.assertIsInstance(collaborations, list)
            
            if collaborations:
                # 检查第一个合作记录的结构
                first_collab = collaborations[0]
                self.assertIn('collaborator', first_collab)
                self.assertIn('frequency', first_collab)
                self.assertIn('works', first_collab)
                
                print(f"合作频率统计测试通过:")
                print(f"  演员: {test_actor}")
                print(f"  合作伙伴数: {len(collaborations)}")
                if collaborations:
                    print(f"  主要合作伙伴: {collaborations[0]['collaborator']} ({collaborations[0]['frequency']} 次)")
            else:
                print(f"演员 {test_actor} 没有合作数据")
                
        except Exception as e:
            self.fail(f"合作频率统计测试失败: {e}")
    
    def test_build_multi_actor_network(self):
        """测试多演员网络构建"""
        try:
            # 选择多个演员
            test_actors = self.cast_data_df.head(3)['cast_name'].tolist()
            
            # 构建多演员网络
            multi_network = self.network_builder.build_multi_actor_network(
                test_actors, self.cast_data_df, self.cast_works_df
            )
            
            # 检查网络
            self.assertIsInstance(multi_network, nx.Graph)
            
            # 检查是否包含目标演员
            for actor in test_actors:
                if multi_network.has_node(actor):
                    node_data = multi_network.nodes[actor]
                    self.assertEqual(node_data.get('node_type'), 'target')
            
            print(f"多演员网络构建测试通过:")
            print(f"  目标演员: {', '.join(test_actors)}")
            print(f"  节点数: {multi_network.number_of_nodes()}")
            print(f"  边数: {multi_network.number_of_edges()}")
            
        except Exception as e:
            self.fail(f"多演员网络构建测试失败: {e}")

if __name__ == '__main__':
    unittest.main()
