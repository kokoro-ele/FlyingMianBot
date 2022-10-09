
from email.quoprimime import unquote
from tokenize import Token
from numpy import TooHardError
import requests
from hoshino import Service
from hoshino.typing import CQEvent
from hoshino.config.aiimggen import Token
import base64
from loguru import logger
import re
import json
from hoshino import aiorequests
import io
from io import BytesIO
from PIL import Image
#import sqlite3

##替换为自己的token
token = Token
##第一个url结尾为?tags=
##第二个url结尾为got_image2image
word2img_url = "http://91.217.139.190:5010/got_image?tags="
img2img_url = "http://91.217.139.190:5010/got_image2image"
sv = Service('AI_image_gen', bundle='娱乐',enable_on_default = False,help_='''
生成色图 
'''.strip())

sv_help='''
使用NAI API生成二次元图
使用方法：生成色图 <tags>[&r18=0|&shape=Portrait/Landscape/Square|&scale=11|&seed=1234]
<tags>为必选参数  [ ]为可选参数，其中：
tags 图片含有的要素，使用大括号{}括住某些tag来增加此tag的权重，括号越多权重越高如{{{loli}}}
r18 字面意思，默认为0,开启为1 请勿在公共群开启
shape 分别为竖图、横图、方图 默认为横图
scale 细节等级，建议为11-24，太高会变奇怪
seed 随机种子，任意数字。相同的种子可能会有相同的结
'''.strip()


# XP_DB_PATH = os.path.expanduser('~/.hoshino/AI_image_xp.db')
# class XpCounter:
#     def __init__(self):
#         os.makedirs(os.path.dirname(XP_DB_PATH), exist_ok=True)
#         self._create_table()
#     def _connect(self):
#         return sqlite3.connect(XP_DB_PATH)
        
#     def _create_table(self):
#         try:
#             self._connect().execute('''CREATE TABLE IF NOT EXISTS XP_NUM
#                           (UID             INT    NOT NULL,
#                            KEYWORD         TEXT   NOT NULL,
#                            NUM             INT    NOT NULL,
#                            PRIMARY KEY(UID,KEYWORD));''')
#         except:
#             raise Exception('创建表发生错误')
            
#     def _add_xp_num(self, uid, keyword):
#         try:
        
#             num = self._get_xp_num(uid, keyword)
#             if num == None:
#                 num = 0
#             num += 1
#             with self._connect() as conn:
#                 conn.execute(
#                     "INSERT OR REPLACE INTO XP_NUM (UID,KEYWORD,NUM) \
#                                 VALUES (?,?,?)", (uid, keyword, num)
#                 )
                  
#         except:
#             raise Exception('更新表发生错误')
            
#     def _get_xp_num(self, uid, keyword):
#         try:
#             r = self._connect().execute("SELECT NUM FROM XP_NUM WHERE UID=? AND KEYWORD=?", (uid, keyword)).fetchone()
#             return 0 if r is None else r[0]
#         except:
#             raise Exception('查找表发生错误')
    
#     def _get_xp_list(self, uid, num):
#         with self._connect() as conn:
#             r = conn.execute(
#                 f"SELECT KEYWORD,NUM FROM XP_NUM WHERE UID={uid} ORDER BY NUM desc LIMIT {num}").fetchall()
#         return r if r else {}

# def get_xp_list(uid):
#     XP = XpCounter()
#     xp_list = XP._get_xp_list(uid, 15)
#     if len(xp_list)>0:
#         data = sorted(xp_list,key=lambda cus:cus[1],reverse=True)
#         new_data = []
#         for xp_data in data:
#             keyword, num = xp_data
#             new_data.append((keyword,num))
#         rankData = sorted(new_data,key=lambda cus:cus[1],reverse=True)
#         return rankData
#     else:
#         return []

# def add_xp_num(uid, keyword):
#     XP = XpCounter()
#     XP._add_xp_num(uid, keyword)

@sv.on_fullmatch('生成色图帮助')
async def gen_pic_help(bot, ev: CQEvent):
    # mes = f'使用NAI API生成二次元图\n'
    # mes += f'使用方法：生成色图 <tags>[&r18=0|&shape=Portrait/Landscape/Square|&scale=11|&seed=1234]\n'
    # mes += f'<tags>为必选参数  [ ]为可选参数，其中：\n'
    # mes += f'tags 图片含有的要素，使用大括号{{}}括住某些tag来增加此tag的权重，如' + '{{{'+'loli' + '}}}\n'
    # mes += f'r18 字面意思，默认为0,开启为1 请勿在公共群开启\n'
    # mes += f'shape 分别为竖图、横图、方图 默认为横图\n'
    # mes += f'scale 细节等级，建议为11-24，太高会变奇怪\n'
    # mes += f'seed 随机种子，任意数字。相同的种子可能会有相同的结果'
    await bot.send(ev, sv_help)

# @sv.on_fullmatch(['我的XP'])
# async def get_my_xp(bot, ev: CQEvent):
#     xp_list = get_xp_list(ev.user_id)
#     uid = ev.user_id
#     msg = '您的XP信息为：\n'
#     if len(xp_list)>0:
#         for xpinfo in xp_list:
#             keyword, num = xpinfo
#             msg += f'关键词：{keyword}；查询次数：{num}\n'
#     else:
#         msg += '暂无您的XP信息'
#     await bot.send(ev, msg)

@sv.on_prefix(('生成色图'))
async def gen_pic(bot, ev: CQEvent):
    try:
        await bot.send(ev, f"正在生成", at_sender=True)
        text = ev.message.extract_plain_text()
        taglist = text.split(',')
        # for tag in taglist:
        #     add_xp_num(uid, tag)
        get_url = word2img_url + text + f'&token={token}'
        # image = await aiorequests.get(get_url)
        temp = get_url
        res = await aiorequests.get(get_url)
        image = await res.content
        load_data = json.loads(re.findall('{"steps".+?}', str(image))[0])
        image_b64 = 'base64://' + str(base64.b64encode(image).decode())
        mes = f"[CQ:image,file={image_b64}]\n"
        mes += f'seed:{load_data["seed"]}   '
        mes += f'scale:{load_data["scale"]}\n'
        mes += f'tags:{text}'
        await bot.send(ev, mes, at_sender=True)
    except:
        await bot.send(ev, "生成失败…")


thumbSize=(768,768)
@sv.on_prefix(('以图生图'))
async def gen_pic_from_pic(bot, ev: CQEvent):
    try:
        await bot.send(ev, f"正在生成", at_sender=True)
        tag = ev.message.extract_plain_text()
        if tag == "":
            url = ev.message[0]["data"]["url"]
        else:
            url = ev.message[1]["data"]["url"]
        post_url = img2img_url + (f"?tags={tag}" if tag != "" else "") 
        # ret = re.match(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
        image = Image.open(io.BytesIO(requests.get(url, timeout=20).content))
        image = image.convert('RGB')
        if (image.size[0] > image.size[1]):
            image_shape = "Landscape"
        elif (image.size[0] == image.size[1]):
            image_shape = "Square"
        else:
            image_shape = "Portrait"
        image.thumbnail(thumbSize, resample=Image.ANTIALIAS)
        imageData = io.BytesIO()
        image.save(imageData, format='JPEG')
        temp = post_url+ "&shape=" + image_shape + f'&token={token}'
        res = await aiorequests.post(post_url+ "&shape=" + image_shape + f'&token={token}', data=base64.b64encode(imageData.getvalue()))
        img = await res.content
        image_b64 = f"base64://{str(base64.b64encode(img).decode())}"
        mes = f"[CQ:image,file={image_b64}]\n"
        mes += f'tags:{tag}'
        await bot.send(ev, mes, at_sender=True)
    except:
        await bot.send(ev, "生成失败…")