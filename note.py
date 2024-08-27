import time
import pygame
import GTC_Pygame_Runtime_Support as PRS
import random


def main(screen):
    clock = pygame.time.Clock()
    button_return = PRS.FeedbackButton([80, 40], [20, 20], '返回', 25, screen, bg_color=(220, 220, 220),
                                       border_color=(220, 220, 220), font_type='ddjbt.ttf')
    # background = pygame.transform.scale(pygame.image.load(f'Data/Image/n{random.randint(1, 2)}.jfif'), (1240, 720))
    file_surface = pygame.Surface((1140, 620))
    progress = 0
    last_tick = False
    load_progress = PRS.ProgressBar(1140, 5, file_surface, [0, 0], color=((220, 220, 220), (32, 161, 98)), sep=10)
    text = ""
    font = pygame.font.Font('ddjbt.ttf', 20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((255, 255, 255))
        file_surface.fill((220, 220, 220))

        button_return.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
        if last_tick and not button_return.state:
            return
        last_tick = button_return.state
        load_progress.next()
        progress += 10
        if progress in [290, 970]:
            time.sleep(random.randint(2, 15) / 10)
        if progress <= 290:
            text = '正在制作文件索引'
        elif progress <= 970:
            text = '正在连接服务器'
        else:
            text = '正在加载组件'
        if progress > 1300:
            break
        ff = font.render(text, 1, [0, 0, 0])
        screen.blit(ff, ff.get_rect(center=(620, 40)))
        screen.blit(file_surface, (50, 70))
        # screen.blit(background, (0, 0))

        pygame.display.update()
        clock.tick(60)

    shade = pygame.Surface((file_surface.get_width(), 5))
    shade.fill((220, 220, 220))
    alpha = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        text = '加载完成'

        screen.fill((255, 255, 255))
        file_surface.fill((220, 220, 220))

        button_return.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
        if last_tick and not button_return.state:
            return
        last_tick = button_return.state
        load_progress.next()
        shade.set_alpha(alpha)
        alpha += 4.25
        file_surface.blit(shade, (0, 0))
        if alpha >= 255:
            break
        ff = font.render(text, 1, [0, 0, 0])
        screen.blit(ff, ff.get_rect(center=(620, 40)))
        screen.blit(file_surface, (50, 70))
        # screen.blit(background, (0, 0))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    sc = pygame.display.set_mode((1240, 720))
    main(sc)
