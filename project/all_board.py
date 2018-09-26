import pygame
from pygame.locals import *
import button_board
import white_board
import file_operator

WHITE = (255, 255, 255)
CYAN = (0, 255, 255)


class Painter:
    def __init__(self):
        file_operator.FileOperator.make_dirs()
        white_screen_width = 900
        white_screen_height = 650
        self.white_surface = pygame.Surface([white_screen_width, white_screen_height])

        button_screen_width = 900
        button_screen_height = 50
        self.button_surface = pygame.Surface([button_screen_width, button_screen_height])

        self.screen = pygame.display.set_mode((900, 650))
        pygame.display.set_caption("Drawboard")
        self.clock = pygame.time.Clock()
        self.brush = white_board.Brush(self.white_surface)

        self.text_list = []  # 现在这一张图里的标注信息
        self.current_surface_no = -1
        # 是否到了两侧的界限
        self.stop = [1, 1]

    def recognize(self, surface):
        # 保存图片
        self.current_surface_no = -1
        info_path = file_operator.FileOperator.save_and_recognize(surface)
        file_operator.FileOperator.load_file(self.text_list, info_path)

    def load_history_surface(self):
        num = self.current_surface_no  # -1代表画板
        if num < 0:
            self.stop[0] = (1 if (file_operator.FileOperator.find_pic_num() == 0) else 0)
            self.stop[1] = 1
            self.white_surface.fill(WHITE)
            self.text_list = []
        else:  # 读过去的信息
            self.stop[0] = (1 if (num == 0) else 0)
            self.stop[1] = 0
            pic_path = "Pictures/" + str(num) + ".png"
            image = pygame.image.load(pic_path).convert_alpha()
            self.white_surface.blit(image, (0, 0))
            info_path = "Infomation/" + str(num) + ".txt"
            self.text_list = file_operator.FileOperator.load_file(self.text_list, info_path)

    def show_surface(self, is_left: bool):
        sum_of_pics = file_operator.FileOperator.find_pic_num()
        num = self.current_surface_no
        if sum_of_pics == 0:
            self.load_history_surface()
            return
        if is_left:
            if num == -1:  # 最新编辑状态
                self.current_surface_no = sum_of_pics - 1
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
            if num == sum_of_pics - 1:
                self.current_surface_no = -1
            else:
                self.current_surface_no += 1

        self.load_history_surface()

    def run(self):
        self.white_surface.fill(WHITE)

        self.current_surface_no = -1
        self.load_history_surface()

        self.button_surface.fill(CYAN)

        while True:
            self.clock.tick(30)

            self.screen.blit(self.white_surface, (0, 0))
            self.screen.blit(self.button_surface, (0, 600))

            # 显示按钮
            buttons = button_board.ButtonPanel(self.screen)
            buttons.render(self.stop)

            # 显示信息
            if len(self.text_list) > 0:
                for word in self.text_list:
                    t = white_board.Text(word.position, word.content)
                    t.display_text(self.screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.white_surface.fill(WHITE)
                        self.text_list = []
                    if event.key == K_RETURN:  # 回车事件
                        self.recognize(self.white_surface)
                    if event.key == K_LEFT:
                        self.show_surface(is_left=True)
                    if event.key == K_RIGHT:
                        self.show_surface(is_left=False)
                elif event.type == MOUSEBUTTONDOWN:
                    if buttons.recongnize_button.is_over():
                        self.recognize(self.white_surface)
                    if buttons.refresh_button.is_over():
                        self.white_surface.fill(WHITE)
                        self.text_list = []
                    if buttons.left_button.is_over():
                        self.show_surface(is_left=True)
                    if buttons.right_button.is_over():
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
