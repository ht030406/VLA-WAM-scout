# -*- coding: utf-8 -*-
"""灵枢 LLM 总结模块：批量生成论文亮点摘要 + 仓库价值判断。

防御性设计：任何一次 API 失败都不影响整体流程——
论文/仓库条目缺失总结时，report.py 会给出可读降级文案。
"""
import json
import re
import ssl
import time
from typing import Dict, List, Optional

import requests
import urllib3

import config


class LingshuClient:
    def __init__(self):
        self.api_key = config.LINGSHU_API_KEY
        if not self.api_key:
            raise RuntimeError("LINGSHU_API_KEY 未配置")
        self.url = f"{config.LINGSHU_BASE_URL.rstrip('/')}/chat/completions"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        # 自签 CA：灵枢链证书
        self.verify = config.CA_CERT_FILE if config.CA_CERT_FILE and _path_exists(config.CA_CERT_FILE) else True

    def chat(self, messages: List[dict], max_tokens: int = None, temperature: float = None,
             retries: int = 2) -> str:
        body = {
            "model": config.LINGSHU_MODEL,
            "messages": messages,
            "max_tokens": max_tokens or config.LLM_MAX_TOKENS,
            "temperature": temperature if temperature is not None else config.LLM_TEMPERATURE,
        }
        for attempt in range(retries + 1):
            try:
                r = self.session.post(self.url, json=body, timeout=180, verify=self.verify)
                if r.status_code == 429:
                    time.sleep(20 * (attempt + 1))
                    continue
                r.raise_for_status()
                data = r.json()
                content = data["choices"][0]["message"].get("content")
                if content is None or not content.strip():
                    # 灵枢偶发返回空 content（或全在 reasoning 里），重试一次
                    time.sleep(4 * (attempt + 1))
                    continue
                return content.strip()
            except (requests.RequestException, KeyError, urllib3.exceptions.HTTPError) as e:
                if attempt == retries:
                    print(f"  [llm] call failed after {retries} retries: {e}")
                    return ""
                time.sleep(5 * (attempt + 1))
        return ""


def _path_exists(p: str) -> bool:
    import os
    return os.path.exists(p)


# --------------------------------------------------------------------------
# 论文：批量生成"一句话核心贡献 + 是否重点"
# --------------------------------------------------------------------------
PAPER_SYSTEM = (
    "你是机器人学前沿研究助理，擅长 VLA（Vision-Language-Action）与 "
    "World Action Model / World Model 方向。对每篇论文只输出 JSON 数组，"
    "每项格式：{\"arxiv_id\": str, \"highlight\": str, \"is_key\": bool, "
    "\"category\": str}\n"
    "highlight 为 40 字以内的一句话中文核心贡献；is_key 表示是否属于今日重点"
    "（方法非常新颖/结果突破/影响大），同一批最多 2 篇为 true，其余 false；"
    "category 取 VLA | WorldModel | RobotPolicy | "
    "EmbodiedBenchmark | Theory 之一。除 JSON 外不要输出任何其他内容。"
)


def summarize_papers(client: LingshuClient, papers: List[dict]) -> Dict[str, dict]:
    """返回 {arxiv_id: {highlight, is_key, category}}，失败条目补空白。"""
    result: Dict[str, dict] = {}
    if not papers:
        return result

    BATCH = 4
    for i in range(0, len(papers), BATCH):
        batch = papers[i:i + BATCH]
        lines = []
        for p in batch:
            title = (p.get("title") or "")[:120]
            abstract = (p.get("abstract") or "")[:250].replace("\n", " ")
            lines.append(f"- id={p['arxiv_id']}\n  title: {title}\n  abstract: {abstract}")
        user_msg = "请总结以下论文：\n\n" + "\n".join(lines)
        raw = client.chat([
            {"role": "system", "content": PAPER_SYSTEM},
            {"role": "user", "content": user_msg},
        ], max_tokens=2000)
        parsed = _parse_json_array(raw)
        if not parsed:
            print("  [llm] paper batch parse failed, using fallbacks")
            parsed = []
        by_id = {str(x.get("arxiv_id", "")).strip(): x for x in parsed if isinstance(x, dict)}
        for p in batch:
            item = by_id.get(p["arxiv_id"]) or {}
            cat = str(item.get("category", "")).strip()
            if cat.lower() in ("worldmodel", "world-model", "world model", "wm"):
                cat = "WorldModel"
            elif cat.lower() in ("vla", "vision-language-action", "vision-language action"):
                cat = "VLA"
            result[p["arxiv_id"]] = {
                "highlight": str(item.get("highlight", "")).strip(),
                "is_key": bool(item.get("is_key")),
                "category": cat,
            }
        time.sleep(1)
    return result


# --------------------------------------------------------------------------
# 仓库：价值判断（是否真源码仓、亮点、强烈关注建议）
# --------------------------------------------------------------------------
REPO_SYSTEM = (
    "你是开源生态研究员，负责从候选列表中挑出真正有研究/使用价值的 VLA 与 "
    "World Action Model 相关开源仓库。只输出 JSON 数组，每项格式："
    "{\"full_name\": str, \"verdict\": \"source\"|\"docs\"|\"noise\", "
    "\"highlight\": str, \"suggest\": bool}\n"
    "verdict: source=含可运行源码(训练/推理/模型实现)；docs=awesome-list/文档/无源码；"
    "noise=与 VLA/WAM 无关。highlight 为 50 字以内中文亮点（源码仓写清框架/能力，"
    "docs 仓写清收录内容）。suggest=true 表示强烈建议关注（源码仓且方法新颖或人气温）。"
    "除 JSON 外不要输出任何其他内容。"
)


def judge_repos(client: LingshuClient, repos: List[dict]) -> Dict[str, dict]:
    """返回 {full_name: {verdict, highlight, suggest}}。"""
    result: Dict[str, dict] = {}
    if not repos:
        return result

    BATCH = 4
    for i in range(0, len(repos), BATCH):
        batch = repos[i:i + BATCH]
        lines = []
        for r in batch:
            desc = (r.get("description") or "")[:120].replace("\n", " ")
            readme = (r.get("readme_snippet") or "")[:220].replace("\n", " ")
            lines.append(
                f"- {r['full_name']} | lang={r.get('language')} | stars={r.get('stars')} "
                f"| created={r.get('created_at', '')[:10]} | pushed={r.get('pushed_at', '')[:10]}\n"
                f"  desc: {desc}\n  readme: {readme}"
            )
        user_msg = "请评估以下仓库：\n\n" + "\n".join(lines)
        raw = client.chat([
            {"role": "system", "content": REPO_SYSTEM},
            {"role": "user", "content": user_msg},
        ], max_tokens=2000)
        parsed = _parse_json_array(raw)
        if not parsed:
            print("  [llm] repo batch parse failed, using fallbacks")
            parsed = []
        by_name = {str(x.get("full_name", "")).strip(): x for x in parsed if isinstance(x, dict)}
        for r in batch:
            item = by_name.get(r["full_name"]) or {}
            verdict = str(item.get("verdict", "")).lower()
            if any(k in verdict for k in ("source", "源码", "代码", "实现", "train")):
                verdict = "source"
            elif any(k in verdict for k in ("docs", "文档", "awesome", "汇总", "list", "收藏")):
                verdict = "docs"
            elif any(k in verdict for k in ("noise", "无关", "噪声", "重复", "低质", "占位")):
                verdict = "noise"
            else:
                verdict = "source"
            result[r["full_name"]] = {
                "verdict": verdict,
                "highlight": str(item.get("highlight", "")).strip(),
                "suggest": bool(item.get("suggest")),
            }
        time.sleep(1)
    return result


# --------------------------------------------------------------------------
# 每日总评
# --------------------------------------------------------------------------
def daily_insight(client: LingshuClient, n_papers: int, n_repos: int,
                  top_papers: List[dict], top_repos: List[dict]) -> str:
    """生成当天 2-3 句趋势总评。"""
    if not top_papers and not top_repos:
        return ""
    lines = []
    for p in top_papers[:3]:
        lines.append(f"- arXiv:{p['arxiv_id']} {p.get('title', '')[:120]}")
    for r in top_repos[:3]:
        lines.append(f"- {r['full_name']} ({r.get('stars', 0)}★) {r.get('description', '')[:100]}")
    user_msg = (
        f"今天共 {n_papers} 篇新论文、{n_repos} 个相关仓库。请用 3 句话以内的中文"
        f"总结今日 VLA/WAM 领域动态与值得关注的方向（结合以下最高优先级条目）：\n"
        + "\n".join(lines)
    )
    return client.chat([
        {"role": "system", "content": "你是 VLA/World Action Model 领域追踪研究员，输出简洁中文。",
         },  # noqa
        {"role": "user", "content": user_msg},
    ], max_tokens=400)


# --------------------------------------------------------------------------
# JSON 解析兜底
# --------------------------------------------------------------------------
def _pick(d: dict, *keys, default=""):
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default


def _norm_json_item(item) -> dict:
    """把模型返回的 JSON 项统一字段名（容忍 full_name/repo/name 等变体）。"""
    if not isinstance(item, dict):
        return {}
    out = {}
    out["arxiv_id"] = str(_pick(item, "arxiv_id", "id", "paper_id", default="")).strip()
    out["full_name"] = str(_pick(item, "full_name", "repo", "repository", "name", "repo_name",
                                 default="")).strip()
    out["highlight"] = str(_pick(item, "highlight", "summary", "亮点", "comment", "assessment",
                                 "reason", "一句话", default="")).strip()
    verdict = str(_pick(item, "verdict", "type", "kind", "classification", "class",
                        "category_type", default="")).strip().lower()
    out["verdict"] = verdict
    out["category"] = str(_pick(item, "category", "area", "方向", default="")).strip()
    suggest = _pick(item, "suggest", "recommend", "key", "important", "is_key",
                    "值得关注", default=None)
    if isinstance(suggest, bool):
        out["suggest"] = suggest
    elif isinstance(suggest, (int, float)):
        out["suggest"] = bool(suggest)
    else:
        out["suggest"] = str(suggest).lower() in ("true", "1", "yes", "是", "建议")
    # is_key 兼容字符串 true/false
    is_key = _pick(item, "is_key", "key", "important", "重点", default=None)
    if isinstance(is_key, bool):
        out["is_key"] = is_key
    elif isinstance(is_key, (int, float)):
        out["is_key"] = bool(is_key)
    elif isinstance(is_key, str):
        out["is_key"] = is_key.strip().lower() in ("true", "1", "yes", "是")
    else:
        out["is_key"] = False
    return out


def _parse_json_array(raw: str) -> Optional[List[dict]]:
    if not raw:
        return None
    text = raw.strip()
    # 可能被代码块包裹
    m = re.search(r"\[.*\]", text, re.S)
    if m:
        text = m.group(0)
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return [_norm_json_item(x) for x in data]
        return None
    except json.JSONDecodeError:
        # 容错：逐行拼 JSON 对象
        objs = re.findall(r"\{[^{}]*\}", text)
        if not objs:
            return None
        out = []
        for o in objs:
            try:
                out.append(_norm_json_item(json.loads(o)))
            except json.JSONDecodeError:
                continue
        return out or None
