from datetime import datetime

import asyncio
import sys
import os

async def restart_system():
    while True:
        now = datetime.now()
        time = f"{now.hour}:{now.minute}:{now.second}"

        if time == "2:30:0":
            os.system("start python -B -m cloudsb")
            os.system("cls")
            print("[과부하 방지] 시스템을 새로 다시 시작하였습니다.\n\n[과부하 방지] 창을 닫아주세요.")

            return sys.exit(0)

        await asyncio.sleep(1)

        