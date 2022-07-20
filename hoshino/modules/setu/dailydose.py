import random
from datetime import datetime
from turtle import forward
import hoshino
from hoshino import Service
from .base import format_setu_msg
from .lolicon import lolicon_search_setu
from .config import get_config, get_group_config
from . import send_msg
from .base import search_setu
sv_help= '''
setu set day/night xxx
'''
sv = Service('每日一涩', enable_on_default=False, help_=sv_help)

async def get_img(keyword):
    num = 1
    msg_list = []
    timg_List = []
    while len(msg_list) == 0:
        timg_List = await lolicon_search_setu(keyword, 0, num)
        timg = timg_List[0]
        if timg['id'] != 0:
            msg = format_setu_msg(timg)
        else:
            msg = timg['title']			
        msg_list.append(msg)

    forward_msg = []
    for msg in msg_list:
        forward_msg.append({
            "type": "node",
            "data": {
                "name": str("注意身体捏"),
                "uin": str("2128365034"),
                "content": msg
            }
        })
    return forward_msg

@sv.scheduled_job('cron', hour="8",minute="0")
#@sv.on_fullmatch('mmm')
async def day():
    forward_msg = await get_img('白丝')
    try:
        await sv.broadcast('白天啦,该看白丝啦', 'day setu message')
        await sv.broadcast_forward(forward_msg, TAG = 'day')
    except:   
        await sv.broadcast('白天啦,该看白丝啦', 'day setu message')
        
@sv.scheduled_job('cron', hour="12",minute="0")
#@sv.on_fullmatch('mmm')
async def night():
    forward_msg = await get_img('雪糕')    
    try:
        await sv.broadcast('太热啦，恰根雪糕啦', 'noon setu message')
        await sv.broadcast_forward(msgs = forward_msg, TAG = 'noon setu message')
    except:
        await sv.broadcast_forward('太涩了发不出去捏', TAG = 'noon setu error')

@sv.scheduled_job('cron', hour="20",minute="0")
#@sv.on_fullmatch('mmm')
async def night():
    forward_msg = await get_img('黑丝')    
    try:
        await sv.broadcast('黑夜啦,该看黑丝啦', 'night setu message')
        await sv.broadcast_forward(msgs = forward_msg, TAG = 'night setu message')
    except:
        await sv.broadcast_forward('太涩了发不出去捏', TAG = 'night setu error')
