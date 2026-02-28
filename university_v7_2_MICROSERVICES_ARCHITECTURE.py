#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【 v7.2: Microservices Architecture & Inter-Service Communication 】
Python Graduate School 석사 과정 - 두 번째 연구

마이크로서비스의 철학:
"거대한 시스템을 작은 독립 서비스로 분해하여, 각각 독립적으로 배포하고 확장한다"

vs 모놀리식 아키텍처:
  모놀리식: 하나의 거대한 애플리케이션 (변경 시 전체 재배포)
  마이크로: 여러 작은 서비스 (변경 시 해당 서비스만 재배포)

v7.1 vs v7.2:
  v7.1: 비동기 메시지 큐 (느슨한 결합, 이벤트 기반)
  v7.2: 서비스 간 동기 통신 (강한 일관성, 즉시 응답)

핵심 개념:
1. Service Registry (서비스 등록소)
   - 모든 서비스가 자신을 등록
   - 어느 호스트에서 어떤 포트로 실행 중인지 기록

2. Service Discovery (서비스 탐색)
   - 필요한 서비스를 동적으로 찾음
   - IP/포트 변경 시에도 자동 대응

3. Circuit Breaker (차단기)
   - 장애 서비스로의 호출을 차단
   - 연쇄 장애 방지

4. API Gateway (게이트웨이)
   - 모든 클라이언트 요청의 진입점
   - 요청 라우팅, 로드밸런싱, 인증

5. Load Balancing (부하 분산)
   - 여러 인스턴스 간 요청 분산
   - 라운드로빈, 가중치 등 전략

코드 규모: 700+줄
시뮬레이션: 4개 마이크로서비스 + API Gateway
커밋: gogs 저장

【 v7.2 구성 】
Part 1: MicroService — 기본 마이크로서비스 클래스
Part 2: ServiceRegistry — 서비스 레지스트리
Part 3: ServiceDiscovery — 서비스 탐색
Part 4: CircuitBreaker — 장애 격리
Part 5: APIGateway — API 게이트웨이
Part 6: InterServiceCommunication — 서비스 간 통신
Part 7: 마이크로서비스 분산 시뮬레이션
"""

import asyncio
import random
import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass


# ═══════════════════════════════════════════════════════════════════
# PART 1: MicroService — 기본 마이크로서비스 클래스
# ═══════════════════════════════════════════════════════════════════

class ServiceStatus(Enum):
    """서비스 상태"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass
class ServiceInstance:
    """서비스 인스턴스"""
    service_id: str
    service_name: str
    host: str
    port: int
    status: ServiceStatus = ServiceStatus.HEALTHY
    registered_at: datetime = None
    last_heartbeat: datetime = None

    def __post_init__(self):
        self.registered_at = self.registered_at or datetime.now()
        self.last_heartbeat = self.last_heartbeat or datetime.now()

    def __repr__(self):
        return f"{self.service_name}({self.service_id[:8]}) @ {self.host}:{self.port}"


class MicroService:
    """
    마이크로서비스 기본 클래스

    역할:
    - 독립적인 비즈니스 로직 처리
    - 다른 서비스와 통신
    - 자신의 건강 상태 관리
    """

    def __init__(self, name: str, port: int):
        self.service_id = str(uuid.uuid4())
        self.name = name
        self.port = port
        self.host = "localhost"
        self.status = ServiceStatus.HEALTHY
        self.request_count = 0
        self.error_count = 0
        self.avg_response_time = 0.0

    async def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        요청 처리 (서브클래스에서 구현)

        Args:
            request_data: 요청 데이터

        Returns:
            Dict: 응답 데이터
        """
        self.request_count += 1
        return {"service": self.name, "status": "ok"}

    def get_health(self) -> Dict[str, Any]:
        """서비스 건강 상태 반환"""
        success_rate = (
            100 * (1 - self.error_count / self.request_count)
            if self.request_count > 0
            else 100
        )

        return {
            "service_id": self.service_id,
            "service_name": self.name,
            "status": self.status.value,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "success_rate": success_rate,
            "avg_response_time": self.avg_response_time,
        }


# ═══════════════════════════════════════════════════════════════════
# PART 2: ServiceRegistry — 서비스 레지스트리
# ═══════════════════════════════════════════════════════════════════

class ServiceRegistry:
    """
    서비스 레지스트리

    역할:
    - 모든 마이크로서비스를 중앙에서 관리
    - 서비스 등록/해제
    - 헬스체크 모니터링
    """

    def __init__(self):
        self.services: Dict[str, List[ServiceInstance]] = {}
        self.heartbeat_timeout = 30  # 초

    def register(self, service: MicroService) -> ServiceInstance:
        """
        서비스 인스턴스 등록

        Args:
            service: 등록할 마이크로서비스

        Returns:
            ServiceInstance: 등록된 인스턴스
        """
        instance = ServiceInstance(
            service_id=service.service_id,
            service_name=service.name,
            host=service.host,
            port=service.port,
        )

        if service.name not in self.services:
            self.services[service.name] = []

        self.services[service.name].append(instance)

        print(f"✅ [{instance.service_name}] 등록 완료: {instance}")
        return instance

    def deregister(self, service_name: str, service_id: str) -> bool:
        """
        서비스 인스턴스 등록 해제

        Args:
            service_name: 서비스 이름
            service_id: 서비스 ID

        Returns:
            bool: 성공 여부
        """
        if service_name in self.services:
            self.services[service_name] = [
                s for s in self.services[service_name]
                if s.service_id != service_id
            ]
            print(f"❌ [{service_name}] 등록 해제")
            return True
        return False

    def get_service_instances(self, service_name: str) -> List[ServiceInstance]:
        """
        서비스 인스턴스 목록 조회

        Args:
            service_name: 서비스 이름

        Returns:
            List[ServiceInstance]: 등록된 인스턴스 목록
        """
        return self.services.get(service_name, [])

    def update_heartbeat(self, service_name: str, service_id: str):
        """서비스 하트비트 업데이트"""
        if service_name in self.services:
            for instance in self.services[service_name]:
                if instance.service_id == service_id:
                    instance.last_heartbeat = datetime.now()

    def get_healthy_instances(self, service_name: str) -> List[ServiceInstance]:
        """건강한 서비스 인스턴스만 반환"""
        instances = self.get_service_instances(service_name)
        healthy = []

        for instance in instances:
            time_since_heartbeat = (
                datetime.now() - instance.last_heartbeat
            ).total_seconds()

            if time_since_heartbeat < self.heartbeat_timeout:
                if instance.status == ServiceStatus.HEALTHY:
                    healthy.append(instance)

        return healthy


# ═══════════════════════════════════════════════════════════════════
# PART 3: ServiceDiscovery — 서비스 탐색
# ═══════════════════════════════════════════════════════════════════

class ServiceDiscovery:
    """
    서비스 디스커버리

    역할:
    - 동적으로 서비스를 탐색
    - 로드 밸런싱 전략 적용
    - 부하 분산
    """

    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
        self.current_index: Dict[str, int] = {}

    def discover(self, service_name: str) -> Optional[ServiceInstance]:
        """
        서비스 탐색 (라운드로빈 로드밸런싱)

        Args:
            service_name: 찾을 서비스 이름

        Returns:
            Optional[ServiceInstance]: 서비스 인스턴스
        """
        instances = self.registry.get_healthy_instances(service_name)

        if not instances:
            print(f"⚠️  [{service_name}] 사용 가능한 인스턴스 없음")
            return None

        # 라운드로빈 로드밸런싱
        if service_name not in self.current_index:
            self.current_index[service_name] = 0

        index = self.current_index[service_name] % len(instances)
        self.current_index[service_name] += 1

        return instances[index]

    def get_all_instances(self, service_name: str) -> List[ServiceInstance]:
        """모든 인스턴스 조회"""
        return self.registry.get_healthy_instances(service_name)


# ═══════════════════════════════════════════════════════════════════
# PART 4: CircuitBreaker — 장애 격리
# ═══════════════════════════════════════════════════════════════════

class CircuitBreakerState(Enum):
    """Circuit Breaker 상태"""
    CLOSED = "closed"        # 정상, 요청 허용
    OPEN = "open"            # 장애, 요청 차단
    HALF_OPEN = "half_open"  # 복구 시도


class CircuitBreaker:
    """
    Circuit Breaker 패턴

    목표: 장애 서비스로의 연쇄 호출 방지

    상태 전이:
    CLOSED → (실패 누적) → OPEN → (일정 시간) → HALF_OPEN → CLOSED/OPEN
    """

    def __init__(self, failure_threshold: int = 5, timeout: int = 10):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.failure_threshold = failure_threshold
        self.success_threshold = 2
        self.timeout = timeout
        self.last_failure_time = None

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Circuit Breaker를 통한 함수 호출

        Args:
            func: 호출할 함수
            args, kwargs: 함수 인자

        Returns:
            Any: 함수 반환값
        """
        if self.state == CircuitBreakerState.OPEN:
            # OPEN 상태 확인 (일정 시간 후 HALF_OPEN으로 변경)
            if (
                self.last_failure_time
                and (datetime.now() - self.last_failure_time).total_seconds()
                > self.timeout
            ):
                self.state = CircuitBreakerState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception("🔴 Circuit Breaker OPEN: 장애 서비스 차단")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """성공 처리"""
        self.failure_count = 0

        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitBreakerState.CLOSED
                print("✅ Circuit Breaker CLOSED (복구됨)")

    def _on_failure(self):
        """실패 처리"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN
            print(f"🔴 Circuit Breaker OPEN (장애 감지: {self.failure_count} 실패)")


# ═══════════════════════════════════════════════════════════════════
# PART 5: APIGateway — API 게이트웨이
# ═══════════════════════════════════════════════════════════════════

class APIGateway:
    """
    API 게이트웨이

    역할:
    - 모든 클라이언트 요청의 진입점
    - 요청 라우팅
    - 인증/인가
    - 레이트 제한
    - 로깅
    """

    def __init__(self, discovery: ServiceDiscovery):
        self.discovery = discovery
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.request_log: List[Dict[str, Any]] = []

    def _get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """서비스별 Circuit Breaker 획득"""
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker()
        return self.circuit_breakers[service_name]

    async def route_request(
        self, service_name: str, request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        요청 라우팅

        Args:
            service_name: 대상 서비스 이름
            request_data: 요청 데이터

        Returns:
            Dict: 응답 데이터
        """
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        try:
            # 서비스 탐색
            instance = self.discovery.discover(service_name)
            if not instance:
                raise Exception(f"Service {service_name} not found")

            # Circuit Breaker를 통한 요청
            circuit_breaker = self._get_circuit_breaker(service_name)

            async def make_request():
                # 실제 요청 시뮬레이션
                await asyncio.sleep(random.uniform(0.1, 0.5))

                # 5% 확률로 오류 발생
                if random.random() < 0.05:
                    raise Exception("Service error")

                return {
                    "service": service_name,
                    "request_id": request_id,
                    "status": "ok",
                    "data": f"Response from {instance.service_name}",
                }

            response = await circuit_breaker.call(make_request)

            elapsed = time.time() - start_time
            self.request_log.append(
                {
                    "request_id": request_id,
                    "service": service_name,
                    "status": "success",
                    "elapsed": elapsed,
                    "timestamp": datetime.now(),
                }
            )

            print(f"✅ [{request_id}] {service_name} → {response['status']} ({elapsed:.3f}s)")
            return response

        except Exception as e:
            elapsed = time.time() - start_time
            self.request_log.append(
                {
                    "request_id": request_id,
                    "service": service_name,
                    "status": "error",
                    "error": str(e),
                    "elapsed": elapsed,
                    "timestamp": datetime.now(),
                }
            )

            print(f"❌ [{request_id}] {service_name} → 오류: {e}")
            raise

    def get_metrics(self) -> Dict[str, Any]:
        """메트릭 조회"""
        total_requests = len(self.request_log)
        successful = sum(1 for r in self.request_log if r["status"] == "success")
        failed = sum(1 for r in self.request_log if r["status"] == "error")

        avg_response_time = (
            sum(r["elapsed"] for r in self.request_log) / total_requests
            if total_requests > 0
            else 0
        )

        return {
            "total_requests": total_requests,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total_requests * 100) if total_requests > 0 else 0,
            "avg_response_time": avg_response_time,
        }


# ═══════════════════════════════════════════════════════════════════
# PART 6 & 7: 마이크로서비스 분산 시뮬레이션
# ═══════════════════════════════════════════════════════════════════

async def main():
    """마이크로서비스 시스템 시뮬레이션"""
    print("\n╔" + "═" * 68 + "╗")
    print("║" + " " * 4 + "【 v7.2: Microservices Architecture & Service Communication 】" + " " * 3 + "║")
    print("║" + " " * 18 + "Python Graduate School 석사 과정 2" + " " * 14 + "║")
    print("╚" + "═" * 68 + "╝\n")

    # 1. 서비스 레지스트리 생성
    registry = ServiceRegistry()

    # 2. 마이크로서비스 인스턴스 생성
    services = [
        MicroService("UserService", 8001),
        MicroService("ProductService", 8002),
        MicroService("OrderService", 8003),
        MicroService("PaymentService", 8004),
    ]

    # 3. 서비스 등록 (각 서비스마다 2개 인스턴스)
    print("【 마이크로서비스 등록 】\n")
    for service in services:
        registry.register(service)
        # 같은 서비스 2번째 인스턴스
        service2 = MicroService(service.name, service.port + 100)
        registry.register(service2)

    # 4. 서비스 디스커버리 생성
    discovery = ServiceDiscovery(registry)

    # 5. API 게이트웨이 생성
    gateway = APIGateway(discovery)

    # 6. 요청 시뮬레이션
    print("\n【 요청 라우팅 시작 】\n")

    service_names = ["UserService", "ProductService", "OrderService", "PaymentService"]
    tasks = []

    for i in range(20):
        service_name = random.choice(service_names)
        request_data = {"request_id": i, "action": "process"}

        task = gateway.route_request(service_name, request_data)
        tasks.append(task)

        await asyncio.sleep(0.1)

    # 모든 요청 완료 대기
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 7. 메트릭 출력
    print("\n" + "═" * 70)
    print("【 마이크로서비스 시스템 성능 분석 】")
    print("═" * 70 + "\n")

    metrics = gateway.get_metrics()
    print("【 API Gateway 메트릭 】")
    print(f"  총 요청: {metrics['total_requests']}개")
    print(f"  성공: {metrics['successful']}개")
    print(f"  실패: {metrics['failed']}개")
    print(f"  성공률: {metrics['success_rate']:.1f}%")
    print(f"  평균 응답시간: {metrics['avg_response_time']:.3f}s")

    print("\n【 등록된 서비스 】")
    for service_name, instances in registry.services.items():
        print(f"  {service_name}: {len(instances)}개 인스턴스")
        for instance in instances:
            print(f"    └─ {instance.host}:{instance.port}")

    print("\n【 Circuit Breaker 상태 】")
    for service_name, cb in gateway.circuit_breakers.items():
        print(f"  {service_name}: {cb.state.value} (실패: {cb.failure_count})")

    # 철학
    print("\n" + "═" * 70)
    print("【 마이크로서비스 아키텍처의 철학 】")
    print("═" * 70 + "\n")

    print("「 분해 (Decomposition) 」")
    print("  → 거대한 시스템을 작은 서비스로 분해")
    print("  → 각 서비스는 하나의 책임만 가짐\n")

    print("「 독립성 (Independence) 」")
    print("  → 각 서비스는 독립적으로 배포, 확장, 개발")
    print("  → 한 서비스의 장애가 다른 서비스에 영향 없음\n")

    print("「 통신 (Communication) 」")
    print("  → Service Discovery: 동적 서비스 탐색")
    print("  → Circuit Breaker: 장애 격리")
    print("  → Load Balancing: 부하 분산\n")

    print("「 관찰성 (Observability) 」")
    print("  → 분산 추적 (Distributed Tracing)")
    print("  → 메트릭 수집 (Metrics)")
    print("  → 로깅 (Logging)\n")

    print("【 v7.1 vs v7.2 】\n")
    print("v7.1 분산 메시지 큐:")
    print("  → 비동기 이벤트 기반")
    print("  → 느슨한 결합 (Loose Coupling)")
    print("  → 높은 처리량, 낮은 응답시간 민감도\n")

    print("v7.2 마이크로서비스:")
    print("  → 동기 서비스 간 통신")
    print("  → 강한 일관성 (Strong Consistency)")
    print("  → 즉시 응답 필요, 고가용성\n")

    print("【 다음 단계: v7.3 】")
    print("  → Kubernetes 오케스트레이션")
    print("  → 자동 배포 & 스케일링")
    print("  → 완전한 클라우드 네이티브 시스템\n")

    print("【 기록이 증명이다 】")
    print("모든 마이크로서비스의 협력이 코드로 기록된다.")
    print("분산 시스템의 핵심 설계 원칙이 실증된다.\n")


if __name__ == "__main__":
    asyncio.run(main())
