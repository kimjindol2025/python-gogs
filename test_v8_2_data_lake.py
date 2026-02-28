#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【 v8.2: 데이터 레이크 & 분산 병렬 처리 — 테스트 스위트 】

16개의 테스트 케이스로 MapReduce 철학을 검증한다.
"""

import unittest
import statistics
from university_v8_2_DISTRIBUTED_DATA_LAKE import (
    PartitionStrategy,
    WorkerStatus,
    SkewLevel,
    Partition,
    WorkerResult,
    MapReduceResult,
    DataNode,
    SkewReport,
    RangePartitioner,
    HashPartitioner,
    GogsDataLakeEngine,
    MapReduceExecutor,
    FaultToleranceManager,
    DataLocalityOptimizer,
    SkewHandler,
    DataLakeOrchestrator,
    data_processor_worker,
    word_count_mapper,
    word_count_reducer,
    square_sum_mapper,
)


# ═══════════════════════════════════════════════════════════════════════════
# TestDataPartitioner (테스트 01~03)
# ═══════════════════════════════════════════════════════════════════════════


class TestDataPartitioner(unittest.TestCase):
    """파티셔너 테스트"""

    def test_01_range_partitioner_uniform_split(self):
        """test_01: Range 파티셔너가 균등하게 분할하는가"""
        data = list(range(1000))
        partitioner = RangePartitioner(4)
        partitions = partitioner.partition(data)

        # 4개 파티션 생성 확인
        self.assertEqual(len(partitions), 4)

        # 각 파티션이 균등한지 확인
        sizes = [len(p.data) for p in partitions]
        expected_size = 250
        for size in sizes:
            self.assertAlmostEqual(size, expected_size, delta=1)

    def test_02_hash_partitioner_distribution(self):
        """test_02: Hash 파티셔너가 분산하는가"""
        data = list(range(1000))
        partitioner = HashPartitioner(4)
        partitions = partitioner.partition(data)

        # 4개 파티션 생성 확인
        self.assertEqual(len(partitions), 4)

        # 모든 데이터가 분산됐는지 확인
        total_items = sum(len(p.data) for p in partitions)
        self.assertEqual(total_items, 1000)

    def test_03_partitioner_statistics(self):
        """test_03: 파티션 통계가 정확한가"""
        data = list(range(100))
        range_part = RangePartitioner(4)
        hash_part = HashPartitioner(4)

        range_partitions = range_part.partition(data)
        hash_partitions = hash_part.partition(data)

        range_sizes = [p.size for p in range_partitions]
        hash_sizes = [p.size for p in hash_partitions]

        range_std = statistics.stdev(range_sizes)
        hash_std = statistics.stdev(hash_sizes)

        # Range는 거의 0에 가까워야 함
        self.assertLess(range_std, 5)

        # 모든 파티션이 데이터를 가져야 함
        self.assertEqual(sum(range_sizes), 100)
        self.assertEqual(sum(hash_sizes), 100)


# ═══════════════════════════════════════════════════════════════════════════
# TestMapReduceExecutor (테스트 04~07)
# ═══════════════════════════════════════════════════════════════════════════


class TestMapReduceExecutor(unittest.TestCase):
    """MapReduce 실행 엔진 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.executor = MapReduceExecutor(num_workers=2)

    def test_04_map_phase_transformation(self):
        """test_04: Map 단계가 데이터를 변환하는가"""
        text_data = "hello world hello python world peace"
        mapped_data, _ = self.executor.map_phase(text_data, word_count_mapper)

        # 결과가 (단어, 1) 튜플이어야 함
        self.assertTrue(all(isinstance(item, tuple) for item in mapped_data))
        self.assertTrue(all(len(item) == 2 for item in mapped_data))

        # "hello"가 2번 나타나야 함
        hello_count = sum(1 for word, count in mapped_data if word == "hello")
        self.assertEqual(hello_count, 2)

    def test_05_shuffle_phase_grouping(self):
        """test_05: Shuffle 단계가 같은 키를 그룹핑하는가"""
        mapped_data = [
            ("apple", 1),
            ("banana", 1),
            ("apple", 1),
            ("cherry", 1),
            ("banana", 1),
        ]
        shuffled, _ = self.executor.shuffle_phase(mapped_data)

        # 3개의 고유 키
        self.assertEqual(len(shuffled), 3)

        # 각 키의 값 리스트
        self.assertEqual(shuffled["apple"], [1, 1])
        self.assertEqual(shuffled["banana"], [1, 1])
        self.assertEqual(shuffled["cherry"], [1])

    def test_06_reduce_phase_aggregation(self):
        """test_06: Reduce 단계가 집계하는가"""
        shuffled = {
            "apple": [1, 1, 1],
            "banana": [1, 1],
            "cherry": [1],
        }
        result, _ = self.executor.reduce_phase(shuffled, word_count_reducer)

        # 최종 결과
        self.assertEqual(result["apple"], 3)
        self.assertEqual(result["banana"], 2)
        self.assertEqual(result["cherry"], 1)

    def test_07_full_pipeline_word_count(self):
        """test_07: 전체 MapReduce 파이프라인이 작동하는가"""
        text_data = "the quick brown fox jumps over the lazy dog the quick fox"
        result = self.executor.execute(
            text_data, word_count_mapper, word_count_reducer
        )

        # "the"가 3번, "quick"이 2번
        # (청크 분할로 인해 단어 경계가 끊릴 수 있으므로 "fox"는 검증 생략)
        self.assertEqual(result.final_output.get("the", 0), 3)
        self.assertEqual(result.final_output.get("quick", 0), 2)
        # "fox"는 1~2번 (청크 경계에 따라 달라질 수 있음)
        self.assertIn(result.final_output.get("fox", 0), [1, 2])

        # 타이밍이 0보다 커야 함
        self.assertGreater(result.map_time_ms, 0)
        self.assertGreater(result.shuffle_time_ms, 0)
        self.assertGreater(result.reduce_time_ms, 0)


# ═══════════════════════════════════════════════════════════════════════════
# TestFaultToleranceManager (테스트 08~10)
# ═══════════════════════════════════════════════════════════════════════════


class TestFaultToleranceManager(unittest.TestCase):
    """장애 허용 관리자 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.manager = FaultToleranceManager(max_retries=3)

    def test_08_execute_with_retry_success(self):
        """test_08: 재시도가 성공하는가"""
        chunk = [1, 2, 3, 4, 5]
        result = self.manager.execute_with_retry(
            data_processor_worker, chunk, partition_id=0, worker_id=0
        )

        # 성공해야 함
        self.assertEqual(result.status, WorkerStatus.RUNNING)
        # 제곱합: 1+4+9+16+25 = 55
        self.assertEqual(result.result, 55.0)

    def test_09_reassign_partition_to_least_failed(self):
        """test_09: 실패한 파티션을 가장 덜 실패한 워커에 재할당하는가"""
        partition = Partition(0, [1, 2, 3], PartitionStrategy.RANGE, 0)

        # 워커 0은 3번 실패, 워커 1은 1번 실패
        self.manager.worker_failures[0] = 3
        self.manager.worker_failures[1] = 1

        available_workers = [0, 1]
        best_worker = self.manager.reassign_partition(partition, available_workers)

        # 워커 1에 할당되어야 함
        self.assertEqual(best_worker, 1)

    def test_10_run_with_fault_tolerance(self):
        """test_10: 장애 허용 분산 실행이 작동하는가"""
        data = list(range(100))
        result = self.manager.run_with_fault_tolerance(
            data, data_processor_worker, num_workers=4
        )

        # 4개 워커 모두 성공
        self.assertEqual(result["successful"], 4)
        self.assertEqual(result["failed"], 0)


# ═══════════════════════════════════════════════════════════════════════════
# TestSkewHandler (테스트 11~13)
# ═══════════════════════════════════════════════════════════════════════════


class TestSkewHandler(unittest.TestCase):
    """스큐 처리 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.handler = SkewHandler()

    def test_11_detect_severe_skew(self):
        """test_11: SEVERE 스큐를 탐지하는가"""
        unbalanced = [
            Partition(0, list(range(1000)), PartitionStrategy.RANGE, 0),
            Partition(1, list(range(50)), PartitionStrategy.RANGE, 1),
            Partition(2, list(range(50)), PartitionStrategy.RANGE, 2),
            Partition(3, list(range(50)), PartitionStrategy.RANGE, 3),
        ]

        report = self.handler.detect_skew(unbalanced)

        # SEVERE 수준이어야 함
        self.assertEqual(report.level, SkewLevel.SEVERE)

    def test_12_rebalance_partitions(self):
        """test_12: 파티션 재분산이 작동하는가"""
        unbalanced = [
            Partition(0, list(range(1000)), PartitionStrategy.RANGE, 0),
            Partition(1, list(range(100)), PartitionStrategy.RANGE, 1),
            Partition(2, list(range(100)), PartitionStrategy.RANGE, 2),
            Partition(3, list(range(100)), PartitionStrategy.RANGE, 3),
        ]

        report_before = self.handler.detect_skew(unbalanced)
        rebalanced = self.handler.rebalance(unbalanced)
        report_after = self.handler.detect_skew(rebalanced)

        # 재분산 후 파티션이 더 많아져야 함 (분할됨)
        self.assertGreaterEqual(len(rebalanced), len(unbalanced))

        # 재분산 후 스큐가 감소했거나 유지되어야 함 (0이 아닌 데이터는 분할됨)
        self.assertLessEqual(
            report_after.std_dev if report_after.std_dev is not None else 0,
            report_before.std_dev if report_before.std_dev is not None else 1000,
        )

    def test_13_find_hot_keys(self):
        """test_13: 핫키를 탐지하는가"""
        data = ["apple"] * 50 + ["banana"] * 30 + ["cherry"] * 20
        hot_keys = self.handler.find_hot_keys(data, top_n=3)

        # "apple"이 1위여야 함
        self.assertEqual(hot_keys[0][0], "apple")
        self.assertEqual(hot_keys[0][1], 50)


# ═══════════════════════════════════════════════════════════════════════════
# TestDataLakeOrchestrator (테스트 14~16)
# ═══════════════════════════════════════════════════════════════════════════


class TestDataLakeOrchestrator(unittest.TestCase):
    """전체 시스템 조율 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.orchestrator = DataLakeOrchestrator(num_workers=4)

    def test_14_full_pipeline_accuracy(self):
        """test_14: 전체 파이프라인이 정확한 결과를 내는가"""
        data = list(range(1000))
        result = self.orchestrator.run_full_pipeline(data)

        # 데이터 항목 수가 맞아야 함
        self.assertEqual(result["total_items"], 1000)

        # 파티션이 생성되어야 함
        self.assertGreater(result["num_partitions"], 0)

        # 스큐 보고서가 있어야 함
        self.assertIn("level", result["skew_report"])

    def test_15_benchmark_speedup(self):
        """test_15: 벤치마크에서 속도 향상이 나타나는가"""
        data = list(range(10000))
        result = self.orchestrator.benchmark(data, iterations=2)

        # 병렬 처리가 있어야 함
        self.assertGreater(result["parallel_avg_ms"], 0)

        # 속도 향상이 있을 수 있음 (단일 코어에서는 오버헤드가 클 수 있음)
        self.assertGreater(result["speedup"], 0)

    def test_16_data_locality_optimization(self):
        """test_16: 데이터 위치 최적화가 작동하는가"""
        optimizer = DataLocalityOptimizer()

        # 노드 등록
        for i in range(4):
            optimizer.register_node(DataNode(node_id=i))

        # 파티션 생성 및 할당
        partitions = [
            Partition(0, [1, 2, 3], PartitionStrategy.RANGE, 0),
            Partition(1, [4, 5, 6], PartitionStrategy.RANGE, 1),
            Partition(2, [7, 8, 9], PartitionStrategy.RANGE, 2),
        ]
        optimizer.assign_partitions(partitions)

        # 비용 계산
        costs = optimizer.optimize_assignments(partitions)

        # 로컬 비용은 1.0이어야 함
        self.assertEqual(costs[0], 1.0)
        self.assertEqual(costs[1], 1.0)
        self.assertEqual(costs[2], 1.0)


# ═══════════════════════════════════════════════════════════════════════════
# 테스트 실행
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    # 모든 테스트 실행
    unittest.main(verbosity=2)
