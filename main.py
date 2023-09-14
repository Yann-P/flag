import os
from flag.cat_agent import CatAgent
from flag.game import Game
from flag.sysadmin_agent import SysAdminAgent
from flag.web import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
    # game = Game()
    # game.pushToNextAgent(SysAdminAgent())
    # game.applyNextAgent()
    # game.run()
