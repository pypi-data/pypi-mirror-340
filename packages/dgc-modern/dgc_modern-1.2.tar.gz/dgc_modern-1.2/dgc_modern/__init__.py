import sys
import threading
import time

class Modern:
    """
    ライブラリのエントリポイントクラス。
    複数の Task インスタンスを管理し、一括で再描画を行います。
    """
    _tasks = []
    _lock = threading.Lock()

    @classmethod
    def append(cls, task: "Task"):
        with cls._lock:
            task.index = len(cls._tasks)
            cls._tasks.append(task)
            task._initial_render()

    @classmethod
    def remove(cls, task: "Task"):
        with cls._lock:
            cls._tasks.remove(task)
            # index を再割り当て
            for i, t in enumerate(cls._tasks):
                t.index = i

    @classmethod
    def render_all(cls):
        """
        全タスクを上から順に再描画。
        """
        with cls._lock:
            for task in cls._tasks:
                task._render()

class Task:
    """
    1つのプログレスバーを表すクラス。
    Modern に登録すると、自動的に同時表示が可能になります。
    """
    def __init__(self, total: int, process_name: str,
                 process_color: str = "blue", iswaiting: bool = False):
        self.total = total
        self.current = 0
        self.process_name = process_name.strip()
        self.process_color = process_color
        self.iswaiting = iswaiting

        self.index: int = -1
        self.log_lines = 0
        self.wait_step = 0
        self.message = "No Message"

        # Modern に登録すると同時に1行分を確保
        Modern.append(self)

    def _initial_render(self):
        print()  # 各タスクごとに1行分を予約

    def set_message(self, message: str):
        self.message = message

    def waitmode(self, status: bool = True):
        self.iswaiting = status

    def start(self):
        self._render()

    def update(self, amount: int = 1):
        if not self.iswaiting:
            self.current = min(self.current + amount, self.total)
        self._render()

    def finish(self):
        self.current = self.total
        self.iswaiting = False
        self._render(final=True)
        Modern.remove(self)

    def _render(self, final: bool = False):
        progress = self.current / self.total if self.total else 0
        bar = self._build_bar(progress)
        percentage = f"{progress:.2%}"
        if final:
            status = f"[DONE]"
        elif self.iswaiting:
            status = f"[WAIT]"
        else:
            status = f"[{self.current}/{self.total}]"
        line = (
            f"{self.process_name} - "
            f"({self._color(self.process_color)}{bar}{self._color('reset')}) "
            f"{percentage} {status} | {self.message}"
        )

        total_move_up = self.log_lines + (len(Modern._tasks) - self.index)
        sys.stdout.write(f"\033[{total_move_up}A")
        sys.stdout.write("\033[K")
        print(line)
        sys.stdout.write(f"\033[{total_move_up}B")
        sys.stdout.flush()

    def _build_bar(self, progress: float) -> str:
        length = 20
        if self.iswaiting:
            busy_pos = self.wait_step % (length)
            self.wait_step += 1
            before = "=" * busy_pos
            after = "-" * (length - busy_pos - 1)
            return f"{self._color(self.process_color)}{before}{self._color(self.process_color)}>{self._color('black')}{after}"
        else:
            filled = int(progress * length)
            empty = length - filled
            return (
                f"{self._color(self.process_color)}{'-' * filled}"
                f"{self._color('black')}{'-' * empty}"
            )

    def _color(self, name: str) -> str:
        codes = {
            "black": 30, "red": 31, "green": 32, "yellow": 33,
            "blue": 34, "magenta": 35, "cyan": 36, "white": 37,
            "reset": 0
        }
        return f"\033[{codes.get(name, 0)}m"
