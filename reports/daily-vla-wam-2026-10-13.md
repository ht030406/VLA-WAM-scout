# VLA / WAM 每日情报 · 2026-10-13 周二

> 数据源：arXiv（19 篇）/ GitHub（25 仓）/ HuggingFace（14 模型）
> 自动生成于 2026-10-13 03:57 UTC · vla-wam-scout

---

## 📌 今日要点

今日 VLA/WAM 动态聚焦于个性化操作与高效适应：Splat2Act 从场景重建实现个性化 VLA 操作，Noise Space Learning 则通过噪声空间学习提升 VLA 跨场景适应能力。世界模型驱动自我改进成为亮点，RSI-Anything 利用世界模型实现递归自提升，LongLive 提供长视频生成与具身世界模型基础设施。资源整合加速领域发展，awesome-vla-wam 系统梳理 VLA/WAM 研究脉络，Awesome-Touch 补充触觉感知与数据采集关键模块。

---

## 📄 新论文（arXiv）

### 重点论文

- **Splat2Act: From Captured Scenes to Personalized VLA Manipulation** `[VLA]`
  - 利用捕获场景重建实现个性化VLA操作，解决通用策略在真实环境零成功率问题
  - Xiaomeng Ye, Krishna Jaganathan, Gyubeum Lim, Gunjan Chhablani et al. · [arXiv](https://arxiv.org/abs/2610.13945) · 💬 Project page: https://splat2act.github.io

- **RSI-Anything: Unlocking Recursive Self-Improvement with World Models** `[WorldModel]`
  - 提出通用递归自我改进框架，用世界模型降低外部反馈依赖，实现持续提升
  - Taoyong Cui, Pinxian Zeng, Wanghan Xu, Hao Xiao et al. · [arXiv](https://arxiv.org/abs/2610.13912) · 💬 Code: https://github.com/Gen-Verse/RSI-Anything

- **SimVTA: Simulation-Grounded Video-Trajectory Alignment for Driving World Action Models** `[WorldModel]`
  - 提出SimVTA，通过模拟接地视频-轨迹对齐提升驾驶世界动作模型的规划性能。
  - Changhui Jing, Haochen Tian, Hongchen Li, Tianyu Li et al. · [arXiv](https://arxiv.org/abs/2610.13781) · 💬 Project page: https://opendrivelab.com/SimVTA/

- **SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices** `[WorldModel]`
  - 提出SmolWAM，轻量级潜在世界动作模型，实现边缘设备上的机器人操作预测。
  - Timi Owolabi, Hikmah Olawore, Frances Adelakun, Ayotomiwa Oyewumi · [arXiv](https://arxiv.org/abs/2610.13740) · 💬 Accepted at the NeurIPS 2026 Robot Learning with World Models Workshop. Code: https://github.com/iitimii/SmolWAM Project

- **Beyond Successful Robot Demonstrations: Learning from Human Interactions and Modeling Failure Dynamics** `[WorldModel]`
  - 从人类交互中学习并建模失败动态，扩展世界模型对交互多样性的覆盖。
  - Peiyan Tu, Cong Wang, Hanxin Zhu, Xin Jin et al. · [arXiv](https://arxiv.org/abs/2610.13522)

- **Beyond Temporal Proximity: Explanatory World Models for Credit Assignment in Reinforcement Learning** `[WorldModel]`
  - 提出解释性世界模型，基于因果相关性而非时间邻近进行强化学习信用分配。
  - Oriol Corcoll, Qiyao Wei, Ciarán Mark Gilligan-Lee · [arXiv](https://arxiv.org/abs/2610.13504)

- **Reflect-VLA: Internalizing Reflective Guidance via Dual-Path On-Policy Self-Distillation for Autonomous Driving** `[VLA]`
  - 提出双路径在线自蒸馏，将反思性引导内化到驾驶VLA策略中。
  - Yuechen Luo, He Chong, Fang Li, Shaoqing Xu et al. · [arXiv](https://arxiv.org/abs/2610.13453)

- **Beyond Actions: Learning Future Operation Targets for Vision-Language-Action Models** `[VLA]`
  - 引入未来操作目标预测，超越动作块以增强VLA策略学习。
  - Min Lin, Bokai Zhou, Jianqi Lin, Kaiyuan Yang et al. · [arXiv](https://arxiv.org/abs/2610.13212)

- **Grounded-Dreamer: Robot Learning from World Model Synthetic Data with Physical Grounding** `[WorldModel]`
  - 提出Grounded-Dreamer，利用物理接地的世界模型合成数据训练机器人策略。
  - Feng Jiang, Shu Chen, Yuanfei Wang, Yuan Li et al. · [arXiv](https://arxiv.org/abs/2610.13164) · 💬 17 pages, 10 figures, 4 tables. Project page: https://fffstrong.github.io/Grounded-Dreamer/

- **Forward Dynamics Models** `[WorldModel]`
  - 提出前向动力学模型，为VLA和WAM提供显式监督以提升策略学习。
  - Zipei Ma, Junzhe Jiang, Jiahui Zhang, Juntong Zhang et al. · [arXiv](https://arxiv.org/abs/2610.13117) · 💬 Project page: https://logosroboticsgroup.github.io/FDM/

### 全部论文

- **Noise Space Learning for VLA Adaptation** — 提出噪声空间学习，在有限交互下高效适配VLA策略，兼顾计算与安全约束 · [2610.13943](https://arxiv.org/abs/2610.13943)
- **Dream to Remember: Continual Steering of Generalist Robot Policies with World Models** — 用世界模型持续引导通用策略，突破演示数据质量与覆盖限制 · [2610.13816](https://arxiv.org/abs/2610.13816)
- **LAPT-Scale: Scaling Embodied Policies with Latent Action Pre-Training on Human Videos** — 利用人类视频进行潜在动作预训练，扩展具身策略的规模。 · [2610.13732](https://arxiv.org/abs/2610.13732)
- **JitterVLA: A Replay Benchmark for Motion Quality in VLA-Driven Human-Robot Manipulation** — 提出JitterVLA基准，评估VLA策略在延迟抖动下的运动质量。 · [2610.13628](https://arxiv.org/abs/2610.13628)
- **RARA: Robust Policy Fine-Tuning through Retrieval-Anchored Representation Alignment for Robotic Manipulation** — 通过检索锚定表示对齐实现机器人操作策略的鲁棒微调，提升少样本适应能力。 · [2610.13578](https://arxiv.org/abs/2610.13578)
- **RESCUE: Is This Alarm Worth Acting On? Counterfactual Evaluation of VLA Runtime Monitors** — 反事实评估VLA运行时监控器，判断警报是否值得响应，考虑时机与干预成本。 · [2610.13516](https://arxiv.org/abs/2610.13516)
- **Dual-Stream Memory for Vision-Language-Action Policies** — 提出双流记忆架构，分别跟踪执行状态并恢复不可见视觉证据。 · [2610.13262](https://arxiv.org/abs/2610.13262)
- **RoleWorld: Knowledge Transfer in World Modeling with Functional Role Abstractions** — 用功能角色抽象实现世界模型跨环境知识迁移，提升泛化。 · [2610.13172](https://arxiv.org/abs/2610.13172)
- **What Visual Representations Do World Action Models Need?** — 研究世界动作模型所需视觉表示，发现外部表示优于VAE重建表示。 · [2610.13024](https://arxiv.org/abs/2610.13024)

---

## 🐙 开源仓库动态

### ⭐ 强烈建议关注

- **[NVlabs/LongLive](https://github.com/NVlabs/LongLive)** `源码仓` `Python` `⭐2768` 🔄活跃 
  - NVIDIA官方长视频生成/世界模型/具身世界动作模型基础设施，含可运行源码
- **[baidu-baige/LoongForge](https://github.com/baidu-baige/LoongForge)** `源码仓` `Python` `⭐678` 🔄活跃 
  - 高性能训练框架，支持LLM/VLM/扩散及具身模型，适配NVIDIA GPU与昆仑XPU。
- **[robocurve/inspect-robots](https://github.com/robocurve/inspect-robots)** `源码仓` `Python` `⭐671` 🔄活跃 
  - 物理AI评估工具，可在任意机械臂/人形上运行LLM/VLA，对接真实与仿真基准。
- **[Noietch/EVA-CLIENT](https://github.com/Noietch/EVA-CLIENT)** `源码仓` `Python` `⭐317` 🔄活跃 
  - 统一框架，支持真实机器人部署、评估与数据采集，可对接 VLA 模型
- **[strands-labs/robots](https://github.com/strands-labs/robots)** `源码仓` `Python` `⭐182` 🔄活跃 
  - 通过Strands Agents用自然语言控制机器人及物理硬件。
- **[UniWAM/UniWAM](https://github.com/UniWAM/UniWAM)** `源码仓` `Python` `⭐120` 🔄活跃 
  - UniWAM统一世界-动作模型的官方实现代码。
- **[RadixRootMind/RadixQuantVLA](https://github.com/RadixRootMind/RadixQuantVLA)** `源码仓` `Jupyter Notebook` `⭐101` 🔄活跃 
  - VLA量化与部署的乐高式统一框架，支持后训练量化与基准测试。
- **[FastCrest/tether](https://github.com/FastCrest/tether)** `源码仓` `Python` `⭐86` 🔄活跃 
  - VLA模型边缘到云部署CLI，支持Jetson/RTX/Apple Silicon等多平台。
- **[gentlefress/OMEGA-0](https://github.com/gentlefress/OMEGA-0)** `源码仓` `Python` `⭐56` 🔄活跃 
  - ω-0潜在预测世界动作模型，用于人形机器人移动操作。
- **[DexForce/UNITAS](https://github.com/DexForce/UNITAS)** `源码仓` `—` `⭐35` 🔄活跃 
  - 3D原生世界动作模型Unitas官方代码，面向具身操作

### 新仓库 / 活跃仓库

- [DravenALG/awesome-vla-wam](https://github.com/DravenALG/awesome-vla-wam) `文档/汇总` `—` `⭐1047` — 收录VLA与WAM研究的精选列表，涵盖机器人具身智能方向
- [linchangyi1/Awesome-Touch](https://github.com/linchangyi1/Awesome-Touch) `文档/汇总` `—` `⭐781` — 触觉感知与操作资源列表，涵盖VLA/WM在触觉中的应用
- [sou350121/VLA-Handbook](https://github.com/sou350121/VLA-Handbook) `文档/汇总` `HTML` `⭐701` — 全中文VLA实战导向学习/面试手册，聚焦机器人具身智能挑战
- [datawhalechina/dive-into-embodied-ai](https://github.com/datawhalechina/dive-into-embodied-ai) `文档/汇总` `Python` `⭐578` — 具身智能入门教程，覆盖强化学习、World-Model、VLA及仿真到真实链路。
- [luohongk/Embodied-AI-Daily](https://github.com/luohongk/Embodied-AI-Daily) `文档/汇总` `HTML` `⭐477` — 自动更新 arXiv 上 VLN/VLA/World Model/SLAM 等论文列表，含最新10篇
- [wadeKeith/Awesome-Embodied-AI](https://github.com/wadeKeith/Awesome-Embodied-AI) `文档/汇总` `Python` `⭐251` — 收录具身智能综述、VLA模型、数据集、仿真器、人形机器人及安全资源。
- [x-zheng16/Awesome-Embodied-AI-Safety](https://github.com/x-zheng16/Awesome-Embodied-AI-Safety) `文档/汇总` `Python` `⭐152` — 具身智能安全综述：风险、攻击与防御，收录500+论文。
- [TingdeLiu/tingdeliu.github.io](https://github.com/TingdeLiu/tingdeliu.github.io) `文档/汇总` `HTML` `⭐116` — 个人研究笔记，涵盖具身智能、视觉语言导航与机器人学习。
- [HyperbolicCurve/Awesome-World-Action-Model](https://github.com/HyperbolicCurve/Awesome-World-Action-Model) `文档/汇总` `Python` `⭐37` — 收录VLA与World Action Model论文及资源的精选列表
- [GehaoZhang6/Grounded-Action-Model](https://github.com/GehaoZhang6/Grounded-Action-Model) `源码仓` `Python` `⭐36` — 3D接地动作模型，以3D接地作为机器人操作基础，含Python实现
- [hanjianhua44/Awesome-VLA-Papers](https://github.com/hanjianhua44/Awesome-VLA-Papers) `文档/汇总` `Python` `⭐30` — VLA论文精选集，覆盖自动驾驶与机器人领域
- [wangskyone/awesome-VLA-WAM](https://github.com/wangskyone/awesome-VLA-WAM) `文档/汇总` `Python` `⭐21` — 收录 VLA 与 World Action Model 相关论文与资源，质量筛选的阅读清单

---

## 🤗 HuggingFace 新模型

- [marcinnowakwyn/my-embodied-ai](https://huggingface.co/marcinnowakwyn/my-embodied-ai) · ⬇13 · 创建于 2026-10-12
- [SamerAyyad/VLA_Samer_24.09.2026_200eps_policy_ACT_500k](https://huggingface.co/SamerAyyad/VLA_Samer_24.09.2026_200eps_policy_ACT_500k) · ⬇5 · 创建于 2026-10-12
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
