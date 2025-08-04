"""
网络可视化模块
Network Visualization Module
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Optional

class NetworkVisualizer:
    """网络可视化器"""
    
    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def plot_network(self, G: nx.Graph, figsize: tuple = (12, 8), 
                    node_size_factor: int = 300, edge_width_factor: float = 0.5,
                    layout: str = 'spring', save_path: Optional[str] = None) -> None:
        """
        使用matplotlib可视化网络
        
        Args:
            G: 网络图
            figsize: 图形大小
            node_size_factor: 节点大小因子
            edge_width_factor: 边宽度因子
            layout: 布局算法 ('spring', 'circular', 'kamada_kawai', 'random')
            save_path: 保存路径
        """
        if G.number_of_nodes() == 0:
            print("网络为空，无法可视化")
            return
        
        plt.figure(figsize=figsize)
        
        # 选择布局算法
        if layout == 'spring':
            pos = nx.spring_layout(G, k=1, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.random_layout(G)
        
        # 设置节点颜色和大小
        node_colors = []
        node_sizes = []
        
        for node, data in G.nodes(data=True):
            if data.get('node_type') == 'target':
                node_colors.append('#FF6B6B')  # 红色 - 目标演员
                node_sizes.append(node_size_factor * 3)
            else:
                node_colors.append('#4ECDC4')  # 青色 - 合作演员
                node_sizes.append(node_size_factor)
        
        # 设置边的宽度
        edge_widths = []
        for u, v, data in G.edges(data=True):
            weight = data.get('weight', 1)
            edge_widths.append(weight * edge_width_factor)
        
        # 绘制网络
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=node_sizes, alpha=0.8)
        
        nx.draw_networkx_edges(G, pos, width=edge_widths, 
                              alpha=0.6, edge_color='gray')
        
        # 添加标签（只显示度数较高的节点标签）
        degrees = dict(G.degree())
        high_degree_nodes = {n: n for n, d in degrees.items() if d >= np.percentile(list(degrees.values()), 70)}
        
        nx.draw_networkx_labels(G, pos, labels=high_degree_nodes, 
                               font_size=8, font_weight='bold')
        
        plt.title(f"演员合作网络\n节点数: {G.number_of_nodes()}, 边数: {G.number_of_edges()}", 
                 fontsize=14, fontweight='bold')
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"网络图已保存到: {save_path}")
        
        plt.show()
    
    def plot_interactive_network(self, G: nx.Graph, title: str = "演员合作网络") -> go.Figure:
        """
        使用plotly创建交互式网络可视化
        
        Args:
            G: 网络图
            title: 图表标题
            
        Returns:
            go.Figure: plotly图表对象
        """
        if G.number_of_nodes() == 0:
            print("网络为空，无法可视化")
            return None
        
        # 计算布局
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # 准备节点数据
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []
        
        for node, data in G.nodes(data=True):
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            # 节点信息
            degree = G.degree(node)
            node_type = data.get('node_type', 'collaborator')
            
            if node_type == 'target':
                works_count = data.get('works_count', 0)
                text = f"{node}<br>目标演员<br>作品数: {works_count}<br>合作伙伴: {degree}"
                node_color.append('#FF6B6B')
                node_size.append(30)
            else:
                collab_count = data.get('collaboration_count', 0)
                text = f"{node}<br>合作演员<br>合作次数: {collab_count}<br>连接数: {degree}"
                node_color.append('#4ECDC4')
                node_size.append(15)
            
            node_text.append(text)
        
        # 准备边数据
        edge_x = []
        edge_y = []
        edge_text = []
        
        for u, v, data in G.edges(data=True):
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
            weight = data.get('weight', 1)
            works = data.get('works', [])
            edge_text.append(f"合作次数: {weight}<br>作品: {', '.join(works[:3])}" + 
                           ("..." if len(works) > 3 else ""))
        
        # 创建边的trace
        edge_trace = go.Scatter(x=edge_x, y=edge_y,
                               line=dict(width=0.5, color='#888'),
                               hoverinfo='none',
                               mode='lines')
        
        # 创建节点的trace
        node_trace = go.Scatter(x=node_x, y=node_y,
                               mode='markers+text',
                               hoverinfo='text',
                               text=[node.split('<br>')[0] for node in node_text],
                               hovertext=node_text,
                               textposition="middle center",
                               marker=dict(showscale=False,
                                         color=node_color,
                                         size=node_size,
                                         line=dict(width=2, color='white')))
        
        # 创建图表
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=title,
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002 ) ],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           width=800,
                           height=600))
        
        return fig
    
    def plot_degree_distribution(self, G: nx.Graph, figsize: tuple = (10, 6)) -> None:
        """
        绘制度分布图
        
        Args:
            G: 网络图
            figsize: 图形大小
        """
        degrees = [G.degree(n) for n in G.nodes()]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # 度分布直方图
        ax1.hist(degrees, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_xlabel('节点度数')
        ax1.set_ylabel('频数')
        ax1.set_title('度分布直方图')
        ax1.grid(True, alpha=0.3)
        
        # 度分布累积图
        degree_counts = {}
        for d in degrees:
            degree_counts[d] = degree_counts.get(d, 0) + 1
        
        degrees_sorted = sorted(degree_counts.keys())
        counts = [degree_counts[d] for d in degrees_sorted]
        
        ax2.loglog(degrees_sorted, counts, 'bo-', alpha=0.7)
        ax2.set_xlabel('节点度数 (log)')
        ax2.set_ylabel('频数 (log)')
        ax2.set_title('度分布对数图')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_collaboration_heatmap(self, collaborations: List[Dict], 
                                 figsize: tuple = (12, 8)) -> None:
        """
        绘制合作关系热力图
        
        Args:
            collaborations: 合作关系数据
            figsize: 图形大小
        """
        if not collaborations:
            print("没有合作数据可显示")
            return
        
        # 准备数据
        names = [c['collaborator'] for c in collaborations[:20]]  # 取前20个
        frequencies = [c['frequency'] for c in collaborations[:20]]
        
        # 创建热力图数据
        data = []
        for i, freq in enumerate(frequencies):
            row = [0] * len(names)
            row[i] = freq
            data.append(row)
        
        plt.figure(figsize=figsize)
        sns.heatmap(data, 
                   xticklabels=names,
                   yticklabels=names,
                   annot=True,
                   cmap='YlOrRd',
                   fmt='d')
        
        plt.title('演员合作频率热力图')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()
    
    def plot_timeline_analysis(self, collaborations: List[Dict], 
                             figsize: tuple = (14, 8)) -> None:
        """
        绘制合作时间线分析
        
        Args:
            collaborations: 合作关系数据
            figsize: 图形大小
        """
        # 准备时间线数据
        timeline_data = []
        for collab in collaborations:
            for year in collab['years']:
                if year and not pd.isna(year):
                    timeline_data.append({
                        'collaborator': collab['collaborator'],
                        'year': int(year),
                        'frequency': collab['frequency']
                    })
        
        if not timeline_data:
            print("没有时间数据可显示")
            return
        
        df = pd.DataFrame(timeline_data)
        
        # 创建子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
        
        # 按年份统计合作次数
        yearly_collabs = df.groupby('year').size()
        ax1.plot(yearly_collabs.index, yearly_collabs.values, marker='o', linewidth=2)
        ax1.set_title('合作关系年度分布')
        ax1.set_xlabel('年份')
        ax1.set_ylabel('合作次数')
        ax1.grid(True, alpha=0.3)
        
        # 热力图显示演员-年份关系
        pivot_data = df.pivot_table(values='frequency', 
                                   index='collaborator', 
                                   columns='year', 
                                   fill_value=0)
        
        # 只显示前15个合作最多的演员
        top_collaborators = df.groupby('collaborator')['frequency'].first().nlargest(15).index
        pivot_data_top = pivot_data.loc[top_collaborators]
        
        sns.heatmap(pivot_data_top, 
                   cmap='YlOrRd', 
                   ax=ax2,
                   cbar_kws={'label': '合作频次'})
        ax2.set_title('主要合作演员时间分布')
        ax2.set_xlabel('年份')
        ax2.set_ylabel('合作演员')
        
        plt.tight_layout()
        plt.show()
    
    def export_network(self, G: nx.Graph, filepath: str, format: str = 'gexf') -> None:
        """
        导出网络数据
        
        Args:
            G: 网络图
            filepath: 文件路径
            format: 导出格式 ('gexf', 'gml', 'graphml', 'json')
        """
        try:
            if format.lower() == 'gexf':
                nx.write_gexf(G, filepath)
            elif format.lower() == 'gml':
                nx.write_gml(G, filepath)
            elif format.lower() == 'graphml':
                nx.write_graphml(G, filepath)
            elif format.lower() == 'json':
                from networkx.readwrite import json_graph
                import json
                data = json_graph.node_link_data(G)
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                raise ValueError(f"不支持的格式: {format}")
            
            print(f"网络数据已导出到: {filepath}")
            
        except Exception as e:
            print(f"导出失败: {e}")
