import cv2 as cv
import numpy as np

color_max: str
color_min: str
count_max: int
count_min: int
img: np.ndarray

color_masks = dict(
    black=((0, 0, 0), (0, 0, 0)),
    blue=((0, 0, 255), (0, 0, 255)),
    green=((0, 255, 0), (0, 255, 0)),
    gray=((127, 127, 127), (127, 127, 127)),
    orange=((255, 165, 0), (255, 165, 0)),
    pink=((255, 0, 255), (255, 0, 255)),
    red=((255, 0, 0), (255, 0, 0)),
    yellow=((255, 255, 0), (255, 255, 0)),
)
color_count = []

for name, (lower, upper) in sorted(color_masks.items(), key=lambda o: o[1]):
    color_count.append(
        (
            len(
                cv.findContours(
                    cv.inRange(
                        cv.cvtColor(img, cv.COLOR_BGR2RGB),
                        np.array(lower),
                        np.array(upper),
                    ),
                    cv.RETR_TREE,
                    cv.CHAIN_APPROX_NONE,
                )[1]
            ),
            name,
        )
    )

key = lambda o: o[0]
count_max, color_max = max(color_count, key=key)
count_min, color_min = min(color_count, key=key)