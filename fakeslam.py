#!/usr/bin/env python3
import os
import sys
import time

sys.path.append("lib/macosx")
sys.path.append("lib/linux")

import numpy as np
from slam import SLAM
from renderer import Renderer
from display import Display2D, Display3D

if __name__ == "__main__":
  W,H = 640,480
  F = H  # with 45 degree FoV
  
  K = np.array([[F,0,W//2],[0,F,H//2],[0,0,1]])
  Kinv = np.linalg.inv(K)

  disp3d = Display3D()
  disp2d = Display2D(W, H)

  slam = SLAM(W, H, K)
  r = Renderer(W, H)

  fn = 0
  pos_x = 0
  dir_x = True
  while 1:
    frame = r.draw([pos_x,0,0])

    # ground truth pose
    pose = np.eye(4)
    pose[0,3] = pos_x

    slam.process_frame(frame, None)
    disp3d.paint(slam.mapp)

    img = slam.mapp.frames[-1].annotate(frame)
    disp2d.paint(img)

    # flip flop
    if pos_x > 10:
      dir_x = False
    elif pos_x < -10:
      dir_x = True
    pos_x += 0.5 * (1 if dir_x else -1)

    """
    fn += 1
    if fn == 5:
      slam.mapp.optimize(verbose=True, rounds=10)
      #print(slam.mapp.serialize())
      while 1:
        break
        time.sleep(1)
    """
