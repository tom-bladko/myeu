'''

GAME LOGIC

Class to manage all background processing related to game play



'''

from src.db import TDB
db = TDB()


def create_managers():
    print("Create all ggame managers")

    from manage.province_manager import ProvinceManager
    db.province_manager = ProvinceManager()

    from manage.country_manager import CountryManager
    db.country_manager = CountryManager()

    from manage.cot_manager import CenterTradeManager
    db.center_trade_manager = CenterTradeManager( {} )

def process_game_logic_before():
    print("Game logic before processing")

    db.province_manager.process_before_all()
    db.country_manager.process_before_all()
    db.center_trade_manager.process_before_all()