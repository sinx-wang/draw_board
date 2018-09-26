import cv2 as cv
import numpy as np


# 数据结构，String shape_type, [x, y]
class ShapeData:
    def __init__(self, shape_type, info_list):
        self.shape_type = shape_type
        self.list = info_list


class ShapeAnalysis:
    def __init__(self, filename):
        self.src = cv.imread(filename)
        self.shape_list = []

    def analysis(self):
        #  h, w, ch = self.src.shape
        #  result = np.zeros((h, w, ch), dtype=np.uint8)
        # 二值化图像
        print("start to detect lines……")
        gray = cv.cvtColor(self.src, cv.COLOR_BGR2GRAY)
        ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

        out_binary, contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in range(len(contours)):

            # 轮廓逼近
            par = 0.01
            i = 1
            while i >= 0:
                epsilon = par * cv.arcLength(contours[cnt], True)
                approx = cv.approxPolyDP(contours[cnt], epsilon, True)

                # 分析几何形状
                corners = len(approx)
                print(corners)
                if corners == 3:
                    shape_type = "triangle"
                    break
                elif corners == 4:
                    shape_type = "rectangle"
                    break
                elif corners >= 10:
                    shape_type = "circle"
                    break
                elif 4 < corners < 10:
                    shape_type = "polygon"
                    par = 0.10
                else:
                    shape_type = "others"
                    par = 0.01

                i -= 1

            # 求解中心位置
            mm = cv.moments(contours[cnt])
            cx = int(mm['m10'] / mm['m00'])
            cy = int(mm['m01'] / mm['m00'])
            # cv.circle(result, (cx, cy), 3, (0, 0, 255), -1)
            print(cx, cy)

            print("形状: %s" % shape_type)

            shape = ShapeData(shape_type, [cx, cy])
            self.shape_list.append(shape)

        return self.shape_list


if __name__ == "__main__":
    ld = ShapeAnalysis("Pictures/7.png")
    print(ld.analysis())
