#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              【 v8.2: 데이터 레이크 & 분산 병렬 처리 】                      ║
║                 Python PhD 박사 과정 — 두 번째 연구                          ║
║                                                                              ║
║                   "빅데이터의 시대에 MapReduce 철학을 구현하라"              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

【 핵심 개념 】

데이터 레이크 (Data Lake) 란?
─────────────────────────────────────────────────────────
모든 형태의 데이터를 원본 상태에서 중앙 저장소에 모으는 아키텍처:
  1. 원본 데이터 보존 (Raw Data)
  2. 분산 저장 (Distributed Storage)
  3. 병렬 처리 (Parallel Processing)
  4. 스케일 무한대 (Unlimited Scale)

MapReduce 철학
─────────────────────────────────────────────────────────
"큰 문제를 작은 조각으로 나누고, 각각 처리한 후, 결과를 모아라"

  1. Map 단계: 각 데이터 청크를 독립적으로 변환
  2. Shuffle 단계: 같은 키끼리 그룹핑
  3. Reduce 단계: 그룹별로 최종 집계

예: 단어 빈도수 계산
  Map:    "the fox jumps" → [("the", 1), ("fox", 1), ("jumps", 1)]
  Shuffle: {"the": [1,1,1], "fox": [1,1], "jumps": [1]}
  Reduce: {"the": 3, "fox": 2, "jumps": 1}

【 시스템 구성 】

1. DataPartitioner        — 데이터를 파티션으로 분할
2. GogsDataLakeEngine     — 기본 분산 처리 엔진
3. MapReduceExecutor      — MapReduce 파이프라인
4. FaultToleranceManager  — 실패 시 재시도 & 재할당
5. DataLocalityOptimizer  — 네트워크 비용 최소화
6. SkewHandler            — 데이터 불균형 처리
7. DataLakeOrchestrator   — 전체 시스템 조율

【 분산 처리의 도전】

1. 데이터 스큐 (Data Skew)
   - 문제: 일부 워커가 다량의 데이터 처리 → 병목
   - 해결: 핫키 탐지 & 재분산

2. 네트워크 오버헤드
   - 문제: 파티션이 다른 노드에 있으면 원격 읽기 3배 비용
   - 해결: 데이터 위치 인식 스케줄링

3. 부분 장애 (Partial Failure)
   - 문제: 워커 중 일부가 실패 → 전체 작업 실패
   - 해결: 자동 재시도 & 재할당

【 파이썬 철학 】

"멀티프로세싱은 GIL을 무너뜨리고, 병렬성을 되찾는다.
 하지만 프로세스 간 통신(IPC)의 직렬화 비용을 반드시 고려하라.
 따라서 각 청크는 충분히 커야 하고, 워커 함수는 반드시 모듈 레벨에 정의되어야 한다."
"""

# ═══════════════════════════════════════════════════════════════════════════
# PART 0: 공용 데이터 클래스 & Enum
# ═══════════════════════════════════════════════════════════════════════════

import multiprocessing as mp
import statistics
import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Callable
from enum import Enum
from collections import defaultdict


class PartitionStrategy(Enum):
    """파티셔닝 전략"""
    RANGE = "RANGE"          # 범위 기반
    HASH = "HASH"            # 해시 기반


class WorkerStatus(Enum):
    """워커 상태"""
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    RETRYING = "RETRYING"


class SkewLevel(Enum):
    """데이터 스큐 수준"""
    BALANCED = "BALANCED"      # std < 10%
    MODERATE = "MODERATE"      # std 10~30%
    SEVERE = "SEVERE"          # std > 30%


@dataclass
class Partition:
    """데이터 파티션"""
    partition_id: int
    data: List[Any]
    strategy: PartitionStrategy
    node_id: int
    size: int = 0

    def __post_init__(self):
        if self.size == 0:
            self.size = len(self.data)


@dataclass
class WorkerResult:
    """워커 결과"""
    worker_id: int
    partition_id: int
    result: Any
    status: WorkerStatus
    attempts: int
    duration_ms: float


@dataclass
class MapReduceResult:
    """MapReduce 결과"""
    total_items: int
    unique_keys: int
    final_output: Dict[Any, Any]
    map_time_ms: float = 0.0
    shuffle_time_ms: float = 0.0
    reduce_time_ms: float = 0.0


@dataclass
class DataNode:
    """데이터 노드"""
    node_id: int
    partitions: List[int] = field(default_factory=list)
    cpu_cores: int = 4
    network_cost: float = 1.0


@dataclass
class SkewReport:
    """스큐 분석 보고서"""
    partition_sizes: List[int]
    mean_size: float
    std_dev: float
    skew_ratio: float
    level: SkewLevel
    hot_keys: List[Tuple[Any, int]] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════
# 모듈 레벨 워커 함수 (pickle 가능 — multiprocessing 필수)
# ═══════════════════════════════════════════════════════════════════════════

def data_processor_worker(data_chunk: List[int]) -> float:
    """제곱합 계산 워커 (사용자 제공 코드)"""
    return sum(val ** 2 for val in data_chunk)


def word_count_mapper(text_chunk: str) -> List[Tuple[str, int]]:
    """텍스트 청크를 단어-카운트 쌍으로 변환"""
    words = text_chunk.lower().split()
    return [(word, 1) for word in words]


def word_count_reducer(key: str, values: List[int]) -> int:
    """단어별 카운트 합산"""
    return sum(values)


def square_sum_mapper(data_chunk: List[int]) -> List[Tuple[str, float]]:
    """수치 데이터를 제곱합으로 변환"""
    total = sum(val ** 2 for val in data_chunk)
    return [("sum", total)]


# ═══════════════════════════════════════════════════════════════════════════
# PART 1: DataPartitioner — 데이터 분할
# ═══════════════════════════════════════════════════════════════════════════

class RangePartitioner:
    """범위 기반 파티셔너: 데이터를 N개의 균등한 청크로 분할"""

    def __init__(self, num_partitions: int = 4):
        self.num_partitions = num_partitions

    def partition(self, data: List[Any]) -> List[Partition]:
        """데이터를 균등 크기의 파티션으로 분할"""
        chunk_size = -(-len(data) // self.num_partitions)  # ceil 나눗셈
        partitions = []

        for i in range(self.num_partitions):
            start = i * chunk_size
            end = min(start + chunk_size, len(data))
            chunk = data[start:end]

            partitions.append(
                Partition(
                    partition_id=i,
                    data=chunk,
                    strategy=PartitionStrategy.RANGE,
                    node_id=i % 4,
                )
            )

        return partitions

    def get_stats(self) -> Dict[str, float]:
        """파티션 통계"""
        return {"strategy": "RANGE"}


class HashPartitioner:
    """해시 기반 파티셔너: hash(item) % N으로 분산"""

    def __init__(self, num_partitions: int = 4):
        self.num_partitions = num_partitions

    def partition(self, data: List[Any]) -> List[Partition]:
        """데이터를 해시 기반으로 분산"""
        buckets: Dict[int, List[Any]] = defaultdict(list)

        for item in data:
            bucket_id = hash(str(item)) % self.num_partitions
            buckets[bucket_id].append(item)

        partitions = []
        for i in range(self.num_partitions):
            partitions.append(
                Partition(
                    partition_id=i,
                    data=buckets.get(i, []),
                    strategy=PartitionStrategy.HASH,
                    node_id=i % 4,
                )
            )

        return partitions

    def get_stats(self) -> Dict[str, float]:
        """파티션 통계"""
        return {"strategy": "HASH"}


# ═══════════════════════════════════════════════════════════════════════════
# PART 2: GogsDataLakeEngine — 기본 분산 처리 엔진
# ═══════════════════════════════════════════════════════════════════════════

class GogsDataLakeEngine:
    """대규모 데이터 분산 처리 엔진"""

    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers

    def run_distributed_analysis(self, massive_data: List[int]) -> Dict[str, Any]:
        """분산 병렬 처리로 제곱합 계산"""
        chunk_size = len(massive_data) // self.num_workers
        results = []

        with mp.Pool(self.num_workers) as pool:
            chunks = [
                massive_data[i * chunk_size : (i + 1) * chunk_size]
                for i in range(self.num_workers)
            ]
            results = pool.map(data_processor_worker, chunks)

        return {"total_square_sum": sum(results), "num_workers": self.num_workers}

    def run_with_timing(self, data: List[int]) -> Dict[str, Any]:
        """직렬 vs 병렬 타이밍 비교"""
        # 직렬 처리
        start = time.time()
        serial_result = sum(val ** 2 for val in data)
        serial_time = (time.time() - start) * 1000

        # 병렬 처리
        start = time.time()
        parallel_result = self.run_distributed_analysis(data)
        parallel_time = (time.time() - start) * 1000

        speedup = serial_time / parallel_time if parallel_time > 0 else 0

        return {
            "serial_result": serial_result,
            "parallel_result": parallel_result["total_square_sum"],
            "serial_time_ms": serial_time,
            "parallel_time_ms": parallel_time,
            "speedup": speedup,
        }


# ═══════════════════════════════════════════════════════════════════════════
# PART 3: MapReduceExecutor — MapReduce 파이프라인
# ═══════════════════════════════════════════════════════════════════════════

class MapReduceExecutor:
    """MapReduce 패턴 구현"""

    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers

    def split_into_chunks(self, data: List[Any], num_chunks: int) -> List[Any]:
        """데이터를 N개 청크로 분할 (문자열/리스트 모두 지원)"""
        if isinstance(data, str):
            # 문자열 분할
            chunk_size = max(1, len(data) // num_chunks)
            chunks = []
            for i in range(0, len(data), chunk_size):
                chunks.append(data[i : i + chunk_size])
            return chunks[:num_chunks]
        else:
            # 리스트 분할
            chunk_size = max(1, len(data) // num_chunks)
            chunks = []
            for i in range(0, len(data), chunk_size):
                chunks.append(data[i : i + chunk_size])
            return chunks[:num_chunks]

    def map_phase(
        self, data: List[Any], map_func: Callable
    ) -> List[Tuple[Any, Any]]:
        """Map 단계: 데이터 청크를 변환"""
        start = time.time()
        chunks = self.split_into_chunks(data, self.num_workers)

        with mp.Pool(self.num_workers) as pool:
            chunk_results = pool.map(map_func, chunks)

        # 모든 결과를 평탄화
        all_mapped = [
            item for chunk_result in chunk_results for item in chunk_result
        ]
        map_time = (time.time() - start) * 1000
        return all_mapped, map_time

    def shuffle_phase(
        self, mapped_data: List[Tuple[Any, Any]]
    ) -> Dict[Any, List[Any]]:
        """Shuffle 단계: 같은 키끼리 그룹핑"""
        start = time.time()
        shuffled = defaultdict(list)
        for key, value in mapped_data:
            shuffled[key].append(value)
        shuffle_time = (time.time() - start) * 1000
        return dict(shuffled), shuffle_time

    def reduce_phase(
        self, shuffled: Dict[Any, List[Any]], reduce_func: Callable
    ) -> Dict[Any, Any]:
        """Reduce 단계: 그룹별 집계"""
        start = time.time()
        result = {}
        for key, values in shuffled.items():
            result[key] = reduce_func(key, values)
        reduce_time = (time.time() - start) * 1000
        return result, reduce_time

    def execute(
        self, data: List[Any], map_func: Callable, reduce_func: Callable
    ) -> MapReduceResult:
        """전체 MapReduce 파이프라인 실행"""
        # Map
        mapped_data, map_time = self.map_phase(data, map_func)

        # Shuffle
        shuffled, shuffle_time = self.shuffle_phase(mapped_data)

        # Reduce
        final_output, reduce_time = self.reduce_phase(shuffled, reduce_func)

        return MapReduceResult(
            total_items=len(data),
            unique_keys=len(final_output),
            final_output=final_output,
            map_time_ms=map_time,
            shuffle_time_ms=shuffle_time,
            reduce_time_ms=reduce_time,
        )


# ═══════════════════════════════════════════════════════════════════════════
# PART 4: FaultToleranceManager — 실패 처리 & 재시도
# ═══════════════════════════════════════════════════════════════════════════

class FaultToleranceManager:
    """장애 허용 분산 처리"""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.worker_failures: Dict[int, int] = defaultdict(int)

    def execute_with_retry(
        self, func: Callable, chunk: List[Any], partition_id: int, worker_id: int
    ) -> WorkerResult:
        """최대 3회까지 재시도하며 작업 실행"""
        for attempt in range(self.max_retries):
            try:
                start = time.time()
                result = func(chunk)
                duration = (time.time() - start) * 1000

                return WorkerResult(
                    worker_id=worker_id,
                    partition_id=partition_id,
                    result=result,
                    status=WorkerStatus.RUNNING,
                    attempts=attempt + 1,
                    duration_ms=duration,
                )
            except Exception as e:
                self.worker_failures[worker_id] += 1
                if attempt == self.max_retries - 1:
                    return WorkerResult(
                        worker_id=worker_id,
                        partition_id=partition_id,
                        result=None,
                        status=WorkerStatus.FAILED,
                        attempts=attempt + 1,
                        duration_ms=0.0,
                    )

    def reassign_partition(
        self, partition: Partition, available_workers: List[int]
    ) -> int:
        """실패한 파티션을 다른 워커에 재할당"""
        best_worker = min(available_workers, key=lambda w: self.worker_failures[w])
        return best_worker

    def run_with_fault_tolerance(
        self, data: List[int], func: Callable, num_workers: int
    ) -> Dict[str, Any]:
        """장애 허용 분산 실행"""
        chunk_size = len(data) // num_workers
        results = []

        for i in range(num_workers):
            chunk = data[i * chunk_size : (i + 1) * chunk_size]
            result = self.execute_with_retry(func, chunk, i, i)
            results.append(result)

        successful = sum(1 for r in results if r.status == WorkerStatus.RUNNING)
        return {
            "successful": successful,
            "failed": num_workers - successful,
            "total_failures": sum(self.worker_failures.values()),
        }


# ═══════════════════════════════════════════════════════════════════════════
# PART 5: DataLocalityOptimizer — 데이터 위치 최적화
# ═══════════════════════════════════════════════════════════════════════════

class DataLocalityOptimizer:
    """데이터 위치 인식 스케줄링"""

    def __init__(self):
        self.nodes: Dict[int, DataNode] = {}

    def register_node(self, node: DataNode) -> None:
        """노드 등록"""
        self.nodes[node.node_id] = node

    def assign_partitions(self, partitions: List[Partition]) -> None:
        """파티션을 노드에 할당"""
        for partition in partitions:
            if partition.node_id in self.nodes:
                self.nodes[partition.node_id].partitions.append(partition.partition_id)

    def calculate_processing_cost(
        self, partition_id: int, target_node_id: int
    ) -> float:
        """처리 비용 계산: 로컬(1.0x) vs 원격(3.0x)"""
        for node in self.nodes.values():
            if partition_id in node.partitions:
                if node.node_id == target_node_id:
                    return 1.0  # 로컬
                else:
                    return 3.0  # 원격
        return 1.0

    def find_optimal_node(self, partition_id: int) -> int:
        """파티션을 처리할 최적 노드 선택"""
        for node in self.nodes.values():
            if partition_id in node.partitions:
                return node.node_id
        return 0  # 기본값

    def optimize_assignments(self, partitions: List[Partition]) -> Dict[int, float]:
        """전체 파티션 최적 배치 및 비용 계산"""
        costs = {}
        for partition in partitions:
            optimal_node = self.find_optimal_node(partition.partition_id)
            cost = self.calculate_processing_cost(partition.partition_id, optimal_node)
            costs[partition.partition_id] = cost
        return costs


# ═══════════════════════════════════════════════════════════════════════════
# PART 6: SkewHandler — 데이터 스큐 처리
# ═══════════════════════════════════════════════════════════════════════════

class SkewHandler:
    """데이터 불균형 탐지 및 재분산"""

    def detect_skew(self, partitions: List[Partition]) -> SkewReport:
        """파티션 크기 기반 스큐 탐지"""
        sizes = [p.size for p in partitions]
        mean_size = statistics.mean(sizes) if sizes else 0
        std_dev = statistics.stdev(sizes) if len(sizes) > 1 else 0

        skew_ratio = (std_dev / mean_size) if mean_size > 0 else 0

        if skew_ratio < 0.1:
            level = SkewLevel.BALANCED
        elif skew_ratio < 0.3:
            level = SkewLevel.MODERATE
        else:
            level = SkewLevel.SEVERE

        return SkewReport(
            partition_sizes=sizes,
            mean_size=mean_size,
            std_dev=std_dev,
            skew_ratio=skew_ratio,
            level=level,
        )

    def find_hot_keys(
        self, data: List[Any], top_n: int = 3
    ) -> List[Tuple[Any, int]]:
        """빈도 상위 N키 탐지"""
        from collections import Counter

        counter = Counter(data)
        return counter.most_common(top_n)

    def rebalance(self, partitions: List[Partition]) -> List[Partition]:
        """큰 파티션을 분할하여 재분산"""
        rebalanced = []
        target_size = max(p.size for p in partitions) * 1.5

        for partition in partitions:
            if partition.size > target_size:
                # 분할
                mid = len(partition.data) // 2
                p1 = Partition(
                    partition_id=partition.partition_id,
                    data=partition.data[:mid],
                    strategy=partition.strategy,
                    node_id=partition.node_id,
                )
                p2 = Partition(
                    partition_id=partition.partition_id + 1000,
                    data=partition.data[mid:],
                    strategy=partition.strategy,
                    node_id=(partition.node_id + 1) % 4,
                )
                rebalanced.extend([p1, p2])
            else:
                rebalanced.append(partition)

        return rebalanced

    def isolate_hot_key(
        self, partitions: List[Partition], hot_key: Any
    ) -> List[Partition]:
        """핫키를 별도 파티션으로 격리"""
        isolated = []
        hot_data = []

        for partition in partitions:
            non_hot = []
            for item in partition.data:
                if item == hot_key:
                    hot_data.append(item)
                else:
                    non_hot.append(item)

            if non_hot:
                isolated.append(
                    Partition(
                        partition_id=partition.partition_id,
                        data=non_hot,
                        strategy=partition.strategy,
                        node_id=partition.node_id,
                    )
                )

        if hot_data:
            isolated.append(
                Partition(
                    partition_id=9999,
                    data=hot_data,
                    strategy=PartitionStrategy.RANGE,
                    node_id=0,
                )
            )

        return isolated


# ═══════════════════════════════════════════════════════════════════════════
# PART 7: DataLakeOrchestrator — 전체 시스템 조율
# ═══════════════════════════════════════════════════════════════════════════

class DataLakeOrchestrator:
    """분산 데이터 레이크 전체 조율"""

    def __init__(self, num_workers: int = 4):
        self.data_lake_engine = GogsDataLakeEngine(num_workers)
        self.map_reduce_executor = MapReduceExecutor(num_workers)
        self.fault_tolerance = FaultToleranceManager()
        self.locality_optimizer = DataLocalityOptimizer()
        self.skew_handler = SkewHandler()
        self.num_workers = num_workers

    def run_full_pipeline(self, data: List[Any]) -> Dict[str, Any]:
        """전체 분산 처리 파이프라인"""
        # 1. 파티셔닝
        range_partitioner = RangePartitioner(self.num_workers)
        hash_partitioner = HashPartitioner(self.num_workers)

        range_partitions = range_partitioner.partition(data)
        hash_partitions = hash_partitioner.partition(data)

        # 2. 스큐 탐지
        skew_report = self.skew_handler.detect_skew(range_partitions)

        # 3. 필요하면 재분산
        if skew_report.level == SkewLevel.SEVERE:
            partitions = self.skew_handler.rebalance(range_partitions)
        else:
            partitions = range_partitions

        # 4. 데이터 위치 최적화
        for i in range(4):
            self.locality_optimizer.register_node(DataNode(node_id=i))
        self.locality_optimizer.assign_partitions(partitions)

        # 5. 장애 허용 실행
        ft_result = self.fault_tolerance.run_with_fault_tolerance(
            data, data_processor_worker, self.num_workers
        )

        return {
            "total_items": len(data),
            "num_partitions": len(partitions),
            "skew_report": {
                "level": skew_report.level.value,
                "std_dev": skew_report.std_dev,
                "skew_ratio": skew_report.skew_ratio,
            },
            "fault_tolerance": ft_result,
        }

    def benchmark(self, data: List[Any], iterations: int = 3) -> Dict[str, Any]:
        """직렬 vs 병렬 속도 비교"""
        serial_times = []
        parallel_times = []

        for _ in range(iterations):
            start = time.time()
            serial_result = sum(val ** 2 for val in data)
            serial_times.append((time.time() - start) * 1000)

            start = time.time()
            parallel_result = self.data_lake_engine.run_distributed_analysis(data)
            parallel_times.append((time.time() - start) * 1000)

        avg_serial = statistics.mean(serial_times)
        avg_parallel = statistics.mean(parallel_times)
        speedup = avg_serial / avg_parallel if avg_parallel > 0 else 0

        return {
            "serial_avg_ms": avg_serial,
            "parallel_avg_ms": avg_parallel,
            "speedup": speedup,
        }


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1~7: 데모 & 철학
# ═══════════════════════════════════════════════════════════════════════════


def main():
    """메인 프로그램"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║   【 v8.2: 데이터 레이크 & 분산 병렬 처리 】                ║")
    print("║   Python PhD 박사 과정 2 — 두 번째 연구                     ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    # SECTION 1: 파티셔닝 비교
    print("[SECTION 1] 파티셔닝 전략 비교")
    test_data = list(range(1000))
    range_part = RangePartitioner(4)
    hash_part = HashPartitioner(4)

    range_partitions = range_part.partition(test_data)
    hash_partitions = hash_part.partition(test_data)

    range_sizes = [p.size for p in range_partitions]
    hash_sizes = [p.size for p in hash_partitions]

    range_std = statistics.stdev(range_sizes)
    hash_std = statistics.stdev(hash_sizes)

    print(f"Range: {range_sizes} std={range_std:.2f}")
    print(f"Hash: {hash_sizes} std={hash_std:.2f}\n")

    # SECTION 2: 병렬 처리 성능
    print("[SECTION 2] 병렬 처리 성능")
    large_data = list(range(100000))
    engine = GogsDataLakeEngine(4)
    timing = engine.run_with_timing(large_data)

    print(
        f"{len(large_data):,} 항목 → 직렬 {timing['serial_time_ms']:.1f}ms / "
        f"병렬 {timing['parallel_time_ms']:.1f}ms = {timing['speedup']:.1f}x\n"
    )

    # SECTION 3: MapReduce 단어 빈도
    print("[SECTION 3] MapReduce: 단어 빈도 계산")
    text_data = (
        "the quick brown fox jumps over the lazy dog "
        "the fox is quick and brown"
    )

    executor = MapReduceExecutor(3)
    mr_result = executor.execute(text_data, word_count_mapper, word_count_reducer)
    top_words = sorted(mr_result.final_output.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"단어빈도: {dict(top_words)}\n")

    # SECTION 4: 스큐 탐지
    print("[SECTION 4] 데이터 스큐 탐지 및 재분산")
    skew_handler = SkewHandler()
    unbalanced = [
        Partition(0, list(range(100)), PartitionStrategy.RANGE, 0),
        Partition(1, list(range(20)), PartitionStrategy.RANGE, 1),
        Partition(2, list(range(500)), PartitionStrategy.RANGE, 2),
        Partition(3, list(range(30)), PartitionStrategy.RANGE, 3),
    ]

    skew_before = skew_handler.detect_skew(unbalanced)
    print(f"재분산 전: {skew_before.level.value}")

    rebalanced = skew_handler.rebalance(unbalanced)
    skew_after = skew_handler.detect_skew(rebalanced)
    print(f"재분산 후: {skew_after.level.value}\n")

    # SECTION 5: 장애 허용
    print("[SECTION 5] 장애 허용 처리")
    ft_manager = FaultToleranceManager()
    data_with_errors = list(range(10000))
    ft_result = ft_manager.run_with_fault_tolerance(
        data_with_errors, data_processor_worker, 4
    )
    print(f"성공: {ft_result['successful']}/4, 실패: {ft_result['failed']}/4\n")

    # SECTION 6: 전체 파이프라인 & 벤치마크
    print("[SECTION 6] 전체 파이프라인 & 벤치마크")
    orchestrator = DataLakeOrchestrator(4)
    huge_data = list(range(50000))

    pipeline_result = orchestrator.run_full_pipeline(huge_data)
    benchmark_result = orchestrator.benchmark(huge_data)

    print(f"가속배율: {benchmark_result['speedup']:.2f}x")
    print(f"스큐레벨: {pipeline_result['skew_report']['level']}\n")

    # SECTION 7: 철학
    print("[SECTION 7] 파이썬 분산 처리 철학")
    print("""
    "멀티프로세싱은 Python GIL을 무너뜨리고 진정한 병렬성을 제공한다.
     하지만 프로세스 간 통신(IPC)의 직렬화 비용을 반드시 고려하라.

     따라서:
     1. 각 청크는 충분히 커야 한다 (최소 1,000 항목)
     2. 워커 함수는 반드시 모듈 레벨에 정의되어야 한다 (pickle 가능)
     3. 데이터 스큐는 전체 시스템의 병목이다 (Amdahl 법칙)
     4. 데이터 위치 인식 스케줄링은 필수다 (로컬: 1.0x, 원격: 3.0x)

     v8.2는 데이터 레이크의 핵심을 증명한다:
     '작은 문제로 나누고, 병렬로 풀고, 결과를 모아라'

     이것이 MapReduce 철학이고, 이것이 빅데이터 시대의 기본이다."
    """)

    print("\n저장 필수 너는 기록이 증명이다 gogs\n")


if __name__ == "__main__":
    main()
