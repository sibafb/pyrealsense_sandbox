#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyrealsense2 as rs
import numpy as np
import cv2

def shot():
    pass

if __name__ == '__main__':
    try:
        WIDTH = 640
        HEIGHT = 480

        # ストリーミング初期化
        config = rs.config()
        config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, WIDTH, HEIGHT, rs.format.z16, 30)


        pipeline = rs.pipeline()
        pipeline.start(config)

        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not color_frame or not depth_frame:
                continue
            # translation to OpenCV Format
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            # depth image to Colormap
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.08), cv2.COLORMAP_JET)      

            # Show Color images
            cv2.namedWindow('color_image', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('color_image', color_image)
            # Show Depth images
            cv2.namedWindow('depth_image', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('depth_image', depth_colormap)
            
            #enter q key to exit
            key = cv2.waitKey(1) & 0xff
            if key == ord("q"):
                break
                
    except KeyboardInterrupt:
        pass
    finally:
       pass
    