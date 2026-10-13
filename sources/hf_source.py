# -*- coding: utf-8 -*-
"""HuggingFace 新模型拉取：按关键词搜最近创建/更新的 VLA/WAM 相关模型。"""
import re
from datetime import datetime, timedelta, timezone
from typing import Dict, List

import requests

import config


# 明确无关的 pipeline / 标签（翻译、普通文本生成等）
HF_IRRELEVANT_HITS = [
    "translation", "text2text", "text-to-text", "opus-mt", "text-generation",
    "image-classification", "audio", "speech", "summarization", "question-answering",
]

# 相关关键词（命中 model_id 或 tags）
HF_RELEVANCE_HITS = [
    "vla", "world model", "world-model", "world action", "action model",
    "embodied", "vision-language-action", "vision language action",
]


def _is_relevant(m: dict) -> bool:
    mid = m.get("id", "")
    tags = [t for t in (m.get("tags") or []) if isinstance(t, str)]
    pipeline = (m.get("pipeline_tag") or "").lower()
    mid_raw = mid
    mid_l, tags_l = mid.lower(), " ".join(tags).lower()
    hay = f"{mid_l} {tags_l} {pipeline}"

    def hit(text_lower: str, keyword: str) -> bool:
        """子串命中（对 lower 文本）。调用前自行处理大小写/分词。"""
        return keyword in text_lower

    # mid 相关性：大小写敏感的全大写 VLA + 严格边界的小写分隔形式
    def mid_relevant() -> bool:
        if "VLA" in mid_raw:  # MyVLA / QwenVLA / MA-VLA / VLA-model 等
            return True
        # 小写/分隔形式：vla 前后不能是字母数字，避免 vlad/vlas 误中
        if re.search(r"(?<![a-z0-9])vla(?![a-z0-9])", mid_l):
            return True
        if any(k in mid_l for k in ("world model", "world-model", "world action",
                                    "action model", "vision-language-action",
                                    "vision language action", "embodied")):
            return True
        return False

    mid_hit = mid_relevant()

    # 无关信号优先剔除（如 opus-mt 翻译、纯文本生成）
    if any(k in hay for k in HF_IRRELEVANT_HITS):
        # 例外：model_id 本身就是明确 VLA/WAM 词则不剔除
        if not mid_hit:
            return False
        return True
    # 相关：mid 命中，或 tags/pipeline 命中
    if mid_hit:
        return True
    return any(hit(tags_l, k) or hit(pipeline, k) for k in HF_RELEVANCE_HITS)


def _iso_recent(iso: str, days: int) -> bool:
    if not iso:
        return False
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except Exception:
        return False
    return dt >= datetime.now(timezone.utc) - timedelta(days=days)


def fetch_models(lookback_days: int = None) -> List[Dict]:
    """搜索近 lookback_days 天新创建的 VLA/WAM 模型（按 createdAt 排序）。"""
    lookback_days = lookback_days or config.LOOKBACK_DAYS
    seen: Dict[str, dict] = {}

    for term in config.HF_SEARCH_TERMS:
        try:
            r = requests.get(
                f"{config.HF_API}/models",
                params={"search": term, "sort": "createdAt", "direction": -1,
                        "limit": min(config.HF_MAX_MODELS, 50)},
                timeout=config.HF_TIMEOUT,
            )
            r.raise_for_status()
            items = r.json()
        except requests.RequestException as e:
            print(f"  [hf] search failed for {term!r}: {e}")
            continue

        for m in items:
            mid = m.get("id", "")
            if not mid:
                continue
            if not _iso_recent(m.get("createdAt", ""), lookback_days):
                continue
            if not _is_relevant(m):
                continue
            seen[mid] = {
                "model_id": mid,
                "url": f"https://huggingface.co/{mid}",
                "downloads": m.get("downloads") or 0,
                "likes": m.get("likes") or 0,
                "createdAt": m.get("createdAt", ""),
                "lastModified": m.get("lastModified", ""),
                "pipeline_tag": m.get("pipeline_tag") or "",
                "tags": (m.get("tags") or [])[:8],
            }

    models = list(seen.values())
    models.sort(key=lambda m: m["downloads"], reverse=True)
    return models[: config.HF_MAX_MODELS]
