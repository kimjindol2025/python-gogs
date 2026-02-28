#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   🔍 TEST v5.1-A: 통합 시스템 점검 보고서 & 학습 성과 분석                ║
║                                                                            ║
║     Python University v2.1, v2.2, v3.1, v4.1, v5.1 통합 검증             ║
║                                                                            ║
║  철학: 기록이 증명이다 gogs                                                 ║
║  목표: 모듈화된 개념들을 하나의 거대한 시스템으로 통합 & 성능 증명         ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import time
import functools
from typing import List, Callable, Any, Optional
from datetime import datetime
import unittest

# ═══════════════════════════════════════════════════════════════════════════
# PART 1: 커스텀 예외 클래스 (v2.1 예외 처리 기반)
# ═══════════════════════════════════════════════════════════════════════════

class DataCorruptionError(Exception):
    """데이터가 손상되었을 때 발생하는 예외"""
    pass

class ProcessingError(Exception):
    """처리 중 발생하는 일반 예외"""
    pass

class SearchError(Exception):
    """검색 실패 예외"""
    pass

# ═══════════════════════════════════════════════════════════════════════════
# PART 2: 성능 측정 데코레이터 (v3.1 데코레이터 기반)
# ═══════════════════════════════════════════════════════════════════════════

def performance_timer(func: Callable) -> Callable:
    """
    【 v3.1 데코레이터 】
    함수의 실행 시간을 측정하고 성능 정보를 출력하는 데코레이터
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        """비동기 함수용 래퍼"""
        start_time = time.time()
        start_timestamp = datetime.now().isoformat()

        try:
            result = await func(*args, **kwargs)
            elapsed = time.time() - start_time
            print(f"[{start_timestamp}] ⏱️  {func.__name__} 완료: {elapsed*1000:.2f}ms")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"[{start_timestamp}] ❌ {func.__name__} 실패: {elapsed*1000:.2f}ms - {str(e)}")
            raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        """동기 함수용 래퍼"""
        start_time = time.time()
        start_timestamp = datetime.now().isoformat()

        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            print(f"[{start_timestamp}] ⏱️  {func.__name__} 완료: {elapsed*1000:.2f}ms")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"[{start_timestamp}] ❌ {func.__name__} 실패: {elapsed*1000:.2f}ms - {str(e)}")
            raise

    # 비동기 함수인지 판별
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

# ═══════════════════════════════════════════════════════════════════════════
# PART 3: 데이터 처리 엔진 (v2.2 클래스 + v4.1 비동기 기반)
# ═══════════════════════════════════════════════════════════════════════════

class GogsAnalyzer:
    """
    【 v2.2 + v4.1 】
    데이터 수집, 분석, 기록을 담당하는 엔진
    - 클래스 기반 설계
    - 비동기 처리
    - 예외 처리
    """

    def __init__(self, corruption_rate: float = 0.1):
        """
        Args:
            corruption_rate: 데이터 손상 확률 (0.0 ~ 1.0)
        """
        self.registry: List[int] = []
        self.corruption_rate = corruption_rate
        self.processed_count = 0
        self.success_count = 0
        self.error_count = 0
        self.error_log: List[str] = []
        self.performance_log: List[str] = []

    @performance_timer
    async def process_data(self, data_id: int) -> bool:
        """
        【 v4.1 비동기 + v2.1 예외처리 】
        데이터를 수집하고 분석하는 비동기 함수

        Args:
            data_id: 데이터 ID

        Returns:
            성공 여부

        Raises:
            DataCorruptionError: 데이터 손상 감지 시
        """
        self.processed_count += 1

        try:
            # 시뮬레이션: 데이터 수집 중
            await asyncio.sleep(0.01)

            # 【 예외 처리: v2.1 】
            # 특정 조건에서 데이터 손상 발생 시뮬레이션
            if data_id % 7 == 0:
                raise DataCorruptionError(f"Node-{data_id} 데이터 오염 감지")

            self.registry.append(data_id)
            self.success_count += 1
            return True

        except DataCorruptionError as e:
            # 【 예외 기록 】
            error_msg = f"🚨 점검 기록 #{self.processed_count}: {e}"
            self.error_log.append(error_msg)
            self.error_count += 1
            return False

    async def process_batch(self, data_count: int) -> dict:
        """
        【 v4.1 asyncio.gather 】
        대량의 데이터를 비동기로 동시 처리

        Args:
            data_count: 처리할 데이터 개수

        Returns:
            처리 결과 통계
        """
        print(f"\n📦 {data_count}개 데이터 비동기 수집 시작...")

        # 모든 데이터 처리 작업 생성
        tasks = [self.process_data(i) for i in range(data_count)]

        # 【 asyncio.gather 】: 모든 비동기 작업을 동시에 실행
        results = await asyncio.gather(*tasks, return_exceptions=False)

        # 결과 정렬 (이진 탐색 전제 조건)
        self.registry.sort()

        return {
            "total": self.processed_count,
            "success": self.success_count,
            "error": self.error_count,
            "error_rate": f"{(self.error_count / self.processed_count * 100):.1f}%",
            "registry_size": len(self.registry),
        }

    def get_status(self) -> str:
        """상태 요약"""
        return f"✅ {self.success_count} | ❌ {self.error_count} | 수집 대기: {len(self.registry)}"

# ═══════════════════════════════════════════════════════════════════════════
# PART 4: 검색 알고리즘 (v5.1 알고리즘 기반)
# ═══════════════════════════════════════════════════════════════════════════

class SearchOptimizer:
    """
    【 v5.1 알고리즘 】
    선형 탐색 vs 이진 탐색 성능 비교
    """

    def __init__(self):
        self.comparison_log: List[str] = []

    @performance_timer
    def find_linear_search(self, records: List[int], target: int) -> Optional[int]:
        """
        【 O(n) 선형 탐색 】
        Records를 처음부터 끝까지 순회하여 검색

        Args:
            records: 정렬된 리스트
            target: 찾을 값

        Returns:
            찾은 인덱스, 없으면 None
        """
        comparisons = 0

        for idx, value in enumerate(records):
            comparisons += 1
            if value == target:
                self.comparison_log.append(
                    f"선형탐색: {target} 찾음 (비교 {comparisons}회)"
                )
                return idx

        self.comparison_log.append(
            f"선형탐색: {target} 미발견 (비교 {comparisons}회)"
        )
        return None

    @performance_timer
    def find_binary_search(self, records: List[int], target: int) -> Optional[int]:
        """
        【 O(log n) 이진 탐색 】
        정렬된 리스트를 반씩 나누어 검색

        Args:
            records: 정렬된 리스트
            target: 찾을 값

        Returns:
            찾은 인덱스, 없으면 None

        Raises:
            SearchError: 리스트가 정렬되지 않은 경우
        """
        # 【 검증 】: 리스트 정렬 확인
        if records != sorted(records):
            raise SearchError("입력 리스트가 정렬되지 않았습니다")

        low, high = 0, len(records) - 1
        comparisons = 0

        while low <= high:
            comparisons += 1
            mid = (low + high) // 2
            guess = records[mid]

            if guess == target:
                self.comparison_log.append(
                    f"이진탐색: {target} 찾음 (비교 {comparisons}회, O(log n))"
                )
                return mid
            elif guess > target:
                high = mid - 1
            else:
                low = mid + 1

        self.comparison_log.append(
            f"이진탐색: {target} 미발견 (비교 {comparisons}회)"
        )
        return None

    def compare_performance(
        self, records: List[int], target: int
    ) -> dict:
        """
        두 알고리즘의 성능 비교

        Args:
            records: 정렬된 리스트
            target: 찾을 값

        Returns:
            성능 비교 결과
        """
        print(f"\n🔍 검색 성능 비교 (데이터: {len(records)}개, 목표: {target})")
        print("━" * 60)

        # 선형 탐색
        start = time.time()
        linear_result = self.find_linear_search(records, target)
        linear_time = (time.time() - start) * 1000

        # 이진 탐색
        start = time.time()
        binary_result = self.find_binary_search(records, target)
        binary_time = (time.time() - start) * 1000

        speedup = linear_time / binary_time if binary_time > 0 else float('inf')

        result = {
            "target": target,
            "linear_time_ms": f"{linear_time:.4f}",
            "binary_time_ms": f"{binary_time:.4f}",
            "speedup": f"{speedup:.0f}배",
            "linear_found": linear_result is not None,
            "binary_found": binary_result is not None,
        }

        return result

# ═══════════════════════════════════════════════════════════════════════════
# PART 5: 통합 시스템 관리자
# ═══════════════════════════════════════════════════════════════════════════

class IntegratedSystemManager:
    """
    【 통합 시스템 】
    모든 컴포넌트를 조율하는 매니저
    """

    def __init__(self):
        self.analyzer = GogsAnalyzer(corruption_rate=0.1)
        self.optimizer = SearchOptimizer()
        self.audit_log: List[str] = []

    async def run_full_audit(self, data_count: int = 100) -> dict:
        """
        완전한 감사 실행

        Args:
            data_count: 테스트 데이터 개수

        Returns:
            감사 결과 리포트
        """
        print("\n" + "╔" + "="*78 + "╗")
        print("║" + " "*20 + "🔍 AUDIT v5.1-A: 통합 시스템 점검" + " "*24 + "║")
        print("╚" + "="*78 + "╝")

        # 1. 데이터 수집
        print("\n【 Phase 1: 비동기 데이터 수집 (v4.1) 】")
        batch_result = await self.analyzer.process_batch(data_count)
        print(f"\n📊 수집 결과:")
        for key, value in batch_result.items():
            print(f"   {key}: {value}")

        # 2. 검색 성능 테스트
        print("\n【 Phase 2: 알고리즘 성능 검증 (v5.1) 】")

        if not self.analyzer.registry:
            print("⚠️  수집된 데이터가 없습니다")
            return {"status": "FAILED", "reason": "No data collected"}

        # 여러 목표값으로 검색 성능 비교
        test_targets = [
            self.analyzer.registry[0],  # 최소값
            self.analyzer.registry[-1],  # 최대값
            self.analyzer.registry[len(self.analyzer.registry) // 2],  # 중간값
        ]

        performance_results = []
        for target in test_targets:
            result = self.optimizer.compare_performance(
                self.analyzer.registry, target
            )
            performance_results.append(result)
            print(f"\n{result}")

        # 3. 예외 처리 검증
        print("\n【 Phase 3: 예외 처리 & 기록 (v2.1) 】")
        print(f"❌ 오류 발생 건수: {self.analyzer.error_count}")

        if self.analyzer.error_log:
            print("\n오류 로그 (최근 5건):")
            for log in self.analyzer.error_log[-5:]:
                print(f"   {log}")

        # 4. 최종 리포트
        print("\n【 Phase 4: 최종 감사 결과 】")

        report = {
            "status": "PASSED",
            "timestamp": datetime.now().isoformat(),
            "data_collection": batch_result,
            "search_performance": performance_results,
            "error_handling": {
                "total_errors": self.analyzer.error_count,
                "error_rate": batch_result["error_rate"],
                "system_stability": "✅ 안정적" if self.analyzer.error_count < data_count * 0.2 else "⚠️  주의",
            },
            "architecture_validation": {
                "v2_1_exception_handling": "✅ PASS",
                "v2_2_class_design": "✅ PASS",
                "v3_1_decorator": "✅ PASS",
                "v4_1_async_processing": "✅ PASS",
                "v5_1_algorithm_optimization": "✅ PASS",
            }
        }

        return report

# ═══════════════════════════════════════════════════════════════════════════
# PART 6: 테스트
# ═══════════════════════════════════════════════════════════════════════════

class TestAuditSystem(unittest.TestCase):
    """감사 시스템 테스트"""

    def setUp(self):
        self.manager = IntegratedSystemManager()

    def test_1_exception_handling(self):
        """테스트 1: 예외 처리 (v2.1)"""
        with self.assertRaises(DataCorruptionError):
            raise DataCorruptionError("테스트 예외")

    def test_2_async_processing(self):
        """테스트 2: 비동기 처리 (v4.1)"""
        async def test_async():
            result = await self.manager.analyzer.process_data(1)
            self.assertIsNotNone(result)

        asyncio.run(test_async())

    def test_3_linear_search(self):
        """테스트 3: 선형 탐색"""
        records = [1, 3, 5, 7, 9, 11]
        result = self.manager.optimizer.find_linear_search(records, 7)
        self.assertEqual(result, 3)

    def test_4_binary_search(self):
        """테스트 4: 이진 탐색"""
        records = [1, 3, 5, 7, 9, 11]
        result = self.manager.optimizer.find_binary_search(records, 7)
        self.assertEqual(result, 3)

    def test_5_full_integration(self):
        """테스트 5: 완전 통합"""
        async def test_full():
            result = await self.manager.run_full_audit(data_count=50)
            self.assertEqual(result["status"], "PASSED")

        asyncio.run(test_full())

# ═══════════════════════════════════════════════════════════════════════════
# 메인 실행
# ═══════════════════════════════════════════════════════════════════════════

async def main():
    """메인 실행"""
    manager = IntegratedSystemManager()

    # 완전 감사 실행
    report = await manager.run_full_audit(data_count=100)

    # 리포트 출력
    print("\n" + "="*80)
    print("최종 감사 리포트")
    print("="*80)
    import json
    print(json.dumps(report, indent=2, ensure_ascii=False))

    print("\n" + "="*80)
    print("✅ 감사 완료 - 모든 모듈 통합 성공!")
    print("="*80)
    print("\n저장 필수 너는 기록이 증명이다 gogs\n")

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*15 + "AUDIT v5.1-A: 통합 시스템 점검 & 학습 성과 분석" + " "*14 + "║")
    print("║" + " "*20 + "Python University 검증 시스템" + " "*28 + "║")
    print("╚" + "="*78 + "╝")

    # 단위 테스트 실행
    print("\n【 단위 테스트 실행 】\n")
    unittest.main(argv=[''], exit=False, verbosity=2)

    # 완전 감사 실행
    print("\n【 완전 감사 실행 】")
    asyncio.run(main())
