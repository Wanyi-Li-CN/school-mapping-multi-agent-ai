# 🏫 多智能体学校地理空间数据构建系统

> 多智能体AI框架 · 学校地理空间数据自动化采集与标准化

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Coze](https://img.shields.io/badge/Coze-AI_Agent-orange.svg)](https://www.coze.cn/)
[![Paper](https://img.shields.io/badge/论文-FSDM2025-success.svg)](./docs/)
[![Award](https://img.shields.io/badge/获奖-最佳学生论文-red.svg)](./docs/)

---

## 📌 项目简介

中国快速城市化导致教育资源与人口分布出现错配，而研究这一问题的核心瓶颈在于**缺乏标准化的学校地理空间数据**。

本项目提出了一套**多智能体AI框架**，通过三个协作的AI智能体自动化完成学校数据的采集、验证与标准化，并以**中国潮州市638所K-12学校**为案例进行了完整验证。

---

## 🧠 多智能体框架

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      STR        │ -> │      SNSE       │ -> │      SNDE       │
│  学校类型识别    │    │  学校名称标准化  │    │  学校名称去重   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

| 智能体 | 功能 |
|--------|------|
| **STR（学校类型识别）** | 通过关键词提取、地址线索和数据库匹配，自动识别学校类型 |
| **SNSE（学校名称标准化）** | 通过正则匹配、格式统一和括号标准化，规范化学校名称 |
| **SNDE（学校名称去重）** | 通过包含检查与词向量相似度匹配，检测并合并重复记录 |

三个智能体均在 **Coze（扣子）** 平台上部署，形成完整的数据处理流水线。

---

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| AI智能体平台 | Coze（扣子） |
| 地理数据处理 | GeoPandas、Shapely |
| 地图API | 高德地图API、天地图API |
| 卫星影像标注 | LabelMe |
| 数据可视化 | Folium、Leaflet |
| 数据分析 | K-means聚类、t-SNE可视化、Hu矩特征 |
| 开发语言 | Python 3.9+ |

---

## 📊 核心成果

- ✅ 识别潮州市 **638所** K-12学校
- ✅ 原始记录 **856条** → 标准化去重后 **638条**
- ✅ 为每所学校标注**卫星影像边界多边形**
- ✅ 完成学校**占地面积估算**
- ✅ 完成学校**形态特征聚类分析**（K-means，K=8）
- ✅ 完成学校分布与**人口密度对比分析**（覆盖3大行政区）

### 人口与学校分布对比

| 行政区 | 出生人口占比 | 小学占比 | 中学占比 | 结论 |
|--------|-------------|---------|---------|------|
| 潮安区 | 46.78% | 49.7% | 42.7% | ✅ 基本均衡 |
| 饶平县 | 36.48% | 31.8% | 30.0% | ⚠️ 学校相对不足 |
| 湘桥区 | 16.73% | 18.5% | 27.3% | 📍 城区中学集中 |

---

## 🗺️ 可视化成果

> 交互式HTML地图位于 `/outputs` 文件夹

| 学校分布图 | 路线规划图 |
|:---:|:---:|
| ![学校分布图](./outputs/screenshot_map.png) | ![路线图](./outputs/screenshot_route.png) |

---

## 📄 论文与获奖

- 论文发表于 **FSDM 2025**（第11届模糊系统与数据挖掘国际会议）
- 🏆 荣获 **最佳学生论文奖（Best Student Paper Award）**

> 论文与证书详见 `/docs` 文件夹

---

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/万义-李-CN/school-mapping-multi-agent-ai.git

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（请勿提交真实API Key）
# 创建 .env 文件，填入：AMAP_KEY=你的高德地图密钥

# 运行地图生成
python src/自定义城市_schools_map.py
```

---

## 📂 项目结构

```
school-mapping-multi-agent-ai/
├── README.md                # 项目说明
├── requirements.txt         # Python依赖
├── .gitignore               # Git忽略文件
├── src/                     # 源代码
│   ├── 自定义城市_schools_map.py
│   ├── 百度卫星图API_路线提取.py
│   └── 外网的卫星图API_路线提取.py
├── data/                    # 样例数据
│   ├── 潮州市_市.geojson
│   └── sample_schools.csv
├── outputs/                 # 可视化结果
│   ├── 潮州市_schools_map.html
│   ├── 潮州市学校路线图.html
│   ├── screenshot_map.png
│   └── screenshot_route.png
└── docs/                    # 论文与证书
    ├── FSDM2025_paper.pdf
    ├── FSDM2025_certificate.jpg
    ├── 学习报告_卫星图_标记潮汕中学.docx
    └── 学习报告_卫星图_路线提取.docx
```

---

## 👩‍💻 作者

**李万义（Wanyi Li）**  
韩山师范学院 · 计算机与信息工程学院  

📧 3066129214@qq.com

---

## 📝 许可证

MIT