# VLA / WAM 每日情报 · 2026-10-13 周二

> 数据源：arXiv（18 篇）/ GitHub（25 仓）/ HuggingFace（15 模型）
> 自动生成于 2026-10-13 06:24 UTC · vla-wam-scout


---

## 📌 今日要点

今日VLA/WAM 研究聚焦于个性化操作（Splat2Act）、噪声空间适应（Noise Space Learning）以及基于世界模型的递归自我改进（RSI-Anything），强调从场景到策略的高效迁移与持续进化。基础设施方面，LongLive 提供长视频生成/世界模型/具身 WAM 的工程支撑，而 awesome-vla-wam 与 Awesome-Touch 分别系统梳理了 VLA/WAM 和触觉感知资源，值得重点关注。整体趋势是：世界模型驱动的自适应与自我提升、多模态触觉融合，以及开源工具链的完善。

---

## 📄 新论文（arXiv）

### 重点论文

- **Splat2Act: From Captured Scenes to Personalized VLA Manipulation** `[VLA]`
  - 从捕获场景到个性化VLA操作，解决通用策略在真实环境零成功率问题
  - Xiaomeng Ye, Krishna Jaganathan, Gyubeum Lim, Gunjan Chhablani et al. · [arXiv](https://arxiv.org/abs/2610.13945) · 💬 Project page: https://splat2act.github.io

- **RSI-Anything: Unlocking Recursive Self-Improvement with World Models** `[WorldModel]`
  - 提出领域通用递归自我改进框架，利用世界模型将交互经验转化为持续改进
  - Taoyong Cui, Pinxian Zeng, Wanghan Xu, Hao Xiao et al. · [arXiv](https://arxiv.org/abs/2610.13912) · 💬 Code: https://github.com/Gen-Verse/RSI-Anything

- **SimVTA: Simulation-Grounded Video-Trajectory Alignment for Driving World Action Models** `[WorldModel]`
  - 提出仿真接地视频-轨迹对齐，用于驾驶世界动作模型后训练，提升规划能力。
  - Changhui Jing, Haochen Tian, Hongchen Li, Tianyu Li et al. · [arXiv](https://arxiv.org/abs/2610.13781) · 💬 Project page: https://opendrivelab.com/SimVTA/

- **LAPT-Scale: Scaling Embodied Policies with Latent Action Pre-Training on Human Videos** `[RobotPolicy]`
  - 利用大规模人类视频进行潜在动作预训练，扩展通用机器人策略。
  - Zhiyuan Xiang, Peidong Liu, Mingyang Li, Jiawei Li et al. · [arXiv](https://arxiv.org/abs/2610.13732) · 💬 Accepted at CoRL 2026; 24 pages including appendix

- **Beyond Successful Robot Demonstrations: Learning from Human Interactions and Modeling Failure Dynamics** `[WorldModel]`
  - 利用人类交互与失败动态学习，扩展世界模型对交互动力学的覆盖。
  - Peiyan Tu, Cong Wang, Hanxin Zhu, Xin Jin et al. · [arXiv](https://arxiv.org/abs/2610.13522)

- **Beyond Temporal Proximity: Explanatory World Models for Credit Assignment in Reinforcement Learning** `[WorldModel]`
  - 提出解释性世界模型，超越时间邻近性实现信用分配。
  - Oriol Corcoll, Qiyao Wei, Ciarán Mark Gilligan-Lee · [arXiv](https://arxiv.org/abs/2610.13504)

- **Reflect-VLA: Internalizing Reflective Guidance via Dual-Path On-Policy Self-Distillation for Autonomous Driving** `[VLA]`
  - 提出双路径在线自蒸馏方法，将反思性指导内化到VLA策略，解决RL标量奖励无法识别具体问题。
  - Yuechen Luo, He Chong, Fang Li, Shaoqing Xu et al. · [arXiv](https://arxiv.org/abs/2610.13453)

- **Beyond Actions: Learning Future Operation Targets for Vision-Language-Action Models** `[VLA]`
  - 提出学习未来操作目标作为辅助预测，使VLA模型超越动作预测，提升操作效果。
  - Min Lin, Bokai Zhou, Jianqi Lin, Kaiyuan Yang et al. · [arXiv](https://arxiv.org/abs/2610.13212)

- **Grounded-Dreamer: Robot Learning from World Model Synthetic Data with Physical Grounding** `[WorldModel]`
  - 提出物理接地的世界模型合成数据方法，减少真实数据依赖。
  - Feng Jiang, Shu Chen, Yuanfei Wang, Yuan Li et al. · [arXiv](https://arxiv.org/abs/2610.13164) · 💬 17 pages, 10 figures, 4 tables. Project page: https://fffstrong.github.io/Grounded-Dreamer/

### 全部论文

- **Noise Space Learning for VLA Adaptation** — 提出噪声空间学习，在噪声空间中适应VLA策略，平衡交互、计算与安全 · [2610.13943](https://arxiv.org/abs/2610.13943)
- **Dream to Remember: Continual Steering of Generalist Robot Policies with World Models** — 利用世界模型持续引导通用机器人策略，通过梦境记忆改进演示覆盖 · [2610.13816](https://arxiv.org/abs/2610.13816)
- **SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices** — 提出轻量潜在世界动作模型，使机器人操作在边缘设备上高效运行。 · [2610.13740](https://arxiv.org/abs/2610.13740)
- **JitterVLA: A Replay Benchmark for Motion Quality in VLA-Driven Human-Robot Manipulation** — 提出VLA运动质量回放基准，评估延迟与抖动对操作的影响。 · [2610.13628](https://arxiv.org/abs/2610.13628)
- **RARA: Robust Policy Fine-Tuning through Retrieval-Anchored Representation Alignment for Robotic Manipulation** — 提出检索锚定表示对齐，提升机器人策略少样本微调的鲁棒性。 · [2610.13578](https://arxiv.org/abs/2610.13578)
- **RESCUE: Is This Alarm Worth Acting On? Counterfactual Evaluation of VLA Runtime Monitors** — 提出反事实评估框架，判断VLA运行时警报是否值得响应。 · [2610.13516](https://arxiv.org/abs/2610.13516)
- **Dual-Stream Memory for Vision-Language-Action Policies** — 提出双流记忆表示，分别跟踪执行状态和恢复不可见视觉证据，增强VLA策略的记忆依赖操作。 · [2610.13262](https://arxiv.org/abs/2610.13262)
- **RoleWorld: Knowledge Transfer in World Modeling with Functional Role Abstractions** — 提出功能角色抽象实现世界模型知识迁移，使LLM智能体高效适应相似交互结构的新环境。 · [2610.13172](https://arxiv.org/abs/2610.13172)
- **Forward Dynamics Models** — 提出前向动力学模型，为VLA提供显式监督。 · [2610.13117](https://arxiv.org/abs/2610.13117)

---

## 🐙 开源仓库动态

### ⭐ 强烈建议关注

- **[NVlabs/LongLive](https://github.com/NVlabs/LongLive)** `源码仓` `Python` `⭐2769` 🔄活跃 
  - NVIDIA 长视频生成/世界模型/具身世界动作模型基础设施，含训练推理代码。
- **[baidu-baige/LoongForge](https://github.com/baidu-baige/LoongForge)** `源码仓` `Python` `⭐678` 🔄活跃 
  - 多模态与具身模型训练框架，支持NVIDIA GPU与昆仑XPU，覆盖LLM/VLM/扩散模型。
- **[robocurve/inspect-robots](https://github.com/robocurve/inspect-robots)** `源码仓` `Python` `⭐671` 🔄活跃 
  - 物理AI评估框架，可在任意机械臂/人形上运行LLM/VLA，对接真实与仿真基准。
- **[Noietch/EVA-CLIENT](https://github.com/Noietch/EVA-CLIENT)** `源码仓` `Python` `⭐318` 🔄活跃 
  - 统一框架，支持真实机器人部署、评估与数据采集
- **[UniWAM/UniWAM](https://github.com/UniWAM/UniWAM)** `源码仓` `Python` `⭐120` 🔄活跃 
  - UniWAM官方代码，统一世界-动作模型，结合预测与决策，提供训练与推理实现。
- **[RadixRootMind/RadixQuantVLA](https://github.com/RadixRootMind/RadixQuantVLA)** `源码仓` `Jupyter Notebook` `⭐102` 🔄活跃 
  - 乐高式VLA后训练量化、基准测试与部署统一框架。
- **[FastCrest/tether](https://github.com/FastCrest/tether)** `源码仓` `Python` `⭐86` 🔄活跃 
  - VLA边缘到云部署CLI，支持Jetson/RTX/Apple Silicon/AMD。
- **[gentlefress/OMEGA-0](https://github.com/gentlefress/OMEGA-0)** `源码仓` `Python` `⭐56` 🔄活跃 
  - 潜在预测世界动作模型，用于人形机器人移动操作官方代码。
- **[GehaoZhang6/Grounded-Action-Model](https://github.com/GehaoZhang6/Grounded-Action-Model)** `源码仓` `Python` `⭐39` 🔄活跃 
  - 3D Grounding 基础模型，面向机器人操作，含 arXiv 论文与 Python 实现。
- **[DexForce/UNITAS](https://github.com/DexForce/UNITAS)** `源码仓` `—` `⭐37` 🔄活跃 
  - 官方代码库，3D 原生 World Action Model，用于具身操作。

### 新仓库 / 活跃仓库

- [DravenALG/awesome-vla-wam](https://github.com/DravenALG/awesome-vla-wam) `文档/汇总` `—` `⭐1047` — 收录 VLA 与 WAM 研究论文及资源的精选列表。
- [linchangyi1/Awesome-Touch](https://github.com/linchangyi1/Awesome-Touch) `文档/汇总` `—` `⭐781` — 触觉感知、数据采集、IL/RL/VLA/WM 等主题的精选资源列表。
- [sou350121/VLA-Handbook](https://github.com/sou350121/VLA-Handbook) `文档/汇总` `HTML` `⭐701` — 全中文 VLA 算法工程师学习与面试手册，聚焦机器人挑战。
- [datawhalechina/dive-into-embodied-ai](https://github.com/datawhalechina/dive-into-embodied-ai) `文档/汇总` `Python` `⭐578` — 具身智能入门教程，覆盖World-Model、VLA、强化学习及工程落地全链路。
- [luohongk/Embodied-AI-Daily](https://github.com/luohongk/Embodied-AI-Daily) `文档/汇总` `HTML` `⭐477` — 每日自动更新VLN/VLA/World Model等具身智能arXiv论文列表
- [wadeKeith/Awesome-Embodied-AI](https://github.com/wadeKeith/Awesome-Embodied-AI) `文档/汇总` `Python` `⭐251` — 收录具身智能综述、VLA模型、数据集、模拟器、人形机器人及安全资源，适合入门导航。
- [strands-labs/robots](https://github.com/strands-labs/robots) `源码仓` `Python` `⭐182` — 通过Strands Agents用自然语言控制机器人及物理硬件，提供智能体交互框架。
- [x-zheng16/Awesome-Embodied-AI-Safety](https://github.com/x-zheng16/Awesome-Embodied-AI-Safety) `文档/汇总` `Python` `⭐152` — 具身AI安全综述，覆盖500+论文，系统梳理感知、认知、规划等环节的风险与防御。
- [TingdeLiu/tingdeliu.github.io](https://github.com/TingdeLiu/tingdeliu.github.io) `文档/汇总` `HTML` `⭐116` — 个人研究笔记，涵盖具身智能、视觉语言导航与机器人学习综述。
- [HyperbolicCurve/Awesome-World-Action-Model](https://github.com/HyperbolicCurve/Awesome-World-Action-Model) `文档/汇总` `Python` `⭐37` — 收录 VLA 与 World Action Model 论文和资源的精选列表，持续更新。
- [JethroJames/awesome-robots-icl](https://github.com/JethroJames/awesome-robots-icl) `文档/汇总` `Python` `⭐31` — 机器人上下文学习综述配套资源，汇总方法、数据集与基准。
- [wangskyone/awesome-VLA-WAM](https://github.com/wangskyone/awesome-VLA-WAM) `文档/汇总` `Python` `⭐21` — 精选 VLA 与 World Action Model 阅读清单，涵盖失败检测/纠正与高效 VLA 主题。

---

## 🤗 HuggingFace 新模型

- [marcinnowakwyn/my-embodied-ai](https://huggingface.co/marcinnowakwyn/my-embodied-ai) · ⬇13 · 创建于 2026-10-12
- [SamerAyyad/VLA_Samer_24.09.2026_200eps_policy_ACT_500k](https://huggingface.co/SamerAyyad/VLA_Samer_24.09.2026_200eps_policy_ACT_500k) · ⬇5 · 创建于 2026-10-12
- [Xiaodong/lingbot-vla-2-robotwin-clean-bs512-step2k](https://huggingface.co/Xiaodong/lingbot-vla-2-robotwin-clean-bs512-step2k) · ⬇0 · 创建于 2026-10-13
- [HenryYHW/VLAlert](https://huggingface.co/HenryYHW/VLAlert) · ⬇0 · 创建于 2026-10-13
- [tsangb34/lingbot-vla-v2-6b-droid-open-drawer-5ep](https://huggingface.co/tsangb34/lingbot-vla-v2-6b-droid-open-drawer-5ep) · ⬇0 · 创建于 2026-10-12
- [Fantasyyy/SDUF-Team-Lingbot-vla-2-competition-10k](https://huggingface.co/Fantasyyy/SDUF-Team-Lingbot-vla-2-competition-10k) · ⬇0 · 创建于 2026-10-12
- [MrBean2024/MA-VLA-pi05-shuffle06-mask04](https://huggingface.co/MrBean2024/MA-VLA-pi05-shuffle06-mask04) · ⬇0 · 创建于 2026-10-12
- [MrBean2024/AE-VLA-TG](https://huggingface.co/MrBean2024/AE-VLA-TG) · ⬇0 · 创建于 2026-10-11
- [MrBean2024/AE-VLA-TG-Armattention](https://huggingface.co/MrBean2024/AE-VLA-TG-Armattention) · ⬇0 · 创建于 2026-10-11
- [MrBean2024/AE-VLA-TG-Skilllora](https://huggingface.co/MrBean2024/AE-VLA-TG-Skilllora) · ⬇0 · 创建于 2026-10-11
- [MrBean2024/AE-VLA-full](https://huggingface.co/MrBean2024/AE-VLA-full) · ⬇0 · 创建于 2026-10-11
- [Luffuly/streaming-code-world-model](https://huggingface.co/Luffuly/streaming-code-world-model) · ⬇0 · 创建于 2026-10-11
- [yogaprat/toy-embodied-ai](https://huggingface.co/yogaprat/toy-embodied-ai) · ⬇0 · 创建于 2026-10-13
- [Stephaniedavis1985/embodied-ai](https://huggingface.co/Stephaniedavis1985/embodied-ai) · ⬇0 · 创建于 2026-10-12
- [nigutierrez/embodied-ai](https://huggingface.co/nigutierrez/embodied-ai) · ⬇0 · 创建于 2026-10-12

---

_由 vla-wam-scout 自动生成。arXiv 数据来自 [arXiv.org](https://arxiv.org)，仓库数据来自 [GitHub](https://github.com) 与 [HuggingFace](https://huggingface.co)。_
