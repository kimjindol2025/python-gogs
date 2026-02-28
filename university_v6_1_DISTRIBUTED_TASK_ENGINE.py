#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════╗
║        Python University v6.1: 분산 작업 처리 엔진 & 고가용성 아키텍처         ║
║                  Distributed Task Engine & High Availability              ║
║                                                                            ║
║  철학: 기록이 증명이다 gogs                                                  ║
║  원칙: 로그와 테스트가 증명되지 않은 코드는 배포될 수 없다                         ║
║                                                                            ║
║  【 핵심 개념 】                                                            ║
║  1. 오케스트레이션 (Orchestration)                                          ║
║  2. 로드 밸런싱 (Load Balancing)                                           ║
║  3. 오토 스케일링 (Auto Scaling)                                           ║
║  4. 장애 복구 (Failover)                                                  ║
║  5. CI/CD 파이프라인 (Continuous Integration/Deployment)                 ║
║  6. 모니터링 & 로깅 (Monitoring & Observability)                          ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import uuid
import random
import time
import threading
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from collections import deque
import json
from datetime import datetime
import unittest

# ═══════════════════════════════════════════════════════════════════════════
# PART 1: 기본 데이터 구조 및 상태 머신
# ═══════════════════════════════════════════════════════════════════════════

class TaskStatus(Enum):
    """작업 상태 머신"""
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"

class WorkerStatus(Enum):
    """워커 노드 상태"""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    DEAD = "DEAD"

class NodeHealth(Enum):
    """노드 헬스 레벨"""
    CRITICAL = 0.0
    POOR = 0.3
    WARNING = 0.6
    GOOD = 0.8
    EXCELLENT = 1.0

@dataclass
class Task:
    """작업 단위 표현"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    data: str = ""
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    assigned_node: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3

    def duration(self) -> float:
        """작업 수행 시간(초)"""
        if self.completed_at:
            return (self.completed_at - self.created_at).total_seconds()
        return 0.0

@dataclass
class Metrics:
    """노드 성능 지표"""
    cpu_usage: float = 0.0      # 0-100%
    memory_usage: float = 0.0   # 0-100%
    task_queue_length: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    request_latency_ms: float = 0.0

    def health_score(self) -> float:
        """헬스 점수 계산 (0-1)"""
        cpu_factor = 1 - (self.cpu_usage / 100)
        mem_factor = 1 - (self.memory_usage / 100)
        queue_factor = 1 - min(self.task_queue_length / 100, 1.0)
        return (cpu_factor + mem_factor + queue_factor) / 3

# ═══════════════════════════════════════════════════════════════════════════
# PART 2: 워커 노드 (v4.2 멀티프로세싱 활용)
# ═══════════════════════════════════════════════════════════════════════════

class WorkerNode:
    """분산 시스템의 워커 노드"""

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.status = WorkerStatus.HEALTHY
        self.metrics = Metrics()
        self.task_history: List[Task] = []
        self.is_alive = True
        self.health_check_count = 0

    def process(self, task: Task) -> Task:
        """작업 처리 (시뮬레이션)"""
        task.status = TaskStatus.PROCESSING
        task.assigned_node = self.node_id

        # CPU/Memory 부하 시뮬레이션
        self.metrics.cpu_usage = random.uniform(20, 80)
        self.metrics.memory_usage = random.uniform(30, 70)
        self.metrics.request_latency_ms = random.uniform(10, 100)

        # 99%는 성공, 1%는 실패
        if random.random() < 0.99:
            task.status = TaskStatus.COMPLETED
            task.result = f"✓ 처리 완료: {task.data}"
            self.metrics.completed_tasks += 1
        else:
            task.status = TaskStatus.FAILED
            task.result = "네트워크 오류"
            self.metrics.failed_tasks += 1

        task.completed_at = datetime.now()
        self.task_history.append(task)

        return task

    def health_check(self) -> bool:
        """헬스 체크"""
        self.health_check_count += 1

        # 99.9% 성공률
        if random.random() < 0.999:
            self.is_alive = True
            score = self.metrics.health_score()
            if score >= 0.8:
                self.status = WorkerStatus.HEALTHY
            elif score >= 0.5:
                self.status = WorkerStatus.DEGRADED
            else:
                self.status = WorkerStatus.UNHEALTHY
            return True
        else:
            self.is_alive = False
            self.status = WorkerStatus.DEAD
            return False

    def get_status(self) -> str:
        """상태 문자열"""
        return f"Node-{self.node_id}[{self.status.name}] CPU:{self.metrics.cpu_usage:.1f}% MEM:{self.metrics.memory_usage:.1f}%"

# ═══════════════════════════════════════════════════════════════════════════
# PART 3: 로드 밸런서
# ═══════════════════════════════════════════════════════════════════════════

class LoadBalancer:
    """요청 분산 알고리즘"""

    def __init__(self):
        self.round_robin_index = 0

    def round_robin(self, workers: List[WorkerNode]) -> Optional[WorkerNode]:
        """라운드 로빈: 순환 분산"""
        if not workers:
            return None
        self.round_robin_index = (self.round_robin_index + 1) % len(workers)
        return workers[self.round_robin_index]

    def least_connection(self, workers: List[WorkerNode]) -> Optional[WorkerNode]:
        """최소 연결: 큐가 가장 짧은 노드 선택"""
        if not workers:
            return None
        return min(workers, key=lambda w: w.metrics.task_queue_length)

    def least_load(self, workers: List[WorkerNode]) -> Optional[WorkerNode]:
        """최소 부하: 헬스 스코어가 가장 높은 노드 선택"""
        if not workers:
            return None
        return max(workers, key=lambda w: w.metrics.health_score())

    def select_worker(self, workers: List[WorkerNode], strategy: str = "health") -> Optional[WorkerNode]:
        """전략에 따라 워커 선택"""
        healthy = [w for w in workers if w.status in [WorkerStatus.HEALTHY, WorkerStatus.DEGRADED]]

        if not healthy:
            return None

        if strategy == "round_robin":
            return self.round_robin(healthy)
        elif strategy == "least_connection":
            return self.least_connection(healthy)
        else:  # health (기본값)
            return self.least_load(healthy)

# ═══════════════════════════════════════════════════════════════════════════
# PART 4: 오토 스케일러
# ═══════════════════════════════════════════════════════════════════════════

class AutoScaler:
    """자동 확장 및 축소"""

    def __init__(self, min_nodes: int = 2, max_nodes: int = 10):
        self.min_nodes = min_nodes
        self.max_nodes = max_nodes
        self.scale_up_threshold = 0.8     # 헬스 점수 < 0.8
        self.scale_down_threshold = 0.2   # 헬스 점수 > 0.2
        self.scale_action_log: List[str] = []

    def should_scale_up(self, workers: List[WorkerNode]) -> bool:
        """스케일업 판단"""
        if len(workers) >= self.max_nodes:
            return False

        avg_health = sum(w.metrics.health_score() for w in workers) / len(workers)
        avg_queue = sum(w.metrics.task_queue_length for w in workers) / len(workers)

        return avg_health < self.scale_up_threshold or avg_queue > 50

    def should_scale_down(self, workers: List[WorkerNode]) -> bool:
        """스케일다운 판단"""
        if len(workers) <= self.min_nodes:
            return False

        avg_health = sum(w.metrics.health_score() for w in workers) / len(workers)
        avg_queue = sum(w.metrics.task_queue_length for w in workers) / len(workers)

        return avg_health > self.scale_down_threshold and avg_queue < 5

    def scale(self, workers: List[WorkerNode], action: str = "up") -> List[WorkerNode]:
        """스케일 실행"""
        if action == "up" and len(workers) < self.max_nodes:
            new_node = WorkerNode(f"node-{len(workers)}")
            workers.append(new_node)
            self.scale_action_log.append(f"[{datetime.now().isoformat()}] ⬆️  SCALE UP: {len(workers)} 노드")
            return workers
        elif action == "down" and len(workers) > self.min_nodes:
            workers.pop()
            self.scale_action_log.append(f"[{datetime.now().isoformat()}] ⬇️  SCALE DOWN: {len(workers)} 노드")
            return workers

        return workers

# ═══════════════════════════════════════════════════════════════════════════
# PART 5: Failover 관리자
# ═══════════════════════════════════════════════════════════════════════════

class FailoverManager:
    """장애 감지 및 복구"""

    def __init__(self):
        self.failover_log: List[str] = []
        self.recovered_tasks: List[Task] = []

    def detect_failures(self, workers: List[WorkerNode]) -> List[WorkerNode]:
        """장애 노드 감지"""
        failed_nodes = []

        for worker in workers:
            if not worker.health_check():
                failed_nodes.append(worker)
                self.failover_log.append(
                    f"[{datetime.now().isoformat()}] ⚠️  FAILURE: {worker.node_id} 다운 감지"
                )

        return failed_nodes

    def failover(self, failed_worker: WorkerNode, healthy_workers: List[WorkerNode]) -> List[Task]:
        """장애 복구: 미완료 작업 재할당"""
        reassigned_tasks = []

        for task in failed_worker.task_history:
            if task.status in [TaskStatus.PROCESSING, TaskStatus.PENDING]:
                task.status = TaskStatus.QUEUED
                task.assigned_node = None
                task.retry_count += 1
                reassigned_tasks.append(task)

                self.failover_log.append(
                    f"[{datetime.now().isoformat()}] 🔄 FAILOVER: Task-{task.id} "
                    f"재할당 (시도 {task.retry_count}/{task.max_retries})"
                )

        self.recovered_tasks.extend(reassigned_tasks)
        return reassigned_tasks

    def remove_dead_node(self, workers: List[WorkerNode], dead_node: WorkerNode) -> List[WorkerNode]:
        """죽은 노드 제거"""
        if dead_node in workers:
            workers.remove(dead_node)
            self.failover_log.append(
                f"[{datetime.now().isoformat()}] 💀 REMOVED: {dead_node.node_id}"
            )
        return workers

# ═══════════════════════════════════════════════════════════════════════════
# PART 6: CI/CD 파이프라인
# ═══════════════════════════════════════════════════════════════════════════

class CIPipeline:
    """지속적 통합 & 배포"""

    def __init__(self):
        self.stages = ["COMMIT", "TEST", "BUILD", "DEPLOY"]
        self.pipeline_log: List[str] = []
        self.test_results: Dict[str, bool] = {}

    def commit(self, code_changes: str) -> bool:
        """Stage 1: 커밋"""
        self.pipeline_log.append(f"[{datetime.now().isoformat()}] 📝 COMMIT: {code_changes}")
        return True

    def test(self, test_name: str, passed: bool) -> bool:
        """Stage 2: 테스트"""
        self.test_results[test_name] = passed
        status = "✓" if passed else "✗"
        self.pipeline_log.append(f"[{datetime.now().isoformat()}] 🧪 TEST {status}: {test_name}")
        return passed

    def build(self, build_id: str) -> bool:
        """Stage 3: 빌드"""
        # 모든 테스트 통과 시에만 빌드
        if all(self.test_results.values()):
            self.pipeline_log.append(f"[{datetime.now().isoformat()}] 🔨 BUILD: {build_id} 성공")
            return True
        else:
            self.pipeline_log.append(f"[{datetime.now().isoformat()}] 🔨 BUILD: {build_id} 실패 (테스트 실패)")
            return False

    def deploy(self, version: str) -> bool:
        """Stage 4: 배포"""
        if all(self.test_results.values()):
            self.pipeline_log.append(f"[{datetime.now().isoformat()}] 🚀 DEPLOY: v{version} 배포 완료")
            return True
        else:
            self.pipeline_log.append(f"[{datetime.now().isoformat()}] 🚀 DEPLOY: v{version} 배포 거부 (테스트 필수)")
            return False

# ═══════════════════════════════════════════════════════════════════════════
# PART 7: 모니터링 & 옵저버빌리티
# ═══════════════════════════════════════════════════════════════════════════

class Monitor:
    """시스템 모니터링"""

    def __init__(self):
        self.logs: deque = deque(maxlen=1000)
        self.metrics_history: List[Dict] = []
        self.start_time = datetime.now()

    def log(self, level: str, message: str):
        """로그 기록"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level}: {message}"
        self.logs.append(log_entry)

    def record_metrics(self, workers: List[WorkerNode], task_queue_len: int):
        """메트릭 기록"""
        timestamp = datetime.now().isoformat()
        metrics = {
            "timestamp": timestamp,
            "total_nodes": len(workers),
            "healthy_nodes": sum(1 for w in workers if w.status == WorkerStatus.HEALTHY),
            "queue_length": task_queue_len,
            "avg_cpu": sum(w.metrics.cpu_usage for w in workers) / len(workers) if workers else 0,
            "avg_memory": sum(w.metrics.memory_usage for w in workers) / len(workers) if workers else 0,
            "total_completed": sum(w.metrics.completed_tasks for w in workers),
            "total_failed": sum(w.metrics.failed_tasks for w in workers),
        }
        self.metrics_history.append(metrics)

    def get_summary(self) -> str:
        """모니터링 요약"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        return f"Uptime: {uptime:.1f}s | Logs: {len(self.logs)} | Metrics: {len(self.metrics_history)}"

# ═══════════════════════════════════════════════════════════════════════════
# PART 8: 분산 작업 처리 엔진 (통합)
# ═══════════════════════════════════════════════════════════════════════════

class DistributedTaskEngine:
    """고가용성 분산 시스템 마스터 오케스트레이터"""

    def __init__(self, initial_nodes: int = 3):
        self.workers: List[WorkerNode] = [WorkerNode(f"node-{i}") for i in range(initial_nodes)]
        self.task_queue: deque = deque()
        self.completed_tasks: List[Task] = []

        self.load_balancer = LoadBalancer()
        self.auto_scaler = AutoScaler(min_nodes=2, max_nodes=8)
        self.failover_manager = FailoverManager()
        self.ci_pipeline = CIPipeline()
        self.monitor = Monitor()

        self.lock = threading.Lock()
        self.is_running = False

    def submit_task(self, task_data: str) -> Task:
        """작업 제출"""
        task = Task(data=task_data)
        task.status = TaskStatus.QUEUED

        with self.lock:
            self.task_queue.append(task)

        self.monitor.log("INFO", f"Task-{task.id} 제출됨")
        return task

    def _process_queue(self):
        """작업 큐 처리 (메인 루프)"""
        while self.task_queue or self.is_running:
            # 1. 작업 선택
            if not self.task_queue:
                continue

            with self.lock:
                if not self.task_queue:
                    continue
                task = self.task_queue.popleft()

            # 2. 워커 선택 (로드 밸런싱)
            worker = self.load_balancer.select_worker(self.workers, strategy="health")

            if not worker:
                self.task_queue.appendleft(task)
                self.monitor.log("WARNING", "사용 가능한 워커 없음")
                continue

            # 3. 작업 처리
            task = worker.process(task)
            self.completed_tasks.append(task)
            self.monitor.log("INFO", f"Task-{task.id} 완료 ({worker.node_id})")

            # 4. 메트릭 기록
            self.monitor.record_metrics(self.workers, len(self.task_queue))

    def orchestrate(self, max_iterations: int = 10):
        """오케스트레이션: 시스템 관리"""
        self.is_running = True

        for iteration in range(max_iterations):
            self.monitor.log("INFO", f"=== Iteration {iteration + 1} ===")

            # 1. 작업 처리
            if self.task_queue:
                task = self.task_queue.popleft()
                worker = self.load_balancer.select_worker(self.workers)

                if worker:
                    task = worker.process(task)
                    self.completed_tasks.append(task)

            # 2. 장애 감지 & 복구
            failed = self.failover_manager.detect_failures(self.workers)
            for failed_worker in failed:
                reassigned = self.failover_manager.failover(failed_worker, self.workers)
                for task in reassigned:
                    if task.retry_count <= task.max_retries:
                        self.task_queue.append(task)

                self.workers = self.failover_manager.remove_dead_node(self.workers, failed_worker)

            # 3. 자동 스케일링
            if self.auto_scaler.should_scale_up(self.workers):
                self.workers = self.auto_scaler.scale(self.workers, "up")
            elif self.auto_scaler.should_scale_down(self.workers):
                self.workers = self.auto_scaler.scale(self.workers, "down")

            # 4. 메트릭 기록
            self.monitor.record_metrics(self.workers, len(self.task_queue))

            # 5. 상태 출력
            for worker in self.workers:
                self.monitor.log("DEBUG", worker.get_status())

        self.is_running = False

    def get_statistics(self) -> Dict:
        """통계"""
        total_tasks = len(self.completed_tasks)
        success_count = sum(1 for t in self.completed_tasks if t.status == TaskStatus.COMPLETED)
        failed_count = sum(1 for t in self.completed_tasks if t.status == TaskStatus.FAILED)

        avg_duration = 0
        if self.completed_tasks:
            avg_duration = sum(t.duration() for t in self.completed_tasks) / total_tasks

        return {
            "total_tasks": total_tasks,
            "successful": success_count,
            "failed": failed_count,
            "success_rate": (success_count / total_tasks * 100) if total_tasks > 0 else 0,
            "avg_duration_sec": avg_duration,
            "active_nodes": len(self.workers),
            "healthy_nodes": sum(1 for w in self.workers if w.status == WorkerStatus.HEALTHY),
        }

# ═══════════════════════════════════════════════════════════════════════════
# PART 9: 데모 함수
# ═══════════════════════════════════════════════════════════════════════════

def demo_1_basic_orchestration():
    """데모 1: 기본 오케스트레이션"""
    print("\n" + "="*80)
    print("데모 1: 기본 오케스트레이션")
    print("="*80)

    engine = DistributedTaskEngine(initial_nodes=3)

    # 작업 제출
    tasks = [
        "데이터 분석 Job 1",
        "모델 학습 Job 2",
        "이미지 처리 Job 3",
        "텍스트 마이닝 Job 4",
    ]

    for task_data in tasks:
        engine.submit_task(task_data)

    # 오케스트레이션 실행
    engine.orchestrate(max_iterations=5)

    # 결과 출력
    stats = engine.get_statistics()
    print(f"\n✓ 작업 완료: {stats['total_tasks']}")
    print(f"  성공: {stats['successful']} | 실패: {stats['failed']}")
    print(f"  성공률: {stats['success_rate']:.1f}%")
    print(f"  활성 노드: {stats['active_nodes']}")

def demo_2_load_balancing():
    """데모 2: 로드 밸런싱 전략 비교"""
    print("\n" + "="*80)
    print("데모 2: 로드 밸런싱 전략")
    print("="*80)

    lb = LoadBalancer()
    workers = [WorkerNode(f"node-{i}") for i in range(3)]

    # 각 워커에 큐 길이 설정
    workers[0].metrics.task_queue_length = 10
    workers[1].metrics.task_queue_length = 5
    workers[2].metrics.task_queue_length = 15

    print("\n[라운드 로빈 전략]")
    for _ in range(3):
        w = lb.round_robin(workers)
        print(f"  선택: {w.node_id}")

    print("\n[최소 연결 전략]")
    for _ in range(3):
        w = lb.least_connection(workers)
        print(f"  선택: {w.node_id} (큐: {w.metrics.task_queue_length})")

    print("\n[헬스 기반 전략]")
    workers[0].metrics.health_score = lambda: 0.9
    workers[1].metrics.health_score = lambda: 0.5
    workers[2].metrics.health_score = lambda: 0.7

    for _ in range(3):
        w = lb.least_load(workers)
        print(f"  선택: {w.node_id}")

def demo_3_auto_scaling():
    """데모 3: 자동 스케일링"""
    print("\n" + "="*80)
    print("데모 3: 자동 스케일링")
    print("="*80)

    scaler = AutoScaler(min_nodes=2, max_nodes=5)
    workers = [WorkerNode(f"node-{i}") for i in range(2)]

    print(f"초기 노드: {len(workers)}")

    # 부하 높음 → 스케일업
    for w in workers:
        w.metrics.cpu_usage = 90
        w.metrics.memory_usage = 85
        w.metrics.task_queue_length = 100

    if scaler.should_scale_up(workers):
        workers = scaler.scale(workers, "up")
        print(f"스케일업! 노드: {len(workers)}")

    # 부하 낮음 → 스케일다운
    for w in workers:
        w.metrics.cpu_usage = 10
        w.metrics.memory_usage = 15
        w.metrics.task_queue_length = 2

    if scaler.should_scale_down(workers):
        workers = scaler.scale(workers, "down")
        print(f"스케일다운! 노드: {len(workers)}")

    print("\n스케일 액션 로그:")
    for log in scaler.scale_action_log:
        print(f"  {log}")

def demo_4_failover():
    """데모 4: 장애 복구"""
    print("\n" + "="*80)
    print("데모 4: 장애 감지 및 Failover")
    print("="*80)

    failover_mgr = FailoverManager()
    workers = [WorkerNode(f"node-{i}") for i in range(3)]

    # 작업 처리
    for i, worker in enumerate(workers):
        for j in range(3):
            task = Task(data=f"Job {i}-{j}")
            worker.process(task)

    print(f"초기 노드: {len(workers)}")
    print(f"총 작업 완료: {sum(w.metrics.completed_tasks for w in workers)}")

    # 장애 감지
    failed = failover_mgr.detect_failures(workers)
    print(f"감지된 장애 노드: {len(failed)}")

    # Failover
    for failed_worker in failed:
        reassigned = failover_mgr.failover(failed_worker, workers)
        workers = failover_mgr.remove_dead_node(workers, failed_worker)
        print(f"  {failed_worker.node_id} 장애 → {len(reassigned)} 작업 재할당")

    print(f"최종 노드: {len(workers)}")
    print(f"복구된 작업: {len(failover_mgr.recovered_tasks)}")

def demo_5_ci_cd_pipeline():
    """데모 5: CI/CD 파이프라인"""
    print("\n" + "="*80)
    print("데모 5: CI/CD 파이프라인")
    print("="*80)

    pipeline = CIPipeline()

    # Stage 1: COMMIT
    pipeline.commit("분산 엔진 v1.0 기능 추가")

    # Stage 2: TEST
    pipeline.test("test_load_balancing", True)
    pipeline.test("test_failover", True)
    pipeline.test("test_scaling", True)
    pipeline.test("test_orchestration", True)

    # Stage 3: BUILD
    build_success = pipeline.build("build-2025-02-25")

    # Stage 4: DEPLOY
    deploy_success = pipeline.deploy("6.1.0")

    print("\n[파이프라인 로그]")
    for log in pipeline.pipeline_log:
        print(f"  {log}")

    print(f"\n배포 가능: {'YES' if deploy_success else 'NO'}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 10: 단위 테스트
# ═══════════════════════════════════════════════════════════════════════════

class TestDistributedTaskEngine(unittest.TestCase):
    """분산 작업 처리 엔진 테스트"""

    def setUp(self):
        self.engine = DistributedTaskEngine(initial_nodes=3)

    def test_1_task_submission_and_processing(self):
        """테스트 1: 작업 제출 및 처리"""
        task = self.engine.submit_task("테스트 작업 1")
        self.assertEqual(task.status, TaskStatus.QUEUED)
        self.assertTrue(len(self.engine.task_queue) > 0)

    def test_2_load_balancer_selection(self):
        """테스트 2: 로드 밸런서 워커 선택"""
        lb = LoadBalancer()
        worker = lb.select_worker(self.engine.workers, strategy="health")
        self.assertIsNotNone(worker)
        self.assertIn(worker, self.engine.workers)

    def test_3_auto_scaler_decision(self):
        """테스트 3: 자동 스케일러 결정"""
        scaler = AutoScaler()
        initial_count = len(self.engine.workers)

        # 부하 높음 → 스케일업 가능 확인
        for w in self.engine.workers:
            w.metrics.cpu_usage = 95
            w.metrics.task_queue_length = 100

        should_scale_up = scaler.should_scale_up(self.engine.workers)
        self.assertTrue(should_scale_up or initial_count >= scaler.max_nodes)

    def test_4_failover_recovery(self):
        """테스트 4: 장애 복구"""
        # 작업 처리
        self.engine.submit_task("작업 A")
        self.engine.orchestrate(max_iterations=2)

        initial_completed = len(self.engine.completed_tasks)
        initial_nodes = len(self.engine.workers)

        # 장애 시뮬레이션
        if self.engine.workers:
            failed = self.engine.failover_manager.detect_failures(self.engine.workers)
            self.assertIsInstance(failed, list)

    def test_5_ci_cd_pipeline_integration(self):
        """테스트 5: CI/CD 파이프라인 통합"""
        pipeline = CIPipeline()
        pipeline.commit("테스트 코드")
        pipeline.test("unit_test_1", True)
        pipeline.test("unit_test_2", True)

        build_result = pipeline.build("build-1")
        self.assertTrue(build_result)

        deploy_result = pipeline.deploy("1.0.0")
        self.assertTrue(deploy_result)

# ═══════════════════════════════════════════════════════════════════════════
# 메인 실행
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "Python University v6.1" + " "*36 + "║")
    print("║" + " "*15 + "Distributed Task Engine & High Availability" + " "*20 + "║")
    print("║" + " "*24 + "기록이 증명이다 gogs" + " "*33 + "║")
    print("╚" + "="*78 + "╝")

    # 데모 실행
    demo_1_basic_orchestration()
    demo_2_load_balancing()
    demo_3_auto_scaling()
    demo_4_failover()
    demo_5_ci_cd_pipeline()

    # 단위 테스트 실행
    print("\n" + "="*80)
    print("단위 테스트 실행")
    print("="*80 + "\n")

    unittest.main(argv=[''], exit=False, verbosity=2)

    print("\n" + "="*80)
    print("✓ v6.1 Distributed Task Engine 완성!")
    print("  다음 단계: v6.2 클라우드 네이티브 & 보안")
    print("="*80)
    print("\n저장 필수 너는 기록이 증명이다 gogs\n")
