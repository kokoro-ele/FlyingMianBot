from hoshino import Service, priv 
import asyncio
from revChatGPT.revChatGPT import Chatbot
import time
import random

config = {
        "Authorization": "<Your Bearer Token Here>", # This is optional
        "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..4tg1KEFNWW_9oq1x.087qK3s1SN0mlh6dtpFe5n2YSBkjl2SuIDrCaTd1wrj_iBQLIXfEvULMSJ6I1qi1Ice3g1RapNYwdXJo-Hfrcx5Ix73B0cAPwIXnRxxYB65fbm9LBElQ54Xy7D5AG47dfyA7fsHueGjgBlXnFTUgOFtsyhYG1jNGNaiFMceAUohD9naSIMWLQMEXRiow1gqwOdBIl97Hb7_wPHw9RPq1QlQBPWJgzuJML7tCQWUdbhgzPwr6XuhGegmZfuS0R2Nk_7IEMHgEVKIYfkHPXK_pzNCsQO4baOng2B48hekrBAZl_ai9qZKQD8I9C5mi1guCGGgJPf-b5pfu2EcOdNXNb3KWY45fCNhPVjy9AvxUbZtJDg5jLYyPaxwvSqe0EBjbehr_W__PM8_H7ho89TeNcIZ7m6KeQ6Z3BREyVbqUaSVhsUtIFL3tIIs7Oh77mVHqq5LQwiSCNZlIOZxKdreZi29dNbUG9xiA2_mDJzHwNTodA7GVU9lJBfwA1wLoaspoJGszDPU7fJfx07Wa5PLhyHIYJW_jeWDf0MRYQ8wqWsCtiO7dv8S_jWdwWkwbR6RFxTMQvdneFjjbiTtB3X0gsQFF5FLrD6ZE_tjNpwIbEqV-JipcM5o1wjbXuxJUYfDBdjioZMKSVnwO01zt4k0lt4GOmgq7zSVCMF-ESfPM_gLImm4ovwVcSVFP6C3AGDnIT4oKJnjf6QPhtNEFgyp9rYX068Rntjb9WaHfL-QHSRWOkeevwiCRc1Lf88lPNZp_x2KUsqBGXPCulpN8AL9pQ94tm9vzzVrKI96m-YoTgZdVggN9DhjZ5qLYhk1dSBlMJ9I-HyQr4-GeHD5I97wskGImRFSdW9y7FAfzI9oPY3GbJ01l7mV611e8SezVdLAQrjazc37-WepDA5Yzpw_lYwTSAsRH5-OMb51gGHbculOkhAHRA7ZEWVn6bLumenmn77BC0ovmJf_0aO8-TfAv0wn2py-xQO4073_TjoLSwNg_zIHJ8Ray7bu21yGUA6cWp8gGVklJbKjswnLXKeFWP2Klq2zx0BW7vFD8fE2HykdFJTgmOP49Iy4dYimkXFLPKskovTxMk4B0T-HdcCOjMHsnrcly4KDVwYhWsdDj8fpdYbF4rm33HsM9aoCKkq_eOziMtyAlYWSKulpSpl7adSVQ7wTPvpRX4Ex0guOJVZFyHDcsucS6CDxGT4ucyaD4PCQ42jLZJv6N-Kr1lVRU5-pzc-UgKXCvW0Uu1I5OPS9-sQuj_2-S2WWcFhqC_ZTHK1vIg23qoZUHpyp4F50qrzaxFi7EXh3VdMW88IOlOr8gVkAD_TRdrRm7l158QpdI2W9HdlUpnmXU-VW2Xvr4NLrOlDZZ9-sr8iJSo5R5uQyYryBj8-BPD766FxCi-DMB5xPWwOzcMOTvKw4PhvzwGdF4RUg4w3tSZgEuQl-arSX3BGGkxkZT6_9jHS7fHBenKfHur74TImgBDyBAZGVx8ix94uI6bIg42H4-LdDPzWqR97kKeKXk-p0AG4gcmtKFGD6XP_mPloCoZD_Ill1bOu_dbgjUE7_ZznT7xzXPndyRqq5vCen9qF8Vwm_VPY6tkG-4kAVJgy90AJEHwIVABcQaFoieymfueliS3Xp3SJ_wf35DjWXmeF25lsDRcICUs2CIcTXJu5GOYrVrJV7iRCechEOuLfnoSK7PfDag5Jmpde17ydaP-_OCwL8-HzoyqOW9c2sKlqeL33pgNAh_xVpXMvZQGV1bRwiqu9H6jv97gZFtVtvlBSzWqAADy9Sgpy3iG_ysSvIQnKmjCz3cwqGYJgIRniSl7IATjQEHREXYBI2eblz30iXR4Lmp7yKJSH9PFMRpvLdvWWJdmZtZu_t7B0w-IM1yjKypS7zdiQlNPxejKFKy9JxR1jVzQdZu2onQKi1HxTSZAORLsKdrdINzPA4XzNumR0s1FOn3d4x8WlGK_nUWQVRLbxzyJ5AG2CZDPohby_MAquUpQBhclU7yiq62iBGfEX2AM_H3x23GCWEvez0185--QSPFi213Hd6qydsLmb8X0sGTpIIkTDsfFir_Fv8aTXZTkY3AZ3kRYkC-GX2t9aOJDJAuS0hWdoK8lABz3uDhaI4rZRqzO86iZ9hIzc8MCc3tHrQEY-Bj-3xwY-3H-SwAinMdIMmmsuAPJpGtT6WkT6ID65dhtcuUyn-2d3qGgbWq5wSR-Y4nTWcooLFtnb4jSqNdnyF-Ze4Ja4atfVuM6ubB7A.UAYXFNh7okvoK3gfewEieg"
        }

user_session = dict()
chatbot = Chatbot(config)

sv_help = """ gpt + 内容可以发送聊天
"""
sv = Service(
    name="chatGPT",  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # 可见性
    enable_on_default=True,  # 默认启用
    bundle="娱乐",  # 分组归类
    help_=sv_help  # 帮助说明
) 


def get_chat_response(session_id, prompt):
    if session_id in user_session:
        # 如果在三分钟内再次发起对话则使用相同的会话ID
        if time.time() < user_session[session_id]['timestamp'] + 60 * 3:
            chatbot.conversation_id = user_session[session_id]['conversation_id']
            chatbot.parent_id = user_session[session_id]['parent_id']
        else:
            chatbot.reset_chat()
    else:
        chatbot.reset_chat() 
    try:
        resp = chatbot.get_chat_response(prompt, output="text") 
        user_cache = dict()
        user_cache['timestamp'] = time.time()
        user_cache['conversation_id'] = resp['conversation_id']
        user_cache['parent_id'] = resp['parent_id']
        user_session[session_id] = user_cache

        return resp['message']
    except Exception as e:
        return f"发生错误: {str(e)}"
 
@sv.on_message()
async def random_resp(bot, ev):
    if(random.random() < 0.2):
        sv.logger.info(
        f"Message {ev.message_id} triggered 'random_resp'"
    )
        await chatGPT_method(bot,ev)


@sv.on_prefix(("gpt"))
async def chatGPT_method(bot, ev): 
    uid = ev.user_id
    gid = ev.group_id
    name = ev.sender['nickname'] 
    msg = str(ev.message.extract_plain_text()).strip()
    resp = await asyncio.get_event_loop().run_in_executor(None, get_chat_response, uid, msg)
    await bot.send(ev, resp, at_sender = True)

 # 定时刷新seesion_token
@sv.scheduled_job("interval", minutes=10)
async def refresh_session(): 
    chatbot.refresh_session()