
import sys
import subprocess
from pathlib import Path


def get_pip_location():
    result = subprocess.run(['pip', '-V'], capture_output=True, text=True)
    output = result.stdout
    return output.split('from')[1].strip()

pip_location = get_pip_location()
print(f"The pip installation directory is: {pip_location}")
python_directory = Path(sys.executable).parent
print(f"Python解释器的安装路径是: {python_directory}")

# this code is to check whether your computer system has configured the python path
# This code checks whether the Python path has been configured on your computer system.
if "python" in sys.executable.lower():
    print('python 已经添加到环境变量中')
else:
    print('python 还没有添加到环境变量中')


