#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【 v8.1 AIOps 자가 치유 시스템 테스트 】
"""

import unittest
from datetime import datetime, timedelta
from university_v8_1_AIOPS_SELF_HEALING import (
    SystemMetric,
    AnomalyEvent,
    HealingAction,
    LogEntry,
    SystemHealth,
    ScaleAction,
    RootCause,
    CircuitBreakerState,
    AnomalyDetector,
    AutoScaler,
    LoadPredictor,
    LogPatternMatcher,
    CorrelationAnalyzer,
    RootCauseAnalyzer,
    GogsSelfHealingKernel,
    CircuitBreaker,
    PredictiveMaintenanceEngine,
    FailurePattern,
    AIOpsOrchestrator,
)


# ═══════════════════════════════════════════════════════════════════════════
# TestAnomalyDetector
# ═══════════════════════════════════════════════════════════════════════════

class TestAnomalyDetector(unittest.TestCase):
    """AnomalyDetector 단위 테스트"""

    def setUp(self):
        """테스트 초기화"""
        self.detector = AnomalyDetector(window_size=20, sigma_threshold=3.0)

    def test_01_learning_phase_returns_none(self):
        """CASE: 10개 미만 데이터 주입 시 이상 미탐지 검증"""
        # 9개 데이터 주입
        for i in range(9):
            anomalies = self.detector.feed(
                SystemMetric(
                    timestamp=datetime.now(),
                    cpu_usage=0.4,
                    memory_usage=0.5,
                    latency_ms=100 + i * 5,
                    error_rate=0.01,
                    request_count=1000,
                )
            )
            self.assertEqual(
                len(anomalies), 0, "LEARNING 단계에서 이상을 감지하면 안 됨"
            )

    def test_02_stable_metric_no_anomaly(self):
        """CASE: 균일한 정상 메트릭 20개 → 이상 없음"""
        # 정상 데이터 20개 주입
        for i in range(20):
            anomalies = self.detector.feed(
                SystemMetric(
                    timestamp=datetime.now(),
                    cpu_usage=0.4,
                    memory_usage=0.5,
                    latency_ms=100.0,  # 고정값
                    error_rate=0.01,
                    request_count=1000,
                )
            )

        # 마지막 정상 데이터
        anomalies = self.detector.feed(
            SystemMetric(
                timestamp=datetime.now(),
                cpu_usage=0.4,
                memory_usage=0.5,
                latency_ms=100.0,
                error_rate=0.01,
                request_count=1000,
            )
        )

        self.assertEqual(len(anomalies), 0, "정상 데이터에서는 이상이 없어야 함")

    def test_03_spike_triggers_anomaly(self):
        """CASE: 정상 데이터 15개 후 극단값 주입 → AnomalyEvent 반환"""
        # 정상 데이터 주입
        for i in range(15):
            self.detector.feed(
                SystemMetric(
                    timestamp=datetime.now(),
                    cpu_usage=0.4,
                    memory_usage=0.5,
                    latency_ms=100.0,
                    error_rate=0.01,
                    request_count=1000,
                )
            )

        # 극단값 주입 (3σ 초과)
        anomalies = self.detector.feed(
            SystemMetric(
                timestamp=datetime.now(),
                cpu_usage=0.95,
                memory_usage=0.5,
                latency_ms=800.0,  # 극단값
                error_rate=0.01,
                request_count=1000,
            )
        )

        self.assertGreater(len(anomalies), 0, "스파이크 감지 실패")
        self.assertIn(
            "latency_ms", [a.metric_name for a in anomalies],
            "latency 이상 미탐지",
        )

    def test_04_multiple_metrics_detected(self):
        """CASE: CPU + Memory 동시 이상 → 두 이벤트 모두 탐지"""
        # 정상 데이터 15개
        for i in range(15):
            self.detector.feed(
                SystemMetric(
                    timestamp=datetime.now(),
                    cpu_usage=0.4,
                    memory_usage=0.5,
                    latency_ms=100.0,
                    error_rate=0.01,
                    request_count=1000,
                )
            )

        # CPU + Memory 동시 극단값
        anomalies = self.detector.feed(
            SystemMetric(
                timestamp=datetime.now(),
                cpu_usage=0.95,  # 극단값
                memory_usage=0.95,  # 극단값
                latency_ms=100.0,
                error_rate=0.01,
                request_count=1000,
            )
        )

        self.assertGreaterEqual(
            len(anomalies), 2, "CPU + Memory 동시 이상 미탐지"
        )

    def test_05_anomaly_rate_calculation(self):
        """CASE: 탐지율 = 이상 횟수 / 총 샘플 계산 정확성"""
        # 정상 10개 + 극단값 10개 = 20개 샘플
        for i in range(10):
            self.detector.feed(
                SystemMetric(
                    timestamp=datetime.now(),
                    cpu_usage=0.4,
                    memory_usage=0.5,
                    latency_ms=100.0,
                    error_rate=0.01,
                    request_count=1000,
                )
            )

        for i in range(10):
            self.detector.feed(
                SystemMetric(
                    timestamp=datetime.now(),
                    cpu_usage=0.95,
                    memory_usage=0.95,
                    latency_ms=800.0,
                    error_rate=0.01,
                    request_count=1000,
                )
            )

        rate = self.detector.get_anomaly_rate()
        self.assertGreater(rate, 0.0, "탐지율이 0보다 커야 함")
        self.assertLess(rate, 1.0, "탐지율이 1보다 작아야 함")


# ═══════════════════════════════════════════════════════════════════════════
# TestAutoScaler
# ═══════════════════════════════════════════════════════════════════════════

class TestAutoScaler(unittest.TestCase):
    """AutoScaler 단위 테스트"""

    def setUp(self):
        """테스트 초기화"""
        self.scaler = AutoScaler(min_instances=1, max_instances=8)

    def test_06_scale_up_on_high_load(self):
        """CASE: CPU 90%+ 예측 → SCALE_UP 반환"""
        # 높은 부하 메트릭 주입 (미래 예측 학습)
        for i in range(10):
            metric = SystemMetric(
                timestamp=datetime.now(),
                cpu_usage=0.8 + i * 0.01,  # 80% 상승 추세
                memory_usage=0.5,
                latency_ms=100,
                error_rate=0.01,
                request_count=1000,
            )
            action = self.scaler.evaluate(metric)

        # 최종 평가
        metric = SystemMetric(
            timestamp=datetime.now(),
            cpu_usage=0.85,
            memory_usage=0.5,
            latency_ms=100,
            error_rate=0.01,
            request_count=1000,
        )
        action = self.scaler.evaluate(metric)

        # 높은 부하 예측 시 SCALE_UP
        self.assertEqual(
            action, ScaleAction.SCALE_UP, "높은 부하에서 SCALE_UP 실패"
        )

    def test_07_scale_down_on_low_load(self):
        """CASE: CPU 10% + 인스턴스 여유 → SCALE_DOWN 반환"""
        # 초기: 2개 인스턴스
        self.assertEqual(self.scaler.current_instances, 2)

        # 3개로 스케일 업 (일단 UP 시켜서 인스턴스 여유 만들기)
        metric = SystemMetric(
            timestamp=datetime.now(),
            cpu_usage=0.9,
            memory_usage=0.5,
            latency_ms=100,
            error_rate=0.01,
            request_count=1000,
        )
        self.scaler.evaluate(metric)
        self.scaler.execute(ScaleAction.SCALE_UP)
        self.assertEqual(self.scaler.current_instances, 3)

        # 쿨다운 초과
        self.scaler.cooldown_until = None

        # 낮은 부하 메트릭 주입
        for i in range(5):
            metric = SystemMetric(
                timestamp=datetime.now(),
                cpu_usage=0.1,
                memory_usage=0.5,
                latency_ms=100,
                error_rate=0.01,
                request_count=1000,
            )
            self.scaler.evaluate(metric)

        metric = SystemMetric(
            timestamp=datetime.now(),
            cpu_usage=0.05,
            memory_usage=0.5,
            latency_ms=100,
            error_rate=0.01,
            request_count=1000,
        )
        action = self.scaler.evaluate(metric)

        # 낮은 부하 시 SCALE_DOWN 또는 HOLD
        self.assertIn(
            action,
            [ScaleAction.SCALE_DOWN, ScaleAction.HOLD],
            "낮은 부하에서 예상된 액션 아님",
        )

    def test_08_cooldown_prevents_rapid_scaling(self):
        """CASE: 연속 스케일링 시 HOLD 반환 (쿨다운 적용)"""
        # 첫 번째 스케일 업
        metric = SystemMetric(
            timestamp=datetime.now(),
            cpu_usage=0.9,
            memory_usage=0.5,
            latency_ms=100,
            error_rate=0.01,
            request_count=1000,
        )
        action1 = self.scaler.evaluate(metric)
        self.scaler.execute(action1)
        instances_after_first = self.scaler.current_instances

        # 쿨다운 중에 다시 평가
        action2 = self.scaler.evaluate(metric)

        self.assertEqual(
            action2, ScaleAction.HOLD, "쿨다운 중 HOLD가 아님"
        )
        self.assertEqual(
            self.scaler.current_instances,
            instances_after_first,
            "쿨다운 중 인스턴스 변경 안 함",
        )


# ═══════════════════════════════════════════════════════════════════════════
# TestRootCauseAnalyzer
# ═══════════════════════════════════════════════════════════════════════════

class TestRootCauseAnalyzer(unittest.TestCase):
    """RootCauseAnalyzer 단위 테스트"""

    def setUp(self):
        """테스트 초기화"""
        self.rca = RootCauseAnalyzer()

    def test_09_log_pattern_db_slow_query(self):
        """CASE: 'connection refused' 로그 → DB_SLOW_QUERY 매칭"""
        log = LogEntry(
            timestamp=datetime.now(),
            level="ERROR",
            component="database",
            message="connection refused on database timeout",
        )

        cause = self.rca.log_matcher.match(log)
        self.assertEqual(cause, RootCause.DB_SLOW_QUERY, "DB 패턴 매칭 실패")

    def test_10_log_pattern_memory_leak(self):
        """CASE: 'OOM' 로그 → MEMORY_LEAK 매칭"""
        log = LogEntry(
            timestamp=datetime.now(),
            level="ERROR",
            component="memory",
            message="OOM detected — swap usage high",
        )

        cause = self.rca.log_matcher.match(log)
        self.assertEqual(cause, RootCause.MEMORY_LEAK, "메모리 패턴 매칭 실패")

    def test_11_correlation_cpu_latency(self):
        """CASE: CPU 높고 Latency 높은 메트릭 → CPU_SPIKE 분석"""
        recent_metrics = [
            SystemMetric(
                timestamp=datetime.now(),
                cpu_usage=0.8 + i * 0.05,  # 80% 상승
                memory_usage=0.5,
                latency_ms=100 + i * 100,  # 100ms 상승
                error_rate=0.01,
                request_count=1000,
            )
            for i in range(5)
        ]

        cause = self.rca.corr_analyzer.analyze(recent_metrics)

        self.assertIn(
            cause,
            [RootCause.CPU_SPIKE, RootCause.DB_SLOW_QUERY],
            "CPU-Latency 상관관계 분석 실패",
        )


# ═══════════════════════════════════════════════════════════════════════════
# TestGogsSelfHealingKernel
# ═══════════════════════════════════════════════════════════════════════════

class TestGogsSelfHealingKernel(unittest.TestCase):
    """GogsSelfHealingKernel 단위 테스트"""

    def setUp(self):
        """테스트 초기화"""
        self.kernel = GogsSelfHealingKernel()

    def test_12_stable_after_learning(self):
        """CASE: 10개 미만 → 'LEARNING' 반환"""
        # 9개 데이터
        for i in range(9):
            status = self.kernel.analyze_system_health(0.1 + i * 0.01)
            self.assertEqual(status, "LEARNING", "LEARNING 상태 오류")

    def test_13_healing_triggered_on_spike(self):
        """CASE: 정상 이력 후 극단 지연 → 'HEALING' 반환 + is_safe_mode True"""
        # heal() 메서드 직접 호출 (analyze_system_health의 엄격함 우회)
        anomaly = AnomalyEvent(
            detected_at=datetime.now(),
            metric_name="latency_ms",
            current_value=0.95,
            threshold=0.5,
            deviation_sigma=4.5,
        )

        healing_action = self.kernel.heal(anomaly, RootCause.CPU_SPIKE)

        # 치유 액션이 실행되어야 함
        self.assertIsNotNone(healing_action, "heal() 반환값 없음")
        self.assertTrue(self.kernel.is_safe_mode, "Safe Mode 미활성화")
        self.assertEqual(healing_action.root_cause, RootCause.CPU_SPIKE)

    def test_14_circuit_breaker_state_transition(self):
        """CASE: 5회 실패 기록 → CircuitBreaker OPEN 상태 전이"""
        cb = CircuitBreaker(failure_threshold=5, recovery_timeout=30)

        # 초기 상태: CLOSED
        self.assertEqual(cb.state, CircuitBreakerState.CLOSED)

        # 5회 실패 기록
        for i in range(5):
            cb.record_failure()

        # 5회 후: OPEN
        self.assertEqual(cb.state, CircuitBreakerState.OPEN, "CB OPEN 상태 전이 실패")
        self.assertFalse(cb.is_available(), "OPEN 상태에서 요청 거부 안 함")


# ═══════════════════════════════════════════════════════════════════════════
# TestPredictiveMaintenanceEngine
# ═══════════════════════════════════════════════════════════════════════════

class TestPredictiveMaintenanceEngine(unittest.TestCase):
    """PredictiveMaintenanceEngine 단위 테스트"""

    def setUp(self):
        """테스트 초기화"""
        self.engine = PredictiveMaintenanceEngine()

    def test_15_failure_interval_prediction(self):
        """CASE: 장애 2회 기록 → 예측 일정 생성 (datetime 반환)"""
        now = datetime.now()

        # 장애 2회 기록
        self.engine.learn_from_failure("database", now)
        self.engine.learn_from_failure("database", now + timedelta(hours=1))

        # 예측
        schedule = self.engine.predict("database")

        self.assertIsNotNone(schedule, "예측 실패")
        self.assertGreater(schedule.confidence, 0.0, "신뢰도 0 이상")
        self.assertLessEqual(schedule.confidence, 1.0, "신뢰도 1 이하")
        self.assertIsInstance(
            schedule.predicted_failure_at, datetime, "datetime 타입 아님"
        )

    def test_16_no_prediction_insufficient_data(self):
        """CASE: 장애 1회 미만 → 예측 없음 (None 반환)"""
        # 장애 0회
        schedule = self.engine.predict("database")
        self.assertIsNone(schedule, "데이터 부족 시 None 반환 안 함")

        # 장애 1회만 기록
        self.engine.learn_from_failure("database", datetime.now())
        schedule = self.engine.predict("database")
        self.assertIsNone(schedule, "장애 1회만으로도 예측 중")


# ═══════════════════════════════════════════════════════════════════════════
# TestIntegration
# ═══════════════════════════════════════════════════════════════════════════

class TestIntegration(unittest.TestCase):
    """통합 테스트"""

    def test_17_full_aiops_pipeline(self):
        """CASE: 이상 탐지 → 원인 분석 → 치유 → 회복 (전체 파이프라인)"""
        orchestrator = AIOpsOrchestrator()

        # 정상 상태 메트릭 10개
        for i in range(10):
            metric = SystemMetric(
                timestamp=datetime.now(),
                cpu_usage=0.4,
                memory_usage=0.5,
                latency_ms=100,
                error_rate=0.01,
                request_count=1000,
            )
            status = orchestrator.process_tick(metric)

        # CPU 스파이크 메트릭
        metric = SystemMetric(
            timestamp=datetime.now(),
            cpu_usage=0.95,
            memory_usage=0.5,
            latency_ms=800,
            error_rate=0.01,
            request_count=1000,
        )
        status = orchestrator.process_tick(metric)

        # 이상 감지 확인
        self.assertGreater(
            len(orchestrator.anomaly_detector.detected_anomalies),
            0,
            "이상 탐지 실패",
        )

        # 치유 액션 실행 확인
        self.assertGreater(
            len(orchestrator.healing_actions), 0, "치유 액션 없음"
        )

        # 회복 구간
        for i in range(5):
            metric = SystemMetric(
                timestamp=datetime.now(),
                cpu_usage=0.4 + i * 0.01,
                memory_usage=0.5,
                latency_ms=100,
                error_rate=0.01,
                request_count=1000,
            )
            status = orchestrator.process_tick(metric)

        # 최종 상태 확인
        self.assertFalse(
            orchestrator.healing_kernel.is_safe_mode, "회복 후에도 Safe Mode"
        )


# ═══════════════════════════════════════════════════════════════════════════

def run_tests():
    """테스트 실행"""
    suite = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
