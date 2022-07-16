from typing import Union
import aiohttp, traceback

from .. import log

player_error = '''未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。
如未绑定，请前往查分器官网进行绑定
https://www.diving-fish.com/maimaidx/prober/'''

async def get_player_data(project: str, payload: dict) -> Union[dict, str]:
    """
    获取用户数据，获取失败时返回字符串
    - `project` : 项目
        - `best` : 玩家数据
        - `plate` : 牌子
    - `payload` : 传递给查分器的数据
    """
    if project == 'best':
        p = 'player'
    elif project == 'plate':
        p = 'plate'
    else:
        return '项目错误'
    try:
        async with aiohttp.request('POST', f'https://www.diving-fish.com/api/maimaidxprober/query/{p}', json=payload) as resp:
            if resp.status == 400:
                data = player_error
            elif resp.status == 403:
                data = '该用户禁止了其他人获取数据。'
            elif resp.status == 200:
                data = await resp.json()
            else:
                data = '未知错误，请联系BOT管理员'
    except Exception as e:
        log.error(f'Error: {traceback.print_exc()}')
        data = f'获取玩家数据时发生错误，请联系BOT管理员: {type(e)}'
    return data

async def get_rating_ranking_data() -> Union[dict, str]:
    """
    获取排名，获取失败时返回字符串
    """
    try:
        async with aiohttp.request('GET', 'https://www.diving-fish.com/api/maimaidxprober/rating_ranking') as resp:
            if resp.status != 200:
                data = '未知错误，请联系BOT管理员'
            else:
                data = await resp.json()
    except Exception as e:
        log.error(f'Error: {traceback.print_exc()}')
        data = f'获取排名时发生错误，请联系BOT管理员: {type(e)}'
    return data
