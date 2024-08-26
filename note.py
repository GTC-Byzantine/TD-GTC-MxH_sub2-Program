import pygame
import GTC_Pygame_Runtime_Support as PRS
import random


def main(screen):
    clock = pygame.time.Clock()
    button_return = PRS.FeedbackButton([80, 40], [20, 20], '返回', 25, screen, bg_color=(200, 200, 200),
                                       border_color=(200, 200, 200), font_type='ddjbt.ttf')
    # background = pygame.transform.scale(pygame.image.load(f'Data/Image/n{random.randint(1, 2)}.jfif'), (1240, 720))
    load_progress = PRS.ProgressBar(1140, 5, screen, [50, 70], color=((200, 200, 200), (32, 161, 98)))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((255, 255, 255))
        button_return.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
        load_progress.next()
        # screen.blit(background, (0, 0))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    sc = pygame.display.set_mode((1240, 720))
    main(sc)
