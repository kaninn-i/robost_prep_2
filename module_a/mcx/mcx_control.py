class MCX():
    def __init__(self):
        self.gripper_state = 0.0

    def connect(self, ip):
        pass
    
    def move_to_start(self):
        pass

    def get_joint_pos(self):
        return [1,1,1,1,1.1]
    def get_cart_pos(self):
        return [1,1,1,1,1.1]

    def MoveJ(self):
        pass

    def MoveL(self):
        pass

    def engage(self):
        pass

    def disengage(self):
        pass

    def manualCartMode(self):
        pass

    def manualJointMode(self):
        pass

    def setJointVelocity(self, velicity=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
        pass

    def setCartesianVelocity(self, velicity=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
        pass