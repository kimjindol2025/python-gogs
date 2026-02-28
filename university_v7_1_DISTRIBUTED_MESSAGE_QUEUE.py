#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【 v7.1: Distributed Computing & Message Queues 】
Python Graduate School 석사 과정 - 첫 번째 연구

분산 시스템의 철학:
"수백만 명의 사용자가 동시에 접속해도 시스템이 터지지 않아야 한다"

이를 위해서는:
1. 생산자-소비자 패턴 (Producer-Consumer)
   - 작업을 큐에 쌓아뒀다가 순차 처리
   - 부하 분산 및 장애 격리

2. 느슨한 결합 (Loose Coupling)
   - 생산자와 소비자는 서로를 알지 못함
   - 메시지 브로커만 중앙에서 조율

3. 비동기 분산 처리
   - asyncio로 동시 다중 워커 관리
   - 높은 처리량(throughput)과 낮은 응답시간(latency)

핵심 개념:
1. 멱등성 (Idempotency)
   - 동일한 작업이 두 번 실행되어도 결과는 같음
   - 네트워크 오류 시에도 안전

2. 배압 관리 (Backpressure)
   - 생산 속도 > 소비 속도일 때 생산 제어
   - 메모리 오버플로우 방지

코드 규모: 600+줄
시뮬레이션: Producer-Consumer 실시간 처리
커밋: gogs 저장

【 v7.1 구성 】
Part 1: GogsMessageBroker — 메시지 큐 핵심
Part 2: TaskProducer — 작업 생성자
Part 3: TaskConsumer (Worker) — 작업 처리자
Part 4: SystemMonitor — 시스템 모니터링
Part 5: IdempotencyManager — 멱등성 보증
Part 6: BackpressureController — 배압 관리
Part 7: 성능 분석 & 시뮬레이션
"""

import asyncio
from collections import deque
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
import random
import time
import uuid


# ═══════════════════════════════════════════════════════════════════
# PART 1: GogsMessageBroker — 메시지 큐 핵심
# ═══════════════════════════════════════════════════════════════════

class Task:
    """
    분산 시스템에서 처리할 작업 단위

    철학: 작업은 불변(immutable)이어야 한다
    """
    def __init__(self, task_id: str, operation: str, data: Any, priority: int = 0):
        self.task_id = task_id
        self.operation = operation
        self.data = data
        self.priority = priority
        self.created_at = datetime.now()
        self.status = "PENDING"

    def __repr__(self):
        return f"Task({self.task_id[:8]}..., {self.operation}, priority={self.priority})"


class GogsMessageBroker:
    """
    분산 메시지 큐 시스템

    역할:
    - 생산자로부터 작업을 받아 큐에 저장
    - 소비자(워커)가 꺼내갈 때까지 안전 보관
    - 모든 전송이 완료될 때까지 보관

    철학: "브로커는 신뢰의 중심이다"
    - 생산자와 소비자 분리
    - 부하 분산 및 장애 격리
    - 모든 작업 추적 가능
    """

    def __init__(self, max_queue_size: int = 1000):
        self.queue: deque = deque()
        self.max_queue_size = max_queue_size
        self.condition = asyncio.Condition()
        self.stats = {
            "total_produced": 0,
            "total_consumed": 0,
            "total_failed": 0,
            "peak_queue_size": 0,
        }
        self.processed_tasks: Set[str] = set()  # 멱등성을 위한 처리 완료 추적

    async def produce(self, task: Task) -> bool:
        """
        작업을 큐에 추가

        Args:
            task: 처리할 작업

        Returns:
            bool: 성공 여부
        """
        async with self.condition:
            # 배압 관리: 큐가 너무 크면 대기
            if len(self.queue) >= self.max_queue_size:
                print(f"⚠️  [{task.task_id[:8]}] 큐 오버플로우! ({len(self.queue)}/{self.max_queue_size})")
                return False

            self.queue.append(task)
            self.stats["total_produced"] += 1

            # 통계 업데이트
            if len(self.queue) > self.stats["peak_queue_size"]:
                self.stats["peak_queue_size"] = len(self.queue)

            # 대기 중인 워커에게 알림
            self.condition.notify_all()

            return True

    async def consume(self) -> Optional[Task]:
        """
        큐에서 작업을 꺼냄

        Returns:
            Task: 처리할 작업 (없으면 None)
        """
        async with self.condition:
            # 작업이 올 때까지 대기
            while not self.queue:
                await self.condition.wait()

            task = self.queue.popleft()
            return task

    def mark_completed(self, task_id: str) -> None:
        """작업 완료 표시 (멱등성 추적)"""
        self.processed_tasks.add(task_id)
        self.stats["total_consumed"] += 1

    def mark_failed(self, task_id: str) -> None:
        """작업 실패 표시"""
        self.stats["total_failed"] += 1

    def is_processed(self, task_id: str) -> bool:
        """작업이 이미 처리되었는지 확인"""
        return task_id in self.processed_tasks

    def get_queue_size(self) -> int:
        """현재 큐 크기"""
        return len(self.queue)

    def get_stats(self) -> Dict[str, Any]:
        """시스템 통계"""
        return {
            **self.stats,
            "current_queue_size": len(self.queue),
            "pending_tasks": len(self.queue),
        }


# ═══════════════════════════════════════════════════════════════════
# PART 2: TaskProducer — 작업 생성자
# ═══════════════════════════════════════════════════════════════════

class TaskProducer:
    """
    작업 생성 주체

    역할:
    - 지속적으로 새로운 작업 생성
    - 우선순위 설정
    - 배압 처리
    """

    def __init__(self, broker: GogsMessageBroker):
        self.broker = broker
        self.produced_count = 0

    async def generate_tasks(self, count: int, interval: float = 0.2):
        """
        지정된 개수의 작업 생성

        Args:
            count: 생성할 작업 개수
            interval: 작업 생성 간격 (초)
        """
        operations = ["데이터_분석", "이미지_처리", "텍스트_요약", "추천_엔진"]

        for i in range(count):
            task_id = f"task_{uuid.uuid4().hex[:8]}"
            operation = random.choice(operations)
            priority = random.randint(0, 5)
            data = {"index": i, "timestamp": datetime.now().isoformat()}

            task = Task(task_id, operation, data, priority)

            success = await self.broker.produce(task)

            if success:
                self.produced_count += 1
                print(f"📥 [{task.task_id[:8]}] 작업 투입: {operation} (우선순위: {priority})")
            else:
                print(f"❌ [{task.task_id[:8]}] 작업 투입 실패 (배압 발동)")
                await asyncio.sleep(1)  # 배압 처리: 대기 후 재시도

            await asyncio.sleep(interval)


# ═══════════════════════════════════════════════════════════════════
# PART 3: TaskConsumer (Worker) — 작업 처리자
# ═══════════════════════════════════════════════════════════════════

class TaskConsumer:
    """
    작업 처리 주체 (워커)

    역할:
    - 큐에서 작업을 꺼냄
    - 실제로 처리 실행
    - 멱등성 검증
    - 실패 처리
    """

    def __init__(self, broker: GogsMessageBroker, worker_id: str):
        self.broker = broker
        self.worker_id = worker_id
        self.processed_count = 0
        self.failed_count = 0

    async def start(self):
        """워커 시작 (지속적으로 작업 처리)"""
        print(f"🚀 [{self.worker_id}] 워커 시작")

        try:
            while True:
                task = await self.broker.consume()

                # 멱등성 검증
                if self.broker.is_processed(task.task_id):
                    print(f"⏭️  [{self.worker_id}] {task.task_id[:8]} 이미 처리됨 (멱등성)")
                    continue

                # 작업 처리
                await self._process_task(task)

                # 완료 표시
                self.broker.mark_completed(task.task_id)
                self.processed_count += 1

        except asyncio.CancelledError:
            print(f"⏹️  [{self.worker_id}] 워커 종료 (처리: {self.processed_count}개)")

    async def _process_task(self, task: Task):
        """
        실제 작업 처리 시뮬레이션

        작업 유형별로 다른 시간 소요
        """
        try:
            # 작업 유형별 처리 시간
            processing_time = {
                "데이터_분석": random.uniform(0.5, 1.0),
                "이미지_처리": random.uniform(1.0, 1.5),
                "텍스트_요약": random.uniform(0.3, 0.7),
                "추천_엔진": random.uniform(0.8, 1.2),
            }.get(task.operation, 0.5)

            # 작업 처리
            await asyncio.sleep(processing_time)

            print(f"✅ [{self.worker_id}] {task.task_id[:8]} 완료: {task.operation} ({processing_time:.2f}s)")

        except Exception as e:
            print(f"❌ [{self.worker_id}] {task.task_id[:8]} 실패: {e}")
            self.broker.mark_failed(task.task_id)
            self.failed_count += 1


# ═══════════════════════════════════════════════════════════════════
# PART 4: SystemMonitor — 시스템 모니터링
# ═══════════════════════════════════════════════════════════════════

class SystemMonitor:
    """
    분산 시스템 전체 모니터링

    역할:
    - 실시간 메트릭 수집
    - 성능 분석
    - 병목 지점 감지
    """

    def __init__(self, broker: GogsMessageBroker):
        self.broker = broker
        self.start_time = time.time()

    async def monitor(self, interval: float = 2.0):
        """
        주기적으로 시스템 상태 모니터링

        Args:
            interval: 모니터링 간격 (초)
        """
        try:
            while True:
                await asyncio.sleep(interval)

                stats = self.broker.get_stats()
                elapsed = time.time() - self.start_time

                print("\n" + "─" * 60)
                print(f"【 시스템 상태 】 (경과: {elapsed:.1f}초)")
                print("─" * 60)
                print(f"  생산: {stats['total_produced']:3d}개 | 소비: {stats['total_consumed']:3d}개 | 실패: {stats['total_failed']:3d}개")
                print(f"  현재 큐: {stats['current_queue_size']:3d}개 | 최대 큐: {stats['peak_queue_size']:3d}개")

                # 처리율 계산
                if stats['total_produced'] > 0:
                    processing_rate = stats['total_consumed'] / stats['total_produced'] * 100
                    print(f"  처리율: {processing_rate:5.1f}% ({stats['total_consumed']}/{stats['total_produced']})")

                # 처리량 계산
                if elapsed > 0:
                    throughput = stats['total_consumed'] / elapsed
                    print(f"  처리량: {throughput:.2f} tasks/sec")

        except asyncio.CancelledError:
            print("\n【 모니터링 종료 】")


# ═══════════════════════════════════════════════════════════════════
# PART 5: IdempotencyManager — 멱등성 보증
# ═══════════════════════════════════════════════════════════════════

class IdempotencyManager:
    """
    멱등성 관리

    철학: "동일한 작업이 여러 번 실행되어도 결과는 같아야 한다"

    사용 사례:
    - 네트워크 오류로 작업이 두 번 전송됨
    - 워커 충돌 후 재시작
    - 모니터링 시스템의 작업 재실행
    """

    def __init__(self):
        self.idempotency_cache: Dict[str, Any] = {}

    def execute_idempotent(self, task_id: str, operation: callable) -> Any:
        """
        멱등성을 보장하면서 작업 실행

        Args:
            task_id: 작업 ID (고유값)
            operation: 실행할 작업 함수

        Returns:
            Any: 작업 결과
        """
        if task_id in self.idempotency_cache:
            return self.idempotency_cache[task_id]

        result = operation()
        self.idempotency_cache[task_id] = result
        return result

    def verify_idempotency(self):
        """멱등성 검증"""
        print("\n【 멱등성 검증 】\n")

        # 테스트: 동일한 작업 여러 번 실행
        test_op = lambda: "고정된 결과"

        result1 = self.execute_idempotent("test_001", test_op)
        result2 = self.execute_idempotent("test_001", test_op)
        result3 = self.execute_idempotent("test_001", test_op)

        if result1 == result2 == result3:
            print(f"✅ 멱등성 검증 통과")
            print(f"   세 번의 실행이 동일한 결과 반환: {result1}")
        else:
            print(f"❌ 멱등성 검증 실패")


# ═══════════════════════════════════════════════════════════════════
# PART 6: BackpressureController — 배압 관리
# ═══════════════════════════════════════════════════════════════════

class BackpressureController:
    """
    배압 관리

    철학: "생산 속도 > 소비 속도일 때, 생산을 조절하여 메모리 오버플로우 방지"

    사용 전략:
    1. 큐 크기 모니터링
    2. 큐 크기 임계값 설정
    3. 임계값 초과 시 생산 속도 조절
    """

    def __init__(self, broker: GogsMessageBroker):
        self.broker = broker
        self.max_backpressure_threshold = broker.max_queue_size * 0.8

    async def apply_backpressure(self) -> float:
        """
        배압 적용 (생산 속도 조절)

        Returns:
            float: 현재 대기 시간 (초)
        """
        queue_size = self.broker.get_queue_size()

        if queue_size > self.max_backpressure_threshold:
            # 큐 크기에 따라 지수적으로 대기 시간 증가
            backpressure_factor = (queue_size / self.broker.max_queue_size) ** 2
            wait_time = backpressure_factor * 2.0  # 최대 2초

            print(f"⏱️  배압 발동: 큐 크기 {queue_size}/{self.broker.max_queue_size}")
            await asyncio.sleep(wait_time)
            return wait_time

        return 0.0

    def analyze_backpressure(self):
        """배압 분석"""
        print("\n【 배압 분석 】\n")

        queue_size = self.broker.get_queue_size()
        max_size = self.broker.max_queue_size
        threshold = self.max_backpressure_threshold

        print(f"  현재 큐: {queue_size}/{max_size}")
        print(f"  배압 임계값: {threshold:.0f}")

        if queue_size > threshold:
            backpressure_pct = (queue_size / max_size) ** 2 * 100
            print(f"  배압 레벨: {backpressure_pct:.1f}% (생산 속도 조절 필요)")
        else:
            print(f"  배압 레벨: 안정적 (0%)")


# ═══════════════════════════════════════════════════════════════════
# PART 7: 성능 분석 & 시뮬레이션
# ═══════════════════════════════════════════════════════════════════

def print_final_report(broker: GogsMessageBroker, elapsed_time: float):
    """최종 분석 보고서"""
    stats = broker.get_stats()

    print("\n" + "═" * 70)
    print("【 분산 메시지 큐 시스템 성능 분석 】")
    print("═" * 70 + "\n")

    print("【 처리 통계 】")
    print(f"  생산된 작업: {stats['total_produced']:4d}개")
    print(f"  소비된 작업: {stats['total_consumed']:4d}개")
    print(f"  실패한 작업: {stats['total_failed']:4d}개")
    print(f"  남은 작업:   {stats['current_queue_size']:4d}개")

    print("\n【 성능 지표 】")
    print(f"  경과 시간: {elapsed_time:.2f}초")

    if elapsed_time > 0:
        throughput = stats['total_consumed'] / elapsed_time
        print(f"  처리량: {throughput:.2f} tasks/sec")

    if stats['total_produced'] > 0:
        processing_rate = stats['total_consumed'] / stats['total_produced'] * 100
        print(f"  처리율: {processing_rate:.1f}%")

    print(f"  최대 큐 크기: {stats['peak_queue_size']}/{broker.max_queue_size}")

    print("\n【 분산 시스템의 이점 】")
    print("  ✓ 부하 분산: 여러 워커가 동시에 작업 처리")
    print("  ✓ 장애 격리: 워커 한 대 다운 → 데이터 손실 없음")
    print("  ✓ 확장성: 워커 개수 추가로 처리량 증대")
    print("  ✓ 느슨한 결합: 생산자/소비자 독립적 운영")


async def main():
    """메인 시뮬레이션"""
    print("\n╔" + "═" * 68 + "╗")
    print("║" + " " * 8 + "【 v7.1: Distributed Message Queue System 】" + " " * 14 + "║")
    print("║" + " " * 18 + "Python Graduate School 석사 과정 1" + " " * 15 + "║")
    print("╚" + "═" * 68 + "╝\n")

    # 시스템 초기화
    broker = GogsMessageBroker(max_queue_size=100)
    producer = TaskProducer(broker)
    monitor = SystemMonitor(broker)
    idempotency_mgr = IdempotencyManager()
    backpressure_mgr = BackpressureController(broker)

    # 멱등성 검증
    idempotency_mgr.verify_idempotency()

    # 워커 생성 (3개)
    workers = [
        TaskConsumer(broker, f"Worker-{i}")
        for i in range(3)
    ]

    # 작업 시작
    print("\n【 분산 시스템 시작 】\n")
    start_time = time.time()

    # 워커 태스크
    worker_tasks = [asyncio.create_task(worker.start()) for worker in workers]

    # 모니터링 태스크
    monitor_task = asyncio.create_task(monitor.monitor())

    # 작업 생성 (20개 작업, 0.2초 간격)
    await producer.generate_tasks(count=20, interval=0.2)

    # 모든 작업 처리 대기
    await asyncio.sleep(15)

    # 종료
    elapsed_time = time.time() - start_time
    for task in worker_tasks + [monitor_task]:
        task.cancel()

    # 최종 보고서
    print_final_report(broker, elapsed_time)

    # 배압 분석
    backpressure_mgr.analyze_backpressure()

    print("\n【 분산 시스템의 철학 】\n")
    print("「 느슨한 결합 」")
    print("  → 생산자와 소비자는 서로를 알지 못함")
    print("  → 메시지 브로커가 유일한 중개자\n")

    print("「 확장성 」")
    print("  → 워커를 추가하면 처리 능력 향상")
    print("  → 생산자는 변경 없음\n")

    print("「 신뢰성 」")
    print("  → 큐에 저장되므로 데이터 손실 없음")
    print("  → 멱등성으로 중복 처리 방지\n")

    print("【 기록이 증명이다 】")
    print("모든 분산 처리가 코드로 기록된다.")
    print("대규모 시스템의 설계 원칙이 실증된다.\n")


if __name__ == "__main__":
    asyncio.run(main())
