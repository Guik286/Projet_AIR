import pygame as pg

BUTTONS = [
    "up",
    "down",
    "left",
    "right",
    "start",
    "select",
    "A",
    "B",
    "Y",
    "X",
    "L",
    "R",
]

class KeysManager : 
    def __init__(self, key_map = None):
        self._last_keys = dict()
        self._new_keys = {but: False for but in BUTTONS}

        if key_map is None:
            self._key_map = {
                "up": [pg.K_w, pg.K_UP],
                "down": [pg.K_s, pg.K_DOWN],
                "left": [pg.K_a, pg.K_LEFT],
                "right": [pg.K_d, pg.K_RIGHT],
                "A": [pg.K_k],
                "B": [pg.K_h],
                "X": [pg.K_l],
                "Y": [pg.K_j],
                "L": [pg.K_o],
                "R": [pg.K_p],
                "start": [pg.K_i],
                "select": [pg.K_t],
            }
        else:
            self._key_map = key_map

            self.arreturgence = False

    def Gestion_evenement(self):
        """Traite un événement de touche entrant."""

        self._last_keys = self._new_keys.copy()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.arreturgence = True
                print("shutdown")
                pg.quit()
                return

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.arreturgence = True
                    

                for but, keys in self._key_map.items():
                    if event.key in keys:
                        self._set_key(but)

            if event.type == pg.KEYUP:
                for but, keys in self._key_map.items():
                    if event.key in keys:
                        self._unset_key(but)

    def _set_key(self, button):
        self._new_keys[button] = True

    def _unset_key(self, button):
        self._new_keys[button] = False

    def is_new_key_press(self, but):
        return self._new_keys[but] and not self._last_keys[but]

    def is_key_down(self, but):
        return self._new_keys[but]

    def is_new_key_release(self, but):
        return self._last_keys[but] and not self._new_keys[but]