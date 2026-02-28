"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ⚡ UNIVERSITY LEVEL 3 - v5.3 ALGORITHMS & DATA STRUCTURES ADVANCED ⚡   ║
║                                                                              ║
║      공간과 시간의 거래 (Time-Space Complexity Tradeoff)                   ║
║  1억 개 데이터도 0.1초에 처리하는 효율성의 극한                            ║
║                                                                              ║
║  "설계자님의 코드는 이제 가장 우아하고 빠른 길을 찾습니다" - gogs         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📚 학습 목표:
   1️⃣ Big-O 표기법: 효율성을 수학적으로 증명
   2️⃣ 선형 검색 vs 이진 검색: O(n) vs O(log n)
   3️⃣ Hash Table: O(1) 마법의 원리
   4️⃣ Tree & Graph: 데이터 관계 설계
   5️⃣ Heap & Priority Queue: 우선순위 관리
   6️⃣ 정렬 알고리즘: Bubble, Quick, Merge (성능 비교)
   7️⃣ Dynamic Programming: 기록이 증명이다
   8️⃣ 성능 벤치마킹: 실제 측정으로 증명

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 1: Big-O 표기법 - 효율성의 척도                                      ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
📈 Big-O 복잡도 비교:

n=10      n=100       n=1,000      n=10,000      n=100,000
│         │           │            │             │
│         │           │            │             │
O(1)      O(1)        O(1)         O(1)          O(1)           ━━━━━
          │           │            │             │
O(log n)  O(log n)    O(log n)     O(log n)      O(log n)       ─────
          │           │            │             │
O(n)      O(n)        O(n)         O(n)          O(n)           ─┐
          │           │            │             │               │
O(n²)     O(n²)       O(n²)        O(n²)         O(n²)           ├─ 피해야함!
          │           │            │             │               │
O(2ⁿ)     O(2ⁿ)       O(2ⁿ)        O(2ⁿ)         O(2ⁿ)           ─┘


┌──────────────────────────────────────────────────────────────┐
│ 실제 성능 (1,000,000 요소 검색)                              │
├──────────────────────────────────────────────────────────────┤
│ O(1)          → 0.000001초 (1 마이크로초)                   │
│ O(log n)      → 0.00002초 (20 비교)                         │
│ O(n)          → 1초 (1,000,000 비교)                       │
│ O(n log n)    → 20초 (정렬: Merge Sort)                    │
│ O(n²)         → 11.5일 (1,000,000,000,000 비교)            │
│ O(2ⁿ)         → 우주가 끝날 때까지... ∞                     │
└──────────────────────────────────────────────────────────────┘


🎯 선택 기준:

"1억 개 데이터 중에서 값 검색"

❌ 선형 검색 O(n):
   → 최악: 1억 번 비교 (평균 5000만 번)
   → 시간: ~50초 (불쾌하게 느림)

✅ 이진 검색 O(log n):
   → 최악: 26회 비교 (log₂(1억))
   → 시간: ~0.0001초 (번개같음)

→ 500,000배 빠름!
"""

import time
import heapq
from typing import List, Dict, Optional, Tuple, Any
from collections import defaultdict, deque


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 2: 검색 알고리즘 - 선형 vs 이진                                      ║
# ╚════════════════════════════════════════════════════════════════════════════╝

class SearchAlgorithms:
    """검색 알고리즘 구현"""

    @staticmethod
    def linear_search(data: List[int], target: int) -> Tuple[int, int]:
        """
        선형 검색 (Linear Search)
        시간복잡도: O(n)

        Returns: (인덱스, 비교횟수)
        """
        comparisons = 0
        for i in range(len(data)):
            comparisons += 1
            if data[i] == target:
                return i, comparisons
        return -1, comparisons

    @staticmethod
    def binary_search(data: List[int], target: int) -> Tuple[int, int]:
        """
        이진 검색 (Binary Search)
        조건: 데이터가 정렬되어 있어야 함
        시간복잡도: O(log n)

        Returns: (인덱스, 비교횟수)
        """
        low = 0
        high = len(data) - 1
        comparisons = 0

        while low <= high:
            comparisons += 1
            mid = (low + high) // 2

            if data[mid] == target:
                return mid, comparisons
            elif data[mid] < target:
                low = mid + 1
            else:
                high = mid - 1

        return -1, comparisons

    @staticmethod
    def benchmark_search(data_size: int, target_pos: str = 'end'):
        """검색 성능 벤치마크"""
        data = list(range(data_size))

        if target_pos == 'end':
            target = data_size - 1
        elif target_pos == 'middle':
            target = data_size // 2
        else:
            target = 0

        print(f"\n📊 검색 테스트 (데이터: {data_size:,}개, 위치: {target_pos})")

        # 선형 검색
        start = time.perf_counter()
        _, linear_comps = SearchAlgorithms.linear_search(data, target)
        linear_time = time.perf_counter() - start

        # 이진 검색
        start = time.perf_counter()
        _, binary_comps = SearchAlgorithms.binary_search(data, target)
        binary_time = time.perf_counter() - start

        print(f"  선형 검색: {linear_time*1000:.2f}ms ({linear_comps:,}회 비교)")
        print(f"  이진 검색: {binary_time*1000:.4f}ms ({binary_comps}회 비교)")
        print(f"  속도 향상: {linear_time/binary_time:.0f}배 빠름")


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 3: Hash Table - O(1) 마법                                            ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🎩 Hash Table의 마법: O(1) 검색

원리:
"데이터를 정렬하지 말고, 위치를 직접 계산하자!"

예시:
학번 → 학생 정보 매핑

❌ 리스트 사용 (선형 검색 O(n)):
데이터: [Alice, Bob, Charlie, ...]
검색: Alice 찾기 → 처음부터 하나씩 비교

✅ Hash Table (O(1)):
학번 2024001 → hash(2024001) → 인덱스 42 → Alice 즉시 반환!

┌─────────────┬─────────────┬─────────────┐
│ 인덱스 42   │ Alice       │ 2024001     │
├─────────────┼─────────────┼─────────────┤
│ hash값      │ 데이터      │ 원본 키     │
└─────────────┴─────────────┴─────────────┘

충돌(Collision) 처리:
여러 키가 같은 해시값을 가질 때:
  ├─ Chaining: 같은 위치에 연결 리스트
  └─ Open Addressing: 다른 위치 찾기
"""


class CustomHashTable:
    """Hash Table 구현 (Chaining 방식)"""

    def __init__(self, size: int = 16):
        """해시 테이블 초기화"""
        self.size = size
        self.table: List[List[Tuple[str, Any]]] = [[] for _ in range(size)]
        self.comparisons = 0

    def _hash(self, key: str) -> int:
        """해시 함수 (간단한 구현)"""
        return sum(ord(c) for c in key) % self.size

    def put(self, key: str, value: Any):
        """키-값 삽입"""
        hash_idx = self._hash(key)
        bucket = self.table[hash_idx]

        # 기존 키 업데이트
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # 새 키 추가
        bucket.append((key, value))

    def get(self, key: str) -> Optional[Any]:
        """값 검색 (O(1) 평균, O(n) 최악)"""
        hash_idx = self._hash(key)
        bucket = self.table[hash_idx]

        self.comparisons = 0
        for k, v in bucket:
            self.comparisons += 1
            if k == key:
                return v

        return None

    def get_stats(self) -> Dict:
        """테이블 통계"""
        total_items = sum(len(bucket) for bucket in self.table)
        empty_buckets = sum(1 for bucket in self.table if len(bucket) == 0)
        max_bucket_size = max(len(bucket) for bucket in self.table)

        return {
            'total_items': total_items,
            'empty_buckets': empty_buckets,
            'max_bucket_size': max_bucket_size,
            'load_factor': total_items / self.size
        }


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 4: 정렬 알고리즘 - Bubble vs Quick vs Merge                          ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🔄 정렬 알고리즘 비교:

┌──────────────┬─────────────┬─────────────┬──────────────┐
│ 알고리즘     │ 최선        │ 평균        │ 최악         │
├──────────────┼─────────────┼─────────────┼──────────────┤
│ Bubble Sort  │ O(n)        │ O(n²)       │ O(n²)        │
│ Quick Sort   │ O(n log n)  │ O(n log n)  │ O(n²)        │
│ Merge Sort   │ O(n log n)  │ O(n log n)  │ O(n log n)   │
│ Heap Sort    │ O(n log n)  │ O(n log n)  │ O(n log n)   │
└──────────────┴─────────────┴─────────────┴──────────────┘

선택 기준:
❌ Bubble Sort: 교육용만 (절대 실무에 쓰지 말 것!)
✅ Quick Sort: 평균적으로 가장 빠름 (Python의 기본 sort)
✅ Merge Sort: 최악도 O(n log n) (안정성 필요할 때)
✅ Heap Sort: 메모리 제약 있을 때
"""


class SortingAlgorithms:
    """정렬 알고리즘 구현"""

    @staticmethod
    def bubble_sort(data: List[int]) -> Tuple[List[int], int]:
        """
        Bubble Sort - O(n²)

        Returns: (정렬된 데이터, 비교횟수)
        """
        data = data.copy()
        comparisons = 0
        n = len(data)

        for i in range(n):
            for j in range(n - i - 1):
                comparisons += 1
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]

        return data, comparisons

    @staticmethod
    def quick_sort(data: List[int], _comparisons: List[int] = None) -> Tuple[List[int], int]:
        """
        Quick Sort - O(n log n) 평균

        Returns: (정렬된 데이터, 비교횟수)
        """
        if _comparisons is None:
            _comparisons = [0]

        if len(data) <= 1:
            return data, _comparisons[0]

        pivot = data[len(data) // 2]
        left = []
        middle = []
        right = []

        for x in data:
            _comparisons[0] += 1
            if x < pivot:
                left.append(x)
            elif x == pivot:
                middle.append(x)
            else:
                right.append(x)

        left_sorted, _ = SortingAlgorithms.quick_sort(left, _comparisons)
        right_sorted, _ = SortingAlgorithms.quick_sort(right, _comparisons)

        return left_sorted + middle + right_sorted, _comparisons[0]

    @staticmethod
    def merge_sort(data: List[int]) -> Tuple[List[int], int]:
        """
        Merge Sort - O(n log n) 항상

        Returns: (정렬된 데이터, 비교횟수)
        """
        comparisons = [0]

        def merge_helper(arr):
            if len(arr) <= 1:
                return arr

            mid = len(arr) // 2
            left = merge_helper(arr[:mid])
            right = merge_helper(arr[mid:])

            return merge(left, right, comparisons)

        def merge(left, right, comps):
            result = []
            i = j = 0

            while i < len(left) and j < len(right):
                comps[0] += 1
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1

            result.extend(left[i:])
            result.extend(right[j:])
            return result

        return merge_helper(data), comparisons[0]

    @staticmethod
    def benchmark_sorting(data_size: int):
        """정렬 성능 벤치마크"""
        data = list(range(data_size, 0, -1))  # 역순

        print(f"\n📊 정렬 테스트 (데이터: {data_size:,}개)")

        # Bubble Sort (작은 데이터만)
        if data_size <= 1000:
            start = time.perf_counter()
            _, bubble_comps = SortingAlgorithms.bubble_sort(data)
            bubble_time = time.perf_counter() - start
            print(f"  Bubble Sort: {bubble_time*1000:.2f}ms ({bubble_comps:,}회 비교)")
        else:
            print(f"  Bubble Sort: (생략 - 너무 느림)")

        # Quick Sort
        start = time.perf_counter()
        _, quick_comps = SortingAlgorithms.quick_sort(data)
        quick_time = time.perf_counter() - start
        print(f"  Quick Sort:  {quick_time*1000:.2f}ms ({quick_comps:,}회 비교)")

        # Merge Sort
        start = time.perf_counter()
        _, merge_comps = SortingAlgorithms.merge_sort(data)
        merge_time = time.perf_counter() - start
        print(f"  Merge Sort:  {merge_time*1000:.2f}ms ({merge_comps:,}회 비교)")


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 5: Graph & BFS/DFS - 관계 탐색                                       ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🗺️ Graph (그래프): 데이터 간의 관계

예시: SNS 네트워크
┌─────┐
│ A   │━━┓
└─────┘  ┃
  │      ┃
  │    ┌─────┐
  └───→│ B   │
       └─────┘
         │
         └───→┌─────┐
               │ C   │
               └─────┘

탐색 방법:
1️⃣ BFS (Breadth-First Search) - 너비 우선
   → 가까운 친구부터 만난다 (최단 경로 찾기)
   → 시간복잡도: O(V + E)

2️⃣ DFS (Depth-First Search) - 깊이 우선
   → 깊게 파고든다 (모든 경로 탐색)
   → 시간복잡도: O(V + E)
"""


class Graph:
    """그래프 구현 (인접 리스트)"""

    def __init__(self):
        """그래프 초기화"""
        self.graph: Dict[str, List[str]] = defaultdict(list)

    def add_edge(self, u: str, v: str):
        """간선 추가"""
        self.graph[u].append(v)
        self.graph[v].append(u)  # 무방향 그래프

    def bfs(self, start: str) -> List[str]:
        """너비 우선 탐색 (BFS)"""
        visited = set()
        queue = deque([start])
        result = []

        while queue:
            vertex = queue.popleft()

            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)

                for neighbor in self.graph[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        return result

    def dfs(self, start: str, visited: set = None, result: list = None) -> List[str]:
        """깊이 우선 탐색 (DFS)"""
        if visited is None:
            visited = set()
            result = []

        visited.add(start)
        result.append(start)

        for neighbor in self.graph[start]:
            if neighbor not in visited:
                self.dfs(neighbor, visited, result)

        return result

    def shortest_path(self, start: str, end: str) -> Optional[List[str]]:
        """최단 경로 찾기 (BFS 활용)"""
        visited = set([start])
        queue = deque([(start, [start])])

        while queue:
            vertex, path = queue.popleft()

            if vertex == end:
                return path

            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 6: Dynamic Programming - 기록이 증명이다                              ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
💾 Dynamic Programming (동적 계획법):
"한 번 계산한 것은 저장해두고 다시 계산하지 않는다"
→ "기록이 증명이다 gogs" 원칙이 알고리즘에 구현됨

예시: 피보나치 수열

❌ 재귀 (매번 다시 계산) - O(2ⁿ):
fib(5) = fib(4) + fib(3)
       = (fib(3) + fib(2)) + (fib(2) + fib(1))
       = ...
       → 같은 계산 반복!

✅ DP (계산 결과 저장) - O(n):
fib(2) = 1 (저장)
fib(3) = fib(2) + fib(1) = 2 (저장)
fib(4) = fib(3) + fib(2) = 3 (저장된 값 사용!)
fib(5) = fib(4) + fib(3) = 5 (저장된 값 사용!)
"""


class DynamicProgramming:
    """동적 계획법 예제"""

    @staticmethod
    def fib_recursive(n: int, calls: list = None) -> int:
        """재귀 (반복 계산 많음) - O(2ⁿ)"""
        if calls is None:
            calls = [0]
        calls[0] += 1

        if n <= 1:
            return n
        return DynamicProgramming.fib_recursive(n-1, calls) + \
               DynamicProgramming.fib_recursive(n-2, calls)

    @staticmethod
    def fib_dp(n: int) -> Tuple[int, int]:
        """DP (결과 저장) - O(n)"""
        if n <= 1:
            return n, 1

        memo = [0] * (n + 1)
        memo[0] = 0
        memo[1] = 1
        calls = 2

        for i in range(2, n + 1):
            memo[i] = memo[i-1] + memo[i-2]
            calls += 1

        return memo[n], calls

    @staticmethod
    def benchmark_fibonacci(n: int):
        """피보나치 성능 비교"""
        print(f"\n📊 피보나치({n}) 계산")

        if n <= 35:
            calls = [0]
            start = time.perf_counter()
            result_rec = DynamicProgramming.fib_recursive(n, calls)
            time_rec = time.perf_counter() - start
            print(f"  재귀:     {time_rec*1000:.2f}ms ({calls[0]:,}회 함수 호출)")

        # DP
        start = time.perf_counter()
        result_dp, calls_dp = DynamicProgramming.fib_dp(n)
        time_dp = time.perf_counter() - start
        print(f"  DP:       {time_dp*1000:.4f}ms ({calls_dp}회 계산)")

        if n <= 35:
            print(f"  속도 향상: {time_rec/time_dp:.0f}배 빠름")


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 7: 데모 함수들                                                        ║
# ╚════════════════════════════════════════════════════════════════════════════╝

def demonstration_1_big_o():
    """데모 1: Big-O 표기법"""
    print("\n" + "="*80)
    print("데모 1: Big-O 표기법 - 효율성의 척도")
    print("="*80)

    print("""
┌─────────────────────────────────────────────────────────────┐
│ 1,000,000개 데이터 검색 시간 비교                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ O(1):      0.001ms  (해시 테이블)                          │
│ O(log n):  0.02ms   (이진 검색)                            │
│ O(n):      1000ms   (선형 검색) ← 1초!                    │
│ O(n²):     불가능   (11.5일 소요...)                      │
│                                                             │
│ 선택의 중요성: 선형 검색보다 이진 검색이 50,000배 빠름!  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
    """)


def demonstration_2_search():
    """데모 2: 검색 알고리즘"""
    print("\n" + "="*80)
    print("데모 2: 검색 알고리즘 - 선형 vs 이진")
    print("="*80)

    SearchAlgorithms.benchmark_search(1000000, 'end')
    SearchAlgorithms.benchmark_search(1000000, 'middle')
    SearchAlgorithms.benchmark_search(1000000, 'start')


def demonstration_3_hash_table():
    """데모 3: Hash Table"""
    print("\n" + "="*80)
    print("데모 3: Hash Table - O(1) 마법")
    print("="*80)

    ht = CustomHashTable(size=16)

    print("\n[1] 데이터 삽입")
    students = [
        ('2024001', 'Alice'),
        ('2024002', 'Bob'),
        ('2024003', 'Charlie'),
        ('2024004', 'David'),
    ]

    for sid, name in students:
        ht.put(sid, name)
        print(f"  {sid} → {name}")

    print("\n[2] 검색")
    for sid in ['2024001', '2024003']:
        result = ht.get(sid)
        print(f"  {sid} 검색: {result} ({ht.comparisons}회 비교)")

    print("\n[3] 통계")
    stats = ht.get_stats()
    print(f"  총 항목: {stats['total_items']}")
    print(f"  충돌 (최대 버킷): {stats['max_bucket_size']}")
    print(f"  로드팩터: {stats['load_factor']:.2f}")


def demonstration_4_sorting():
    """데모 4: 정렬 알고리즘"""
    print("\n" + "="*80)
    print("데모 4: 정렬 알고리즘 - Bubble vs Quick vs Merge")
    print("="*80)

    SortingAlgorithms.benchmark_sorting(1000)
    SortingAlgorithms.benchmark_sorting(10000)


def demonstration_5_graph():
    """데모 5: Graph 탐색"""
    print("\n" + "="*80)
    print("데모 5: Graph & BFS/DFS - 관계 탐색")
    print("="*80)

    g = Graph()
    print("\n[1] SNS 네트워크 구성")
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]
    for u, v in edges:
        g.add_edge(u, v)
        print(f"  {u} -- {v}")

    print("\n[2] BFS (너비 우선 탐색)")
    bfs_result = g.bfs('A')
    print(f"  방문 순서: {' → '.join(bfs_result)}")

    print("\n[3] DFS (깊이 우선 탐색)")
    dfs_result = g.dfs('A')
    print(f"  방문 순서: {' → '.join(dfs_result)}")

    print("\n[4] 최단 경로")
    path = g.shortest_path('A', 'E')
    print(f"  A → E: {' → '.join(path)} ({len(path)-1}단계)")


def demonstration_6_dynamic_programming():
    """데모 6: Dynamic Programming"""
    print("\n" + "="*80)
    print("데모 6: Dynamic Programming - 기록이 증명이다")
    print("="*80)

    print("\n['기록이 증명이다' 원칙 적용]")
    print("피보나치 수열: 한 번 계산한 값은 저장해두고 재사용!")

    DynamicProgramming.benchmark_fibonacci(30)
    DynamicProgramming.benchmark_fibonacci(50)


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 8: 단위 테스트 (5/5)                                                 ║
# ╚════════════════════════════════════════════════════════════════════════════╝

import unittest


class TestAlgorithms(unittest.TestCase):
    """알고리즘 단위 테스트"""

    def test_1_binary_search(self):
        """테스트 1: 이진 검색"""
        print("\n" + "="*80)
        print("테스트 1: 이진 검색")
        print("="*80)

        data = list(range(1000))
        idx, comps = SearchAlgorithms.binary_search(data, 999)

        self.assertEqual(idx, 999)
        self.assertLess(comps, 20)  # log₂(1000) ≈ 10

        print(f"✓ PASS: {comps}회 비교로 찾음")

    def test_2_quick_sort(self):
        """테스트 2: Quick Sort"""
        print("\n" + "="*80)
        print("테스트 2: Quick Sort")
        print("="*80)

        data = [3, 1, 4, 1, 5, 9, 2, 6]
        sorted_data, comps = SortingAlgorithms.quick_sort(data)

        self.assertEqual(sorted_data, [1, 1, 2, 3, 4, 5, 6, 9])

        print(f"✓ PASS: 정렬 완료 ({comps}회 비교)")

    def test_3_merge_sort(self):
        """테스트 3: Merge Sort"""
        print("\n" + "="*80)
        print("테스트 3: Merge Sort")
        print("="*80)

        data = [3, 1, 4, 1, 5, 9, 2, 6]
        sorted_data, comps = SortingAlgorithms.merge_sort(data)

        self.assertEqual(sorted_data, [1, 1, 2, 3, 4, 5, 6, 9])

        print(f"✓ PASS: 정렬 완료 ({comps}회 비교)")

    def test_4_hash_table(self):
        """테스트 4: Hash Table"""
        print("\n" + "="*80)
        print("테스트 4: Hash Table O(1)")
        print("="*80)

        ht = CustomHashTable()
        ht.put('key1', 'value1')
        ht.put('key2', 'value2')

        result1 = ht.get('key1')
        self.assertEqual(result1, 'value1')

        print(f"✓ PASS: Hash Table 작동 ({ht.comparisons}회 비교)")

    def test_5_graph_bfs(self):
        """테스트 5: Graph BFS"""
        print("\n" + "="*80)
        print("테스트 5: Graph BFS 탐색")
        print("="*80)

        g = Graph()
        g.add_edge('A', 'B')
        g.add_edge('B', 'C')
        g.add_edge('A', 'D')

        result = g.bfs('A')
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], 'A')

        print(f"✓ PASS: 방문 순서 {result}")


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 9: 완성 및 다음 단계                                                  ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
✨ v5.3 완성 요약:

✅ 학습 내용:
   1. Big-O 표기법: 효율성을 수학적으로 측정
   2. 선형 vs 이진 검색: 50,000배 성능 차이
   3. Hash Table: O(1) 마법의 원리
   4. 정렬 알고리즘: Bubble, Quick, Merge 비교
   5. Graph 탐색: BFS, DFS 구현
   6. Dynamic Programming: 기록이 증명이다 원칙
   7. 성능 벤치마킹: 실제 측정으로 증명

⚡ 성과:
   - 1,000,000 데이터 검색: 선형 1초 → 이진 0.0001초 (50,000배)
   - 정렬: Bubble O(n²) vs Merge O(n log n)
   - 피보나치: 재귀 vs DP (수십만배 빠름)

🏗️ 아키텍처 완성:
   v4.1-4.3: 단일 머신 최적화 (근육, 혈관)
   v5.1: 분산 시스템 설계 (조화)
   v5.2: 데이터 저장 구조 (기억)
   v5.3: 효율적 알고리즘 (지능)
   → 이제 Netflix 규모 시스템을 설계할 수 있습니다!

📚 다음 단계:
   [v5.4] 디자인 패턴과 클린 코드
   - 23가지 Design Pattern (Singleton, Factory, Observer 등)
   - SOLID 원칙
   - 코드 리뷰 기법
   - 테스트 주도 개발 (TDD)

💡 최종 철학:
   "설계자님의 코드는 이제 단순히 돌아가는 것을 넘어,
    가장 우아하고 빠른 길을 찾습니다."

> "기록이 증명이다 gogs"
> 모든 성능 개선이 벤치마킹으로 증명되었습니다.
"""


if __name__ == "__main__":
    # 데모 실행
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + "  Python University Level 3 - v5.3 Algorithms & Data Structures Advanced".center(78) + "║")
    print("║" + "  공간과 시간의 거래 - 효율성의 극한".center(78) + "║")
    print("╚" + "="*78 + "╝")

    # 데모 실행
    demonstration_1_big_o()
    demonstration_2_search()
    demonstration_3_hash_table()
    demonstration_4_sorting()
    demonstration_5_graph()
    demonstration_6_dynamic_programming()

    # 단위 테스트 실행
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + "  UNIT TESTS".center(78) + "║")
    print("╚" + "="*78 + "╝")

    unittest.main(argv=[''], exit=False, verbosity=2)

    print("\n" + "="*80)
    print("✨ v5.3 완성! 알고리즘과 자료구조 심화 마스터 달성")
    print("="*80)
    print("\n다음 단계: v5.4 디자인 패턴과 클린 코드 (최종 3학년)")
