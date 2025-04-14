# -*- coding: utf-8 -*-
import requests
import json
from typing import List, Dict


def get_SegSearchCandidates(Query: str, Candidates: List[Dict]) -> str or None:
    """
    获取分段搜索候选结果。

    :param Query: 搜索查询字符串
    :param Candidates: 候选结果列表，每个元素是一个字典，包含 "Score", "Text", "Attrs" 等键
    :return: 按分数排序后的前 5 个候选结果的 JSON 字符串，如果请求失败则返回 None
    """
    api_url = "https://genie.bytedance.com/pre/entsol/genie/skills/it-service/common/SegSearchCandidates"
    payload = {
        "Query": Query,
        "TopN": 0,
        "Candidates": Candidates
    }

    headers = {
        'Authorization': 'Basic bWFzLTZrMGJxLWgwMmhxbDM4MjQtMzJrcXQ6YTljNDIwMWJlOTc4OTg4MDRhZmZiNTQyMzA2ZTMxMzU=',
        'Content-Type': 'application/json'
    }

    try:
        # 发起 POST 请求
        response = requests.post(api_url, headers=headers, json=payload)
        # 检查响应状态码
        response.raise_for_status()
        result = response.json()
        if result and 'Candidates' in result:
            top_5_scores = sorted(result['Candidates'], key=lambda x: x.get('Score', 0), reverse=True)[:5]
            return json.dumps(top_5_scores, ensure_ascii=False)
    except requests.RequestException as e:
        print(f"请求发生错误: {e}")
    except (KeyError, ValueError) as e:
        print(f"处理响应数据时发生错误: {e}")

    return None
