# -*- coding:utf-8 -*-

import tensorflow as tf
import numpy as np
import glob


class camera:
    def __init__(self, pic):
        self.pic = pic

    def getCameraCalibrationCoefficients(self, chessboardname, nx, ny):  # 计算相机畸变系数
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((ny * nx, 3), np.float32)
        objp[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d points in real world space
        imgpoints = []  # 2d points in image plane.

        images = glob.glob(chessboardname)
        if len(images) > 0:
            print("images num for calibration : ", len(images))
        else:
            print("No image for calibration.")
            return

        ret_count = 0
        for idx, fname in enumerate(images):
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_size = (img.shape[1], img.shape[0])
            # Finde the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

            # If found, add object points, image points
            if ret == True:
                ret_count += 1
                objpoints.append(objp)
                imgpoints.append(corners)

        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = \
            cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)

    def undistortImage(self, distortImage):
        return cv2.undistort(distortImage, self.mtx, self.dist, None, self.mtx)

    def execute(self):
        self.nx = 9
        self.ny = 6
        self.ret, self.mtx, self.dist, self.rvecs, \
        self.tvecs = self.getCameraCalibrationCoefficients('/camera_cal/calibration*.jpg', nx, ny)
