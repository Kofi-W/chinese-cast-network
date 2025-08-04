"""
华语影视演员合作网络数据分析工具
Chinese Cast Network Analysis Tool
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from typing import Optional, List
from .data_loader import DataLoader
from .network_builder import NetworkBuilder
from .visualizer import NetworkVisualizer

class CastNetwork:
    """华语影视演员合作网络分析主类"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.network_builder = NetworkBuilder()
        self.visualizer = NetworkVisualizer()
        self.cast_data_df = None
        self.cast_works_df = None
        self.works_data_df = None
    
    def load_data(self, cast_data_path='data/cast_data.csv', 
                  cast_works_path='data/cast_works_data.csv',
                  works_data_path='data/works_data.csv'):
        """加载数据文件"""
        self.cast_data_df, self.cast_works_df, self.works_data_df = self.data_loader.load_data(
            cast_data_path, cast_works_path, works_data_path
        )
        return self
    
    def build_actor_network(self, cast_name):
        """构建指定演员的合作网络"""
        if self.cast_data_df is None or self.cast_works_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.network_builder.build_actor_network(
            cast_name, self.cast_data_df, self.cast_works_df
        )
    
    def build_actor_network_by_id(self, cast_id: int, include_roles: Optional[List[str]] = None):
        """根据演员ID构建合作网络（用于处理重名情况）
        
        Args:
            cast_id: 演员ID
            include_roles: 要包含的职能列表，如 ['演员', '导演']。None表示包含所有职能
            
        Returns:
            nx.Graph: 演员合作网络图
        """
        if self.cast_data_df is None or self.cast_works_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.network_builder.build_actor_network_by_id(
            cast_id, self.cast_data_df, self.cast_works_df, include_roles
        )
    
    def get_actors_by_name_with_selection(self, cast_name):
        """获取同名演员列表供用户选择"""
        if self.cast_data_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.data_loader.get_actors_by_name_with_selection(cast_name)
    
    def build_multi_actor_network(self, cast_names):
        """构建多个演员的合作网络"""
        if self.cast_data_df is None or self.cast_works_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.network_builder.build_multi_actor_network(
            cast_names, self.cast_data_df, self.cast_works_df
        )
    
    def get_collaboration_frequency(self, cast_name, top_n=10):
        """获取演员的合作频率统计"""
        if self.cast_data_df is None or self.cast_works_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.network_builder.get_collaboration_frequency(
            cast_name, self.cast_data_df, self.cast_works_df, top_n
        )
    
    def get_collaboration_frequency_by_id(self, cast_id, top_n=10):
        """根据演员ID获取合作频率统计（用于处理重名情况）"""
        if self.cast_data_df is None or self.cast_works_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.network_builder.get_collaboration_frequency_by_id(
            cast_id, self.cast_data_df, self.cast_works_df, top_n
        )
    
    def get_cast_collaboration_data(self, cast_name):
        """获取指定演员的所有合作数据"""
        if self.cast_data_df is None or self.cast_works_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.data_loader.get_cast_collaboration_data(cast_name)
    
    def get_cast_collaboration_data_by_id(self, cast_id: int, include_roles: Optional[List[str]] = None):
        """根据演员ID获取合作数据（用于处理重名情况）
        
        Args:
            cast_id: 演员ID
            include_roles: 要包含的职能列表，如 ['演员', '导演']。None表示包含所有职能
            
        Returns:
            pd.DataFrame: 合作数据
        """
        if self.cast_data_df is None or self.cast_works_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.data_loader.get_cast_collaboration_data_by_id(cast_id, include_roles)
    
    def get_available_roles(self):
        """获取数据中所有可用的职能列表"""
        if self.cast_works_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.data_loader.get_available_roles()
    
    def get_role_statistics(self):
        """获取各职能的统计信息"""
        if self.cast_works_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.data_loader.get_role_statistics()
    
    def get_genres_statistics(self):
        """获取作品题材的统计信息"""
        if self.cast_works_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.data_loader.get_genres_statistics()
    
    def search_actors(self, keyword, limit=10):
        """搜索演员"""
        if self.cast_data_df is None:
            raise ValueError("请先调用 load_data() 加载数据")
        
        return self.data_loader.search_actors(keyword, limit)
    
    def visualize_network(self, network, **kwargs):
        """可视化网络"""
        return self.visualizer.plot_network(network, **kwargs)
    
    def visualize_interactive_network(self, network, title="演员合作网络"):
        """创建交互式网络可视化"""
        return self.visualizer.plot_interactive_network(network, title)
    
    def get_network_stats(self, network):
        """获取网络统计信息"""
        return self.network_builder.get_network_stats(network)
    
    def export_network(self, network, filepath, format='gexf'):
        """导出网络数据"""
        return self.visualizer.export_network(network, filepath, format)
