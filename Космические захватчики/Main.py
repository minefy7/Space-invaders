import random

import pygame

pygame.init()


class Ship():
    def __init__(self, image_ship, x, y, image_laser):
        self.speed = 10
        self.image_ship = image_ship
        self.x = x
        self.y = y
        self.health = 100
        self.rect = None
        self.lasers = []
        self.cd_counter = 0
        self.image_laser = image_laser

    def draw(self, screen):
        screen.blit(self.image_ship, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(screen)

    def move_lasers(self, speed, objs):
        self.cd()
        for laser in self.lasers:
            laser.move()
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if collide(laser, obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def cd(self):
        if self.cd_counter > 0:
            self.cd_counter += 1
        if self.cd_counter >= 30:
            self.cd_counter = 0

    def shoot(self):
        if self.cd_counter == 0:
            laser = Laser(15,self.image_laser, self.x + self.image_ship.get_width() // 2 - self.image_laser.get_width() // 2, self.y)
            self.lasers.append(laser)
            self.cd_counter = 1


class Laser():
    def __init__(self,speed, image, x, y):
        self.speed = speed
        self.image = image
        self.x = x
        self.y = y
        print(image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(image)
    def move(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y <= 0 or self.y >= 750


class Player_ship(Ship):
    def __init__(self, x, y):
        super().__init__(ship_y, x, y, pixel_laser_y)
        self.rect = self.image_ship.get_rect(topleft=(x, y))

        self.mask = pygame.mask.from_surface(ship_y)
    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

    def move_lasers(self, speed, objs):
        self.cd()
        for laser in self.lasers:
            laser.move( )
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if collide(laser, obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)


class Enemy_ship(Ship):
    def __init__(self, x,y):
        Ship.__init__(self, pixel_ship_r, x, y, pixel_laser_r)

        self.rect = self.image_ship.get_rect(topleft = (x,y))
        self.mask = pygame.mask.from_surface(pixel_ship_r)
    def move_y(self):
        self.y += 2
    def shoot(self):
        if self.cd_counter ==  0:
            laser = Laser(-15 , pixel_laser_r, self.x,self.y)
            self.lasers.append(laser)
            self.cd_counter = 1
font = pygame.font.SysFont(None, 50)

screen = pygame.display.set_mode((750, 750))
pygame.display.set_caption('Космические захватчки')

WHITE = (255, 255, 255)

background = pygame.image.load("./images/background-black.png").convert()
background = pygame.transform.scale(background, (750, 750))
pixel_laser_b = pygame.image.load("./images/pixel_laser_blue.png").convert_alpha()
pixel_laser_g = pygame.image.load("./images/pixel_laser_green.png").convert_alpha()
pixel_laser_r = pygame.image.load("./images/pixel_laser_red.png").convert_alpha()
pixel_laser_y = pygame.image.load("./images/pixel_laser_yellow.png").convert_alpha()
pixel_ship_b = pygame.image.load('./images/pixel_ship_blue_small.png').convert_alpha()
pixel_ship_g = pygame.image.load('./images/pixel_ship_green_small.png').convert_alpha()
pixel_ship_r = pygame.image.load('./images/pixel_ship_red_small.png').convert_alpha()
ship_y = pygame.image.load("./images/pixel_ship_yellow.png").convert_alpha()

clock = pygame.time.Clock()

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
def run():
    running = True
    health = 3
    lvl = 1
    enemies = []
    player = Player_ship(375, 600)

    def redraw_window():
        screen.blit(background, (0, 0))
        lives_label = font.render(f"Жизни: {health}", True, WHITE)
        level_label = font.render(f"Уровень: {lvl}", True, WHITE)

        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (750 - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(screen)

        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        pygame.display.update()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
        if len(enemies) == 0:
            for i in range(1,4):
                enemy = Enemy_ship(random.randint(0,650), random.randint(-100, 50))
                enemies.append(enemy)

        if collide(enemy, player):
            player.health -= 10
            enemies.remove(enemy)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player.speed > 0:
            player.x -= player.speed
        if keys[pygame.K_d] and player.x + player.speed < 750 - player.image_ship.get_width():
            player.x += player.speed
        if keys[pygame.K_w] and player.y - player.speed > 0:
            player.y -= player.speed
        if keys[pygame.K_s] and player.y + player.speed < 750 - player.image_ship.get_height():
            player.y += player.speed
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:
            enemy.move_y()
            if random.randrange(0, 120) == 1:
                enemy.shoot()
            enemy.move_lasers(15, player.lasers)
            if enemy.health <= 0:
                enemies.remove(enemy)

        player.update_rect()
        player.move_lasers(15, enemy.lasers)
        redraw_window()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            run()

    screen.blit(background, (0, 0))
    title_label = font.render('Нажмите на экран что бы начать игру.', False, WHITE)
    screen.blit(title_label, (50, 325))
    pygame.display.update()

pygame.quit()

