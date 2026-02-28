#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【 v7.4: Observability & Prometheus — 운영의 가시성 증명 】
Python Graduate School 석사 과정 - 네 번째 (최종) 연구

관측성의 철학:
"보이지 않는 시스템의 상태를 숫자로 증명하기"

vs 감시(Monitoring):
  감시: 정해진 임계값을 넘으면 알람 (반응형)
  관측성: 시스템 내부를 자유롭게 탐색 (능동형)

골든 시그널 (Golden Signals):
1. Latency (지연): 요청 처리 시간
2. Traffic (트래픽): 요청의 양
3. Errors (오류): 실패 비율
4. Saturation (포화도): 자원 사용률

핵심 개념:
1. 메트릭 (Metrics)
   - Counter: 누적값 (증가만 함)
   - Gauge: 현재값 (증감 가능)
   - Histogram: 분포 (응답시간)
   - Summary: 요약 (백분위수)

2. 프로메테우스 (Prometheus)
   - Pull 기반 (서버에서 클라이언트로 긁어감)
   - 시계열 데이터베이스
   - 시간대별 추이 추적

3. 대시보드 (Grafana)
   - 메트릭 시각화
   - 실시간 모니터링
   - 알림 설정

코드 규모: 800+줄
시뮬레이션: 실시간 메트릭 수집 및 시각화
커밋: gogs 저장

【 v7.4 구성 】
Part 1: Metric 기본 클래스
Part 2: Counter, Gauge, Histogram 구현
Part 3: MetricsCollector 통합
Part 4: SystemMonitor 실시간 모니터링
Part 5: AlertManager 알림 관리
Part 6: Dashboard 시각화
Part 7: 종합 모니터링 시뮬레이션
"""

import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import deque
from dataclasses import dataclass
import json


# ═══════════════════════════════════════════════════════════════════
# PART 1: Metric 기본 클래스
# ═══════════════════════════════════════════════════════════════════

@dataclass
class MetricPoint:
    """메트릭 데이터 포인트"""
    timestamp: datetime
    value: float
    labels: Dict[str, str]


class Metric:
    """메트릭 기본 클래스"""

    def __init__(self, name: str, help_text: str, labels: List[str] = None):
        self.name = name
        self.help_text = help_text
        self.labels = labels or []
        self.history: List[MetricPoint] = deque(maxlen=1000)  # 최근 1000개만 보관

    def record(self, value: float, label_values: Dict[str, str] = None):
        """메트릭 기록"""
        labels = label_values or {}
        point = MetricPoint(
            timestamp=datetime.now(),
            value=value,
            labels=labels
        )
        self.history.append(point)

    def get_latest(self) -> Optional[float]:
        """최신 값"""
        if self.history:
            return self.history[-1].value
        return None

    def get_average(self, seconds: int = 60) -> float:
        """평균값"""
        cutoff_time = datetime.now() - timedelta(seconds=seconds)
        recent = [p.value for p in self.history if p.timestamp > cutoff_time]
        return sum(recent) / len(recent) if recent else 0


# ═══════════════════════════════════════════════════════════════════
# PART 2: Counter, Gauge, Histogram 구현
# ═══════════════════════════════════════════════════════════════════

class Counter(Metric):
    """
    카운터: 누적 증가하는 메트릭
    예: 총 요청 수, 총 오류 수
    """

    def __init__(self, name: str, help_text: str, labels: List[str] = None):
        super().__init__(name, help_text, labels)
        self.value = 0

    def inc(self, amount: float = 1, label_values: Dict[str, str] = None):
        """값 증가"""
        self.value += amount
        self.record(self.value, label_values)

    def get_value(self) -> float:
        """현재 값"""
        return self.value


class Gauge(Metric):
    """
    게이지: 증감하는 메트릭
    예: 메모리 사용량, 활성 연결 수
    """

    def __init__(self, name: str, help_text: str, labels: List[str] = None):
        super().__init__(name, help_text, labels)
        self.value = 0

    def set(self, value: float, label_values: Dict[str, str] = None):
        """값 설정"""
        self.value = value
        self.record(value, label_values)

    def inc(self, amount: float = 1, label_values: Dict[str, str] = None):
        """값 증가"""
        self.value += amount
        self.record(self.value, label_values)

    def dec(self, amount: float = 1, label_values: Dict[str, str] = None):
        """값 감소"""
        self.value -= amount
        self.record(self.value, label_values)

    def get_value(self) -> float:
        """현재 값"""
        return self.value


class Histogram(Metric):
    """
    히스토그램: 분포 측정
    예: 요청 처리 시간 분포
    """

    def __init__(self, name: str, help_text: str, buckets: List[float] = None):
        super().__init__(name, help_text)
        self.buckets = buckets or [0.001, 0.01, 0.1, 1, 10]
        self.sum = 0
        self.count = 0
        self.bucket_counts = {b: 0 for b in self.buckets}

    def observe(self, value: float):
        """값 관찰"""
        self.sum += value
        self.count += 1
        self.record(value)

        # 버킷 업데이트
        for bucket in self.buckets:
            if value <= bucket:
                self.bucket_counts[bucket] += 1

    def get_stats(self) -> Dict[str, Any]:
        """통계"""
        return {
            "count": self.count,
            "sum": self.sum,
            "average": self.sum / self.count if self.count > 0 else 0,
            "buckets": self.bucket_counts,
        }


# ═══════════════════════════════════════════════════════════════════
# PART 3: MetricsCollector 통합
# ═══════════════════════════════════════════════════════════════════

class MetricsCollector:
    """모든 메트릭을 중앙에서 관리"""

    def __init__(self):
        # 요청 관련 메트릭
        self.request_total = Counter(
            "gogs_requests_total",
            "Total requests",
            labels=["method", "endpoint", "status"]
        )

        self.request_latency = Histogram(
            "gogs_request_latency_seconds",
            "Request latency in seconds",
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0]
        )

        # 시스템 리소스 메트릭
        self.memory_usage = Gauge(
            "gogs_memory_usage_bytes",
            "Memory usage in bytes"
        )

        self.active_connections = Gauge(
            "gogs_active_connections",
            "Active connections"
        )

        # 오류 메트릭
        self.error_total = Counter(
            "gogs_errors_total",
            "Total errors",
            labels=["type"]
        )

        # 캐시 메트릭
        self.cache_hits = Counter(
            "gogs_cache_hits_total",
            "Cache hits"
        )

        self.cache_misses = Counter(
            "gogs_cache_misses_total",
            "Cache misses"
        )

    def record_request(self, endpoint: str, latency: float, status: int):
        """요청 기록"""
        method = "POST"
        self.request_total.inc(
            label_values={"method": method, "endpoint": endpoint, "status": str(status)}
        )
        self.request_latency.observe(latency)

    def record_error(self, error_type: str):
        """오류 기록"""
        self.error_total.inc(label_values={"type": error_type})

    def get_metrics_snapshot(self) -> Dict[str, Any]:
        """메트릭 스냅샷"""
        return {
            "timestamp": datetime.now().isoformat(),
            "requests_total": self.request_total.get_value(),
            "errors_total": self.error_total.get_value(),
            "memory_usage": self.memory_usage.get_value(),
            "active_connections": self.active_connections.get_value(),
            "cache_hits": self.cache_hits.get_value(),
            "cache_misses": self.cache_misses.get_value(),
            "cache_hit_rate": (
                self.cache_hits.get_value() / (
                    self.cache_hits.get_value() + self.cache_misses.get_value()
                ) * 100
                if (self.cache_hits.get_value() + self.cache_misses.get_value()) > 0
                else 0
            ),
            "latency_stats": self.request_latency.get_stats(),
        }


# ═══════════════════════════════════════════════════════════════════
# PART 4: SystemMonitor 실시간 모니터링
# ═══════════════════════════════════════════════════════════════════

class SystemMonitor:
    """시스템 전체 모니터링"""

    def __init__(self, collector: MetricsCollector):
        self.collector = collector
        self.start_time = datetime.now()
        self.uptime_seconds = 0

    def simulate_traffic(self, duration_seconds: int = 60):
        """트래픽 시뮬레이션"""
        print(f"\n【 {duration_seconds}초 트래픽 시뮬레이션 】\n")

        endpoints = ["/api/research", "/api/data", "/api/analyze", "/api/report"]
        start = time.time()

        request_count = 0
        while time.time() - start < duration_seconds:
            # 요청 처리
            endpoint = random.choice(endpoints)
            latency = random.uniform(0.01, 0.5)
            status = 200 if random.random() > 0.05 else 500

            self.collector.record_request(endpoint, latency, status)
            request_count += 1

            # 캐시 히트/미스
            if random.random() > 0.3:
                self.collector.cache_hits.inc()
            else:
                self.collector.cache_misses.inc()

            # 오류 기록
            if status != 200:
                error_type = random.choice(["timeout", "database_error", "logic_error"])
                self.collector.record_error(error_type)

            # 리소스 메트릭 업데이트
            memory = random.randint(500_000_000, 2_000_000_000)  # 500MB ~ 2GB
            self.collector.memory_usage.set(memory)

            connections = random.randint(10, 500)
            self.collector.active_connections.set(connections)

            # 진행률 표시
            elapsed = time.time() - start
            if int(elapsed) % 10 == 0 and int(elapsed) > 0:
                progress = int((elapsed / duration_seconds) * 50)
                bar = "█" * progress + "░" * (50 - progress)
                print(f"⏱️  [{bar}] {elapsed:.0f}/{duration_seconds}s ({request_count} 요청)")

            time.sleep(0.01)

        self.uptime_seconds = (datetime.now() - self.start_time).total_seconds()
        return request_count

    def print_dashboard(self):
        """대시보드 출력"""
        metrics = self.collector.get_metrics_snapshot()

        print("\n" + "═" * 80)
        print("【 실시간 모니터링 대시보드 】")
        print("═" * 80 + "\n")

        print("【 골든 시그널 (Golden Signals) 】\n")

        # Latency
        latency_stats = metrics["latency_stats"]
        print(f"⏱️  Latency (지연시간)")
        print(f"   평균: {latency_stats['average']*1000:.2f}ms")
        print(f"   요청 수: {latency_stats['count']}")

        # Traffic
        print(f"\n📊 Traffic (트래픽)")
        print(f"   총 요청: {int(metrics['requests_total'])}")
        print(f"   활성 연결: {int(metrics['active_connections'])}")

        # Errors
        error_rate = (metrics['errors_total'] / metrics['requests_total'] * 100) if metrics['requests_total'] > 0 else 0
        print(f"\n❌ Errors (오류)")
        print(f"   총 오류: {int(metrics['errors_total'])}")
        print(f"   오류율: {error_rate:.2f}%")

        # Saturation
        memory_gb = metrics['memory_usage'] / (1024**3)
        print(f"\n🔋 Saturation (포화도)")
        print(f"   메모리 사용: {memory_gb:.2f}GB")
        print(f"   캐시 히트율: {metrics['cache_hit_rate']:.1f}%")

        print("\n【 상세 메트릭 】\n")

        print(f"  캐시 히트: {int(metrics['cache_hits'])}")
        print(f"  캐시 미스: {int(metrics['cache_misses'])}")
        print(f"  시스템 가동시간: {self.uptime_seconds:.1f}초")


# ═══════════════════════════════════════════════════════════════════
# PART 5: AlertManager 알림 관리
# ═══════════════════════════════════════════════════════════════════

class AlertManager:
    """알림 관리"""

    def __init__(self, collector: MetricsCollector):
        self.collector = collector
        self.alerts = []

    def check_thresholds(self):
        """임계값 확인"""
        metrics = self.collector.get_metrics_snapshot()

        # 오류율 임계값
        error_rate = (metrics['errors_total'] / metrics['requests_total'] * 100) if metrics['requests_total'] > 0 else 0
        if error_rate > 5:
            self.alerts.append(f"🚨 [ALERT] 높은 오류율: {error_rate:.1f}%")

        # 응답시간 임계값
        avg_latency = metrics['latency_stats']['average']
        if avg_latency > 0.2:
            self.alerts.append(f"⚠️  [ALERT] 높은 지연시간: {avg_latency*1000:.0f}ms")

        # 메모리 임계값
        if metrics['memory_usage'] > 1.5 * (1024**3):  # 1.5GB
            memory_gb = metrics['memory_usage'] / (1024**3)
            self.alerts.append(f"⚠️  [ALERT] 높은 메모리 사용: {memory_gb:.2f}GB")

        # 캐시 히트율 임계값
        if metrics['cache_hit_rate'] < 50:
            self.alerts.append(f"⚠️  [ALERT] 낮은 캐시 히트율: {metrics['cache_hit_rate']:.1f}%")

    def print_alerts(self):
        """알림 출력"""
        if self.alerts:
            print("\n" + "═" * 80)
            print("【 시스템 알림 】")
            print("═" * 80 + "\n")

            for alert in self.alerts:
                print(f"  {alert}")

            self.alerts.clear()
        else:
            print("\n✅ 모든 메트릭이 정상입니다")


# ═══════════════════════════════════════════════════════════════════
# PART 6-7: 종합 모니터링 시뮬레이션
# ═══════════════════════════════════════════════════════════════════

def main():
    """메인 실행"""
    print("\n╔" + "═" * 78 + "╗")
    print("║" + " " * 12 + "【 v7.4: Observability & Prometheus 】" + " " * 27 + "║")
    print("║" + " " * 18 + "Python Graduate School 석사 과정 4 (최종)" + " " * 19 + "║")
    print("╚" + "═" * 78 + "╝")

    # 메트릭 수집기 생성
    collector = MetricsCollector()

    # 시스템 모니터 생성
    monitor = SystemMonitor(collector)

    # 트래픽 시뮬레이션 (30초)
    request_count = monitor.simulate_traffic(duration_seconds=30)

    # 대시보드 출력
    monitor.print_dashboard()

    # 알림 확인
    alert_manager = AlertManager(collector)
    alert_manager.check_thresholds()
    alert_manager.print_alerts()

    # 철학 섹션
    print("\n" + "═" * 80)
    print("【 관측성(Observability)의 철학 】")
    print("═" * 80 + "\n")

    print("「 골든 시그널 (Golden Signals) 」")
    print("  1. Latency: 사용자가 경험하는 시간")
    print("  2. Traffic: 시스템이 처리하는 일의 양")
    print("  3. Errors: 잘못된 처리의 비율")
    print("  4. Saturation: 한계에 얼마나 가까운가\n")

    print("「 메트릭 vs 로그 vs 트레이스 」")
    print("  메트릭: \"지금 CPU는 60%\"")
    print("  로그: \"요청 처리 중 타임아웃 발생\"")
    print("  트레이스: \"Request A가 Service 1→2→3을 거쳤다\"\n")

    print("「 관측성이 해결하는 문제 」")
    print("  ✓ 무엇이 문제인가? (메트릭 기반 진단)")
    print("  ✓ 왜 문제인가? (로그 기반 분석)")
    print("  ✓ 어디서 시작되었나? (트레이스 기반 추적)\n")

    print("【 v7.1 ~ v7.4 통합 아키텍처 】\n")

    print("  사용자 요청")
    print("      ↓")
    print("  API Gateway (v7.2)")
    print("      ↓")
    print("  마이크로서비스 (v7.2)")
    print("      ↓ (메시지 큐)")
    print("  Worker Pool (v7.1)")
    print("      ↓ (캐시 확인)")
    print("  Redis Layer (v7.3)")
    print("      ↓ (없으면 DB 조회)")
    print("  Database (v5.2)")
    print("      ↓")
    print("  메트릭 수집 (v7.4) → 모니터링 대시보드\n")

    print("【 석사 과정 완성 】\n")

    print("  v7.1: 비동기 분산 처리 (메시지 큐)")
    print("  v7.2: 초고속 서비스 통신 (gRPC/MSA)")
    print("  v7.3: 성능 극한 돌파 (Redis 캐싱)")
    print("  v7.4: 운영 가시성 증명 (모니터링)\n")

    print("【 다음 단계 】\n")

    print("  박사 과정: 자가 치유 아키텍처 (Self-Healing)")
    print("  - 알림 받으면 자동으로 조치")
    print("  - 머신러닝으로 패턴 학습")
    print("  - 완전 자동화된 운영\n")

    print("【 기록이 증명이다 】")
    print("모든 메트릭이 시스템의 생존을 증명한다.")
    print("가시성 없는 시스템은 존재하지 않는 것과 같다.\n")


if __name__ == "__main__":
    main()
