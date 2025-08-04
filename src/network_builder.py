"""
网络构建模块
Network Building Module
"""

import pandas as pd
import networkx as nx
from collections import defaultdict
from typing import Dict, List, Set

class NetworkBuilder:
    """合作网络构建器"""
    
    def __init__(self):
        pass
    
    def build_actor_network(self, cast_name: str, cast_data_df: pd.DataFrame, 
                          cast_works_df: pd.DataFrame) -> nx.Graph:
        """
        构建指定演员的合作网络
        这是核心功能的实现
        
        Args:
            cast_name: 演员姓名
            cast_data_df: 演员数据
            cast_works_df: 演员作品关系数据
            
        Returns:
            nx.Graph: 合作网络图
        """
        # 1. 通过cast_name从演员表中查找所有匹配的演员
        target_actors = cast_data_df[cast_data_df['cast_name'] == cast_name]
        if target_actors.empty:
            raise ValueError(f"未找到演员: {cast_name}")
        
        # 处理重名情况
        if len(target_actors) > 1:
            print(f"找到 {len(target_actors)} 个同名演员 '{cast_name}':")
            for idx, row in target_actors.iterrows():
                print(f"  {idx + 1}. ID: {row['cast_id']} - 代表作: {row['main_works']}")
            raise ValueError(f"存在多个同名演员，请使用 build_actor_network_by_id(cast_id) 方法指定具体的演员ID")
        
        # 只有一个匹配结果，继续处理
        cast_id = target_actors.iloc[0]['cast_id']
        main_works = target_actors.iloc[0]['main_works']
        
        return self._build_network_by_id(cast_id, cast_name, main_works, cast_works_df)
    
    def build_actor_network_by_id(self, cast_id: str, cast_data_df: pd.DataFrame, 
                                cast_works_df: pd.DataFrame,
                                include_roles: List[str] = None) -> nx.Graph:
        """
        根据演员ID构建合作网络
        用于处理重名演员的情况
        
        Args:
            cast_id: 演员ID
            cast_data_df: 演员数据
            cast_works_df: 演员作品关系数据
            include_roles: 要包含的职能列表，如 ['演员', '导演']。如果为None则包含所有职能
            
        Returns:
            nx.Graph: 合作网络图
        """
        # 获取演员信息
        target_actor = cast_data_df[cast_data_df['cast_id'] == cast_id]
        if target_actor.empty:
            raise ValueError(f"未找到演员ID: {cast_id}")
        
        cast_name = target_actor.iloc[0]['cast_name']
        main_works = target_actor.iloc[0]['main_works']
        
        return self._build_network_by_id(cast_id, cast_name, main_works, cast_works_df, include_roles)
    
    def _build_network_by_id(self, cast_id: str, cast_name: str, main_works: str, 
                           cast_works_df: pd.DataFrame, 
                           include_roles: List[str] = None) -> nx.Graph:
        """
        内部方法：根据cast_id构建网络
        
        Args:
            cast_id: 演员ID
            cast_name: 演员姓名
            main_works: 代表作品
            cast_works_df: 演员作品关系数据
            include_roles: 要包含的职能列表
            
        Returns:
            nx.Graph: 合作网络图
        """
        # 2. 使用cast_id从cast_works_data表筛选出该cast的所有作品
        actor_works = cast_works_df[cast_works_df['cast_id'] == cast_id]
        
        if actor_works.empty:
            print(f"演员 {cast_name} (ID: {cast_id}) 没有作品记录")
            return nx.Graph()
        
        # 3. 根据职能筛选数据
        if include_roles is not None:
            # 筛选所有相关作品的数据
            work_ids = set(actor_works['work_id'].tolist())
            all_cast_data = cast_works_df[cast_works_df['work_id'].isin(work_ids)]
            filtered_cast_data = all_cast_data[all_cast_data['cast_role'].isin(include_roles)]
            
            print(f"职能筛选: 从 {len(all_cast_data)} 条记录筛选到 {len(filtered_cast_data)} 条记录")
            print(f"包含职能: {', '.join(include_roles)}")
            
            # 使用筛选后的数据
            cast_works_df = filtered_cast_data
            
            # 重新获取该演员在筛选后数据中的作品
            actor_works = cast_works_df[cast_works_df['cast_id'] == cast_id]
            if actor_works.empty:
                print(f"演员 {cast_name} 在指定职能 {include_roles} 中没有记录")
                return nx.Graph()
        
        # 4. 构建合作网络
        G = nx.Graph()
        
        # 添加目标演员节点
        G.add_node(cast_name, 
                  cast_id=cast_id,
                  node_type='target',
                  works_count=len(actor_works),
                  main_works=main_works,
                  include_roles=include_roles or ['所有职能'])
        
        # 统计合作关系
        collaborations = defaultdict(lambda: {
            'works': set(), 
            'count': 0, 
            'work_types': set(),
            'genres': set(),
            'years': set(),
            'cast_id': None,
            'roles': set()  # 新增：记录合作者的职能
        })
        
        # 获取该演员所有作品的ID
        work_ids = set(actor_works['work_id'].tolist())
        
        # 遍历该演员的每部作品，找出合作者
        for work_id in work_ids:
            # 获取该作品的所有演职员
            work_cast = cast_works_df[cast_works_df['work_id'] == work_id]
            
            # 获取作品信息
            work_info = work_cast.iloc[0] if not work_cast.empty else None
            work_title = work_info['work_title'] if work_info is not None else str(work_id)
            work_type = work_info['work_type'] if work_info is not None else 'Unknown'
            work_year = work_info['work_year'] if work_info is not None else None
            work_genres = work_info['work_genres'] if work_info is not None else 'Unknown'
            
            # 找出与目标演员合作的其他演员
            for _, collaborator in work_cast.iterrows():
                if collaborator['cast_id'] != cast_id:  # 不包括自己
                    collab_name = collaborator['cast_name']
                    collab_id = collaborator['cast_id']
                    collab_role = collaborator['cast_role']
                    
                    # 记录合作关系
                    collaborations[collab_name]['works'].add(work_title)
                    collaborations[collab_name]['count'] += 1
                    collaborations[collab_name]['work_types'].add(work_type)
                    collaborations[collab_name]['genres'].add(work_genres)
                    collaborations[collab_name]['roles'].add(collab_role)
                    if work_year:
                        collaborations[collab_name]['years'].add(work_year)
                    collaborations[collab_name]['cast_id'] = collab_id
        
        # 添加合作者节点和边
        for collab_name, collab_info in collaborations.items():
            if collab_info['count'] > 0:
                # 添加合作者节点
                G.add_node(collab_name,
                          cast_id=collab_info['cast_id'],
                          node_type='collaborator',
                          collaboration_count=collab_info['count'],
                          roles=list(collab_info['roles']))
                
                # 添加合作关系边
                G.add_edge(cast_name, collab_name,
                          weight=collab_info['count'],
                          works=list(collab_info['works']),
                          work_types=list(collab_info['work_types']),
                          genres=list(collab_info['genres']),
                          years=sorted(list(collab_info['years'])) if collab_info['years'] else [],
                          collaborator_roles=list(collab_info['roles']))
        
        role_filter_info = f" (职能筛选: {', '.join(include_roles)})" if include_roles else ""
        print(f"构建完成: {cast_name} (ID: {cast_id}) 的合作网络{role_filter_info} 包含 {G.number_of_nodes()} 个节点, {G.number_of_edges()} 条边")
        print(f"参演作品数: {len(work_ids)}")
        
        return G
    
    def build_multi_actor_network(self, cast_names: List[str], cast_data_df: pd.DataFrame, 
                                cast_works_df: pd.DataFrame) -> nx.Graph:
        """
        构建多个演员的合作网络
        
        Args:
            cast_names: 演员姓名列表
            cast_data_df: 演员数据
            cast_works_df: 演员作品关系数据
            
        Returns:
            nx.Graph: 多演员合作网络图
        """
        G = nx.Graph()
        
        all_collaborators = set()
        
        # 为每个目标演员构建网络并合并
        for cast_name in cast_names:
            try:
                actor_network = self.build_actor_network(cast_name, cast_data_df, cast_works_df)
                
                # 合并网络
                for node, data in actor_network.nodes(data=True):
                    if node in cast_names:
                        data['node_type'] = 'target'
                    G.add_node(node, **data)
                    all_collaborators.add(node)
                
                for u, v, data in actor_network.edges(data=True):
                    if G.has_edge(u, v):
                        # 合并边的权重和作品信息
                        existing_data = G[u][v]
                        existing_data['weight'] += data['weight']
                        existing_data['works'] = list(set(existing_data['works'] + data['works']))
                        existing_data['work_types'] = list(set(existing_data['work_types'] + data['work_types']))
                        existing_data['years'] = sorted(list(set(existing_data['years'] + data['years'])))
                    else:
                        G.add_edge(u, v, **data)
                        
            except ValueError as e:
                print(f"跳过演员 {cast_name}: {e}")
        
        print(f"多演员网络构建完成: {G.number_of_nodes()} 个节点, {G.number_of_edges()} 条边")
        
        return G
    
    def build_work_network(self, work_id: str, cast_works_df: pd.DataFrame) -> nx.Graph:
        """
        构建单部作品内的演员合作网络
        
        Args:
            work_id: 作品ID
            cast_works_df: 演员作品关系数据
            
        Returns:
            nx.Graph: 作品内演员网络图
        """
        work_cast = cast_works_df[cast_works_df['work_id'] == work_id]
        
        if work_cast.empty:
            raise ValueError(f"未找到作品: {work_id}")
        
        G = nx.Graph()
        cast_list = work_cast['cast_name'].tolist()
        
        # 获取作品信息
        work_info = work_cast.iloc[0]
        work_title = work_info['work_title']
        work_type = work_info['work_type']
        work_year = work_info['work_year']
        
        # 添加所有演员节点
        for _, cast_info in work_cast.iterrows():
            G.add_node(cast_info['cast_name'],
                      cast_id=cast_info['cast_id'],
                      cast_role=cast_info['cast_role'],
                      cast_order=cast_info['cast_order'])
        
        # 添加所有演员之间的合作关系（完全图）
        for i in range(len(cast_list)):
            for j in range(i + 1, len(cast_list)):
                actor1, actor2 = cast_list[i], cast_list[j]
                if actor1 != actor2:
                    G.add_edge(actor1, actor2,
                              work_id=work_id,
                              work_title=work_title,
                              work_type=work_type,
                              work_year=work_year,
                              weight=1)
        
        return G
    
    def get_collaboration_frequency(self, cast_name: str, cast_data_df: pd.DataFrame, 
                                  cast_works_df: pd.DataFrame, top_n: int = 10) -> List[Dict]:
        """
        获取演员的合作频率统计
        
        Args:
            cast_name: 演员姓名
            cast_data_df: 演员数据
            cast_works_df: 演员作品关系数据
            top_n: 返回前N个合作伙伴
            
        Returns:
            List[Dict]: 合作频率统计结果
        """
        try:
            network = self.build_actor_network(cast_name, cast_data_df, cast_works_df)
        except ValueError as e:
            if "存在多个同名演员" in str(e):
                print(f"无法直接分析 '{cast_name}' 的合作频率: {e}")
                return []
            else:
                raise e
        
        collaborations = []
        for neighbor in network.neighbors(cast_name):
            edge_data = network[cast_name][neighbor]
            collaborations.append({
                'collaborator': neighbor,
                'frequency': edge_data['weight'],
                'works': edge_data['works'],
                'work_count': len(edge_data['works']),
                'work_types': edge_data['work_types'],
                'years': edge_data['years']
            })
        
        # 按合作频率排序
        collaborations.sort(key=lambda x: x['frequency'], reverse=True)
        
        return collaborations[:top_n]
    
    def get_collaboration_frequency_by_id(self, cast_id: str, cast_data_df: pd.DataFrame, 
                                        cast_works_df: pd.DataFrame, top_n: int = 10) -> List[Dict]:
        """
        根据演员ID获取合作频率统计
        用于处理重名演员的情况
        
        Args:
            cast_id: 演员ID
            cast_data_df: 演员数据
            cast_works_df: 演员作品关系数据
            top_n: 返回前N个合作伙伴
            
        Returns:
            List[Dict]: 合作频率统计结果
        """
        network = self.build_actor_network_by_id(cast_id, cast_data_df, cast_works_df)
        
        # 获取演员姓名
        target_actor = cast_data_df[cast_data_df['cast_id'] == cast_id]
        cast_name = target_actor.iloc[0]['cast_name']
        
        collaborations = []
        for neighbor in network.neighbors(cast_name):
            edge_data = network[cast_name][neighbor]
            collaborations.append({
                'collaborator': neighbor,
                'frequency': edge_data['weight'],
                'works': edge_data['works'],
                'work_count': len(edge_data['works']),
                'work_types': edge_data['work_types'],
                'years': edge_data['years']
            })
        
        # 按合作频率排序
        collaborations.sort(key=lambda x: x['frequency'], reverse=True)
        
        return collaborations[:top_n]
    
    def get_network_stats(self, G: nx.Graph) -> Dict:
        """
        获取网络统计信息
        
        Args:
            G: 网络图
            
        Returns:
            Dict: 网络统计信息
        """
        stats = {
            'nodes': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'density': nx.density(G),
            'is_connected': nx.is_connected(G),
        }
        
        if G.number_of_nodes() > 0:
            stats['average_clustering'] = nx.average_clustering(G)
            
            # 计算度分布
            degrees = [G.degree(n) for n in G.nodes()]
            stats['average_degree'] = sum(degrees) / len(degrees) if degrees else 0
            stats['max_degree'] = max(degrees) if degrees else 0
            stats['min_degree'] = min(degrees) if degrees else 0
            
            if nx.is_connected(G):
                stats['diameter'] = nx.diameter(G)
                stats['average_path_length'] = nx.average_shortest_path_length(G)
            else:
                stats['connected_components'] = nx.number_connected_components(G)
                # 获取最大连通分量的统计
                largest_cc = max(nx.connected_components(G), key=len)
                largest_subgraph = G.subgraph(largest_cc)
                stats['largest_component_size'] = len(largest_cc)
                stats['largest_component_diameter'] = nx.diameter(largest_subgraph)
        
        return stats
