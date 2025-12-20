
import random

# 两个人狭路相逢的例子
def person_movement():
    directions = ['left', 'right']

    def person(name):
        my_direction = random.choice(directions)
        while not_passed:
            if other_person_direction == my_direction:
                # 撞上了，换方向
                my_direction = random.choice(directions)
            # 结果可能又撞上...

    # 两个人不断"谦让"，但永远走不过去
