#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProteinFoldDAO Streamlit 前端应用
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

# 添加AI模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai'))
from predictor import ProteinFoldingPredictor

# 页面配置
st.set_page_config(
    page_title="ProteinFoldDAO",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GitHub风格CSS样式
st.markdown("""
<style>
    /* GitHub风格主题 */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    
    .main-header {
        text-align: center;
        color: #58a6ff;
        margin-bottom: 2rem;
        font-weight: 600;
        font-size: 2.5rem;
        text-shadow: 0 0 10px rgba(88, 166, 255, 0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #7d8590;
        margin-bottom: 3rem;
        font-size: 1.1rem;
    }
    
    .prediction-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .prediction-card:hover {
        border-color: #58a6ff;
        box-shadow: 0 8px 15px rgba(88, 166, 255, 0.2);
    }
    
    .success-message {
        background-color: #0d4429;
        border: 1px solid #238636;
        color: #7ee787;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .error-message {
        background-color: #490202;
        border: 1px solid #da3633;
        color: #f85149;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .warning-message {
        background-color: #3c2415;
        border: 1px solid #d29922;
        color: #f0c674;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .info-message {
        background-color: #0c2d6b;
        border: 1px solid #1f6feb;
        color: #79c0ff;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .blockchain-info {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        color: #e6edf3;
        font-size: 0.9rem;
    }
    
    .metric-container {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        color: #58a6ff;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .metric-label {
        color: #7d8590;
        font-size: 0.9rem;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background-color: #238636;
        color: white;
        border: 1px solid #238636;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #2ea043;
        border-color: #2ea043;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* 输入框样式 */
    .stTextArea > div > div > textarea {
        background-color: #0d1117;
        border: 1px solid #30363d;
        color: #e6edf3;
        border-radius: 6px;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1);
    }
    
    /* 选择框样式 */
    .stSelectbox > div > div {
        background-color: #0d1117;
        border: 1px solid #30363d;
        color: #e6edf3;
        border-radius: 6px;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background-color: #0d1117;
    }
    
    .css-1d391kg .stMarkdown {
        color: #e6edf3;
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #161b22;
        border-bottom: 1px solid #30363d;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #7d8590;
        border-radius: 6px 6px 0 0;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        color: #58a6ff;
        background-color: #0d1117;
        border-bottom: 2px solid #58a6ff;
    }
    
    /* 代码块样式 */
    .stCode {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        color: #e6edf3;
    }
    
    /* 进度条样式 */
    .stProgress > div > div > div > div {
        background-color: #238636;
    }
    
    /* 图表容器样式 */
    .stImage {
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 0.5rem;
        background-color: #161b22;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .prediction-card {
            padding: 1rem;
        }
    }
    
    /* 滚动条样式 */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0d1117;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #484f58;
    }
</style>
""", unsafe_allow_html=True)

class BlockchainManager:
    """区块链交互管理器"""
    
    def __init__(self):
        self.contract_address = "0x742d35Cc6634C0532925a3b8D2C5C5C5C5C5C5C5"  # 示例地址
        self.network_id = 11155111  # Sepolia
        self.rpc_url = "https://sepolia.infura.io/v3/YOUR_PROJECT_ID"
        
    def get_contract_abi(self):
        """获取合约ABI"""
        return [
            {
                "inputs": [
                    {"internalType": "string", "name": "_sequence", "type": "string"},
                    {"internalType": "uint256", "name": "_stabilityScore", "type": "uint256"}
                ],
                "name": "submitPrediction",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "_predictionId", "type": "uint256"}],
                "name": "vote",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "_predictionId", "type": "uint256"}],
                "name": "getPrediction",
                "outputs": [
                    {
                        "components": [
                            {"internalType": "uint256", "name": "id", "type": "uint256"},
                            {"internalType": "address", "name": "submitter", "type": "address"},
                            {"internalType": "string", "name": "sequence", "type": "string"},
                            {"internalType": "uint256", "name": "stabilityScore", "type": "uint256"},
                            {"internalType": "uint256", "name": "voteCount", "type": "uint256"},
                            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                            {"internalType": "bool", "name": "isValid", "type": "bool"}
                        ],
                        "internalType": "struct ProteinFoldingDAO.Prediction",
                        "name": "prediction",
                        "type": "tuple"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getAllPredictionIds",
                "outputs": [{"internalType": "uint256[]", "name": "ids", "type": "uint256[]"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getStats",
                "outputs": [
                    {"internalType": "uint256", "name": "totalPredictions", "type": "uint256"},
                    {"internalType": "uint256", "name": "totalVotes", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
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
        # 示例数据 - 显示有意义的蛋白质信息
        example_predictions = [
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
        
        # 初始化session state
        if 'user_predictions' not in st.session_state:
            st.session_state.user_predictions = []
        
        # 合并示例数据和用户提交的预测，按时间排序
        all_predictions = example_predictions + st.session_state.user_predictions
        all_predictions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return all_predictions

def display_prediction_result(result):
    """显示预测结果"""
    if "error" in result:
        st.markdown(f"""
        <div class="error-message">
            <strong>❌ 预测失败:</strong> {result['error']}
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div class="success-message">
        <strong>✅ AI预测完成!</strong> 蛋白折叠分析已成功完成
    </div>
    """, unsafe_allow_html=True)
    
    # 创建两列布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 预测结果")
        
        # GitHub风格的指标卡片
        metrics_data = [
            ("稳定性分数", f"{result['stability_score']:.3f}", "🎯"),
            ("序列长度", f"{result['sequence_length']} 氨基酸", "📏"),
            ("分子量", f"{result['molecular_weight']:.2f} Da", "⚖️"),
            ("不稳定性指数", f"{result['instability_index']:.2f}", "📊"),
            ("疏水性", f"{result['hydrophobicity']:.3f}", "💧"),
            ("电荷平衡", f"{result['charge_balance']:.3f}", "⚡")
        ]
        
        for label, value, icon in metrics_data:
            st.markdown(f"""
            <div class="metric-container">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="metric-label">{icon} {label}</span>
                    <span class="metric-value">{value}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📈 能量路径图")
        if result['energy_plot']:
            # 解码base64图像
            image_data = base64.b64decode(result['energy_plot'])
            image = Image.open(io.BytesIO(image_data))
            st.image(image, caption="蛋白折叠能量路径", use_container_width=True)
        else:
            st.markdown("""
            <div class="warning-message">
                <strong>⚠️ 警告:</strong> 能量图生成失败
            </div>
            """, unsafe_allow_html=True)

def main():
    """主应用函数"""
    
    # 页面标题
    st.markdown('<h1 class="main-header">🧬 ProteinFoldDAO</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">去中心化蛋白折叠预测DAO | Decentralized Protein Folding Prediction DAO</p>', unsafe_allow_html=True)
    
    # GitHub风格徽章
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <img src="https://img.shields.io/badge/AI-Bioinformatics-blue?style=for-the-badge&logo=python" alt="AI">
        <img src="https://img.shields.io/badge/Blockchain-Ethereum-purple?style=for-the-badge&logo=ethereum" alt="Blockchain">
        <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
        <img src="https://img.shields.io/badge/Status-Beta-orange?style=for-the-badge" alt="Status">
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化组件
    predictor = ProteinFoldingPredictor()
    blockchain = BlockchainManager()
    
    # 侧边栏
    with st.sidebar:
        st.markdown("## 🔗 区块链状态")
        
        # 模拟MetaMask连接状态
        wallet_connected = st.checkbox("MetaMask已连接", value=False)
        
        if wallet_connected:
            st.markdown("""
            <div class="success-message" style="margin: 0.5rem 0;">
                <strong>✅ 钱包已连接</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="info-message" style="margin: 0.5rem 0;">
                <strong>地址:</strong> 0x742d35...C5C5C5
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-message" style="margin: 0.5rem 0;">
                <strong>⚠️ 请连接MetaMask钱包</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # 显示合约信息
        st.markdown("### 📋 合约信息")
        st.markdown(f"""
        <div class="blockchain-info">
            <strong>地址:</strong> {blockchain.contract_address}<br>
            <strong>网络:</strong> Sepolia ({blockchain.network_id})
        </div>
        """, unsafe_allow_html=True)
        
        # 获取统计信息
        stats = {"totalPredictions": 2, "totalVotes": 23}  # 模拟数据
        
        st.markdown("### 📊 统计信息")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div style="text-align: center;">
                    <div class="metric-value">{stats['totalPredictions']}</div>
                    <div class="metric-label">总预测数</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <div style="text-align: center;">
                    <div class="metric-value">{stats['totalVotes']}</div>
                    <div class="metric-label">总投票数</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 主内容区域
    tab1, tab2, tab3 = st.tabs(["🧬 AI预测", "📋 预测列表", "ℹ️ 关于"])
    
    with tab1:
        st.markdown("## 🧬 蛋白折叠预测")
        
        # 序列输入
        st.markdown("### 📝 输入蛋白序列")
        
        # 示例序列
        example_sequences = {
            "GFP (绿色荧光蛋白)": "MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK",
            "胰岛素": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN",
            "血红蛋白": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR"
        }
        
        selected_example = st.selectbox("选择示例序列:", ["自定义输入"] + list(example_sequences.keys()))
        
        if selected_example == "自定义输入":
            sequence_input = st.text_area(
                "输入氨基酸序列 (单字母代码):",
                height=200,
                placeholder="例如: MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
            )
        else:
            sequence_input = st.text_area(
                "氨基酸序列:",
                value=example_sequences[selected_example],
                height=200
            )
        
        # 预测按钮
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            predict_button = st.button("🚀 开始预测", type="primary", use_container_width=True)
        
        # 执行预测
        if predict_button:
            if not sequence_input.strip():
                st.error("❌ 请输入蛋白序列")
            else:
                with st.spinner("🧠 AI正在分析序列..."):
                    result = predictor.predict_folding(sequence_input)
                
                # 显示结果
                display_prediction_result(result)
                
                # 保存结果到session state
                st.session_state['prediction_result'] = result
                st.session_state['sequence_input'] = sequence_input
        
        # 提交到区块链
        if 'prediction_result' in st.session_state and 'error' not in st.session_state['prediction_result']:
            st.markdown("---")
            st.markdown("### 🔗 提交到DAO")
            
            if not wallet_connected:
                st.warning("⚠️ 请先连接MetaMask钱包")
            else:
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    submit_button = st.button("📤 提交预测", type="secondary", use_container_width=True)
                
                if submit_button:
                    result = st.session_state['prediction_result']
                    stability_score_scaled = int(result['stability_score'] * 1000)
                    
                    with st.spinner("⛓️ 正在提交到区块链..."):
                        submission_result = blockchain.submit_prediction_simulation(
                            st.session_state['sequence_input'],
                            stability_score_scaled
                        )
                    
                    if submission_result['success']:
                        st.success("✅ 预测已成功提交到DAO!")
                        st.markdown(f"""
                        <div class="blockchain-info">
                        <strong>交易哈希:</strong> {submission_result['tx_hash']}<br>
                        <strong>区块号:</strong> {submission_result['block_number']}<br>
                        <strong>Gas使用:</strong> {submission_result['gas_used']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 添加跳转到预测列表的提示
                        st.info("💡 点击上方的 '📋 预测列表' 标签查看您刚提交的预测！")
                        
                        # 自动切换到预测列表标签
                        st.markdown("""
                        <script>
                        setTimeout(function() {
                            // 尝试切换到预测列表标签
                            var tabs = document.querySelectorAll('[data-testid="stTabs"] button');
                            if (tabs.length > 1) {
                                tabs[1].click();
                            }
                        }, 2000);
                        </script>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("❌ 提交失败，请重试")
    
    with tab2:
        st.markdown("## 📋 社区预测列表")
        
        # 添加刷新按钮
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 最新预测")
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
                
                # GitHub风格的预测卡片
                st.markdown(f"""
                <div class="prediction-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h4 style="margin: 0; color: #58a6ff;">🧬 {protein_name}</h4>
                        <div style="display: flex; gap: 1rem;">
                            <span style="color: #7ee787;">🎯 {pred['stabilityScore']/1000:.3f}</span>
                            <span style="color: #f0c674;">🗳️ {pred['voteCount']}</span>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 1rem;">
                        <div style="color: #7d8590; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            <strong>生物体:</strong> {organism}
                        </div>
                        <div style="color: #7d8590; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            <strong>序列长度:</strong> {len(pred['sequence'])} 氨基酸
                        </div>
                        <div style="color: #7d8590; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            <strong>提交时间:</strong> {datetime.fromtimestamp(pred['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}
                        </div>
                        <div style="color: #7d8590; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            <strong>描述:</strong> {description}
                        </div>
                        <div style="color: #7d8590; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            <strong>功能:</strong> {function}
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 1rem;">
                        <div style="color: #7d8590; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            <strong>序列预览:</strong>
                        </div>
                        <div class="blockchain-info" style="font-size: 0.8rem; max-height: 100px; overflow-y: auto;">
                            {pred['sequence'][:100] + "..." if len(pred['sequence']) > 100 else pred['sequence']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 投票区域
                with st.expander(f"🗳️ 对 {protein_name} 进行投票", expanded=False):
                    if wallet_connected:
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
                    else:
                        st.markdown("""
                        <div class="warning-message">
                            <strong>⚠️ 请连接MetaMask钱包进行投票</strong><br>
                            投票需要区块链交互，请确保钱包已连接
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
    
    with tab3:
        st.markdown("## ℹ️ 关于 ProteinFoldDAO")
        
        # 项目愿景卡片
        st.markdown("""
        <div class="prediction-card">
            <h3 style="color: #58a6ff; margin-top: 0;">🎯 项目愿景</h3>
            <p style="color: #e6edf3; line-height: 1.6;">
                ProteinFoldDAO 是一个结合人工智能、生物信息学和区块链技术的开源项目，
                旨在通过AI加速蛋白质结构预测，并利用Ethereum DAO机制实现社区协作与资助。
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 核心功能
        st.markdown("### 🚀 核心功能")
        features = [
            ("AI驱动预测", "输入蛋白序列，输出折叠稳定性分数和能量路径可视化", "🧠"),
            ("DAO协作", "Ethereum智能合约支持提交预测、社区投票和分红机制", "🗳️"),
            ("用户友好UI", "Streamlit前端集成MetaMask钱包，实现端到端交互", "🎨")
        ]
        
        for title, desc, icon in features:
            st.markdown(f"""
            <div class="prediction-card">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
                    <h4 style="margin: 0; color: #58a6ff;">{title}</h4>
                </div>
                <p style="color: #e6edf3; margin: 0; line-height: 1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 技术栈
        st.markdown("### 🛠️ 技术栈")
        tech_stack = {
            "AI/后端": "Python 3.12 + BioPython + PyTorch + Matplotlib",
            "区块链": "Solidity ^0.8.0 + OpenZeppelin + Web3.py",
            "前端": "Streamlit + MetaMask"
        }
        
        for category, techs in tech_stack.items():
            st.markdown(f"""
            <div class="metric-container">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="metric-label"><strong>{category}</strong></span>
                    <span class="metric-value" style="font-size: 0.9rem;">{techs}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 社会影响
        st.markdown("""
        <div class="prediction-card">
            <h3 style="color: #58a6ff; margin-top: 0;">🌍 社会影响</h3>
            <p style="color: #e6edf3; line-height: 1.6;">
                加速绿色生物技术发展，让全球生物黑客和小团队能够民主化设计自定义蛋白，
                无需依赖中心化实验室或高额资金。
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 开源协议和链接
        st.markdown("### 📄 开源协议")
        st.markdown("""
        <div class="success-message">
            <strong>MIT License</strong> - 欢迎贡献和扩展！
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔗 相关链接")
        links = [
            ("GitHub仓库", "https://github.com/your-username/ProteinFoldDAO", "📦"),
            ("项目文档", "https://your-docs-site.com", "📚"),
            ("社区讨论", "https://your-discord.com", "💬")
        ]
        
        for name, url, icon in links:
            st.markdown(f"""
            <div class="info-message">
                <strong>{icon} {name}:</strong> <a href="{url}" style="color: #79c0ff;">{url}</a>
            </div>
            """, unsafe_allow_html=True)
        
        # 版本信息
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #7d8590; font-size: 0.9rem;">
            <strong>版本</strong>: 1.0.0 | <strong>最后更新</strong>: 2024年1月
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
