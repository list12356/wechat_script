from PIL import ImageGrab
import numpy as np
import cv2

from .constant import MALE, FEMALE


# bgr
TEMPLATE_MALE = cv2.imread("./image/male.png", 0)
# TEMPLATE_MALE = TEMPLATE_MALE[:, :, 0]
TEMPLATE_FEMALE = cv2.imread("./image/female.png", 0)
# TEMPLATE_FEMALE = TEMPLATE_FEMALE[:, :, 2]

DEBUG_NUM = 0

def get_gender(x, y):
    global DEBUG_NUM
    img = np.array(ImageGrab.grab())
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img[y + 43: y + 66, x + 38: x + 248, :]
    # cv2.imwrite('./test_{!s}.png'.format(DEBUG_NUM), img)
    # DEBUG_NUM += 1

    corr_male = cv2.matchTemplate(img[:, :, 0], TEMPLATE_MALE, cv2.TM_CCOEFF_NORMED)
    corr_male = np.max(corr_male)
    corr_female = cv2.matchTemplate(img[:, :, 2], TEMPLATE_FEMALE, cv2.TM_CCOEFF_NORMED)
    corr_female = np.max(corr_female)
    print('%.3f, %.3f' % (corr_male, corr_female))
    if max(corr_female, corr_male) < 0.9:
        return 0
    return MALE if corr_male > corr_female else FEMALE