#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2025/4/10 16:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI
from meutils.llm.openai_utils import to_openai_params

from meutils.schemas.openai_types import CompletionRequest


class Completions(object):

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    async def create(self, request: CompletionRequest):
        data = to_openai_params(request)
        if 'gemini' in request.model:
            data.pop("seed", None)
            data.pop("presence_penalty", None)
            data.pop("frequency_penalty", None)
            data.pop("extra_body", None)

        return await self.client.chat.completions.create(**data)


if __name__ == '__main__':
    # 测试

    request = CompletionRequest(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一个助手"},
            {"role": "user", "content": "你好"}
        ],
        stream=False
    )
    arun(Completions().create(request))
