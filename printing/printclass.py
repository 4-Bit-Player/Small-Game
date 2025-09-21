import shutil
import queue
import time
from decoration import deco


class PrintClass:
    def __init__(self, q: queue.Queue, test=False):
        self.constant_refresh = False
        self.queue: queue.Queue = q
        self.max_line_chars, self.max_columns = shutil.get_terminal_size()
        self.current_output = ""
        self.target_fps: int = 60
        self.target_fps_time: float = 1.0/self.target_fps
        self.output: str = ""
        self.output_lines = 50
        self.centered = False
        self.show_fps = test
        self.fps_counter = FpsCounter(self.target_fps)


    def run(self):
        old_frame_time = time.perf_counter()
        new_frame_time = time.perf_counter() + 1
        while True:
            if self.check_queue():
                self.get_new_output()
                self.refresh_output()

            if self.check_terminal_update():
                deco.full_clear()
                self.refresh_output()

            if self.constant_refresh:
                self.refresh_output()
            self.fps_counter.add_frame_time(new_frame_time, old_frame_time)
            if self.show_fps:
                self.fps_counter.display_fps_info(self.current_output, self.output_lines)


            new_frame_time = time.perf_counter()
            self.sleep(self.target_fps_time - (new_frame_time - old_frame_time))
            old_frame_time = time.perf_counter()

    def change_fps(self, new_fps_limit):
        self.fps_counter.update_fps_goal(new_fps_limit)
        self.target_fps: int = new_fps_limit
        self.target_fps_time: float = 1.0 / new_fps_limit

    def refresh_output(self):
        new_output = ""
        new_newlines = self.output.count("\n")
        start = 0
        if self.centered:
            new_output += "\n" * max(0, int((self.max_columns - max(new_newlines, 35))/2))
            for i in range(new_newlines):
                newline_index = self.output.find("\n", start)
                new_line = self.output[start:newline_index+1]
                new_output += " " * int((self.max_line_chars - deco.line_len)/2) + new_line
                start = newline_index+1
        else:
            new_output = self.output

        if self.output_lines <= self.max_columns:
            deco.clear_screen(self.output_lines + 10)
        else:
            deco.full_clear()
        self.output_lines = new_output.count("\n") + 1
        self.current_output = new_output[:-1]
        print(self.current_output, end="", flush=True)


    def check_terminal_update(self) -> bool:
        new_lines, new_columns = shutil.get_terminal_size()
        if new_lines != self.max_line_chars or new_columns != self.max_columns:
            self.max_line_chars = new_lines
            self.max_columns = new_columns
            return True
        return False


    def get_new_output(self):
        n_out:list[tuple[str], bool] = self.queue.get()
        if type(n_out[0]) == tuple:
            call = n_out[0][0]
            if call == "show fps":
                self.show_fps = n_out[1]
            elif call == "constant refresh":
                self.constant_refresh = n_out[1]
            elif call == "change fps":
                self.change_fps(n_out[1])
            return
        #self.header = n_out[1]["header"] if "header" in n_out[1] else ""
        #self.hud = n_out[1]["hud"] if "hud" in n_out[1] else False
        self.centered = n_out[1]
        self.output = n_out[0] + "\n"


    def check_queue(self):
        return self.queue.qsize() != 0


    @staticmethod
    def sleep(seconds):
        if seconds <= 0:
            return
        # using the default instead of my small tinkering, because it didn't work correctly on other systems
        time.sleep(seconds)
        return
        t_start = time.perf_counter()
        t_stop = t_start + seconds
        while time.perf_counter() < t_stop:
            time.sleep(0.0000001)
            pass





class FpsCounter:
    def __init__(self, fps_goal):
        self.fps_goal = fps_goal
        self.sleep_time = 0.0
        self.theoretic_fps = "---"
        self.actual_fps = "---"
        self.average_accuracy = fps_goal*2
        self.average_fps_list = [1 for _ in range(self.average_accuracy)]
        self.average_fps_index = 0
        self.average_output_calc_time_list = [1 for _ in range(self.average_accuracy)]
        self.average_output_calc_time_index = 0
        self.self_calculation_start = time.perf_counter()
        self.calculation_time = time.perf_counter()
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
        self.should_sleep_time = (1/self.fps_goal) - self.self_calculation_time - self.calculation_time
        self.self_calculation_time = old_end_time - self.self_calculation_start
        self.self_calculation_start = time.perf_counter()
        self.calculation_time = time.perf_counter() - new_start_time
        self.sleep_time = new_start_time - old_end_time
        self.average_output_calc_time_list[self.average_output_calc_time_index] = self.calculation_time
        self.average_output_calc_time_index = (self.average_output_calc_time_index + 1) % self.average_accuracy

        if self.calculation_time != 0:
            self.theoretic_fps = str(round(1/self.calculation_time, 6))
        else:
            self.theoretic_fps = "---"

        if self.calculation_time + self.sleep_time != 0:
            average_fps =  1 / (self.calculation_time + self.sleep_time + self.self_calculation_time)
            self.average_fps_list[self.average_fps_index] = average_fps
            self.average_fps_index = (self.average_fps_index + 1) % self.average_accuracy
            self.actual_fps = str(round(average_fps, 6))
        else:
            self.actual_fps = "---"



    def display_fps_info(self, output:str, line_amount:int):
        deco.clear_screen(line_amount + 6, 0)
        #os.system('cls')
        print(output +
              f"\n\nOutput calculation time: {self.calculation_time:.6f} (theoretic fps: {self.theoretic_fps})"
              f"\nAverage output calculation time: {sum(self.average_output_calc_time_list)/self.average_accuracy:.6f}"
              f"\nSleep time:            {self.sleep_time:.6f} (actual fps: {self.actual_fps})"
              f"\nShould have slept for: {self.should_sleep_time:.6f}"
              f"\nAverage fps: {sum(self.average_fps_list)/len(self.average_fps_list):.6f}"
              f"\nFps calculation time needed: {self.self_calculation_time:.6f}")
        #sys.stdout.flush()
































