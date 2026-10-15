# VLA / WAM 每日情报 · 2026-10-15 周四

> 数据源：arXiv（38 篇）/ GitHub（10 仓）/ HuggingFace（11 模型）
> 自动生成于 2026-10-15 06:40 UTC · vla-wam-scout

> 🗂 去重：论文重复忽略 22 篇；仓库重复忽略 15 个；模型重复忽略 14 个

---

## 📌 今日要点

今日 VLA/WAM 动态聚焦于“世界模型+精确动作”双线：SafeDriveVLA 以导航条件世界模型提升驾驶冲突感知，VITAL 与 Graph-Reweighted BC 则分别从视觉运动映射和人类干预重加权优化操作精度。开源侧，Psi0 推进人形通用智能，opendm 探索开放世界具身基础模型，MindPaw 降低入门门槛。值得关注的方向是：将世界模型预测与干预式学习结合，以提升复杂场景下的动作鲁棒性与泛化能力。

---

## 📄 新论文（arXiv）

### 重点论文

- **SafeDriveVLA: Navigation-Conditioned World Model Dreaming for Conflict-Aware End-to-End Autonomous Driving** `[WorldModel]`
  - 提出导航条件世界模型梦境，实现冲突感知的端到端自动驾驶
  - Shaoyuan Xie, Zihan Zhang, Jingxuan Wang, Jiashu Qu et al. · [arXiv](https://arxiv.org/abs/2610.20609) · 💬 Accepted at CoRL 2026. Project page: https://safedrive-vla.github.io/SafeDriveVLA/

- **VITAL: From Visual Motion to Precise Action** `[WorldModel]`
  - 从视觉运动直接推导动作目标，避免轨迹表示与视觉动态脱节
  - Ao Liang, Youquan Liu, Mingxiao Li, Wei Chow et al. · [arXiv](https://arxiv.org/abs/2610.20604) · 💬 Technical Report; 37 pages, 14 figures, 19 tables; Project Page at https://worldbench.github.io/vital GitHub at https://

- **When Do Discrete Actions Make Good Continuous Controllers?** `[RobotPolicy]`
  - 质疑连续动作参数化共识，探究离散动作在连续控制中的适用条件。
  - Zeji Yi, Soham Dasgupta, Xinyang Zhang, Koushil Sreenath et al. · [arXiv](https://arxiv.org/abs/2610.20429) · 💬 53 pages (12 main text), 19 figures, 12 tables. Project page: https://iscoyizj.github.io/discrete-action-website/

- **PAWA: Panoramic Action-conditioned World Modeling for Multiple Agents** `[WorldModel]`
  - 提出多智能体全景动作条件世界模型，预测视野外的环境变化。
  - Siqi Yang, Yimu Wang, Ziqi Cai, Chengxuan Zhu et al. · [arXiv](https://arxiv.org/abs/2610.20240) · 💬 24 pages. Project page: https://pawa.siki.moe

- **OneLA: Learning Many Worlds from Latent Actions** `[WorldModel]`
  - 从视频学习潜在动作，统一跨域世界模型控制空间
  - Ziyu Zhu, Zhaoxu Sun, Fan Jiang, Chiyu Wang et al. · [arXiv](https://arxiv.org/abs/2610.20160)

- **Atomic-WAM: Execution-Grounded Atomic-Motion Reasoning for World Action Models** `[WorldModel]`
  - 提出原子运动推理，为世界动作模型提供执行接地
  - Shijun Shi, Zhe Liu, Zhi Hou, Yinan Chen et al. · [arXiv](https://arxiv.org/abs/2610.20157)

- **FoveaVLA: Foveation Actions Replace the Wrist Camera in VLAs** `[VLA]`
  - 提出用学习到的注视动作替代腕部相机，外部相机即可获取细节，简化硬件并保持操作精度。
  - Bingao Chen, Lihan Zha, C. Karen Liu, Guy Tevet · [arXiv](https://arxiv.org/abs/2610.20064) · 💬 Project website: https://tml.stanford.edu/FoveaVLA/

- **Complementary Future Token Pruning for World Action Models** `[WorldModel]`
  - 提出无训练的未来帧token剪枝框架，显著降低世界动作模型推理延迟。
  - Baekseung Kim, Junhoo Lee, Sohyeon Hong, Suhyun Jeon et al. · [arXiv](https://arxiv.org/abs/2610.19957)

- **StateCraft: Augmenting Video World Models with Abstract-State Reasoning** `[WorldModel]`
  - 用抽象状态推理增强视频世界模型的长程一致性
  - Lorenzo Venturoli, Nedko Savov, Xi Wang, Marc Pollefeys et al. · [arXiv](https://arxiv.org/abs/2610.19795)

- **Coordi-pi: Coordination-Aware Dual-Hand Action Representation for Bimanual Dexterous Manipulation** `[RobotPolicy]`
  - 提出协调感知的双手动作表示提升灵巧操作
  - Yiming Meng, Yanming Shao, Weijie Shen, Kunyang Lin et al. · [arXiv](https://arxiv.org/abs/2610.19753)

- **ACRO: Actor-Critic Rollout Orchestration** `[VLA]`
  - 提出ACRO演员-评论家编排层，动态决定VLA策略继续或干预，提升成功率。
  - Junhoo Lee, Seungyeon Kim, Baekseung Kim, Minkyu Kim et al. · [arXiv](https://arxiv.org/abs/2610.19677) · 💬 18 pages

- **SPECTRA-VLA: Base-Fine Hyperspectral Token Transfer at Frozen Vision-Language-Action Interfaces** `[VLA]`
  - 提出SPECTRA-VLA，冻结VLA接口下高光谱token迁移，无需重训练实现光谱升级。
  - Chih-Chung Hsu · [arXiv](https://arxiv.org/abs/2610.19651) · 💬 34 pages: 11-page main paper and 23-page supplementary material

- **Back on Track: Deployment-time Policy Improvement via World Model Planning** `[WorldModel]`
  - 部署时用世界模型规划改进策略，无需额外收集数据即可纠错。
  - Colton Crosby, Hao Wang, Mac Schwager, Somil Bansal · [arXiv](https://arxiv.org/abs/2610.19579)

- **VLRLA: Deployment-Time Adaptation of Vision-Language-Action Models through In-Context Reinforcement Learning** `[VLA]`
  - 提出VLRLA，通过上下文强化学习实现VLA模型部署时自适应。
  - Diyuan Shi, Yiqi Tang, Hongyin Zhang, You Wu et al. · [arXiv](https://arxiv.org/abs/2610.19517)

- **Robota-Embed: Unified VLA Embeddings for Robot In-Context Learning and Evolution** `[VLA]`
  - 首个联合编码任务、执行阶段与后续动作的VLA嵌入模型，支持机器人上下文学习与进化。
  - Yunze Liu, Jing Wang, Shenrui Wu, Wenkun He et al. · [arXiv](https://arxiv.org/abs/2610.19495) · 💬 34 pages, 14 figures. Project page: https://robota-ai.github.io/robota-embed/

- **Active Generative Simulation: Meta-Learning What to Simulate for Sim-and-Real Policy Co-Training** `[WorldModel]`
  - 提出主动生成式仿真，元学习决定模拟内容，实现仿真与真实策略协同训练。
  - Liqian Ma, Vaibhav Saxena, Utkarsh Aashu Mishra, Shuo Cheng et al. · [arXiv](https://arxiv.org/abs/2610.19479) · 💬 CoRL 2026

- **PACER: Process-Aware VLA Policy Learning from Human Corrections for Robotic Disassembly** `[VLA]`
  - 提出过程感知VLA策略，利用人类纠正学习机器人拆解的顺序与精确操作。
  - Chang Liu, Sibo Tian, Litian Gong, Zhiwen Fan et al. · [arXiv](https://arxiv.org/abs/2610.19248)

- **Decoupled Drift-Diffusion World Models for Consistent Future Frame Prediction** `[WorldModel]`
  - 提出解耦漂移-扩散世界模型，分别建模确定性与随机未来帧变化。
  - Anton Arapin, Aditya Singh, Yixin Wang, Jun Gao et al. · [arXiv](https://arxiv.org/abs/2610.19212) · 💬 32 pages, 18 figures, 7 tables. Project page: https://anton-arapin.github.io/d3wm-site

- **Imagining Goals with Geometric Horizon Models for Policy Generalization** `[RobotPolicy]`
  - 提出几何地平线模型想象目标，提升离线策略的泛化能力。
  - Daniel Lawson, Dhruv Sreenivas, Adriana Hugessen, Khimya Khetarpal et al. · [arXiv](https://arxiv.org/abs/2610.19129)

- **Action Jets: Learning the Local Shape of the Action-conditioned Data Manifold** `[WorldModel]`
  - 学习动作条件数据流形的局部形状，以加速世界模型的动作评估。
  - Anton Arapin, Chahyon Ku, Bernadette Bucher · [arXiv](https://arxiv.org/abs/2610.19007) · 💬 34 pages, 14 figures, 23 tables. Project page: https://anton-arapin.github.io/action-jets-site

### 全部论文

- **Graph-Reweighted Behavior Cloning with Human Interventions for Precise Robotic Manipulation** — 用图重加权行为克隆处理人类干预数据，提升精细操作精度 · [2610.20504](https://arxiv.org/abs/2610.20504)
- **AdaRSI: On-Demand Recursive Self-Improvement for Embodied Agents** — 提出按需递归自我改进，让具身智能体在长程任务中持续提升 · [2610.20474](https://arxiv.org/abs/2610.20474)
- **Towards Agentic Robots: Model, Data, Environment, and Harness** — 提出智能体机器人框架，整合模型、数据、环境与工具链，实现目标导向编排。 · [2610.20442](https://arxiv.org/abs/2610.20442)
- **Human Demonstrations as Post-Training Data for Any Robot Body: Retargeting the Object, Not the Hand** — 提出以物体为重定向目标，将人类演示用于任意机器人本体的后训练。 · [2610.20351](https://arxiv.org/abs/2610.20351)
- **ObjDream: Guiding Vision-Language-Action Models with Object-Level Understanding and Future State Prediction** — 提出对象级理解与未来状态预测引导VLA模型，提升操作能力 · [2610.20223](https://arxiv.org/abs/2610.20223)
- **Tactile-Guided Robot Learning: From Representation Learning to Foundation Models** — 综述触觉引导的机器人学习，从表征到基础模型 · [2610.20134](https://arxiv.org/abs/2610.20134)
- **MorphAct: Robot Policies Morphing with the Worlds They Act In** — 提出策略参数随交互环境动态调整的机器人策略，提升跨环境泛化能力。 · [2610.20019](https://arxiv.org/abs/2610.20019)
- **Neurosymbolic Learning of Interpretable World Models** — 提出神经符号可解释世界模型，融合符号知识提升表示透明度和规划能力。 · [2610.19955](https://arxiv.org/abs/2610.19955)
- **What Matters for World Modeling in Vision-Language-Action Models?** — 系统分析VLA中世界模型的设计选择与关键因素 · [2610.19825](https://arxiv.org/abs/2610.19825)
- **One-shot Human Video-Guided Adaptation for Vision-Language-Action Models** — 单段人类视频引导VLA快速适应新任务 · [2610.19746](https://arxiv.org/abs/2610.19746)
- **Accelerating VLA Inference with Perturbation Informed Execution** — 提出扰动知情执行，利用动作块内扰动信息加速VLA推理，减少无效执行。 · [2610.19656](https://arxiv.org/abs/2610.19656)
- **Model What Matters: Decision-Guided Selective World Modeling for Language Agents** — 提出决策引导选择性世界建模，聚焦任务相关状态，提升语言智能体RL效率。 · [2610.19642](https://arxiv.org/abs/2610.19642)
- **ForceBench: Benchmarking Force Integration for Robotic Manipulation** — 提出力觉集成基准ForceBench，统一任务与设置以评估VLA力反馈效果。 · [2610.19604](https://arxiv.org/abs/2610.19604)
- **Cracking Mobile Manipulation: From Failure Diagnosis to Agentic Robot System** — 诊断移动操作失败原因，构建智能体系统提升长程任务成功率。 · [2610.19600](https://arxiv.org/abs/2610.19600)
- **Paraphrase Consensus Is Not Self-Consistency: Instruction Reliance and Robustness in VLA Policies** — 揭示VLA策略对指令改写极敏感，提示集成虽提升语言鲁棒性但非自洽性。 · [2610.19438](https://arxiv.org/abs/2610.19438)
- **SonoWorld: Towards Interactive Pose-Controllable Ultrasound World Models** — 提出交互式姿态可控的超声世界模型，为机器人超声策略学习提供仿真环境。 · [2610.19327](https://arxiv.org/abs/2610.19327)
- **End-to-End Vision-Language-Action Policies for Autonomous Lunar Rover Docking** — 提出端到端VLA策略用于月球车自主对接，应对极端光照与感知扰动。 · [2610.19224](https://arxiv.org/abs/2610.19224)
- **Post-Training, Finetuning, and Steering:A Field Guide for Curating Training Data** — 系统梳理VLA模型后训练、微调与引导的数据策展方法，提供实践指南。 · [2610.19143](https://arxiv.org/abs/2610.19143)

---

## 🐙 开源仓库动态

### ⭐ 强烈建议关注

- **[physical-superintelligence-lab/Psi0](https://github.com/physical-superintelligence-lab/Psi0)** `源码仓` `Python` `⭐2864` 🔄活跃 
  - 开源人形机器人VLA基础模型，面向通用移动操作与操作智能。
- **[dexmal/opendm](https://github.com/dexmal/opendm)** `源码仓` `Python` `⭐2304` 🔄活跃 
  - 开放世界具身智能基础模型，支持通用操作与交互。
- **[OpenWAM-Official/OpenWAM](https://github.com/OpenWAM-Official/OpenWAM)** `源码仓` `Python` `⭐1033` 🔄活跃 
  - 开源模块化世界-动作模型预训练框架，系统探索WAM。
- **[FluxVLA/FluxVLA](https://github.com/FluxVLA/FluxVLA)** `源码仓` `Python` `⭐741` 🔄活跃 
  - 一站式VLA工程平台，覆盖数据到真机部署，含模型实现与训练推理代码
- **[xiaomi-research/recogdrive](https://github.com/xiaomi-research/recogdrive)** `源码仓` `Python` `⭐623` 🔄活跃 
  - ReCogDrive强化认知框架，面向端到端自动驾驶，含训练推理代码
- **[OpenWAM/OpenWAM](https://github.com/OpenWAM/OpenWAM)** `源码仓` `Python` `⭐199` 🔄活跃 
  - 斯坦福官方开源，可组合世界-动作模型框架，Python实现。
- **[greenvla/GreenVLA](https://github.com/greenvla/GreenVLA)** `源码仓` `Python` `⭐144` 🔄活跃 
  - Sber团队分阶段VLA模型，面向通用机器人，含论文与代码。

### 新仓库 / 活跃仓库

- [RealXiaoze/humanoid-motion-intelligence](https://github.com/RealXiaoze/humanoid-motion-intelligence) `文档/汇总` `—` `⭐648` — 人形机器人运动智能知识库，收录论文、开源项目、产业与求职信息
- [worldbench/awesome-vla-for-ad](https://github.com/worldbench/awesome-vla-for-ad) `文档/汇总` `HTML` `⭐500` — VLA自动驾驶综述列表，涵盖过去现在未来工作

---

## 🤗 HuggingFace 新模型

- [vorobyovmaxim/embodied-ai](https://huggingface.co/vorobyovmaxim/embodied-ai) · ⬇14 · 创建于 2026-10-13
- [irambv05/embodied-ai](https://huggingface.co/irambv05/embodied-ai) · ⬇12 · 创建于 2026-10-13
- [immarcussantos/study-embodied-ai](https://huggingface.co/immarcussantos/study-embodied-ai) · ⬇11 · 创建于 2026-10-13
- [t0rn0d0/VLA-Delta-robotwin](https://huggingface.co/t0rn0d0/VLA-Delta-robotwin) · ⬇0 · 创建于 2026-10-15
- [t0rn0d0/VLA-Delta-libero](https://huggingface.co/t0rn0d0/VLA-Delta-libero) · ⬇0 · 创建于 2026-10-15
- [mliv/lingbot-vla-v2-arx5-block-fullframe-fixed](https://huggingface.co/mliv/lingbot-vla-v2-arx5-block-fullframe-fixed) · ⬇0 · 创建于 2026-10-15
- [Donghyun1228/ttt-vla-libero-sglp-mlp-decoder-20261015](https://huggingface.co/Donghyun1228/ttt-vla-libero-sglp-mlp-decoder-20261015) · ⬇0 · 创建于 2026-10-15
- [tsangb34/lingbot-vla-v2-6b-droid-pour-water-5ep](https://huggingface.co/tsangb34/lingbot-vla-v2-6b-droid-pour-water-5ep) · ⬇0 · 创建于 2026-10-14
- [SamerAyyad/VLA_Samer_11.10.2026_300eps_policy_SmolVLA](https://huggingface.co/SamerAyyad/VLA_Samer_11.10.2026_300eps_policy_SmolVLA) · ⬇0 · 创建于 2026-10-14
- [t0rn0d0/VLA-Delta-base](https://huggingface.co/t0rn0d0/VLA-Delta-base) · ⬇0 · 创建于 2026-10-14
- [SignalIsPuPuPu/GTA-VLA-pretrain-380k](https://huggingface.co/SignalIsPuPuPu/GTA-VLA-pretrain-380k) · ⬇0 · 创建于 2026-10-14

---

_由 vla-wam-scout 自动生成。arXiv 数据来自 [arXiv.org](https://arxiv.org)，仓库数据来自 [GitHub](https://github.com) 与 [HuggingFace](https://huggingface.co)。_
