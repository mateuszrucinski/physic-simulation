import pygame
import subprocess

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symulacje Fizyczne")

background_image = pygame.image.load("gwiazdy-na-nocnym-niebie.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

font = pygame.font.Font(None, 50)

button_width, button_height = 400, 100
crate_button = pygame.Rect(WIDTH // 2 - button_width // 2, 150, button_width, button_height)
pendulum_button = pygame.Rect(WIDTH // 2 - button_width // 2, 300, button_width, button_height)
cannon_button = pygame.Rect(WIDTH // 2 - button_width // 2, 450, button_width, button_height)

def draw_button_with_border(button, text, button_color, border_color, border_width=5):
    #border
    pygame.draw.rect(screen, border_color, button.inflate(border_width * 2, border_width * 2), border_radius=15)

    pygame.draw.rect(screen, button_color, button, border_radius=15)

    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=button.center)
    screen.blit(text_surface, text_rect)

running = True

while running:
    screen.blit(background_image, (0, 0))

    draw_button_with_border(crate_button, "Przeciąganie Skrzyni", (124,252,0), (0,100,0))
    draw_button_with_border(pendulum_button, "Wahadło Matematyczne", (205,92,92), (128,0,0))
    draw_button_with_border(cannon_button, "Symulacja Armaty", (138,43,226), (75,0,130))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pendulum_button.collidepoint(event.pos):
                subprocess.Popen(["python", "pendulum.py"])
            elif cannon_button.collidepoint(event.pos):
                subprocess.Popen(["python", "cannon.py"])
            elif crate_button.collidepoint(event.pos):
                subprocess.Popen(["python", "main.py"])

    pygame.display.flip()

pygame.quit()
