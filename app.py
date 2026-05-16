import customtkinter as ctk
import random
import time
from collections import deque


# =========================
# BFS LOGIC
# =========================

def string_to_state(s):
    return [
        [int(s[0]), int(s[1]), int(s[2])],
        [int(s[3]), int(s[4]), int(s[5])],
        [int(s[6]), int(s[7]), int(s[8])]
    ]


def state_to_string(state):
    return "".join(str(num) for row in state for num in row)


def clone_state(state):
    return [row[:] for row in state]


def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None


def get_neighbors(state):
    x, y = find_zero(state)

    directions = [
        ("UP", -1, 0),
        ("DOWN", 1, 0),
        ("LEFT", 0, -1),
        ("RIGHT", 0, 1)
    ]

    neighbors = []

    for action, dx, dy in directions:
        new_x = x + dx
        new_y = y + dy

        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = clone_state(state)

            new_state[x][y], new_state[new_x][new_y] = (
                new_state[new_x][new_y],
                new_state[x][y]
            )

            neighbors.append((new_state, action))

    return neighbors


def is_valid_input(s):
    if len(s) != 9:
        return False

    return "".join(sorted(s)) == "012345678"


def inversion_count(s):
    arr = [int(x) for x in s if x != "0"]
    count = 0

    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                count += 1

    return count


def is_solvable(start, goal):
    return inversion_count(start) % 2 == inversion_count(goal) % 2


def bfs(start, goal):
    start_key = state_to_string(start)
    goal_key = state_to_string(goal)

    frontier = deque()
    frontier.append({
        "state": start,
        "path": [start],
        "actions": []
    })

    reached = set()
    reached.add(start_key)

    nodes_expanded = 0

    while frontier:
        node = frontier.popleft()
        nodes_expanded += 1

        current_state = node["state"]
        current_key = state_to_string(current_state)

        if current_key == goal_key:
            return {
                "path": node["path"],
                "actions": node["actions"],
                "nodes_expanded": nodes_expanded,
                "depth": len(node["actions"]),
                "cost": len(node["actions"])
            }

        for next_state, action in get_neighbors(current_state):
            next_key = state_to_string(next_state)

            if next_key not in reached:
                reached.add(next_key)

                frontier.append({
                    "state": next_state,
                    "path": node["path"] + [next_state],
                    "actions": node["actions"] + [action]
                })

    return None


# =========================
# UI APP
# =========================

class EightPuzzleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("8-Puzzle BFS Solver")
        self.geometry("1250x760")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.solution_path = []
        self.solution_actions = []
        self.current_index = 0
        self.animation_running = False

        self.tile_buttons = []

        self.build_ui()
        self.draw_board(string_to_state("531620478"))

    # =========================
    # BUILD UI
    # =========================

    def build_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color="#0b1020")
        self.main_container.pack(fill="both", expand=True)

        # Top menu
        self.topbar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.topbar.pack(fill="x", padx=25, pady=(15, 0))

        self.menu_button = ctk.CTkButton(
            self.topbar,
            text="⋮",
            width=45,
            height=42,
            font=("Arial", 24, "bold"),
            fg_color="#111827",
            hover_color="#1f2937",
            command=self.open_menu
        )
        self.menu_button.pack(side="right")

        # Title
        self.title_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.title_frame.pack(pady=(20, 30))

        self.badge = ctk.CTkLabel(
            self.title_frame,
            text="BFS Algorithm",
            text_color="#38bdf8",
            fg_color="#0f2740",
            corner_radius=18,
            padx=14,
            pady=6,
            font=("Arial", 14, "bold")
        )
        self.badge.pack(pady=(0, 12))

        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="8-Puzzle Solver",
            font=("Arial", 46, "bold"),
            text_color="white"
        )
        self.title_label.pack()

        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Giải bài toán 8-Puzzle bằng thuật toán BFS và mô phỏng từng bước di chuyển.",
            font=("Arial", 16),
            text_color="#9ca3af"
        )
        self.subtitle_label.pack(pady=(8, 0))

        # Main layout
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack()

        self.left_panel = ctk.CTkFrame(
            self.content_frame,
            width=330,
            height=430,
            corner_radius=24,
            fg_color="#111827"
        )
        self.left_panel.grid(row=0, column=0, padx=25, sticky="n")
        self.left_panel.grid_propagate(False)

        self.center_panel = ctk.CTkFrame(
            self.content_frame,
            width=430,
            height=500,
            fg_color="transparent"
        )
        self.center_panel.grid(row=0, column=1, padx=25, sticky="n")

        self.right_panel = ctk.CTkFrame(
            self.content_frame,
            width=370,
            height=430,
            corner_radius=24,
            fg_color="#111827"
        )
        self.right_panel.grid(row=0, column=2, padx=25, sticky="n")
        self.right_panel.grid_propagate(False)

        self.build_left_panel()
        self.build_board()
        self.build_right_panel()

    def build_left_panel(self):
        self.shuffle_button = ctk.CTkButton(
            self.left_panel,
            text="Shuffle Puzzle",
            height=42,
            corner_radius=14,
            fg_color="#0f172a",
            hover_color="#1e293b",
            command=self.shuffle_puzzle
        )
        self.shuffle_button.pack(fill="x", padx=24, pady=(24, 20))

        self.start_label = ctk.CTkLabel(
            self.left_panel,
            text='Enter initial state, from top-left to right-bottom,\n9 characters, e.g. "012345678"',
            justify="left",
            text_color="white",
            font=("Arial", 13, "bold")
        )
        self.start_label.pack(anchor="w", padx=24)

        self.start_entry = ctk.CTkEntry(
            self.left_panel,
            height=42,
            corner_radius=12,
            fg_color="#2b2c35",
            border_width=0,
            text_color="white"
        )
        self.start_entry.pack(fill="x", padx=24, pady=(8, 18))
        self.start_entry.insert(0, "531620478")

        self.goal_label = ctk.CTkLabel(
            self.left_panel,
            text="Enter goal state",
            text_color="white",
            font=("Arial", 13, "bold")
        )
        self.goal_label.pack(anchor="w", padx=24)

        self.goal_entry = ctk.CTkEntry(
            self.left_panel,
            height=42,
            corner_radius=12,
            fg_color="#2b2c35",
            border_width=0,
            text_color="white"
        )
        self.goal_entry.pack(fill="x", padx=24, pady=(8, 18))
        self.goal_entry.insert(0, "012345678")

        self.algorithm_label = ctk.CTkLabel(
            self.left_panel,
            text="Choose Algorithm",
            text_color="white",
            font=("Arial", 13, "bold")
        )
        self.algorithm_label.pack(anchor="w", padx=24)

        self.algorithm_box = ctk.CTkOptionMenu(
            self.left_panel,
            values=["BFS"],
            height=42,
            corner_radius=12,
            fg_color="#2b2c35",
            button_color="#2b2c35",
            button_hover_color="#374151"
        )
        self.algorithm_box.pack(fill="x", padx=24, pady=(8, 18))

        self.solve_button = ctk.CTkButton(
            self.left_panel,
            text="Solve Puzzle",
            height=44,
            corner_radius=14,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.solve_puzzle
        )
        self.solve_button.pack(fill="x", padx=24)

        self.error_label = ctk.CTkLabel(
            self.left_panel,
            text="",
            text_color="#f87171",
            wraplength=280,
            font=("Arial", 13, "bold")
        )
        self.error_label.pack(padx=24, pady=(12, 0))

        self.note_label = ctk.CTkLabel(
            self.left_panel,
            text="Quy ước: số 0 là ô trống.\nBFS dùng hàng đợi FIFO để tìm lời giải ngắn nhất.",
            text_color="#9ca3af",
            justify="left",
            wraplength=280,
            font=("Arial", 12)
        )
        self.note_label.pack(anchor="w", padx=24, pady=(8, 0))

    def build_board(self):
        self.board_frame = ctk.CTkFrame(
            self.center_panel,
            width=420,
            height=420,
            corner_radius=26,
            fg_color="#111827"
        )
        self.board_frame.pack()
        self.board_frame.pack_propagate(False)

        self.board_grid = ctk.CTkFrame(self.board_frame, fg_color="transparent")
        self.board_grid.place(relx=0.5, rely=0.5, anchor="center")

        for i in range(3):
            row = []
            for j in range(3):
                tile = ctk.CTkLabel(
                    self.board_grid,
                    text="",
                    width=118,
                    height=118,
                    corner_radius=18,
                    fg_color="#2d9bf0",
                    text_color="white",
                    font=("Arial", 42, "bold")
                )
                tile.grid(row=i, column=j, padx=6, pady=6)
                row.append(tile)
            self.tile_buttons.append(row)

        self.action_label = ctk.CTkLabel(
            self.center_panel,
            text="Action: Waiting",
            text_color="#38bdf8",
            font=("Arial", 18, "bold")
        )
        self.action_label.pack(pady=(18, 12))

        self.control_frame = ctk.CTkFrame(self.center_panel, fg_color="transparent")
        self.control_frame.pack()

        self.prev_button = ctk.CTkButton(
            self.control_frame,
            text="◄ Prev",
            width=100,
            height=40,
            fg_color="#0f172a",
            hover_color="#1e293b",
            command=self.prev_step
        )
        self.prev_button.grid(row=0, column=0, padx=8)

        self.stop_button = ctk.CTkButton(
            self.control_frame,
            text="Stop",
            width=100,
            height=40,
            fg_color="#0f172a",
            hover_color="#1e293b",
            command=self.stop_animation
        )
        self.stop_button.grid(row=0, column=1, padx=8)

        self.next_button = ctk.CTkButton(
            self.control_frame,
            text="Next ►",
            width=100,
            height=40,
            fg_color="#0f172a",
            hover_color="#1e293b",
            command=self.next_step
        )
        self.next_button.grid(row=0, column=2, padx=8)

    def build_right_panel(self):
        self.result_title = ctk.CTkLabel(
            self.right_panel,
            text="Results",
            text_color="#38bdf8",
            font=("Arial", 30, "bold")
        )
        self.result_title.pack(anchor="w", padx=24, pady=(24, 18))

        self.status_label = ctk.CTkLabel(
            self.right_panel,
            text="Pending user input...",
            text_color="#f59e0b",
            font=("Arial", 15, "bold")
        )
        self.status_label.pack(anchor="w", padx=24, pady=(0, 18))

        self.runtime_label = self.create_result_line("Runtime Duration:")
        self.nodes_label = self.create_result_line("Nodes Expanded:")
        self.depth_label = self.create_result_line("Search Depth:")
        self.cost_label = self.create_result_line("Path Cost:")

        self.path_title = ctk.CTkLabel(
            self.right_panel,
            text="Path to Goal:",
            text_color="white",
            font=("Arial", 15, "bold")
        )
        self.path_title.pack(anchor="w", padx=24, pady=(14, 8))

        self.path_text = ctk.CTkTextbox(
            self.right_panel,
            width=320,
            height=140,
            corner_radius=14,
            fg_color="#0f172a",
            text_color="#d1d5db",
            font=("Consolas", 12)
        )
        self.path_text.pack(padx=24)
        self.path_text.insert("1.0", "Chưa có dữ liệu")
        self.path_text.configure(state="disabled")

    def create_result_line(self, title):
        label = ctk.CTkLabel(
            self.right_panel,
            text=f"{title} ",
            text_color="white",
            font=("Arial", 15, "bold")
        )
        label.pack(anchor="w", padx=24, pady=9)
        return label

    # =========================
    # MENU
    # =========================

    def open_menu(self):
        menu = ctk.CTkToplevel(self)
        menu.title("Menu")
        menu.geometry("360x280")
        menu.resizable(False, False)
        menu.configure(fg_color="#111827")

        title = ctk.CTkLabel(
            menu,
            text="Theme",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        title.pack(pady=(18, 10))

        theme_frame = ctk.CTkFrame(menu, fg_color="transparent")
        theme_frame.pack(pady=10)

        ctk.CTkButton(
            theme_frame,
            text="System",
            width=95,
            height=70,
            fg_color="#374151",
            command=lambda: ctk.set_appearance_mode("system")
        ).grid(row=0, column=0, padx=6)

        ctk.CTkButton(
            theme_frame,
            text="Light",
            width=95,
            height=70,
            fg_color="#374151",
            command=lambda: ctk.set_appearance_mode("light")
        ).grid(row=0, column=1, padx=6)

        ctk.CTkButton(
            theme_frame,
            text="Dark",
            width=95,
            height=70,
            fg_color="#374151",
            command=lambda: ctk.set_appearance_mode("dark")
        ).grid(row=0, column=2, padx=6)

        ctk.CTkButton(
            menu,
            text="Print",
            height=38,
            fg_color="#2b2c35",
            command=lambda: self.show_message("Print chỉ hỗ trợ tốt trên bản web.")
        ).pack(fill="x", padx=25, pady=(18, 8))

        ctk.CTkButton(
            menu,
            text="Record screen",
            height=38,
            fg_color="#2b2c35",
            command=lambda: self.show_message("Python desktop không ghi màn hình sẵn. Có thể dùng OBS hoặc thư viện pyautogui.")
        ).pack(fill="x", padx=25)

        ctk.CTkLabel(
            menu,
            text="Made with Python CustomTkinter",
            text_color="#9ca3af",
            font=("Arial", 14, "bold")
        ).pack(pady=20)

    def show_message(self, message):
        popup = ctk.CTkToplevel(self)
        popup.title("Thông báo")
        popup.geometry("380x150")
        popup.resizable(False, False)

        label = ctk.CTkLabel(
            popup,
            text=message,
            wraplength=320,
            font=("Arial", 14),
            text_color="white"
        )
        label.pack(pady=30)

        ctk.CTkButton(
            popup,
            text="OK",
            command=popup.destroy
        ).pack()

    # =========================
    # BOARD FUNCTIONS
    # =========================

    def draw_board(self, state):
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                tile = self.tile_buttons[i][j]

                if value == 0:
                    tile.configure(text="", fg_color="#111827")
                else:
                    tile.configure(text=str(value), fg_color="#2d9bf0")

        self.update_action_text()

    def update_action_text(self):
        if not self.solution_path:
            self.action_label.configure(text="Action: Waiting")
        elif self.current_index == 0:
            self.action_label.configure(text="Action: Start")
        else:
            action = self.solution_actions[self.current_index - 1]
            self.action_label.configure(text=f"Action: Move {action}")

    def update_results(self, result, runtime):
        self.status_label.configure(
            text="Solving animation...",
            text_color="#f59e0b"
        )

        self.runtime_label.configure(
            text=f"Runtime Duration: {runtime:.3f} ms"
        )

        self.nodes_label.configure(
            text=f"Nodes Expanded: {result['nodes_expanded']}"
        )

        self.depth_label.configure(
            text=f"Search Depth: {result['depth']}"
        )

        self.cost_label.configure(
            text=f"Path Cost: {result['cost']}"
        )

        path_content = ""

        for i, state in enumerate(result["path"]):
            path_content += f"Step {i}"
            if i > 0:
                path_content += f" - Move {result['actions'][i - 1]}"
            path_content += "\n"
            path_content += state_to_string(state) + "\n\n"

        self.path_text.configure(state="normal")
        self.path_text.delete("1.0", "end")
        self.path_text.insert("1.0", path_content)
        self.path_text.configure(state="disabled")

    # =========================
    # BUTTON ACTIONS
    # =========================

    def solve_puzzle(self):
        self.stop_animation()

        start_str = self.start_entry.get().strip()
        goal_str = self.goal_entry.get().strip()

        self.error_label.configure(text="")

        if not is_valid_input(start_str) or not is_valid_input(goal_str):
            self.error_label.configure(
                text="Input phải gồm đúng 9 số từ 0 đến 8, không trùng nhau."
            )
            return

        if not is_solvable(start_str, goal_str):
            self.error_label.configure(
                text="Trạng thái này không thể giải được."
            )
            return

        start = string_to_state(start_str)
        goal = string_to_state(goal_str)

        start_time = time.perf_counter()
        result = bfs(start, goal)
        end_time = time.perf_counter()

        if result is None:
            self.error_label.configure(text="Không tìm thấy lời giải.")
            return

        runtime = (end_time - start_time) * 1000

        self.solution_path = result["path"]
        self.solution_actions = result["actions"]
        self.current_index = 0

        self.update_results(result, runtime)
        self.start_animation()

    def start_animation(self):
        self.animation_running = True
        self.current_index = 0
        self.draw_board(self.solution_path[self.current_index])
        self.after(700, self.animate_next)

    def animate_next(self):
        if not self.animation_running:
            return

        if self.current_index < len(self.solution_path) - 1:
            self.current_index += 1
            self.draw_board(self.solution_path[self.current_index])
            self.after(700, self.animate_next)
        else:
            self.animation_running = False
            self.status_label.configure(
                text="Solved successfully!",
                text_color="#22c55e"
            )

    def stop_animation(self):
        self.animation_running = False

    def next_step(self):
        self.stop_animation()

        if not self.solution_path:
            return

        if self.current_index < len(self.solution_path) - 1:
            self.current_index += 1
            self.draw_board(self.solution_path[self.current_index])

        if self.current_index == len(self.solution_path) - 1:
            self.status_label.configure(
                text="Solved successfully!",
                text_color="#22c55e"
            )

    def prev_step(self):
        self.stop_animation()

        if not self.solution_path:
            return

        if self.current_index > 0:
            self.current_index -= 1
            self.draw_board(self.solution_path[self.current_index])

        self.status_label.configure(
            text="Manual step mode",
            text_color="#38bdf8"
        )

    def shuffle_puzzle(self):
        self.stop_animation()

        goal_str = self.goal_entry.get().strip()

        if not is_valid_input(goal_str):
            self.error_label.configure(text="Goal state không hợp lệ.")
            return

        arr = list("012345678")

        while True:
            random.shuffle(arr)
            start_str = "".join(arr)

            if is_solvable(start_str, goal_str):
                break

        self.start_entry.delete(0, "end")
        self.start_entry.insert(0, start_str)

        self.solution_path = []
        self.solution_actions = []
        self.current_index = 0

        self.draw_board(string_to_state(start_str))

        self.status_label.configure(
            text="Pending user input...",
            text_color="#f59e0b"
        )

        self.runtime_label.configure(text="Runtime Duration:")
        self.nodes_label.configure(text="Nodes Expanded:")
        self.depth_label.configure(text="Search Depth:")
        self.cost_label.configure(text="Path Cost:")
        self.error_label.configure(text="")

        self.path_text.configure(state="normal")
        self.path_text.delete("1.0", "end")
        self.path_text.insert("1.0", "Chưa có dữ liệu")
        self.path_text.configure(state="disabled")


if __name__ == "__main__":
    app = EightPuzzleApp()
    app.mainloop()