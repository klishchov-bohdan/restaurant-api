import asyncio
from decimal import Decimal

import gspread

from app.background.worker import worker
from app.config import settings
from app.dependencies import get_uow
from app.redis_conn import redis_sync
from app.utils.uow import UnitOfWork

CREDENTIALS_FILE_LOCAL_PATH = '../credentials.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


class DBSaver:
    @staticmethod
    async def _add_many_to_repo(menus: list, submenus: list, dishes: list, uow: UnitOfWork) -> dict:
        async with uow:
            menus = await uow.menu_repo.add_many(menus)
            submenus = await uow.submenu_repo.add_many(submenus)
            dishes = await uow.dish_repo.add_many(dishes)
            await uow.commit()
        return {
            'menus': menus,
            'submenus': submenus,
            'dishes': dishes
        }

    @staticmethod
    def _save_fee_to_redis(dishes: list) -> None:
        for dish in dishes:
            redis_sync.set(f'dish_{dish["id"]}_fee', float(dish['fee']))


class GSheetTasks(DBSaver):
    @staticmethod
    @worker.task(name='sync_database')
    def sync_database():
        gc = gspread.service_account('./credentials.json')

        spreadsheet = gc.open_by_url(
            'https://docs.google.com/spreadsheets/d/1g73VTQrxzM5YCn2kw4Cc4BrjJ_vQ_qCgErDgSMJAg_8')

        worksheet = spreadsheet.get_worksheet(0)
        rows = worksheet.get_all_values()
        menus, submenus, dishes = [], [], []
        current_menu_id = None
        current_submenu_id = None
        for row in rows:
            if row[0].isdigit():
                current_menu_id = row[0]
                menus.append({
                    'id': int(row[0]),
                    'title': row[1],
                    'description': row[2]
                })

            elif row[1].isdigit():
                current_submenu_id = row[1]
                submenus.append({
                    'id': int(row[1]),
                    'title': row[2],
                    'description': row[3],
                    'menu_id': int(current_menu_id)
                })
            elif row[2].isdigit():
                dishes.append({
                    'id': int(row[2]),
                    'title': row[3],
                    'description': row[4],
                    'price': Decimal(row[5]),
                    'fee': Decimal(row[6]),
                    'submenu_id': int(current_submenu_id)
                })
        uow = get_uow()
        asyncio.run(GSheetTasks._add_many_to_repo(menus, submenus, dishes, uow))
        keys = redis_sync.scan_iter(f'{settings.api_prefix}*')
        for key in keys:
            redis_sync.delete(key)
        GSheetTasks._save_fee_to_redis(dishes)


worker.conf.beat_schedule = {
    'run-me-every-fifteen-seconds': {
        'task': 'sync_database',
        'schedule': 15.0
    }
}
