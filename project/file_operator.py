import os
import pygame
import shape_analysis
import white_board


class FileOperator:
    def __init__(self):
        pass

    # 创建文件夹
    @staticmethod
    def make_dirs():
        if not os.path.exists("Pictures"):
            os.mkdir("Pictures")
        if not os.path.exists("Infomation"):
            os.mkdir("Infomation")

    # 返回图片总数
    @staticmethod
    def find_pic_num():
        pic_dir_path = "Pictures"
        max_num = len([name for name in os.listdir(pic_dir_path) if os.path.isfile(os.path.join(pic_dir_path, name))])
        return max_num

    # 保存并识别
    @staticmethod
    def save_and_recognize(surface: pygame.Surface):
        # 保存图片
        pic_dir_path = "Pictures"
        info_dir_path = "Infomation"
        max_num = FileOperator.find_pic_num()
        pic_path = os.path.join(pic_dir_path, str(max_num) + ".png")
        info_path = os.path.join(info_dir_path, str(max_num) + ".txt")
        pygame.image.save(surface, pic_path)
        info_file = open(info_path, 'a')

        # 识别图片
        ld = shape_analysis.ShapeAnalysis(pic_path)
        analysis_result = ld.analysis()
        for shape_data in analysis_result:
            info_file.write(shape_data.shape_type + " " + str(shape_data.list[0]) + "," + str(shape_data.list[1]))
            info_file.write('\n')

        info_file.close()
        return info_path

    # 加载描述信息
    @staticmethod
    def load_file(text_list: list, path: str):
        # 把读到的标注信息放入text_list中
        file_content = open(path)
        for line in file_content:
            type_str, pos_str = line.split()
            pos = [int(pos_str.split(',')[0]), int(pos_str.split(',')[1])]
            # text = Text(pos, type_str)
            text = white_board.Text(pos, type_str)
            text_list.append(text)
        file_content.close()
        return text_list
