class GoldenBanana:
    def __init__(self, name: str):
        self.name = name
        self.collected = False
        self.slam = 0
        self.cranky()
        self.frees()
        self.guns()
        self.instruments()

    def cranky(self, dk=0, diddy=0, chunky=0, lanky=0, tiny=0):
        self.dk_cranky = dk
        self.diddy_cranky = diddy
        self.chunky_cranky = chunky
        self.lanky_cranky = lanky
        self.tiny_cranky = tiny

    def frees(self, dk=False, diddy=False, chunky=False, lanky=False, tiny=False):
        self.frees_dk = dk
        self.frees_diddy = diddy
        self.frees_chunky = chunky
        self.frees_lanky = lanky
        self.frees_tiny = tiny

    def guns(self, dk=False, diddy=False, chunky=False, lanky=False, tiny=False):
        self.dk_gun = dk
        self.diddy_gun = diddy
        self.chunky_gun = chunky
        self.lanky_gun = lanky
        self.tiny_gun = tiny

    def instruments(self, dk=False, diddy=False, chunky=False, lanky=False, tiny=False):
        self.dk_instrument = dk
        self.diddy_instrument = diddy
        self.chunky_instrument = chunky
        self.lanky_instrument = lanky
        self.tiny_instrument = tiny

    def pickup(self, dk=False, diddy=False, chunky=False, lanky=False, tiny=False):
        self.dk_pickup = dk
        self.diddy_pickup = diddy
        self.chunky_pickup = chunky
        self.lanky_pickup = lanky
        self.tiny_pickup = tiny

    def shared_moves(self, barrel=False, dive=False, homing=False, orange=False, sniper=False, vine=False):
        self.barrel = barrel
        self.dive = dive
        self.homing = homing
        self.orange = orange
        self.sniper = sniper
        self.vine = vine
