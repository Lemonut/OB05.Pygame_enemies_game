import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Game")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Настройки игрока
PLAYER_SIZE = 50
PLAYER_VEL = 5

# Настройки врагов
ENEMY_SIZE = 30
ENEMY_VEL = 3
ENEMY_SPAWN_RATE = 25

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        # Ограничение движения в пределах окна
        self.rect.x = max(0, min(self.rect.x, WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - PLAYER_SIZE))

    def draw(self, win):
        pygame.draw.rect(win, BLUE, self.rect)

class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - ENEMY_SIZE), -ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE)

    def move(self):
        self.rect.y += ENEMY_VEL

    def draw(self, win):
        pygame.draw.rect(win, RED, self.rect)

    def off_screen(self):
        return self.rect.y > HEIGHT

def main():
    clock = pygame.time.Clock()
    player = Player(WIDTH // 2, HEIGHT - PLAYER_SIZE)
    enemies = []
    run = True
    score = 0

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-PLAYER_VEL, 0)
        if keys[pygame.K_RIGHT]:
            player.move(PLAYER_VEL, 0)
        if keys[pygame.K_UP]:
            player.move(0, -PLAYER_VEL)
        if keys[pygame.K_DOWN]:
            player.move(0, PLAYER_VEL)

        # Создание врагов
        if random.randint(1, ENEMY_SPAWN_RATE) == 1:
            enemies.append(Enemy())

        # Движение и удаление врагов
        for enemy in enemies:
            enemy.move()
            if enemy.off_screen():
                enemies.remove(enemy)
                score += 1

        # Проверка столкновений
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                score -= 10  # Вычитаем 10 баллов при столкновении
                enemies.remove(enemy)  # Удаляем врага после столкновения

                # Проверка на отрицательный счет
                if score < 0:
                    run = False  # Завершаем игру, если счет отрицательный

        # Отрисовка
        WIN.fill(WHITE)
        player.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)

        # Отображение счета
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(f"Score: {score}", 1, (0, 0, 0))
        WIN.blit(text, (10, 10))

        pygame.display.update()

    # Сообщение о завершении игры
    font = pygame.font.SysFont("comicsans", 50)
    text = font.render("Game Over!", 1, (255, 0, 0))
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)  # Задержка перед закрытием окна

    pygame.quit()

if __name__ == "__main__":
    main()