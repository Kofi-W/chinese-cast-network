"""
测试数据加载模块
Test Data Loader Module
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    """测试数据加载器"""
    
    def setUp(self):
        """测试前准备"""
        self.data_loader = DataLoader()
        self.test_cast_data_path = 'data/cast_data.csv'
        self.test_cast_works_path = 'data/cast_works_data.csv'
        self.test_works_data_path = 'data/works_data.csv'
    
    def test_load_data(self):
        """测试数据加载"""
        try:
            cast_data_df, cast_works_df, works_data_df = self.data_loader.load_data(
                self.test_cast_data_path,
                self.test_cast_works_path,
                self.test_works_data_path
            )
            
            # 检查数据是否成功加载
            self.assertIsNotNone(cast_data_df)
            self.assertIsNotNone(cast_works_df)
            self.assertIsNotNone(works_data_df)
            
            # 检查数据结构
            self.assertIn('cast_id', cast_data_df.columns)
            self.assertIn('cast_name', cast_data_df.columns)
            self.assertIn('main_works', cast_data_df.columns)
            
            self.assertIn('work_id', cast_works_df.columns)
            self.assertIn('cast_id', cast_works_df.columns)
            self.assertIn('cast_name', cast_works_df.columns)
            
            self.assertIn('work_id', works_data_df.columns)
            self.assertIn('work_title', works_data_df.columns)
            
            print(f"数据加载测试通过:")
            print(f"  演员数据: {len(cast_data_df)} 条记录")
            print(f"  演员作品关系: {len(cast_works_df)} 条记录")
            print(f"  作品数据: {len(works_data_df)} 条记录")
            
        except Exception as e:
            self.fail(f"数据加载失败: {e}")
    
    def test_get_actor_by_name(self):
        """测试按姓名查找演员"""
        try:
            # 先加载数据
            self.data_loader.load_data(
                self.test_cast_data_path,
                self.test_cast_works_path,
                self.test_works_data_path
            )
            
            # 测试查找已知演员
            test_actor = "周星驰"
            result = self.data_loader.get_actor_by_name(test_actor)
            
            if not result.empty:
                self.assertEqual(result.iloc[0]['cast_name'], test_actor)
                print(f"演员查找测试通过: 找到 {test_actor}")
            else:
                print(f"未找到演员 {test_actor}，尝试其他演员...")
                # 随机选择一个演员进行测试
                sample_actor = self.data_loader.cast_data_df.iloc[0]['cast_name']
                result = self.data_loader.get_actor_by_name(sample_actor)
                self.assertFalse(result.empty)
                print(f"演员查找测试通过: 找到 {sample_actor}")
                
        except Exception as e:
            self.fail(f"演员查找测试失败: {e}")
    
    def test_get_cast_collaboration_data(self):
        """测试获取演员合作数据"""
        try:
            # 先加载数据
            self.data_loader.load_data(
                self.test_cast_data_path,
                self.test_cast_works_path,
                self.test_works_data_path
            )
            
            # 选择第一个演员进行测试
            test_actor = self.data_loader.cast_data_df.iloc[0]['cast_name']
            
            collaboration_data = self.data_loader.get_cast_collaboration_data(test_actor)
            
            # 检查结果
            if not collaboration_data.empty:
                self.assertIn('work_id', collaboration_data.columns)
                self.assertIn('cast_name', collaboration_data.columns)
                print(f"合作数据获取测试通过: {test_actor} 有 {len(collaboration_data)} 条合作记录")
            else:
                print(f"演员 {test_actor} 没有合作数据")
                
        except Exception as e:
            self.fail(f"合作数据获取测试失败: {e}")

if __name__ == '__main__':
    unittest.main()
