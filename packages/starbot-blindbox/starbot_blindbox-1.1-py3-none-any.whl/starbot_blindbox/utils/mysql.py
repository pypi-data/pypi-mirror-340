import datetime
from math import trunc

import aiomysql
import traceback
from loguru import logger
from starbot.utils import config
import re


class Mysql:
    db = None

    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306, loop=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.loop = loop
        self.pool = None

    # 创建连接池
    async def connect(self):
        try:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.database,
                loop=self.loop,
                autocommit=True
            )
        except:
            print(f"connect error:{traceback.format_exc()}")

    # 测试
    async def test(self):
        await self.execute(f"use {self.database}")

    # 关闭连接池
    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()

    # 执行一条非查询类语句
    async def execute(self, query: str, args: tuple = None) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                return cur.rowcount

    # 批量执行非查询类语句
    async def executemany(self, query: str, args: list = None) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.executemany(query, args)
                return cur.rowcount

    # 查询单条数据
    async def fetchone(self, query: str, args: tuple = None) -> dict:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                return await cur.fetchone()

    # 查询多条数据
    async def fetchall(self, query: str, args=None) -> list:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                return await cur.fetchall()

    # 封装单条插入
    async def insert(self, table: str, data: dict) -> int:
        """
        :param table: 表名
        :param data: 数据
        :return:
        """
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        try:
            return await self.execute(query, tuple(data.values()))
        except:
            print(f"execute {query} with {data} failed, error{traceback.format_exc()}")
            return 0

    # 封装批量插入
    async def insert_many(self, table: str, data_list: list) -> int:
        """
        :param table: 表名
        :param data_list: 数据列表
        :return:
        """
        keys = ','.join(data_list[0].keys())
        values = ','.join(['%s'] * len(data_list[0]))
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        args = [tuple(data.values()) for data in data_list]
        try:
            return await self.executemany(query, args)
        except:
            print(f"execute {query} with {args} failed, error{traceback.format_exc()}")
            return 0

    # 封装单条插入
    async def upsert(self, table: str, data: dict) -> int:
        """
        :param table: 表名
        :param data: 数据
        :return:
        """
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        query = f'REPLACE INTO {table} ({keys}) VALUES ({values})'
        try:
            return await self.execute(query, tuple(data.values()))
        except:
            print(f"execute {query} with {data} failed, error{traceback.format_exc()}")
            return 0

def is_can_use():
    if not Mysql.db:
        return False
    if not Mysql.db.pool:
        return False
    return True

async def init():
    host = config.get("MYSQL_HOST")
    port = config.get("MYSQL_PORT")
    db = config.get("MYSQL_DB")
    logger.info(f"开始连接 Mysql 数据库, {host}:{port}/{db}")
    username = config.get("MYSQL_USERNAME")
    password = config.get("MYSQL_PASSWORD")
    Mysql.db = Mysql(host, username, password, db, port)
    try:
        await Mysql.db.connect()
        await Mysql.db.test()
    except Exception as ex:
        raise ValueError(f"连接 Mysql 数据库失败, 请检查是否启动了 Mysql 服务或提供的配置中连接参数是否正确 {ex}")
    logger.success("成功连接 Mysql 数据库")

async def init_sql():
    table_name = "bot_blind_box"
    tables = await Mysql.db.fetchall("show tables;")
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name not in table_list:
        logger.success("开始创建 Mysql 表")
        create_sql = """
            create table if not exists bot_blind_box(
                `id` int AUTO_INCREMENT PRIMARY KEY,
                `gift_id` int comment '礼物id',
                `gift_name` varchar(50) comment '礼物名称',
                `user_id` bigint comment '用户id',
                `room_id` bigint comment '直播间id',
                `up_id` bigint comment '主播id',
                `num` int    comment '数量',
                `box_gift_id` int comment '盒子id',
                `box_gift_name` varchar(50) comment '盒子名称',
                `discount_price` int comment '单价(分)',
                `total_discount_price` int comment '总价(分)',
                `total_pay_price` int  comment '支付总价(分)',
                `total_profile` int  comment '盈亏(分)',
                `tick` int  comment '时间戳',
                `date` datetime  comment '时间',
                KEY `gift_id` (`gift_id`) USING BTREE,
                KEY `box_gift_id` (`box_gift_id`) USING BTREE,
                KEY `user_id` (`user_id`) USING BTREE,
                KEY `room_id` (`room_id`) USING BTREE,
                KEY `up_id` (`up_id`) USING BTREE
            ) CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
        """
        await Mysql.db.execute(create_sql)

    logger.success("创建 Mysql 表成功")

async def insert_gift(room_id, up_id, base):
    # 礼物统计
    gift_num = base["num"]
    giftId = base['giftId']
    now = datetime.datetime.now()
    if base["blind_gift"] is not None:
        box_price = base["total_coin"] // 10
        gift_price = base["discount_price"] // 10
        profit = trunc(gift_price * gift_num) - box_price

        data = dict()
        data["gift_id"] = giftId
        data["gift_name"] = base["giftName"]
        data["user_id"] = base["uid"]
        data["room_id"] = room_id
        data["up_id"] = up_id
        data["box_gift_id"] = base['blind_gift']['original_gift_id']
        data["box_gift_name"] = base['blind_gift']['original_gift_name']
        data["num"] = gift_num
        data["discount_price"] = gift_price
        data["total_discount_price"] = trunc(gift_price * gift_num)
        data["total_pay_price"] = box_price
        data["total_profile"] = profit
        data['tick'] = int(now.timestamp())
        data['date'] = now
        await Mysql.db.insert("bot_blind_box", data)

async def get_room_blind_data_params(start, end, room_id, my_uid=0):
    """
    获取盲盒数据
    Args:
        room_id : 房间id
    """
    if my_uid == 0:
        sql = f"select gift_id, gift_name, box_gift_id, box_gift_name, sum(total_profile) as profile, sum(num) as num from bot_blind_box where `tick`>={start} and `tick`<{end} and room_id={room_id} group by gift_id, gift_name, box_gift_id, box_gift_name order by profile desc"
    else:
        sql = f"select gift_id, gift_name, box_gift_id, box_gift_name, sum(total_profile) as profile, sum(num) as num from bot_blind_box where `tick`>={start} and `tick`<{end} and room_id={room_id} and user_id={my_uid} group by gift_id, gift_name, box_gift_id, box_gift_name order by profile desc"
    data = await Mysql.db.fetchall(sql)
    gift_count = []
    gift_ids = []
    gift_names = []
    gift_desc = []

    box_gift_counts = []
    box_gift_ids = []
    box_gift_names = []
    box_gift_desc = []

    total_profit = 0
    box_count_dict = {}
    for v in data:
        gift_id = int(v.get('gift_id'))
        gift_name = v.get('gift_name')
        box_gift_id = int(v.get('box_gift_id'))
        box_gift_name = v.get('box_gift_name')

        profile = round(int(v.get('profile'))/100, 1)
        count = int(v.get('num'))
        if (box_gift_id, box_gift_name) not in box_count_dict:
            box_count_dict[(box_gift_id, box_gift_name)] = 0
        box_count_dict[(box_gift_id, box_gift_name)] += count

        total_profit += profile
        gift_count.append(profile)
        gift_names.append(gift_name)
        gift_ids.append(gift_id)
        gift_desc.append(str(count)+"个")


    for k, v in sorted(box_count_dict.items(), key=lambda d:d[1], reverse=True):
        gift_id, gift_name = k
        box_gift_counts.append(v)
        box_gift_names.append(gift_name)
        box_gift_ids.append(gift_id)
    params = {
        "is_space": len(gift_count)==0,
        "gift_counts": gift_count,
        "gift_names": gift_names,
        "gift_ids": gift_ids,
        "box_gift_counts": box_gift_counts,
        "box_gift_names": box_gift_names,
        "box_gift_ids": box_gift_ids,
        "gift_descs": gift_desc,
        "total_profit": total_profit
    }
    return params