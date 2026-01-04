
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
import sys


class CarControlDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # 加载汽车模型（替换为你的模型路径）
        self.car = self.loader.loadModel("models/car.obj")
        # 如果是glTF格式
        # self.car = self.loader.loadModel("models/car.gltf")

        if self.car is None:
            print("无法加载模型！请检查路径")
            return

        # 设置模型到场景中
        self.car.reparentTo(self.render)
        self.car.setScale(0.1)  # 调整大小
        self.car.setPos(0, 10, 0)

        # 查找模型部件（部件名称需要在建模时设置）
        self.door_left = self.car.find("**/door_left")  # 左前门
        self.door_right = self.car.find("**/door_right")  # 右前门
        self.trunk = self.car.find("**/trunk")  # 后备箱
        self.hood = self.car.find("**/hood")  # 引擎盖

        # 初始化部件状态
        self.door_angle = 0
        self.trunk_angle = 0
        self.hood_angle = 0

        # 设置摄像机
        self.camera.setPos(0, -15, 5)
        self.camera.lookAt(0, 0, 0)

        # 设置灯光
        alight = AmbientLight('ambientLight')
        alight.setColor((0.5, 0.5, 0.5, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        dlight = DirectionalLight('directionalLight')
        dlight.setColor((0.8, 0.8, 0.8, 1))
        dlight.setShadowCaster(True, 512, 512)
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)

        # 添加控制指令文本
        self.add_instructions()

        # 绑定键盘控制
        self.accept("1", self.toggle_door, ["left"])
        self.accept("2", self.toggle_door, ["right"])
        self.accept("3", self.toggle_trunk)
        self.accept("4", self.toggle_hood)
        self.accept("q", sys.exit)

    def add_instructions(self):
        """添加操作说明"""
        instructions = [
            "控制指令:",
            "1 - 开关左前门",
            "2 - 开关右前门",
            "3 - 开关后备箱",
            "4 - 开关引擎盖",
            "Q - 退出程序"
        ]

        for i, text in enumerate(instructions):
            OnscreenText(
                text=text,
                pos=(-1.3, 0.9 - i * 0.05),
                scale=0.05,
                fg=(1, 1, 1, 1),
                align=TextNode.ALeft
            )

    def toggle_door(self, side):
        """开关车门"""
        if side == "left" and self.door_left:
            if self.door_angle == 0:
                # 开门
                self.door_left.setH(self.door_left.getH() + 60)
                self.door_angle = 60
            else:
                # 关门
                self.door_left.setH(self.door_left.getH() - 60)
                self.door_angle = 0

        elif side == "right" and self.door_right:
            if self.door_angle == 0:
                self.door_right.setH(self.door_right.getH() - 60)
                self.door_angle = 60
            else:
                self.door_right.setH(self.door_right.getH() + 60)
                self.door_angle = 0

    def toggle_trunk(self):
        """开关后备箱"""
        if self.trunk:
            if self.trunk_angle == 0:
                # 开启后备箱
                self.trunk.setP(self.trunk.getP() - 45)
                self.trunk_angle = 45
            else:
                # 关闭后备箱
                self.trunk.setP(self.trunk.getP() + 45)
                self.trunk_angle = 0

    def toggle_hood(self):
        """开关引擎盖"""
        if self.hood:
            if self.hood_angle == 0:
                self.hood.setP(self.hood.getP() + 30)
                self.hood_angle = 30
            else:
                self.hood.setP(self.hood.getP() - 30)
                self.hood_angle = 0

if __name__ == "__main__":
    app = CarControlDemo()
    app.run()

