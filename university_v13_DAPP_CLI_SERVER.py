#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║       【 v13: 셀프 호스팅 분산 AI 플랫폼 (CLI + 웹 서버) 】              ║
║                                                                              ║
║  표준 라이브러리만 사용 (http.server, json, sqlite3 불필요)               ║
║  CLI 모드 + HTTP 웹 서버 동시 지원                                         ║
║  데이터 영속성 (JSON 파일 기반)                                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import json
import hashlib
import random
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from io import StringIO
import sys


# ═══════════════════════════════════════════════════════════════════════════════
# v12 플랫폼 데이터 구조 (단순화)
# ═══════════════════════════════════════════════════════════════════════════════

class SimplifiedPlatform:
    """단순화된 플랫폼 (v12에서 이식)"""

    def __init__(self):
        self._data_providers = {}
        self._trainers = {}
        self._validators = {}
        self._rounds_history = []
        self._wallets = {}
        self._current_round = 0
        self.load_data()

    def load_data(self):
        """디스크에서 데이터 로드"""
        try:
            with open("platform_data.json", "r") as f:
                data = json.load(f)
                self._data_providers = data.get("providers", {})
                self._trainers = data.get("trainers", {})
                self._validators = data.get("validators", {})
                self._rounds_history = data.get("rounds", [])
                self._wallets = data.get("wallets", {})
                self._current_round = data.get("current_round", 0)
        except FileNotFoundError:
            pass

    def save_data(self):
        """디스크에 데이터 저장"""
        data = {
            "providers": self._data_providers,
            "trainers": self._trainers,
            "validators": self._validators,
            "rounds": self._rounds_history,
            "wallets": self._wallets,
            "current_round": self._current_round
        }
        with open("platform_data.json", "w") as f:
            json.dump(data, f, indent=2)

    def register_data_provider(self, provider_id):
        """데이터 제공자 등록"""
        if provider_id in self._data_providers:
            return False, "이미 존재"
        self._data_providers[provider_id] = {
            "quality": 0.8,
            "datasets": 0,
            "reward": 0.0
        }
        self._wallets[provider_id] = 300.0
        self.save_data()
        return True, f"✓ {provider_id} 등록됨"

    def register_trainer(self, trainer_id):
        """학습자 등록"""
        if trainer_id in self._trainers:
            return False, "이미 존재"
        self._trainers[trainer_id] = {
            "accuracy": 0.0,
            "rounds_trained": 0,
            "reward": 0.0
        }
        self._wallets[trainer_id] = 500.0
        self.save_data()
        return True, f"✓ {trainer_id} 등록됨"

    def register_validator(self, validator_id, stake):
        """검증자 등록 (DPoS)"""
        if validator_id in self._validators:
            return False, "이미 존재"
        self._validators[validator_id] = {
            "stake": float(stake),
            "validations": 0,
            "reward": 0.0
        }
        self._wallets[validator_id] = float(stake)
        self.save_data()
        return True, f"✓ {validator_id} 등록됨 (스테이크: {stake} GOG)"

    def start_round(self, model_id):
        """라운드 시작"""
        if not self._trainers:
            return False, "등록된 학습자 없음"

        round_data = {
            "round": self._current_round + 1,
            "model_id": model_id,
            "timestamp": time.time(),
            "trainers_trained": len(self._trainers),
            "validators_participated": min(len(self._validators), 5),
            "accuracy": 0.5 + self._current_round * 0.08,
            "rewards": {}
        }

        # 보상 배분
        trainer_pool = 500  # 50% of 1000
        validator_pool = 350  # 35% of 1000
        provider_pool = 150  # 15% of 1000

        for trainer_id in self._trainers:
            reward = trainer_pool / len(self._trainers)
            self._wallets[trainer_id] = self._wallets.get(trainer_id, 0) + reward
            round_data["rewards"][trainer_id] = reward

        for validator_id in list(self._validators.keys())[:5]:
            reward = validator_pool / min(len(self._validators), 5)
            self._wallets[validator_id] = self._wallets.get(validator_id, 0) + reward
            round_data["rewards"][validator_id] = reward

        self._rounds_history.append(round_data)
        self._current_round += 1
        self.save_data()

        return True, f"✓ 라운드 {round_data['round']} 완료 (정확도: {round_data['accuracy']:.1%})"

    def get_wallet(self, address):
        """지갑 조회"""
        balance = self._wallets.get(address, 0.0)
        return balance

    def get_leaderboard(self):
        """리더보드"""
        board = {
            "trainers": sorted(
                [(k, self._wallets.get(k, 0)) for k in self._trainers],
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "validators": sorted(
                [(k, self._wallets.get(k, 0)) for k in self._validators],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }
        return board

    def get_stats(self):
        """통계"""
        total_distributed = sum(
            sum(r.get("rewards", {}).values())
            for r in self._rounds_history
        )
        return {
            "rounds_completed": len(self._rounds_history),
            "participants": len(self._trainers) + len(self._validators) + len(self._data_providers),
            "total_distributed": total_distributed,
            "total_wallets": sum(self._wallets.values())
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CLI 인터페이스
# ═══════════════════════════════════════════════════════════════════════════════

class DAppCLI:
    """CLI 인터페이스"""

    def __init__(self, platform):
        self.platform = platform
        self.running = True

    def show_banner(self):
        """배너"""
        print("\n" + "═" * 70)
        print("【 v13: 분산 AI 플랫폼 DApp (CLI) 】")
        print("═" * 70)
        print("명령어: help / register / start_round / leaderboard / stats / wallet / exit\n")

    def show_help(self):
        """도움말"""
        print("""
【 명령어 목록 】
  register data_provider <id>        데이터 제공자 등록
  register trainer <id>              학습자 등록
  register validator <id> <stake>    검증자 등록 (DPoS)
  start_round <model_id>             라운드 시작
  leaderboard                         리더보드 조회
  stats                              플랫폼 통계
  wallet <address>                   지갑 잔액 조회
  help                               도움말
  exit                               종료
""")

    def process_command(self, cmd):
        """명령어 처리"""
        parts = cmd.strip().split()
        if not parts:
            return

        command = parts[0]

        if command == "help":
            self.show_help()
        elif command == "exit":
            self.running = False
            print("✓ 종료합니다.")
        elif command == "register" and len(parts) >= 2:
            role = parts[1]
            if role == "data_provider" and len(parts) >= 3:
                success, msg = self.platform.register_data_provider(parts[2])
                print(msg)
            elif role == "trainer" and len(parts) >= 3:
                success, msg = self.platform.register_trainer(parts[2])
                print(msg)
            elif role == "validator" and len(parts) >= 4:
                success, msg = self.platform.register_validator(parts[2], parts[3])
                print(msg)
        elif command == "start_round" and len(parts) >= 2:
            success, msg = self.platform.start_round(parts[1])
            print(msg)
        elif command == "leaderboard":
            board = self.platform.get_leaderboard()
            print("\n【 Top 5 Trainers 】")
            for i, (name, balance) in enumerate(board["trainers"], 1):
                print(f"  {i}. {name}: {balance:.0f} GOG")
            print("\n【 Top 5 Validators 】")
            for i, (name, balance) in enumerate(board["validators"], 1):
                print(f"  {i}. {name}: {balance:.0f} GOG")
        elif command == "stats":
            stats = self.platform.get_stats()
            print(f"\n【 플랫폼 통계 】")
            print(f"  라운드: {stats['rounds_completed']}")
            print(f"  참여자: {stats['participants']}명")
            print(f"  총 배분: {stats['total_distributed']:.0f} GOG")
            print(f"  총 잔액: {stats['total_wallets']:.0f} GOG")
        elif command == "wallet" and len(parts) >= 2:
            balance = self.platform.get_wallet(parts[1])
            print(f"✓ {parts[1]} 잔액: {balance:.0f} GOG")
        else:
            print("? 알 수 없는 명령어. help 입력")

    def run(self):
        """CLI 실행"""
        self.show_banner()
        while self.running:
            try:
                cmd = input("> ").strip()
                if cmd:
                    self.process_command(cmd)
            except KeyboardInterrupt:
                print("\n✓ 종료합니다.")
                self.running = False
            except Exception as e:
                print(f"✗ 오류: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# HTTP 웹 서버
# ═══════════════════════════════════════════════════════════════════════════════

class DAppHTTPHandler(BaseHTTPRequestHandler):
    """HTTP 요청 핸들러"""

    platform = None

    def do_GET(self):
        """GET 요청 처리"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == "/":
            self.serve_homepage()
        elif path == "/api/stats":
            self.serve_json(self.platform.get_stats())
        elif path == "/api/leaderboard":
            self.serve_json(self.platform.get_leaderboard())
        elif path == "/api/wallet":
            address = query.get("address", ["unknown"])[0]
            balance = self.platform.get_wallet(address)
            self.serve_json({"address": address, "balance": balance})
        else:
            self.send_error(404)

    def do_POST(self):
        """POST 요청 처리"""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()
        data = json.loads(body) if body else {}

        path = urlparse(self.path).path

        if path == "/api/register":
            role = data.get("role")
            if role == "trainer":
                success, msg = self.platform.register_trainer(data.get("id"))
                self.serve_json({"success": success, "message": msg})
            elif role == "validator":
                success, msg = self.platform.register_validator(
                    data.get("id"), data.get("stake", 1000)
                )
                self.serve_json({"success": success, "message": msg})
            else:
                self.serve_json({"success": False, "message": "알 수 없는 역할"})
        elif path == "/api/start_round":
            success, msg = self.platform.start_round(data.get("model_id", "model_001"))
            self.serve_json({"success": success, "message": msg})
        else:
            self.send_error(404)

    def serve_homepage(self):
        """홈페이지"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>v13 분산 AI 플랫폼</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1000px; margin: 0 auto; }
        .section { margin: 20px 0; padding: 10px; border: 1px solid #ddd; }
        button { padding: 10px 20px; margin: 5px; cursor: pointer; }
        #output { background: #f0f0f0; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 v13: 분산 AI 플랫폼 DApp</h1>

        <div class="section">
            <h2>참여자 등록</h2>
            <input type="text" id="trainer_id" placeholder="Trainer ID" />
            <button onclick="registerTrainer()">학습자 등록</button>
            <button onclick="registerValidator()">검증자 등록 (1000 GOG)</button>
        </div>

        <div class="section">
            <h2>라운드 관리</h2>
            <button onclick="startRound()">라운드 시작</button>
            <button onclick="loadStats()">통계</button>
        </div>

        <div class="section">
            <h2>리더보드</h2>
            <button onclick="loadLeaderboard()">리더보드 조회</button>
        </div>

        <div id="output"></div>
    </div>

    <script>
        const API = "/api";

        async function registerTrainer() {
            const id = document.getElementById("trainer_id").value || "trainer_" + Date.now();
            const res = await fetch(API + "/register", {
                method: "POST",
                body: JSON.stringify({role: "trainer", id: id})
            });
            const data = await res.json();
            show(data.message);
        }

        async function registerValidator() {
            const id = document.getElementById("trainer_id").value || "validator_" + Date.now();
            const res = await fetch(API + "/register", {
                method: "POST",
                body: JSON.stringify({role: "validator", id: id, stake: 1000})
            });
            const data = await res.json();
            show(data.message);
        }

        async function startRound() {
            const res = await fetch(API + "/start_round", {
                method: "POST",
                body: JSON.stringify({model_id: "model_001"})
            });
            const data = await res.json();
            show(data.message);
        }

        async function loadStats() {
            const res = await fetch(API + "/stats");
            const data = await res.json();
            show("<h3>📊 통계</h3>" +
                "<p>라운드: " + data.rounds_completed + "</p>" +
                "<p>참여자: " + data.participants + "명</p>" +
                "<p>총 배분: " + data.total_distributed.toFixed(0) + " GOG</p>");
        }

        async function loadLeaderboard() {
            const res = await fetch(API + "/leaderboard");
            const data = await res.json();
            let html = "<h3>🏆 리더보드</h3>";
            html += "<h4>학습자</h4>";
            data.trainers.forEach((item, i) => {
                html += "<p>" + (i+1) + ". " + item[0] + ": " + item[1].toFixed(0) + " GOG</p>";
            });
            html += "<h4>검증자</h4>";
            data.validators.forEach((item, i) => {
                html += "<p>" + (i+1) + ". " + item[0] + ": " + item[1].toFixed(0) + " GOG</p>";
            });
            show(html);
        }

        function show(msg) {
            document.getElementById("output").innerHTML = msg;
        }
    </script>
</body>
</html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def serve_json(self, data):
        """JSON 응답"""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        """로그 억제"""
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# 메인 실행
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║       【 v13: 셀프 호스팅 분산 AI 플랫폼 】                  ║")
    print("║       CLI 모드 또는 웹 서버 (http://localhost:8888)        ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")

    platform = SimplifiedPlatform()

    print("선택: 1) CLI 모드  2) 웹 서버  3) 두 가지 모두")
    choice = input("입력 (1/2/3) [기본: 1]: ").strip() or "1"

    if choice in ["1", "3"]:
        cli = DAppCLI(platform)
        if choice == "1":
            cli.run()
        else:
            # 스레드에서 CLI 실행
            cli_thread = threading.Thread(target=cli.run, daemon=True)
            cli_thread.start()
            time.sleep(1)

    if choice in ["2", "3"]:
        DAppHTTPHandler.platform = platform
        server = HTTPServer(("0.0.0.0", 8888), DAppHTTPHandler)
        print("🌐 웹 서버 시작: http://localhost:8888")
        print("(CLI 모드에서 exit 입력하면 서버도 종료됩니다.)\n")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n✓ 서버 종료")


if __name__ == "__main__":
    main()
