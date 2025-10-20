#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蛋白质数据库搜索界面
集成UniProt、PDB、AlphaFold等数据库
"""

import streamlit as st
import pandas as pd
import sys
import os
import time

# 添加AI模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai'))
from database_manager import ProteinDatabaseManager, ProteinInfo

class DatabaseSearchInterface:
    """数据库搜索界面"""
    
    def __init__(self):
        self.db_manager = ProteinDatabaseManager()
    
    def render_search_interface(self):
        """渲染搜索界面"""
        st.markdown("## 🔍 蛋白质数据库搜索")
        
        # 搜索表单
        with st.form("protein_search_form"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                protein_name = st.text_input(
                    "蛋白质名称",
                    placeholder="例如: insulin, p53, GFP",
                    help="输入蛋白质的通用名称或基因名称"
                )
            
            with col2:
                organism = st.selectbox(
                    "生物体",
                    ["全部", "Homo sapiens", "Mus musculus", "Escherichia coli", "Saccharomyces cerevisiae"],
                    help="选择特定的生物体"
                )
            
            search_button = st.form_submit_button("🔍 搜索", use_container_width=True)
        
        # 搜索结果显示
        if search_button and protein_name:
            self._handle_search(protein_name, organism)
        
        # 热门蛋白质推荐
        self._render_popular_proteins()
    
    def _handle_search(self, protein_name: str, organism: str):
        """处理搜索请求"""
        with st.spinner("正在搜索蛋白质数据库..."):
            # 转换生物体名称
            organism_filter = None if organism == "全部" else organism
            
            # 执行搜索
            results = self.db_manager.search_protein_by_name(protein_name, organism_filter or "")
            
            if results:
                st.success(f"找到 {len(results)} 个相关蛋白质")
                self._display_search_results(results)
            else:
                st.warning("未找到相关蛋白质，请尝试其他关键词")
    
    def _display_search_results(self, results: list[ProteinInfo]):
        """显示搜索结果"""
        # 创建结果表格
        df_data = []
        for protein in results:
            df_data.append({
                "UniProt ID": protein.uniprot_id,
                "蛋白质名称": protein.name[:50] + "..." if len(protein.name) > 50 else protein.name,
                "生物体": protein.organism,
                "序列长度": protein.length,
                "分子量 (Da)": f"{protein.molecular_weight:.0f}" if protein.molecular_weight else "N/A",
                "PDB结构": len(protein.pdb_ids),
                "AlphaFold": "是" if protein.alphafold_id else "否"
            })
        
        df = pd.DataFrame(df_data)
        
        # 显示表格
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "UniProt ID": st.column_config.TextColumn(
                    "UniProt ID",
                    help="点击查看详细信息"
                ),
                "蛋白质名称": st.column_config.TextColumn(
                    "蛋白质名称",
                    width="medium"
                ),
                "生物体": st.column_config.TextColumn(
                    "生物体",
                    width="small"
                ),
                "序列长度": st.column_config.NumberColumn(
                    "序列长度",
                    format="%d"
                ),
                "分子量 (Da)": st.column_config.TextColumn(
                    "分子量",
                    width="small"
                ),
                "PDB结构": st.column_config.NumberColumn(
                    "PDB结构数",
                    format="%d"
                ),
                "AlphaFold": st.column_config.TextColumn(
                    "AlphaFold",
                    width="small"
                )
            }
        )
        
        # 详细查看按钮
        if len(results) > 0:
            st.markdown("### 📋 选择蛋白质进行详细分析")
            
            selected_protein = st.selectbox(
                "选择蛋白质",
                options=range(len(results)),
                format_func=lambda x: f"{results[x].name} ({results[x].uniprot_id})",
                key="protein_selection"
            )
            
            if st.button("🔬 详细分析", use_container_width=True):
                self._analyze_protein(results[selected_protein])
    
    def _analyze_protein(self, protein: ProteinInfo):
        """分析选中的蛋白质"""
        st.session_state['selected_protein'] = protein
        st.session_state['protein_sequence'] = protein.sequence
        st.success(f"已选择蛋白质: {protein.name}")
        
        # 显示蛋白质基本信息
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("UniProt ID", protein.uniprot_id)
            st.metric("序列长度", f"{protein.length} 氨基酸")
        
        with col2:
            st.metric("分子量", f"{protein.molecular_weight:.0f} Da" if protein.molecular_weight else "N/A")
            st.metric("PDB结构数", len(protein.pdb_ids))
        
        with col3:
            st.metric("AlphaFold结构", "可用" if protein.alphafold_id else "不可用")
            st.metric("生物体", protein.organism)
        
        # 显示序列
        st.markdown("### 🧬 蛋白质序列")
        st.code(protein.sequence, language="text")
        
        # 显示功能描述
        if protein.function:
            st.markdown("### 📝 功能描述")
            st.info(protein.function)
        
        # 显示相关结构
        if protein.pdb_ids:
            st.markdown("### 🏗️ 相关PDB结构")
            for pdb_id in protein.pdb_ids[:5]:  # 只显示前5个
                st.markdown(f"- [{pdb_id}](https://www.rcsb.org/structure/{pdb_id})")
        
        # 自动填充到预测表单
        if st.button("🚀 使用此序列进行预测", use_container_width=True):
            st.session_state['protein_sequence'] = protein.sequence
            st.session_state['protein_name'] = protein.name
            st.rerun()
    
    def _render_popular_proteins(self):
        """渲染热门蛋白质推荐"""
        st.markdown("---")
        st.markdown("### 🌟 热门蛋白质")
        
        if st.button("🔄 加载热门蛋白质", use_container_width=True):
            with st.spinner("加载热门蛋白质..."):
                popular_proteins = self.db_manager.get_popular_proteins()
                
                if popular_proteins:
                    st.success(f"加载了 {len(popular_proteins)} 个热门蛋白质")
                    
                    # 显示热门蛋白质列表
                    for i, protein in enumerate(popular_proteins):
                        with st.expander(f"{protein.name} ({protein.uniprot_id})"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.write(f"**生物体**: {protein.organism}")
                                st.write(f"**序列长度**: {protein.length} 氨基酸")
                                st.write(f"**分子量**: {protein.molecular_weight:.0f} Da" if protein.molecular_weight else "**分子量**: N/A")
                            
                            with col2:
                                if st.button(f"选择", key=f"select_popular_{i}"):
                                    st.session_state['protein_sequence'] = protein.sequence
                                    st.session_state['protein_name'] = protein.name
                                    st.success(f"已选择: {protein.name}")
                                    st.rerun()

def main():
    """主函数"""
    st.set_page_config(
        page_title="蛋白质数据库搜索",
        page_icon="🔍",
        layout="wide"
    )
    
    # 页面标题
    st.title("🔍 ProteinFoldDAO 数据库搜索")
    st.markdown("搜索全球最大的蛋白质数据库，获取详细的蛋白质信息")
    
    # 创建搜索界面
    search_interface = DatabaseSearchInterface()
    search_interface.render_search_interface()
    
    # 侧边栏信息
    with st.sidebar:
        st.markdown("### 📊 数据库信息")
        st.info("""
        **UniProt**: 2.5亿+蛋白质序列
        **PDB**: 20万+3D结构
        **AlphaFold**: 2.14亿预测结构
        """)
        
        st.markdown("### 💡 搜索提示")
        st.markdown("""
        - 使用蛋白质的通用名称
        - 可以搜索基因名称
        - 支持部分匹配
        - 选择特定生物体缩小范围
        """)

if __name__ == "__main__":
    main()
