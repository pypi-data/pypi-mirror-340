import argparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import os
import pyautogui
import sys
import time
from typing import Literal, Optional

import pydash
from ..utils import index as utils

# TDD execRun
# def add(a, b):
#     return a + b

# res = utils.execRun(
#     [
#         "x = 1",
#         "y = 2",
#         "add(x, y)",
#     ],
#     space={**globals(), **locals()},
# )
# print(res)  # 3

# TDD enum
# from enum import Enum
# class Ab(Enum):
#     a = '1'
#     b = '2'
# ab: Ab = Ab.a
# print(ab.name == 'a') # True
# print(ab.value == '1') # True

# TDD 列表推导式 & 生成器表达式
# arr = [1, 2]
# print([v + 1 for v in arr])  # [2, 3]
# print((v + 1 for v in arr if v % 2 == 0))  # <generator object <genexpr> at 0x12fe589e0>

# TDD 并发测试
# executor = ThreadPoolExecutor(max_workers=2)

# def _sleep(a: int):
#     time.sleep(1)
#     return a

# async def findOnScreen2(a: int):

#     # 获取当前正在运行的事件循环
#     loop = asyncio.get_running_loop()

#     # 使用partial 相当于js中的 bind 预制参数
#     bindLocateOnScreen = partial(
#         _sleep,
#         a
#     )
#     # 使用共享的 executor 并发执行 定位操作
#     locationFuture = loop.run_in_executor(executor, bindLocateOnScreen)
#     try:
#         # 等待全部操作完成
#         # (location,) = await asyncio.gather(locationFuture)
#         location = await locationFuture
#     except Exception as err:
#         location = None
#     if location is None:
#         return None
#     return location


def add(a, b):
    print(a, b)
    return a + b


async def main():
    # TDD findOnScreen
    # 测试 confidence 取值 预期是 选中能识别 未选中 不能识别
    confidence = 0.99
    [res1, res2, res3] = await asyncio.gather(
        *[
            # n 选中
            utils.findOnScreen(
                os.path.join(
                    utils.imagesDirPath, "dmr/ck/job2/7-1-n-selected-include.png"
                ),
                confidence=confidence,
            ),
            # n 未选中
            utils.findOnScreen(
                os.path.join(
                    utils.imagesDirPath, "dmr/ck/job2/3-1-n-unselected-click.png"
                ),
                confidence=confidence,
            ),
            utils.findOnScreen(
                os.path.join(
                    utils.imagesDirPath, "dmr/ck/job2/6-1-breakdown-prompt-click.png"
                ),
                confidence=0.8,
            ),
        ]
    )
    print(res1, res2, res3)
    pyautogui.press("e")
    pyautogui.press("space")
    # print(1 < float('inf'))
    # obj = {'a': 1, 'b': 2, 'c': 3}
    # args = {k: v for k, v in obj.items() if k != 'a'}
    # print(args) # {'b': 2, 'c': 3}
    # for v in range(1, 10):
    #     print(v, type(v))
    #     await asyncio.sleep(1)
    #     pass

    startTime = int(time.time() * 1000)

    # (asd1, asd2, asd3, asd4) = await asyncio.gather(*[findOnScreen2(1), findOnScreen2(1), findOnScreen2(1), findOnScreen2(1)])
    # (asd1, asd2, asd3) = await asyncio.gather(*[findOnScreen2(1), findOnScreen2(1), findOnScreen2(1)])
    # print('asd', asd1, asd2, asd3)
    # obj1 = {'a': None, 'b': None}
    # obj2 = {'a': 1, 'b': 2}
    # res = add(**{**obj1, **obj2})
    # print(res)

    # # 在当前鼠标位置基础上，y轴向上移动100像素（即y-100）
    # pyautogui.move(xOffset=0, yOffset=-100, duration=0.3) # 是对的
    # pyautogui.click(x=500,y=325)
    # time.sleep(1)
    # # 向上滚动 200 单位
    # pyautogui.scroll(200)
    # time.sleep(1)
    # # 或者向下滚动 200 单位
    # pyautogui.scroll(-200)
    # time.sleep(1)
    utils.printDebug(f"整体任务耗时：{int(time.time() * 1000) - startTime} ms")

    return


# 运行异步函数 它自己本身是同步的
asyncio.run(main())

# uv run -m src.test.index
