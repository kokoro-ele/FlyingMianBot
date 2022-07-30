import random
import asyncio
from datetime import datetime
import hoshino
from hoshino import Service
from hoshino.modules.groupmaster.anti_lex import hour_call
from .base import format_setu_msg
from .lolicon import get_setu_online
from .acggov import acggov_search_setu
from .config import get_config, get_group_config
from . import send_msg
from .base import search_setu
sv_help= '''
启用请联系维护者
'''
sv = Service('每日一涩', enable_on_default=False, help_=sv_help)
sv18 = Service('每日一涩r18', enable_on_default=False, help_=sv_help)


async def get_img(keyword,mode):
    num = 1
    msg_list = []
    timg_List = []
    while len(msg_list) == 0:
        if(mode == 1):
            timg_List = await get_setu_online(1, 1)
        if(mode == 0):
            timg_List = await acggov_search_setu(keyword,num)    
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

@sv18.scheduled_job('cron', hour='*/2')
async def day():
    forward_msg = await get_img('萝莉',1)
    try:
        await asyncio.sleep(0.8)
        await sv.broadcast('我先放盒纸巾在这里.jpg', 'r18 setu message')
        await sv.broadcast_forward(forward_msg, TAG = 'r18')
    except:   
        await sv.broadcast('太涩了发不出去捏', 'day setu message')
@sv.scheduled_job('cron', hour="7",minute="00")
async def day():
    forward_msg = await get_img('白丝')
    try:
        await asyncio.sleep(0.8)
        await sv.broadcast('白天啦,该看白丝啦', 'day setu message')
        await sv.broadcast_forward(forward_msg, TAG = 'day')
    except:   
        await sv.broadcast('太涩了发不出去捏', 'day setu message')
        
@sv.scheduled_job('cron', hour="14",minute="0")
async def noon():
    forward_msg = await get_img('雪糕')    
    try:
        await asyncio.sleep(0.8)
        await sv.broadcast('太热啦，恰根雪糕捏', 'noon setu message')
        await sv.broadcast_forward(msgs = forward_msg, TAG = 'noon setu message')
    except:
        await sv.broadcast_forward('太涩了发不出去捏', TAG = 'noon setu error')


@sv.scheduled_job('cron', hour="19",minute="0")
async def night():
    forward_msg = await get_img('黑丝')    
    try:
        await asyncio.sleep(0.8)
        await sv.broadcast('黑夜啦,该看黑丝啦', 'night setu message')
        await sv.broadcast_forward(msgs = forward_msg, TAG = 'night setu message')
    except:
        await sv.broadcast_forward('太涩了发不出去捏', TAG = 'night setu error')

@sv.scheduled_job('cron', hour="22",minute="0")
async def night():
    forward_msg = await get_img('巧克力')    
    try:
        await asyncio.sleep(0.8)
        await sv.broadcast('恰点巧克力睡觉力捏', 'night setu message')
        await sv.broadcast_forward(msgs = forward_msg, TAG = 'night setu message')
    except:
        await sv.broadcast_forward('太涩了发不出去捏', TAG = 'night setu error')
