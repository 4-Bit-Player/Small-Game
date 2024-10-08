import shutil
import queue
import sys
import time
from decoration import deco

class PrintClass:
    def __init__(self, q: queue.Queue):
        self.queue: queue.Queue = q
        self.max_line_chars, self.max_columns = shutil.get_terminal_size()
        self.current_output = ""
        self.target_fps: int = 60
        self.target_fps_time: float = 1.0/self.target_fps
        self.output: str = ""
        self.output_lines = 50
        self.centered = False
        self.show_fps = False
        self.fps_counter = FpsCounter(self.target_fps)


    def start(self):
        old_frame_time = time.perf_counter()
        new_frame_time = time.perf_counter() + 1
        while True:
            if self.check_queue():
                self.get_new_output()
                self.refresh_output()

            if self.check_terminal_update():
                deco.full_clear()
                #deco.clear_screen(self.output.count("\n")+1000, 100)
                self.refresh_output()

            self.fps_counter.add_frame_time(new_frame_time, old_frame_time)
            if self.show_fps:
                self.fps_counter.display_fps_info(self.current_output, self.output_lines)


            new_frame_time = time.perf_counter()
            time.sleep(max(0.0, self.target_fps_time - (new_frame_time - old_frame_time)))
            old_frame_time = time.perf_counter()



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


        deco.clear_screen(self.output_lines + 10)
        self.output_lines = new_output.count("\n") + 1
        self.current_output = new_output[:-1]
        print(self.current_output, end="")


    def check_terminal_update(self) -> bool:
        new_lines, new_columns = shutil.get_terminal_size()
        if new_lines != self.max_line_chars or new_columns != self.max_columns:
            self.max_line_chars = new_lines
            self.max_columns = new_columns
            return True
        return False


    def get_new_output(self):
        n_out:[str, bool] = self.queue.get()
        if type(n_out[0]) != tuple:
            if n_out[0] == "toggle fps":
                self.show_fps = not self.show_fps
            return
        #self.header = n_out[1]["header"] if "header" in n_out[1] else ""
        #self.hud = n_out[1]["hud"] if "hud" in n_out[1] else False
        self.centered = n_out[1]
        self.output = n_out[0][0] + "\n"


    def check_queue(self):
        if self.queue.qsize() == 0:
            return False
        return True





class FpsCounter:
    def __init__(self, fps_goal):
        self.last_actual_calculation_time = 0.0
        self.calculation_time = time.perf_counter()
        self.sleep_time = 0.0
        self.theoretic_fps = "---"
        self.actual_fps = "---"
        self.average_accuracy = fps_goal*2
        self.average_fps_list = [1 for _ in range(self.average_accuracy)]
        self.average_fps_index = 0
        self.self_calculation_start = time.perf_counter()
        self.calculation_time = time.perf_counter()
        self.self_calculation_time = 0.0

    def add_frame_time(self, old_end_time, new_start_time):
        self.self_calculation_time = old_end_time - self.self_calculation_start
        self.self_calculation_start = time.perf_counter()
        self.calculation_time = time.perf_counter() - new_start_time
        self.sleep_time = new_start_time - old_end_time

        if self.calculation_time != 0:

            self.last_actual_calculation_time = self.calculation_time
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
        deco.clear_screen(line_amount + 5, 0)
        #os.system('cls')
        print(output +
              f"\n\nOutput calculation time: {self.calculation_time: .6f} (theoretic fps: {self.theoretic_fps})"
              f"\nSleep time: {self.sleep_time: .6f} (actual fps: {self.actual_fps})"
              f"\nAverage fps: {round(sum(self.average_fps_list)/len(self.average_fps_list),6)}"
              f"\nFps calculation time needed: {round(self.self_calculation_time, 6)}")
        sys.stdout.flush()
































