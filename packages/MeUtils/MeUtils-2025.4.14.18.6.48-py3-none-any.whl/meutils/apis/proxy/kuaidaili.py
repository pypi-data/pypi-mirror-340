#!/usr/bin/env Python
# -*- coding: utf-8 -*-


from meutils.pipe import *
from meutils.caches import rcache
from meutils.decorators.retry import retrying

url = "https://dps.kdlapi.com/api/getdps/?secret_id=owklc8tk3ypo00ohu80o&signature=8gqqy7w64g7uunseaz9tcae7h8saa24p&num=1&pt=1&format=json&sep=1"


@rcache(ttl=60 - 5)
@retrying()
async def get_proxy_list():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        proxy_list = response.json().get('data').get('proxy_list')

        return [f"http://{proxy}" for proxy in proxy_list]


if __name__ == '__main__':
    arun(get_proxy_list())
