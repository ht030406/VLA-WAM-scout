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
"""
import sys
import traceback
from datetime import datetime, timezone

import config
from sources import arxiv_source, github_source, hf_source
from summarize import LingshuClient, summarize_papers, judge_repos, daily_insight
import report as report_mod


def main() -> int:
    ts = datetime.now(timezone.utc)
    date_str = f"{ts.year}-{ts.month:02d}-{ts.day:02d}"
    print(f"== vla-wam-scout 开始采集 [{date_str}] ==")

    # ---------- 1. 采集 ----------
    print("[1/4] 拉取 arXiv 论文...")
    try:
        papers = arxiv_source.fetch_papers()
    except Exception as e:
        papers = []
        print(f"  !! arXiv 采集失败: {e}")
    print(f"  -> {len(papers)} 篇论文")

    print("[2/4] 扫描 GitHub 仓库...")
    try:
        repos = github_source.fetch_repos()
    except Exception as e:
        repos = []
        print(f"  !! GitHub 采集失败: {e}")
    print(f"  -> {len(repos)} 个仓库")

    print("[3/4] 拉取 HuggingFace 新模型...")
    try:
        models = hf_source.fetch_models()
    except Exception as e:
        models = []
        print(f"  !! HuggingFace 采集失败: {e}")
    print(f"  -> {len(models)} 个模型")

    # ---------- 2. LLM 总结 ----------
    print("[4/4] 灵枢 LLM 总结...")
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

    # ---------- 3. 写报告 ----------
    md = report_mod.build_markdown_report(papers, repos, models,
                                          paper_summaries, repo_judgements, insight)
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
    print(f"   论文 {len(papers)} 篇 / 仓库 {len(repos)} 个 / 模型 {len(models)} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())
