# 8-Puzzle BFS Solver - Python UI

## Giới thiệu

Dự án này là chương trình giải bài toán **8-Puzzle** bằng thuật toán **BFS - Breadth First Search** và có giao diện người dùng được xây dựng bằng **Python CustomTkinter**.

Chương trình cho phép người dùng nhập trạng thái ban đầu, trạng thái đích, sau đó thuật toán BFS sẽ tìm đường đi ngắn nhất để đưa puzzle từ trạng thái ban đầu về trạng thái đích.

Giao diện được thiết kế theo phong cách hiện đại, tương tự bản web `index.html`, gồm bảng puzzle, nút điều khiển, phần kết quả và hoạt ảnh di chuyển từng bước.

---

## Công nghệ sử dụng

Dự án sử dụng:

- Python
- CustomTkinter
- Thuật toán BFS
- Queue / hàng đợi
- Set để lưu trạng thái đã duyệt

---

## Cài đặt thư viện

Trước khi chạy chương trình, cần cài thư viện `customtkinter`.

Chạy lệnh sau trong terminal:

```bash
pip install customtkinter
```

---

## Cách chạy chương trình

### Bước 1: Tạo file Python

Tạo file:

```text
app.py
```

Sau đó dán code chương trình vào file `app.py`.

### Bước 2: Chạy chương trình

Mở terminal trong thư mục chứa file và chạy:

```bash
python app.py
```

Hoặc nếu dùng Python 3:

```bash
python3 app.py
```

---

## Bài toán 8-Puzzle là gì?

8-Puzzle là bài toán gồm một bảng `3x3` có các số từ `1` đến `8` và một ô trống.

Trong chương trình này:

```text
0 = Ô trống
```

Ví dụ trạng thái:

```text
5 3 1
6 2 0
4 7 8
```

Được nhập dưới dạng chuỗi:

```text
531620478
```

Chương trình sẽ đọc chuỗi này từ trái sang phải, từ trên xuống dưới.

---

## Trạng thái ban đầu và trạng thái đích

Trong giao diện có 2 ô nhập:

### Initial State

Là trạng thái ban đầu của puzzle.

Ví dụ:

```text
531620478
```

Tương ứng với ma trận:

```text
5 3 1
6 2 0
4 7 8
```

### Goal State

Là trạng thái đích cần đạt được.

Ví dụ:

```text
012345678
```

Tương ứng với ma trận:

```text
0 1 2
3 4 5
6 7 8
```

---

## Quy tắc nhập dữ liệu

Người dùng phải nhập đúng 9 ký tự gồm các số từ `0` đến `8`.

Ví dụ hợp lệ:

```text
531620478
```

Ví dụ không hợp lệ:

```text
12345678
```

Vì thiếu 1 số.

Ví dụ không hợp lệ:

```text
112345678
```

Vì số `1` bị lặp lại.

---

## Thuật toán BFS

BFS là viết tắt của **Breadth First Search**, nghĩa là tìm kiếm theo chiều rộng.

Thuật toán BFS hoạt động bằng cách duyệt các trạng thái theo từng mức độ sâu.

BFS sử dụng:

```text
frontier = hàng đợi các trạng thái chờ xét
reached = tập hợp các trạng thái đã đi qua
```

Vì BFS duyệt theo từng lớp nên nếu tìm được lời giải, đó là lời giải có số bước ngắn nhất.

---

## Ý tưởng thuật toán BFS trong chương trình

Mỗi trạng thái của bài toán là một ma trận `3x3`.

Từ một trạng thái hiện tại, chương trình tìm vị trí của ô trống `0`.

Sau đó sinh ra các trạng thái con bằng cách di chuyển ô trống:

```text
UP
DOWN
LEFT
RIGHT
```

Nếu trạng thái con chưa từng xuất hiện trong `reached`, chương trình sẽ thêm nó vào `frontier`.

Quá trình lặp lại cho đến khi tìm được trạng thái đích.

---

## Tập luật di chuyển

Ô trống `0` có thể di chuyển theo 4 hướng nếu hợp lệ:

```text
IF ô trống không ở hàng trên cùng
    THEN có thể đi UP

IF ô trống không ở hàng dưới cùng
    THEN có thể đi DOWN

IF ô trống không ở cột trái cùng
    THEN có thể đi LEFT

IF ô trống không ở cột phải cùng
    THEN có thể đi RIGHT
```

Ví dụ:

Nếu ô trống ở giữa bảng:

```text
1 2 3
4 0 5
6 7 8
```

Thì có thể đi đủ 4 hướng:

```text
UP, DOWN, LEFT, RIGHT
```

Nếu ô trống ở góc trên trái:

```text
0 1 2
3 4 5
6 7 8
```

Thì chỉ có thể đi:

```text
DOWN, RIGHT
```

---

## Cấu trúc chính của chương trình

Chương trình gồm 2 phần lớn:

```text
1. Phần xử lý thuật toán BFS
2. Phần giao diện CustomTkinter
```

---

## Các hàm xử lý thuật toán

### `string_to_state(s)`

Chuyển chuỗi nhập vào thành ma trận `3x3`.

Ví dụ:

```python
string_to_state("531620478")
```

Kết quả:

```python
[
    [5, 3, 1],
    [6, 2, 0],
    [4, 7, 8]
]
```

---

### `state_to_string(state)`

Chuyển ma trận `3x3` thành chuỗi để dễ lưu vào `set`.

Ví dụ:

```python
[
    [5, 3, 1],
    [6, 2, 0],
    [4, 7, 8]
]
```

Được chuyển thành:

```text
531620478
```

Hàm này giúp chương trình kiểm tra trạng thái đã đi qua hay chưa.

---

### `find_zero(state)`

Tìm vị trí của ô trống `0`.

Ví dụ:

```text
5 3 1
6 2 0
4 7 8
```

Ô trống nằm ở vị trí:

```text
(1, 2)
```

---

### `get_neighbors(state)`

Sinh ra các trạng thái con từ trạng thái hiện tại.

Chương trình sẽ thử di chuyển ô trống theo 4 hướng:

```text
UP
DOWN
LEFT
RIGHT
```

Nếu hướng đi hợp lệ, chương trình tạo ra một trạng thái mới.

---

### `is_valid_input(s)`

Kiểm tra chuỗi nhập vào có hợp lệ không.

Điều kiện hợp lệ:

```text
Có đúng 9 ký tự
Gồm đủ các số từ 0 đến 8
Không trùng số
```

---

### `is_solvable(start, goal)`

Kiểm tra bài toán có thể giải được hay không.

Không phải mọi trạng thái 8-Puzzle đều có lời giải.

Chương trình dùng số nghịch thế để kiểm tra khả năng giải được của puzzle.

---

### `bfs(start, goal)`

Đây là hàm chính thực hiện thuật toán BFS.

Hàm này trả về:

```text
path = danh sách các trạng thái từ đầu đến đích
actions = danh sách các hành động di chuyển
nodes_expanded = số node đã mở rộng
depth = độ sâu tìm kiếm
cost = chi phí đường đi
```

---

## Giải thích hàm BFS

Thuật toán BFS trong chương trình hoạt động như sau:

```text
Bắt đầu với trạng thái ban đầu

Đưa trạng thái ban đầu vào frontier

Đưa trạng thái ban đầu vào reached

Trong khi frontier chưa rỗng:
    Lấy trạng thái đầu tiên ra khỏi frontier

    Nếu trạng thái đó là trạng thái đích:
        Trả về đường đi

    Sinh các trạng thái con bằng cách di chuyển ô trống

    Với mỗi trạng thái con:
        Nếu trạng thái con chưa có trong reached:
            Thêm vào reached
            Thêm vào frontier
```

---

## Pseudocode BFS

```text
BFS(start, goal):
    frontier = queue()
    frontier.push(start)

    reached = set()
    reached.add(start)

    while frontier is not empty:
        node = frontier.pop_front()

        if node == goal:
            return solution

        for child in get_neighbors(node):
            if child not in reached:
                reached.add(child)
                frontier.push(child)

    return failure
```

---

## Giao diện chương trình

Giao diện gồm 3 phần chính:

### 1. Bảng điều khiển bên trái

Gồm:

```text
Shuffle Puzzle
Enter initial state
Enter goal state
Choose Algorithm
Solve Puzzle
```

---

### 2. Bảng puzzle ở giữa

Hiển thị ma trận `3x3`.

Các ô số từ `1` đến `8` được hiển thị bằng các ô màu xanh.

Ô số `0` được xem là ô trống.

Khi bấm **Solve Puzzle**, các ô sẽ tự động di chuyển từng bước đến trạng thái đích.

---

### 3. Bảng kết quả bên phải

Hiển thị:

```text
Runtime Duration
Nodes Expanded
Search Depth
Path Cost
Path to Goal
```

Ý nghĩa:

| Thành phần | Ý nghĩa |
|---|---|
| Runtime Duration | Thời gian chạy thuật toán |
| Nodes Expanded | Số trạng thái đã mở rộng |
| Search Depth | Độ sâu tìm kiếm |
| Path Cost | Số bước di chuyển |
| Path to Goal | Danh sách trạng thái từ đầu đến đích |

---

## Các nút chức năng

### Shuffle Puzzle

Tạo ngẫu nhiên một trạng thái ban đầu có thể giải được.

### Solve Puzzle

Chạy thuật toán BFS để tìm lời giải.

Sau khi tìm được lời giải, chương trình tự động chạy hoạt ảnh các bước di chuyển.

### Prev

Lùi lại một bước trong đường đi lời giải.

### Stop

Dừng hoạt ảnh tự động.

### Next

Tiến lên một bước trong đường đi lời giải.

### Menu ba chấm

Menu có các chức năng:

```text
System
Light
Dark
Print
Record screen
```

Trong bản Python desktop, Print và Record screen chỉ hiển thị thông báo vì đây không phải trình duyệt web.

---

## Kết quả mong đợi

Khi chạy chương trình, người dùng nhập trạng thái ban đầu và trạng thái đích.

Ví dụ:

```text
Initial State: 531620478
Goal State:    012345678
```

Sau khi bấm:

```text
Solve Puzzle
```

Chương trình sẽ:

```text
Kiểm tra input
Kiểm tra puzzle có giải được không
Chạy BFS
Hiển thị kết quả
Tự động chạy hoạt ảnh các bước di chuyển
```

---

## Ví dụ output trong phần Results

```text
Solved successfully!

Runtime Duration: 15.234 ms
Nodes Expanded: 1250
Search Depth: 18
Path Cost: 18
```

Phần `Path to Goal` hiển thị từng trạng thái:

```text
Step 0
531620478

Step 1 - Move LEFT
531602478

Step 2 - Move DOWN
531672408
```

---

## Kiến thức AI được minh họa

Dự án này minh họa các kiến thức trong môn Trí tuệ nhân tạo:

### State

State là trạng thái hiện tại của bài toán.

Trong 8-Puzzle, state là một ma trận `3x3`.

---

### Initial State

Initial State là trạng thái ban đầu.

Ví dụ:

```text
531620478
```

---

### Goal State

Goal State là trạng thái cần đạt đến.

Ví dụ:

```text
012345678
```

---

### Action

Action là hành động di chuyển ô trống:

```text
UP
DOWN
LEFT
RIGHT
```

---

### State Space

State Space là không gian trạng thái, gồm tất cả các trạng thái có thể đạt được từ trạng thái ban đầu.

---

### Frontier

Frontier là hàng đợi chứa các trạng thái đang chờ được xét.

Trong BFS, frontier hoạt động theo cơ chế FIFO:

```text
Vào trước, ra trước
```

---

### Reached

Reached là tập hợp các trạng thái đã được sinh ra hoặc đã đi qua.

Reached giúp tránh việc xét lại cùng một trạng thái nhiều lần.

---

### Node

Node là một trạng thái trong cây tìm kiếm, kèm theo đường đi và hành động dẫn đến trạng thái đó.

---

### Search Depth

Search Depth là độ sâu của lời giải, tức là số bước từ trạng thái ban đầu đến trạng thái đích.

---

### Path Cost

Path Cost là chi phí đường đi.

Trong bài toán này, mỗi hành động có chi phí bằng `1`, nên:

```text
Path Cost = Search Depth
```

---

## Vì sao BFS tìm được lời giải ngắn nhất?

BFS duyệt các trạng thái theo từng mức độ sâu.

Nó xét tất cả trạng thái ở độ sâu `0`, rồi đến độ sâu `1`, rồi độ sâu `2`, và cứ tiếp tục như vậy.

Vì vậy, khi BFS gặp trạng thái đích lần đầu tiên, đó là lời giải có số bước ít nhất.

---

## Ưu điểm

- Có giao diện trực quan.
- Code bằng Python.
- Dễ chạy và dễ hiểu.
- Dùng thuật toán BFS đúng yêu cầu.
- Có hoạt ảnh mô phỏng đường đi.
- Có kiểm tra trạng thái hợp lệ.
- Có kiểm tra trạng thái có giải được không.
- Hiển thị các thông số thuật toán.

---

## Hạn chế

- BFS có thể tốn bộ nhớ nếu trạng thái quá khó.
- Chỉ hỗ trợ bài toán 8-Puzzle kích thước `3x3`.
- Giao diện desktop chưa linh hoạt như web.
- Chức năng Print và Record screen chưa hoạt động giống trình duyệt web.

---

## Hướng phát triển

Có thể mở rộng chương trình theo các hướng sau:

1. Thêm thuật toán DFS.
2. Thêm thuật toán UCS.
3. Thêm thuật toán A*.
4. Thêm heuristic Manhattan Distance.
5. Thêm heuristic Misplaced Tiles.
6. Cho phép chỉnh tốc độ hoạt ảnh.
7. Thêm nút Reset.
8. Lưu kết quả tìm kiếm ra file.
9. Thêm giao diện so sánh các thuật toán.
10. Hỗ trợ puzzle kích thước lớn hơn như 15-Puzzle.

---

## Cấu trúc file đề xuất

```text
8-puzzle-bfs-python-ui/
│
├── app.py
├── README.md
└── requirements.txt
```

File `requirements.txt` có thể gồm:

```text
customtkinter
```

---

## Tác giả

Dự án được thực hiện cho bài học về thuật toán tìm kiếm trong môn Trí tuệ nhân tạo.

---

## Kết luận

Dự án này mô phỏng bài toán **8-Puzzle** sử dụng thuật toán **BFS** với giao diện Python bằng **CustomTkinter**.

Chương trình giúp người học hiểu rõ:

```text
Cách biểu diễn trạng thái
Cách sinh trạng thái con
Cách hoạt động của BFS
Vai trò của frontier và reached
Cách truy vết đường đi từ trạng thái đầu đến trạng thái đích
```

Đây là một ví dụ trực quan, phù hợp cho việc học và trình bày bài toán tìm kiếm trong Trí tuệ nhân tạo.
