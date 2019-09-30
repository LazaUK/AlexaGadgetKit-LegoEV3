# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# 
# You may not use this file except in compliance with the terms and conditions 
# set forth in the accompanying LICENSE.TXT file.
#
# THESE MATERIALS ARE PROVIDED ON AN "AS IS" BASIS. AMAZON SPECIFICALLY DISCLAIMS, WITH 
# RESPECT TO THESE MATERIALS, ALL WARRANTIES, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

# Updated by Laziz & Farid Turakulovs
# in October 2019
# for submission to Hackster.io's Alexa Lego Voice Challenge

import time
import logging
import json
import random
import threading
from enum import Enum

from agt import AlexaGadget

from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.motor import OUTPUT_A, SpeedPercent, MediumMotor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor

# Set the logging level to INFO to see messages from AlexaGadget
logging.basicConfig(level=logging.INFO)

class Command(Enum):
    """
    The list of preset commands and their invocation variation.
    These variations correspond to the skill slot values.
    """
    QUIZ = ['quiz', 'quiz mode', 'game', 'game mode']
    ROTATION = ['next move', 'next round']

class EventName(Enum):
    """
    The list of custom event name sent from this gadget
    """
    QUIZ = "Quiz"
    TOUCH = "Touch"
    SPEECH = "Speech"


class MindstormsGadget(AlexaGadget):
    """
    A Mindstorms gadget that can perform bi-directional interaction with an Alexa skill.
    """

    def __init__(self):
        """
        Performs Alexa Gadget initialization routines and ev3dev resource allocation.
        """
        super().__init__()

        # Robot state
        self.quiz_mode = False

        # Activate sensors and actuators
        self.fan = MediumMotor(OUTPUT_A)
        self.sound = Sound()
        self.leds = Leds()
        self.ts = TouchSensor()
        self.cl = ColorSensor()
        self.cl.mode = 'COL-COLOR'


        # Start threads
        threading.Thread(target=self._touch_thread, daemon=True).start()

    def on_connected(self, device_addr):
        """
        Gadget connected to the paired Echo device.
        :param device_addr: the address of the device we connected to
        """
        self.leds.set_color("LEFT", "GREEN")
        self.leds.set_color("RIGHT", "GREEN")
        print("{} connected to Echo device".format(self.friendly_name))

    def on_disconnected(self, device_addr):
        """
        Gadget disconnected from the paired Echo device.
        :param device_addr: the address of the device we disconnected from
        """
        self.leds.set_color("LEFT", "BLACK")
        self.leds.set_color("RIGHT", "BLACK")
        print("{} disconnected from Echo device".format(self.friendly_name))

    def on_custom_mindstorms_gadget_control(self, directive):
        """
        Handles the Custom.Mindstorms.Gadget control directive.
        :param directive: the custom directive with the matching namespace and name
        """
        try:
            payload = json.loads(directive.payload.decode("utf-8"))
            print("Control payload: {}".format(payload))
            control_type = payload["type"]

            if control_type == "command":
                # Expected params: [command]
                self._activate(payload["command"])

        except KeyError:
            print("Missing expected parameters: {}".format(directive))

    def _activate(self, command, speed=50):
        """
        Handles preset commands.
        :param command: the preset command
        :param speed: the speed if applicable
        """
        print("Activate command: ({}, {})".format(command, speed))

        if command in Command.QUIZ.value:
            self.quiz_mode = True
            self._send_event(EventName.SPEECH, {'speechOut': "Show me your coloured token"})

            # Indicate readiness through LEDs
            self.leds.set_color("LEFT", "YELLOW", 1)
            self.leds.set_color("RIGHT", "YELLOW", 1)
            time.sleep(0.3)

        if command in Command.ROTATION.value:
            print("Next round")
            self.fan.on_for_rotations(SpeedPercent(100), 3)
            self._send_event(EventName.QUIZ, {'rotation': 1})
            self.quiz_mode = False
            print("Sent answer back, round ended")
            self.leds.set_color("LEFT", "GREEN", 1)
            self.leds.set_color("RIGHT", "GREEN", 1)


    def _send_event(self, name: EventName, payload):
        """
        Sends a custom event to trigger a sentry action.
        :param name: the name of the custom event
        :param payload: the sentry JSON payload
        """
        self.send_custom_event('Custom.Mindstorms.Gadget', name.value, payload)

    def _touch_thread(self):
        """
        Monitor and wait till the touch sensor is pressed
        """
        while True:
            while self.quiz_mode:
                if self.ts.is_pressed:
                    print("Touch sensor pressed. Sending event to skill")
                    self.leds.set_color("LEFT", "RED", 1)
                    self.leds.set_color("RIGHT", "RED", 1)
                    self._send_event(EventName.TOUCH, {'answer': self.cl.value()})
                    # self.quiz_mode = False
                time.sleep(0.2)
            time.sleep(1)

if __name__ == '__main__':
    # Startup sequence
    gadget = MindstormsGadget()
    gadget.sound.play_song((('C4', 'e'), ('D4', 'e'), ('E5', 'q')))
    gadget.leds.set_color("LEFT", "GREEN")
    gadget.leds.set_color("RIGHT", "GREEN")

    # Gadget main entry point
    gadget.main()

    # Shutdown sequence
    gadget.sound.play_song((('E5', 'e'), ('C4', 'e')))
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")