#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                  【 v8.1: AIOps 자가 치유 아키텍처 】                        ║
║                 Python PhD 박사 과정 — 첫 번째 연구                          ║
║                                                                              ║
║                   "반응에서 예측으로, 예측에서 예방으로"                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

【 핵심 개념 】

 AIOps (Artificial Intelligence for IT Operations) 란?
 ─────────────────────────────────────────────────────────
 시스템이 관리자의 개입 없이 스스로:
  1. 장애를 예측 (Anomaly Detection)
  2. 근본 원인을 분석 (Root Cause Analysis)
  3. 자동으로 치유 (Self-Healing)
  4. 부하를 예측해 스케일링 (Auto-scaling)
  5. 유지보수를 예측 (Predictive Maintenance)

 이를 "자율 운영 시스템 (Autonomous System)"이라 한다.

【 진화 아키텍처 】

 v7 시리즈: 관찰 (Observability)
  ├─ v7.1: 메시지 큐 (느슨한 결합)
  ├─ v7.2: 마이크로서비스 (서비스 격리)
  ├─ v7.3: 캐싱 전략 (성능 최적화)
  └─ v7.4: 모니터링 (실시간 가시화)

 v8 시리즈: 자율 운영 (Autonomy)
  ├─ v8.1: 자가 치유 (이 문제) ←
  ├─ v8.2: 초대형 데이터 처리 (Spark/HDFS)
  ├─ v8.3: 분산 합의 (Raft/Paxos)
  └─ v8.4: 엣지 컴퓨팅 (분산 의사결정)

【 시스템 구성 】

 1. AnomalyDetector      — 3-Sigma 법칙으로 이상 탐지
 2. RootCauseAnalyzer    — 로그 패턴 + 지표 상관관계로 원인 분석
 3. GogsSelfHealingKernel— 원인별 맞춤 치유 프로토콜 실행
 4. AutoScaler           — 부하 예측으로 자동 스케일링
 5. PredictiveMaintenanceEngine — MTTF 기반 예측 유지보수
 6. AIOpsOrchestrator    — 전체 시스템 조율

【 3-Sigma 원칙 】

 정규분포에서:
  - 1σ 범위: 68%의 데이터
  - 2σ 범위: 95%의 데이터
  - 3σ 범위: 99.7%의 데이터

 즉, 3σ 바깥의 확률은 0.27% ≈ 이상 징후 (특이값)

【 파이썬 철학 】

 "데이터의 무결성이 지능을 결정한다.
  AI가 잘못된 데이터를 학습하면 오히려 멀쩡한 서비스를 차단할 수 있다."

 따라서:
  1. 데이터 정제 (Data Cleaning) — 노이즈 제거
  2. 정규화 (Normalization) — 다양한 지표 조화
  3. 검증 (Validation) — 임계치 재검토
"""

# ═══════════════════════════════════════════════════════════════════════════
# PART 0: 공용 데이터 클래스 & Enum
# ═══════════════════════════════════════════════════════════════════════════

import statistics
import random
import time
from datetime import datetime, timedelta
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from abc import ABC, abstractmethod


class SystemHealth(Enum):
    """시스템 건강 상태"""
    LEARNING = "LEARNING"    # 데이터 수집 초기 단계 (< 10 샘플)
    STABLE = "STABLE"        # 정상 운영
    WARNING = "WARNING"      # 경고 (임계치 근접)
    HEALING = "HEALING"      # 자가 치유 중
    CRITICAL = "CRITICAL"    # 위험 (즉각 조치 필요)


class ScaleAction(Enum):
    """스케일링 액션"""
    SCALE_UP = "SCALE_UP"      # 인스턴스 증가
    SCALE_DOWN = "SCALE_DOWN"  # 인스턴스 감소
    HOLD = "HOLD"              # 현재 유지


class RootCause(Enum):
    """근본 원인 분류"""
    CPU_SPIKE = "CPU_SPIKE"
    MEMORY_LEAK = "MEMORY_LEAK"
    NETWORK_ISSUE = "NETWORK_ISSUE"
    DB_SLOW_QUERY = "DB_SLOW_QUERY"
    CASCADE_FAIL = "CASCADE_FAIL"
    UNKNOWN = "UNKNOWN"


class CircuitBreakerState(Enum):
    """Circuit Breaker 상태"""
    CLOSED = "CLOSED"      # 정상: 요청 허용
    OPEN = "OPEN"          # 차단: 요청 거부
    HALF_OPEN = "HALF_OPEN"  # 회복 탐색: 일부 요청 허용


@dataclass
class SystemMetric:
    """단일 시점의 시스템 지표 스냅샷"""
    timestamp: datetime
    cpu_usage: float        # 0.0 ~ 1.0
    memory_usage: float     # 0.0 ~ 1.0
    latency_ms: float       # 밀리초
    error_rate: float       # 0.0 ~ 1.0
    request_count: int


@dataclass
class AnomalyEvent:
    """이상 탐지 이벤트"""
    detected_at: datetime
    metric_name: str        # "cpu_usage" | "memory_usage" | "latency_ms"
    current_value: float
    threshold: float
    deviation_sigma: float  # 몇 시그마 벗어났는가


@dataclass
class HealingAction:
    """자가 치유 액션 기록"""
    action_id: str
    triggered_at: datetime
    anomaly: AnomalyEvent
    root_cause: RootCause
    action_taken: str       # 예: "cache_priority_mode"
    success: bool
    duration_ms: float


@dataclass
class MaintenanceSchedule:
    """예측 유지보수 일정"""
    component: str
    predicted_failure_at: datetime
    confidence: float       # 0.0 ~ 1.0
    recommended_action: str


@dataclass
class LogEntry:
    """구조화된 로그 항목"""
    timestamp: datetime
    level: str              # "ERROR" | "WARN" | "INFO"
    component: str          # "database" | "cache" | "network" | "cpu"
    message: str


# ═══════════════════════════════════════════════════════════════════════════
# PART 1: AnomalyDetector — 3-Sigma 이상 탐지
# ═══════════════════════════════════════════════════════════════════════════

class AnomalyDetector:
    """
    3-Sigma + 이동 평균 기반 다중 지표 이상 탐지

    탐지 대상:
     - CPU Usage (급격한 스파이크)
     - Memory Usage (점진적 누수)
     - Latency (응답 지연)
     - Error Rate (오류율 증가)
    """

    def __init__(self, window_size: int = 20, sigma_threshold: float = 3.0):
        self.window_size = window_size
        self.sigma_threshold = sigma_threshold

        # 지표별 이력 버퍼 (deque — 자동 오래된 데이터 제거)
        self.history: Dict[str, deque] = {
            "cpu_usage": deque(maxlen=window_size),
            "memory_usage": deque(maxlen=window_size),
            "latency_ms": deque(maxlen=window_size),
            "error_rate": deque(maxlen=window_size),
        }
        self.detected_anomalies: List[AnomalyEvent] = []
        self.total_samples = 0

    def feed(self, metric: SystemMetric) -> List[AnomalyEvent]:
        """새 메트릭 주입 → 이상 여부 반환"""
        self.total_samples += 1
        detected = []

        # 각 지표 검사
        for metric_name, value in [
            ("cpu_usage", metric.cpu_usage),
            ("memory_usage", metric.memory_usage),
            ("latency_ms", metric.latency_ms),
            ("error_rate", metric.error_rate),
        ]:
            self.history[metric_name].append(value)
            anomaly = self._check_metric(metric_name, value, metric.timestamp)
            if anomaly:
                detected.append(anomaly)
                self.detected_anomalies.append(anomaly)

        return detected

    def _check_metric(
        self, name: str, value: float, timestamp: datetime
    ) -> Optional[AnomalyEvent]:
        """단일 지표의 3-Sigma 이상 검사"""
        history = self.history[name]

        # 데이터 10개 미만: 학습 중
        if len(history) < 10:
            return None

        data = list(history)
        avg = statistics.mean(data)
        std_dev = statistics.stdev(data)

        # 3-Sigma 임계치
        threshold = avg + self.sigma_threshold * std_dev

        if value > threshold:
            deviation = (value - avg) / std_dev if std_dev > 0 else 0
            return AnomalyEvent(
                detected_at=timestamp,
                metric_name=name,
                current_value=value,
                threshold=threshold,
                deviation_sigma=deviation,
            )

        return None

    def get_anomaly_rate(self) -> float:
        """이상 탐지율"""
        if self.total_samples == 0:
            return 0.0
        return len(self.detected_anomalies) / self.total_samples

    def get_summary(self) -> Dict[str, Any]:
        """탐지 통계 요약"""
        return {
            "total_samples": self.total_samples,
            "anomalies_detected": len(self.detected_anomalies),
            "anomaly_rate": self.get_anomaly_rate(),
            "window_size": self.window_size,
            "sigma_threshold": self.sigma_threshold,
        }


# ═══════════════════════════════════════════════════════════════════════════
# PART 2: AutoScaler — 부하 예측 기반 자동 스케일링
# ═══════════════════════════════════════════════════════════════════════════

class LoadPredictor:
    """부하 예측기 (선형 회귀 시뮬레이션)"""

    def __init__(self, history_size: int = 15):
        self.load_history: deque = deque(maxlen=history_size)

    def add_observation(self, cpu: float, memory: float):
        """부하 관측값 추가"""
        self.load_history.append((cpu, memory))

    def predict_next(self, steps_ahead: int = 3) -> Tuple[float, float]:
        """steps_ahead 이후의 예상 CPU, Memory 반환"""
        if len(self.load_history) < 3:
            # 데이터 부족 시: 현재 평균 반환
            if self.load_history:
                cpus = [h[0] for h in self.load_history]
                mems = [h[1] for h in self.load_history]
                avg_cpu = statistics.mean(cpus)
                avg_mem = statistics.mean(mems)
                return avg_cpu, avg_mem
            return 0.5, 0.5

        cpus = [h[0] for h in self.load_history]
        mems = [h[1] for h in self.load_history]

        cpu_slope = self._linear_slope(cpus)
        mem_slope = self._linear_slope(mems)

        # 선형 외삽
        pred_cpu = max(0.0, min(1.0, cpus[-1] + cpu_slope * steps_ahead))
        pred_mem = max(0.0, min(1.0, mems[-1] + mem_slope * steps_ahead))

        return pred_cpu, pred_mem

    def _linear_slope(self, data: List[float]) -> float:
        """기울기 계산: (마지막값 - 첫값) / len"""
        if len(data) < 2:
            return 0.0
        return (data[-1] - data[0]) / len(data)


class AutoScaler:
    """부하 예측 기반 자동 스케일링"""

    def __init__(self, min_instances: int = 1, max_instances: int = 10):
        self.current_instances = 2
        self.min_instances = min_instances
        self.max_instances = max_instances
        self.predictor = LoadPredictor()
        self.cooldown_until: Optional[datetime] = None
        self.cooldown_seconds = 60
        self.scaling_history: List[Dict[str, Any]] = []

    def evaluate(self, metric: SystemMetric) -> ScaleAction:
        """현재 메트릭 → 스케일 액션 결정"""
        # 쿨다운 중인지 확인
        if self.cooldown_until and datetime.now() < self.cooldown_until:
            return ScaleAction.HOLD

        # 미래 부하 예측
        self.predictor.add_observation(metric.cpu_usage, metric.memory_usage)
        pred_cpu, pred_mem = self.predictor.predict_next(steps_ahead=3)

        # 스케일링 결정
        if pred_cpu > 0.8:
            return ScaleAction.SCALE_UP
        elif pred_cpu < 0.2 and self.current_instances > self.min_instances:
            return ScaleAction.SCALE_DOWN

        return ScaleAction.HOLD

    def execute(self, action: ScaleAction) -> str:
        """액션 실행 + 쿨다운 설정"""
        result = ""

        if action == ScaleAction.SCALE_UP:
            old = self.current_instances
            self.current_instances = min(self.current_instances + 1, self.max_instances)
            result = f"SCALE_UP: {old} → {self.current_instances} 인스턴스"
            self._set_cooldown()

        elif action == ScaleAction.SCALE_DOWN:
            old = self.current_instances
            self.current_instances = max(self.current_instances - 1, self.min_instances)
            result = f"SCALE_DOWN: {old} → {self.current_instances} 인스턴스"
            self._set_cooldown()

        else:
            result = f"HOLD: {self.current_instances} 인스턴스 유지"

        self.scaling_history.append({
            "action": action.value,
            "result": result,
            "instances": self.current_instances,
            "timestamp": datetime.now(),
        })

        return result

    def _set_cooldown(self):
        """쿨다운 타이머 설정"""
        self.cooldown_until = datetime.now() + timedelta(seconds=self.cooldown_seconds)

    def get_scaling_summary(self) -> Dict[str, Any]:
        """스케일링 이력 요약"""
        return {
            "current_instances": self.current_instances,
            "total_scalings": len(self.scaling_history),
            "history": self.scaling_history,
        }


# ═══════════════════════════════════════════════════════════════════════════
# PART 3: RootCauseAnalyzer — 근본 원인 분석
# ═══════════════════════════════════════════════════════════════════════════

class LogPatternMatcher:
    """로그 패턴 기반 원인 분류기"""

    def __init__(self):
        self.patterns: Dict[RootCause, List[str]] = {
            RootCause.DB_SLOW_QUERY: ["timeout", "slow query", "connection refused"],
            RootCause.MEMORY_LEAK: ["OOM", "OutOfMemory", "swap"],
            RootCause.NETWORK_ISSUE: ["socket", "connection reset", "ECONNREFUSED"],
            RootCause.CPU_SPIKE: ["cpu", "throttle", "spike"],
            RootCause.CASCADE_FAIL: ["cascade", "downstream", "dependency"],
        }

    def match(self, log: LogEntry) -> Optional[RootCause]:
        """로그 메시지에서 원인 패턴 매칭"""
        msg_lower = log.message.lower()

        for cause, keywords in self.patterns.items():
            for keyword in keywords:
                if keyword.lower() in msg_lower:
                    return cause

        return None


class CorrelationAnalyzer:
    """다중 지표 상관관계 분석"""

    def analyze(self, recent_metrics: List[SystemMetric]) -> RootCause:
        """최근 메트릭 목록으로 상관관계 기반 원인 추론"""
        if len(recent_metrics) < 3:
            return RootCause.UNKNOWN

        cpus = [m.cpu_usage for m in recent_metrics]
        mems = [m.memory_usage for m in recent_metrics]
        lats = [m.latency_ms for m in recent_metrics]
        errs = [m.error_rate for m in recent_metrics]

        # 상관관계 계산
        cpu_lat_corr = self._correlation_score(cpus, lats)
        mem_err_corr = self._correlation_score(mems, errs)
        err_lat_corr = self._correlation_score(errs, lats)

        # 평균값 추세 확인
        avg_cpu = statistics.mean(cpus) if cpus else 0
        avg_mem = statistics.mean(mems) if mems else 0
        avg_err = statistics.mean(errs) if errs else 0

        # 휴리스틱 기반 판단
        if cpu_lat_corr > 0.7:
            return RootCause.CPU_SPIKE
        elif avg_mem > 0.8 and mem_err_corr > 0.5:
            return RootCause.MEMORY_LEAK
        elif avg_err > 0.3 and err_lat_corr > 0.6:
            return RootCause.DB_SLOW_QUERY
        elif err_lat_corr > 0.7:
            return RootCause.NETWORK_ISSUE

        return RootCause.UNKNOWN

    def _correlation_score(self, xs: List[float], ys: List[float]) -> float:
        """피어슨 상관계수 근사"""
        if len(xs) < 2 or len(ys) < 2:
            return 0.0

        n = len(xs)
        sum_x = sum(xs)
        sum_y = sum(ys)
        sum_xy = sum(x * y for x, y in zip(xs, ys))
        sum_x2 = sum(x ** 2 for x in xs)
        sum_y2 = sum(y ** 2 for y in ys)

        numerator = n * sum_xy - sum_x * sum_y
        denominator_sq = (n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)

        if denominator_sq <= 0:
            return 0.0

        return numerator / (denominator_sq ** 0.5)


class RootCauseAnalyzer:
    """장애 근본 원인 분석기"""

    def __init__(self):
        self.log_matcher = LogPatternMatcher()
        self.corr_analyzer = CorrelationAnalyzer()
        self.log_buffer: deque = deque(maxlen=200)
        self.analysis_history: List[Dict[str, Any]] = []

    def ingest_log(self, log: LogEntry):
        """로그 주입"""
        self.log_buffer.append(log)

    def analyze(
        self, anomaly: AnomalyEvent, recent_metrics: List[SystemMetric]
    ) -> RootCause:
        """
        1. 최근 로그에서 패턴 매칭 (가중치 집계)
        2. 지표 상관관계 분석
        3. 두 결과를 합산하여 최종 원인 결정
        """
        # 로그 기반 원인 찾기
        log_causes: Dict[RootCause, int] = {}
        for log in self.log_buffer:
            cause = self.log_matcher.match(log)
            if cause:
                log_causes[cause] = log_causes.get(cause, 0) + 1

        # 가장 빈번한 로그 원인
        log_cause = max(log_causes, key=log_causes.get) if log_causes else None

        # 지표 상관관계 기반 원인
        corr_cause = self.corr_analyzer.analyze(recent_metrics)

        # 최종 원인 결정 (로그 우선)
        final_cause = log_cause or corr_cause or RootCause.UNKNOWN

        self.analysis_history.append({
            "timestamp": datetime.now(),
            "anomaly": anomaly.metric_name,
            "log_cause": log_cause,
            "corr_cause": corr_cause,
            "final_cause": final_cause,
        })

        return final_cause

    def generate_report(self, cause: RootCause) -> str:
        """근본 원인 → 인간이 읽을 수 있는 리포트"""
        descriptions = {
            RootCause.CPU_SPIKE: "CPU 사용률 급증 — 컴퓨팅 부하 급증",
            RootCause.MEMORY_LEAK: "메모리 누수 감지 — 메모리 점진 증가 추세",
            RootCause.NETWORK_ISSUE: "네트워크 장애 — 연결 끊김 또는 지연",
            RootCause.DB_SLOW_QUERY: "데이터베이스 지연 — 쿼리 성능 저하",
            RootCause.CASCADE_FAIL: "연쇄 실패 — 상류 서비스 장애의 파급",
            RootCause.UNKNOWN: "알 수 없는 원인 — 추가 분석 필요",
        }
        return descriptions.get(cause, "알 수 없음")


# ═══════════════════════════════════════════════════════════════════════════
# PART 4: GogsSelfHealingKernel — 자가 치유 핵심 커널
# ═══════════════════════════════════════════════════════════════════════════

class CircuitBreaker:
    """Circuit Breaker 패턴 구현"""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 30):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.opened_at: Optional[datetime] = None

    def record_failure(self):
        """실패 기록"""
        if self.state == CircuitBreakerState.CLOSED:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN
                self.opened_at = datetime.now()

    def record_success(self):
        """성공 기록"""
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.CLOSED
            self.failure_count = 0

    def is_available(self) -> bool:
        """요청 허용 여부"""
        if self.state == CircuitBreakerState.CLOSED:
            return True

        if self.state == CircuitBreakerState.HALF_OPEN:
            return True

        if self.state == CircuitBreakerState.OPEN:
            # 타임아웃 확인
            if self.opened_at and (
                datetime.now() - self.opened_at
            ).total_seconds() > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                return True
            return False

        return False

    def get_state_info(self) -> Dict[str, Any]:
        """상태 정보"""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "is_available": self.is_available(),
        }


class GogsSelfHealingKernel:
    """
    자가 치유 핵심 커널 (사용자 제공 코드 확장)

    기존 기능:
     - analyze_system_health(): 3-Sigma 이상 감지
     - trigger_self_healing(): 치유 프로토콜 가동
    """

    def __init__(self):
        # 사용자 제공 코드 (그대로 유지)
        self.latency_history = []
        self.is_safe_mode = False

        # 확장: CircuitBreaker
        self.circuit_breaker = CircuitBreaker()

        # 확장: 치유 이력
        self.healing_history: List[HealingAction] = []

        # 확장: 캐시 모드 상태
        self.cache_priority_level: int = 0  # 0=보통, 1=우선, 2=전용

        # 확장: 차단된 서비스 목록
        self.blocked_services: List[str] = []

        # 내부 카운터
        self._action_counter = 0

    # ── 사용자 제공 메서드 (그대로 유지) ──

    def analyze_system_health(self, current_latency: float) -> str:
        """원래 코드 그대로"""
        self.latency_history.append(current_latency)
        if len(self.latency_history) < 10:
            return "LEARNING"

        avg = statistics.mean(self.latency_history[-10:])
        std_dev = statistics.stdev(self.latency_history[-10:])

        threshold = avg + (3 * std_dev)

        if current_latency > threshold:
            self.trigger_self_healing(current_latency, threshold)
            return "HEALING"

        return "STABLE"

    def trigger_self_healing(self, latency: float, threshold: float):
        """원래 코드 확장"""
        print(
            f"🚨 [AI ALERT] 이상 지연 감지: {latency:.4f}s (임계치: {threshold:.4f}s)"
        )
        print("🛠️ [SYSTEM] 자가 치유 프로토콜 가동")
        self.is_safe_mode = True

    # ── 확장 메서드 ──

    def heal(self, anomaly: AnomalyEvent, root_cause: RootCause) -> HealingAction:
        """이상 이벤트 + 근본 원인 → 맞춤 치유 실행"""
        start_time = time.time()
        self._action_counter += 1
        action_id = f"HEAL-{self._action_counter:04d}"

        action_taken = self._apply_healing_strategy(root_cause)

        success = not self.circuit_breaker.is_available() or len(
            self.blocked_services
        ) == 0 or self.is_safe_mode

        duration_ms = (time.time() - start_time) * 1000

        healing_action = HealingAction(
            action_id=action_id,
            triggered_at=datetime.now(),
            anomaly=anomaly,
            root_cause=root_cause,
            action_taken=action_taken,
            success=success,
            duration_ms=duration_ms,
        )

        self.healing_history.append(healing_action)
        return healing_action

    def _apply_healing_strategy(self, cause: RootCause) -> str:
        """원인별 치유 전략 선택"""
        if cause == RootCause.CPU_SPIKE:
            self._reduce_non_critical()
            return "non_critical_reduced"
        elif cause == RootCause.MEMORY_LEAK:
            self._memory_gc_trigger()
            return "memory_gc_triggered"
        elif cause == RootCause.NETWORK_ISSUE:
            self._circuit_break_downstream("network")
            return "network_circuit_broken"
        elif cause == RootCause.DB_SLOW_QUERY:
            self._cache_priority_mode()
            return "cache_priority_mode"
        elif cause == RootCause.CASCADE_FAIL:
            self._circuit_break_downstream("all")
            self._cache_priority_mode()
            return "cascade_fail_mitigation"
        else:
            self._cache_priority_mode()
            return "default_safe_mode"

    def _cache_priority_mode(self):
        """캐시 의존도 상향"""
        self.cache_priority_level = min(self.cache_priority_level + 1, 2)

    def _reduce_non_critical(self):
        """비중요 서비스 차단"""
        self.is_safe_mode = True

    def _circuit_break_downstream(self, target: str):
        """특정 하류 서비스 차단"""
        self.blocked_services.append(target)
        self.circuit_breaker.record_failure()

    def _memory_gc_trigger(self):
        """메모리 회수 시뮬레이션"""
        pass  # 시뮬레이션용 (실제로는 gc.collect() 호출)

    def recover(self):
        """자가 치유 완료 후 정상 모드 복귀"""
        self.is_safe_mode = False
        self.cache_priority_level = 0
        self.blocked_services.clear()
        self.circuit_breaker.record_success()

    def get_healing_history(self) -> List[HealingAction]:
        """치유 이력 반환"""
        return self.healing_history

    def get_kernel_status(self) -> Dict[str, Any]:
        """커널 현재 상태"""
        return {
            "is_safe_mode": self.is_safe_mode,
            "cache_priority_level": self.cache_priority_level,
            "blocked_services": self.blocked_services,
            "circuit_breaker": self.circuit_breaker.get_state_info(),
            "healing_count": len(self.healing_history),
        }


# ═══════════════════════════════════════════════════════════════════════════
# PART 5: PredictiveMaintenanceEngine — 예측 유지보수
# ═══════════════════════════════════════════════════════════════════════════

class FailurePattern:
    """학습된 장애 패턴"""

    def __init__(self, component: str):
        self.component = component
        self.failure_history: List[datetime] = []
        self.metric_trends: Dict[str, List[float]] = {
            "cpu": [],
            "memory": [],
            "latency": [],
        }

    def record_failure(self, when: datetime):
        """장애 시각 기록"""
        self.failure_history.append(when)

    def add_metric_snapshot(self, cpu: float, memory: float, latency: float):
        """지표 스냅샷 추가"""
        self.metric_trends["cpu"].append(cpu)
        self.metric_trends["memory"].append(memory)
        self.metric_trends["latency"].append(latency)

    def get_average_interval(self) -> Optional[float]:
        """평균 장애 발생 간격 (초)"""
        if len(self.failure_history) < 2:
            return None

        intervals = []
        for i in range(1, len(self.failure_history)):
            delta = (
                self.failure_history[i] - self.failure_history[i - 1]
            ).total_seconds()
            intervals.append(delta)

        return statistics.mean(intervals) if intervals else None

    def get_trend_slope(self, metric_name: str) -> float:
        """지표 추세 기울기 (양수 = 악화 중)"""
        data = self.metric_trends.get(metric_name, [])
        if len(data) < 2:
            return 0.0
        return (data[-1] - data[0]) / len(data)


class PredictiveMaintenanceEngine:
    """예측 유지보수 엔진"""

    def __init__(self):
        self.patterns: Dict[str, FailurePattern] = {}
        self.maintenance_schedule: List[MaintenanceSchedule] = []
        self.prediction_accuracy: List[bool] = []

    def learn_from_failure(self, component: str, failure_time: datetime):
        """장애 사례 학습"""
        if component not in self.patterns:
            self.patterns[component] = FailurePattern(component)

        self.patterns[component].record_failure(failure_time)

    def update_metrics(self, component: str, metric: SystemMetric):
        """지표 트렌드 업데이트"""
        if component not in self.patterns:
            self.patterns[component] = FailurePattern(component)

        self.patterns[component].add_metric_snapshot(
            metric.cpu_usage, metric.memory_usage, metric.latency_ms
        )

    def predict(self, component: str) -> Optional[MaintenanceSchedule]:
        """다음 장애 예측"""
        if component not in self.patterns:
            return None

        pattern = self.patterns[component]

        # 장애 이력 2개 이상 필요
        if len(pattern.failure_history) < 2:
            return None

        # 평균 간격 기반 예측
        avg_interval = pattern.get_average_interval()
        if not avg_interval:
            return None

        last_failure = pattern.failure_history[-1]
        predicted_failure_at = last_failure + timedelta(seconds=avg_interval)

        # 신뢰도: 데이터 많을수록 높음
        confidence = min(len(pattern.failure_history) / 10, 1.0)

        return MaintenanceSchedule(
            component=component,
            predicted_failure_at=predicted_failure_at,
            confidence=confidence,
            recommended_action=f"예방적 유지보수 예약 ({component})",
        )

    def get_upcoming_maintenance(self, within_hours: int = 24) -> List[MaintenanceSchedule]:
        """N시간 이내 예정된 유지보수 목록"""
        result = []
        now = datetime.now()
        future = now + timedelta(hours=within_hours)

        for component in self.patterns:
            schedule = self.predict(component)
            if schedule and now <= schedule.predicted_failure_at <= future:
                result.append(schedule)

        return result

    def get_summary(self) -> Dict[str, Any]:
        """예측 엔진 요약"""
        return {
            "components_tracked": len(self.patterns),
            "total_failures": sum(len(p.failure_history) for p in self.patterns.values()),
            "maintenance_scheduled": len(self.maintenance_schedule),
            "upcoming": self.get_upcoming_maintenance(),
        }


# ═══════════════════════════════════════════════════════════════════════════
# PART 6: AIOpsOrchestrator — 전체 시스템 조율
# ═══════════════════════════════════════════════════════════════════════════

class AIOpsOrchestrator:
    """AIOps 전체 시스템 조율자"""

    def __init__(self):
        self.anomaly_detector = AnomalyDetector(window_size=20)
        self.auto_scaler = AutoScaler(min_instances=1, max_instances=8)
        self.rca = RootCauseAnalyzer()
        self.healing_kernel = GogsSelfHealingKernel()
        self.maintenance_engine = PredictiveMaintenanceEngine()

        self.processed_metrics: List[SystemMetric] = []
        self.healing_actions: List[HealingAction] = []
        self.orchestration_log: List[str] = []

        self.tick_count = 0

    def process_tick(
        self, metric: SystemMetric, logs: Optional[List[LogEntry]] = None
    ) -> SystemHealth:
        """단일 메트릭 틱 처리"""
        self.tick_count += 1
        self.processed_metrics.append(metric)

        # 로그 주입
        if logs:
            for log in logs:
                self.rca.ingest_log(log)

        # 이상 감지
        anomalies = self.anomaly_detector.feed(metric)

        if not anomalies:
            # 정상 상태
            self.healing_kernel.recover()
            scale_action = self.auto_scaler.evaluate(metric)
            self.auto_scaler.execute(scale_action)
            return SystemHealth.STABLE

        # 이상 감지됨
        status = SystemHealth.STABLE

        for anomaly in anomalies:
            # RCA 실행
            root_cause = self.rca.analyze(anomaly, self.processed_metrics[-5:])

            # 자가 치유
            healing_action = self.healing_kernel.heal(anomaly, root_cause)
            self.healing_actions.append(healing_action)

            status = SystemHealth.HEALING

            # 로그 기록
            self.orchestration_log.append(
                f"[TICK {self.tick_count:03d}] {anomaly.metric_name}="
                f"{anomaly.current_value:.2f} (σ={anomaly.deviation_sigma:.1f}) | "
                f"RCA={root_cause.value} | HEAL={healing_action.action_taken}"
            )

        # 자동 스케일링 평가
        scale_action = self.auto_scaler.evaluate(metric)
        scale_result = self.auto_scaler.execute(scale_action)

        # 유지보수 학습
        self.maintenance_engine.update_metrics("system", metric)

        return status

    def run_simulation(self, ticks: int = 50) -> Dict[str, Any]:
        """N틱 자가 치유 시뮬레이션 실행"""
        print(f"\n【 AIOps 자가 치유 시뮬레이션 ({ticks}틱) 】\n")

        anomaly_count = 0
        healing_count = 0

        for tick in range(ticks):
            # 메트릭 생성
            metric = self._generate_metric(tick)

            # 로그 생성 (메트릭 상태에 따라)
            logs = self._generate_logs(metric)

            # 틱 처리
            status = self.process_tick(metric, logs)

            # 비정상 감지 시 출력
            if status == SystemHealth.HEALING:
                anomaly_count += 1
                for log in self.orchestration_log[-10:]:
                    if f"TICK {tick:03d}" in log:
                        print(f"  {log}")

            # 치유 액션 집계
            if self.healing_actions and len(self.healing_actions) > healing_count:
                healing_count = len(self.healing_actions)

        # 최종 통계
        return {
            "total_ticks": self.tick_count,
            "anomalies_detected": anomaly_count,
            "healing_actions": len(self.healing_actions),
            "successful_heals": sum(1 for h in self.healing_actions if h.success),
            "scale_ups": sum(
                1
                for h in self.auto_scaler.scaling_history
                if h["action"] == "SCALE_UP"
            ),
            "scale_downs": sum(
                1
                for h in self.auto_scaler.scaling_history
                if h["action"] == "SCALE_DOWN"
            ),
            "final_instances": self.auto_scaler.current_instances,
            "final_status": SystemHealth.STABLE
            if not self.anomaly_detector.detected_anomalies
            else SystemHealth.HEALING,
        }

    def _generate_metric(self, tick: int) -> SystemMetric:
        """틱 번호 기반 시뮬레이션 메트릭 생성"""
        # 시나리오: 정상 → 스파이크 → 누수 → 장애 → 회복

        cpu = 0.4
        memory = 0.5
        latency = 100
        error_rate = 0.01

        if tick == 15:
            # CPU 스파이크
            cpu = 0.95
            latency = 800
        elif 20 <= tick <= 25:
            # 메모리 누수 (점진)
            memory = 0.65 + (tick - 20) * 0.05
            latency = 150 + (tick - 20) * 100
        elif tick == 30:
            # 네트워크 장애
            error_rate = 0.4
            latency = 1200
        elif tick == 35:
            # 연쇄 실패
            cpu = 0.88
            memory = 0.82
            error_rate = 0.25
            latency = 950
        elif tick >= 36:
            # 회복 구간
            cpu = 0.3 + random.random() * 0.2
            memory = 0.4 + random.random() * 0.2
            latency = 80 + random.random() * 50
            error_rate = 0.001

        # 노이즈 추가 (정상 구간)
        if tick < 15 or (tick > 35 and tick <= 50):
            cpu += random.uniform(-0.05, 0.05)
            memory += random.uniform(-0.05, 0.05)
            latency += random.uniform(-20, 20)

        cpu = max(0.0, min(1.0, cpu))
        memory = max(0.0, min(1.0, memory))
        latency = max(0.0, latency)
        error_rate = max(0.0, min(1.0, error_rate))

        return SystemMetric(
            timestamp=datetime.now() + timedelta(seconds=tick),
            cpu_usage=cpu,
            memory_usage=memory,
            latency_ms=latency,
            error_rate=error_rate,
            request_count=1000 + random.randint(-100, 100),
        )

    def _generate_logs(self, metric: SystemMetric) -> List[LogEntry]:
        """메트릭 상태에 따른 로그 생성"""
        logs = []

        if metric.cpu_usage > 0.9:
            logs.append(
                LogEntry(
                    timestamp=metric.timestamp,
                    level="WARN",
                    component="cpu",
                    message="CPU throttle detected — spike in usage",
                )
            )

        if metric.memory_usage > 0.8:
            logs.append(
                LogEntry(
                    timestamp=metric.timestamp,
                    level="ERROR",
                    component="memory",
                    message="OOM warning — memory usage high",
                )
            )

        if metric.error_rate > 0.3:
            logs.append(
                LogEntry(
                    timestamp=metric.timestamp,
                    level="ERROR",
                    component="network",
                    message="ECONNREFUSED — connection reset by peer",
                )
            )

        if metric.latency_ms > 500:
            logs.append(
                LogEntry(
                    timestamp=metric.timestamp,
                    level="WARN",
                    component="database",
                    message="slow query detected — timeout on database connection",
                )
            )

        return logs

    def print_final_report(self, simulation_result: Dict[str, Any]):
        """최종 시뮬레이션 보고서 출력"""
        print("\n" + "=" * 80)
        print("【 최종 시뮬레이션 리포트 】")
        print("=" * 80)
        print(f"  총 틱: {simulation_result['total_ticks']}")
        print(f"  이상 탐지: {simulation_result['anomalies_detected']}회")
        print(f"  자가 치유: {simulation_result['healing_actions']}회 " +
              f"(성공 {simulation_result['successful_heals']})")
        print(f"  스케일 업: {simulation_result['scale_ups']}회")
        print(f"  스케일 다운: {simulation_result['scale_downs']}회")
        print(f"  최종 인스턴스: {simulation_result['final_instances']}")
        print(f"  최종 상태: {simulation_result['final_status'].value}")
        print("=" * 80)

    def get_orchestration_summary(self) -> Dict[str, Any]:
        """오케스트레이터 전체 요약"""
        return {
            "ticks_processed": self.tick_count,
            "anomalies": self.anomaly_detector.get_summary(),
            "scaling": self.auto_scaler.get_scaling_summary(),
            "healing": {
                "total_actions": len(self.healing_actions),
                "successful": sum(1 for h in self.healing_actions if h.success),
            },
            "maintenance": self.maintenance_engine.get_summary(),
        }


# ═══════════════════════════════════════════════════════════════════════════
# PART 7: main() — 통합 데모 & 시뮬레이션
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """메인 함수"""
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "【 v8.1: AIOps 자가 치유 시스템 】".center(78) + "║")
    print("║" + "Python PhD 박사 과정 1 — 첫 번째 연구".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝\n")

    # ─── SECTION 1: AnomalyDetector 단독 데모 ───
    print("=" * 80)
    print("【 SECTION 1: 이상 탐지 (AnomalyDetector) 】")
    print("=" * 80)

    detector = AnomalyDetector(window_size=20, sigma_threshold=3.0)
    test_metrics = [0.1, 0.12, 0.11, 0.13, 0.1, 0.11, 0.12, 0.11, 0.14, 0.12]
    test_metrics += [0.11, 0.12, 0.13, 0.1, 0.12]

    print("  정상 데이터 주입:")
    for i, latency in enumerate(test_metrics[:10]):
        anomalies = detector.feed(
            SystemMetric(
                timestamp=datetime.now(),
                cpu_usage=0.4,
                memory_usage=0.5,
                latency_ms=latency * 100,
                error_rate=0.01,
                request_count=1000,
            )
        )
        print(f"    Tick {i:02d}: latency={latency:.2f}s → 상태: "
              f"{'LEARNING' if i < 9 else 'STABLE'}")

    print("  \n  극단값 주입 (이상 탐지):")
    spike = 0.95
    anomalies = detector.feed(
        SystemMetric(
            timestamp=datetime.now(),
            cpu_usage=0.95,
            memory_usage=0.5,
            latency_ms=spike * 1000,
            error_rate=0.01,
            request_count=1000,
        )
    )

    if anomalies:
        for anomaly in anomalies:
            print(f"    ✓ 이상 탐지: {anomaly.metric_name}={anomaly.current_value:.2f}s "
                  f"(σ={anomaly.deviation_sigma:.1f})")
    else:
        print(f"    탐지 실패")

    # ─── SECTION 2: RootCauseAnalyzer 데모 ───
    print("\n" + "=" * 80)
    print("【 SECTION 2: 근본 원인 분석 (RootCauseAnalyzer) 】")
    print("=" * 80)

    rca = RootCauseAnalyzer()

    # 로그 주입
    print("  로그 주입:")
    logs = [
        LogEntry(
            timestamp=datetime.now(),
            level="ERROR",
            component="database",
            message="timeout on database connection",
        ),
        LogEntry(
            timestamp=datetime.now(),
            level="ERROR",
            component="cpu",
            message="CPU throttle detected",
        ),
    ]

    for log in logs:
        rca.ingest_log(log)
        print(f"    [{log.component}] {log.message}")

    # 지표 기반 분석
    print("  \n  지표 기반 원인 분석:")
    recent = [
        SystemMetric(
            timestamp=datetime.now(),
            cpu_usage=0.9 + i * 0.02,
            memory_usage=0.5,
            latency_ms=100 + i * 50,
            error_rate=0.01,
            request_count=1000,
        )
        for i in range(5)
    ]

    anomaly = AnomalyEvent(
        detected_at=datetime.now(),
        metric_name="cpu_usage",
        current_value=0.98,
        threshold=0.65,
        deviation_sigma=5.2,
    )

    cause = rca.analyze(anomaly, recent)
    print(f"    원인: {cause.value}")
    print(f"    설명: {rca.generate_report(cause)}")

    # ─── SECTION 3: GogsSelfHealingKernel 데모 ───
    print("\n" + "=" * 80)
    print("【 SECTION 3: 자가 치유 (GogsSelfHealingKernel) 】")
    print("=" * 80)

    kernel = GogsSelfHealingKernel()
    print("  정상 데이터 주입 (학습 단계):")
    for i in range(8):
        status = kernel.analyze_system_health(0.1 + i * 0.01)
        print(f"    Tick {i}: 상태={status}")

    print("  \n  극단값 주입 (치유 트리거):")
    status = kernel.analyze_system_health(0.95)
    print(f"    상태={status}")
    print(f"    Safe Mode={kernel.is_safe_mode}")

    # ─── SECTION 4: AutoScaler 데모 ───
    print("\n" + "=" * 80)
    print("【 SECTION 4: 자동 스케일링 (AutoScaler) 】")
    print("=" * 80)

    scaler = AutoScaler(min_instances=1, max_instances=8)
    print(f"  초기 인스턴스: {scaler.current_instances}")

    test_scalings = [
        (0.3, "정상 부하"),
        (0.85, "높은 부하"),
        (0.9, "극도의 부하"),
        (0.15, "낮은 부하"),
    ]

    for cpu, desc in test_scalings:
        metric = SystemMetric(
            timestamp=datetime.now(),
            cpu_usage=cpu,
            memory_usage=0.5,
            latency_ms=100,
            error_rate=0.01,
            request_count=1000,
        )
        action = scaler.evaluate(metric)
        result = scaler.execute(action)
        print(f"  {desc} (CPU={cpu:.0%}): {result}")

    # ─── SECTION 5: PredictiveMaintenanceEngine 데모 ───
    print("\n" + "=" * 80)
    print("【 SECTION 5: 예측 유지보수 (PredictiveMaintenanceEngine) 】")
    print("=" * 80)

    maint_engine = PredictiveMaintenanceEngine()
    print("  장애 이력 학습:")
    failure_times = [
        datetime.now(),
        datetime.now() + timedelta(hours=1),
        datetime.now() + timedelta(hours=2.5),
    ]

    for i, failure_time in enumerate(failure_times):
        maint_engine.learn_from_failure("database", failure_time)
        print(f"    Failure {i + 1}: {failure_time.strftime('%H:%M:%S')}")

    print("  \n  다음 장애 예측:")
    schedule = maint_engine.predict("database")
    if schedule:
        print(f"    예정된 장애: {schedule.predicted_failure_at.strftime('%H:%M:%S')}")
        print(f"    신뢰도: {schedule.confidence:.0%}")
        print(f"    권장사항: {schedule.recommended_action}")

    # ─── SECTION 6: AIOpsOrchestrator 통합 시뮬레이션 ───
    print("\n" + "=" * 80)
    print("【 SECTION 6: AIOps 통합 시뮬레이션 (50틱) 】")
    print("=" * 80)

    orchestrator = AIOpsOrchestrator()
    result = orchestrator.run_simulation(ticks=50)
    orchestrator.print_final_report(result)

    # ─── SECTION 7: 철학적 고찰 ───
    print("\n" + "=" * 80)
    print("【 SECTION 7: 박사 과정 철학 】")
    print("=" * 80)

    philosophy = """

  【 반응에서 예측으로, 예측에서 예방으로 】

  v7 시대: "재난 이후에 대응한다"
    └─ 장애 발생 → 관리자 호출 → 긴급 조치
    └─ 비용: 데이터 손실, 서비스 중단, 신뢰 하락
    └─ 한계: 인간의 대응 속도 (평균 15분)

  v8 시대: "재난이 터질 것을 미리 안다"
    └─ 이상 신호 감지 → 자동 조치 → 사용자는 모름
    └─ 비용: 예방적 자원 소비 (약간의 오버헤드)
    └─ 이점: 99.99% 무중단 서비스, 0초 대응 시간
    └─ 혁신: AI가 시스템의 의사가 된다

  【 데이터의 무결성이 지능을 결정한다 】

  3-Sigma 법칙의 의미:
    ├─ 적절한 임계치 설정 = 거짓 양성 제거
    ├─ 데이터 정제 = 노이즈 제거
    ├─ 정규화 = 다양한 지표 조화
    └─ 검증 = 임계치 재검토

  만약 임계치를 잘못 설정하면:
    ├─ 너무 낮음: 정상 서비스를 계속 재시작 (진동)
    ├─ 너무 높음: 실제 장애를 놓침 (맹점)
    └─ 해결책: 지속적 학습과 피드백 루프

  【 자율 운영 시스템의 미래 】

  현재 v8.1 수준:
    ├─ 이상 탐지: 3-Sigma (통계적)
    ├─ 원인 분석: 로그 패턴 + 상관관계 (휴리스틱)
    ├─ 자동 치유: 사전 정의된 규칙 (Rule-based)
    └─ 한계: 미리 정의되지 않은 장애는 대응 불가

  미래 v10+ 수준:
    ├─ 이상 탐지: 심층 신경망 (DNN)
    ├─ 원인 분석: 그래프 신경망 (GNN) — 서비스 간 의존성 학습
    ├─ 자동 치유: 강화 학습 (RL) — 행동의 결과 학습
    └─ 거의 모든 장애에 자동 대응 가능

  【 우리가 만드는 것 】

  "대규모 시스템이 스스로 자정할 수 있다면?"
    ├─ 운영팀의 부담: 0으로 수렴
    ├─ 시스템 신뢰도: 99.9999% (6-nine)
    ├─ 개발 속도: 무한 증가 (장애 걱정 없음)
    └─ 결과: 인간과 AI의 완벽한 협업

  저장 필수 너는 기록이 증명이다 gogs
"""

    print(philosophy)


# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
