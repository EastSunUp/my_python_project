
# 代码内容被删除,之前这里的代码内容是我自己写的.
# TODO 空闲时,记得完善相应代码内容

import time

timestamp = time.time()
while True:
    # if (time.time() - timestamp)/3 > 1:
    #     print(f"{time.time() - timestamp}s has been past")
    #     timestamp = time.time()
    if (time.time() - timestamp)  >= 3:
        print(f"{time.time() - timestamp}s has been past")
        timestamp = time.time()

