#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vla-wam-scout 每日运行入口。

用法：
    pip install -r requirements.txt
    cp .env.example .env   # 填入 LINGSHU_API_KEY 等
    python run_daily.py

产出（写入 reports/）：
    daily-vla-wam-YYYY-MM-DD.md   每日 Markdown 情报日报
    latest.md                     当日日报拷贝（固定名，便于取用）
    repos.md                      仓库数据表（可集成进网站）
    state.json                    跨日去重状态（已报道条目登记）
"""
import sys
import traceback
from datetime import datetime, timezone

import config
from sources import arxiv_source, github_source, hf_source
from summarize import LingshuClient, summarize_papers, judge_repos, daily_insight
from state import StateStore
import report as report_mod


def main() -> int:
    ts = datetime.now(timezone.utc)
    date_str = f"{ts.year}-{ts.month:02d}-{ts.day:02d}"
    print(f"== vla-wam-scout 开始采集 [{date_str}] ==")

    # ---------- 1. 加载去重状态 ----------
    state = StateStore()
    n_seen = sum(len(v) for v in state.data.values())
    print(f"[0/5] 加载去重状态 reports/{state.path.name}: 已报道 {n_seen} 条")

    # ---------- 2. 采集 ----------
    print("[1/5] 拉取 arXiv 论文...")
    try:
        papers_raw = arxiv_source.fetch_papers()
    except Exception as e:
        papers_raw = []
        print(f"  !! arXiv 采集失败: {e}")
    print(f"  -> {len(papers_raw)} 篇论文")

    print("[2/5] 扫描 GitHub 仓库...")
    try:
        repos_raw = github_source.fetch_repos()
    except Exception as e:
        repos_raw = []
        print(f"  !! GitHub 采集失败: {e}")
    print(f"  -> {len(repos_raw)} 个仓库")

    print("[3/5] 拉取 HuggingFace 新模型...")
    try:
        models_raw = hf_source.fetch_models()
    except Exception as e:
        models_raw = []
        print(f"  !! HuggingFace 采集失败: {e}")
    print(f"  -> {len(models_raw)} 个模型")

    # ---------- 3. 跨日去重 ----------
    print("[4/5] 跨日去重...")
    papers, papers_dup = state.split_papers(papers_raw)
    repos, repos_dup, repos_surge = state.split_repos(repos_raw)
    models, models_dup = state.split_models(models_raw)
    # 飙升仓库并入本期展示（带 _surge 标记），同时从"重复"里剔除
    repos = repos + repos_surge
    print(f"  论文：新增 {len(papers)} / 重复忽略 {len(papers_dup)}")
    print(f"  仓库：新增 {len(repos)}（含飙升重报 {len(repos_surge)}）/ 重复忽略 {len(repos_dup)}")
    print(f"  模型：新增 {len(models)} / 重复忽略 {len(models_dup)}")

    # ---------- 4. LLM 总结（只总结新增部分） ----------
    print("[5/5] 灵枢 LLM 总结...")
    paper_summaries: dict = {}
    repo_judgements: dict = {}
    insight = ""
    try:
        client = LingshuClient()
        if papers:
            print("  总结论文...")
            paper_summaries = summarize_papers(client, papers)
        if repos:
            print("  评估仓库...")
            repo_judgements = judge_repos(client, repos)
        if papers or repos:
            print("  生成每日要点...")
            insight = daily_insight(client, len(papers), len(repos),
                                    papers[:8], repos[:8])
    except Exception as e:
        print(f"  !! LLM 总结阶段失败（报告将降级）：{e}")
        traceback.print_exc()

    # ---------- 5. 登记状态 + 写报告 ----------
    state.mark_papers(papers)
    state.mark_repos(repos)
    state.mark_models(models)
    state.save()

    dedup_info = {
        "papers": (len(papers_dup),), "repos": (len(repos_dup), len(repos_surge)),
        "models": (len(models_dup),),
    }
    md = report_mod.build_markdown_report(
        papers, repos, models, paper_summaries, repo_judgements, insight,
        dedup_info=dedup_info,
    )
    repos_md = report_mod.build_repos_md(repos, repo_judgements, date_str)

    daily_file = config.REPORTS_DIR / f"daily-vla-wam-{date_str}.md"
    latest_file = config.REPORTS_DIR / "latest.md"
    repos_file = config.REPORTS_DIR / "repos.md"
    daily_file.write_text(md, encoding="utf-8")
    latest_file.write_text(md, encoding="utf-8")
    repos_file.write_text(repos_md, encoding="utf-8")

    print(f"\n== 完成：{daily_file}")
    print(f"   latest.md   -> {latest_file}")
    print(f"   repos.md    -> {repos_file}")
    print(f"   state.json  -> {state.path}")
    print(f"   论文 {len(papers)} 篇（忽略 {len(papers_dup)} 重复）/ "
          f"仓库 {len(repos)} 个（忽略 {len(repos_dup)} 重复）/ "
          f"模型 {len(models)} 个（忽略 {len(models_dup)} 重复）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
