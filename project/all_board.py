import os
import pygame
from pygame.locals import *
import shape_analysis


class Button:
    def __init__(self, image, position, screen):
        self.image = pygame.image.load(image).convert_alpha()
        self.position = position
        self.screen = screen

    # 判断鼠标是否在按钮上
    def is_over(self):
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.image.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def render(self):
        x, y = self.position
        w, h = self.image.get_size()
        self.screen.blit(self.image, (x - w / 2, y - h / 2))


class Brush:
    def __init__(self, screen):
        self.screen = screen
        self.color = (0, 0, 0)
        self.size = 1
        self.drawing = False
        self.last_pos = None

    def start_draw(self, pos):
        self.drawing = True
        self.last_pos = pos

    def end_draw(self):
        self.drawing = False

    def draw(self, pos):
        if self.drawing:
            # pygame.draw.circle(self.screen, self.color, pos, self.size)
            pygame.draw.line(self.screen, self.color, self.last_pos, pos, self.size * 2)
            self.last_pos = pos


class Text:
    def __init__(self, position, content):
        self.content = content
        self.position = position

    def display_text(self, screen):
        pygame.font.init()
        self.my_font = pygame.font.SysFont("arial", 16)
        self.text_surface = self.my_font.render(self.content, True, (0, 0, 0))
        x, y = self.position
        screen.blit(self.text_surface, (x, y))


class Painter:
    def __init__(self):
        self.make_dirs()
        white_screen_width = 900
        white_screen_height = 650
        self.white_surface = pygame.Surface([white_screen_width, white_screen_height])

        button_screen_width = 900
        button_screen_height = 50
        self.button_surface = pygame.Surface([button_screen_width, button_screen_height])

        self.screen = pygame.display.set_mode((900, 650))
        pygame.display.set_caption("Drawboard")
        self.clock = pygame.time.Clock()

        self.text_list = []  # 现在这一张图里的标注信息
        self.current_surface_no = -1
        # 是否到了两侧的界限
        self.left_stop = True
        self.right_stop = True

    @staticmethod
    def make_dirs():
        if not os.path.exists("Pictures"):
            os.mkdir("Pictures")
        if not os.path.exists("Infomation"):
            os.mkdir("Infomation")

    @staticmethod
    def find_pic_num():
        pic_dir_path = "Pictures"
        max_num = 0
        max_num = len([name for name in os.listdir(pic_dir_path) if os.path.isfile(os.path.join(pic_dir_path, name))])
        return max_num

    def recognize(self, surface):
        # 保存图片
        self.current_surface_no = -1
        pic_dir_path = "Pictures"
        info_dir_path = "Infomation"
        max_num = self.find_pic_num()
        pic_path = os.path.join(pic_dir_path, str(max_num) + ".png")
        info_path = os.path.join(info_dir_path, str(max_num) + ".txt")
        pygame.image.save(surface, pic_path)
        info_file = open(info_path, 'a')

        # 识别图片
        ld = shape_analysis.ShapeAnalysis(pic_path)
        analysis_result = ld.analysis()
        for shape_data in analysis_result:
            info_file.write(shape_data.shape_type + " " + str(shape_data.list[0]) + "," +str(shape_data.list[1]))
            info_file.write('\n')

        info_file.close()
        self.load_info(info_path)

    def load_info(self, path):
        # 把读到的标注信息放入text_list中
        file_content = open(path)
        for line in file_content:
            type_str, pos_str = line.split()
            pos = [int(pos_str.split(',')[0]), int(pos_str.split(',')[1])]
            text = Text(pos, type_str)
            self.text_list.append(text)
        file_content.close()

    def load_history_surface(self):
        num = self.current_surface_no  # -1代表画板

        if num < 0:
            if self.find_pic_num() == 0:
                self.left_stop = True
            else:
                self.left_stop = False
            self.right_stop = True
            self.white_surface.fill((255, 255, 255))
            self.text_list = []
        else: # 读过去的
            if num == 0:
                self.left_stop = True
            else:
                self.left_stop = False
            self.right_stop = False
            pic_path = "Pictures/" + str(num) + ".png"
            image = pygame.image.load(pic_path).convert_alpha()
            self.white_surface.blit(image, (0, 0))

            info_path = "Infomation/" + str(num) + ".txt"
            self.load_info(info_path)

    def button_view(self):
        stop_button_path = 'Resourse/button_stop.png'
        self.recongnize_button = Button('Resourse/button_confirm.png', (100, 625), self.screen)
        self.refresh_button = Button('Resourse/button_refresh.png', (200, 625), self.screen)
        if self.left_stop:
            left_button_path = stop_button_path
        else:
            left_button_path = 'Resourse/button_left.png'
        if self.right_stop:
            right_button_path = stop_button_path
        else:
            right_button_path = 'Resourse/button_right.png'
        self.left_button = Button(left_button_path, (650, 625), self.screen)
        self.right_button = Button(right_button_path, (750, 625), self.screen)
        self.recongnize_button.render()
        self.refresh_button.render()
        self.left_button.render()
        self.right_button.render()

    def show_surface(self, is_left):
        sum = self.find_pic_num()
        num = self.current_surface_no
        if sum == 0:
            self.load_history_surface()
            return
        if is_left:
            if num == -1:  # 最新编辑状态
                self.current_surface_no = sum - 1
                self.text_list = []
            elif num == 0:
                return
            else:
                self.current_surface_no -= 1
                self.text_list = []
        else:
            if num == -1:
                return
            self.text_list = []
            if num == sum - 1:
                self.current_surface_no = -1
            else:
                self.current_surface_no += 1

        self.load_history_surface()

    def run(self):
        self.white_surface.fill((255, 255, 255))

        self.current_surface_no = -1
        self.load_history_surface()

        self.button_surface.fill((0, 255, 255))
        self.brush = Brush(self.white_surface)

        while True:
            self.clock.tick(30)

            self.screen.blit(self.white_surface, (0, 0))
            self.screen.blit(self.button_surface, (0, 600))

            self.button_view()

            if len(self.text_list) > 0:
                for word in self.text_list:
                    t = Text(word.position, word.content)
                    t.display_text(self.screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.white_surface.fill((255, 255, 255))
                        self.text_list = []
                    if event.key == K_RETURN:  # 回车事件
                        self.recognize(self.white_surface)
                    if event.key == K_LEFT:
                        self.show_surface(is_left=True)
                    if event.key == K_RIGHT:
                        self.show_surface(is_left=False)
                elif event.type == MOUSEBUTTONDOWN:
                    if self.recongnize_button.is_over():
                        self.recognize(self.white_surface)
                    if self.refresh_button.is_over():
                        self.white_surface.fill((255, 255, 255))
                        self.text_list = []
                    if self.left_button.is_over():
                        self.show_surface(is_left=True)
                    if self.right_button.is_over():
                        self.show_surface(is_left=False)
                    self.brush.start_draw(pygame.mouse.get_pos())
                elif event.type == MOUSEMOTION:
                    self.brush.draw(event.pos)
                elif event.type == MOUSEBUTTONUP:
                    self.brush.end_draw()
            pygame.display.update()


if __name__ == '__main__':
    app = Painter()
    app.run()
