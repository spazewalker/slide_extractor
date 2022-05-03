from sys import argv
import cv2
from tqdm import tqdm
import time
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim
from glob import glob
import img2pdf
# Please note this script was writen in a hurry, just before an exam. So, don't judge the code quality😅

def get_basic(img):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img = cv2.resize(img, (0, 0), fx=0.1, fy=0.1)
  return img
  
def get_ssim(img1, imgs):
  flag = False
  if ssim(img1, imgs[-1]) > 0.9:
    flag = True
  return flag

if __name__ == '__main__':
  prev_imgs = []
  vidcap = cv2.VideoCapture(argv[1])
  success,image = vidcap.read()
  g_ = get_basic(image)
  prev_frame = np.zeros_like(g_)
  prev_imgs.append(g_)
  len_vid = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
  count = 0
  f_count = 0
  for i in tqdm(range(len_vid)):
    success,image = vidcap.read()
    if not success:
      break
    g_ = get_basic(image)
    if(not get_ssim(g_, prev_imgs)):
      cv2.imwrite("%sframe%s.jpg" % (argv[1],str(count).zfill(4)), image)     # save frame as JPEG file
      prev_imgs.append(g_)
      count += 1
    prev_frame=g_
    f_count+=1
  # vidcap.close()
  frames = glob("%sframe*.jpg" % argv[1])
  images = []
  for i in range(len(frames)):
    img = cv2.imread(frames[i])
    images.append(img)
  print("finding duplicates")
  dup = []
  for i in range(len(images)):
    for j in range(i+1, len(images)):
      s = ssim(get_basic(images[i]), get_basic(images[j]))
      if s > 0.9:
        dup.append(j)
  print("removing duplicates")
  for i in range(len(dup)):
    try:
      os.remove(frames[dup[i]])
    except:
      print("file {} not found".format(frames[dup[i]]))

  print("converting to pdf")

  frames = glob("%sframe*.jpg" % argv[1])
  with open("%s.pdf" % (argv[1]).split('.')[0], "wb") as f:
    f.write(img2pdf.convert(frames))
  
  print('removing frames')
  for i in range(len(frames)):
    try:
      os.remove(frames[i])
    except:
      print("file {} not found".format(frames[i]))
  print("done")
