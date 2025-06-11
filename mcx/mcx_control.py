class MCX():
    def __init__(self):
        self.gripper_state = 0.0

    def connect(self, ip):
        pass
        
    def disconnect(self):
        """Disconnect from the robot."""
        if self.is_connected:
            try:
                self.is_connected = False
                print("Disconnected from the robot.")
            except Exception as e:
                print(f"Failed to disconnect from the robot: {e}")
        else:
            print("No active connection to disconnect.")


    def move_to_start(self):
        pass

    def get_joint_pos(self):
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    def get_linear_pos(self):
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    def get_cart_pos(self):
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def MoveJ(self, cords):
        pass

    def MoveL(self, cords):
        pass

    def MoveC(self, cords):
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