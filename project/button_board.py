import pygame


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


class ButtonPanel:
    def __init__(self, screen):
        self.screen = screen
        self.stop_button_path = 'Resourse/button_stop.png'
        self.left_button_path = 'Resourse/button_left.png'
        self.right_button_path = 'Resourse/button_right.png'
        self.recongnize_button = Button('Resourse/button_confirm.png', (100, 625), self.screen)
        self.refresh_button = Button('Resourse/button_refresh.png', (200, 625), self.screen)
        self.left_button = Button(self.left_button_path, (650, 625), self.screen)
        self.right_button = Button(self.right_button_path, (750, 625), self.screen)

    def render(self, stop: list):
        self.left_button_path = 'Resourse/button_left.png'
        self.right_button_path = 'Resourse/button_right.png'
        # stop[0] = 1 左极限, stop = 0 正常, stop[1] = 1 右极限
        if stop[0] == 1:
            self.left_button_path = self.stop_button_path
            self.left_button = Button(self.left_button_path, (650, 625), self.screen)
        if stop[1] == 1:
            self.right_button_path = self.stop_button_path
            self.right_button = Button(self.right_button_path, (750, 625), self.screen)
        self.recongnize_button.render()
        self.refresh_button.render()
        self.left_button.render()
        self.right_button.render()
