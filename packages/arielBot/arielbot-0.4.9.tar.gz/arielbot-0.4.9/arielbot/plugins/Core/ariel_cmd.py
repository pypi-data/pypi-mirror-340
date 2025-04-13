from nonebot import on_command,on_regex
from nonebot.adapters import Bot
from nonebot.adapters import Message
from nonebot.params import CommandArg,RegexStr
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import GROUP_ADMIN
from nonebot.adapters.onebot.v11 import GROUP_OWNER
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from arielbot.plugins.Core.ariel_tools import *
import re

from arielbot.plugins.Core.ariel_tools import LoginTools
from arielbot.plugins.Core.ariel_rule import bot_is_active
from arielbot.plugins.Core.ariel_push import DynPusher



login = on_command("login", aliases={"登录"}, permission=SUPERUSER)

add_sub = on_command("sub", rule=bot_is_active, aliases={"订阅"}, permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)
del_sub = on_command("unsub",  rule=bot_is_active, aliases={"删除"}, permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)

live_active = on_command("live_on", rule=bot_is_active, permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)
live_deactivate = on_command("live_off", rule=bot_is_active, permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)

dyn_active = on_command("dyn_on", rule=bot_is_active, permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)
dyn_deactivate = on_command("dyn_off", rule=bot_is_active, permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)

bot_active = on_command("bot_on", permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)
bot_deactivate = on_command("bot_off", permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)

sub_list = on_command("list",  rule=bot_is_active, aliases={"列表"})
bot_help = on_command("help")

b23 = on_regex(r"(https?://b23\.tv/[\w-]+)(?=[^\w-]|$)", flags=re.IGNORECASE)
s_dyn = on_command("sd")

get_img = on_command("img")

@get_img.handle()
async def _(event:GroupMessageEvent,args: Message = CommandArg()):
    if args.extract_plain_text() and args.extract_plain_text().isdigit():
        message = await DynPusher.search_dyn_img_by_id(args.extract_plain_text())
        if message is None:
            await get_img.finish()
        else:
            await get_img.finish(message)
    else:
        await get_img.finish()


@s_dyn.handle()
async def _(event:GroupMessageEvent,args: Message = CommandArg()):
    if args.extract_plain_text() and args.extract_plain_text().isdigit():
        dyn_img = await DynPusher.search_dyn_by_id(args.extract_plain_text())
        if dyn_img is None:
            await s_dyn.finish()
        else:
            await s_dyn.finish(dyn_img)
    else:
        await s_dyn.finish()


@b23.handle()
async def _(event:GroupMessageEvent,param:str = RegexStr ()):
    print(param)
    if param:
        dyn_img = await DynPusher.push_short_link_dynamic(param)
        if dyn_img is None:
            await b23.finish()
        else:
            await b23.finish(dyn_img)
    else:
        await b23.finish()

@login.handle()
async def _(bot:Bot,event:GroupMessageEvent):
    login_handler = LoginTools()
    await login_handler.login_handle(bot, event)
    await login.finish()

@add_sub.handle()
async def _(event:GroupMessageEvent, args: Message = CommandArg()):
    if args.extract_plain_text() and args.extract_plain_text().isdigit():
        add_sub_processor = AddSubTools(args.extract_plain_text())
        result = await add_sub_processor.add_sub_processor(event)
        await add_sub.finish(result)
    else:
        await add_sub.finish("请携带正确的uid后重试")

@del_sub.handle()
async def _(event:GroupMessageEvent, args: Message = CommandArg()):
    if args.extract_plain_text() and args.extract_plain_text().isdigit():
        del_sub_processor = DelSubTools(args.extract_plain_text())
        result = await del_sub_processor.del_sub_processor(event)
        await del_sub.finish(result)
    else:
        await del_sub.finish("请携带正确的uid后重试")


@live_active.handle()
async def _(event:GroupMessageEvent, args: Message = CommandArg()):
    if args.extract_plain_text() and args.extract_plain_text().isdigit():
        live_active_processor = UpdateSubTools(args.extract_plain_text())
        result = await live_active_processor.update_sub_handler(event,1)
        await live_active.finish(result)
    else:
        await live_active.finish("请携带正确的uid后重试")
    
@live_deactivate.handle()
async def _(event:GroupMessageEvent, args: Message = CommandArg()):
    if args.extract_plain_text() and args.extract_plain_text().isdigit():
        live_deactivate_processor = UpdateSubTools(args.extract_plain_text())
        result = await live_deactivate_processor.update_sub_handler(event,0)
        await live_deactivate.finish(result)
    else:
        await live_deactivate.finish("请携带正确的uid后重试")

@dyn_active.handle()
async def _(event:GroupMessageEvent, args: Message = CommandArg()):
    if args.extract_plain_text() and args.extract_plain_text().isdigit():
        dyn_active_processor = UpdateSubTools(args.extract_plain_text())
        result = await dyn_active_processor.update_sub_handler(event,dyn_active=1)
        await dyn_active.finish(result)
    else:
        await dyn_active.finish("请携带正确的uid后重试")
        
@dyn_deactivate.handle()
async def _(event:GroupMessageEvent, args: Message = CommandArg()):
    if args.extract_plain_text() and args.extract_plain_text().isdigit():
        dyn_deactivate_processor = UpdateSubTools(args.extract_plain_text())
        result = await dyn_deactivate_processor.update_sub_handler(event,dyn_active=0)
        await dyn_deactivate.finish(result)
    else:
        await dyn_deactivate.finish("请携带正确的uid后重试")

@bot_active.handle()
async def _(event:GroupMessageEvent):
    bot_active_processor = UpdateBotStatusTools()
    result = await bot_active_processor.update_bot_status_processor(event,1)
    await bot_active.finish(result)

@bot_deactivate.handle()
async def _(event:GroupMessageEvent):
    bot_deactivate_processor = UpdateBotStatusTools()
    result = await bot_deactivate_processor.update_bot_status_processor(event,0)
    if result is None:
        await bot_deactivate.finish()
    else:
        await bot_deactivate.finish(result)

@bot_help.handle()
async def _():
    await bot_help.finish(MessageSegment.image("https://i0.hdslb.com/bfs/new_dyn/abef945ad1d209ad1d2360624180a15d490040351.png"))

@sub_list.handle()
async def _(event:GroupMessageEvent):
    sub_list_processor = SubListTools()
    img = await sub_list_processor.get_sub_list_data(event)
    await sub_list.finish(img)
    

