# -*- coding: utf-8 -*-

from it_assistant.do_ai import do_ai_auto

# 假设 Testsuitelink 是一个有效的文档链接
Testsuitelink = "your_testsuitelink_here"

try:
    startAt, row_count = do_ai_auto(Testsuitelink)
    if startAt is not None and row_count is not None:
        print(f"成功执行，startAt: {startAt}, row_count: {row_count}")
    else:
        print("执行过程中出现错误")
except Exception as e:
    print(f"调用 do_ai_auto 函数时出现异常: {e}")
