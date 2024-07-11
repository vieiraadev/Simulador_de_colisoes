import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60

BALL_RADIUS = 15
BALL_COUNT = 20
BALL_SPEED = 5

class Ball:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.x - BALL_RADIUS < 0 or self.x + BALL_RADIUS > WIDTH:
            self.vx = -self.vx

        if self.y - BALL_RADIUS < 0 or self.y + BALL_RADIUS > HEIGHT:
            self.vy = -self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

    def collide(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < 2 * BALL_RADIUS:
            angle = math.atan2(dy, dx)
            sin_a = math.sin(angle)
            cos_a = math.cos(angle)

            vx1_rot = self.vx * cos_a + self.vy * sin_a
            vy1_rot = -self.vx * sin_a + self.vy * cos_a
            vx2_rot = other.vx * cos_a + other.vy * sin_a
            vy2_rot = -other.vx * sin_a + other.vy * cos_a

            vx1_rot, vx2_rot = vx2_rot, vx1_rot

            self.vx = vx1_rot * cos_a - vy1_rot * sin_a
            self.vy = vx1_rot * sin_a + vy1_rot * cos_a
            other.vx = vx2_rot * cos_a - vy2_rot * sin_a
            other.vy = vx2_rot * sin_a + vy2_rot * cos_a

            overlap = 2 * BALL_RADIUS - distance
            self.x += math.cos(angle) * overlap / 2
            self.y += math.sin(angle) * overlap / 2
            other.x -= math.cos(angle) * overlap / 2
            other.y -= math.sin(angle) * overlap / 2

def random_velocity():
    angle = random.uniform(0, 2 * math.pi)
    speed = random.uniform(1, BALL_SPEED)
    return speed * math.cos(angle), speed * math.sin(angle)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Colisões Elásticas em 2D")
    clock = pygame.time.Clock()

    def create_balls():
        balls = []
        colors = [(255, 0, 0), (0, 0, 255)]  # Red and Blue
        for _ in range(BALL_COUNT):
            x = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
            y = random.randint(BALL_RADIUS, HEIGHT - BALL_RADIUS)
            vx, vy = random_velocity()
            color = random.choice(colors)
            balls.append(Ball(x, y, vx, vy, color))
        return balls

    balls = create_balls()
    collision_count = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    balls = create_balls()
                    collision_count = 0

        screen.fill(BACKGROUND_COLOR)

        for i, ball in enumerate(balls):
            ball.move()
            ball.draw(screen)
            for other in balls[i+1:]:
                initial_vx, initial_vy = ball.vx, ball.vy
                ball.collide(other)
                if (ball.vx, ball.vy) != (initial_vx, initial_vy):
                    collision_count += 1

        text = font.render(f"Colisões: {collision_count}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
