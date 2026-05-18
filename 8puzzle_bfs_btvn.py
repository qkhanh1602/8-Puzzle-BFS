import customtkinter as ctk
import random
import time
import threading
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


def format_state(state):
    """Hiển thị ma trận 3x3 dạng chữ để đưa vào phần giải từng bước."""
    return "\n".join(" ".join(str(x) if x != 0 else "_" for x in row) for row in state)


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

def generate_by_random_walk(goal_str, steps=14):
    """
    Tạo puzzle bằng cách đi ngẫu nhiên từ goal.
    Cách này giúp puzzle luôn giải được và không quá khó,
    tránh BFS bị treo do trạng thái ngẫu nhiên quá sâu.
    """
    state = string_to_state(goal_str)
    last_action = None

    opposite = {
        "UP": "DOWN",
        "DOWN": "UP",
        "LEFT": "RIGHT",
        "RIGHT": "LEFT"
    }

    for _ in range(steps):
        neighbors = get_neighbors(state)

        # Tránh vừa đi xong lại quay ngược ngay lập tức
        if last_action is not None:
            neighbors = [
                item for item in neighbors
                if item[1] != opposite.get(last_action)
            ] or neighbors

        state, last_action = random.choice(neighbors)

    return state_to_string(state)


def preview_queue(queue_items, limit=8):
    """
    Trả về danh sách trạng thái trong frontier dạng chuỗi.
    Chỉ hiển thị vài phần tử đầu để UI không quá dài.
    """
    items = []
    for node in list(queue_items)[:limit]:
        items.append(state_to_string(node["state"]))

    if len(queue_items) > limit:
        items.append(f"... +{len(queue_items) - limit} trạng thái")

    return items


def preview_reached(reached_set, limit=8):
    items = list(reached_set)[:limit]

    if len(reached_set) > limit:
        items.append(f"... +{len(reached_set) - limit} trạng thái")

    return items


def bfs(start, goal, mode="early"):
    """
    Có 2 cách mô phỏng BFS:

    mode="early":
        Cách 1 - kiểm tra child trước khi đưa vào frontier.
        Child mới sinh nếu chưa có trong reached thì thêm vào reached và frontier ngay.

    mode="late":
        Cách 2 - đưa child vào frontier trước.
        Khi lấy node ra khỏi frontier mới kiểm tra node đó đã nằm trong reached chưa.
    """
    if mode == "late":
        return bfs_late_check(start, goal)

    return bfs_early_check(start, goal)


def bfs_early_check(start, goal):
    """
    BFS Cách 1:
    Sinh node con -> kiểm tra reached -> nếu chưa có thì đưa vào frontier và reached.
    """
    start_key = state_to_string(start)
    goal_key = state_to_string(goal)

    frontier = deque()
    frontier.append({
        "state": start,
        "path": [start],
        "actions": [],
        "parent_action": "START"
    })

    reached = set()
    reached.add(start_key)

    nodes_expanded = 0
    trace = []

    while frontier:
        node = frontier.popleft()
        nodes_expanded += 1

        current_state = node["state"]
        current_key = state_to_string(current_state)

        trace_item = {
            "iteration": nodes_expanded,
            "node": current_state,
            "node_key": current_key,
            "action": node["parent_action"],
            "mode": "Cách 1: kiểm tra trước khi thêm vào Frontier",
            "frontier_before_expand": preview_queue(frontier),
            "frontier_size_before": len(frontier),
            "reached_before_expand": preview_reached(reached),
            "reached_size_before": len(reached),
            "children": [],
            "frontier_after_expand": [],
            "frontier_size_after": 0,
            "reached_size_after": 0,
            "is_goal": current_key == goal_key,
            "is_skip": False
        }

        if current_key == goal_key:
            trace_item["frontier_after_expand"] = preview_queue(frontier)
            trace_item["frontier_size_after"] = len(frontier)
            trace_item["reached_size_after"] = len(reached)
            trace.append(trace_item)

            return {
                "path": node["path"],
                "actions": node["actions"],
                "nodes_expanded": nodes_expanded,
                "depth": len(node["actions"]),
                "cost": len(node["actions"]),
                "trace": trace
            }

        for next_state, action in get_neighbors(current_state):
            next_key = state_to_string(next_state)

            child_info = {
                "action": action,
                "state_key": next_key,
                "state": next_state,
                "status": ""
            }

            if next_key not in reached:
                reached.add(next_key)

                frontier.append({
                    "state": next_state,
                    "path": node["path"] + [next_state],
                    "actions": node["actions"] + [action],
                    "parent_action": action
                })

                child_info["status"] = "ADD vào frontier và reached"
            else:
                child_info["status"] = "SKIP vì đã có trong reached"

            trace_item["children"].append(child_info)

        trace_item["frontier_after_expand"] = preview_queue(frontier)
        trace_item["frontier_size_after"] = len(frontier)
        trace_item["reached_size_after"] = len(reached)
        trace.append(trace_item)

    return None


def bfs_late_check(start, goal):
    """
    BFS Cách 2:
    Sinh node con -> đưa vào frontier trước.
    Khi lấy node ra khỏi frontier mới kiểm tra reached.
    """
    goal_key = state_to_string(goal)

    frontier = deque()
    frontier.append({
        "state": start,
        "path": [start],
        "actions": [],
        "parent_action": "START"
    })

    reached = set()
    nodes_expanded = 0
    trace = []
    iteration = 0

    while frontier:
        node = frontier.popleft()
        iteration += 1

        current_state = node["state"]
        current_key = state_to_string(current_state)

        already_reached = current_key in reached

        trace_item = {
            "iteration": iteration,
            "node": current_state,
            "node_key": current_key,
            "action": node["parent_action"],
            "mode": "Cách 2: lấy khỏi Frontier rồi mới kiểm tra Reached",
            "frontier_before_expand": preview_queue(frontier),
            "frontier_size_before": len(frontier),
            "reached_before_expand": preview_reached(reached),
            "reached_size_before": len(reached),
            "children": [],
            "frontier_after_expand": [],
            "frontier_size_after": 0,
            "reached_size_after": 0,
            "is_goal": False,
            "is_skip": already_reached
        }

        if already_reached:
            trace_item["children"].append({
                "action": "SKIP",
                "state_key": current_key,
                "state": current_state,
                "status": "BỎ QUA vì node này đã có trong reached"
            })
            trace_item["frontier_after_expand"] = preview_queue(frontier)
            trace_item["frontier_size_after"] = len(frontier)
            trace_item["reached_size_after"] = len(reached)
            trace.append(trace_item)
            continue

        reached.add(current_key)
        nodes_expanded += 1
        trace_item["is_goal"] = current_key == goal_key

        if current_key == goal_key:
            trace_item["frontier_after_expand"] = preview_queue(frontier)
            trace_item["frontier_size_after"] = len(frontier)
            trace_item["reached_size_after"] = len(reached)
            trace.append(trace_item)

            return {
                "path": node["path"],
                "actions": node["actions"],
                "nodes_expanded": nodes_expanded,
                "depth": len(node["actions"]),
                "cost": len(node["actions"]),
                "trace": trace
            }

        for next_state, action in get_neighbors(current_state):
            next_key = state_to_string(next_state)

            child_info = {
                "action": action,
                "state_key": next_key,
                "state": next_state,
                "status": ""
            }

            frontier.append({
                "state": next_state,
                "path": node["path"] + [next_state],
                "actions": node["actions"] + [action],
                "parent_action": action
            })

            if next_key in reached:
                child_info["status"] = "VẪN ADD vào frontier, nhưng sau này sẽ bị SKIP"
            else:
                child_info["status"] = "ADD vào frontier trước, chưa thêm reached"

            trace_item["children"].append(child_info)

        trace_item["frontier_after_expand"] = preview_queue(frontier)
        trace_item["frontier_size_after"] = len(frontier)
        trace_item["reached_size_after"] = len(reached)
        trace.append(trace_item)

    return None


# =========================
# UI APP
# =========================

class EightPuzzleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("8-Puzzle BFS Solver")
        self.geometry("1450x940")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.solution_path = []
        self.solution_actions = []
        self.current_index = 0
        self.animation_running = False

        self.bfs_trace = []
        self.trace_index = 0

        self.tile_buttons = []

        self.build_ui()
        self.draw_board(string_to_state("531620478"))

    # =========================
    # BUILD UI
    # =========================

    def build_ui(self):
        self.main_container = ctk.CTkScrollableFrame(
            self,
            fg_color="#0b1020",
            scrollbar_button_color="#1e3a5f",
            scrollbar_button_hover_color="#2563eb"
        )
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
        self.title_frame.pack(pady=(4, 12))

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
        self.badge.pack(pady=(0, 8))

        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="8-Puzzle Solver",
            font=("Arial", 34, "bold"),
            text_color="white"
        )
        self.title_label.pack()

        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Giải bài toán 8-Puzzle bằng thuật toán BFS và mô phỏng frontier, reached giống trên bảng.",
            font=("Arial", 13),
            text_color="#9ca3af"
        )
        self.subtitle_label.pack(pady=(6, 0))

        # Main layout
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack(pady=(0, 0))

        self.left_panel = ctk.CTkFrame(
            self.content_frame,
            width=310,
            height=350,
            corner_radius=24,
            fg_color="#111827"
        )
        self.left_panel.grid(row=0, column=0, padx=20, sticky="n")
        self.left_panel.grid_propagate(False)

        self.center_panel = ctk.CTkFrame(
            self.content_frame,
            width=360,
            height=430,
            fg_color="transparent"
        )
        self.center_panel.grid(row=0, column=1, padx=20, sticky="n")

        self.right_panel = ctk.CTkFrame(
            self.content_frame,
            width=330,
            height=350,
            corner_radius=24,
            fg_color="#111827"
        )
        self.right_panel.grid(row=0, column=2, padx=20, sticky="n")
        self.right_panel.grid_propagate(False)

        self.build_left_panel()
        self.build_board()
        self.build_right_panel()
        self.build_step_explain_panel()

    def build_left_panel(self):
        self.shuffle_button = ctk.CTkButton(
            self.left_panel,
            text="🔀 Shuffle Puzzle",
            height=42,
            corner_radius=14,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.shuffle_puzzle
        )
        self.shuffle_button.pack(fill="x", padx=20, pady=(18, 14))

        self.start_label = ctk.CTkLabel(
            self.left_panel,
            text='Enter initial state, from top-left to right-bottom,\n9 characters, e.g. "012345678"',
            justify="left",
            text_color="white",
            font=("Arial", 13, "bold")
        )
        self.start_label.pack(anchor="w", padx=20)

        self.start_entry = ctk.CTkEntry(
            self.left_panel,
            height=42,
            corner_radius=12,
            fg_color="#2b2c35",
            border_width=0,
            text_color="white"
        )
        self.start_entry.pack(fill="x", padx=20, pady=(6, 12))
        self.start_entry.insert(0, "531620478")

        self.goal_label = ctk.CTkLabel(
            self.left_panel,
            text="Enter goal state",
            text_color="white",
            font=("Arial", 13, "bold")
        )
        self.goal_label.pack(anchor="w", padx=20)

        self.goal_entry = ctk.CTkEntry(
            self.left_panel,
            height=42,
            corner_radius=12,
            fg_color="#2b2c35",
            border_width=0,
            text_color="white"
        )
        self.goal_entry.pack(fill="x", padx=20, pady=(6, 12))
        self.goal_entry.insert(0, "012345678")

        self.algorithm_label = ctk.CTkLabel(
            self.left_panel,
            text="Choose Algorithm",
            text_color="white",
            font=("Arial", 13, "bold")
        )
        self.algorithm_label.pack(anchor="w", padx=20)

        self.algorithm_box = ctk.CTkOptionMenu(
            self.left_panel,
            values=[
                "BFS Cách 1 - Check trước khi thêm",
                "BFS Cách 2 - Check khi lấy ra"
            ],
            height=42,
            corner_radius=12,
            fg_color="#2b2c35",
            button_color="#2b2c35",
            button_hover_color="#374151"
        )
        self.algorithm_box.pack(fill="x", padx=20, pady=(6, 12))

        self.solve_button = ctk.CTkButton(
            self.left_panel,
            text="Solve Puzzle",
            height=44,
            corner_radius=14,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.solve_puzzle
        )
        self.solve_button.pack(fill="x", padx=20)

        self.error_label = ctk.CTkLabel(
            self.left_panel,
            text="",
            text_color="#f87171",
            wraplength=280,
            font=("Arial", 13, "bold")
        )
        self.error_label.pack(padx=20, pady=(8, 0))

        self.note_label = ctk.CTkLabel(
            self.left_panel,
            text="Quy ước: số 0 là ô trống.\nBFS dùng hàng đợi FIFO để tìm lời giải ngắn nhất.",
            text_color="#9ca3af",
            justify="left",
            wraplength=280,
            font=("Arial", 12)
        )
        self.note_label.pack(anchor="w", padx=20, pady=(6, 0))

    def build_board(self):
        self.board_frame = ctk.CTkFrame(
            self.center_panel,
            width=340,
            height=340,
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
                    width=92,
                    height=92,
                    corner_radius=18,
                    fg_color="#2d9bf0",
                    text_color="white",
                    font=("Arial", 34, "bold")
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
        self.action_label.pack(pady=(10, 8))

        self.control_frame = ctk.CTkFrame(self.center_panel, fg_color="transparent")
        self.control_frame.pack()

        self.prev_button = ctk.CTkButton(
            self.control_frame,
            text="◄ Prev",
            width=90,
            height=40,
            fg_color="#0f172a",
            hover_color="#1e293b",
            command=self.prev_step
        )
        self.prev_button.grid(row=0, column=0, padx=6)

        self.stop_button = ctk.CTkButton(
            self.control_frame,
            text="Stop",
            width=90,
            height=40,
            fg_color="#0f172a",
            hover_color="#1e293b",
            command=self.stop_animation
        )
        self.stop_button.grid(row=0, column=1, padx=6)

        self.next_button = ctk.CTkButton(
            self.control_frame,
            text="Next ►",
            width=90,
            height=40,
            fg_color="#0f172a",
            hover_color="#1e293b",
            command=self.next_step
        )
        self.next_button.grid(row=0, column=2, padx=6)

    def build_right_panel(self):
        self.result_title = ctk.CTkLabel(
            self.right_panel,
            text="Results",
            text_color="#38bdf8",
            font=("Arial", 26, "bold")
        )
        self.result_title.pack(anchor="w", padx=20, pady=(18, 12))

        self.status_label = ctk.CTkLabel(
            self.right_panel,
            text="Pending user input...",
            text_color="#f59e0b",
            font=("Arial", 15, "bold")
        )
        self.status_label.pack(anchor="w", padx=20, pady=(0, 10))

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
        self.path_title.pack(anchor="w", padx=20, pady=(8, 6))

        self.path_text = ctk.CTkTextbox(
            self.right_panel,
            width=290,
            height=100,
            corner_radius=14,
            fg_color="#0f172a",
            text_color="#d1d5db",
            font=("Consolas", 12)
        )
        self.path_text.pack(padx=20)
        self.path_text.insert("1.0", "Chưa có dữ liệu")
        self.path_text.configure(state="disabled")

    def build_step_explain_panel(self):
        """
        Vùng trực quan BFS có thể cuộn:
        - Hàng 1: node đang xét, node con, frontier, reached
        - Hàng 2: tổng quan các bước lời giải, mỗi bước là một board 3x3
        """
        self.explain_panel = ctk.CTkFrame(
            self.main_container,
            width=1160,
            height=430,
            corner_radius=22,
            fg_color="#0f172a",
            border_width=1,
            border_color="#1f3b59"
        )
        self.explain_panel.pack(pady=(12, 28))
        self.explain_panel.pack_propagate(False)

        header_frame = ctk.CTkFrame(self.explain_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=16, pady=(10, 4))

        title = ctk.CTkLabel(
            header_frame,
            text="BFS Step Visualizer",
            text_color="#38bdf8",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(side="left")

        self.trace_hint = ctk.CTkLabel(
            header_frame,
            text="Kéo xuống để xem tổng quan đường đi: mỗi bảng là một lần hành động",
            text_color="#94a3b8",
            font=("Segoe UI", 12, "bold")
        )
        self.trace_hint.pack(side="left", padx=18)

        self.trace_counter_label = ctk.CTkLabel(
            header_frame,
            text="Trace: 0/0",
            text_color="#9ca3af",
            font=("Segoe UI", 13, "bold")
        )
        self.trace_counter_label.pack(side="right")

        body = ctk.CTkFrame(self.explain_panel, fg_color="transparent")
        body.pack(fill="x", padx=14, pady=(0, 6))

        self.node_card = ctk.CTkFrame(
            body, width=210, height=172, corner_radius=18,
            fg_color="#111827", border_width=1, border_color="#38bdf8"
        )
        self.node_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.node_card.grid_propagate(False)

        self.children_card = ctk.CTkFrame(
            body, width=315, height=172, corner_radius=18,
            fg_color="#111827", border_width=1, border_color="#f59e0b"
        )
        self.children_card.grid(row=0, column=1, sticky="nsew", padx=8)
        self.children_card.grid_propagate(False)

        self.frontier_card = ctk.CTkFrame(
            body, width=315, height=172, corner_radius=18,
            fg_color="#111827", border_width=1, border_color="#2563eb"
        )
        self.frontier_card.grid(row=0, column=2, sticky="nsew", padx=8)
        self.frontier_card.grid_propagate(False)

        self.reached_card = ctk.CTkFrame(
            body, width=270, height=172, corner_radius=18,
            fg_color="#111827", border_width=1, border_color="#22c55e"
        )
        self.reached_card.grid(row=0, column=3, sticky="nsew", padx=(8, 0))
        self.reached_card.grid_propagate(False)

        nav = ctk.CTkFrame(self.explain_panel, fg_color="transparent")
        nav.pack(fill="x", padx=14, pady=(0, 8))

        ctk.CTkButton(
            nav, text="◄ Trace trước", width=125, height=32,
            corner_radius=12, fg_color="#0f172a", hover_color="#1e293b",
            command=self.prev_trace
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            nav, text="Trace sau ►", width=125, height=32,
            corner_radius=12, fg_color="#0f172a", hover_color="#1e293b",
            command=self.next_trace
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            nav, text="Trace lời giải", width=130, height=32,
            corner_radius=12, fg_color="#2563eb", hover_color="#1d4ed8",
            command=self.show_solution_trace
        ).pack(side="left")

        self.solution_overview_panel = ctk.CTkFrame(
            self.explain_panel,
            width=1125,
            height=155,
            corner_radius=18,
            fg_color="#111827",
            border_width=1,
            border_color="#334155"
        )
        self.solution_overview_panel.pack(fill="x", padx=14, pady=(0, 10))
        self.solution_overview_panel.pack_propagate(False)

        self.render_empty_trace()
        self.render_solution_overview()

    def render_solution_overview(self):
        """Hiển thị tổng quan đường đi: mỗi bước là một board nhỏ."""
        if not hasattr(self, "solution_overview_panel"):
            return

        self.clear_widgets(self.solution_overview_panel)

        header = ctk.CTkFrame(self.solution_overview_panel, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(8, 2))

        ctk.CTkLabel(
            header,
            text="TỔNG QUAN CÁC BƯỚC LỜI GIẢI",
            text_color="#38bdf8",
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")

        if self.solution_path:
            ctk.CTkLabel(
                header,
                text=f"{len(self.solution_path) - 1} hành động",
                text_color="#f59e0b",
                font=("Segoe UI", 12, "bold")
            ).pack(side="right")
        else:
            ctk.CTkLabel(
                header,
                text="Bấm Solve Puzzle để hiện từng bảng",
                text_color="#94a3b8",
                font=("Segoe UI", 12, "bold")
            ).pack(side="right")

        scroller = ctk.CTkScrollableFrame(
            self.solution_overview_panel,
            width=1095,
            height=103,
            orientation="horizontal",
            fg_color="#020617",
            corner_radius=14
        )
        scroller.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        if not self.solution_path:
            ctk.CTkLabel(
                scroller,
                text="Chưa có dữ liệu. Sau khi giải, mỗi trạng thái sẽ được hiển thị thành một bảng 3x3 ở đây.",
                text_color="#94a3b8",
                font=("Segoe UI", 12, "bold")
            ).pack(padx=20, pady=30)
            return

        for idx, state in enumerate(self.solution_path):
            action = "START" if idx == 0 else self.solution_actions[idx - 1]
            color = "#38bdf8" if idx == 0 else "#22c55e"
            if idx == self.current_index:
                color = "#f59e0b"

            card = self.create_state_card(
                scroller,
                state,
                title=f"Step {idx}",
                subtitle=action,
                color=color,
                width=88,
                height=88,
                cell=15,
                font_size=8
            )
            card.pack(side="left", padx=6, pady=6)

            if idx < len(self.solution_path) - 1:
                ctk.CTkLabel(
                    scroller,
                    text="→",
                    text_color="#64748b",
                    font=("Segoe UI", 18, "bold")
                ).pack(side="left", padx=(0, 2), pady=28)

    def create_result_line(self, title):
        label = ctk.CTkLabel(
            self.right_panel,
            text=f"{title} ",
            text_color="white",
            font=("Arial", 15, "bold")
        )
        label.pack(anchor="w", padx=20, pady=6)
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
    # TRACE FUNCTIONS
    # =========================

    def clear_widgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def string_key_to_state(self, key):
        if key.startswith("..."):
            return None
        if len(key) != 9 or not key.isdigit():
            return None
        return string_to_state(key)

    def create_section_header(self, parent, title, subtitle, color):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(7, 3))

        ctk.CTkLabel(
            header,
            text=title,
            text_color=color,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=subtitle,
            text_color="#94a3b8",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

    def create_mini_board(self, parent, state, cell=20, font_size=10,
                          tile_color="#1d4ed8", empty_color="#020617"):
        board = ctk.CTkFrame(parent, fg_color="transparent")

        for i in range(3):
            for j in range(3):
                value = state[i][j]
                fg = empty_color if value == 0 else tile_color
                text = "" if value == 0 else str(value)

                ctk.CTkLabel(
                    board,
                    text=text,
                    width=cell,
                    height=cell,
                    corner_radius=6,
                    fg_color=fg,
                    text_color="white",
                    font=("Segoe UI", font_size, "bold")
                ).grid(row=i, column=j, padx=1, pady=1)

        return board

    def create_state_card(self, parent, state, title="", subtitle="", color="#38bdf8",
                          width=86, height=82, cell=16, font_size=8):
        card = ctk.CTkFrame(
            parent,
            width=width,
            height=height,
            corner_radius=12,
            fg_color="#0b1220",
            border_width=1,
            border_color=color
        )
        card.pack_propagate(False)

        if title:
            ctk.CTkLabel(
                card,
                text=title,
                text_color=color,
                font=("Segoe UI", 8, "bold")
            ).pack(pady=(3, 1))

        board = self.create_mini_board(card, state, cell=cell, font_size=font_size, tile_color=color)
        board.pack(pady=(0, 1))

        if subtitle:
            ctk.CTkLabel(
                card,
                text=subtitle,
                text_color="#cbd5e1",
                font=("Segoe UI", 8, "bold")
            ).pack()

        return card

    def render_empty_trace(self):
        for frame in [self.node_card, self.children_card, self.frontier_card, self.reached_card]:
            self.clear_widgets(frame)

        self.create_section_header(self.node_card, "NODE", "Chưa có dữ liệu", "#38bdf8")
        self.create_section_header(self.children_card, "NODE CON", "Bấm Solve Puzzle", "#f59e0b")
        self.create_section_header(self.frontier_card, "FRONTIER", "Queue FIFO", "#60a5fa")
        self.create_section_header(self.reached_card, "REACHED", "State đã biết", "#22c55e")

        def placeholder(parent, text, color="#94a3b8", pady=24):
            box = ctk.CTkFrame(parent, fg_color="transparent")
            box.pack(fill="both", expand=True, padx=8, pady=(2, 8))

            ctk.CTkLabel(
                box,
                text=text,
                text_color=color,
                font=("Segoe UI", 11, "bold"),
                justify="center",
                wraplength=150
            ).pack(expand=True)

        placeholder(self.node_card, "Chọn cách BFS\nrồi bấm Solve", "#94a3b8")
        placeholder(self.children_card, "Các node con\nsẽ hiện ở đây", "#94a3b8")
        placeholder(self.frontier_card, "Hàng đợi Frontier\nsẽ hiện ở đây", "#94a3b8")
        placeholder(self.reached_card, "Reached dùng để\ntránh lặp state", "#94a3b8")

    def render_list_of_state_cards(self, parent, keys, color, empty_text, max_items=4):
        list_frame = ctk.CTkScrollableFrame(
            parent,
            width=280,
            height=100,
            corner_radius=12,
            fg_color="#020617"
        )
        list_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        if not keys:
            ctk.CTkLabel(
                list_frame,
                text=empty_text,
                text_color="#64748b",
                font=("Segoe UI", 12, "bold")
            ).pack(pady=25)
            return

        row = 0
        col = 0
        for idx, key in enumerate(keys[:max_items], start=1):
            state = self.string_key_to_state(key)

            if state is None:
                ctk.CTkLabel(
                    list_frame,
                    text=key,
                    text_color="#94a3b8",
                    font=("Segoe UI", 11, "bold")
                ).grid(row=row, column=col, padx=5, pady=5, sticky="w")
            else:
                card = self.create_state_card(
                    list_frame,
                    state,
                    title=f"#{idx}",
                    subtitle="",
                    color=color,
                    width=82,
                    height=80,
                    cell=15,
                    font_size=8
                )
                card.grid(row=row, column=col, padx=5, pady=5)

            col += 1
            if col >= 3:
                col = 0
                row += 1

        if len(keys) > max_items:
            ctk.CTkLabel(
                list_frame,
                text=f"+{len(keys) - max_items} state",
                text_color="#94a3b8",
                font=("Segoe UI", 11, "bold")
            ).grid(row=row, column=col, padx=7, pady=5)

    def show_trace_at(self, index):
        if not self.bfs_trace:
            return

        index = max(0, min(index, len(self.bfs_trace) - 1))
        self.trace_index = index
        item = self.bfs_trace[self.trace_index]

        for frame in [self.node_card, self.children_card, self.frontier_card, self.reached_card]:
            self.clear_widgets(frame)

        # NODE ĐANG XÉT
        node_subtitle = f"Iter {item['iteration']} | {item['action']} | {item['node_key']}"
        if item["is_goal"]:
            node_subtitle += " | GOAL"

        self.create_section_header(self.node_card, "NODE ĐANG XÉT", node_subtitle, "#38bdf8")
        big_board = self.create_mini_board(
            self.node_card,
            item["node"],
            cell=30,
            font_size=15,
            tile_color="#2563eb",
            empty_color="#020617"
        )
        big_board.pack(pady=(3, 4))

        ctk.CTkLabel(
            self.node_card,
            text=item.get("mode", "Lấy đầu hàng đợi FIFO"),
            text_color="#cbd5e1",
            font=("Segoe UI", 9, "bold"),
            wraplength=175,
            justify="center"
        ).pack()

        # CHILDREN
        self.create_section_header(
            self.children_card,
            "NODE CON SINH RA",
            "Move UP / DOWN / LEFT / RIGHT",
            "#f59e0b"
        )

        children_scroll = ctk.CTkScrollableFrame(
            self.children_card,
            width=285,
            height=100,
            corner_radius=12,
            fg_color="#020617"
        )
        children_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        if item["is_goal"]:
            ctk.CTkLabel(
                children_scroll,
                text="Đã gặp GOAL\n=> Dừng BFS",
                text_color="#22c55e",
                font=("Arial", 13, "bold"),
                justify="center"
            ).pack(pady=20)
        else:
            for idx, child in enumerate(item["children"]):
                status_add = "ADD" in child["status"]
                status_skip = "SKIP" in child["status"] or "BỎ QUA" in child["status"]

                if "VẪN ADD" in child["status"]:
                    color = "#f59e0b"
                    status_text = "ADD rồi SKIP"
                elif status_add and not status_skip:
                    color = "#22c55e"
                    status_text = "ADD"
                else:
                    color = "#ef4444"
                    status_text = "SKIP"

                card = self.create_state_card(
                    children_scroll,
                    child["state"],
                    title=f"{child['action']}",
                    subtitle=status_text,
                    color=color,
                    width=84,
                    height=86,
                    cell=15,
                    font_size=8
                )
                card.grid(row=0, column=idx, padx=5, pady=5)

        # FRONTIER
        frontier_title = f"FRONTIER ({item['frontier_size_after']})"
        self.create_section_header(
            self.frontier_card,
            frontier_title,
            "Các state đang chờ xét",
            "#60a5fa"
        )
        self.render_list_of_state_cards(
            self.frontier_card,
            item["frontier_after_expand"],
            color="#60a5fa",
            empty_text="Frontier rỗng",
            max_items=6
        )

        # REACHED
        reached_title = f"REACHED ({item['reached_size_after']})"
        self.create_section_header(
            self.reached_card,
            reached_title,
            "Tránh lặp lại state cũ",
            "#22c55e"
        )
        self.render_list_of_state_cards(
            self.reached_card,
            item["reached_before_expand"],
            color="#22c55e",
            empty_text="Reached rỗng",
            max_items=5
        )

        self.trace_counter_label.configure(
            text=f"Trace: {self.trace_index + 1}/{len(self.bfs_trace)}"
        )

    def next_trace(self):
        if self.bfs_trace and self.trace_index < len(self.bfs_trace) - 1:
            self.show_trace_at(self.trace_index + 1)

    def prev_trace(self):
        if self.bfs_trace and self.trace_index > 0:
            self.show_trace_at(self.trace_index - 1)

    def show_solution_trace(self):
        if not self.solution_path or not self.bfs_trace:
            return

        solution_keys = [state_to_string(s) for s in self.solution_path]
        current_key = solution_keys[min(self.current_index, len(solution_keys) - 1)]

        for index, item in enumerate(self.bfs_trace):
            if item["node_key"] == current_key:
                self.show_trace_at(index)
                return

        # Nếu không khớp current node thì nhảy tới node đầu của lời giải
        for index, item in enumerate(self.bfs_trace):
            if item["node_key"] in set(solution_keys):
                self.show_trace_at(index)
                return

    # =========================
    # BUTTON ACTIONS
    # =========================

    def get_bfs_mode(self):
        selected = self.algorithm_box.get()
        if "Cách 2" in selected:
            return "late"
        return "early"

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

        # Tránh bấm nhiều lần làm app bị đơ
        self.solve_button.configure(state="disabled", text="Đang giải BFS...")
        self.shuffle_button.configure(state="disabled")
        self.status_label.configure(
            text="Đang chạy BFS, vui lòng chờ...",
            text_color="#f59e0b"
        )

        # Chạy BFS ở luồng phụ để UI không bị Not Responding
        mode = self.get_bfs_mode()

        worker = threading.Thread(
            target=self.solve_puzzle_worker,
            args=(start_str, goal_str, mode),
            daemon=True
        )
        worker.start()

    def solve_puzzle_worker(self, start_str, goal_str, mode):
        start = string_to_state(start_str)
        goal = string_to_state(goal_str)

        start_time = time.perf_counter()
        result = bfs(start, goal, mode=mode)
        end_time = time.perf_counter()

        runtime = (end_time - start_time) * 1000

        # Mọi cập nhật UI phải quay về main thread bằng after()
        self.after(0, lambda: self.finish_solve(result, runtime))

    def finish_solve(self, result, runtime):
        self.solve_button.configure(state="normal", text="Solve Puzzle")
        self.shuffle_button.configure(state="normal")

        if result is None:
            self.error_label.configure(text="Không tìm thấy lời giải.")
            self.status_label.configure(
                text="Không tìm thấy lời giải",
                text_color="#f87171"
            )
            return

        self.solution_path = result["path"]
        self.solution_actions = result["actions"]
        self.bfs_trace = result["trace"]
        self.trace_index = 0
        self.current_index = 0

        self.update_results(result, runtime)
        self.show_trace_at(0)
        self.render_solution_overview()
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
            self.render_solution_overview()
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
            self.render_solution_overview()

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
            self.render_solution_overview()

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

        # Tạo puzzle bằng random walk từ goal thay vì shuffle toàn bộ.
        # Nhờ vậy BFS chạy nhanh hơn, không bị đứng app.
        start_str = generate_by_random_walk(goal_str, steps=14)

        self.start_entry.delete(0, "end")
        self.start_entry.insert(0, start_str)

        self.solution_path = []
        self.solution_actions = []
        self.bfs_trace = []
        self.trace_index = 0
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

        self.render_empty_trace()
        self.render_solution_overview()
        self.trace_counter_label.configure(text="Trace: 0/0")



if __name__ == "__main__":
    app = EightPuzzleApp()
    app.mainloop()
