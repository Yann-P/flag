from flag.cat_agent import CatAgent
from flag.game import Game
from flag.sysadmin_agent import SysAdminAgent

if __name__ == "__main__":
    game = Game()
    game.pushToNextAgent(SysAdminAgent())
    game.applyNextAgent()
    game.run()
