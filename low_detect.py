# -*- coding:utf-8 -*-

# import tensorflow as tf
import cv2
import numpy as np


class detect:
    def __init__(self, pic):
        # self.pic = cv2.imread(pic_path)
        self.pic = pic
        if self.pic is None:
            print("Invalid Picture Path")
            exit(0)
        # cv2.imshow('image', self.pic)
        # self.new=cv2.imread(pic_path)
        self.new = pic

    def rd2gray(self):
        self.gray = cv2.cvtColor(self.pic, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('picture', self.gray)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def edgecutting(self):
        low = 50
        high = 150
        self.can = cv2.Canny(self.gray, low, high)

    def interest(self, vertices):
        mask = np.zeros_like(self.can)
        if len(self.can.shape) > 2:
            channel_count = self.can.shape[2]
            ignore_mask_color = (255,) * channel_count
        else:
            ignore_mask_color = 255

        cv2.fillPoly(mask, [vertices], ignore_mask_color)
        self.mas = cv2.bitwise_and(self.can, mask)

    def hough(self):
        rho = 2  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 15  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 40  # minimum number of pixels making up a line
        max_line_gap = 20  # maximum gap in pixels between connectable line segments
        # Hough Transform 检测线段，线段两个端点的坐标存在lines中
        self.lines = cv2.HoughLinesP(self.mas, rho, theta, threshold, np.array([]),
                                     min_line_length, max_line_gap)

    def draw_lines(self, color=[0, 0, 255], thickness=3):
        left_lines_x = []
        left_lines_y = []
        right_lines_x = []
        right_lines_y = []
        line_ymax = 0
        line_ymin = 999
        for line in self.lines:
            for x1, y1, x2, y2 in line:
                line_ymax = max(y1, y2, line_ymax)
                line_ymin = min(y1, y2, line_ymin)
                if x2 == x1:
                    continue
                else:
                    k = (y2 - y1) / (x2 - x1)
                if k > 0.3:
                    left_lines_x.extend([x1, x2])
                    left_lines_y.extend([y1, y2])
                elif k < -0.3:
                    right_lines_x.extend([x1, x2])
                    right_lines_y.extend([y1, y2])
        if len(left_lines_x):
            left_line_k, left_line_b = np.polyfit(left_lines_x, left_lines_y, 1)
            cv2.line(self.new, (int((line_ymax - left_line_b) / left_line_k), line_ymax),
                     (int((line_ymin - left_line_b) / left_line_k), line_ymin), color, thickness)
        if len(right_lines_x):
            right_line_k, right_line_b = np.polyfit(right_lines_x, right_lines_y, 1)
            cv2.line(self.new, (int((line_ymax - right_line_b) / right_line_k), line_ymax),
                     (int((line_ymin - right_line_b) / right_line_k), line_ymin), color, thickness)

    def execute(self):
        self.rd2gray()
        self.edgecutting()
        left = [0, self.can.shape[0]]
        right = [self.can.shape[1], self.can.shape[0]]
        apex = [self.can.shape[1] / 2, 310]
        vertices = np.array([left, right, apex], np.int32)
        self.interest(vertices)
        self.hough()
        self.draw_lines()
        return self.new
        # cv2.imshow('canny', self.new)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


if __name__ == '__main__':
    # path = './solidWhiteCurve.jpg'
    # carc = detect(path)
    # carc.execute()
    path = './solidWhiteRight.mp4'
    path = './solidYellowLeft.mp4'
    path = './challenge.mp4'

    video = cv2.VideoCapture(path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 保存为xvid格式，xvid是一种视频编解码器
    fps = video.get(cv2.CAP_PROP_FPS)
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter('ChallengeOutput.avi', fourcc, fps, size)

    while (video.isOpened()):
        ret, frame = video.read()
        # print(shape(frame))
        if ret == True:
            carc = detect(frame)
            new_pic = carc.execute()
            out.write(new_pic)
            cv2.imshow('frame', new_pic)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    video.release()
    out.release()
    cv2.destroyAllWindows()
