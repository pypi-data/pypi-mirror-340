import asyncio
import os
from io import BytesIO
from typing import Dict, Any, List, Union, Tuple, Optional

from PIL import Image, ImageDraw
from loguru import logger
import starbot
import inspect
from starbot.painter.PicGenerator import Color, PicGenerator
from starbot.utils.utils import mask_round, timestamp_format
import time
from starbot.core.live import get_gift_config
from starbot.utils.utils import get_session


class BlindBoxGenerator:
    """
    直播报告生成器
    """
    cache_gift_name_and_url = {}
    cache_gift_png = {}

    @classmethod
    async def generate(cls, param: Dict[str, Any]) -> str:
        """
        根据传入直播报告参数生成直播报告图片

        Args:
            param: 直播报告参数

        Returns:
            直播报告图片的 Base64 字符串
        """
        width = 1000
        height = 100000
        top_blank = 75
        margin = 50


        async def get_gift_face(gift_id):
            if gift_id in BlindBoxGenerator.cache_gift_png:
                image_data = BlindBoxGenerator.cache_gift_png[gift_id]
                return Image.open(BytesIO(image_data))
            elif gift_id in BlindBoxGenerator.cache_gift_name_and_url:
                name, url = BlindBoxGenerator.cache_gift_name_and_url[gift_id]
                logger.info(f"新增礼物图片缓存, gift_id:{gift_id}, name:{name}")
                response = await get_session().get(url)
                image_data = await response.read()
                BlindBoxGenerator.cache_gift_png[gift_id] = image_data
                return Image.open(BytesIO(image_data))
            else:
                resource_base_path = os.path.dirname(inspect.getfile(starbot))
                return Image.open(f"{resource_base_path}/resource/face.png")

        generator = PicGenerator(width, height)
        pic = (generator.set_pos(margin, top_blank + margin)
               .draw_rounded_rectangle(0, top_blank, width, height - top_blank, 35, Color.WHITE)
               .copy_bottom(35))

        # 标题
        pic.draw_chapter("盲盒数据")

        # 防止后续绘图覆盖主播立绘
        logo_limit = (0, 0)

        # 主播信息
        uname = param.get('uname', '')
        room_id = param.get('room_id', 0)
        pic.draw_tip(f"{uname} ({room_id})")

        width = 1000
        height = 100000
        face_size = 100
        logo_limit = (650, 100)
        margin = 50
        pic = PicGenerator(width, height)
        # uids = []
        # counts = []
        is_space = param.get('is_space')
        up = param.get('up')
        face = param.get('face')
        title = param.get('title')
        my_uid = param.get('my_uid')
        gift_ids = param.get('gift_ids')
        counts = param.get('gift_counts')
        unames = param.get('gift_names')
        last_tick = param.get('last_tick')

        box_gift_ids = param.get('box_gift_ids')
        box_counts = param.get('box_gift_counts')
        box_unames = param.get('box_gift_names')

        isNeedUpdate = False
        allGift = set()
        allGift.update(gift_ids)
        allGift.update(box_gift_ids)
        for gift_id in allGift:
            if gift_id not in BlindBoxGenerator.cache_gift_name_and_url:
                isNeedUpdate = True

        if isNeedUpdate:
            data = await get_gift_config()
            for v in data.get("list"):
                gift_id = v['id']
                gift_name = v['name']
                img_basic = v['img_basic']
                if gift_id in allGift:
                    BlindBoxGenerator.cache_gift_name_and_url[gift_id] = (gift_name, img_basic)

        box_profit = param.get('total_profit')
        descs = param.get('gift_descs')

        pic.set_pos(175, 80).draw_rounded_rectangle(0, 0, width, height, 35, Color.WHITE).copy_bottom(35)

        pic.draw_img_alpha(mask_round(face.resize((face_size, face_size)).convert("RGBA")), (50, 50))


        # status = await redis.get_live_status(up.room_id)
        # status_str = "正在直播" if status == 1 else "未开播"
        # status_color = Color.RED if status == 1 else Color.GREEN
        # pic.draw_text(["直播间状态: ", status_str], [Color.BLACK, status_color])

        # note_str = "本次直播数据" if status == 1 else "上次直播数据"

        pic.draw_section(f"{uname} {title}").set_pos(50, 150 + pic.row_space)

        if my_uid:
            pic.draw_tip(f"UID: {up.uid}   房间号: {up.room_id}   {up.uname}的直播间")

        box_profit_color = Color.RED if box_profit > 0 else (Color.GREEN if box_profit < 0 else Color.GRAY)
        pic.draw_text(["盲盒盈亏: ", str(round(box_profit, 2)), " 元"], [Color.BLACK, box_profit_color, Color.BLACK])
        if last_tick:
            pic.draw_tip("此处为本直播间最近一场直播的数据")
        if not my_uid:
            my_title = "我的" + title.replace("数据", "")
            pic.draw_tip(f"使用\"{my_title}\"命令可查询我在本直播间的数据")
        elif "月" not in title:
            pic.draw_tip(f"使用\"X月盲盒\"命令可查询直播间的月数据")

        pic.draw_tip(f"查询时间: {timestamp_format(int(time.time()), '%Y/%m/%d %H:%M:%S')}")
        if is_space:
            if my_uid:
                pic.draw_text_multiline(50, f"未查询到 {uname} 在 {up.uname} 的{title}")
            else:
                pic.draw_text_multiline(50, f"未查询到 {title}")
            pic.draw_text("请先在直播间中互动后再来查询")
        else:
            download_face_tasks = [
                 get_gift_face(gift) for gift in gift_ids
            ]
            faces = list(await asyncio.gather(*download_face_tasks, return_exceptions=True))

            pic.draw_section(f"盲盒盈亏数据")
            ranking_img = cls.get_double_ranking(
                pic.row_space, faces, unames, counts, pic.width - (margin * 2), descs=descs, is_convert_mask=False
            )
            pic.draw_img_alpha(pic.auto_size_img_by_limit(ranking_img, logo_limit))

            pic.draw_section(f"盲盒数量")
            download_face_tasks = [
                 get_gift_face(gift) for gift in box_gift_ids
            ]
            box_faces = list(await asyncio.gather(*download_face_tasks, return_exceptions=True))
            ranking_img = cls.get_ranking(
                pic.row_space, box_faces, box_unames, box_counts, pic.width - (margin * 2), is_convert_mask=False
            )
            pic.draw_img_alpha(pic.auto_size_img_by_limit(ranking_img, logo_limit))

        # 底部版权信息，请务必保留此处
        pic.draw_text("")
        pic.draw_text_right(25, "Designed By StarBot", Color.GRAY)
        pic.draw_text_right(25, "https://github.com/Starlwr/StarBot", Color.LINK)
        from .. import VER
        pic.draw_text_right(25, f"starbot-blindbox-plugin {VER}", Color.RED)
        pic.crop_and_paste_bottom()
        return pic.base64()

    @classmethod
    def __get_rank_bar_pic(cls,
                           width: int,
                           height: int,
                           start_color: Union[Color, Tuple[int, int, int]] = Color.DEEPBLUE,
                           end_color: Union[Color, Tuple[int, int, int]] = Color.LIGHTBLUE,
                           reverse: bool = False) -> Image:
        """
        生成排行榜中排行条图片

        Args:
            width: 排行条长度
            height: 排行条宽度
            start_color: 排行条渐变起始颜色。默认：深蓝色 (57, 119, 230)
            end_color: 排行条渐变终止颜色。默认：浅蓝色 (55, 187, 248)
            reverse: 是否生成反向排行条，用于双向排行榜的负数排行条。默认：False
        """
        if isinstance(start_color, Color):
            start_color = start_color.value
        if isinstance(end_color, Color):
            end_color = end_color.value
        if reverse:
            start_color, end_color = end_color, start_color

        r_step = (end_color[0] - start_color[0]) / width
        g_step = (end_color[1] - start_color[1]) / width
        b_step = (end_color[2] - start_color[2]) / width

        now_color = [start_color[0], start_color[1], start_color[2]]

        bar = Image.new("RGBA", (width, 1))
        draw = ImageDraw.Draw(bar)

        for i in range(width):
            draw.point((i, 0), (int(now_color[0]), int(now_color[1]), int(now_color[2])))
            now_color[0] += r_step
            now_color[1] += g_step
            now_color[2] += b_step

        bar = bar.resize((width, height))

        mask = Image.new("L", (width, height), 255)
        mask_draw = ImageDraw.Draw(mask)
        if not reverse:
            mask_draw.polygon(((width - height, height), (width, 0), (width, height)), 0)
        else:
            mask_draw.polygon(((0, 0), (0, height), (height, height)), 0)
        bar.putalpha(mask)
        mask.close()

        return bar

    @classmethod
    def get_ranking(cls,
                    row_space: int,
                    faces: List[Image.Image],
                    unames: List[str],
                    counts: Union[List[int], List[float]],
                    width: int,
                    top_count: Optional[Union[int, float]] = None,
                    start_color: Union[Color, Tuple[int, int, int]] = Color.DEEPBLUE,
                    end_color: Union[Color, Tuple[int, int, int]] = Color.LIGHTBLUE,
                    descs: Union[None, List[str]] = None,
                    is_convert_mask=True) -> Image:
        """
        绘制排行榜

        Args:
            row_space: 行间距
            faces: 头像图片列表，按照数量列表降序排序
            unames: 昵称列表，按照数量列表降序排序
            counts: 数量列表，降序排序
            width: 排行榜图片宽度
            top_count: 第一名数量，后续排行条长度会基于此数量计算长度。默认：自动取数量列表中第一名
            start_color: 排行条渐变起始颜色。默认：深蓝色 (57, 119, 230)
            end_color: 排行条渐变终止颜色。默认：浅蓝色 (55, 187, 248)
        """
        count = len(counts)
        if count == 0 or len(faces) != len(unames) or len(unames) != len(counts):
            raise ValueError("绘制排行榜错误, 头像昵称列表与数量列表长度不匹配")

        face_size = 100
        offset = 10
        bar_height = 30

        bar_x = face_size - offset
        top_bar_width = width - face_size + offset
        if top_count is None:
            top_count = counts[0]

        chart = PicGenerator(width, (face_size * count) + (row_space * (count - 1)))
        chart.set_row_space(row_space)
        for i in range(count):
            bar_width = int(counts[i] / top_count * top_bar_width)

            if bar_width != 0:
                bar = cls.__get_rank_bar_pic(bar_width, bar_height, start_color, end_color)
                chart.draw_img_alpha(bar, (bar_x, chart.y + int((face_size - bar_height) / 2)))
            chart.draw_tip(unames[i], Color.BLACK, (bar_x + (offset * 2), chart.y))
            if descs:
                count_length2 = chart.get_tip_length("(" + descs[i] + ")")
                count_pos = (max(chart.x + bar_width-count_length2, bar_x + (offset * 3) + chart.get_tip_length(unames[i])), chart.y)
                chart.draw_tip(str(counts[i]) + "(" + descs[i] + ")", xy=count_pos)
            else:
                count_pos = (max(chart.x + bar_width, bar_x + (offset * 3) + chart.get_tip_length(unames[i])), chart.y)
                chart.draw_tip(str(counts[i]), xy=count_pos)
            if is_convert_mask:
                chart.draw_img_alpha(mask_round(faces[i].resize((face_size, face_size)).convert("RGBA")))
            else:
                chart.draw_img_alpha(faces[i].resize((face_size, face_size)).convert("RGBA"))

        return chart.img

    @classmethod
    def get_double_ranking(cls,
                           row_space: int,
                           faces: List[Image.Image],
                           unames: List[str],
                           counts: Union[List[int], List[float]],
                           width: int,
                           top_count: Optional[Union[int, float]] = None,
                           start_color: Union[Color, Tuple[int, int, int]] = Color.DEEPRED,
                           end_color: Union[Color, Tuple[int, int, int]] = Color.LIGHTRED,
                           reverse_start_color: Union[Color, Tuple[int, int, int]] = Color.DEEPGREEN,
                           reverse_end_color: Union[Color, Tuple[int, int, int]] = Color.LIGHTGREEN,
                           descs: Union[None, List[str]] = None,
                            is_convert_mask = True) -> Image:
        """
        绘制双向排行榜

        Args:
            row_space: 行间距
            faces: 头像图片列表，按照数量列表降序排序
            unames: 昵称列表，按照数量列表降序排序
            counts: 数量列表，降序排序
            width: 排行榜图片宽度
            top_count: 第一名数量，后续排行条长度会基于此数量计算长度。默认：自动取数量列表中第一名
            start_color: 正向排行条渐变起始颜色，数量为正时使用。默认：深红色 (57, 119, 230)
            end_color: 正向排行条渐变终止颜色，数量为正时使用。默认：浅红色 (55, 187, 248)
            reverse_start_color: 反向排行条渐变起始颜色，数量为负时使用。默认：深绿色 (57, 119, 230)
            reverse_end_color: 反向排行条渐变终止颜色，数量为负时使用。默认：浅绿色 (55, 187, 248)
        """
        count = len(counts)
        if count == 0 or len(faces) != len(unames) or len(unames) != len(counts):
            raise ValueError("绘制排行榜错误, 头像昵称列表与数量列表长度不匹配")

        face_size = 100
        offset = 10
        bar_height = 30

        face_x = int((width - face_size) / 2)
        bar_x = face_x + face_size - offset
        reverse_bar_x = face_x + offset
        top_bar_width = (width - face_size) / 2 + offset
        if top_count is None:
            top_count = max(max(counts), abs(min(counts)))

        chart = PicGenerator(width, (face_size * count) + (row_space * (count - 1)))
        chart.set_row_space(row_space)
        for i in range(count):
            bar_width = int(abs(counts[i]) / top_count * top_bar_width) if top_count != 0 else 0.1
            if bar_width != 0:
                if counts[i] > 0:
                    bar = cls.__get_rank_bar_pic(bar_width, bar_height, start_color, end_color)
                    chart.draw_img_alpha(bar, (bar_x, chart.y + int((face_size - bar_height) / 2)))
                elif counts[i] < 0:
                    bar = cls.__get_rank_bar_pic(bar_width, bar_height, reverse_start_color, reverse_end_color, True)
                    chart.draw_img_alpha(bar, (reverse_bar_x - bar_width, chart.y + int((face_size - bar_height) / 2)))
            if counts[i] >= 0:
                chart.draw_tip(unames[i], Color.BLACK, (bar_x + (offset * 2), chart.y))
                if descs:
                    count_length2 = chart.get_tip_length("(" + descs[i] + ")")
                    count_pos = (
                    max(face_x + bar_width-count_length2, bar_x + (offset * 3) + chart.get_tip_length(unames[i])), chart.y)
                    chart.draw_tip(str(counts[i]) + "(" + descs[i] + ")", xy=count_pos)
                else:
                    count_pos = (
                    max(face_x + bar_width, bar_x + (offset * 3) + chart.get_tip_length(unames[i])), chart.y)
                    chart.draw_tip(str(counts[i]), xy=count_pos)
            else:
                uname_length = chart.get_tip_length(unames[i])
                if descs:
                    count_length = chart.get_tip_length(str(counts[i])+ "(" + descs[i] + ")")
                else:
                    count_length = chart.get_tip_length(str(counts[i]))

                chart.draw_tip(unames[i], Color.BLACK, (reverse_bar_x - (offset * 2) - uname_length, chart.y))
                count_pos = (max(10, min(face_x + face_size - bar_width - count_length,
                                 reverse_bar_x - (offset * 3) - uname_length - count_length)), chart.y)
                if descs:
                    chart.draw_tip(str(counts[i]) + "(" + descs[i] + ")", xy=count_pos)
                else:
                    chart.draw_tip(str(counts[i]), xy=count_pos)
            if is_convert_mask:
                chart.set_pos(x=face_x).draw_img_alpha(mask_round(faces[i].resize((face_size, face_size)).convert("RGBA")))
            else:
                chart.set_pos(x=face_x).draw_img_alpha(faces[i].resize((face_size, face_size)).convert("RGBA"))
            chart.set_pos(x=0)

        return chart.img
