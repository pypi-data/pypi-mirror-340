#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2017 - 2025 VECTIONEER.
#

import time

from .system_defs import States, StateEvents, ModeCommands, Modes, InterpreterEvents, InterpreterStates, \
    MotionGeneratorStates


class RobotCommand(object):
    """Class represents a state machine of the robot arm.

        Args:
            req(motorcortex.Request): reference to a Request instance
            motorcortex_types(motorcortex.MessageTypes): reference to a MessageTypes instance
            system_id(int): system id, for example for the dual-arm robot

    """

    def __init__(self, req, motorcortex_types, system_id=None):
        self.__Motorcortex = motorcortex_types.getNamespace("motorcortex")
        self.__motorcortex_types = motorcortex_types
        self.__req = req
        self.__kinematics_update_counter = 0
        self.__system_id = system_id

    @staticmethod
    def __addSystem(name, system_id):
        if not system_id:
            return name
        return f"{name}{system_id:02d}"

    def off(self):
        """Switch robot to Off state.

            Returns:
                bool: True if operation is completed, False if failed

        """

        self.__req.setParameter("root/Logic/stateCommand", StateEvents.GOTO_OFF_E.value).get()
        actual_state = self.__req.getParameter("root/Logic/state").get().value[0]

        while actual_state != States.OFF_S.value:
            actual_state = self.__req.getParameter("root/Logic/state").get().value[0]
            time.sleep(0.1)

        return True

    def disengage(self):
        """Switch robot to Disengage state.

            Returns:
                bool: True if operation is completed, False if failed

        """

        self.__req.setParameter("root/Logic/stateCommand", StateEvents.GOTO_DISENGAGED_E.value).get()
        actual_state = self.__req.getParameter("root/Logic/state").get().value[0]

        # if actual_state == States.DISENGAGED_S.value:
        #     return True
        # elif (actual_state == States.OFF_S.value) or \
        #         (actual_state == States.OFF_TO_DISENGAGED_T.value) or \
        #         (actual_state == States.ENGAGED_TO_DISENGAGED_T.value):
        #     self.__req.setParameter("root/Logic/stateCommand", StateEvents.GOTO_DISENGAGED_E.value).get()
        # elif (actual_state == States.DISENGAGED_TO_ENGAGED_T.value) or \
        #         (actual_state == States.ENGAGED_S.value):
        #     self.__req.setParameter("root/Logic/stateCommand", StateEvents.GOTO_DISENGAGED_E.value).get()
        # else:
        #     print("Can not switch off from state: %d" % actual_state)
        #     return False

        while actual_state != States.DISENGAGED_S.value:
            actual_state = self.__req.getParameter("root/Logic/state").get().value[0]
            time.sleep(0.1)

        return True

    def engage(self):
        """Switch robot to Engage state.

            Returns:
                bool: True if operation is completed, False if failed

        """

        self.__req.setParameter("root/Logic/stateCommand", StateEvents.GOTO_ENGAGED_E.value).get()
        actual_state = self.__req.getParameter("root/Logic/state").get().value[0]

        # if actual_state == States.ENGAGED_S.value:
        #     return True
        # elif (actual_state == States.DISENGAGED_TO_ENGAGED_T.value) or \
        #         (actual_state == States.ENGAGED_TO_DISENGAGED_T.value) or \
        #         (actual_state == States.DISENGAGED_S.value):
        #     self.__req.setParameter("root/Logic/stateCommand", StateEvents.GOTO_ENGAGED_E.value).get()
        #
        # elif (actual_state == States.OFF_TO_DISENGAGED_T.value) or \
        #         (actual_state == States.DISENGAGED_TO_OFF_T.value) or \
        #         (actual_state == States.OFF_S.value):
        #     self.__req.setParameter("root/Logic/stateCommand", StateEvents.GOTO_DISENGAGED_E.value).get()
        #     self.__req.setParameter("root/Logic/stateCommand", StateEvents.GOTO_ENGAGED_E.value).get()
        # else:
        #     print("Can not switch off from state: %d" % actual_state)
        #     return False

        while actual_state != States.ENGAGED_S.value:
            actual_state = self.__req.getParameter("root/Logic/state").get().value[0]
            time.sleep(0.1)

        return True

    def acknowledge(self, timeout_s=20.0):
        """Acknowledge the errors and warnings. If robot is in EStop state brings it to the Off state,
        if robot is in ForceDisengaged/ForceIdle state brings it to the Disengaged/Idle state.

            Returns:
                bool: True if operation is completed, False if failed
        """

        actual_state = self.__req.getParameter("root/Logic/state").get().value[0]
        self.__req.setParameter("root/Logic/stateCommand", StateEvents.ACKNOWLEDGE_ERROR.value).get()
        if actual_state == States.ESTOP_OFF_S.value or actual_state == States.RESET_ESTOP_T.value:
            return self.__waitForTheParameterValuet("root/Logic/state", States.OFF_S.value, timeout_s)
        elif actual_state == States.FORCEDISENGAGED_S.value or actual_state == States.RESET_FORCEDDISENGAGE_T.value:
            return self.__waitForTheParameterValuet("root/Logic/state", States.DISENGAGED_S.value, timeout_s)

        return True

    def __waitForTheParameterValuet(self, parameter_name, target_value, timeout_s):
        timer = 0
        actual_vale = None
        while timer <= timeout_s:
            actual_vale = self.__req.getParameter(parameter_name).get().value[0]
            if actual_vale == target_value:
                return True
            time.sleep(0.1)
            timer += 0.1
        return False

    def manualCartMode(self):
        """Switch robot to a manual Cartesian motion.

            Returns:
                bool: True if operation is completed, False if failed

        """

        actual_mode = self.__req.getParameter("root/Logic/mode").get().value[0]
        while actual_mode != Modes.MANUAL_CART_MODE_M.value:
            self.__req.setParameter("root/Logic/modeCommand", ModeCommands.GOTO_MANUAL_CART_MODE_E.value).get()
            time.sleep(0.1)
            actual_mode = self.__req.getParameter("root/Logic/mode").get().value[0]
        return True

    def manualJointMode(self):
        """Switch robot to a manual joint motion.

            Returns:
                bool: True if operation is completed, False if failed

        """

        actual_mode = self.__req.getParameter("root/Logic/mode").get().value[0]
        while actual_mode != Modes.MANUAL_JOINT_MODE_M.value:
            self.__req.setParameter("root/Logic/modeCommand", ModeCommands.GOTO_MANUAL_JOINT_MODE_E.value).get()
            time.sleep(0.1)
            actual_mode = self.__req.getParameter("root/Logic/mode").get().value[0]
        return True

    def semiAutoMode(self):
        """Switch robot to semi-auto mode. Semi-auto moves arm to the target
        when you user holds a button. Semi-auto is active for example during
        move to start of the program.

            Returns:
                bool: True if operation is completed, False if failed

        """

        actual_mode = self.__req.getParameter("root/Logic/mode").get().value[0]
        while actual_mode != Modes.SEMI_AUTO_M.value:
            self.__req.setParameter("root/Logic/modeCommand", ModeCommands.GOTO_SEMI_AUTO_E.value).get()
            time.sleep(0.1)
            actual_mode = self.__req.getParameter("root/Logic/mode").get().value[0]
        return True

    def toolTipOffset(self, tool_tip_offset):
        """Update tool-tip offset. Robot should be manual joint mode.

            Args:
                tool_tip_offset(list(double)): new tool tip offset in Cartesian frame of the last segment, rotation
                is defined in Euler ZYX angles.

            Returns:
                bool: True if operation is completed, False if failed

        """

        if self.manualJointMode():
            fade_time = self.__req.getParameter(
                f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/mechanism/tooltipFader/fadeTime").get()
            self.__req.setParameterList([
                {
                    "path": f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/mechanism/ttOffset",
                    "value": tool_tip_offset
                },
                {
                    "path": f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/mechanism/update",
                    "value": self.__kinematics_update_counter
                }]).get()
            self.__kinematics_update_counter = self.__kinematics_update_counter + 1
            time.sleep(fade_time.value[0])
            return True

        return False

    def moveToPoint(self, target_joint_coord_rad, v_max=0.5, a_max=1.0):
        """Move arm to a specified pose in joint space.

            Args:
                target_joint_coord_rad(list(double)): target pose in joint space, rad

            Returns:
                bool: True if operation is completed, False if failed

        """

        if self.semiAutoMode():
            self.__req.setParameterList([
                {
                    "path": f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/semiAutoMotionGenerator/maxAcc",
                    "value": a_max
                },
                {
                    "path": f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/semiAutoMotionGenerator/maxVel",
                    "value": v_max
                },
                {
                    "path": f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/semiAutoMotionGenerator/target",
                    "value": target_joint_coord_rad
                }]).get()

            while True:
                self.__req.setParameter(
                    f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/activateSemiAuto",
                    True).get()
                motion_state = \
                    self.__req.getParameter(
                        f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/semiAutoMotionGenerator/motionGenStateOut").get().value[
                        0]
                if motion_state != MotionGeneratorStates.RUNNING_S.value:
                    self.__req.setParameter(
                        f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/activateSemiAuto",
                        False).get()
                    return True
                time.sleep(0.1)

        return False

    def moveToStart(self, timeout_s):
        """Move arm to the start of the program.

            Args:
                timeout_s(double): timeout in seconds

            Returns:
                bool: True if operation is completed, False if failed

        """

        self.__req.setParameter(
            f"root/{self.__addSystem('MotionInterpreter', self.__system_id)}/interpreterCommand",
            InterpreterEvents.MOVE_TO_START.value).get()
        sleep_s = 0.1
        max_number_of_tries = timeout_s / sleep_s
        counter = 0
        time.sleep(1.0)
        while True:
            counter += 1
            self.__req.setParameter(
                f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/activateMoveToStart",
                1).get()
            interpreter_stat = self.getState()
            if interpreter_stat == InterpreterStates.PROGRAM_PAUSE_S.value:
                self.__req.setParameter(
                    f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/activateMoveToStart",
                    0).get()
                return True
            if counter > max_number_of_tries:
                self.__req.setParameter(
                    f"root/{self.__addSystem('ManipulatorControl', self.__system_id)}/activateMoveToStart",
                    0).get()
                return False
            time.sleep(sleep_s)

    def play(self, wait_time=1.0):
        """Plays the program.

            Args:
                wait_time(double): short delay after which actual state of the interpreter is requested

            Returns:
                InterpreterStates: actual state of the program interpreter

        """

        self.__req.setParameter(
            f"root/{self.__addSystem('MotionInterpreter', self.__system_id)}/interpreterCommand",
            InterpreterEvents.PLAY_PROGRAM_E.value).get()
        time.sleep(wait_time)
        return self.getState()

    def pause(self, wait_time=1.0):
        """Pause the program.

            Args:
                wait_time(double): short delay after which actual state of the interpreter is requested

            Returns:
                InterpreterStates: actual state of the program interpreter

        """

        self.__req.setParameter(
            f"root/{self.__addSystem('MotionInterpreter', self.__system_id)}/interpreterCommand",
            InterpreterEvents.PAUSE_PROGRAM_E.value).get()
        time.sleep(wait_time)
        return self.getState()

    def stop(self, wait_time=1.0):
        """Stop the program.

            Args:
                wait_time(double): short delay after which actual state of the interpreter is requested

            Returns:
                InterpreterStates: actual state of the program interpreter

        """

        self.__req.setParameter(
            f"root/{self.__addSystem('MotionInterpreter', self.__system_id)}/interpreterCommand",
            InterpreterEvents.STOP_PROGRAM_E.value).get()
        time.sleep(wait_time)
        return self.getState()

    def reset(self, wait_time=1.0):
        """Stop the program and clear the interpreter buffer.

            Args:
                wait_time(double): short delay after which actual state of the interpreter is requested

            Returns:
                InterpreterStates: actual state of the program interpreter

        """

        self.__req.setParameter(
            f"root/{self.__addSystem('MotionInterpreter', self.__system_id)}/interpreterCommand",
            InterpreterEvents.RESET_INTERPRETER_E.value).get()
        time.sleep(wait_time)
        return self.getState()

    def getState(self):
        """
            Returns:
                InterpreterStates: actual state of the interpreter

        """
        return self.__req.getParameter(
            f"root/{self.__addSystem('MotionInterpreter', self.__system_id)}/actualStateOut").get().value[0]
