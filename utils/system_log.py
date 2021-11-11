from datetime import datetime

async def log_pr(message: str):
    now = datetime.now()
    time = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"
    print(f"[{time}] " + message)

    return