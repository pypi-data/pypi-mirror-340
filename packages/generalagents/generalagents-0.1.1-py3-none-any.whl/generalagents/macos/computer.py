import subprocess
import tempfile
import time
from fractions import Fraction

import pyautogui
from PIL import Image
from pytweening import easeInOutQuad

from generalagents.action import (
    Action,
    ActionDoubleClick,
    ActionDrag,
    ActionKeyPress,
    ActionLeftClick,
    ActionMouseMove,
    ActionRightClick,
    ActionScroll,
    ActionStop,
    ActionTripleClick,
    ActionType,
    ActionWait,
    Coordinate,
)

pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.001  # We are waiting manually in the code
MOUSE_SETTINGS = {"duration": 0.101, "tween": easeInOutQuad}  # duration <= 0.1 is treated as 0 by pyautogui


class Computer:
    def __init__(self, pause_after_action: float = 0.1, pause_for_wait: float = 0.1):
        """A Computer interface for macOS control.

        Args:
            pause_after_action: Time in seconds to wait after executing an action.
            pause_for_wait: Time in seconds to wait when executing a wait action.
        """
        self.pause_after_action = pause_after_action
        self.pause_for_wait = pause_for_wait

        w, h = pyautogui.size()

        # On high-DPI displays (e.g. Retina), pyautogui.size() may return scaled-down dimensions.
        # To standardize, we calculate a scale factor based on the maximum dimension and resize accordingly.
        self.scale_factor = Fraction(max(w, h), 1200)
        self.size = (round(w / self.scale_factor), round(h / self.scale_factor))

    def observe(self) -> Image.Image:
        """Observe current state of the computer"""
        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            subprocess.run(["screencapture", "-C", "-x", "-m", f.name], check=True)
            return Image.open(f.name).resize(self.size)

    def execute(self, action: Action) -> Image.Image:
        """Execute a control action and observe the resulting state of the computer.

        Args:
            action: The action to execute (e.g., mouse click, keyboard input).

        Returns:
            A screenshot of the screen after the action has been performed,
            allowing observation of the effect of the action.
        """
        self._execute_action(action)
        time.sleep(self.pause_after_action)
        return self.observe()

    def _scaled(self, coord: Coordinate) -> tuple[int, int]:
        return round(coord.x * self.scale_factor), round(coord.y * self.scale_factor)

    def _execute_action(self, action: Action) -> None:
        match action:
            case ActionKeyPress(kind="key_press", keys=keys) if keys:
                for key in keys:
                    pyautogui.keyDown(key)
                for key in reversed(keys):
                    pyautogui.keyUp(key)

            case ActionType(kind="type", text=text) if text:
                pyautogui.write(text)

            case ActionLeftClick(kind="left_click", coordinate=coord):
                pyautogui.click(*self._scaled(coord), button="left", **MOUSE_SETTINGS)

            case ActionRightClick(kind="right_click", coordinate=coord):
                pyautogui.click(*self._scaled(coord), button="right", **MOUSE_SETTINGS)

            case ActionDoubleClick(kind="double_click", coordinate=coord):
                pyautogui.doubleClick(*self._scaled(coord), **MOUSE_SETTINGS)

            case ActionTripleClick(kind="triple_click", coordinate=coord):
                pyautogui.tripleClick(*self._scaled(coord), **MOUSE_SETTINGS)

            case ActionMouseMove(kind="mouse_move", coordinate=coord):
                pyautogui.moveTo(*self._scaled(coord), **MOUSE_SETTINGS)

            case ActionDrag(kind="drag", drag_start=start, drag_end=end):
                pyautogui.moveTo(*self._scaled(start))
                pyautogui.dragTo(*self._scaled(end), duration=0.5)

            case ActionScroll(kind="scroll", scroll_delta=delta, coordinate=coord):
                pyautogui.moveTo(*self._scaled(coord))
                pyautogui.scroll(float(delta * self.scale_factor))

            case ActionWait(kind="wait"):
                pyautogui.sleep(self.pause_for_wait)

            case ActionStop(kind="stop"):
                pass
