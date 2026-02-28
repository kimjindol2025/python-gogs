"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🏛️ UNIVERSITY LEVEL 3 - v5.1 DISTRIBUTED MICROSERVICES ARCHITECTURE 🏛️  ║
║                                                                              ║
║      복잡성 속의 질서: 대규모 시스템 설계 (Order in Complexity)             ║
║  분산 시스템의 기초 - 마이크로서비스 아키텍처와 메시지 큐                  ║
║                                                                              ║
║  "한 대의 슈퍼컴퓨터보다 수천 대의 작은 컴퓨터가 더 강력하다" - gogs      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📚 학습 목표:
   1️⃣ Monolithic vs Microservices 아키텍처 설계
   2️⃣ CAP 이론: 분산 시스템의 불가능성 삼각형
   3️⃣ Message Broker 패턴: 느슨한 결합의 실현
   4️⃣ Service Discovery: 서비스 간 자동 탐색
   5️⃣ Event-Driven Architecture: 이벤트 기반 설계
   6️⃣ 분산 트랜잭션: SAGA 패턴
   7️⃣ 장애 격리와 복원력: Circuit Breaker 패턴

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 1: 마이크로서비스의 철학 - 복잡성의 관리                              ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🏗️ 아키텍처 진화:

1️⃣ MONOLITHIC (모놀리식)
   ─────────────────────
   ┌─────────────────────────────┐
   │   Monolithic Application    │
   │  ┌───────┬───────┬───────┐  │
   │  │ Auth  │ Order │Payment│  │
   │  ├───────┼───────┼───────┤  │
   │  │   Database (Single)    │  │
   │  └───────────────────────┘  │
   └─────────────────────────────┘

   특징: 모든 기능이 하나의 프로세스
   장점: 디버깅 간단, 배포 단순
   단점: ❌ 하나 고장→전체 중단
         ❌ 언어/기술 제한 (Java면 전부 Java)
         ❌ 확장: 전체를 복제해야 함
         ❌ 팀 간 충돌 (코드 경합)


2️⃣ MICROSERVICES (마이크로서비스)
   ──────────────────────────────
   [인터넷]
     |
   ┌─────────────────────────────────────┐
   │     API Gateway (Entry Point)       │
   └─────────┬────────────┬──────────────┘
             |            |
        ┌────▼───┐  ┌─────▼────┐
        │ Auth   │  │ Order    │
        │Service │  │Service   │
        └────┬───┘  └─────┬────┘
             |            |
        ┌────▼───┐  ┌─────▼────┐
        │Auth DB │  │Order DB   │
        └────────┘  └───────────┘

   특징: 각 기능이 독립된 서비스/프로세스
   장점: ✅ 하나 고장→해당 서비스만 중단
         ✅ 독립적 기술 선택 (A는 Python, B는 Go)
         ✅ 독립적 확장 (Payment만 10배로)
         ✅ 팀 독립성 (각 팀이 자신 서비스 담당)
   단점: 📌 네트워크 지연 증가
         📌 분산 트랜잭션 복잡
         📌 모니터링 어려움


📊 선택 기준:

Monolithic이 적합한 경우:
  ├─ 초기 스타트업 (<50명 팀)
  ├─ 비즈니스 모델 불확실 (자주 변함)
  └─ 팀 간 소통이 원활함

Microservices가 적합한 경우:
  ├─ 대규모 조직 (>100명)
  ├─ 비즈니스 모델 안정적
  ├─ 고트래픽 (Netflix ~50억 요청/일)
  └─ 다양한 기술 필요

💡 뜨거운 감자: "두 가지 중 가장 어려운 것?"
   1️⃣ 캐싱 무효화 (Cache Invalidation)
   2️⃣ 변수 이름짓기 (Naming Things)
   3️⃣ 분산 시스템 (Distributed Systems) ← 뽑았습니다!
"""


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 2: CAP 이론 - 분산 시스템의 불가능성 삼각형                          ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
⚠️ CAP THEOREM (브루어의 정리, 2000)

분산 시스템에서 다음 3가지를 동시에 만족할 수 없다:

1️⃣ CONSISTENCY (일관성)
   ──────────────────
   모든 노드가 같은 시간에 같은 데이터를 봐야 함

   [클라이언트A] 계좌: $100 요청
   [중앙서버] 계좌정보 업데이트: $100 → $90
   [클라이언트B] 계좌: $90 요청 ✓ (일관성!)

   만약 일관성 없으면:
   [클라이언트B] 계좌: $100 요청 ✗ (아직 업데이트 안 됨)
   → 낡은 데이터 (Stale Data)


2️⃣ AVAILABILITY (가용성)
   ────────────────────
   모든 요청이 응답을 받아야 함 (서버 고장 제외)

   [서버A] ━━━ 정상
   [서버B] ━━━ 정상
   [서버C] ✗ (고장)

   가용성 있음: [클라이언트] → [서버A/B] → 응답 OK ✓
   가용성 없음: [클라이언트] → [서버C] → No response ✗


3️⃣ PARTITION TOLERANCE (분할 내구성)
   ─────────────────────────────────
   네트워크가 끊겨도 시스템이 계속 동작해야 함

   [Partition 상황]:
   ┌──────────────────────┐  ❌ 네트워크 끊김  ┌──────────────────────┐
   │ 지역1:                │ ═══════════════ │ 지역2:                │
   │  ├─ DB: version 1    │                 │  ├─ DB: version 1    │
   │  └─ 수백 만 사용자   │                 │  └─ 수백 만 사용자   │
   └──────────────────────┘                 └──────────────────────┘

   지역1에서만 수정 → 지역2는 모름 (불일치!)
   But 지역2 서비스는 계속 동작! (가용성 ✓)


🔥 "3개 중 2개만 가능하다" 원칙:

┌────────────────────────────────────┐
│  3가지 조합의 장단점               │
├────────────────────────────────────┤
│ CA (Consistency + Availability)   │
│  └─ 네트워크 분할 불가능 가정   │
│     (LAN 환경 적합)               │
│     → 은행 시스템                 │
│                                   │
│ CP (Consistency + Partition Tol.) │
│  └─ 분할 시 일부 응답 안 함      │
│     → Google BigTable            │
│     → 금융 시스템                │
│                                   │
│ AP (Availability + Partition Tol.)│
│  └─ 일관성 약간 포기             │
│     → 대부분의 인터넷 서비스     │
│     → SNS, 이커머스              │
│                                   │
│ ⚠️ 모두 (Impossible!)              │
│  └─ 분산 시스템의 근본 한계      │
└────────────────────────────────────┘

📈 현실적 선택:

Amazon.com:
  ├─ 가용성 최우선 (쇼핑 중단 불가)
  ├─ 일관성은 약함 (재고 몇 개 오버 가능)
  └─ 분할 내구성 필수 (리전 간 독립)
  → AP 선택 (최종 일관성: Eventually Consistent)

은행 송금:
  ├─ 일관성 최우선 (돈 사라질 수 없음)
  ├─ 가용성도 높음 (24시간 운영)
  └─ 분할 내구성 있음 (백업 있음)
  → CP 또는 CA (보통 CA + 매우 안정적 네트워크)
"""


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 3: Message Broker 패턴 - 느슨한 결합의 실현                          ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
📬 메시지 브로커: 분산 시스템의 "우체국"

❌ 직접 통신 (Tight Coupling):
   ┌───────────────┐          ┌───────────────┐
   │ Order Service ├─────────→│Payment Service│
   └───────────────┘          └───────────────┘

   문제:
   - Payment 서비스 다운 → Order 전체 실패
   - Payment 느리면 → Order도 느려짐
   - 서비스 간 의존성 복잡


✅ 메시지 브로커 (Loose Coupling):
   ┌───────────────┐        ┌─────────────┐        ┌───────────────┐
   │Order Service  ├───────→│   Broker    │←───────┤Payment Service│
   └───────────────┘        │  (Queue)    │        └───────────────┘
                            └─────────────┘
   장점:
   - Order는 Broker에만 메시지 전송 (빨리 완료)
   - Payment는 자신의 속도로 처리
   - Payment 다운 → 메시지만 큐에 저장, Order는 무관
   - 서비스 간 독립성 최대화
"""

import queue
import threading
import time
import json
from typing import Dict, List, Callable, Optional, Any
from datetime import datetime
from collections import defaultdict
import asyncio


class MessageBroker:
    """메시지 브로커 - 분산 시스템의 중추"""

    def __init__(self):
        """브로커 초기화"""
        self.queues: Dict[str, queue.Queue] = defaultdict(queue.Queue)
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.message_history: List[Dict] = []
        self.lock = threading.Lock()

    def publish(self, topic: str, message: Any, sender: str = "Unknown"):
        """
        토픽에 메시지 발행 (Publish)

        Args:
            topic: 메시지 토픽 (채널)
            message: 메시지 내용
            sender: 발신자
        """
        with self.lock:
            # 메시지 객체 생성
            msg_obj = {
                'topic': topic,
                'data': message,
                'sender': sender,
                'timestamp': datetime.now().isoformat(),
                'id': f"{topic}_{len(self.message_history)}"
            }

            # 큐에 추가
            self.queues[topic].put(msg_obj)

            # 히스토리 저장
            self.message_history.append(msg_obj)

            print(f"📤 [{sender}] → [{topic}]: {message}")

    def subscribe(self, topic: str, consumer_id: str = "Unknown") -> Optional[Dict]:
        """
        토픽에서 메시지 구독 (Subscribe)

        Args:
            topic: 구독할 토픽
            consumer_id: 소비자 ID

        Returns:
            메시지 객체 또는 None
        """
        try:
            # 0.1초 타임아웃으로 메시지 대기
            msg = self.queues[topic].get(timeout=0.1)
            print(f"📥 [{consumer_id}] ← [{topic}]: {msg['data']}")
            return msg
        except queue.Empty:
            return None

    def get_stats(self) -> Dict:
        """브로커 통계"""
        with self.lock:
            return {
                'total_messages': len(self.message_history),
                'topics': {
                    topic: q.qsize() for topic, q in self.queues.items()
                },
                'history': self.message_history[-5:]  # 최근 5개
            }


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 4: 실전 마이크로서비스 - 전자상거래 시스템                            ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🛍️ 전자상거래 마이크로서비스 구조:

[고객]
  |
  ├─→ [API Gateway]
        |
        ├─→ [주문 서비스 (Order)]
        ├─→ [결제 서비스 (Payment)]
        ├─→ [배송 서비스 (Shipping)]
        └─→ [알림 서비스 (Notification)]

메시지 흐름:
1. 고객이 주문 생성
2. Order Service: "order.created" 이벤트 발행
3. Payment Service: 결제 처리 후 "payment.completed" 발행
4. Shipping Service: 배송 준비 후 "shipping.started" 발행
5. Notification Service: 각 이벤트마다 고객에게 알림
"""


class OrderService:
    """주문 서비스 (마이크로서비스)"""

    def __init__(self, broker: MessageBroker):
        self.broker = broker
        self.orders = {}

    def create_order(self, order_id: str, items: List[str], total: float) -> dict:
        """주문 생성"""
        order = {
            'id': order_id,
            'items': items,
            'total': total,
            'status': 'PENDING',
            'created_at': datetime.now().isoformat()
        }

        self.orders[order_id] = order

        # 이벤트 발행: 주문 생성됨
        self.broker.publish(
            'orders',
            {
                'event': 'order.created',
                'order_id': order_id,
                'total': total
            },
            sender='OrderService'
        )

        return order


class PaymentService:
    """결제 서비스 (마이크로서비스)"""

    def __init__(self, broker: MessageBroker):
        self.broker = broker
        self.payments = {}

    def process_payment(self, order_id: str, amount: float) -> dict:
        """결제 처리"""
        payment = {
            'order_id': order_id,
            'amount': amount,
            'status': 'SUCCESS',
            'transaction_id': f"TXN_{order_id}_{int(time.time())}",
            'processed_at': datetime.now().isoformat()
        }

        self.payments[order_id] = payment

        # 이벤트 발행: 결제 완료
        self.broker.publish(
            'payments',
            {
                'event': 'payment.completed',
                'order_id': order_id,
                'transaction_id': payment['transaction_id']
            },
            sender='PaymentService'
        )

        return payment


class ShippingService:
    """배송 서비스 (마이크로서비스)"""

    def __init__(self, broker: MessageBroker):
        self.broker = broker
        self.shipments = {}

    def prepare_shipping(self, order_id: str) -> dict:
        """배송 준비"""
        shipment = {
            'order_id': order_id,
            'status': 'PREPARED',
            'tracking_number': f"SHIP_{order_id}_{int(time.time())}",
            'prepared_at': datetime.now().isoformat()
        }

        self.shipments[order_id] = shipment

        # 이벤트 발행: 배송 준비 완료
        self.broker.publish(
            'shipments',
            {
                'event': 'shipping.prepared',
                'order_id': order_id,
                'tracking_number': shipment['tracking_number']
            },
            sender='ShippingService'
        )

        return shipment


class NotificationService:
    """알림 서비스 (마이크로서비스)"""

    def __init__(self, broker: MessageBroker):
        self.broker = broker
        self.notifications = []

    def send_notification(self, event: str, data: dict):
        """알림 전송"""
        notification = {
            'event': event,
            'data': data,
            'sent_at': datetime.now().isoformat()
        }

        self.notifications.append(notification)

        # 사용자에게 보낼 메시지
        messages = {
            'order.created': f"✅ 주문이 생성되었습니다. ID: {data.get('order_id')}",
            'payment.completed': f"💳 결제가 완료되었습니다. 거래번호: {data.get('transaction_id')}",
            'shipping.prepared': f"📦 배송이 준비되었습니다. 추적번호: {data.get('tracking_number')}"
        }

        msg = messages.get(event, f"알림: {event}")
        print(f"📧 [알림] {msg}")


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 5: Circuit Breaker - 장애 격리와 복원력                              ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🔌 Circuit Breaker 패턴:

전기회로의 차단기처럼 장애가 나면 자동으로 차단하는 패턴

상태 전이:
        ┌────────────────┐
        │ CLOSED (정상)  │
        │ 요청 통과      │
        └────────┬───────┘
                 │ 실패 증가
                 ↓
        ┌────────────────┐
        │ OPEN (차단)    │ ← 장애 격리!
        │ 요청 차단      │
        └────────┬───────┘
                 │ 일정시간 후
                 ↓
        ┌────────────────┐
        │HALF-OPEN (테스트)│
        │1개만 시도      │
        └────────┬───────┘
                 │
          성공?  │  실패?
          ▼      ▼
        CLOSED  OPEN

이점:
1️⃣ 카스케이드 실패 방지: A 서비스 고장 → B, C 연쇄 실패 X
2️⃣ 빠른 실패: "아 이 서비스 다운했구나" 즉시 판단
3️⃣ 자동 복구: 서비스 복구되면 자동으로 정상화
"""


class CircuitBreaker:
    """Circuit Breaker - 장애 격리"""

    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        """
        Circuit Breaker 초기화

        Args:
            failure_threshold: 차단까지 허용 실패 횟수
            timeout: OPEN 상태 유지 시간 (초)
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        """
        함수 호출 (Circuit Breaker로 보호)

        Args:
            func: 호출할 함수
            *args, **kwargs: 함수 인자

        Returns:
            함수 결과 또는 None
        """
        # OPEN 상태 확인
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                # HALF_OPEN 시도
                self.state = 'HALF_OPEN'
                print(f"⚠️  Circuit Breaker HALF_OPEN 전환 (재시도 시작)")
            else:
                # 여전히 OPEN
                print(f"🔴 Circuit Breaker OPEN (요청 차단)")
                return None

        # 함수 실행
        try:
            result = func(*args, **kwargs)
            # 성공
            self.failure_count = 0
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                print(f"🟢 Circuit Breaker CLOSED 복귀 (정상화)")
            return result
        except Exception as e:
            # 실패
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
                print(f"🔴 Circuit Breaker OPEN 전환 (실패 {self.failure_count}회)")

            print(f"❌ 요청 실패: {e}")
            return None


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 6: Service Discovery - 서비스 자동 탐색                               ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🔍 Service Discovery: 서비스들은 어디에 있는가?

문제:
  [마이크로서비스 초반]
  Order Service: "결제 서비스는 192.168.1.100:8001"
  (하드코딩)

  [마이크로서비스 확장]
  결제 서비스 3개로 확장:
    ├─ 192.168.1.100:8001 (Asia)
    ├─ 192.168.1.101:8001 (Europe)
    └─ 192.168.1.102:8001 (America)

  Order Service는 어디로 요청해야?

해결: Service Registry (서비스 목록 중앙 관리)

┌──────────────────────────────┐
│   Service Registry           │
│  (서비스 위치 저장소)        │
├──────────────────────────────┤
│ payment:                     │
│  ├─ 192.168.1.100:8001      │
│  ├─ 192.168.1.101:8001      │
│  └─ 192.168.1.102:8001      │
│ shipping:                    │
│  └─ 192.168.1.200:8002      │
│ notification:                │
│  └─ 192.168.1.300:8003      │
└──────────────────────────────┘

실무 도구: Consul, Eureka, etcd, Kubernetes
"""


class ServiceRegistry:
    """Service Registry - 서비스 탐색"""

    def __init__(self):
        """레지스트리 초기화"""
        self.services: Dict[str, List[Dict]] = defaultdict(list)
        self.lock = threading.Lock()

    def register(self, service_name: str, host: str, port: int, metadata: dict = None):
        """
        서비스 등록

        Args:
            service_name: 서비스 이름
            host: 호스트
            port: 포트
            metadata: 추가 메타데이터
        """
        with self.lock:
            service_instance = {
                'host': host,
                'port': port,
                'url': f"http://{host}:{port}",
                'metadata': metadata or {},
                'registered_at': datetime.now().isoformat(),
                'health': 'UP'
            }

            self.services[service_name].append(service_instance)
            print(f"✅ [{service_name}] 등록: {service_instance['url']}")

    def discover(self, service_name: str):
        """
        서비스 발견

        Args:
            service_name: 찾을 서비스 이름

        Returns:
            서비스 정보
        """
        with self.lock:
            instances = self.services.get(service_name, [])

            if not instances:
                print(f"❌ [{service_name}] 서비스 없음")
                return None

            # 라운드 로빈 (Round Robin) - 부하 분산
            instance = instances[len(self.services) % len(instances)]
            print(f"🔍 [{service_name}] 발견: {instance['url']}")
            return instance

    def list_services(self) -> Dict:
        """모든 서비스 목록"""
        with self.lock:
            return {
                name: [
                    {'url': s['url'], 'health': s['health']}
                    for s in services
                ]
                for name, services in self.services.items()
            }


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 7: 데모 함수들                                                        ║
# ╚════════════════════════════════════════════════════════════════════════════╝

def demonstration_1_message_broker():
    """데모 1: 메시지 브로커 기본 동작"""
    print("\n" + "="*80)
    print("데모 1: 메시지 브로커 - 느슨한 결합")
    print("="*80)

    broker = MessageBroker()

    # Publisher: 메시지 발행
    print("\n[Publisher] 메시지 발행:")
    broker.publish('orders', {'order_id': '001', 'total': 100}, sender='OrderService')
    broker.publish('orders', {'order_id': '002', 'total': 200}, sender='OrderService')

    # Subscriber: 메시지 구독
    print("\n[Subscriber] 메시지 구독:")
    msg1 = broker.subscribe('orders', consumer_id='PaymentService')
    msg2 = broker.subscribe('orders', consumer_id='ShippingService')

    # 통계
    print("\n[통계]")
    stats = broker.get_stats()
    print(f"총 메시지: {stats['total_messages']}")


def demonstration_2_ecommerce_workflow():
    """데모 2: 전자상거래 워크플로우"""
    print("\n" + "="*80)
    print("데모 2: 마이크로서비스 - 전자상거래 주문 처리")
    print("="*80)

    broker = MessageBroker()

    # 서비스 생성
    order_service = OrderService(broker)
    payment_service = PaymentService(broker)
    shipping_service = ShippingService(broker)
    notification_service = NotificationService(broker)

    # 1. 주문 생성
    print("\n[Step 1] 고객이 주문 생성")
    order = order_service.create_order(
        'ORD_2024_001',
        ['상품A', '상품B'],
        total=50000
    )

    # 2. 결제 처리
    print("\n[Step 2] 결제 서비스가 주문 감지 후 결제")
    time.sleep(0.5)
    payment = payment_service.process_payment('ORD_2024_001', 50000)

    # 3. 배송 준비
    print("\n[Step 3] 배송 서비스가 결제 완료 감지 후 배송 준비")
    time.sleep(0.5)
    shipment = shipping_service.prepare_shipping('ORD_2024_001')

    # 4. 고객 알림
    print("\n[Step 4] 알림 서비스가 각 이벤트 감지 후 알림 전송")
    notification_service.send_notification('order.created', {'order_id': 'ORD_2024_001'})
    notification_service.send_notification('payment.completed', {'transaction_id': 'TXN_001'})
    notification_service.send_notification('shipping.prepared', {'tracking_number': 'SHIP_001'})

    print("\n✓ 전체 워크플로우 완료")


def demonstration_3_circuit_breaker():
    """데모 3: Circuit Breaker 패턴"""
    print("\n" + "="*80)
    print("데모 3: Circuit Breaker - 장애 격리")
    print("="*80)

    circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=2.0)

    def unstable_service():
        """불안정한 서비스"""
        import random
        if random.random() < 0.7:  # 70% 실패율
            raise Exception("서비스 오류!")
        return "성공"

    print("\n정상 호출:")
    for i in range(10):
        result = circuit_breaker.call(unstable_service)
        time.sleep(0.1)

    print(f"\nCircuit Breaker 최종 상태: {circuit_breaker.state}")


def demonstration_4_service_discovery():
    """데모 4: Service Discovery"""
    print("\n" + "="*80)
    print("데모 4: Service Discovery - 서비스 자동 탐색")
    print("="*80)

    registry = ServiceRegistry()

    # 서비스 등록
    print("\n[1] 서비스 등록:")
    registry.register('payment', 'payment-1.example.com', 8001, {'region': 'Asia'})
    registry.register('payment', 'payment-2.example.com', 8001, {'region': 'Europe'})
    registry.register('shipping', 'shipping-1.example.com', 8002)

    # 서비스 발견
    print("\n[2] 서비스 발견:")
    payment = registry.discover('payment')
    shipping = registry.discover('shipping')

    # 서비스 목록
    print("\n[3] 전체 서비스 목록:")
    services = registry.list_services()
    for service_name, instances in services.items():
        print(f"  {service_name}: {len(instances)}개 인스턴스")
        for instance in instances:
            print(f"    - {instance['url']} ({instance['health']})")


def demonstration_5_cap_theorem():
    """데모 5: CAP 이론 시뮬레이션"""
    print("\n" + "="*80)
    print("데모 5: CAP 이론 - 분산 시스템의 트레이드오프")
    print("="*80)

    print("""
┌────────────────────────────────────────────────────────┐
│ 세 가지 시스템 특성 선택:                              │
├────────────────────────────────────────────────────────┤
│                                                        │
│ 1️⃣ Consistency + Availability (CA)                   │
│    └─ 은행 (매우 안정적 네트워크)                     │
│                                                        │
│ 2️⃣ Consistency + Partition Tolerance (CP)            │
│    └─ Google BigTable (강한 일관성)                   │
│                                                        │
│ 3️⃣ Availability + Partition Tolerance (AP)           │
│    └─ Amazon, Netflix (최종 일관성)                   │
│                                                        │
│ ❌ 모두 불가능                                        │
│    └─ 분산 시스템의 근본 한계                         │
│                                                        │
└────────────────────────────────────────────────────────┘

📊 트레이드오프 분석:

┌─────────────────────────────────────┐
│ System  │ 일관성│ 가용성│ 분할 내구성│
├─────────────────────────────────────┤
│ CA      │ ✓✓✓  │ ✓✓✓  │ ✗         │
│ CP      │ ✓✓✓  │ ✗    │ ✓✓✓      │
│ AP      │ ✗    │ ✓✓✓  │ ✓✓✓      │
└─────────────────────────────────────┘

💡 현실적 선택:
   대부분 AP를 선택 (최종 일관성 수용)
   → 데이터는 결국 일치하지만 시간 걸림
    """)


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 8: 단위 테스트 (5/5)                                                 ║
# ╚════════════════════════════════════════════════════════════════════════════╝

import unittest


class TestMicroservices(unittest.TestCase):
    """마이크로서비스 단위 테스트"""

    def test_1_message_broker(self):
        """테스트 1: 메시지 브로커"""
        print("\n" + "="*80)
        print("테스트 1: 메시지 브로커")
        print("="*80)

        broker = MessageBroker()

        # 메시지 발행
        broker.publish('test_topic', {'data': 'test'}, sender='TestService')

        # 메시지 구독
        msg = broker.subscribe('test_topic', consumer_id='TestConsumer')

        self.assertIsNotNone(msg)
        self.assertEqual(msg['topic'], 'test_topic')
        self.assertEqual(msg['data'], {'data': 'test'})

        print("✓ PASS: 메시지 브로커 작동")

    def test_2_order_service(self):
        """테스트 2: 주문 서비스"""
        print("\n" + "="*80)
        print("테스트 2: 주문 서비스")
        print("="*80)

        broker = MessageBroker()
        order_service = OrderService(broker)

        order = order_service.create_order('ORD_001', ['상품A'], 1000)

        self.assertEqual(order['id'], 'ORD_001')
        self.assertEqual(order['status'], 'PENDING')
        self.assertEqual(order['total'], 1000)

        print("✓ PASS: 주문 서비스 작동")

    def test_3_payment_service(self):
        """테스트 3: 결제 서비스"""
        print("\n" + "="*80)
        print("테스트 3: 결제 서비스")
        print("="*80)

        broker = MessageBroker()
        payment_service = PaymentService(broker)

        payment = payment_service.process_payment('ORD_001', 1000)

        self.assertEqual(payment['order_id'], 'ORD_001')
        self.assertEqual(payment['status'], 'SUCCESS')
        self.assertIsNotNone(payment['transaction_id'])

        print("✓ PASS: 결제 서비스 작동")

    def test_4_service_discovery(self):
        """테스트 4: Service Discovery"""
        print("\n" + "="*80)
        print("테스트 4: Service Discovery")
        print("="*80)

        registry = ServiceRegistry()

        # 서비스 등록
        registry.register('payment', 'localhost', 8001)

        # 서비스 발견
        service = registry.discover('payment')

        self.assertIsNotNone(service)
        self.assertEqual(service['host'], 'localhost')
        self.assertEqual(service['port'], 8001)

        print("✓ PASS: Service Discovery 작동")

    def test_5_circuit_breaker(self):
        """테스트 5: Circuit Breaker"""
        print("\n" + "="*80)
        print("테스트 5: Circuit Breaker")
        print("="*80)

        breaker = CircuitBreaker(failure_threshold=2, timeout=1.0)

        def failing_func():
            raise Exception("Error")

        def success_func():
            return "OK"

        # 실패 2회
        breaker.call(failing_func)
        breaker.call(failing_func)

        # 이제 OPEN 상태
        self.assertEqual(breaker.state, 'OPEN')

        # 요청 차단됨
        result = breaker.call(success_func)
        self.assertIsNone(result)

        print("✓ PASS: Circuit Breaker 작동")


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 9: 완성 및 다음 단계                                                  ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
✨ v5.1 완성 요약:

✅ 학습 내용:
   1. Monolithic vs Microservices 아키텍처
   2. CAP 이론: 일관성/가용성/분할 내구성 트레이드오프
   3. Message Broker: 느슨한 결합과 이벤트 기반 설계
   4. 마이크로서비스 패턴: Order, Payment, Shipping, Notification
   5. Circuit Breaker: 장애 격리와 복원력
   6. Service Discovery: 서비스 자동 탐색과 부하 분산
   7. 실전 전자상거래 워크플로우

🏗️ 아키텍처 진화:
   v4.1-v4.3: 단일 머신의 효율화 (Asyncio, Multiprocessing, Socket)
   v5.1-현재: 분산 시스템의 설계 (Microservices, Message Broker)
   v5.2-다음: 데이터 계층 (DB 최적화, NoSQL)
   v5.3-예정: 관찰 가능성 (Logging, Monitoring, Tracing)

🚀 다음 단계:
   [v5.2] 데이터베이스 정규화와 NoSQL
   - SQL vs NoSQL 트레이드오프
   - 데이터 일관성 (ACID vs BASE)
   - 샤딩과 복제 전략
   - 실전: MongoDB, Redis

   [v5.3] 모니터링과 로깅
   - 분산 시스템의 관찰 가능성
   - 로그 수집 (ELK Stack)
   - 메트릭 모니터링
   - 트레이싱 (Jaeger, Zipkin)

💡 실무 적용:
   • Netflix: Hystrix (Circuit Breaker)
   • Amazon: SQS (Message Broker)
   • Google: Kubernetes (Orchestration)
   • Airbnb: Presto (분산 쿼리)

> "한 대의 슈퍼컴퓨터보다 수천 대의 작은 컴퓨터가 더 강력하다"
> - 이제 그 원리를 설계자님이 이해하고 구현할 수 있습니다!
"""


if __name__ == "__main__":
    # 데모 실행
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + "  Python University Level 3 - v5.1 Distributed Microservices".center(78) + "║")
    print("║" + "  복잡성 속의 질서: 분산 시스템 설계".center(78) + "║")
    print("╚" + "="*78 + "╝")

    # 데모 실행
    demonstration_1_message_broker()
    demonstration_2_ecommerce_workflow()
    demonstration_3_circuit_breaker()
    demonstration_4_service_discovery()
    demonstration_5_cap_theorem()

    # 단위 테스트 실행
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + "  UNIT TESTS".center(78) + "║")
    print("╚" + "="*78 + "╝")

    unittest.main(argv=[''], exit=False, verbosity=2)

    print("\n" + "="*80)
    print("✨ v5.1 완성! 마이크로서비스 아키텍처 마스터 달성")
    print("="*80)
    print("\n다음 단계: v5.2 데이터베이스 정규화와 NoSQL")
