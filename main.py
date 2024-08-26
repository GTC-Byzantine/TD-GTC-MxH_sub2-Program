'''
	Name: 2025年贵阳市师生素养提升活动作品-
	Description: 一款可以
	Author: (评审公平原因,不透漏)
	Support library: python(>=3.9 bit)、pycharm、sys、time、random
	Version: 0.202408224-02
	Tags: 学生、人工智能
'''
import pygame
import sys
import GTC_Pygame_Runtime_Support as PRS

# 初始化Pygame
pygame.init()

# 设置窗口尺寸
window_width = 1240
window_height = 720

try:
    # 创建窗口
    screen = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption("数学小帮手")
    icon = pygame.image.load('Data/Icon/math-home.ico')
    pygame.display.set_icon(icon)

    # 加载背景图片
    background = pygame.image.load('Data/Image/bk.png')
except pygame.error as e:
    print(f"加载资源失败: {e}")
    pygame.quit()
    sys.exit()


# 定义Button类，并使用指定字体文件
class Button:
    def __init__(self, x, y, width, height, color, text, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color

        try:
            # 加载并使用'./ddjbt.ttf'作为字体，增大字体大小以匹配按钮尺寸
            self.font = pygame.font.Font('./ddjbt.ttf', 62)
        except pygame.error as e:
            print(f"加载字体失败: {e}")
            pygame.quit()
            sys.exit()
        self.clicked = False
        self.hovering = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and self.clicked:
            if self.rect.collidepoint(event.pos):
                print(f"准备启动 {self.text} 模块")
                self.clicked = False


showing_surface = pygame.Surface((1240, 720))
button_note = PRS.button_support.FeedbackButton([280, 80], [590, 300], '课堂小记', 62, showing_surface,
                                                bg_color=[0, 145, 220],
                                                border_color=[209, 240, 255], text_color=[255, 255, 255],
                                                font_type='ddjbt.ttf', change_color=((0, 145, 220), (0, 220, 145)))
button_harbor = PRS.button_support.FeedbackButton([280, 80], [910, 300], '数学港湾', 62, showing_surface,
                                                  bg_color=[0, 145, 220],
                                                  border_color=[209, 240, 255], text_color=[255, 255, 255],
                                                  font_type='ddjbt.ttf', change_color=((0, 145, 220), (0, 220, 145)))
button_test = PRS.button_support.FeedbackButton([280, 80], [590, 420], '测试园地', 62, showing_surface,
                                                bg_color=[0, 145, 220],
                                                border_color=[209, 240, 255], text_color=[255, 255, 255],
                                                font_type='ddjbt.ttf', change_color=((0, 145, 220), (0, 220, 145)))
button_field = PRS.button_support.FeedbackButton([280, 80], [910, 420], '学习园地', 62, showing_surface,
                                                 bg_color=[0, 145, 220],
                                                 border_color=[209, 240, 255], text_color=[255, 255, 255],
                                                 font_type='ddjbt.ttf', change_color=((0, 145, 220), (0, 220, 145)))

running = True
while running:
    # showing_surface = showing_surface_t
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 绘制背景图片
    showing_surface.blit(background, (0, 0))

    button_note.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    button_harbor.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    button_test.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    button_field.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])

    screen.blit(showing_surface, (0, 0))
    pygame.display.update()

# 清理并关闭Pygame
pygame.quit()
sys.exit()
