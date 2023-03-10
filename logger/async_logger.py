# Я сначала написал логгер асинхронно, потому что думал, что это будет необходимо, поскольку
# окно времени на лог во все места — одна секунда за вычетом времени на все остальные действия.
# Потом подумал "А правда ли это будет необходимо?" и переписал его синхронно, каким в итоге оставил.
# Файл в проекте оставил исключительно из пижонства :р

from datetime import datetime as dt

import asyncio
import aiofiles
import aiosqlite


class AsyncLogger:
    def __init__(self):
        self.dbLogFileName = 'kettle_logs.sqlite3'
        self.txtLogFileName = 'kettle_logs.txt'

    async def async_log_to_txt(self, message: str, datetime_mark: dt | None = None):
        async with aiofiles.open(self.txtLogFileName, 'a') as file:
            hour_minute_line_prefix = f"[{datetime_mark.strftime('%H:%M')}] " if datetime_mark else ''
            await file.write(f"{hour_minute_line_prefix}{message}\n")

    async def async_log_to_db(self, message, datetime_mark: dt):
        async with aiosqlite.connect(self.dbLogFileName) as db:
            await db.execute('INSERT INTO logs (message, date_mark, time_mark) VALUES (?, ?, ?)',
                             (message, datetime_mark.strftime('%Y-%m-%d'), datetime_mark.strftime('%H:%M:%S'))
                             )
            await db.commit()

    async def async_full_log(self, message: str):
        dt_mark = dt.today()
        tasks = (self.async_log_to_db(message, dt_mark), self.async_log_to_txt(message, dt_mark))
        await asyncio.gather(*tasks)

# Синхронные заглушки для методов
    def log_to_txt(self, message: str, datetime_mark: dt | None = None):
        asyncio.run(self.async_log_to_txt(message, datetime_mark))

    def log_to_db(self, message: str, datetime_mark: dt):
        asyncio.run(self.async_log_to_db(message, datetime_mark))

    def full_log(self, message: str):
        asyncio.run(self.async_full_log(message))
