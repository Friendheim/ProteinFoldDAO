#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProteinFoldDAO Streamlit 前端应用 - iOS风格设计
集成AI预测、区块链交互和MetaMask钱包
"""

import streamlit as st
import json
import base64
import io
import requests
from PIL import Image
import sys
import os
from datetime import datetime
import time
import streamlit.components.v1 as components

# 页面配置
st.set_page_config(
    page_title="ProteinFoldDAO",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 添加AI模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai'))

# 导入将在main函数中进行

# iOS风格CSS样式
st.markdown("""
<style>
    /* iOS风格主题 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* 主标题 */
    .main-header {
        text-align: center;
        color: #1d1d1f;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        text-align: center;
        color: #6e6e73;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* 卡片样式 */
    .card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .card-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1d1d1f;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0, 122, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
    }
    
    /* 次要按钮 */
    .secondary-button {
        background: rgba(142, 142, 147, 0.12) !important;
        color: #1d1d1f !important;
        box-shadow: none !important;
    }
    
    .secondary-button:hover {
        background: rgba(142, 142, 147, 0.2) !important;
        transform: translateY(-1px);
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 1rem;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 1rem;
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
        color: #6e6e73;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #007AFF;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* 状态指示器 */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .status-connected {
        background: rgba(52, 199, 89, 0.1);
        color: #34C759;
    }
    
    .status-disconnected {
        background: rgba(255, 59, 48, 0.1);
        color: #FF3B30;
    }
    
    /* 预测结果卡片 */
    .prediction-result {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    .metric-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        margin-bottom: 8px;
    }
    
    .metric-item:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    
    .metric-label {
        color: #6e6e73;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    .metric-value {
        color: #1d1d1f;
        font-weight: 600;
        font-size: 1.1rem;
        text-align: right;
    }
    
    /* 预测列表卡片 */
    .prediction-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .prediction-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
    
    /* 成功/错误消息 */
    .success-message {
        background: rgba(52, 199, 89, 0.1);
        color: #34C759;
        padding: 12px 16px;
        border-radius: 12px;
        border-left: 4px solid #34C759;
        margin: 16px 0;
    }
    
    .error-message {
        background: rgba(255, 59, 48, 0.1);
        color: #FF3B30;
        padding: 12px 16px;
        border-radius: 12px;
        border-left: 4px solid #FF3B30;
        margin: 16px 0;
    }
    
    .info-message {
        background: rgba(0, 122, 255, 0.1);
        color: #007AFF;
        padding: 12px 16px;
        border-radius: 12px;
        border-left: 4px solid #007AFF;
        margin: 16px 0;
    }
    
    /* 隐藏Streamlit默认元素 */
    .stApp > header {
        visibility: hidden;
    }
    
    .stApp > div:nth-child(2) > div > div > div {
        padding-top: 1rem;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
    }
</style>
""", unsafe_allow_html=True)

class BlockchainManager:
    """区块链管理器 - 模拟版本"""
    
    def __init__(self):
        self.contract_address = "0x1234567890123456789012345678901234567890"
        self.network = "sepolia"
    
    def submit_prediction_simulation(self, sequence, stability_score, submitter_address="0x742d35Cc6634C0532925a3b8D2C5C5C5C5C5C5C5"):
        """模拟提交预测到区块链"""
        # 在实际部署中，这里会调用Web3.py与智能合约交互
        
        # 初始化session state
        if 'user_predictions' not in st.session_state:
            st.session_state.user_predictions = []
        if 'prediction_counter' not in st.session_state:
            st.session_state.prediction_counter = 100  # 从100开始避免与示例数据冲突
        
        # 添加到用户预测列表
        prediction_id = st.session_state.prediction_counter
        st.session_state.prediction_counter += 1
        
        new_prediction = {
            "id": prediction_id,
            "submitter": submitter_address,
            "sequence": sequence,
            "stabilityScore": int(stability_score * 1000),  # 转换为整数
            "voteCount": 0,
            "timestamp": int(time.time()),
            "isValid": True
        }
        
        st.session_state.user_predictions.append(new_prediction)
        
        return {
            "success": True,
            "tx_hash": "0x" + "".join([f"{i:02x}" for i in os.urandom(32)]),
            "block_number": 12345678,
            "gas_used": 150000
        }
    
    def get_predictions_simulation(self):
        """获取预测列表（包含用户提交的预测）"""
        # 首次将示例数据写入会话，之后保持会话内可变状态以支持投票累积
        if 'example_predictions' not in st.session_state:
            st.session_state.example_predictions = [
                {
                    "id": 1,
                    "submitter": "0x742d35Cc6634C0532925a3b8D2C5C5C5C5C5C5C5",
                    "protein_name": "绿色荧光蛋白 (GFP)",
                    "organism": "Aequorea victoria",
                    "sequence": "MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK",
                    "stabilityScore": 720,
                    "voteCount": 15,
                    "timestamp": int(time.time()) - 3600,
                    "isValid": True,
                    "description": "来自水母的荧光蛋白，在生物成像中广泛应用",
                    "function": "荧光标记蛋白，用于细胞生物学研究"
                },
                {
                    "id": 2,
                    "submitter": "0x1234567890123456789012345678901234567890",
                    "protein_name": "胰岛素",
                    "organism": "Homo sapiens",
                    "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN",
                    "stabilityScore": 680,
                    "voteCount": 8,
                    "timestamp": int(time.time()) - 7200,
                    "isValid": True,
                    "description": "调节血糖水平的重要激素",
                    "function": "促进葡萄糖摄取和糖原合成"
                },
                {
                    "id": 3,
                    "submitter": "0x9b3d35Cc6634C0532925a3b8D2C5C5C5C5C5C5C5C",
                    "protein_name": "p53肿瘤抑制蛋白",
                    "organism": "Homo sapiens",
                    "sequence": "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGPDEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQKTYQGSYGFRLGFLHSGTAKSVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHERCSDSDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCNSSCMGGMNRRPILTIITLEDSSGNLLGRNSFEVRVCACPGRDRRTEEENLRKKGEPHHELPPGSTKRALPNNTSSSPQPKKKPLDGEYFTLQIRGRERFEMFRELNEALELKDAQAGKEPGGSRAHSSHLKSKKGQSTSRHKKLMFKTEGPDSD",
                    "stabilityScore": 750,
                    "voteCount": 23,
                    "timestamp": int(time.time()) - 1800,
                    "isValid": True,
                    "description": "关键的肿瘤抑制蛋白，调节细胞周期和凋亡",
                    "function": "DNA损伤响应和细胞凋亡调控"
                }
            ]
        if 'user_predictions' not in st.session_state:
            st.session_state.user_predictions = []

        # 合并示例数据和用户提交的预测，按时间排序
        all_predictions = st.session_state.example_predictions + st.session_state.user_predictions
        all_predictions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return all_predictions

    def vote_prediction_simulation(self, prediction_id: int) -> bool:
        """为给定预测投票（会话内模拟）"""
        # 在示例预测中查找
        for pred in st.session_state.get('example_predictions', []):
            if pred.get('id') == prediction_id:
                pred['voteCount'] = int(pred.get('voteCount', 0)) + 1
                return True
        # 在用户预测中查找
        for pred in st.session_state.get('user_predictions', []):
            if pred.get('id') == prediction_id:
                pred['voteCount'] = int(pred.get('voteCount', 0)) + 1
                return True
        return False

def display_prediction_result(result):
    """显示预测结果 - iOS风格"""
    if "error" in result:
        st.markdown(f"""
        <div class="error-message">
            <strong>⚠️ 预测失败</strong><br>
            {result['error']}
        </div>
        """, unsafe_allow_html=True)
        return
    
    # 创建结果卡片
    st.markdown("""
    <div class="prediction-result">
        <div class="card-header">
            🧬 预测结果
        </div>
    """, unsafe_allow_html=True)
    
    # 主要指标 - 纵向布局
    st.markdown("### 📊 基础分析")
    
    # 创建两列布局：左侧文字，右侧图片
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # 基础指标 - 纵向排列，减少项目数量
        st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <div class="metric-item">
                <span class="metric-label">序列长度</span>
                <span class="metric-value">{result['sequence_length']} 氨基酸</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">稳定性分数</span>
                <span class="metric-value">{result['stability_score']:.3f}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">分子量</span>
                <span class="metric-value">{result['molecular_weight']:.0f} Da</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">疏水性</span>
                <span class="metric-value">{result['hydrophobicity']:.3f}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">电荷平衡</span>
                <span class="metric-value">{result['charge_balance']:.3f}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">不稳定性指数</span>
                <span class="metric-value">{result['instability_index']:.1f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        # 能量图显示在右侧，与下面图表大小一致
        st.markdown("### 📈 能量路径图")
        if result['energy_plot']:
            try:
                image_data = base64.b64decode(result['energy_plot'])
                image = Image.open(io.BytesIO(image_data))
                # 设置固定尺寸，与下面的图表保持一致
                st.image(image, caption="蛋白折叠能量路径", width=400)
            except:
                st.markdown("""
                <div class="error-message">
                    <strong>⚠️ 能量图显示失败</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-message">
                <strong>📊 能量图生成中...</strong>
            </div>
            """, unsafe_allow_html=True)

        # 3D 结构可视化（使用 3Dmol.js，无需额外 Python 依赖）
        st.markdown("### 🧩 3D 结构可视化")
        # 简要说明
        st.caption("支持直接输入 PDB ID（如: 1CRN）或 UniProt ID 自动加载 AlphaFold 模型")
        col_3d_a, col_3d_b = st.columns([1, 1])
        # 从会话读取默认值
        default_pdb = st.session_state.get('pdb_id_input', '')
        default_uniprot = st.session_state.get('uniprot_id_input', '')
        with col_3d_a:
            pdb_id = st.text_input("PDB ID", key="pdb_id_input", value=default_pdb, placeholder="如: 1CRN")
        with col_3d_b:
            uniprot_id = st.text_input("UniProt ID", key="uniprot_id_input", value=default_uniprot, placeholder="如: P69905")

        # 离线模式与本地文件
        col_off_a, col_off_b = st.columns([1, 1])
        with col_off_a:
            offline_mode = st.checkbox("离线模式（本地渲染）", value=False)
        with col_off_b:
            pdb_file = st.file_uploader("上传本地 PDB 文件", type=["pdb"], accept_multiple_files=False)

        load_3d = st.button("加载 3D 结构", key="load_3d_structure", use_container_width=True)

        def _render_3d_py3dmol(pdb_text: str) -> bool:
            try:
                import py3Dmol  # type: ignore
                from streamlit.components.v1 import html as st_html
                view = py3Dmol.view(width=700, height=430)
                view.addModel(pdb_text, 'pdb')
                view.setStyle({'cartoon': {'color': 'spectrum'}})
                view.zoomTo()
                st_html(view._make_html(), height=450)
                return True
            except Exception:
                return False

        def _render_3d_from_text(pdb_text: str, label: str = ""):
            # 优先使用 py3Dmol（适合离线本地），失败则用前端 3Dmol.js
            if _render_3d_py3dmol(pdb_text):
                if label:
                    st.caption(f"已加载：{label}")
                return
            import streamlit.components.v1 as components
            from json import dumps as _dumps
            pdb_json = _dumps(pdb_text)
            label_json = _dumps(label)
            html = f"""
            <div id=\"viewer3d\" style=\"width:100%; height:400px; position:relative; border-radius:12px; overflow:hidden; background: #f3f6fb;\"></div>
            <div id=\"viewer_msg\" style=\"font-size:12px;color:#6e6e73;margin-top:6px;\"></div>
            <script src=\"https://cdn.jsdelivr.net/npm/3dmol@2.4.0/build/3Dmol-min.js\"></script>
            <script>
              (function(){{
                var container = document.getElementById('viewer3d');
                var msg = document.getElementById('viewer_msg');
                if (!container) return;
                var viewer = $3Dmol.createViewer(container, {{ backgroundColor: 'white' }});
                var pdb = {pdb_json};
                var label = {label_json};
                viewer.addModel(pdb, 'pdb');
                viewer.setStyle({{}}, {{ cartoon: {{ color: 'spectrum' }} }});
                viewer.zoomTo();
                viewer.render();
                msg.textContent = label ? ('已加载：' + label) : '';
              }})();
            </script>
            """
            components.html(html, height=460)

        def _render_3d_view(pdb_id_val: str, uniprot_id_val: str):
            import streamlit.components.v1 as components
            import json as _json
            import requests as _req
            # 先尝试后端抓取，避免前端 CORS/CDN 限制
            urls = []
            if uniprot_id_val:
                uid = uniprot_id_val
                urls += [
                    f"https://alphafold.ebi.ac.uk/files/AF-{uid}-F1-model_v4.pdb",
                    f"https://alphafold.ebi.ac.uk/files/AF-{uid}-F1-model_v3.pdb",
                    f"https://alphafold.ebi.ac.uk/files/AF-{uid}-F1-model_v2.pdb",
                ]
            if pdb_id_val:
                pid = pdb_id_val
                urls = [f"https://files.rcsb.org/download/{pid}.pdb", f"https://files.rcsb.org/view/{pid}.pdb"] + urls

            headers = {"User-Agent": "ProteinFoldDAO/1.0"}
            pdb_text = None
            loaded_label = None
            for u in urls:
                try:
                    resp = _req.get(u, headers=headers, timeout=10)
                    if resp.ok and len(resp.text) > 200:
                        pdb_text = resp.text
                        loaded_label = u
                        break
                except Exception:
                    continue

            if pdb_text:
                _render_3d_from_text(pdb_text, loaded_label or "")
                return

            # 后端抓取失败再尝试前端 3Dmol.download（有些环境允许直连）
            urls_json = _json.dumps(urls)
            viewer_html = f"""
            <div id=\"viewer3d\" style=\"width:100%; height:400px; position:relative; border-radius:12px; overflow:hidden; background: #f3f6fb;\"></div>
            <div id=\"viewer_msg\" style=\"font-size:12px;color:#6e6e73;margin-top:6px;\"></div>
            <script src=\"https://cdn.jsdelivr.net/npm/3dmol@2.4.0/build/3Dmol-min.js\"></script>
            <script>
              (function(){{
                var container = document.getElementById('viewer3d');
                var msg = document.getElementById('viewer_msg');
                if (!container) return;
                var viewer = $3Dmol.createViewer(container, {{ backgroundColor: 'white' }});
                var urls = {urls_json};
                function finish(){{
                  viewer.setStyle({{}}, {{ cartoon: {{ color: 'spectrum' }} }});
                  viewer.zoomTo();
                  viewer.render();
                }}
                function tryAlpha(i){{
                  if(i>=urls.length){{
                    container.innerHTML = '<div style=\'padding:12px;color:#FF3B30;\'>3D结构加载失败：所有候选链接均不可用</div>';
                    return;
                  }}
                  $3Dmol.download(urls[i], viewer, {{}}, function(){{
                    msg.textContent = '已加载：' + urls[i];
                    finish();
                  }}, function(){{ tryAlpha(i+1); }});
                }}
                tryAlpha(0);
              }})();
            </script>
            """
            components.html(viewer_html, height=460)

        # 点击按钮或自动加载（当数据库模块触发 autoload 标记时）
        should_load = load_3d or st.session_state.get('autoload_3d', False)
        if should_load:
            # 离线模式优先：使用上传文件
            if offline_mode and pdb_file is not None:
                try:
                    pdb_text_local = pdb_file.getvalue().decode('utf-8', errors='ignore')
                    if pdb_text_local:
                        _render_3d_from_text(pdb_text_local, label="本地文件")
                        # 清除一次性标记
                        if 'autoload_3d' in st.session_state:
                            st.session_state.pop('autoload_3d')
                        st.stop()
                except Exception as _:
                    st.error("本地 PDB 读取失败，请确认文件编码为文本格式")

            uid_val = (uniprot_id or st.session_state.get('uniprot_id_input', '')).strip().upper()
            pid_val = (pdb_id or st.session_state.get('pdb_id_input', '')).strip().upper()
            # 清除自动加载标记，避免重复渲染
            if 'autoload_3d' in st.session_state:
                st.session_state.pop('autoload_3d')

            if uid_val or pid_val:
                _render_3d_view(pid_val, uid_val)
            else:
                st.info("请输入 PDB ID 或 UniProt ID，或上传本地 PDB 后再点击加载")

        # 若未安装 py3Dmol 而勾选了离线模式，提示安装方式
        if offline_mode:
            try:
                import py3Dmol  # type: ignore
            except Exception:
                st.info("离线渲染建议安装 py3Dmol：pip install py3Dmol。未安装时将尝试在线 3Dmol.js。")
    
    # 检查是否有扩展的蛋白质特性数据
    if 'amino_acid_composition' in result:
        st.markdown("---")
        
        # 扩展分析 - 纵向布局
        st.markdown("### 🧬 详细分析")
        
        # 创建两列布局：左侧分析，右侧图表
        col_analysis, col_charts = st.columns([1, 1])
        
        with col_analysis:
            # 氨基酸类别分布 - 纵向排列，只显示主要类别
            st.markdown("#### 📊 氨基酸类别分布")
            aa_dist = result['amino_acid_distribution']
            # 只显示前4个主要类别
            for i, (category, data) in enumerate(aa_dist.items()):
                if i >= 4:  # 限制显示数量
                    break
                st.markdown(f"""
                <div class="metric-item">
                    <span class="metric-label">{category}</span>
                    <span class="metric-value">{data['percentage']:.1f}% ({data['count']}个)</span>
                </div>
                """, unsafe_allow_html=True)
            
            # 二级结构倾向性 - 纵向排列
            st.markdown("#### 🌀 二级结构倾向性")
            ss_tendency = result['secondary_structure_tendency']
            st.markdown(f"""
            <div class="metric-item">
                <span class="metric-label">α-螺旋倾向</span>
                <span class="metric-value">{ss_tendency['helix_tendency']:.1f}%</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">β-折叠倾向</span>
                <span class="metric-value">{ss_tendency['sheet_tendency']:.1f}%</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">转角倾向</span>
                <span class="metric-value">{ss_tendency['turn_tendency']:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
            
            # 热稳定性分析 - 纵向排列，减少项目
            st.markdown("#### 🔥 稳定性分析")
            thermo = result['thermostability_indicators']
            st.markdown(f"""
            <div class="metric-item">
                <span class="metric-label">热稳定性评分</span>
                <span class="metric-value">{thermo['thermostability_score']:.3f}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">半胱氨酸含量</span>
                <span class="metric-value">{thermo['cysteine_content']:.2f}%</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">无序倾向性</span>
                <span class="metric-value">{result['disorder_tendency']:.3f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col_charts:
            # 氨基酸组成图表
            st.markdown("#### 🧬 氨基酸组成")
            aa_comp = result['amino_acid_composition']
            aa_names = list(aa_comp.keys())
            aa_percentages = [aa_comp[aa]['percentage'] for aa in aa_names]
            
            import pandas as pd
            df_aa = pd.DataFrame({
                '氨基酸': aa_names,
                '含量(%)': aa_percentages
            })
            
            st.bar_chart(df_aa.set_index('氨基酸'))
            
            # 氨基酸类别分布图表
            st.markdown("#### 📊 类别分布图")
            categories = list(aa_dist.keys())
            percentages = [aa_dist[cat]['percentage'] for cat in categories]
            
            df_cat = pd.DataFrame({
                '类别': categories,
                '含量(%)': percentages
            })
            
            st.bar_chart(df_cat.set_index('类别'))
    else:
        st.markdown("""
        <div class="info-message">
            <strong>💡 提示</strong><br>
            请重新运行预测以获取完整的蛋白质特性分析数据。
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    """主应用函数"""
    
    # 页面标题
    st.markdown('<h1 class="main-header">🧬 ProteinFoldDAO</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">去中心化蛋白折叠预测平台</p>', unsafe_allow_html=True)
    
    # 在函数内部导入AI模块
    try:
        from predictor import ProteinFoldingPredictor
        predictor = ProteinFoldingPredictor()
    except ImportError as e:
        st.error(f"无法导入AI模块: {e}")
        st.stop()
    
    # 初始化组件
    blockchain = BlockchainManager()
    
    # 侧边栏 - 钱包状态
    with st.sidebar:
        st.markdown("## 🔗 钱包状态")
        
        # 模拟MetaMask连接状态
        wallet_connected = st.checkbox("连接MetaMask", value=False)
        
        if wallet_connected:
            st.markdown("""
            <div class="status-indicator status-connected">
                <span>●</span>
                <span>已连接</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            **钱包地址:**  
            `0x742d35Cc6634C0532925a3b8D2C5C5C5C5C5C5C5`
            """)
            st.markdown("""
            **网络:** Sepolia测试网
            """)
        else:
            st.markdown("""
            <div class="status-indicator status-disconnected">
                <span>●</span>
                <span>未连接</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 快速操作
        st.markdown("## ⚡ 快速操作")
        if st.button("🔄 刷新数据", key="refresh_sidebar"):
            st.rerun()
        
        if st.button("📊 查看统计", key="stats_sidebar"):
            st.info("统计功能开发中...")
    
    # 主要内容区域
    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs(["🧬 AI预测", "🔍 数据库搜索", "📋 预测列表", "ℹ️ 关于"])
    
    with tab1:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                🧬 蛋白序列预测
            </div>
        """, unsafe_allow_html=True)
        
        # 序列输入
        st.markdown("### 📝 输入蛋白序列")
        
        # 预设序列选择
        preset_sequences = {
            "选择预设序列": "",
            "GFP (绿色荧光蛋白)": "MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK",
            "胰岛素": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN",
            "人血清白蛋白": "MKWVTFISLLFLFSSAYSRGVFRRDTHKSEIAHRFKDLGEEHFKGLVLIAFSQYLQQCPFDEHVKLVNELTEFAKTCVADESHAGCEKSLHTLFGDELCKVASLRETYGDMADCCEKQEPERNECFLSHKDDSPDLPKLKPDPNTLCDEFKADEKKFWGKYLYEIARRHPYFYAPELLYYANKYNGVFQECCQAEDKGACLLPKIETMREKVLASSARQRLRCASIQKFGERALKAWSVARLSQKFPKAEFVEVTKLVTDLTKVHKECCHGDLLECADDRADLAKYICENQDSISSKLKECCEKPLLEKSHCIAEVENDEMPADLPSLAADFVESKDVCKNYAEAKDVFLGMFLYEYARRHPDYSVVLLLRLAKTYETTLEKCCAAADPHECYAKVFDEFKPLVEEPQNLIKQNCELFEQLGEYKFQNALLVRYTKKVPQVSTPTLVEVSRNLGKVGSKCCKHPEAKRMPCAEDYLSVVLNQLCVLHEKTPVSDRVTKCCTESLVNRRPCFSALTPDETYVPKAFDEKLFTFHADICTLPDTEKQIKKQTALVELLKHKPKATEEQLKTVMENFVAFVDKCCAADDKEACFAVEGPKLVVSTQTALA"
        }
        
        selected_preset = st.selectbox("选择预设序列", list(preset_sequences.keys()))
        
        # 检查是否有从数据库选择的序列
        default_sequence = ""
        if 'protein_sequence' in st.session_state and st.session_state['protein_sequence']:
            default_sequence = st.session_state['protein_sequence']
            # 显示选择的蛋白质信息
            if 'protein_name' in st.session_state:
                col_info, col_clear = st.columns([3, 1])
                with col_info:
                    st.info(f"已选择蛋白质: {st.session_state['protein_name']}")
                with col_clear:
                    if st.button("清除选择", key="clear_selection"):
                        st.session_state.pop('protein_sequence', None)
                        st.session_state.pop('protein_name', None)
                        st.rerun()
        
        if selected_preset != "选择预设序列":
            sequence_input = st.text_area(
                "蛋白序列 (FASTA格式)",
                value=preset_sequences[selected_preset],
                height=120,
                placeholder="输入蛋白序列，例如：MKWVTFISLLFLFSSAYS..."
            )
        else:
            sequence_input = st.text_area(
                "蛋白序列 (FASTA格式)",
                value=default_sequence,
                height=120,
                placeholder="输入蛋白序列，例如：MKWVTFISLLFLFSSAYS..."
            )
        
        # 预测按钮
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            predict_button = st.button("🚀 开始预测", type="primary", use_container_width=True)
        
        # 执行预测
        if predict_button and sequence_input:
            with st.spinner("🧬 AI正在分析蛋白序列..."):
                result = predictor.predict_folding(sequence_input)
                st.session_state['prediction_result'] = result
                st.session_state['sequence_input'] = sequence_input
        
        # 显示预测结果
        if 'prediction_result' in st.session_state:
            display_prediction_result(st.session_state['prediction_result'])
            
            # 提交到DAO按钮
            if st.session_state['prediction_result'] and 'error' not in st.session_state['prediction_result']:
                st.markdown("---")
                st.markdown("### 📤 提交到DAO")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    submit_button = st.button("📤 提交预测到DAO", type="primary", use_container_width=True)
                
                if submit_button:
                    with st.spinner("📤 正在提交到区块链..."):
                        stability_score_scaled = st.session_state['prediction_result']['stability_score']
                        submission_result = blockchain.submit_prediction_simulation(
                            st.session_state['sequence_input'],
                            stability_score_scaled
                        )
                    
                    if submission_result['success']:
                        st.markdown("""
                        <div class="success-message">
                            <strong>✅ 预测已成功提交到DAO!</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="info-message">
                            <strong>交易哈希:</strong> {submission_result['tx_hash']}<br>
                            <strong>区块号:</strong> {submission_result['block_number']}<br>
                            <strong>Gas使用:</strong> {submission_result['gas_used']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.info("💡 点击上方的 '📋 预测列表' 标签查看您刚提交的预测！")
                    else:
                        st.markdown("""
                        <div class="error-message">
                            <strong>❌ 提交失败，请重试</strong>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        # 数据库搜索功能
        st.markdown("""
        <div class="card">
            <div class="card-header">
                🔍 蛋白质数据库搜索
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 使用说明
        st.info("""
        💡 **使用说明**: 
        1. 在下方搜索框中输入蛋白质名称（如：insulin, p53, GFP）
        2. 选择生物体（可选）
        3. 点击"选择"按钮填充序列到预测表单，或点击"预测"按钮直接进行AI分析
        4. 切换到"🧬 AI预测"标签页查看结果
        """)
        
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
            with st.spinner("正在搜索蛋白质数据库..."):
                try:
                    from simple_database_manager import SimpleProteinDatabaseManager
                    db_manager = SimpleProteinDatabaseManager()
                    
                    # 转换生物体名称
                    organism_filter = None if organism == "全部" else organism
                    
                    # 执行搜索
                    results = db_manager.search_protein_by_name(protein_name, organism_filter) # type: ignore
                    
                    if results:
                        st.success(f"找到 {len(results)} 个相关蛋白质")
                        
                        # 显示搜索结果
                        for i, protein in enumerate(results[:5]):  # 只显示前5个
                            with st.expander(f"{protein.name} ({protein.uniprot_id})"):
                                col1 = st.columns(1)[0]
                                with col1:
                                    st.write(f"**生物体**: {protein.organism}")
                                    st.write(f"**序列长度**: {protein.length} 氨基酸")
                                    st.write(f"**分子量**: {protein.molecular_weight:.0f} Da" if protein.molecular_weight else "**分子量**: N/A")
                                    st.write(f"**功能**: {protein.function[:100]}..." if len(protein.function) > 100 else f"**功能**: {protein.function}")
                                    # 显示 PDB ID 列表
                                    pdb_list = getattr(protein, 'pdb_ids', []) or []
                                    pdb_str = ", ".join(pdb_list) if pdb_list else "N/A"
                                    st.write(f"**PDB ID**: {pdb_str}")

                                # 显示蛋白质序列（可复制）
                                st.markdown("---")
                                st.markdown("### 🧬 蛋白质序列")
                                seq_area = st.text_area(
                                    f"序列内容 ({protein.name})",
                                    value=protein.sequence or "",
                                    height=120,
                                    key=f"sequence_display_{i}",
                                )

                                # 序列操作按钮
                                col_copy = st.columns(1)[0]
                                with col_copy:
                                    # 改为前端复制按钮（数据库搜索结果）
                                    from streamlit.components.v1 import html as st_html
                                    copy_uid = f"sr_{i}"
                                    seq_js = (
                                        protein.sequence
                                        .replace('\\', r'\\')
                                        .replace('`', r'\`')
                                        .replace('</', '<\\/')
                                        .replace('\n', ' ')
                                    )
                                    copy_html = """
                                    <div style=\"width:100%; display:flex; gap:8px;\"> 
                                      <button id=\"copy_seq_{uid}\" style=\"
                                        flex:1; display:flex; align-items:center; justify-content:center;
                                        height:44px; background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
                                        color:#fff; border:none; padding:0 16px; border-radius:12px;
                                        font-weight:600; font-size:1rem; box-sizing:border-box;
                                        box-shadow:0 4px 16px rgba(0,122,255,0.3); cursor:pointer;\">📋 复制序列</button>
                                      <button id=\"copy_pdb_{uid}\" style=\"
                                        width:160px; display:flex; align-items:center; justify-content:center;
                                        height:44px; background: rgba(142,142,147,0.12);
                                        color:#1d1d1f; border:none; padding:0 12px; border-radius:12px;
                                        font-weight:600; font-size:0.95rem; box-sizing:border-box; cursor:pointer;\">复制PDB ID</button>
                                    </div>
                                    <script>
                                      (function(){
                                        var b1=document.getElementById('copy_seq_{uid}');
                                        var b2=document.getElementById('copy_pdb_{uid}');
                                        if(b1){
                                          b1.addEventListener('click', function(){
                                            navigator.clipboard.writeText(`{seq}`).then(function(){
                                              var old=b1.innerText; b1.innerText='已复制'; setTimeout(function(){ b1.innerText=old; }, 1200);
                                            });
                                          });
                                        }
                                        if(b2){
                                          b2.addEventListener('click', function(){
                                            navigator.clipboard.writeText('{pdb}').then(function(){
                                              var old=b2.innerText; b2.innerText='已复制'; setTimeout(function(){ b2.innerText=old; }, 1200);
                                            });
                                          });
                                        }
                                      })();
                                    </script>
                                    """.replace('{uid}', copy_uid).replace('{seq}', seq_js).replace('{pdb}', (", ".join(getattr(protein,'pdb_ids',[]) or [])).replace("'","\'").replace("\"","\\\""))
                                    st_html(copy_html, height=70)

                        if len(results) > 5:
                            st.info(f"还有 {len(results) - 5} 个结果，请使用更具体的关键词")
                    
                    else:
                        st.warning("未找到相关蛋白质，请尝试其他关键词")
                
                except Exception as e:
                    st.error(f"搜索出错: {str(e)}")
                    st.info("请确保已安装必要的依赖包")
        
        # 热门蛋白质推荐
        st.markdown("---")
        st.markdown("### 🌟 热门蛋白质")
        
        if st.button("🔄 加载热门蛋白质", use_container_width=True):
            with st.spinner("加载热门蛋白质..."):
                try:
                    from simple_database_manager import SimpleProteinDatabaseManager
                    db_manager = SimpleProteinDatabaseManager()
                    popular_proteins = db_manager.get_popular_proteins()
                    
                    if popular_proteins:
                        st.success(f"加载了 {len(popular_proteins)} 个热门蛋白质")
                        
                        # 显示热门蛋白质列表
                        for i, protein in enumerate(popular_proteins):
                            with st.expander(f"{protein.name} ({protein.uniprot_id})"):
                                col1 = st.columns(1)[0]
                                with col1:
                                    st.write(f"**生物体**: {protein.organism}")
                                    st.write(f"**序列长度**: {protein.length} 氨基酸")
                                    st.write(f"**分子量**: {protein.molecular_weight:.0f} Da" if protein.molecular_weight else "**分子量**: N/A")
                                    # 显示 PDB ID 列表
                                    pdb_list = getattr(protein, 'pdb_ids', []) or []
                                    pdb_str = ", ".join(pdb_list) if pdb_list else "N/A"
                                    st.write(f"**PDB ID**: {pdb_str}")

                                # 显示蛋白质序列（可复制）
                                st.markdown("---")
                                st.markdown("### 🧬 蛋白质序列")
                                seq_area = st.text_area(
                                    f"序列内容 ({protein.name})",
                                    value=protein.sequence or "",
                                    height=120,
                                    key=f"popular_sequence_display_{i}",
                                )

                                # 序列操作按钮
                                col_copy = st.columns(1)[0]
                                with col_copy:
                                    # 改为前端复制按钮（热门蛋白）
                                    from streamlit.components.v1 import html as st_html
                                    copy_uid = f"pop_{i}"
                                    seq_js = (
                                        protein.sequence
                                        .replace('\\', r'\\')
                                        .replace('`', r'\`')
                                        .replace('</', '<\\/')
                                        .replace('\n', ' ')
                                    )
                                    copy_html = """
                                    <div style=\"width:100%; display:flex; gap:8px;\">
                                      <button id=\"copy_seq_{uid}\" style=\"
                                        flex:1; display:flex; align-items:center; justify-content:center;
                                        height:44px; background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
                                        color:#fff; border:none; padding:0 16px; border-radius:12px;
                                        font-weight:600; font-size:1rem; box-sizing:border-box;
                                        box-shadow:0 4px 16px rgba(0,122,255,0.3); cursor:pointer;\">📋 复制序列</button>
                                      <button id=\"copy_pdb_{uid}\" style=\"
                                        width:160px; display:flex; align-items:center; justify-content:center;
                                        height:44px; background: rgba(142,142,147,0.12);
                                        color:#1d1d1f; border:none; padding:0 12px; border-radius:12px;
                                        font-weight:600; font-size:0.95rem; box-sizing:border-box; cursor:pointer;\">复制PDB ID</button>
                                    </div>
                                    <script>
                                      (function(){
                                        var b1=document.getElementById('copy_seq_{uid}');
                                        var b2=document.getElementById('copy_pdb_{uid}');
                                        if(b1){
                                          b1.addEventListener('click', function(){
                                            navigator.clipboard.writeText(`{seq}`).then(function(){
                                              var old=b1.innerText; b1.innerText='已复制'; setTimeout(function(){ b1.innerText=old; }, 1200);
                                            });
                                          });
                                        }
                                        if(b2){
                                          b2.addEventListener('click', function(){
                                            navigator.clipboard.writeText('{pdb}').then(function(){
                                              var old=b2.innerText; b2.innerText='已复制'; setTimeout(function(){ b2.innerText=old; }, 1200);
                                            });
                                          });
                                        }
                                      })();
                                    </script>
                                    """.replace('{uid}', copy_uid).replace('{seq}', seq_js).replace('{pdb}', (", ".join(getattr(protein,'pdb_ids',[]) or [])).replace("'","\'").replace("\"","\\\""))
                                    st_html(copy_html, height=70)
                    
                    else:
                        st.warning("无法加载热门蛋白质")
                
                except Exception as e:
                    st.error(f"加载出错: {str(e)}")
                    st.info("请确保已安装必要的依赖包")
    
    with tab3:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                📋 社区预测列表
            </div>
        """, unsafe_allow_html=True)
        
        # 刷新按钮
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("🔄 刷新", help="刷新预测列表"):
                st.rerun()
        
        # 获取预测列表
        predictions = blockchain.get_predictions_simulation()
        
        if not predictions:
            st.markdown("""
            <div class="info-message">
                <strong>📭 暂无预测数据</strong><br>
                成为第一个提交预测的用户！
            </div>
            """, unsafe_allow_html=True)
        else:
            for pred in predictions:
                # 获取蛋白质信息
                protein_name = pred.get('protein_name', f"蛋白质 #{pred['id']}")
                organism = pred.get('organism', '未知生物体')
                description = pred.get('description', '蛋白质折叠预测')
                function = pred.get('function', '功能未知')
                
                # iOS风格的预测卡片
                st.markdown(f"""
                <div class="prediction-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <h4 style="margin: 0; color: #1d1d1f; font-weight: 600;">🧬 {protein_name}</h4>
                        <div style="display: flex; gap: 16px;">
                            <span style="color: #34C759; font-weight: 600;">🎯 {pred['stabilityScore']/1000:.3f}</span>
                            <span style="color: #007AFF; font-weight: 600;">🗳️ {pred['voteCount']}</span>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 16px;">
                        <div style="color: #6e6e73; font-size: 0.9rem; margin-bottom: 8px;">
                            <strong>生物体:</strong> {organism}
                        </div>
                        <div style="color: #6e6e73; font-size: 0.9rem; margin-bottom: 8px;">
                            <strong>序列长度:</strong> {len(pred['sequence'])} 氨基酸
                        </div>
                        <div style="color: #6e6e73; font-size: 0.9rem; margin-bottom: 8px;">
                            <strong>提交时间:</strong> {datetime.fromtimestamp(pred['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}
                        </div>
                        <div style="color: #6e6e73; font-size: 0.9rem; margin-bottom: 8px;">
                            <strong>描述:</strong> {description}
                        </div>
                        <div style="color: #6e6e73; font-size: 0.9rem; margin-bottom: 12px;">
                            <strong>功能:</strong> {function}
                        </div>
                    </div>
                    
                    <div style="background: rgba(0,0,0,0.02); padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                        <div style="font-family: 'SF Mono', Monaco, monospace; font-size: 0.85rem; color: #1d1d1f; word-break: break-all;">
                            {pred['sequence'][:100]}{'...' if len(pred['sequence']) > 100 else ''}
                        </div>
                    </div>
                    
                    <div style="display: flex; gap: 8px;"></div>
                </div>
                """, unsafe_allow_html=True)

                # 投票区域 - iOS风格
                with st.expander(f"🗳️ 对 {protein_name} 进行投票", expanded=False):
                    st.markdown("**请为这个蛋白质预测投票并说明理由：**")
                    
                    # 投票选项
                    vote_choice = st.radio(
                        "您的投票选择：",
                        ["👍 支持", "👎 反对", "🤔 中立"],
                        key=f"vote_choice_{pred['id']}"
                    )
                    
                    # 投票说明
                    vote_reason = st.text_area(
                        "请说明您的投票理由：",
                        placeholder="例如：这个预测的稳定性分数合理，序列分析准确...",
                        key=f"vote_reason_{pred['id']}"
                    )
                    
                    # 提交投票按钮
                    if st.button(f"提交投票", key=f"submit_vote_{pred['id']}", type="primary"):
                        if vote_reason.strip():
                            st.success(f"✅ 投票成功！您选择了 {vote_choice}，理由：{vote_reason}")
                            st.info("💡 您的投票已记录到区块链，感谢参与社区治理！")
                        else:
                            st.warning("⚠️ 请填写投票理由")
                
                # 交互按钮行（统一宽度）
                c1, c2, _ = st.columns([1, 1, 6])
                with c1:
                    if st.button("👍 快速投票", key=f"quick_vote_{pred['id']}", use_container_width=True):
                        ok = blockchain.vote_prediction_simulation(pred['id'])
                        if ok:
                            st.success("已投票")
                            st.rerun()
                        else:
                            st.error("投票失败")
                with c2:
                    # 使用前端复制到剪贴板（保持与左侧按钮等宽），避免 f-string 花括号冲突
                    uid = pred['id']
                    seq_js = pred['sequence'].replace('\\', r'\\').replace('`', r'\`').replace('</', '<\\/').replace('\n', ' ')
                    html_snippet = """
                    <div style=\"width:100%; height:48px; margin:0; padding:0;\">
                      <button id=\"copy_btn_{uid}\" style=\"
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        width:100%;
                        height:48px;
                        background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
                        color: #ffffff;
                        border: none;
                        padding: 0 24px;
                        border-radius: 12px;
                        font-weight: 600;
                        font-size: 1rem;
                        box-sizing: border-box;
                        box-shadow: 0 4px 16px rgba(0, 122, 255, 0.3);
                        cursor: pointer;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;\">📋 复制序列</button>
                    </div>
                    <script>
                      (function(){{
                        var btn = document.getElementById('copy_btn_{uid}');
                        if (btn){{
                          btn.addEventListener('click', function(){{
                            navigator.clipboard.writeText(`{seq}`).then(function(){{
                              var old = btn.innerText;
                              btn.innerText = '已复制';
                              setTimeout(function(){{ btn.innerText = old; }}, 1200);
                            }});
                          }});
                        }}
                      }})();
                    </script>
                    """.format(uid=uid, seq=seq_js)
                    components.html(html_snippet, height=86)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        # 使用原生组件渲染，避免 HTML 被当作代码显示
        st.markdown("""
        <div class="card">
            <div class="card-header">ℹ️ 关于ProteinFoldDAO</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("""
        **ProteinFoldDAO** 是一个去中心化的蛋白折叠预测平台，结合了人工智能、区块链与社区协作，
        旨在用开放透明的方式推动蛋白质结构与功能研究、应用与普及。
        """)

        # 愿景与使命
        st.subheader("🌍 愿景与使命")
        st.markdown(
            "- **愿景**: 让蛋白质知识成为可被任何人自由使用与验证的公共基础设施。\n"
            "- **使命**: 通过 AI 预测与社区治理，持续改进蛋白质特性评估与知识库质量，缩短科研到应用的距离。"
        )

        # 核心功能
        st.subheader("🎯 核心功能")
        st.markdown(
            "- AI 驱动的蛋白折叠与稳定性多维度分析\n"
            "- 全球蛋白质数据库检索（UniProt, PDB, AlphaFold）\n"
            "- 一键生成可视化（能量路径、组成分布等）\n"
            "- 社区提交/投票/校验，形成可追溯的知识共识\n"
            "- 去中心化存证与可验证的审计轨迹"
        )

        # 工作流
        st.subheader("🔁 系统工作流")
        st.markdown(
            "1. 用户输入或从数据库检索蛋白序列\n"
            "2. 模型进行序列清洗与合法性校验\n"
            "3. 进行特性分析与可视化生成\n"
            "4. 结果可提交到社区列表，接受投票与讨论\n"
            "5. 持续优化模型与结果，沉淀到公共知识库"
        )

        # 数据来源
        st.subheader("📚 数据来源")
        st.markdown(
            "- **UniProt**（蛋白序列/功能注释）\n"
            "- **PDB**（三维结构）\n"
            "- **AlphaFold**（预测结构与置信分数）\n"
            "- 本地缓存与可选扩展数据源"
        )

        # AI 预测说明
        st.subheader("🧠 AI 预测说明与指标")
        st.markdown(
            "- 序列清理与验证（长度/合法字符/边界条件）\n"
            "- 稳定性评分、疏水性、电荷平衡、不稳定性指数\n"
            "- 氨基酸组成与类别分布\n"
            "- 二级结构倾向、无序倾向、热稳定相关指标\n"
            "- 能量路径图（固定尺寸，便于视觉对齐）\n"
            "- 分子量、等电点、柔性指数、平均体积等"
        )

        # 隐私与合规
        st.subheader("🔒 隐私与合规")
        st.markdown(
            "- 仅处理用户主动输入的序列与公开数据源结果\n"
            "- 不收集个人隐私信息；可选的浏览器统计已在本地关闭\n"
            "- 区块链存证仅记录必要摘要信息，避免敏感数据上链"
        )

        # 路线图
        st.subheader("🗺️ 路线图（Roadmap）")
        st.markdown(
            "- 短期：完善数据库检索、指标对齐、前端体验与国际化\n"
            "- 中期：引入结构层级指标、PDB 可视化与更丰富的对比分析\n"
            "- 长期：自治治理、论文与产业合作、标准化接口与插件生态"
        )

        # 社区与治理
        st.subheader("🤝 社区与治理")
        st.markdown(
            "- 任何人都可以提交预测与改进建议\n"
            "- 通过投票与讨论形成共识，促进模型与数据质量迭代\n"
            "- 贡献者将获得公开的可验证贡献记录"
        )

        # 技术栈（保留原有章节并微调）
        st.subheader("🔬 技术栈")
        st.markdown(
            "- **AI 模块**: Python, BioPython, Matplotlib\n"
            "- **数据库**: UniProt API, PDB API, AlphaFold DB\n"
            "- **区块链**: Ethereum, Solidity, Web3.py\n"
            "- **前端**: Streamlit, iOS 风格设计\n"
            "- **部署**: Hardhat, Sepolia 测试网"
        )

        # FAQ
        st.subheader("❓ 常见问题（FAQ）")
        with st.expander("如何输入序列？"):
            st.markdown("将氨基酸序列粘贴到“AI预测”页的文本框，或在数据库中复制。支持大小写，会自动清理空格与无关字符。")
        with st.expander("序列校验不通过怎么办？"):
            st.markdown("检查是否存在非法字符，长度是否在 5–1000 之间；页面会提示具体原因。")
        with st.expander("为什么有些图表或中文字体显示警告？"):
            st.markdown("这是 Matplotlib 在当前字体下对部分字符不支持的警告，不影响核心功能，后续会内置更全面的字体集。")
        with st.expander("如何参与治理？"):
            st.markdown("在“预测列表”中提交/投票并讨论；后续会提供提案与投票的链上治理模块。")

        # 链接区（保留现有按钮）
        st.subheader("🔗 链接")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.link_button("📚 文档", url="https://github.com/Friendheim/ProteinFoldDAO/blob/main/ProteinFoldDAO/README.md", use_container_width=True)
        with col_b:
            st.link_button("🐙 GitHub", url="https://github.com/Friendheim/ProteinFoldDAO/tree/main/ProteinFoldDAO", use_container_width=True)
        with col_c:
            st.link_button("💬 社区", url="http://www.ebi.ac.uk/uniprot/", use_container_width=True)

if __name__ == "__main__":
    main()
