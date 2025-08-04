"""
数据加载模块
Data Loading Module
"""

import pandas as pd
import os
from typing import Tuple, List

class DataLoader:
    """数据加载器"""
    
    def __init__(self):
        self.cast_data_df = None
        self.cast_works_df = None
        self.works_data_df = None
    
    def load_data(self, cast_data_path: str = 'data/cast_data.csv', 
                  cast_works_path: str = 'data/cast_works_data.csv',
                  works_data_path: str = 'data/works_data.csv') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        加载演员数据、演员作品关系数据和作品数据
        
        Args:
            cast_data_path: 演员表CSV文件路径
            cast_works_path: 演员作品关系表CSV文件路径
            works_data_path: 作品表CSV文件路径
            
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: 演员数据、演员作品关系数据、作品数据
        """
        if not os.path.exists(cast_data_path):
            raise FileNotFoundError(f"演员表文件不存在: {cast_data_path}")
        
        if not os.path.exists(cast_works_path):
            raise FileNotFoundError(f"演员作品关系表文件不存在: {cast_works_path}")
            
        if not os.path.exists(works_data_path):
            raise FileNotFoundError(f"作品表文件不存在: {works_data_path}")
        
        try:
            # 加载演员表
            self.cast_data_df = pd.read_csv(cast_data_path, encoding='utf-8')
            print(f"成功加载演员数据: {len(self.cast_data_df)} 条记录")
            
            # 加载演员作品关系表
            self.cast_works_df = pd.read_csv(cast_works_path, encoding='utf-8')
            print(f"成功加载演员作品关系数据: {len(self.cast_works_df)} 条记录")
            
            # 加载作品表
            self.works_data_df = pd.read_csv(works_data_path, encoding='utf-8')
            print(f"成功加载作品数据: {len(self.works_data_df)} 条记录")
            
            # 数据预处理
            self._preprocess_data()
            
            return self.cast_data_df, self.cast_works_df, self.works_data_df
            
        except Exception as e:
            raise Exception(f"数据加载失败: {str(e)}")
    
    def _preprocess_data(self):
        """数据预处理"""
        # 清理空值和重复数据
        if self.cast_data_df is not None:
            self.cast_data_df = self.cast_data_df.dropna(subset=['cast_id', 'cast_name'])
            self.cast_data_df = self.cast_data_df.drop_duplicates(subset=['cast_id'])
        
        if self.cast_works_df is not None:
            self.cast_works_df = self.cast_works_df.dropna(subset=['work_id', 'cast_id'])
            # 确保年份是数值类型
            self.cast_works_df['work_year'] = pd.to_numeric(self.cast_works_df['work_year'], errors='coerce')
            
        if self.works_data_df is not None:
            self.works_data_df = self.works_data_df.dropna(subset=['work_id'])
            self.works_data_df = self.works_data_df.drop_duplicates(subset=['work_id'])
    
    def get_actor_by_name(self, cast_name: str) -> pd.DataFrame:
        """
        根据演员姓名查找演员信息
        
        Args:
            cast_name: 演员姓名
            
        Returns:
            pd.DataFrame: 匹配的演员信息
        """
        if self.cast_data_df is None:
            raise ValueError("请先加载数据")
        
        return self.cast_data_df[self.cast_data_df['cast_name'] == cast_name]
    
    def get_actors_by_name_with_selection(self, cast_name: str) -> pd.DataFrame:
        """
        根据演员姓名查找演员信息，处理重名情况
        返回所有匹配的演员供用户选择
        
        Args:
            cast_name: 演员姓名
            
        Returns:
            pd.DataFrame: 所有匹配的演员信息，包含cast_name, cast_id, main_works
        """
        if self.cast_data_df is None:
            raise ValueError("请先加载数据")
        
        matches = self.cast_data_df[self.cast_data_df['cast_name'] == cast_name]
        
        if matches.empty:
            print(f"未找到演员: {cast_name}")
            return pd.DataFrame()
        
        # 只返回用户需要的字段
        result = matches[['cast_name', 'cast_id', 'main_works']].copy()
        
        if len(result) > 1:
            print(f"找到 {len(result)} 个同名演员 '{cast_name}':")
            print("请选择正确的演员:")
            for idx, row in result.iterrows():
                print(f"  {idx + 1}. ID: {row['cast_id']} - 代表作: {row['main_works']}")
        
        return result
    
    def get_actor_works(self, cast_id: str) -> pd.DataFrame:
        """
        根据演员ID获取该演员的所有作品
        
        Args:
            cast_id: 演员ID
            
        Returns:
            pd.DataFrame: 该演员的所有作品数据
        """
        if self.cast_works_df is None:
            raise ValueError("请先加载数据")
        
        return self.cast_works_df[self.cast_works_df['cast_id'] == cast_id]
    
    def get_work_cast(self, work_id: str) -> pd.DataFrame:
        """
        根据作品ID获取该作品的所有演职员
        
        Args:
            work_id: 作品ID
            
        Returns:
            pd.DataFrame: 该作品的所有演职员数据
        """
        if self.cast_works_df is None:
            raise ValueError("请先加载数据")
        
        return self.cast_works_df[self.cast_works_df['work_id'] == work_id]
    
    def get_cast_collaboration_data(self, cast_name: str) -> pd.DataFrame:
        """
        获取指定演员的所有合作数据
        这是核心功能：通过cast_name选择cast_id，然后获取所有相关作品的cast数据
        
        Args:
            cast_name: 演员姓名
            
        Returns:
            pd.DataFrame: 该演员所有作品的完整cast数据
        """
        # 1. 通过cast_name从演员表中查找所有匹配的演员
        actor_matches = self.get_actors_by_name_with_selection(cast_name)
        
        if actor_matches.empty:
            raise ValueError(f"未找到演员: {cast_name}")
        
        # 如果有多个同名演员，需要用户选择
        if len(actor_matches) > 1:
            print(f"\n警告: 找到多个同名演员 '{cast_name}'")
            print("请使用 get_cast_collaboration_data_by_id(cast_id) 方法，并提供具体的 cast_id")
            return pd.DataFrame()
        
        # 只有一个匹配结果，继续处理
        cast_id = actor_matches.iloc[0]['cast_id']
        return self._get_collaboration_data_by_id(cast_id, cast_name)
    
    def get_cast_collaboration_data_by_id(self, cast_id: str, 
                                        include_roles: List[str] = None) -> pd.DataFrame:
        """
        根据演员ID获取合作数据
        用于处理重名演员的情况
        
        Args:
            cast_id: 演员ID
            include_roles: 要包含的职能列表，如 ['演员', '导演']。如果为None则包含所有职能
            
        Returns:
            pd.DataFrame: 该演员所有作品的完整cast数据
        """
        if self.cast_data_df is None or self.cast_works_df is None:
            raise ValueError("请先加载数据")
        
        # 获取演员姓名
        actor_info = self.cast_data_df[self.cast_data_df['cast_id'] == cast_id]
        if actor_info.empty:
            raise ValueError(f"未找到演员ID: {cast_id}")
        
        cast_name = actor_info.iloc[0]['cast_name']
        return self._get_collaboration_data_by_id(cast_id, cast_name, include_roles)
    
    def _get_collaboration_data_by_id(self, cast_id: str, cast_name: str, 
                                    include_roles: List[str] = None) -> pd.DataFrame:
        """
        内部方法：根据cast_id获取合作数据
        
        Args:
            cast_id: 演员ID
            cast_name: 演员姓名
            include_roles: 要包含的职能列表
            
        Returns:
            pd.DataFrame: 合作数据
        """
        # 2. 使用cast_id从cast_works_data表筛选出该cast的所有作品
        actor_works = self.get_actor_works(cast_id)
        
        if actor_works.empty:
            print(f"演员 {cast_name} (ID: {cast_id}) 没有作品记录")
            return pd.DataFrame()
        
        # 3. 获取这些作品的所有cast数据
        all_work_ids = actor_works['work_id'].unique()
        
        # 获取这些作品中的所有演员数据
        collaboration_data = self.cast_works_df[
            self.cast_works_df['work_id'].isin(all_work_ids)
        ].copy()
        
        # 4. 根据职能筛选数据
        if include_roles is not None:
            before_filter = len(collaboration_data)
            collaboration_data = collaboration_data[
                collaboration_data['cast_role'].isin(include_roles)
            ]
            after_filter = len(collaboration_data)
            print(f"职能筛选: {before_filter} -> {after_filter} 条记录 (保留职能: {', '.join(include_roles)})")
        
        print(f"演员 {cast_name} (ID: {cast_id}) 共参演 {len(all_work_ids)} 部作品，涉及 {len(collaboration_data)} 条演员记录")
        
        return collaboration_data
    
    def search_actors(self, keyword: str, limit: int = 10) -> pd.DataFrame:
        """
        搜索演员
        
        Args:
            keyword: 搜索关键词
            limit: 返回结果数量限制
            
        Returns:
            pd.DataFrame: 搜索结果
        """
        if self.cast_data_df is None:
            raise ValueError("请先加载数据")
        
        # 在演员姓名中搜索
        results = self.cast_data_df[
            self.cast_data_df['cast_name'].str.contains(keyword, na=False, case=False)
        ].head(limit)
        
        return results
    
    def get_available_roles(self) -> List[str]:
        """
        获取数据中所有可用的职能类型
        
        Returns:
            List[str]: 职能类型列表
        """
        if self.cast_works_df is None:
            raise ValueError("请先加载数据")
        
        roles = self.cast_works_df['cast_role'].unique().tolist()
        roles = [role for role in roles if pd.notna(role)]  # 过滤空值
        return sorted(roles)
    
    def get_role_statistics(self) -> pd.DataFrame:
        """
        获取职能统计信息
        
        Returns:
            pd.DataFrame: 职能统计结果
        """
        if self.cast_works_df is None:
            raise ValueError("请先加载数据")
        
        role_stats = self.cast_works_df.groupby('cast_role').agg({
            'cast_id': 'nunique',  # 不重复人数
            'work_id': 'nunique',  # 参与作品数
            'cast_name': 'count'   # 总记录数
        }).rename(columns={
            'cast_id': '人数',
            'work_id': '作品数',
            'cast_name': '记录数'
        }).sort_values('记录数', ascending=False)
        
        return role_stats
    
    def get_genres_statistics(self) -> pd.DataFrame:
        """
        获取作品题材统计信息
        
        Returns:
            pd.DataFrame: 题材统计结果
        """
        if self.cast_works_df is None:
            raise ValueError("请先加载数据")
        
        # 处理多个题材的情况（用/分隔）
        all_genres = []
        for genres_str in self.cast_works_df['work_genres'].dropna():
            if isinstance(genres_str, str):
                genres = [g.strip() for g in genres_str.split('/')]
                all_genres.extend(genres)
        
        # 统计题材出现频次
        from collections import Counter
        genre_counts = Counter(all_genres)
        
        # 转换为DataFrame
        genre_stats = pd.DataFrame([
            {'题材': genre, '作品数': count} 
            for genre, count in genre_counts.most_common()
        ])
        
        return genre_stats
