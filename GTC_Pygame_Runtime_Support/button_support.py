import sys
import pygame
import os
from typing import List, Tuple

pygame.init()


class FeedbackButton:
    # 初始化反馈按钮
    def __init__(self, size: List[int], pos: List[int], text: str, text_size: int,
                 surface: pygame.Surface, bg_color=(30, 255, 189), border_color=(255, 255, 255),
                 change_color: Tuple[Tuple[int, int, int], Tuple[int, int, int]] = ((0, 112, 255), (0, 255, 112)),
                 text_color: List[int] = (0, 0, 0), speed: int = 2, font_type: str = 'microsoftyahei'):
        self.size = size
        self.pos = pos

        if os.path.exists(font_type):
            self.text = pygame.font.Font(font_type, text_size).render(text, True, text_color)
        else:
            self.text = pygame.font.SysFont(font_type, text_size).render(text, True, text_color)
        self.color = [bg_color, border_color, change_color]
        self.font_rect = self.text.get_rect()

        self.font_rect.center = (pos[0] + size[0] // 2, pos[1] + size[1] // 2)
        self.iter = 0
        self.color_iter = 0
        self.speed = speed

        self.color_delta = [(self.color[2][0][0] - self.color[2][1][0]) / 4,
                            (self.color[2][0][1] - self.color[2][1][1]) / 4,
                            (self.color[2][0][2] - self.color[2][1][2]) / 4]
        self.surface = surface
        self.temp_color = [0, 0, 0]
        self.state = False
        self.lock = False

    def in_area(self, mouse_pos):
        if self.pos[0] <= mouse_pos[0] <= self.size[0] + self.pos[0] and self.pos[1] <= mouse_pos[1] <= self.size[1] + \
                self.pos[1]:
            return True
        return False

    # 更新按钮状态并绘制
    def operate(self, mouse_pos, effectiveness):
        if self.in_area(mouse_pos):
            self.iter += self.speed
            self.iter = min(self.iter, 12)
            if effectiveness and not self.lock:
                self.color_iter += 1
                self.color_iter = min(4, self.color_iter)
                self.state = True
            else:
                self.color_iter -= 1
                self.color_iter = max(0, self.color_iter)
                self.state = False
            if self.lock and not effectiveness:
                self.lock = False
        else:
            self.iter -= self.speed
            self.iter = max(0, self.iter)
            self.color_iter -= 1
            self.color_iter = max(0, self.color_iter)
            self.state = False
            if effectiveness:
                self.lock = True
            else:
                self.lock = False

        self.temp_color = list(self.color[2][0])

        for item in range(len(self.temp_color)):
            self.temp_color[item] -= self.color_iter * self.color_delta[item]

        pygame.draw.rect(self.surface, self.temp_color, (self.pos[0] - self.iter, self.pos[1] - self.iter,
                                                         self.size[0] + 2 * self.iter, self.size[1] + 2 * self.iter),
                         border_radius=min(self.size) // 4, width=6)
        pygame.draw.rect(self.surface, self.color[0], [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4)
        pygame.draw.rect(self.surface, self.color[1], [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4, width=4)

        self.surface.blit(self.text, self.font_rect)

    def change_pos(self, pos: Tuple[int, int]):
        self.pos = pos
        self.font_rect.center = (pos[0] + self.size[0] // 2, pos[1] + self.size[1] // 2)


class DelayButton:
    # 初始化延迟响应按钮
    def __init__(self, size, pos, text, text_size, surface, bg_color=(30, 255, 189), border_color=(255, 255, 255),
                 change_color=((0, 112, 255), (0, 255, 112)), text_color=(0, 0, 0), speed=2):
        self.size = size
        self.pos = pos
        # 使用默认的黑体字体
        self.text = pygame.font.SysFont('SimHei', text_size).render(text, True, text_color)
        self.color = [bg_color, border_color, change_color]
        self.font_rect = self.text.get_rect()
        self.font_rect.center = (pos[0] + size[0] // 2,
                                 pos[1] + size[1] // 2)
        self.iter = 0
        self.color_iter = 0
        self.speed = speed
        self.color_delta = [(self.color[2][0][0] - self.color[2][1][0]) / 4,
                            (self.color[2][0][1] - self.color[2][1][1]) / 4,
                            (self.color[2][0][2] - self.color[2][1][2]) / 4]
        self.surface = surface
        self.temp_color = [0, 0, 0]
        self.state_1 = False
        self.state_2 = False
        self.last = False
        self.click = 0

    # 检查鼠标位置是否在按钮区域内
    def in_area(self, mouse_pos):
        if self.pos[0] <= mouse_pos[0] <= self.size[0] + self.pos[0] and self.pos[1] <= mouse_pos[1] <= self.size[1] + \
                self.pos[1]:
            return True
        return False

    # 更新按钮状态并绘制
    def operate(self, mouse_pos, effectiveness):
        if self.in_area(mouse_pos):
            self.state_2 = True
            if effectiveness:
                self.state_1 = True
                if not self.last:
                    self.last = True
                    self.click += 1
            else:
                self.last = False
        else:
            if effectiveness:
                self.state_2 = False
                self.state_1 = False
                self.last = False
                self.click = 0
            if not self.state_1:
                self.state_2 = False
        if self.state_2:
            self.iter += self.speed
            self.iter = min(self.iter, 12)
        else:
            self.iter -= self.speed
            self.iter = max(self.iter, 0)
        if self.state_1:
            self.color_iter += 1
            self.color_iter = min(4, self.color_iter)
        else:
            self.color_iter -= 1
            self.color_iter = max(0, self.color_iter)

        self.temp_color = list(self.color[2][0])
        # 根据颜色迭代值调整颜色
        for item in range(len(self.temp_color)):
            self.temp_color[item] -= self.color_iter * self.color_delta[item]
        # 绘制按钮背景
        pygame.draw.rect(self.surface, self.temp_color, (self.pos[0] - self.iter, self.pos[1] - self.iter,
                                                         self.size[0] + 2 * self.iter, self.size[1] + 2 * self.iter),
                         border_radius=min(self.size) // 4, width=6)
        pygame.draw.rect(self.surface, self.color[0], [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4)
        pygame.draw.rect(self.surface, self.color[1], [self.pos[0], self.pos[1], self.size[0], self.size[1]],
                         border_radius=min(self.size) // 4, width=4)

        # 显示文本
        self.surface.blit(self.text, self.font_rect)

# if __name__ == '__main__':
#     screen = pygame.display.set_mode((500, 500))
#     # 创建反馈按钮实例
#     button_1 = FeedbackButton([80, 40], [20, 20], '按钮', 20
