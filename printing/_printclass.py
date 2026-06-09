from math import ceil
from shutil import get_terminal_size
from queue import Queue
from time import sleep, perf_counter

from ._deco import using_ansi, replace_ansi, get_line_len, clear_lines, remove_escape_sequences, full_clear, p_reset, \
    _COLOR_LOOKUP_TABLE


class PrintClass:
    def __init__(self, q: Queue, terminal_reset_allowed: bool):
        self.constant_refresh = False
        self.queue: Queue = q
        self.max_line_chars:int = 0
        self.max_columns:int = 0
        self.current_output = ""
        self.target_fps: int = 60
        self.target_fps_time: float = 1.0 / self.target_fps
        self.output: str = ""
        self.centered = False
        self.show_fps = False
        # self.fps_counter = FpsCounter(self.target_fps)
        self._is_running = True
        self._is_paused = False
        self._old_frame_time: float = perf_counter()
        self._terminal_reset_allowed: bool = terminal_reset_allowed
        self._last_lines: list[str] = []
        self._current_lines: list[str] = []

    def run(self):
        # old_frame_time = perf_counter()
        # new_frame_time = perf_counter() + 1
        should_refresh_output = False
        while self._is_running:
            if self._is_paused:
                if self.check_queue():
                    self.get_new_output()
                self.sleep()
                if not self._is_paused:
                    should_refresh_output = True
                continue

            if self.check_queue():
                while self.check_queue():
                    self.get_new_output()
                if self._is_paused or not self._is_running:
                    continue
                should_refresh_output = True

            if self.check_terminal_update():
                should_refresh_output = True

            if self.constant_refresh:
                should_refresh_output = True

            if should_refresh_output:
                should_refresh_output = False
                self.refresh_output()

            # self.fps_counter.add_frame_time(new_frame_time, old_frame_time)
            # if self.show_fps:
            #     self.fps_counter.display_fps_info(self.current_output, self.output_lines)

            # new_frame_time = perf_counter()
            self.sleep()
            # old_frame_time = perf_counter()

    def change_fps(self, new_fps_limit):
        # self.fps_counter.update_fps_goal(new_fps_limit)
        self.target_fps: int = new_fps_limit
        self.target_fps_time: float = 1.0 / new_fps_limit

    def refresh_output(self):
        self.current_output = self.output[:]

        if not using_ansi():
            self.current_output = replace_ansi(self.current_output)
        self._print_output()
        # print(self.current_output, end="", flush=True)

    def check_terminal_update(self) -> bool:
        new_chars, new_columns = get_terminal_size()
        new_chars -= 1
        new_columns -= 1
        if new_chars != self.max_line_chars or new_columns != self.max_columns:
            self.max_line_chars = new_chars
            self.max_columns = new_columns
            return True
        return False

    def _print_output(self):
        self.check_terminal_update()
        self._format_lines()
        self._clear_output()
        out = self._current_lines
        if self.centered:
            offset = max(0, int((self.max_line_chars - get_line_len()) / 2))
            spacing = " " * offset
            out = []
            for line in self._current_lines:
                out.append(spacing + line)
        self._last_lines = out
        print("\n".join(out), end="")

    def _format_lines(self):
        index = -1
        self._current_lines = self.current_output.split("\n")
        max_length = self.max_line_chars

        line_len = get_line_len()
        if self.centered and max_length > line_len:
            max_length = max(5, line_len)
        while index + 1 < len(self._current_lines):
            index += 1
            line = self._current_lines[index]
            if len(line) <= max_length:
                continue
            no_seq_line = remove_escape_sequences(line)
            if len(no_seq_line) <= max_length:
                continue
            self._format_long_line(self._current_lines, no_seq_line, index, max_length)

    def __get_index_ascii_safe(self, line:str, index:int) -> int:
        total_length = len(line)
        no_ascii = remove_escape_sequences(line)
        if total_length == len(no_ascii) or line[:index] == no_ascii[:index]:
            return index
        esc_begin = line.rfind("\033", 0, index)
        if esc_begin == -1:
            return index # This should never be the case. It would require a different start for the escape sequences.
        return esc_begin

    def _get_trailing_escape_sequence(self, line:str) -> str:
        """
        Checks if there is and returns the last escape sequence if the last sequence is not a reset.
        """
        index = line.rfind("\033")
        if index == -1:
            return ""
        last_part:str = line[index:]
        if last_part.startswith(p_reset):
            return ""
        for code in _COLOR_LOOKUP_TABLE.values():
            if last_part.startswith(code):
                return code
        return ""

    def _format_long_line(self, data: list[str], no_seq_line:str ,index: int, max_length:int) -> None:
        line = data[index]
        space_count = line.count(" ")
        space_index = -1
        space_number = -1
        for i in range(1, space_count+1):
            new_index = no_seq_line.find(" ", space_index + 1)
            if new_index <= max_length:
                space_index = new_index
                space_number = i
                continue
            break
        if space_index == -1:
            if len(no_seq_line) == len(line):
                data[index] = line[:max_length]
                data.insert(index + 1, line[max_length+1:])
                return
            index = self.__get_index_ascii_safe(line, index)
            new_line = line[:max_length]
            trailing_esc_sequence = self._get_trailing_escape_sequence(new_line)
            if len(trailing_esc_sequence) > 0:
                data[index] = new_line + p_reset
                data.insert(index + 1, trailing_esc_sequence + line[max_length:])
                return
            data[index] = new_line
            data.insert(index + 1, line[max_length:])
            return
        space_index = -1
        for i in range(space_number):
            space_index = line.find(" ", space_index + 1)

        new_line = line[:space_index]
        trailing_esc_sequence = self._get_trailing_escape_sequence(new_line)
        if len(trailing_esc_sequence) > 0:
            data[index] = new_line + p_reset
            data.insert(index + 1, trailing_esc_sequence + line[space_index:])
            return
        
        data[index] = new_line
        data.insert(index + 1, line[space_index+1:])

    def _clear_output(self) -> None:
        if len(self._last_lines) <= 0:
            return
        new_lines = 0
        for line in self._last_lines:
            new_lines += max(ceil((len(remove_escape_sequences(line))) / (self.max_line_chars + 1)), 1)
        new_lines = min(new_lines, self.max_columns)
        if new_lines >= self.max_columns and self._terminal_reset_allowed:
            full_clear()
            return
        clear_lines(new_lines)

    def get_new_output(self) -> None:
        n_out: list[str | bool | tuple] = self.queue.get()
        if type(n_out[0]) == tuple:
            call = n_out[0][0]
            if call == "show fps":
                self.show_fps = n_out[1]
            elif call == "constant refresh":
                self.constant_refresh = n_out[1]
            elif call == "change fps":
                self.change_fps(n_out[1])
            elif call == "exit":
                self._is_running = False
            elif call == "center text":
                self.centered = n_out[1]
            elif call == "pause":
                self._is_paused = n_out[1]
            return
        self.output = n_out[0]
        return

    def check_queue(self):
        return self.queue.qsize() != 0

    def sleep(self) -> None:
        """
        Sleeps to try to reach the target amount of updates per second.
        """
        new_frame_time = perf_counter()
        target_time = self.target_fps_time - (new_frame_time - self._old_frame_time)

        if target_time <= 0:
            self._old_frame_time = new_frame_time
            return

        # using the default instead of my small tinkering, because it didn't work correctly on other systems
        sleep(target_time)

        self._old_frame_time = perf_counter()
        return
        # t_start = time.perf_counter()
        # t_stop = t_start + seconds
        # while time.perf_counter() < t_stop:
        #    time.sleep(0.0000001)
        #    pass


class FpsCounter:
    def __init__(self, fps_goal):
        self.fps_goal = fps_goal
        self.sleep_time = 0.0
        self.theoretic_fps = "---"
        self.actual_fps = "---"
        self.average_accuracy = fps_goal * 2
        self.average_fps_list = [1 for _ in range(self.average_accuracy)]
        self.average_fps_index = 0
        self.average_output_calc_time_list = [1 for _ in range(self.average_accuracy)]
        self.average_output_calc_time_index = 0
        self.self_calculation_start = perf_counter()
        self.calculation_time = perf_counter()
        self.self_calculation_time = 0.0
        self.should_sleep_time = 0.0

    def update_fps_goal(self, new_fps_goal):
        self.fps_goal = new_fps_goal
        self.average_accuracy = min(1000, int(new_fps_goal * 2))
        self.average_fps_list = [1 for _ in range(self.average_accuracy)]
        self.average_output_calc_time_list = [1 for _ in range(self.average_accuracy)]
        self.average_fps_index = 0
        self.average_output_calc_time_index = 0

    def add_frame_time(self, old_end_time, new_start_time):
        self.should_sleep_time = (1 / self.fps_goal) - self.self_calculation_time - self.calculation_time
        self.self_calculation_time = old_end_time - self.self_calculation_start
        self.self_calculation_start = perf_counter()
        self.calculation_time = perf_counter() - new_start_time
        self.sleep_time = new_start_time - old_end_time
        self.average_output_calc_time_list[self.average_output_calc_time_index] = self.calculation_time
        self.average_output_calc_time_index = (self.average_output_calc_time_index + 1) % self.average_accuracy

        if self.calculation_time != 0:
            self.theoretic_fps = str(round(1 / self.calculation_time, 6))
        else:
            self.theoretic_fps = "---"

        if self.calculation_time + self.sleep_time != 0:
            average_fps = 1 / (self.calculation_time + self.sleep_time + self.self_calculation_time)
            self.average_fps_list[self.average_fps_index] = average_fps
            self.average_fps_index = (self.average_fps_index + 1) % self.average_accuracy
            self.actual_fps = str(round(average_fps, 6))
        else:
            self.actual_fps = "---"

    def display_fps_info(self, output: str, line_amount: int):
        clear_lines(line_amount + 6, 0)
        print(output +
              f"\n\nOutput calculation time   : {self.calculation_time:.6f} (theoretic fps: {self.theoretic_fps})"
              f"\nAverage output calc time   : {sum(self.average_output_calc_time_list) / self.average_accuracy:.6f}"
              f"\nSleep time                 : {self.sleep_time:.6f} (actual fps: {self.actual_fps})"
              f"\nShould have slept for      : {self.should_sleep_time:.6f}"
              f"\nAverage fps                : {sum(self.average_fps_list) / len(self.average_fps_list):.6f}"
              f"\nFps calculation time needed: {self.self_calculation_time:.6f}")
