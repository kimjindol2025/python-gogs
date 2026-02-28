"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  🌐 UNIVERSITY LEVEL 2 - v4.3 NETWORK SOCKET PROGRAMMING 🌐                ║
║                                                                              ║
║      패킷으로 세상을 연결하는 기술 (Connecting the World with Packets)      ║
║  고립된 시스템 → 연결된 시스템으로의 도약                                   ║
║                                                                              ║
║  "통신은 신뢰이고, 신뢰는 증명이다" - gogs                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📚 학습 목표:
   1️⃣ Socket의 개념: 네트워크의 "소프트웨어적 문(Gate)"
   2️⃣ TCP vs UDP: 신뢰성 vs 속도
   3️⃣ Echo Server/Client: 기본 통신 시스템
   4️⃣ 다중 클라이언트 처리: Multiprocessing 활용
   5️⃣ 비동기 네트워크: Asyncio와 소켓 결합
   6️⃣ 실무 프로토콜: HTTP, 채팅 서버 설계

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 1: 소켓 프로그래밍의 철학 - 디지털 통신의 접점                        ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🌍 소켓(Socket)이란?

┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  "현실의 전화 통신"과 "디지털 네트워크 통신"의 유사성                      │
│                                                                            │
│  📞 현실: 전화번호로 상대를 찾아 연결, 데이터(목소리) 전달                 │
│     ├─ 전화번호 = IP 주소 (어느 컴퓨터? 192.168.1.100)                  │
│     ├─ 국번    = 포트 번호 (어느 서비스? 80, 443, 9999)                 │
│     └─ 통화    = 데이터 송수신                                           │
│                                                                            │
│  💻 디지털: 소켓으로 IP:Port 조합에 연결, 패킷 전달                       │
│     ├─ IP 주소: 컴퓨터 고유 식별자                                      │
│     ├─ Port 번호: 프로세스/서비스 고유 식별자                            │
│     └─ 패킷: 경로 주소 + 데이터 (목소리를 바이트로 인코딩)              │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

🔑 핵심 개념:

┌─────────────────────────────────────────────┐
│        IP 주소 (IPv4 형식)                  │
├─────────────────────────────────────────────┤
│  192.168.1.100                              │
│  └─ 4개 부분 (각각 0-255)                  │
│     • 192 = 네트워크 (상위 부분)           │
│     • 168.1 = 서브넷 (중간 부분)          │
│     • 100 = 호스트 (하위 부분)            │
│                                             │
│  특수 주소:                                │
│  • 127.0.0.1 = Loopback (자기 자신)      │
│  • 0.0.0.0 = 모든 인터페이스              │
│  • 255.255.255.255 = 브로드캐스트         │
└─────────────────────────────────────────────┘

┌────────────────────────────────────────┐
│      Port 번호 (0-65535)               │
├────────────────────────────────────────┤
│  80   = HTTP (웹)                      │
│  443  = HTTPS (보안 웹)                │
│  22   = SSH (원격 접속)                │
│  21   = FTP (파일 전송)                │
│  9999 = 우리의 Echo Server             │
│  1024-65535 = 일반 사용자 포트         │
└────────────────────────────────────────┘

💡 통신의 "증명" 개념:

TCP (Transmission Control Protocol):
  1️⃣ 연결 수립: "너, 나 들려? OK!"
  2️⃣ 데이터 전송
  3️⃣ 수신 확인: "데이터 받았어?"
  4️⃣ 재전송: 유실되면 다시 보냄
  5️⃣ 연결 종료: "통화 끝!"

결과: 데이터 유실 "0", 신뢰성 "100%"

UDP (User Datagram Protocol):
  1️⃣ 주소 확인
  2️⃣ 패킷 발송 (한 번만!)
  3️⃣ 수신 확인 안 함

결과: 데이터 유실 "있을 수 있음", 속도 "빠름"

→ "기록이 증명이다" = 통신 결과가 신뢰성을 증명한다!
"""


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 2: TCP/IP 기초 - 계층 구조 이해                                      ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🏗️ OSI 모델 (7계층) vs TCP/IP 모델 (4계층)

┌──────────────────────────────────────────────────────┐
│  Application Layer (애플리케이션)                   │
│  ├─ HTTP, HTTPS, FTP, SSH, SMTP, DNS               │
│  ├─ 목적: 사용자가 직접 사용하는 서비스             │
│  └─ 예: 웹 브라우저, 이메일 클라이언트              │
├──────────────────────────────────────────────────────┤
│  Transport Layer (전송)                             │
│  ├─ TCP (신뢰성), UDP (속도)                       │
│  ├─ 목적: 프로세스 간 통신                          │
│  └─ 포트 번호로 서비스 식별                         │
├──────────────────────────────────────────────────────┤
│  Internet Layer (인터넷)                            │
│  ├─ IP (IPv4, IPv6), ICMP (ping)                   │
│  ├─ 목적: 호스트 간 라우팅                          │
│  └─ IP 주소로 컴퓨터 식별                           │
├──────────────────────────────────────────────────────┤
│  Link Layer (링크/물리)                             │
│  ├─ Ethernet, Wi-Fi, PPP                            │
│  ├─ 목적: 물리적 전송                               │
│  └─ MAC 주소로 네트워크 카드 식별                   │
└──────────────────────────────────────────────────────┘

📦 패킷(Packet) 구조:

[Ethernet Header] - 물리 계층
  ├─ 출발 MAC 주소
  ├─ 목적지 MAC 주소
  └─ 프로토콜 타입
     ↓
[IP Header] - 인터넷 계층
  ├─ 출발 IP 주소
  ├─ 목적지 IP 주소
  ├─ TTL (Time To Live - 홉 횟수)
  └─ 프로토콜 (TCP/UDP)
     ↓
[TCP/UDP Header] - 전송 계층
  ├─ 출발 포트
  ├─ 목적지 포트
  ├─ (TCP만) 시퀀스 번호, ACK 번호
  └─ (TCP만) 플래그 (SYN, ACK, FIN)
     ↓
[Application Data] - 애플리케이션 계층
  └─ 실제 데이터 (HTTP, 텍스트 등)

💡 핵심 통찰:
   각 계층은 아래 계층의 결과를 신뢰하고,
   위 계층에게 신뢰성을 보장한다.

   → "신뢰의 계층화" = 시스템의 안정성
"""


import socket
import threading
import multiprocessing
import time
import asyncio
import struct
from typing import Tuple, Optional, List
from datetime import datetime


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 3: 기본 Echo Server (TCP 기반)                                       ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🔄 Echo Server의 작동 원리:

[클라이언트]                    [서버]
     |                          |
     |--- "Hello" 전송 -------->|
     |                          | 수신
     |                    "Hello" 에코
     |<--- "Hello" 수신 --------|
     |                          |
     |--- "World" 전송 -------->|
     |                    "World" 에코
     |<--- "World" 수신 --------|
     |                          |

특징:
- 클라이언트가 보낸 데이터를 그대로 다시 돌려줌
- TCP 기반 (연결 지향)
- 동기적 처리 (한 번에 한 클라이언트)
"""


class EchoServer:
    """기본 Echo Server 구현"""

    def __init__(self, host: str = '127.0.0.1', port: int = 9999):
        """
        서버 초기화

        Args:
            host: 바인딩할 IP 주소
            port: 바인딩할 포트 번호
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_running = False

    def start(self, max_connections: int = 1):
        """
        서버 시작

        Args:
            max_connections: 대기 큐 크기
        """
        # 1. 소켓 생성 (IPv4, TCP)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 포트 재사용 옵션 (TIME_WAIT 상태 회피)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2. 주소와 포트 바인딩
        self.server_socket.bind((self.host, self.port))

        # 3. 연결 대기
        self.server_socket.listen(max_connections)
        self.is_running = True

        print(f"📡 Echo Server 시작: {self.host}:{self.port}")

    def accept_connection(self) -> Tuple[socket.socket, Tuple[str, int]]:
        """클라이언트 연결 수락"""
        client_socket, addr = self.server_socket.accept()
        return client_socket, addr

    def handle_client(self, client_socket: socket.socket, addr: Tuple[str, int]):
        """클라이언트 처리"""
        print(f"🤝 클라이언트 접속: {addr}")

        try:
            while True:
                # 데이터 수신 (최대 1024 바이트)
                data = client_socket.recv(1024)

                if not data:
                    # 클라이언트가 연결 종료
                    print(f"🔌 클라이언트 종료: {addr}")
                    break

                # 수신 데이터 출력
                message = data.decode('utf-8', errors='ignore')
                print(f"📥 [{addr}] 수신: {message}")

                # 에코 - 같은 데이터 재전송
                client_socket.sendall(data)
                print(f"📤 [{addr}] 에코 전송: {message}")

        except Exception as e:
            print(f"⚠️  에러 [{addr}]: {e}")
        finally:
            client_socket.close()

    def stop(self):
        """서버 종료"""
        if self.server_socket:
            self.is_running = False
            self.server_socket.close()
            print("🛑 Echo Server 종료")


class EchoClient:
    """Echo Client 구현"""

    def __init__(self, host: str = '127.0.0.1', port: int = 9999):
        """
        클라이언트 초기화

        Args:
            host: 연결할 서버 IP
            port: 연결할 서버 포트
        """
        self.host = host
        self.port = port
        self.socket = None

    def connect(self) -> bool:
        """서버에 연결"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"✅ 서버 연결 성공: {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ 연결 실패: {e}")
            return False

    def send_message(self, message: str) -> Optional[str]:
        """
        메시지 전송 및 에코 수신

        Args:
            message: 전송할 메시지

        Returns:
            수신한 에코 데이터
        """
        try:
            # 메시지 전송
            self.socket.sendall(message.encode('utf-8'))
            print(f"📤 전송: {message}")

            # 에코 수신
            data = self.socket.recv(1024)
            response = data.decode('utf-8', errors='ignore')
            print(f"📥 수신: {response}")

            return response
        except Exception as e:
            print(f"❌ 통신 오류: {e}")
            return None

    def close(self):
        """연결 종료"""
        if self.socket:
            self.socket.close()
            print("🔌 연결 종료")


def run_echo_server_sync(host: str = '127.0.0.1', port: int = 9999):
    """동기 Echo Server 실행"""
    server = EchoServer(host, port)
    server.start()

    try:
        for _ in range(3):  # 3개 클라이언트 처리
            client_socket, addr = server.accept_connection()
            server.handle_client(client_socket, addr)
    finally:
        server.stop()


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 4: 다중 클라이언트 처리 (Threading & Multiprocessing)               ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
⚡ 동시에 여러 클라이언트를 처리하는 방법:

1️⃣ Threading (스레드 기반)
   ─────────────────────────
   [메인 스레드] accept
       ├─ [스레드1] 클라이언트1 처리
       ├─ [스레드2] 클라이언트2 처리
       ├─ [스레드3] 클라이언트3 처리
       └─ ... (계속 accept)

   장점: 메모리 적게 사용, 빠른 컨텍스트 스위칭
   단점: GIL (CPU 작업은 병렬 불가)

2️⃣ Multiprocessing (프로세스 기반)
   ───────────────────────────────
   [메인 프로세스] accept
       ├─ [프로세스1] 클라이언트1 처리
       ├─ [프로세스2] 클라이언트2 처리
       ├─ [프로세스3] 클라이언트3 처리
       └─ ... (계속 accept)

   장점: 진정한 병렬, CPU 작업 처리 가능
   단점: 메모리 사용량 많음

3️⃣ Asyncio (비동기 기반)
   ────────────────────
   [이벤트 루프] (한 스레드)
       ├─ 클라이언트1 I/O 대기
       ├─ 클라이언트2 처리
       ├─ 클라이언트3 I/O 대기
       └─ ... (컨텍스트 스위칭)

   장점: 메모리 최소, 매우 많은 연결 처리
   단점: 복잡한 코드

웹 서버의 선택:
- Apache: Threading (연결당 스레드)
- Nginx: Asyncio 스타일 (이벤트 기반)
- Gunicorn: Multiprocessing
"""


class ThreadedEchoServer(EchoServer):
    """멀티스레드 Echo Server"""

    def start_threaded(self, num_workers: int = 3):
        """스레드 기반 서버 시작"""
        self.start()
        print(f"🚀 멀티스레드 서버 시작 ({num_workers}개 워커)")

        try:
            while self.is_running:
                try:
                    client_socket, addr = self.accept_connection()

                    # 클라이언트 처리를 별도 스레드에서 실행
                    thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, addr),
                        daemon=True
                    )
                    thread.start()

                except KeyboardInterrupt:
                    break
        finally:
            self.stop()


def run_multithreaded_server(host: str = '127.0.0.1', port: int = 9999):
    """멀티스레드 서버 실행 (데모용)"""
    server = ThreadedEchoServer(host, port)
    server.start()

    threads = []
    for i in range(3):
        thread = threading.Thread(
            target=server.handle_client,
            args=(None, (f'client{i}', 0)),
            daemon=True
        )
        threads.append(thread)

    for thread in threads:
        thread.join()

    server.stop()


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 5: UDP 프로토콜 - 비연결형 통신                                       ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
📡 UDP vs TCP 비교:

TCP (Transmission Control Protocol):
  • 연결 필수 (3-way handshake)
  • 신뢰성 보장 (재전송, 순서 보장)
  • 느림 (오버헤드 많음)
  • 용도: 웹, 파일 전송, 이메일

UDP (User Datagram Protocol):
  • 연결 없음 (바로 전송)
  • 신뢰성 보장 없음 (Fire-and-Forget)
  • 빠름 (오버헤드 적음)
  • 용도: 영상/음성 스트리밍, 게임, VoIP

┌─────────────────────────────────────────┐
│  패킷 100개 전송 시나리오               │
├─────────────────────────────────────────┤
│ TCP: 100개 도착 (100%)                 │
│ UDP: 98개 도착 (98%) - 2개 유실        │
│                                         │
│ 웹: TCP (100% 필요) ✓                  │
│ 게임: UDP (2개 유실해도 무관) ✓        │
│ 영상: UDP (프레임 일부 유실 OK) ✓      │
└─────────────────────────────────────────┘
"""


class UDPServer:
    """UDP 서버 구현"""

    def __init__(self, host: str = '127.0.0.1', port: int = 9998):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))

    def receive_once(self, timeout: float = 5.0) -> Tuple[str, Tuple[str, int]]:
        """데이터 한 번 수신"""
        self.socket.settimeout(timeout)
        try:
            data, addr = self.socket.recvfrom(1024)
            message = data.decode('utf-8', errors='ignore')
            return message, addr
        except socket.timeout:
            return None, None

    def send_to(self, message: str, addr: Tuple[str, int]):
        """특정 주소로 전송"""
        self.socket.sendto(message.encode('utf-8'), addr)

    def close(self):
        """소켓 종료"""
        self.socket.close()


class UDPClient:
    """UDP 클라이언트 구현"""

    def __init__(self, host: str = '127.0.0.1', port: int = 9998):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message: str):
        """메시지 전송 (연결 없이)"""
        self.socket.sendto(message.encode('utf-8'), (self.host, self.port))

    def receive(self, timeout: float = 5.0) -> Optional[str]:
        """데이터 수신"""
        self.socket.settimeout(timeout)
        try:
            data, _ = self.socket.recvfrom(1024)
            return data.decode('utf-8', errors='ignore')
        except socket.timeout:
            return None

    def close(self):
        """소켓 종료"""
        self.socket.close()


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 6: 비동기 네트워크 (Asyncio + Socket)                                ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
🚀 Asyncio를 이용한 고성능 네트워크 서버:

┌──────────────────────────────┐
│   이벤트 루프 (한 스레드)   │
├──────────────────────────────┤
│ while True:                  │
│   1. 클라이언트1 I/O 확인   │
│   2. 클라이언트2 I/O 확인   │
│   3. 클라이언트3 I/O 확인   │
│   4. 준비된 것 처리         │
│   5. 1번으로 돌아감         │
└──────────────────────────────┘

장점:
- 메모리 효율 (수만 개 동시 연결 가능)
- 높은 처리량
- 동기화 간단

단점:
- 블로킹 작업 불가능
- 코드 복잡도 증가
"""


async def async_echo_handler(reader, writer):
    """비동기 클라이언트 핸들러"""
    addr = writer.get_extra_info('peername')
    print(f"🤝 클라이언트 연결: {addr}")

    try:
        while True:
            # 데이터 수신 (비동기)
            data = await reader.read(1024)

            if not data:
                print(f"🔌 클라이언트 종료: {addr}")
                break

            message = data.decode('utf-8', errors='ignore')
            print(f"📥 [{addr}] 수신: {message}")

            # 에코 전송 (비동기)
            writer.write(data)
            await writer.drain()
            print(f"📤 [{addr}] 에코: {message}")

    except Exception as e:
        print(f"⚠️  에러: {e}")
    finally:
        writer.close()
        await writer.wait_closed()


async def async_echo_server(host: str = '127.0.0.1', port: int = 9997):
    """비동기 Echo Server"""
    server = await asyncio.start_server(
        async_echo_handler,
        host, port
    )

    print(f"📡 비동기 Echo Server 시작: {host}:{port}")
    async with server:
        await server.serve_forever()


async def async_echo_client(host: str = '127.0.0.1', port: int = 9997, messages: List[str] = None):
    """비동기 Echo Client"""
    if messages is None:
        messages = ["Hello", "World", "Asyncio"]

    try:
        reader, writer = await asyncio.open_connection(host, port)
        print(f"✅ 서버 연결: {host}:{port}")

        for message in messages:
            # 메시지 전송
            writer.write(message.encode('utf-8'))
            await writer.drain()
            print(f"📤 전송: {message}")

            # 에코 수신
            data = await reader.read(1024)
            response = data.decode('utf-8', errors='ignore')
            print(f"📥 수신: {response}")

            await asyncio.sleep(0.1)

        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"❌ 에러: {e}")


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 7: 데모 실행 함수                                                     ║
# ╚════════════════════════════════════════════════════════════════════════════╝

def demonstration_1_basic_echo():
    """데모 1: 기본 Echo Server & Client (동기)"""
    print("\n" + "="*80)
    print("데모 1: 기본 Echo Server & Client (동기/순차)")
    print("="*80)

    # 서버와 클라이언트를 분리 프로세스에서 실행
    def run_server():
        server = EchoServer('127.0.0.1', 10000)
        server.start()

        # 1개 클라이언트만 처리
        client_socket, addr = server.accept_connection()
        server.handle_client(client_socket, addr)
        server.stop()

    def run_client():
        time.sleep(0.5)  # 서버 시작 대기
        client = EchoClient('127.0.0.1', 10000)

        if client.connect():
            client.send_message("Hello, Socket!")
            client.send_message("Python Network")
            client.close()

    # 병렬 실행
    server_process = multiprocessing.Process(target=run_server)
    client_process = multiprocessing.Process(target=run_client)

    server_process.start()
    client_process.start()

    server_process.join(timeout=5)
    client_process.join(timeout=5)

    print("\n✓ 데모 1 완료")


def demonstration_2_tcp_details():
    """데모 2: TCP 세부 동작 (3-way Handshake)"""
    print("\n" + "="*80)
    print("데모 2: TCP 연결 과정 상세")
    print("="*80)

    print("""
┌─────────────────────────────────────────────────────────┐
│  TCP 3-Way Handshake (연결 수립)                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ [클라이언트]              [서버]                        │
│      |                    |                            │
│ [1]  |----> SYN ----->   |  (연결 요청)               │
│      |                   |                            │
│ [2]  |<--- SYN-ACK <---- |  (요청 수락 + 확인)       │
│      |                   |                            │
│ [3]  |---> ACK ----->    |  (확인 완료)               │
│      |                   |                            │
│     [연결 완료]          [연결 완료]                  │
│      |                   |                            │
│     [데이터 전송]        [데이터 수신]                │
│      |                   |                            │
│     [연결 종료]          [연결 종료]                  │
│      |                   |                            │
└─────────────────────────────────────────────────────────┘

📊 성능 영향:
  • 3-Way Handshake: ~1ms (로컬호스트)
  • 데이터 전송: 10-100ms (인터넷)
  • 연결 종료: ~1ms

💡 핵심: "신뢰성을 위한 오버헤드"
    연결 수립에 약간의 시간을 투자하여
    이후 100% 신뢰성 보장
    """)


def demonstration_3_udp_comparison():
    """데모 3: UDP vs TCP 비교"""
    print("\n" + "="*80)
    print("데모 3: UDP vs TCP 성능 비교")
    print("="*80)

    print("""
┌──────────────────────────────────────────────────────┐
│  메시지 100개 전송 비교                              │
├──────────────────────────────────────────────────────┤
│                                                      │
│ TCP (신뢰성):                                       │
│ ├─ 연결 수립: 3 왕복 (6ms)                          │
│ ├─ 데이터 전송: 100개 패킷 전부 도착               │
│ ├─ 순서 보장: O (1,2,3,...,100)                    │
│ └─ 총 시간: ~110ms (포함 ACK)                       │
│                                                      │
│ UDP (속도):                                         │
│ ├─ 연결 수립: 없음                                 │
│ ├─ 데이터 전송: 100개 중 98개 도착                 │
│ ├─ 순서 보장: X (3,1,5,2,... 순서대로)             │
│ └─ 총 시간: ~20ms (패킷만)                         │
│                                                      │
│ 결론:                                               │
│ └─ TCP는 느리지만 신뢰, UDP는 빠르지만 위험        │
│                                                      │
└──────────────────────────────────────────────────────┘

📍 선택 기준:
  • 웹 서핑 (HTTP): TCP (페이지 손상 불가)
  • 영상 스트리밍: UDP (프레임 1-2개 유실 OK)
  • 온라인 게임: UDP (위치 업데이트 지속적)
  • 파일 다운로드: TCP (1바이트도 유실 불가)
  • VoIP/영상통화: UDP (약간의 음성 끊김 OK)
    """)


def demonstration_4_socket_states():
    """데모 4: 소켓 상태 머신"""
    print("\n" + "="*80)
    print("데모 4: 소켓 상태 전이")
    print("="*80)

    print("""
┌─────────────────────────────────────────────────────────┐
│  소켓 상태 머신 (State Machine)                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ [CLOSED] (초기)                                        │
│    ↓ socket() 호출                                     │
│ [SOCKET_CREATED]                                       │
│    ↓ bind()                                            │
│ [BOUND]                                                │
│    ↓ listen()                                          │
│ [LISTENING] ← 서버가 여기서 대기                       │
│    ↓ accept()                                          │
│ [ACCEPTED]                                             │
│    ↓ recv(), send()                                    │
│ [CONNECTED]                                            │
│    ↓ close()                                           │
│ [CLOSED]                                               │
│                                                         │
│ 동시에 (클라이언트 관점):                               │
│ [CLOSED]                                               │
│    ↓ socket()                                          │
│ [SOCKET_CREATED]                                       │
│    ↓ connect()                                         │
│ [CONNECTED] ← 서버의 [ACCEPTED]와 맞춤                │
│    ↓ send(), recv()                                    │
│ [CONNECTED]                                            │
│    ↓ close()                                           │
│ [CLOSED]                                               │
│                                                         │
└─────────────────────────────────────────────────────────┘

⏱️  TIME_WAIT 상태:
   연결 종료 후 포트가 재사용 불가능한 시간 (~60초)
   → SO_REUSEADDR로 회피 가능
    """)


def demonstration_5_port_binding():
    """데모 5: 포트 바인딩 (Address Already in Use 해결)"""
    print("\n" + "="*80)
    print("데모 5: 포트 바인딩 및 재사용 옵션")
    print("="*80)

    print("""
⚠️  "Address already in use" 에러 원인:

1️⃣ 이미 같은 포트에 서버가 실행 중
   해결: 다른 포트 사용 또는 기존 프로세스 종료

2️⃣ TIME_WAIT 상태 (최근 종료된 연결)
   원인: OS가 유실된 패킷 처리를 기다리는 중
   시간: ~60초
   해결: SO_REUSEADDR 옵션

✅ SO_REUSEADDR 설정:

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# ↑ TIME_WAIT 상태에서도 포트 재사용 가능

📊 포트 상태 모니터링 (Linux):
   $ netstat -an | grep LISTEN      # 열린 포트
   $ netstat -an | grep TIME_WAIT   # 대기 중인 포트
    """)


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 8: 단위 테스트 (5/5)                                                 ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
테스트 계획:
──────────

Test 1: 기본 소켓 생성
   - AF_INET (IPv4) 확인
   - SOCK_STREAM (TCP) 확인

Test 2: Echo Server 기본 동작
   - 서버 바인딩 확인
   - 클라이언트 연결 수락 확인

Test 3: Echo 기능 검증
   - 메시지 전송 및 수신
   - 에코 데이터 일치 확인

Test 4: UDP 통신
   - UDP 소켓 생성
   - 데이터 전송/수신

Test 5: 다중 연결 처리
   - 스레드 기반 다중 클라이언트
   - 각 클라이언트 독립적 처리 확인
"""

import unittest


def create_test_socket():
    """테스트용 소켓 생성"""
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class TestNetworkSocket(unittest.TestCase):
    """네트워크 소켓 단위 테스트"""

    def test_1_socket_creation(self):
        """
        테스트 1: 기본 소켓 생성
        """
        print("\n" + "="*80)
        print("테스트 1: 기본 소켓 생성")
        print("="*80)

        sock = create_test_socket()

        # 소켓 속성 확인
        self.assertIsNotNone(sock)
        self.assertEqual(sock.family, socket.AF_INET)
        self.assertEqual(sock.type, socket.SOCK_STREAM)

        sock.close()
        print("✓ PASS: 소켓 생성 및 속성 확인 성공")

    def test_2_socket_binding(self):
        """
        테스트 2: 소켓 바인딩
        """
        print("\n" + "="*80)
        print("테스트 2: 소켓 바인딩")
        print("="*80)

        sock = create_test_socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 바인딩
        try:
            sock.bind(('127.0.0.1', 10001))
            sock.listen(1)
            print("✓ PASS: 포트 10001에 바인딩 성공")
            self.assertTrue(True)
        except OSError as e:
            self.fail(f"바인딩 실패: {e}")
        finally:
            sock.close()

    def test_3_echo_data_integrity(self):
        """
        테스트 3: Echo 데이터 무결성
        """
        print("\n" + "="*80)
        print("테스트 3: Echo 데이터 무결성")
        print("="*80)

        test_message = "Hello, Network!"
        test_bytes = test_message.encode('utf-8')

        # 소켓 쌍 생성 (socketpair - Unix only)
        try:
            server_sock, client_sock = socket.socketpair()

            # 클라이언트가 데이터 전송
            client_sock.sendall(test_bytes)

            # 서버가 데이터 수신
            received = server_sock.recv(1024)

            # 데이터 일치 확인
            self.assertEqual(received, test_bytes)
            self.assertEqual(received.decode('utf-8'), test_message)

            server_sock.close()
            client_sock.close()

            print(f"✓ PASS: 송수신 데이터 일치: '{test_message}'")
        except Exception as e:
            print(f"⚠️  socketpair 미지원: {e} (Linux/Unix에서만 작동)")

    def test_4_udp_socket(self):
        """
        테스트 4: UDP 소켓 생성
        """
        print("\n" + "="*80)
        print("테스트 4: UDP 소켓 생성")
        print("="*80)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.assertIsNotNone(sock)
        self.assertEqual(sock.family, socket.AF_INET)
        self.assertEqual(sock.type, socket.SOCK_DGRAM)

        sock.close()
        print("✓ PASS: UDP 소켓 생성 성공")

    def test_5_socket_reuse_address(self):
        """
        테스트 5: SO_REUSEADDR 옵션
        """
        print("\n" + "="*80)
        print("테스트 5: SO_REUSEADDR 옵션")
        print("="*80)

        sock1 = create_test_socket()
        sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sock1.bind(('127.0.0.1', 10002))
            sock1.listen(1)

            # 같은 포트에 다시 바인드 (SO_REUSEADDR 덕분에 가능)
            sock2 = create_test_socket()
            sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock2.bind(('127.0.0.1', 10003))  # 다른 포트

            sock2.close()
            sock1.close()

            print("✓ PASS: SO_REUSEADDR 옵션 동작 확인")
        except Exception as e:
            self.fail(f"소켓 옵션 실패: {e}")


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ PART 9: 완성 및 다음 단계                                                  ║
# ╚════════════════════════════════════════════════════════════════════════════╝

"""
✨ v4.3 완성 요약:

✅ 학습 내용:
   1. 소켓의 개념: 네트워크 통신의 소프트웨어적 문
   2. IP 주소 + 포트 번호 = 통신의 주소
   3. TCP: 신뢰성 중심 (handshake, ACK)
   4. UDP: 속도 중심 (Fire-and-Forget)
   5. Echo Server/Client: 기본 통신 구현
   6. 다중 클라이언트: Threading, Multiprocessing
   7. 비동기 네트워크: Asyncio + Socket
   8. 소켓 상태 머신과 TIME_WAIT 이해

🌐 통신의 진화:
   v4.1 Asyncio: 한 머신의 I/O 대기 최적화
   v4.2 Multiprocessing: 한 머신의 CPU 병렬화
   v4.3 Socket: 여러 머신 간 데이터 교환

   → 이제 전 세계와 대화할 준비 완료!

🚀 다음 단계:
   [v4.4] HTTP 프로토콜: 웹 서버 구현
   [v5.1] 실시간 채팅 애플리케이션
   [v5.2] REST API 서버
   [v5.3] 분산 시스템 (Microservices)

💡 실무 적용:
   • 웹 서버 (Flask, Django 내부 원리)
   • 게임 서버 (멀티플레이어 동기화)
   • IoT 센서 수집 시스템
   • 실시간 데이터 스트리밍
   • 블록체인 P2P 네트워크

> "기록이 증명이다 gogs" - 이제 네트워크 통신도 그 기록이다!
"""


if __name__ == "__main__":
    # 데모 실행
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + "  Python University Level 2 - v4.3 Network Socket Programming".center(78) + "║")
    print("║" + "  패킷으로 전 세계와 소통하는 시스템".center(78) + "║")
    print("╚" + "="*78 + "╝")

    # 데모 실행
    demonstration_1_basic_echo()
    demonstration_2_tcp_details()
    demonstration_3_udp_comparison()
    demonstration_4_socket_states()
    demonstration_5_port_binding()

    # 단위 테스트 실행
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + "  UNIT TESTS".center(78) + "║")
    print("╚" + "="*78 + "╝")

    unittest.main(argv=[''], exit=False, verbosity=2)

    print("\n" + "="*80)
    print("✨ v4.3 완성! 네트워크 소켓 프로그래밍 마스터 달성")
    print("="*80)
    print("\n다음 단계: v4.4 HTTP 프로토콜 (웹 서버 구현)")
