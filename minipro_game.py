import pyxel
import random

SCREEN_W = 160
SCREEN_H = 120

CANDY_W = 16
CANDY_H = 8

BASKET_W = 24
BASKET_H = 8

LANE_X = [20, 50, 80, 110]

NORMAL_CANDIES = [
    {"u": 0,  "score": 10, "speed": 1}, 
    {"u": 16, "score": 20, "speed": 2},  
    {"u": 32, "score": 30, "speed": 3},  
    {"u": 48, "score": 40, "speed": 4},  
]

RARE_CANDY = {"u": 64, "score": 100, "speed": 1}

class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Candy Catch")
        pyxel.load("my_resource.pyxres")

        self.basket_x = SCREEN_W // 2
        self.basket_y = SCREEN_H - 12

        self.score = 0
        self.life = 3
        self.game_over = False

        self.spawn_candy()

        pyxel.run(self.update, self.draw)

    def spawn_candy(self):
        if random.random() < 0.1:
            self.candy = RARE_CANDY
        else:
            self.candy = random.choice(NORMAL_CANDIES)

        self.candy_x = random.choice(LANE_X)
        self.candy_y = -CANDY_H

    def restart(self):
        self.score = 0
        self.life = 3
        self.game_over = False
        self.spawn_candy()

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.restart()
            return

        if pyxel.btn(pyxel.KEY_LEFT):
            self.basket_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.basket_x += 2

        self.basket_x = max(0, min(self.basket_x, SCREEN_W - BASKET_W))

        self.candy_y += self.candy["speed"]

        if self.check_hit():
            self.score += self.candy["score"]
            self.spawn_candy()
            return

        if self.candy_y > SCREEN_H:
            self.life -= 1
            if self.life <= 0:
                self.game_over = True
            else:
                self.spawn_candy()

    def check_hit(self):
        return (
            self.candy_x < self.basket_x + BASKET_W and
            self.candy_x + CANDY_W > self.basket_x and
            self.candy_y < self.basket_y + BASKET_H and
            self.candy_y + CANDY_H > self.basket_y
        )

    def draw(self):
        pyxel.bltm(0, 0, 0, 0, 0, 160, 128)

        if not self.game_over:
            pyxel.blt(
                self.candy_x,
                self.candy_y,
                0,
                self.candy["u"], 0,
                CANDY_W, CANDY_H,
                0
            )

            pyxel.blt(
                self.basket_x,
                self.basket_y,
                0,
                0, 8,
                BASKET_W, BASKET_H,
                0
            )

        pyxel.text(5, 5, f"SCORE: {self.score}", 7)

        for i in range(self.life):
            pyxel.blt(
                80 + i * 10,
                5,
                0,
                96, 0,
                8, 8,
                0
            )

        if self.game_over:
            pyxel.text(55, 55, "GAME OVER", 8)
            pyxel.text(42, 65, "PRESS R TO RESTART", 7)


App()

