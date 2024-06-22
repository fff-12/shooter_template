from pygame import *
from random import randint
from time import time as timer #імпортуємо функцію для засікання часу, щоб інтерпретатор не шукав цю функцію в pygame модулі time, даємо їй іншу назву самі

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render('YOU WIN!', True, (0, 255, 0))
lose = font2.render('YOU LOSE!', True, (255, 0, 0))


img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_superEnemy = "big.png"
img_non_killable_enemy = "asteroid.png"
img_health = "healthPoint.png"

score = 0
lost = 0
goal = 50
max_lost = 50
life = 5
inf = False

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(size_x, sixe_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y, sprite_speed):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, sixe_y, sprite_speed)
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_width - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top + 60, 20, 15, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x < 0:
            self.rect.y = randint(80, win_height - 80)
            self.rect.x = 740
            lost +=1

class Asteroid(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.y = randint(80, win_height - 80)
            self.rect.x = 740

class SuperEnemy(Enemy):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed, max_hits):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        self.max_hits = max_hits
    def gotHit(self):
        self.max_hits -= 1
    def isKilled(self):
        if(self.max_hits <= 0):
            self.kill()
            return True
        else: return False
    def super_update(self):
        self.rect.x -= self.speed
        global lost, finish
        if self.rect.x < 0:
            finish = True
            window.blit(lose, (200, 200))


class HealthPack(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.y = randint(80, win_height - 80)
            self.rect.x = 740 
    def apply(self):
        global life
        life += 1
        self.kill()
    def kill_all2(self):
        global monsters, asteroids, superMonsters

        monsters.empty()
        asteroids.empty()
        superMonsters.empty()
        self.kill()
    
    def inf2(self):
        global inf

        inf = True
        self.kill()

class Bullet(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        self.image = transform.rotate(self.image, -90)
    def update(self):
        self.rect.x -= self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.x > 700:
            self.kill()

def first_spawn():
    for i in range(1, 8):
        monster = Enemy(img_enemy, 740, randint(80, win_height - 80), 150, 110, randint(1, 3))
        monsters.add(monster)
    for i in range(1, 5):
        asteroid = Asteroid(img_non_killable_enemy, 740, randint(80, win_height - 80), 150, 110,randint(1, 7))
        asteroids.add(asteroid)
    for i in range(1, 6):
        superMonster = SuperEnemy(img_superEnemy, 740, randint(80, win_height - 80), 150, 110, randint(1, 3), 3)
        superMonsters.add(superMonster)



win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

player = Player(img_hero, 5, win_height - 100, 120, 120, 10)
# health_pack = HealthPack(img_health, randint(30, win_width - 30), -40, 30, 30, 7)


health_packs = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
superMonsters = sprite.Group()
kill_all = sprite.Group()
infs = sprite.Group()
# health_packs.add(health_pack)

first_spawn()

run = True
finish = False
clock = time.Clock()
FPS = 30
rel_time = False  # прапор, що відповідає за перезаряджання
num_fire = 0  # змінна для підрахунку пострілів    
spawn_time = 0
spawn_time1 = 0
timer_s = 0
inf_time = 0
boss = sprite.Group()
bhp = 40

boss1 = SuperEnemy('pudge.png', 740, randint(80, win_height - 80), 300, 240, 2, 40)
boss.add(boss1)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and not finish: ###
            if e.key == K_SPACE:
                if num_fire < 30 and rel_time == False:
                    num_fire += 1
                    player.fire()

                if num_fire >= 30 and rel_time == False : #якщо гравець зробив 20 пострілів
                    last_time = timer() #засікаємо час, коли це сталося
                    rel_time = True #ставимо прапор перезарядки

    spawn_time += clock.get_time() / 1000
    spawn_time1 += clock.get_time() / 1000
    timer_s += clock.get_time() / 1000

    if inf == True:
        inf_time += clock.get_time() / 1000
        if int(inf_time) >= 2:
            inf = False

    if not finish:
        window.blit(background, (0, 0))
        if int(timer_s) >= 30:
            for i in boss:
                i.super_update()
            boss.draw(window)
        
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        health_packs.update()
        superMonsters.update()
        kill_all.update()
        infs.update()

        health_packs.draw(window)
        kill_all.draw(window)
        infs.draw(window)
        player.reset()
        monsters.draw(window)
        superMonsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if life == 1 and len(health_packs) == 0:
            health_pack = HealthPack(img_health, 740, randint(80, win_height - 80), 30, 30, 7)
            health_packs.add(health_pack)

        if len(kill_all) == 0 and spawn_time >= 17:
            kill_all1 = HealthPack('pngegg.png', 740, randint(80, win_height - 80), 30, 30, 7)
            kill_all.add(kill_all1)
            spawn_time = 0
        
        if len(infs) == 0 and spawn_time1 >= 15:
            inf1 = HealthPack('miki.png', 740, randint(80, win_height - 80), 30, 30, 7)
            infs.add(inf1)
            spawn_time1 = 0

        if rel_time == True:
            now_time = timer() # зчитуємо час
            if now_time - last_time < 2: #поки не минуло 2 секунди виводимо інформацію про перезарядку
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (win_width/2-200, win_height-100))
            else:
                num_fire = 0     #обнулюємо лічильник куль
                rel_time = False #скидаємо прапор перезарядки

        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy(img_enemy, 740, randint(80, win_height - 80), 150, 110, randint(1, 3))
            monsters.add(monster)

        for superMonster in superMonsters:
            if sprite.spritecollide(superMonster, bullets, True):
                superMonster.gotHit()
                if superMonster.isKilled():
                    score = score + 1
                    superMonster = SuperEnemy(img_superEnemy, 740, randint(80, win_height - 80), 150, 110, randint(1, 3), 3)
                    superMonsters.add(superMonster)

        for i in boss:
            if sprite.spritecollide(i, bullets, True):
                i.gotHit()
                bhp -= 1
                if i.isKilled():
                    score = score + 15

        # якщо спрайт торкнувся ворога зменшує життя
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False) or sprite.spritecollide(player, superMonsters, False):
            if not inf:
                life = life - 1
            if sprite.spritecollide(player, monsters, True):
                monster = Enemy(img_enemy, 740, randint(80, win_height - 80), 150, 110, randint(1, 3))
                monsters.add(monster)
            if sprite.spritecollide(player, asteroids, True):
                asteroid = Asteroid(img_non_killable_enemy, 740, randint(80, win_height - 80), 150, 110, randint(1, 7))
                asteroids.add(asteroid)
            if sprite.spritecollide(player, superMonsters, True):
                superMonster = SuperEnemy(img_superEnemy, 740, randint(80, win_height - 80), 150, 110, randint(1, 3), 3)
                superMonsters.add(superMonster)

        if sprite.spritecollide(player, health_packs, True):
            health_pack.apply()

        if sprite.spritecollide(player, kill_all, True):
            kill_all1.kill_all2()
            first_spawn()

        if sprite.spritecollide(player, infs, True):
            inf1.inf2()
            inf_time = 0

        # програш
        if life == 0 or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))

        # перевірка виграшу: скільки очок набрали?
        if score >= goal and timer_s >= 60:
            finish = True
            window.blit(win, (200, 200))
        
        if score < goal and timer_s >= 60:
            finish = True
            window.blit(lose, (200, 200))



        text = font1.render(f"Рахунок: " + str(score),1, (255,255,255))
        window.blit(text,(10, 20))

        text_lose = font1.render("Пропущенно: " + str(lost),1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_life = font1.render(str(life), 1, (0, 150, 0))
        window.blit(text_life, (650, 10))

        text_timer = font1.render(f"{60 - int(timer_s)}sec", 1, (255, 255, 255))
        window.blit(text_timer, (350, 10))

        for i in boss:
            if int(timer_s) >= 30 and not i.isKilled():
                boss_hp = font1.render(f"{bhp}boss hp", 1, (255, 255, 255))
                window.blit(boss_hp, (350, 40))
        

        display.update()

    clock.tick(FPS)
