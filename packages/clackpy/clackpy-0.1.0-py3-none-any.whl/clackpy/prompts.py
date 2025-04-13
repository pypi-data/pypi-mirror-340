#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
clack.prompts: A Python port attempt of parts of the @clack/prompts library.

This module provides basic building blocks for creating interactive
command-line prompts, inspired by the JavaScript library @clack/prompts.

It includes:
- Terminal symbol definitions (Unicode and fallback).
- ANSI color formatting.
- Utility functions for string manipulation and UI rendering.
- Prompt classes: TextPrompt, SelectPrompt, ConfirmPrompt, PasswordPrompt, MultiSelectPrompt.

Requires the 'readchar' library for cross-platform keypress handling:
  pip install readchar
"""

import sys
import re
import shutil
import os
import signal
from typing import Any, List, Optional, Callable, Union, TypeVar, Generic, Dict, Tuple

try:
    import readchar
except ImportError:
    print("Error: The 'readchar' library is required.")
    print("Please install it using: pip install readchar")
    sys.exit(1)

def is_unicode_supported() -> bool:
    return sys.stdout.encoding and sys.stdout.encoding.lower().startswith('utf')

UNICODE = is_unicode_supported()

def s(unicode_sym: str, fallback: str) -> str:
    return unicode_sym if UNICODE else fallback

S_STEP_ACTIVE = s('◆', '*')
S_STEP_CANCEL = s('■', 'x')
S_STEP_ERROR = s('▲', 'x')
S_STEP_SUBMIT = s('◇', 'o')
S_BAR_START = s('┌', 'T')
S_BAR = s('│', '|')
S_BAR_END = s('└', '—')
S_RADIO_ACTIVE = s('●', '>')
S_RADIO_INACTIVE = s('○', ' ')
S_CHECKBOX_ACTIVE = s('◻', '[•]')
S_CHECKBOX_SELECTED = s('◼', '[+]')
S_CHECKBOX_INACTIVE = s('◻', '[ ]')
S_PASSWORD_MASK = s('▪', '•')
S_BAR_H = s('─', '-')
S_CORNER_TOP_RIGHT = s('╮', '+')
S_CONNECT_LEFT = s('├', '+')
S_CORNER_BOTTOM_RIGHT = s('╯', '+')
S_INFO = s('●', '•')
S_SUCCESS = s('◆', '*')
S_WARN = s('▲', '!')
S_ERROR = s('■', 'x')

CANCEL_SYMBOL = object()

class Color:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    INVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    STRIKETHROUGH = "\033[9m"
    RESET = "\033[0m"

    @staticmethod
    def _colorize(text: str, color_code: str) -> str:
        return f"{color_code}{text}{Color.RESET}"

    @staticmethod
    def gray(text: str) -> str:
        return Color._colorize(text, Color.BRIGHT_BLACK)

    @staticmethod
    def cyan(text: str) -> str:
        return Color._colorize(text, Color.CYAN)

    @staticmethod
    def red(text: str) -> str:
        return Color._colorize(text, Color.RED)

    @staticmethod
    def green(text: str) -> str:
        return Color._colorize(text, Color.GREEN)

    @staticmethod
    def yellow(text: str) -> str:
        return Color._colorize(text, Color.YELLOW)

    @staticmethod
    def blue(text: str) -> str:
        return Color._colorize(text, Color.BLUE)

    @staticmethod
    def magenta(text: str) -> str:
        return Color._colorize(text, Color.MAGENTA)

    @staticmethod
    def dim(text: str) -> str:
        return Color._colorize(text, Color.DIM)

    @staticmethod
    def inverse(text: str) -> str:
        return Color._colorize(text, Color.INVERSE)

    @staticmethod
    def hidden(text: str) -> str:
        return Color._colorize(text, Color.HIDDEN)

    @staticmethod
    def strikethrough(text: str) -> str:
        return Color._colorize(text, Color.STRIKETHROUGH)

    @staticmethod
    def reset(text: str) -> str:
        return f"{text}{Color.RESET}"

def strip_ansi(text: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def symbol(state: str) -> str:
    if state == 'initial' or state == 'active':
        return Color.cyan(S_STEP_ACTIVE)
    elif state == 'cancel':
        return Color.red(S_STEP_CANCEL)
    elif state == 'error':
        return Color.yellow(S_STEP_ERROR)
    elif state == 'submit':
        return Color.green(S_STEP_SUBMIT)
    return ' '

def get_terminal_size() -> Tuple[int, int]:
    try:
        return shutil.get_terminal_size()
    except OSError:
        return (80, 24)

def limit_lines(text: str, max_lines: int) -> str:
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    return "\n".join(lines[:max_lines - 1]) + "\n" + Color.dim("...")

def limit_options(
    options: List[Any],
    cursor: int,
    max_items: Optional[int] = None,
    style: Callable[[Any, bool], str] = lambda x, _: str(x)
) -> List[str]:
    if max_items is None:
        try:
            max_items = max(get_terminal_size()[1] - 5, 3)
        except OSError:
            max_items = 7

    num_options = len(options)
    if num_options <= max_items:
        return [style(option, i == cursor) for i, option in enumerate(options)]

    window_size = max(1, max_items - 2)
    half_window = window_size // 2
    start = max(0, min(cursor - half_window, num_options - window_size))
    end = min(num_options, start + window_size)
    if end - start < window_size and num_options > window_size:
         start = max(0, end - window_size)
    visible_options = options[start:end]
    result = []
    show_top_dots = start > 0
    show_bottom_dots = end < num_options
    if show_top_dots:
        result.append(Color.dim("..."))
    for i, option in enumerate(visible_options):
        actual_index = start + i
        is_cursor_on = actual_index == cursor
        result.append(style(option, is_cursor_on))
    if show_bottom_dots:
        if len(result) < max_items:
            result.append(Color.dim("..."))
    return result[:max_items]

def is_cancel(value: Any) -> bool:
    return value is CANCEL_SYMBOL

CURSOR_HIDE = "\033[?25l"
CURSOR_SHOW = "\033[?25h"
ERASE_DOWN = "\033[J"
ERASE_LINE = "\033[2K"
CURSOR_UP_ONE = "\033[A"
CARRIAGE_RETURN = "\r"

V = TypeVar('V')

class BasePrompt(Generic[V]):
    def __init__(
        self,
        message: str,
        initial_value: Optional[V] = None,
        validate: Optional[Callable[[V], Optional[str]]] = None
    ):
        self.message = message
        self.value: V = initial_value
        self._validate = validate
        self.state: str = "initial"
        self.error: str = ""
        self._rendered_lines: int = 0

    def _render_prompt(self) -> str:
        raise NotImplementedError

    def _handle_key(self, key: str) -> bool:
        return False

    def _finalize(self):
        pass

    def _clear_render(self):
        if self._rendered_lines > 0:
            clear_sequence = (CURSOR_UP_ONE + ERASE_LINE) * self._rendered_lines
            sys.stdout.write(CARRIAGE_RETURN + clear_sequence)
            sys.stdout.flush()
            self._rendered_lines = 0

    def _render(self):
        self._clear_render()
        output = self._render_prompt()
        self._rendered_lines = output.count('\n') + 1
        sys.stdout.write(output + '\n')
        sys.stdout.flush()

    def prompt(self) -> Union[V, object]:
        original_sigint_handler = signal.getsignal(signal.SIGINT)

        def _handle_sigint(sig, frame):
            nonlocal self
            self.state = "cancel"
            signal.signal(signal.SIGINT, original_sigint_handler)

        try:
            sys.stdout.write(CURSOR_HIDE)
            self.state = "active"
            signal.signal(signal.SIGINT, _handle_sigint)
            self._render()
            while self.state in ["active", "error"]:
                key = readchar.readkey()
                if key == readchar.key.CTRL_C:
                    self.state = "cancel"
                    break
                elif key == readchar.key.ENTER:
                    if self._validate:
                        validation_result = self._validate(self.value)
                        if validation_result is not None:
                            self.state = "error"
                            self.error = validation_result
                        else:
                            self.state = "submit"
                    else:
                        self.state = "submit"
                    if self.state == "submit":
                        break
                handled_by_subclass = self._handle_key(key)
                if self.state == "error" and handled_by_subclass:
                    self.state = "active"
                    self.error = ""
                self._render()
            self._finalize()
            self._clear_render()
            final_output = self._render_prompt()
            sys.stdout.write(final_output)
            sys.stdout.flush()
            return CANCEL_SYMBOL if self.state == "cancel" else self.value
        finally:
            if self.state != 'active':
                 sys.stdout.write('\n')
            sys.stdout.write(CURSOR_SHOW)
            sys.stdout.flush()
            signal.signal(signal.SIGINT, original_sigint_handler)

class TextPrompt(BasePrompt[str]):
    def __init__(
        self,
        message: str,
        placeholder: str = '',
        default_value: str = '',
        initial_value: str = '',
        validate: Optional[Callable[[str], Optional[str]]] = None
    ):
        super().__init__(message, initial_value=initial_value or '', validate=validate)
        self.placeholder = placeholder
        self.default_value = default_value
        self._cursor_pos = len(self.value)

    def _handle_key(self, key: str) -> bool:
        handled = True
        if key == readchar.key.BACKSPACE or key == '\x7f':
            if self._cursor_pos > 0:
                self.value = self.value[:self._cursor_pos-1] + self.value[self._cursor_pos:]
                self._cursor_pos -= 1
        elif key == readchar.key.DELETE:
             if self._cursor_pos < len(self.value):
                self.value = self.value[:self._cursor_pos] + self.value[self._cursor_pos+1:]
        elif key == readchar.key.LEFT:
            if self._cursor_pos > 0:
                self._cursor_pos -= 1
        elif key == readchar.key.RIGHT:
            if self._cursor_pos < len(self.value):
                self._cursor_pos += 1
        elif key == readchar.key.HOME:
             self._cursor_pos = 0
        elif key == readchar.key.END:
             self._cursor_pos = len(self.value)
        elif not key.startswith('\x1b') and len(key) == 1 and not key < ' ':
            self.value = self.value[:self._cursor_pos] + key + self.value[self._cursor_pos:]
            self._cursor_pos += 1
        else:
            handled = False
        return handled

    def _get_value_with_cursor(self, mask: Optional[str] = None) -> str:
        val = self.value
        pos = self._cursor_pos
        display_val = (mask * len(val)) if mask else val
        if self.state != 'active':
            return display_val
        if pos >= len(val):
            return display_val + Color.inverse(' ')
        else:
            cursor_char = display_val[pos]
            return display_val[:pos] + Color.inverse(cursor_char) + display_val[pos+1:]

    def _render_prompt(self, mask: Optional[str] = None) -> str:
        prefix = f"{symbol(self.state)} {self.message}"
        lines = [f"{Color.gray(S_BAR)}"]
        if self.state == 'submit':
            submitted_value = self.value if self.value else Color.dim(self.default_value or 'N/A')
            display_submitted = (mask * len(submitted_value)) if mask else submitted_value
            lines.append(f"{prefix} {Color.dim('›')} {display_submitted}")
            lines.append(f"{Color.gray(S_BAR_END)}")
        elif self.state == 'cancel':
            cancelled_value = Color.strikethrough(Color.dim(self.value or self.placeholder or ' '))
            display_cancelled = (mask * len(strip_ansi(cancelled_value))) if mask else cancelled_value
            lines.append(f"{prefix} {Color.dim('›')} {display_cancelled}")
            lines.append(f"{Color.red(S_BAR_END)}  {Color.red('Operation cancelled.')}")
        elif self.state == 'error':
            lines.append(prefix)
            display_value = self._get_value_with_cursor(mask)
            lines.append(f"{Color.yellow(S_BAR)}  {display_value}")
            lines.append(f"{Color.yellow(S_BAR_END)}  {Color.yellow(self.error)}")
        else:
            lines.append(prefix)
            if not self.value and self.placeholder:
                placeholder_display = Color.inverse(self.placeholder[0] if self.placeholder else ' ') + \
                                      Color.dim(self.placeholder[1:])
                lines.append(f"{Color.cyan(S_BAR)}  {placeholder_display}")
            else:
                 lines.append(f"{Color.cyan(S_BAR)}  {self._get_value_with_cursor(mask)}")
            lines.append(f"{Color.cyan(S_BAR_END)}")
        return "\n".join(lines)

    def _finalize(self):
        if self.state == 'submit' and not self.value and self.default_value:
            self.value = self.default_value

class PasswordPrompt(TextPrompt):
    def __init__(
        self,
        message: str,
        mask: str = S_PASSWORD_MASK,
        validate: Optional[Callable[[str], Optional[str]]] = None
    ):
        super().__init__(message, initial_value='', validate=validate)
        self._mask = mask

    def _render_prompt(self) -> str:
        return super()._render_prompt(mask=self._mask)

class ConfirmPrompt(BasePrompt[bool]):
    def __init__(
        self,
        message: str,
        active: str = "Yes",
        inactive: str = "No",
        initial_value: bool = True
    ):
        super().__init__(message, initial_value=initial_value)
        self._active_text = active
        self._inactive_text = inactive

    def _handle_key(self, key: str) -> bool:
        key_lower = key.lower()
        handled = True
        if key_lower == 'y' or key == readchar.key.LEFT or key == readchar.key.UP:
            self.value = True
        elif key_lower == 'n' or key == readchar.key.RIGHT or key == readchar.key.DOWN:
            self.value = False
        elif key == readchar.key.SPACE:
            self.value = not self.value
        else:
            handled = False
        return handled

    def _render_prompt(self) -> str:
        prefix = f"{symbol(self.state)} {self.message}"
        lines = [f"{Color.gray(S_BAR)}"]
        yes_style = Color.inverse if self.value else Color.dim
        no_style = Color.inverse if not self.value else Color.dim
        if self.state == 'submit':
            submitted_value = self._active_text if self.value else self._inactive_text
            lines.append(f"{prefix} {Color.dim('›')} {Color.dim(submitted_value)}")
            lines.append(f"{Color.gray(S_BAR_END)}")
        elif self.state == 'cancel':
            cancelled_value = self._active_text if self.value else self._inactive_text
            lines.append(f"{prefix} {Color.dim('›')} {Color.strikethrough(Color.dim(cancelled_value))}")
            lines.append(f"{Color.red(S_BAR_END)}  {Color.red('Operation cancelled.')}")
        elif self.state == 'error':
            lines.append(prefix)
            lines.append(f"{Color.yellow(S_BAR)}  {yes_style(self._active_text)} / {no_style(self._inactive_text)}")
            lines.append(f"{Color.yellow(S_BAR_END)}  {Color.yellow(self.error)}")
        else:
            lines.append(prefix)
            lines.append(f"{Color.cyan(S_BAR)}  {yes_style(self._active_text)} / {no_style(self._inactive_text)}")
            lines.append(f"{Color.cyan(S_BAR_END)}")
        return "\n".join(lines)

OptionType = Union[str, Dict[str, Any]]
OptionValueType = TypeVar('OptionValueType')

class SelectPrompt(BasePrompt[OptionValueType]):
    def __init__(
        self,
        message: str,
        options: List[OptionType],
        initial_value: Optional[OptionValueType] = None,
        max_items: Optional[int] = None,
    ):
        self._options: List[Dict[str, Any]] = []
        initial_cursor = 0
        for i, opt in enumerate(options):
            if isinstance(opt, str):
                normalized_opt = {"value": opt, "label": opt}
            else:
                normalized_opt = opt.copy()
                if "value" not in normalized_opt:
                    normalized_opt["value"] = normalized_opt.get("label", str(i))
                if "label" not in normalized_opt:
                     normalized_opt["label"] = str(normalized_opt["value"])
            self._options.append(normalized_opt)
            if initial_value is not None and normalized_opt["value"] == initial_value:
                initial_cursor = i
        self._cursor_index = initial_cursor
        super().__init__(message, initial_value=self._options[self._cursor_index]["value"])
        self._max_items = max_items

    def _handle_key(self, key: str) -> bool:
        handled = True
        num_options = len(self._options)
        if key == readchar.key.UP or key == readchar.key.LEFT:
            self._cursor_index = (self._cursor_index - 1 + num_options) % num_options
            self.value = self._options[self._cursor_index]["value"]
        elif key == readchar.key.DOWN or key == readchar.key.RIGHT:
            self._cursor_index = (self._cursor_index + 1) % num_options
            self.value = self._options[self._cursor_index]["value"]
        else:
            handled = False
        return handled

    def _render_option(self, option: Dict[str, Any], is_cursor_on: bool) -> str:
        sym = S_RADIO_ACTIVE if is_cursor_on else S_RADIO_INACTIVE
        label = option.get("label", str(option["value"]))
        hint = option.get("hint")
        line_color = Color.cyan if is_cursor_on else Color.dim
        label_style = Color.reset if is_cursor_on else Color.dim
        line = f"{line_color(sym)} {label_style(label)}"
        if hint and is_cursor_on:
            line += f" {Color.dim(hint)}"
        return line

    def _render_prompt(self) -> str:
        prefix = f"{symbol(self.state)} {self.message}"
        lines = [f"{Color.gray(S_BAR)}"]
        if self.state == 'submit':
            submitted_label = next((opt.get("label", str(opt["value"])) for opt in self._options if opt["value"] == self.value), str(self.value))
            lines.append(f"{prefix} {Color.dim('›')} {Color.dim(submitted_label)}")
            lines.append(f"{Color.gray(S_BAR_END)}")
        elif self.state == 'cancel':
            cancelled_label = next((opt.get("label", str(opt["value"])) for opt in self._options if opt["value"] == self.value), str(self.value))
            lines.append(f"{prefix} {Color.dim('›')} {Color.strikethrough(Color.dim(cancelled_label))}")
            lines.append(f"{Color.red(S_BAR_END)}  {Color.red('Operation cancelled.')}")
        elif self.state == 'error':
             lines.append(prefix)
             lines.append(f"{Color.yellow(S_BAR)}  {Color.yellow('Error state not typical for select')}")
             lines.append(f"{Color.yellow(S_BAR_END)}  {Color.yellow(self.error)}")
        else:
            lines.append(prefix)
            rendered_options = limit_options(
                self._options,
                self._cursor_index,
                max_items=self._max_items,
                style=self._render_option
            )
            max_width = get_terminal_size()[0] - 6
            for option_line in rendered_options:
                 display_line = strip_ansi(option_line)
                 if len(display_line) > max_width:
                     ansi_indices = [m.start() for m in re.finditer(r'\x1B\[[0-?]*[ -/]*[@-~]', option_line)]
                     visible_chars_count = 0
                     truncate_at = len(option_line)
                     for i, char in enumerate(option_line):
                         is_ansi = any(i >= start and i < start + len(m.group(0))
                                       for start in ansi_indices
                                       for m in re.finditer(r'\x1B\[[0-?]*[ -/]*[@-~]', option_line) if m.start() == start)
                         if not is_ansi:
                             visible_chars_count += 1
                         if visible_chars_count > max_width - 3:
                             truncate_at = i
                             break
                     option_line = option_line[:truncate_at] + Color.dim("...") + Color.RESET
                 lines.append(f"{Color.cyan(S_BAR)}  {option_line}")
            lines.append(f"{Color.cyan(S_BAR_END)}")
        return "\n".join(lines)

class MultiSelectPrompt(BasePrompt[List[OptionValueType]]):
    def __init__(
        self,
        message: str,
        options: List[OptionType],
        initial_value: Optional[List[OptionValueType]] = None,
        required: bool = False,
        max_items: Optional[int] = None,
    ):
        self._options: List[Dict[str, Any]] = []
        for i, opt in enumerate(options):
            if isinstance(opt, str):
                normalized_opt = {"value": opt, "label": opt}
            else:
                normalized_opt = opt.copy()
                if "value" not in normalized_opt:
                    normalized_opt["value"] = normalized_opt.get("label", str(i))
                if "label" not in normalized_opt:
                     normalized_opt["label"] = str(normalized_opt["value"])
            self._options.append(normalized_opt)
        self._cursor_index = 0
        initial_selection = list(initial_value) if initial_value is not None else []

        def _validate_multiselect(value: List[OptionValueType]) -> Optional[str]:
            if required and not value:
                return "At least one option must be selected."
            return None

        super().__init__(message, initial_value=initial_selection, validate=_validate_multiselect)
        self._max_items = max_items

    def _toggle_selection(self):
        option_value = self._options[self._cursor_index]["value"]
        if option_value in self.value:
            self.value.remove(option_value)
        else:
            try:
                 original_index = [opt['value'] for opt in self._options].index(option_value)
                 insert_pos = 0
                 for val in self.value:
                     try:
                         val_original_index = [opt['value'] for opt in self._options].index(val)
                         if val_original_index < original_index:
                             insert_pos +=1
                         else:
                             break
                     except ValueError:
                         continue
                 self.value.insert(insert_pos, option_value)
            except ValueError:
                 self.value.append(option_value)

    def _handle_key(self, key: str) -> bool:
        handled = True
        num_options = len(self._options)
        if key == readchar.key.UP or key == readchar.key.LEFT:
            self._cursor_index = (self._cursor_index - 1 + num_options) % num_options
        elif key == readchar.key.DOWN or key == readchar.key.RIGHT:
            self._cursor_index = (self._cursor_index + 1) % num_options
        elif key == readchar.key.SPACE:
            self._toggle_selection()
        elif key.lower() == 'a':
            if len(self.value) == len(self._options):
                self.value = []
            else:
                self.value = [opt['value'] for opt in self._options]
        else:
            handled = False
        return handled

    def _render_option(self, option: Dict[str, Any], is_cursor_on: bool) -> str:
        option_value = option["value"]
        is_selected = option_value in self.value
        if is_cursor_on:
            sym = S_CHECKBOX_SELECTED if is_selected else S_CHECKBOX_ACTIVE
            line_color = Color.cyan
            label_style = Color.reset
        else:
            sym = S_CHECKBOX_SELECTED if is_selected else S_CHECKBOX_INACTIVE
            line_color = Color.dim
            label_style = Color.dim
        label = option.get("label", str(option_value))
        hint = option.get("hint")
        line = f"{line_color(sym)} {label_style(label)}"
        if hint and is_cursor_on:
            line += f" {Color.dim(hint)}"
        return line

    def _render_prompt(self) -> str:
        prefix = f"{symbol(self.state)} {self.message}"
        lines = [f"{Color.gray(S_BAR)}"]
        if self.state == 'submit':
            submitted_values_set = set(self.value)
            submitted_labels = [
                opt.get("label", str(opt["value"]))
                for opt in self._options if opt["value"] in submitted_values_set
            ]
            display_value = Color.dim(", ".join(submitted_labels) or "None")
            lines.append(f"{prefix} {Color.dim('›')} {display_value}")
            lines.append(f"{Color.gray(S_BAR_END)}")
        elif self.state == 'cancel':
            cancelled_values_set = set(self.value)
            cancelled_labels = [
                opt.get("label", str(opt["value"]))
                for opt in self._options if opt["value"] in cancelled_values_set
            ]
            display_value = Color.strikethrough(Color.dim(", ".join(cancelled_labels) or "None"))
            lines.append(f"{prefix} {Color.dim('›')} {display_value}")
            lines.append(f"{Color.red(S_BAR_END)}  {Color.red('Operation cancelled.')}")
        elif self.state == 'error':
             lines.append(prefix)
             rendered_options = limit_options(
                 self._options,
                 self._cursor_index,
                 max_items=self._max_items,
                 style=self._render_option
             )
             for option_line in rendered_options:
                  lines.append(f"{Color.yellow(S_BAR)}  {option_line}")
             lines.append(f"{Color.yellow(S_BAR_END)}  {Color.yellow(self.error)}")
        else:
            lines.append(prefix)
            rendered_options = limit_options(
                self._options,
                self._cursor_index,
                max_items=self._max_items,
                style=self._render_option
            )
            max_width = get_terminal_size()[0] - 6
            for option_line in rendered_options:
                 display_line = strip_ansi(option_line)
                 if len(display_line) > max_width:
                     ansi_indices = [m.start() for m in re.finditer(r'\x1B\[[0-?]*[ -/]*[@-~]', option_line)]
                     visible_chars_count = 0
                     truncate_at = len(option_line)
                     for i, char in enumerate(option_line):
                         is_ansi = any(i >= start and i < start + len(m.group(0)) for start in ansi_indices for m in re.finditer(r'\x1B\[[0-?]*[ -/]*[@-~]', option_line) if m.start() == start)
                         if not is_ansi:
                             visible_chars_count += 1
                         if visible_chars_count > max_width - 3:
                             truncate_at = i
                             break
                     option_line = option_line[:truncate_at] + Color.dim("...") + Color.RESET
                 lines.append(f"{Color.cyan(S_BAR)}  {option_line}")
            lines.append(f"{Color.cyan(S_BAR_END)}")
        return "\n".join(lines)

def text(
    message: str,
    placeholder: str = '',
    default_value: str = '',
    initial_value: str = '',
    validate: Optional[Callable[[str], Optional[str]]] = None
) -> Union[str, object]:
    prompt = TextPrompt(
        message=message,
        placeholder=placeholder,
        default_value=default_value,
        initial_value=initial_value,
        validate=validate
    )
    return prompt.prompt()

def password(
    message: str,
    mask: str = S_PASSWORD_MASK,
    validate: Optional[Callable[[str], Optional[str]]] = None
) -> Union[str, object]:
    prompt = PasswordPrompt(
        message=message,
        mask=mask,
        validate=validate
    )
    return prompt.prompt()

def confirm(
    message: str,
    active: str = "Yes",
    inactive: str = "No",
    initial_value: bool = True
) -> Union[bool, object]:
    prompt = ConfirmPrompt(
        message=message,
        active=active,
        inactive=inactive,
        initial_value=initial_value
    )
    return prompt.prompt()

def select(
    message: str,
    options: List[OptionType],
    initial_value: Optional[OptionValueType] = None,
    max_items: Optional[int] = None,
) -> Union[OptionValueType, object]:
    prompt = SelectPrompt(
        message=message,
        options=options,
        initial_value=initial_value,
        max_items=max_items
    )
    return prompt.prompt()

def multiselect(
    message: str,
    options: List[OptionType],
    initial_value: Optional[List[OptionValueType]] = None,
    required: bool = False,
    max_items: Optional[int] = None,
) -> Union[List[OptionValueType], object]:
    prompt = MultiSelectPrompt(
        message=message,
        options=options,
        initial_value=initial_value,
        required=required,
        max_items=max_items
    )
    return prompt.prompt()

if __name__ == "__main__":
    print(f"{Color.blue('--- Clack.py Demo ---')}\n")
    OVERWRITE_SEQ = CURSOR_UP_ONE + CARRIAGE_RETURN + Color.gray(S_BAR) + '\n'
    name = text(
        message="What's your name?",
        placeholder="e.g., Jane Doe",
        validate=lambda v: "Name cannot be empty." if not v else None
    )
    sys.stdout.write(OVERWRITE_SEQ)
    sys.stdout.flush()
    if is_cancel(name):
        print("\nOperation cancelled.")
        sys.exit(0)
    secret = password(
        message="Enter a secret password:",
        validate=lambda v: "Password must be at least 4 characters." if len(v) < 4 else None
    )
    sys.stdout.write(OVERWRITE_SEQ)
    sys.stdout.flush()
    if is_cancel(secret):
        print("\nOperation cancelled.")
        sys.exit(0)
    should_continue = confirm(
        message="Do you want to proceed?",
        initial_value=True
    )
    sys.stdout.write(OVERWRITE_SEQ)
    sys.stdout.flush()
    if is_cancel(should_continue):
        print("\nOperation cancelled.")
        sys.exit(0)
    if not should_continue:
        sys.stdout.write(CURSOR_UP_ONE + ERASE_LINE)
        print(Color.yellow("Exiting as requested."))
        sys.exit(0)
    project_options = [
        {"value": "web", "label": "Website", "hint": "Frontend project"},
        {"value": "api", "label": "API Service", "hint": "Backend project"},
        "cli",
        {"value": "other", "label": "Other"},
    ]
    project_type = select(
        message="Select project type:",
        options=project_options,
        initial_value="web"
    )
    sys.stdout.write(OVERWRITE_SEQ)
    sys.stdout.flush()
    if is_cancel(project_type):
        print("\nOperation cancelled.")
        sys.exit(0)
    features = multiselect(
        message="Select features to include:",
        options=[
            {"value": "auth", "label": "Authentication"},
            {"value": "db", "label": "Database Setup"},
            {"value": "docker", "label": "Docker Support", "hint": "Recommended"},
            {"value": "lint", "label": "Linter & Formatter"},
            {"value": "tests", "label": "Unit Tests"},
        ],
        initial_value=["lint", "tests"],
        required=True
    )
    if is_cancel(features):
        print("\nOperation cancelled.")
        sys.exit(0)
    print(f"\n{Color.blue('--- Demo Complete ---')}")
