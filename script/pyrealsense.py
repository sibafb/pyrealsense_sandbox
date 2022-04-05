#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyrealsense2 as rs
import numpy as np
import cv2


if __name__ == '__main__':
    try:
        WIDTH = 640
        HEIGHT = 480

        # ストリーミング初期化
        #https://intelrealsense.github.io/librealsense/python_docs/_generated/pyrealsense2.config.html#pyrealsense2.config.enable_stream
        config = rs.config()
        config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, WIDTH, HEIGHT, rs.format.z16, 30)
        config.enable_stream(rs.stream.infrared, 1, WIDTH, HEIGHT, rs.format.y8, 6)
        config.enable_stream(rs.stream.infrared, 2, WIDTH, HEIGHT, rs.format.y8, 6)


        pipeline = rs.pipeline()
        pipeline.start(config)

        while True:
            frames = pipeline.wait_for_frames()

            #https://intelrealsense.github.io/librealsense/python_docs/_generated/pyrealsense2.composite_frame.html#pyrealsense2-composite-frame
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            ir1_frame = frames.get_infrared_frame(1)
            ir2_frame = frames.get_infrared_frame(2)

            if not color_frame or not depth_frame or not ir1_frame or not ir2_frame:
                continue
            # translation to OpenCV Format
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            ir1_image = np.asanyarray(ir1_frame.get_data())
            ir2_image = np.asanyarray(ir2_frame.get_data())
            # depth image to Colormap
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.08), cv2.COLORMAP_JET)      

            # Show Color images
            cv2.namedWindow('color_image', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('color_image', color_image)
            # Show Depth images
            cv2.namedWindow('depth_image', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('depth_image', depth_colormap)

            # Show Ir1 images
            cv2.namedWindow('ir1_image', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('ir1_image', ir1_image) 

            # Show Ir2 images
            cv2.namedWindow('ir2_image', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('ir2_image', ir2_image) 
            
            #enter q key to exit
            key = cv2.waitKey(1) & 0xff
            if key == ord("q"):
                break
                
    except KeyboardInterrupt:
        pass
    finally:
       pass
    