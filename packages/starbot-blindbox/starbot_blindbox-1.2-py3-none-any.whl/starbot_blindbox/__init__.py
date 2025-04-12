from loguru import logger

from .utils import mysql
from starbot.utils import redis, config
from starbot.core.room import Up
from starbot.utils.utils import get_session
import json

VER = "v1.2"


def register():
    """
        注册插件
    """
    try:
        __register_mysql()
    except Exception as ex:
        logger.error(f"盲盒插件未成功启用, {ex}")
    pass


# 注册mysql
def __register_mysql():
    old_init = redis.init
    async def init():
        await old_init()
        await __init()

    redis.init = init


async def __init():
    """
        初始化
    """
    try:
        await __check_update()
        await mysql.init()
        await mysql.init_sql()
        await mysql.get_room_blind_data_params(1, 99999999999, 1, 1)
        __register_room()
        logger.success(f"盲盒插件成功启用")
    except Exception as ex:
        logger.error(f"盲盒插件未成功启用, {ex}")
    pass

# 注册礼物事件
def __register_room():
    old_connect = Up.connect

    async def connect(self):
        await old_connect(self)
        @self._Up__room.on("SEND_GIFT")
        async def on_gift(event):
            """
            礼物事件
            """
            base = event["data"]["data"]
            # 盲盒统计
            if base["blind_gift"] is not None:
                await mysql.insert_gift(self.room_id, self.uid, base)

    Up.connect = connect
    pass

async def __check_update():
    if config.get("CHECK_VERSION"):
        try:
            response = await get_session().get("https://mirrors.cloud.tencent.com/pypi/json/starbot-blindbox")
            data = await response.text()
            latest_version = json.loads(data)["info"]["version"]
            if latest_version != VER.replace("v", ""):
                logger.warning(f"检测到 starBot-blindbox-plugin 新版本 v{latest_version}, 建议升级到最新版本, "
                               "升级内容和升级注意事项请参阅官网或 Github 页的迁移指南")
                cmd = "pip install -i https://mirrors.cloud.tencent.com/pypi/simple --upgrade starbot-blindbox=="
                logger.warning(f"升级命令: {cmd}{latest_version}")
        except Exception:
            logger.error("获取 starBot-blindbox-plugin 最新版本失败")