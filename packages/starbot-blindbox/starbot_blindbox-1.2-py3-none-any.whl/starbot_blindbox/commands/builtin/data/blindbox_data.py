import re
from datetime import datetime, timedelta
from typing import Union, Optional

from graia.ariadne import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Source, At
from graia.ariadne.message.parser.twilight import Twilight, FullMatch, ElementMatch, UnionMatch, RegexMatch, ResultValue
from graia.ariadne.model import Friend, Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from loguru import logger

from starbot.core.datasource import DataSource
from starbot.core.model import PushType
from starbot.utils import config, redis
from ....utils import mysql
from starbot.utils.utils import get_unames_and_faces_by_uids, remove_command_param_placeholder


from ....painter.BlindBoxGenerator import BlindBoxGenerator

prefix = config.get("COMMAND_PREFIX")

channel = Channel.current()


async def get_blind_data(app, source, sender, title, up, startTick, endTick):
    params = await mysql.get_room_blind_data_params(startTick, endTick, up.room_id)
    uname, face = await get_unames_and_faces_by_uids([str(up.uid)])
    params['uname'] = uname[0]
    params['face'] = face[0]
    params['room_id'] = up.room_id
    params["up"] = up
    params["last_tick"] = startTick
    params['title'] = title
    data = await BlindBoxGenerator.generate(params)
    await app.send_message(sender, MessageChain(Image(base64=data)))


async def get_my_blind_data(app, source, sender, title, up, myUid, startTick, endTick):
    params = await mysql.get_room_blind_data_params(startTick, endTick, up.room_id, myUid)
    uname, face = await get_unames_and_faces_by_uids([str(myUid)])
    params['uname'] = uname[0]
    params['face'] = face[0]
    params['room_id'] = up.room_id
    params["up"] = up
    params["last_tick"] = startTick
    params["my_uid"] = myUid
    params['title'] = title
    data = await BlindBoxGenerator.generate(params)
    await app.send_message(sender, MessageChain(Image(base64=data)))


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage, GroupMessage],
        inline_dispatchers=[Twilight(
            ElementMatch(At, optional=True),
            FullMatch(prefix),
            UnionMatch("盲盒数据")
        )],
    )
)
async def blind_data(app: Ariadne, source: Source, sender: Union[Friend, Group]):
    logger.info(f"{'群' if isinstance(sender, Group) else '好友'}[{sender.id}] 触发命令 : 盲盒数据")

    if not mysql.is_can_use():
        logger.info(f"未激活盲盒插件")
        return

    datasource: DataSource = app.options["StarBotDataSource"]
    ups = datasource.get_ups_by_target(sender.id, PushType.Group if isinstance(sender, Group) else PushType.Friend)

    if not ups:
        if isinstance(sender, Group):
            await app.send_message(sender, MessageChain("本群未关联直播间~"), quote=source)
        else:
            await app.send_message(sender, MessageChain("此处未关联直播间~"), quote=source)
        return

    for up in ups:
        startTick = await redis.get_live_start_time(up.room_id)
        endTick = 9999999999
        if not startTick:
            now = datetime.now()
            startTick = int(datetime(now.year, now.month, now.day).timestamp())

        await get_blind_data(app, source, sender, "盲盒数据", up, startTick, endTick)


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage, GroupMessage],
        inline_dispatchers=[Twilight(
            ElementMatch(At, optional=True),
            FullMatch(prefix),
            UnionMatch("今日盲盒数据", "今日盲盒", "今天盲盒", "今天盲盒数据")
        )],
    )
)
async def daily_blind_data(app: Ariadne, source: Source, sender: Union[Friend, Group]):
    logger.info(f"{'群' if isinstance(sender, Group) else '好友'}[{sender.id}] 触发命令 : 今日盲盒")

    # if isinstance(sender, Group) and await redis.exists_disable_command("DenyRoomData", sender.id):
    #     await app.send_message(sender, MessageChain("此命令已被禁用~"), quote=source)
    #     return
    if not mysql.is_can_use():
        logger.info(f"未激活盲盒插件")
        return

    datasource: DataSource = app.options["StarBotDataSource"]
    ups = datasource.get_ups_by_target(sender.id, PushType.Group if isinstance(sender, Group) else PushType.Friend)

    if not ups:
        if isinstance(sender, Group):
            await app.send_message(sender, MessageChain("本群未关联直播间~"), quote=source)
        else:
            await app.send_message(sender, MessageChain("此处未关联直播间~"), quote=source)
        return

    for up in ups:
        now = datetime.now()
        startTick = int(datetime(now.year, now.month, now.day).timestamp())
        endTick = startTick+24*3600
        await get_blind_data(app, source, sender, "今日盲盒数据", up, startTick, endTick)


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage, GroupMessage],
        inline_dispatchers=[Twilight(
            ElementMatch(At, optional=True),
            FullMatch(prefix),
            UnionMatch("我的盲盒", "我的盲盒数据")
        )],
    )
)
async def my_blind_data(app: Ariadne, source: Source, sender: Union[Friend, Group], member: Optional[Member]):
    logger.info(f"{'群' if isinstance(sender, Group) else '好友'}[{sender.id}] 触发命令 : 我的盲盒")

    if not mysql.is_can_use():
        logger.info(f"未激活盲盒插件")
        return

    datasource: DataSource = app.options["StarBotDataSource"]
    ups = datasource.get_ups_by_target(sender.id, PushType.Group if isinstance(sender, Group) else PushType.Friend)

    if not ups:
        if isinstance(sender, Group):
            await app.send_message(sender, MessageChain("本群未关联直播间~"), quote=source)
        else:
            await app.send_message(sender, MessageChain("此处未关联直播间~"), quote=source)
        return

    if isinstance(sender, Friend):
        qq = sender.id
    else:
        qq = member.id
    uid = await redis.get_bind_uid(qq)

    if not uid:
        await app.send_message(
            sender, MessageChain(f"请先使用\"{prefix}绑定 [UID]\"命令绑定B站UID后再查询~\n命令示例:{prefix}绑定 114514")
        )
        return

    for up in ups:
        now = datetime.now()
        startTick = await redis.get_live_start_time(up.room_id)
        endTick = 9999999999
        if not startTick:
            now = datetime.now()
            startTick = int(datetime(now.year, now.month, now.day).timestamp())
        await get_my_blind_data(app, source, sender, "盲盒数据", up, uid, startTick, endTick)


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage, GroupMessage],
        inline_dispatchers=[Twilight(
            ElementMatch(At, optional=True),
            FullMatch(prefix),
            UnionMatch("我的今日盲盒数据", "我的今日盲盒", "我的今天盲盒", "我的今天盲盒数据")
        )],
    )
)
async def my_daily_blind_data(app: Ariadne, source: Source, sender: Union[Friend, Group], member: Optional[Member]):
    logger.info(f"{'群' if isinstance(sender, Group) else '好友'}[{sender.id}] 触发命令 : 我的今日盲盒")

    if not mysql.is_can_use():
        logger.info(f"未激活盲盒插件")
        return

    datasource: DataSource = app.options["StarBotDataSource"]
    ups = datasource.get_ups_by_target(sender.id, PushType.Group if isinstance(sender, Group) else PushType.Friend)

    if not ups:
        if isinstance(sender, Group):
            await app.send_message(sender, MessageChain("本群未关联直播间~"), quote=source)
        else:
            await app.send_message(sender, MessageChain("此处未关联直播间~"), quote=source)
        return

    if isinstance(sender, Friend):
        qq = sender.id
    else:
        qq = member.id
    uid = await redis.get_bind_uid(qq)

    if not uid:
        await app.send_message(
            sender, MessageChain(f"请先使用\"{prefix}绑定 [UID]\"命令绑定B站UID后再查询~\n命令示例:{prefix}绑定 114514")
        )
        return

    for up in ups:
        now = datetime.now()
        startTick = int(datetime(now.year, now.month, now.day).timestamp())
        endTick = startTick+24*3600
        await get_my_blind_data(app, source, sender, "今日盲盒数据", up, uid, startTick, endTick)

@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage, GroupMessage],
        inline_dispatchers=[Twilight(
            ElementMatch(At, optional=True),
            FullMatch(prefix),
            UnionMatch("昨天盲盒数据", "昨日盲盒数据", "昨天盲盒", "昨日盲盒")
        )],
    )
)
async def blind_data_before(app: Ariadne, source: Source, sender: Union[Friend, Group]):
    logger.info(f"{'群' if isinstance(sender, Group) else '好友'}[{sender.id}] 触发命令 : 盲盒数据")

    if not mysql.is_can_use():
        logger.info(f"未激活盲盒插件")
        return

    datasource: DataSource = app.options["StarBotDataSource"]
    ups = datasource.get_ups_by_target(sender.id, PushType.Group if isinstance(sender, Group) else PushType.Friend)

    if not ups:
        if isinstance(sender, Group):
            await app.send_message(sender, MessageChain("本群未关联直播间~"), quote=source)
        else:
            await app.send_message(sender, MessageChain("此处未关联直播间~"), quote=source)
        return

    for up in ups:
        now = datetime.now()-timedelta(days=1)
        startTick = int(datetime(now.year, now.month, now.day).timestamp())
        endTick = startTick+24*3600
        await get_blind_data(app, source, sender, "昨日盲盒数据", up, startTick, endTick)


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage, GroupMessage],
        inline_dispatchers=[Twilight(
            ElementMatch(At, optional=True),
            FullMatch(prefix),
            UnionMatch("昨日我的盲盒", "昨天我的盲盒数据", "我的昨日盲盒数据", "我的昨天盲盒数据", "我的昨天盲盒", "我的昨日盲盒")
        )],
    )
)
async def my_blind_data_before(app: Ariadne, source: Source, sender: Union[Friend, Group], member: Optional[Member]):
    logger.info(f"{'群' if isinstance(sender, Group) else '好友'}[{sender.id}] 触发命令 : 我的盲盒")

    if not mysql.is_can_use():
        logger.info(f"未激活盲盒插件")
        return

    datasource: DataSource = app.options["StarBotDataSource"]
    ups = datasource.get_ups_by_target(sender.id, PushType.Group if isinstance(sender, Group) else PushType.Friend)

    if not ups:
        if isinstance(sender, Group):
            await app.send_message(sender, MessageChain("本群未关联直播间~"), quote=source)
        else:
            await app.send_message(sender, MessageChain("此处未关联直播间~"), quote=source)
        return

    if isinstance(sender, Friend):
        qq = sender.id
    else:
        qq = member.id
    uid = await redis.get_bind_uid(qq)

    if not uid:
        await app.send_message(
            sender, MessageChain(f"请先使用\"{prefix}绑定 [UID]\"命令绑定B站UID后再查询~\n命令示例:{prefix}绑定 114514")
        )
        return

    for up in ups:
        now = datetime.now() - timedelta(days=1)
        startTick = int(datetime(now.year, now.month, now.day).timestamp())
        endTick = startTick+24*3600
        await get_my_blind_data(app, source, sender, "昨日盲盒数据", up, uid, startTick, endTick)


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage, GroupMessage],
        inline_dispatchers=[Twilight(
            ElementMatch(At, optional=True),
            FullMatch(prefix),
            "monthChain" @ RegexMatch(r"\d+月盲盒(数据)?")
        )],
    )
)
async def blind_data_month(app: Ariadne, source: Source, sender: Union[Friend, Group], member: Optional[Member],
               monthChain: MessageChain = ResultValue()):
    logger.info(f"{'群' if isinstance(sender, Group) else '好友'}[{sender.id}] 触发命令 : {monthChain}")
    if not mysql.is_can_use():
        logger.info(f"未激活盲盒插件")
        return

    monthStr = remove_command_param_placeholder(monthChain.display)
    match = re.search(r'\d+', monthStr)
    if match:
        month = int(match.group())
    else:
        return
    if month <= 0 or month >12:
        return

    datasource: DataSource = app.options["StarBotDataSource"]
    ups = datasource.get_ups_by_target(sender.id, PushType.Group if isinstance(sender, Group) else PushType.Friend)

    if not ups:
        if isinstance(sender, Group):
            await app.send_message(sender, MessageChain("本群未关联直播间~"), quote=source)
        else:
            await app.send_message(sender, MessageChain("此处未关联直播间~"), quote=source)
        return

    for up in ups:
        now = datetime.now()
        startTick = int(datetime(now.year, month, 1).timestamp())
        if month == 12:
            endTick = int(datetime(now.year+1, 1, 1).timestamp())
        else:
            endTick = int(datetime(now.year, month+1, 1).timestamp())
        await get_blind_data(app, source, sender, f"{month}月盲盒", up, startTick, endTick)


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage, GroupMessage],
        inline_dispatchers=[Twilight(
            ElementMatch(At, optional=True),
            FullMatch(prefix),
            "monthChain" @ RegexMatch(r"我的\d+月盲盒(数据)?")
        )],
    )
)
async def my_blind_data_month(app: Ariadne, source: Source, sender: Union[Friend, Group], member: Optional[Member],
               monthChain: MessageChain = ResultValue()):
    logger.info(f"{'群' if isinstance(sender, Group) else '好友'}[{sender.id}] 触发命令 : {monthChain}")
    if not mysql.is_can_use():
        logger.info(f"未激活盲盒插件")
        return

    monthStr = remove_command_param_placeholder(monthChain.display)
    match = re.search(r'\d+', monthStr)
    if match:
        month = int(match.group())
    else:
        return
    if month <= 0 or month >12:
        return

    datasource: DataSource = app.options["StarBotDataSource"]
    ups = datasource.get_ups_by_target(sender.id, PushType.Group if isinstance(sender, Group) else PushType.Friend)

    if not ups:
        if isinstance(sender, Group):
            await app.send_message(sender, MessageChain("本群未关联直播间~"), quote=source)
        else:
            await app.send_message(sender, MessageChain("此处未关联直播间~"), quote=source)
        return

    if isinstance(sender, Friend):
        qq = sender.id
    else:
        qq = member.id
    uid = await redis.get_bind_uid(qq)

    if not uid:
        await app.send_message(
            sender, MessageChain(f"请先使用\"{prefix}绑定 [UID]\"命令绑定B站UID后再查询~\n命令示例:{prefix}绑定 114514")
        )
        return

    for up in ups:
        now = datetime.now()
        startTick = int(datetime(now.year, month, 1).timestamp())
        if month == 12:
            endTick = int(datetime(now.year+1, 1, 1).timestamp())
        else:
            endTick = int(datetime(now.year, month+1, 1).timestamp())

        await get_my_blind_data(app, source, sender, f"{month}月盲盒", up, uid, startTick, endTick)


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage, GroupMessage],
        inline_dispatchers=[Twilight(
            ElementMatch(At, optional=True),
            FullMatch(prefix),
            "weekChain" @ UnionMatch("本周盲盒", "上周盲盒", "本周盲盒数据", "上周盲盒数据")
        )],
    )
)
async def week_blind_data_month(app: Ariadne, source: Source, sender: Union[Friend, Group], member: Optional[Member],
                           weekChain: MessageChain = ResultValue()):
    logger.info(f"{'群' if isinstance(sender, Group) else '好友'}[{sender.id}] 触发命令 : {weekChain}")
    if not mysql.is_can_use():
        logger.info(f"未激活盲盒插件")
        return

    monthStr = remove_command_param_placeholder(weekChain.display)
    if "本周" in monthStr:
        subSecond = 0
    else:
        subSecond = 7*24*3600

    datasource: DataSource = app.options["StarBotDataSource"]
    ups = datasource.get_ups_by_target(sender.id, PushType.Group if isinstance(sender, Group) else PushType.Friend)

    if not ups:
        if isinstance(sender, Group):
            await app.send_message(sender, MessageChain("本群未关联直播间~"), quote=source)
        else:
            await app.send_message(sender, MessageChain("此处未关联直播间~"), quote=source)
        return

    for up in ups:
        now = datetime.now()
        startTick = (datetime(now.year, now.month, now.day) - timedelta(days=now.weekday())).timestamp() - subSecond
        endTick = startTick + 7*24*3600
        weekStr = "上周" if subSecond > 0 else "本周"
        await get_blind_data(app, source, sender, f"{weekStr}盲盒", up, startTick, endTick)


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage, GroupMessage],
        inline_dispatchers=[Twilight(
            ElementMatch(At, optional=True),
            FullMatch(prefix),
            "weekChain" @ UnionMatch("我的本周盲盒", "我的上周盲盒", "我的本周盲盒数据", "我的上周盲盒数据")
        )],
    )
)
async def my_week_blind_data_month(app: Ariadne, source: Source, sender: Union[Friend, Group], member: Optional[Member],
                              weekChain: MessageChain = ResultValue()):
    logger.info(f"{'群' if isinstance(sender, Group) else '好友'}[{sender.id}] 触发命令 : {weekChain}")
    if not mysql.is_can_use():
        logger.info(f"未激活盲盒插件")
        return

    monthStr = remove_command_param_placeholder(weekChain.display)
    if "本周" in monthStr:
        subSecond = 0
    else:
        subSecond = 7*24*3600

    datasource: DataSource = app.options["StarBotDataSource"]
    ups = datasource.get_ups_by_target(sender.id, PushType.Group if isinstance(sender, Group) else PushType.Friend)

    if not ups:
        if isinstance(sender, Group):
            await app.send_message(sender, MessageChain("本群未关联直播间~"), quote=source)
        else:
            await app.send_message(sender, MessageChain("此处未关联直播间~"), quote=source)
        return

    if isinstance(sender, Friend):
        qq = sender.id
    else:
        qq = member.id
    uid = await redis.get_bind_uid(qq)

    if not uid:
        await app.send_message(
            sender, MessageChain(f"请先使用\"{prefix}绑定 [UID]\"命令绑定B站UID后再查询~\n命令示例:{prefix}绑定 114514")
        )
        return

    for up in ups:
        now = datetime.now()
        startTick = (datetime(now.year, now.month, now.day) - timedelta(days=now.weekday())).timestamp() - subSecond
        endTick = startTick + 7 * 24 * 3600
        weekStr = "上周" if subSecond > 0 else "本周"
        await get_my_blind_data(app, source, sender, f"{weekStr}盲盒", up, uid, startTick, endTick)