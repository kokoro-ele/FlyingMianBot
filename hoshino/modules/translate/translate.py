from functools import total_ordering
from unicodedata import name
from nonebot import on_command, CommandSession
from nonebot import permission as perm
from sqlalchemy import null


from sogou_tr.sogou_tr import sogou_tr
from datetime import datetime, timedelta

# sogou_tr使用帮助：
# print(sogou_tr('hello world'))  # -> '你好世界'
# print(sogou_tr('hello world', to_lang='de'))  # ->'Hallo Welt'
# print(sogou_tr('hello world', to_lang='fr'))  # ->'Salut tout le monde'
# print(sogou_tr('hello world', to_lang='ja'))  # ->'ハローワールド'


@on_command('translate', aliases=('翻译', '翻譯', '翻訳'), permission=perm.GROUP_ADMIN, only_to_me=False)
async def translate(session: CommandSession):
    if session.state['success'] == 0:
        await session.send('缺少语言种类或文本哦！')
    elif session.state['success'] == 1:
        tolang = session.get('tolang')
        await session.send(f'{tolang}不支持的语言种类捏！')
    elif session.state['success'] == -1:
        await session.send('翻译姬待命中捏！')    
    else:
        tolang = session.get('tolang')
        text = session.get('text')
        translation = await get_translation(text,tolang)
        if translation:
            await session.send(f'机翻译文：\n{translation}')
        else:
            await session.send("纳尼！搜狗翻译寄了捏...")


@translate.args_parser
async def _(session: CommandSession):
    names = session.current_arg_text.split()
    if len(names) == 1:
        session.state['success'] = 0
        return 
    elif len(names) == 0:
        session.state['success'] = -1
        return
    else:
        session.state['text'] = names[1]
        if(names[0] == '英文' or names[0] == '英语' ):
            session.state['tolang'] = 'en'
        elif(names[0] == '日语' or names[0] == '日文'):
            session.state['tolang'] = 'ja'
        elif(names[0] == '中文' or names[0] == '汉语'):
            session.state['tolang'] = 'zh'
        else:
            session.state['tolang'] = names[0]
            session.state['success'] = 1
        session.state['success'] = 2    
        return


async def get_translation(text: str,tolang: str) -> str:
    if not hasattr(get_translation, 'cdtime'):
        get_translation.cdtime = datetime.now() - timedelta(seconds=3)
    now = datetime.now()
    if(now < get_translation.cdtime):
        return '翻译姬冷却中...'
    else:
        get_translation.cdtime = datetime.now() + timedelta(seconds=1)
        try:
            print(text)
            ret = sogou_tr(text,to_lang = tolang)
            print(ret)
            # print(sogou_tr.json)
            return ret
        except:
            return null
