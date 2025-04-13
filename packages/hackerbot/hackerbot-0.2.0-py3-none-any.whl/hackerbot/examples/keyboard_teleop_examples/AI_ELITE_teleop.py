################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.01
#
# This script is an example of how to use the AI_ELITE_teleop behavior.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from hackerbot import Hackerbot
import time
import os

import sys
from select import select
from arm_teleop import ArmTeleop
from base_teleop import BaseTeleop, KBHit
from head_teleop import HeadTeleop

class AI_ELITE_Teleop(ArmTeleop, BaseTeleop, HeadTeleop):
    def __init__(self):
        self.kb = KBHit()

        self.robot = Hackerbot()
        self.robot.base.initialize()
        
        # Modify movement parameters
        self.step_size = 0.2 # mm
        self.max_l_step_size = 300.0 # mm/s
        self.max_r_step_size = 90.0 # degree/s
        
        self.joint_speed = 50

        self.j_agl_1 = 0
        self.j_agl_2 = 0
        self.j_agl_3 = 0
        self.j_agl_4 = 0
        self.j_agl_5 = 0
        self.j_agl_6 = 0

        self.yaw = 180
        self.pitch = 180

        self.base_command = None
        self.head_command = None
        self.arm_command = None

        self.stop = False
        self.last_key = None  # Track last keypress
        
        # Print initial instructions to terminal
        self.print_terminal_instructions()

    def print_terminal_instructions(self):
        """Print instructions to the terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\n" + "="*10 + " Robot Teleop Controls " + "="*10 + "\r")
        print("Base controls:\r")
        print("   ↑ / ↓    : FWD/BCK |   ← / →    : L/R | space  : STOP\r")
        print("=" * 30 + "\r")
        print("Head Controls:\r")
        print("   u/i : Yaw L/R |   j/k : Pitch U/D")
        print("=" * 30 + "\r")
        print("Arm Controls:\r")
        print("   q/w : Joint 1 L/R     |   a/s : Joint 2 BCK/FWD |   z/x : Joint 3 BCK/FWD")
        print("   e/r : Joint 4 BCK/FWD |   d/f : Joint 5 L/R     |   c/v : Joint 6 L/R")
        print("\nGripper:")
        print("   g/h    : Open/Close gripper | b    : Calibrate gripper\r")
        
        print("\nOther:")
        print("   o/p : increase/decrease step size | -/+ : decrease/increase speed\r")
        print("\nCTRL-C or 0 to quit\r")
        print("=" * 43 + "\r")

    def update_display(self):
        """Update step size and speed in place without adding new lines"""
        sys.stdout.write(f"\rCurrent step size: {self.step_size:.1f} | Current joint speed: {self.joint_speed}    ")
        sys.stdout.flush()  # Ensure immediate update

    def get_command(self):
        self.base_command = False
        self.head_command = False
        self.arm_command = False
        key = None
        # Read keyboard input
        if self.kb.kbhit() is not None:
            key = self.kb.getch()
            # print(f"key: {key}\r")
            while sys.stdin in select([sys.stdin], [], [], 0)[0]:  
                sys.stdin.read(1)

            if key == self.last_key:
                self.last_key = None
                return None, None  

            self.last_key = key  # Update last key

            # Check for quit conditions
            if key == '0':  # '0' key to quit
                self.stop = True
                return None, None
                
            if key == 'o':
                self.step_size += 0.1
                if self.step_size > 1: 
                    self.step_size = 1
            elif key == 'p':
                self.step_size -= 0.1
                if self.step_size < 0.1:
                    self.step_size = 0.1
            elif key == '-':
                self.joint_speed -= 10
                if self.joint_speed < 10:
                    self.joint_speed = 10
            elif key == '+':
                self.joint_speed += 10
                if self.joint_speed > 100:
                    self.joint_speed = 100
            if key in ['\x1b[A', '\x1b[B', '\x1b[D', '\x1b[C', ' ']:
                l_vel, r_vel = BaseTeleop.get_base_command_from_key(self, key)
                self.base_command = True
                return l_vel, r_vel
            elif key in ['u', 'i', 'j', 'k']:
                y, p = HeadTeleop.get_head_value_from_key(self, key)
                self.head_command = True
                return y, p
            elif key in ['q', 'w', 'a', 's', 'z', 'x', 'e', 'r', 'd', 'f', 'c', 'v', 'g', 'h', 'b']:
                command, value = ArmTeleop.get_arm_value_from_key(self, key)
                self.arm_command = True
                return command, value
            else:
                return None, None

        else:
            self.last_key = None
            return 0.0, 0.0

    def run(self):
        while not self.stop:
            input_1, input_2 = self.get_command()
            if input_1 is not None and input_2 is not None:
                response = None  # Initialize response
                if self.base_command:
                    response = self.robot.base.drive(input_1, input_2, block=False)
                    time.sleep(0.01)
                elif self.head_command:
                    response = self.robot.head.look(input_1, input_2, self.joint_speed)
                    time.sleep(0.01)
                elif self.arm_command:
                    command = input_1
                    value = input_2
                    if isinstance(command, int):  # Joint movement
                        # Limit joint angles based on which joint
                        max_angle = 175.0 if command == 6 else 165.0
                        if abs(value) <= max_angle:
                            response = self.robot.arm.move_joint(command, value, self.joint_speed)
                    elif command == 'gripper_open':
                        response = self.robot.arm.gripper.open()
                    elif command == 'gripper_close':
                        response = self.robot.arm.gripper.close()
                    elif command == 'gripper_calibrate':
                        response = self.robot.arm.gripper.calibrate()
                    
                    time.sleep(0.2)

                if response == False:
                    break

            input_1 = None
            input_2 = None
            self.update_display()

    def stow(self):
        self.robot.arm.move_joints(0,0,0,0,0,0,50) 
        self.robot.head.look(180,180,50)

    def cleanup(self):
        """Cleanup method to properly shut down the robot and restore terminal settings"""
        try:
            # Restore terminal settings
            self.kb.set_normal_term()
            # self.robot.stop_driver()
            self.stow()
            # Destroy the robot connection
            self.robot.base.destroy(auto_dock=True)
            
        except Exception as e:
            print(f"\nError during cleanup: {e}")
            # Try to restore terminal settings even if there's an error
            try:
                self.kb.set_normal_term()
            except:
                pass

    def __del__(self):
        """Destructor to ensure cleanup is called"""
        self.cleanup()

# Main entry point
if __name__ == '__main__':
    teleop = None
    try:
        teleop = AI_ELITE_Teleop()
        teleop.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if teleop:
            teleop.cleanup()