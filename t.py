max_top, max_right, max_bottom, max_left = None, None, None, None
top, right, bottom, left = 1,2,3,4
if not max_top or top < max_top:
    print(1)
    max_top = top
if not max_right or right > max_right:
    print(2)
    max_right = right
if not max_bottom or bottom > max_bottom:
    print(3)
    max_bottom = bottom
if not max_bottom or bottom < max_bottom:
    print(4)
    max_left = left