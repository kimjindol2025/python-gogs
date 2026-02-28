#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║        【 v9.3: 행성급 분산 합의 시스템(Planetary Consensus) 】             ║
║         포스트 닥터 연구 — 지구 규모 인프라 설계                            ║
║                                                                              ║
║              "빛의 속도와 타협하는 글로벌 합의 아키텍처"                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

【 핵심 개념 】

Raft 알고리즘 (Consensus Algorithm)
─────────────────────────────────────────────────────────
분산 시스템에서 모든 서버가 동일한 상태를 유지하도록 하는 알고리즘.

3가지 핵심 상태:
  1. Leader (리더): 클라이언트 요청 처리, 로그 복제 관리
  2. Follower (팔로워): 리더의 명령 따르기
  3. Candidate (후보자): 리더 선출 시 투표 신청

네트워크 지연과의 싸움
─────────────────────────────────────────────────────────
지구 반대편 통신: 100~300ms 지연
→ 이 지연을 견뎌내면서도 데이터 일관성 유지

Quorum (정족수) 원리
─────────────────────────────────────────────────────────
N개 노드 중 과반수(N/2 + 1)가 동의하면 전체의 결정으로 간주.
→ 일부 노드 장애에도 시스템 유지 가능

【 시스템 구성 】

1. LogReplicator          — 로그 복제 메커니즘
2. LeaderElection        — 리더 선출 프로토콜
3. StateM achine         — 상태 기계 (상태 전이)
4. RaftConsensus         — Raft 합의 엔진
5. GlobalDatacenter      — 지구 규모 시뮬레이션
6. DisasterRecovery      — 재해 복구 시스템

【 파이썬 철학 】

"지구를 하나의 컴퓨터처럼 다루되,
 물리적 한계(빛의 속도)를 인정하고 설계하는 것.
 이것이 포스트 닥터급 사고다."
"""

# ═══════════════════════════════════════════════════════════════════════════
# PART 0: 공용 데이터 클래스 & Enum
# ═══════════════════════════════════════════════════════════════════════════

import time
import random
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from collections import defaultdict


class NodeState(Enum):
    """노드 상태 (Raft)"""
    FOLLOWER = "FOLLOWER"
    CANDIDATE = "CANDIDATE"
    LEADER = "LEADER"


class EntryType(Enum):
    """로그 엔트리 타입"""
    DATA = "DATA"
    CONFIGURATION = "CONFIGURATION"
    SNAPSHOT = "SNAPSHOT"


@dataclass
class LogEntry:
    """Raft 로그 엔트리"""
    term: int
    index: int
    entry_type: EntryType
    data: Any
    timestamp: float = field(default_factory=time.time)


@dataclass
class VoteRequest:
    """리더 선출 투표 요청"""
    term: int
    candidate_id: str
    last_log_index: int
    last_log_term: int


@dataclass
class VoteResponse:
    """투표 응답"""
    term: int
    granted: bool
    voter_id: str


@dataclass
class AppendEntriesRequest:
    """로그 복제 요청"""
    term: int
    leader_id: str
    prev_log_index: int
    prev_log_term: int
    entries: List[LogEntry]
    leader_commit_index: int


@dataclass
class GlobalNodeMetrics:
    """글로벌 노드 메트릭"""
    node_id: str
    region: str
    state: NodeState
    log_size: int
    commitment_index: int
    network_latency_ms: float
    uptime_seconds: float


# ═══════════════════════════════════════════════════════════════════════════
# PART 1: LogReplicator — 로그 복제
# ═══════════════════════════════════════════════════════════════════════════

class LogReplicator:
    """로그 복제 메커니즘"""

    def __init__(self):
        self.logs: Dict[str, List[LogEntry]] = defaultdict(list)
        self.commitment_index: Dict[str, int] = defaultdict(lambda: 0)
        self.replication_count = 0

    def append_log(self, node_id: str, entry: LogEntry) -> bool:
        """로그에 엔트리 추가"""
        self.logs[node_id].append(entry)
        self.replication_count += 1
        return True

    def replicate_to_followers(
        self, leader_id: str, followers: List[str], entry: LogEntry
    ) -> Dict[str, bool]:
        """리더가 팔로워들에게 로그 복제"""
        replication_results = {}

        for follower_id in followers:
            # 네트워크 지연 시뮬레이션 (50~300ms)
            latency = random.uniform(50, 300) / 1000

            success = self.append_log(follower_id, entry)
            replication_results[follower_id] = success

        return replication_results

    def check_quorum_replication(
        self, num_nodes: int, replication_results: Dict[str, bool]
    ) -> bool:
        """과반수 복제 확인 (Quorum)"""
        success_count = sum(1 for v in replication_results.values() if v) + 1  # 리더 포함

        quorum_size = (num_nodes // 2) + 1

        return success_count >= quorum_size

    def commit_entries(self, node_id: str, commit_index: int) -> int:
        """커밋할 엔트리 적용"""
        old_commit_index = self.commitment_index[node_id]
        self.commitment_index[node_id] = max(old_commit_index, commit_index)

        return self.commitment_index[node_id]

    def get_log_status(self, node_id: str) -> Dict[str, Any]:
        """로그 상태"""
        return {
            "node_id": node_id,
            "log_size": len(self.logs[node_id]),
            "committed_entries": self.commitment_index[node_id],
            "total_replications": self.replication_count,
        }


# ═══════════════════════════════════════════════════════════════════════════
# PART 2: LeaderElection — 리더 선출
# ═══════════════════════════════════════════════════════════════════════════

class LeaderElection:
    """Raft 리더 선출 프로토콜"""

    def __init__(self):
        self.term = 0
        self.voted_for: Dict[int, Optional[str]] = defaultdict(lambda: None)
        self.election_count = 0
        self.leader_changes = 0
        self.current_leader: Optional[str] = None

    def start_election(self, candidate_id: str, num_nodes: int) -> bool:
        """리더 선출 시작"""
        self.term += 1
        self.election_count += 1

        # 자신에게 투표
        votes_received = 1
        quorum_size = (num_nodes // 2) + 1

        # 다른 노드들로부터 투표 수집 (시뮬레이션)
        for _ in range(num_nodes - 1):
            # 투표 성공률: 80%
            if random.random() < 0.8:
                votes_received += 1

        # 과반수 투표 확인
        if votes_received >= quorum_size:
            self.current_leader = candidate_id
            self.leader_changes += 1
            return True

        return False

    def receive_vote_request(
        self, candidate_id: str, term: int, voter_id: str
    ) -> VoteResponse:
        """투표 요청 처리"""
        # 더 큰 term이 나타나면 자신의 term 업데이트
        if term > self.term:
            self.term = term
            self.voted_for[term] = None

        # 이미 투표했으면 거절
        if self.voted_for[term] is not None:
            return VoteResponse(term=self.term, granted=False, voter_id=voter_id)

        # 투표 실시
        self.voted_for[term] = candidate_id
        return VoteResponse(term=self.term, granted=True, voter_id=voter_id)

    def handle_leader_failure(self, num_nodes: int) -> bool:
        """리더 장애 복구 (새 선출 시작)"""
        # 새로운 리더 선출 시작 (Timeout trigger)
        backup_candidate = f"backup_leader_{random.randint(1, num_nodes)}"
        return self.start_election(backup_candidate, num_nodes)

    def get_election_status(self) -> Dict[str, Any]:
        """선출 상태"""
        return {
            "current_term": self.term,
            "current_leader": self.current_leader,
            "elections_held": self.election_count,
            "leader_changes": self.leader_changes,
        }


# ═══════════════════════════════════════════════════════════════════════════
# PART 3: StateMachine — 상태 기계
# ═══════════════════════════════════════════════════════════════════════════

class StateMachine:
    """분산 상태 기계"""

    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.applied_entries = 0
        self.state_version = 0

    def apply_entry(self, entry: LogEntry) -> bool:
        """로그 엔트리를 상태에 적용"""
        if entry.entry_type == EntryType.DATA:
            # 데이터 업데이트
            if isinstance(entry.data, dict):
                self.state.update(entry.data)
            else:
                self.state[f"entry_{entry.index}"] = entry.data

            self.applied_entries += 1
            self.state_version += 1
            return True

        elif entry.entry_type == EntryType.CONFIGURATION:
            # 구성 변경 (노드 추가/제거)
            self.state["configuration"] = entry.data
            return True

        elif entry.entry_type == EntryType.SNAPSHOT:
            # 스냅샷 (전체 상태 복구)
            self.state = entry.data.copy()
            self.state_version = entry.term
            return True

        return False

    def get_state_snapshot(self) -> Dict[str, Any]:
        """현재 상태 스냅샷"""
        return {
            "state": self.state.copy(),
            "version": self.state_version,
            "applied_entries": self.applied_entries,
        }

    def verify_state_consistency(self, other_state: Dict[str, Any]) -> bool:
        """다른 노드의 상태와 일관성 확인"""
        return self.state_version == other_state.get("version", -1)


# ═══════════════════════════════════════════════════════════════════════════
# PART 4: RaftConsensus — Raft 합의 엔진
# ═══════════════════════════════════════════════════════════════════════════

class RaftConsensus:
    """Raft 합의 엔진"""

    def __init__(self, node_id: str, num_nodes: int):
        self.node_id = node_id
        self.num_nodes = num_nodes
        self.state = NodeState.FOLLOWER
        self.log_replicator = LogReplicator()
        self.election = LeaderElection()
        self.state_machine = StateMachine()
        self.consensus_rounds = 0

    def handle_client_request(self, data: Any) -> bool:
        """클라이언트 요청 처리"""
        if self.state != NodeState.LEADER:
            return False

        # 로그에 엔트리 추가
        entry = LogEntry(
            term=self.election.term,
            index=len(self.log_replicator.logs[self.node_id]),
            entry_type=EntryType.DATA,
            data=data,
        )

        self.log_replicator.append_log(self.node_id, entry)

        # 팔로워들에게 복제
        follower_ids = [f"node_{i}" for i in range(self.num_nodes) if f"node_{i}" != self.node_id]
        replication_results = self.log_replicator.replicate_to_followers(
            self.node_id, follower_ids, entry
        )

        # 과반수 복제 확인
        if self.log_replicator.check_quorum_replication(self.num_nodes, replication_results):
            # 커밋
            self.log_replicator.commit_entries(
                self.node_id, len(self.log_replicator.logs[self.node_id])
            )
            self.state_machine.apply_entry(entry)
            self.consensus_rounds += 1
            return True

        return False

    def reach_consensus(self, data: Any) -> bool:
        """합의 도달"""
        # 리더 선출 (아직 리더가 없으면)
        if self.election.current_leader is None:
            if self.election.start_election(self.node_id, self.num_nodes):
                self.state = NodeState.LEADER

        # 리더가 되었으면 클라이언트 요청 처리
        if self.state == NodeState.LEADER:
            return self.handle_client_request(data)

        return False

    def get_consensus_status(self) -> Dict[str, Any]:
        """합의 상태"""
        return {
            "node_id": self.node_id,
            "state": self.state.value,
            "term": self.election.term,
            "leader": self.election.current_leader,
            "consensus_rounds": self.consensus_rounds,
            "logs": self.log_replicator.get_log_status(self.node_id),
            "state_machine": self.state_machine.get_state_snapshot(),
        }


# ═══════════════════════════════════════════════════════════════════════════
# PART 5: GlobalDatacenter — 지구 규모 시뮬레이션
# ═══════════════════════════════════════════════════════════════════════════

class GlobalDatacenter:
    """지구 규모 분산 데이터센터"""

    def __init__(self, num_nodes: int = 5):
        self.num_nodes = num_nodes
        self.nodes: Dict[str, RaftConsensus] = {}
        self.regions = ["north_america", "europe", "asia", "south_america", "africa"]
        self.network_latencies: Dict[Tuple[str, str], float] = {}
        self.global_consensus_achieved = 0

        # 노드 초기화
        for i in range(num_nodes):
            node_id = f"node_{i}"
            region = self.regions[i % len(self.regions)]
            node = RaftConsensus(node_id, num_nodes)
            self.nodes[node_id] = node

    def simulate_network_latency(self, from_node: str, to_node: str) -> float:
        """네트워크 지연 시뮬레이션 (지구 둘레 기반)"""
        key = (from_node, to_node)

        if key not in self.network_latencies:
            # 지구 반대편까지의 지연: 100~300ms
            self.network_latencies[key] = random.uniform(50, 300)

        return self.network_latencies[key]

    def broadcast_consensus_request(self, data: Any) -> Dict[str, bool]:
        """글로벌 합의 요청 전파"""
        results = {}

        for node_id, node in self.nodes.items():
            # 네트워크 지연
            latency = self.simulate_network_latency("client", node_id)

            # 합의 도달 시도
            success = node.reach_consensus(data)
            results[node_id] = success

        # 과반수 성공 확인
        success_count = sum(1 for v in results.values() if v)
        quorum_size = (self.num_nodes // 2) + 1

        if success_count >= quorum_size:
            self.global_consensus_achieved += 1

        return results

    def handle_regional_failure(self, region: str) -> Dict[str, Any]:
        """지역 장애 처리"""
        # 해당 지역의 모든 노드 실패
        failed_nodes = [
            nid for nid, node in self.nodes.items() if node.election.current_leader != nid
        ]

        # 새로운 리더 선출
        remaining_nodes = [n for n in self.nodes.keys() if n not in failed_nodes]

        recovery_success = False
        if remaining_nodes:
            for node_id in remaining_nodes:
                if self.nodes[node_id].election.handle_leader_failure(self.num_nodes):
                    recovery_success = True
                    break

        return {
            "failed_region": region,
            "failed_nodes_count": len(failed_nodes),
            "recovery_success": recovery_success,
            "recovery_time_ms": random.uniform(100, 500),
        }

    def get_global_status(self) -> Dict[str, Any]:
        """글로벌 상태"""
        metrics = []
        for node_id, node in self.nodes.items():
            metrics.append(
                {
                    "node_id": node_id,
                    "state": node.state.value,
                    "consensus_rounds": node.consensus_rounds,
                }
            )

        return {
            "num_nodes": self.num_nodes,
            "global_consensus_achieved": self.global_consensus_achieved,
            "node_metrics": metrics,
            "network_latencies": {str(k): v for k, v in self.network_latencies.items()},
        }


# ═══════════════════════════════════════════════════════════════════════════
# PART 6: DisasterRecovery — 재해 복구
# ═══════════════════════════════════════════════════════════════════════════

class DisasterRecovery:
    """재해 복구 시스템"""

    def __init__(self):
        self.failure_history: List[Dict[str, Any]] = []
        self.recovery_time_total = 0.0
        self.recovery_success_count = 0

    def detect_failure(self, node_id: str, failure_type: str) -> Dict[str, Any]:
        """장애 감지"""
        start_time = time.time()

        failure_record = {
            "node_id": node_id,
            "failure_type": failure_type,  # "crash", "network_partition", "data_corruption"
            "detected_at": start_time,
            "status": "DETECTED",
        }

        self.failure_history.append(failure_record)
        return failure_record

    def initiate_recovery(self, failure_record: Dict[str, Any]) -> bool:
        """복구 시작"""
        start_time = time.time()

        # 재해 유형에 따른 복구
        if failure_record["failure_type"] == "crash":
            # 1. 로그 복제본에서 복구
            # 2. 상태 스냅샷 적용
            recovery_time = random.uniform(50, 200)
            success = True

        elif failure_record["failure_type"] == "network_partition":
            # 1. 다른 파티션의 데이터 동기화
            # 2. 쓰기 작업 재수행
            recovery_time = random.uniform(100, 300)
            success = True

        else:
            # 데이터 손상: 스냅샷 복구
            recovery_time = random.uniform(200, 500)
            success = random.random() < 0.95  # 95% 성공률

        actual_recovery_time = (time.time() - start_time) * 1000 + recovery_time

        if success:
            self.recovery_success_count += 1
            self.recovery_time_total += actual_recovery_time

        return success

    def verify_recovery(self, node_id: str, expected_state: Dict[str, Any]) -> bool:
        """복구 검증"""
        # 복구된 노드의 상태와 기대값 비교
        # (실제로는 node_id의 상태를 검증)
        return True  # 시뮬레이션에서는 항상 성공

    def get_recovery_status(self) -> Dict[str, Any]:
        """복구 상태"""
        avg_recovery_time = (
            self.recovery_time_total / self.recovery_success_count
            if self.recovery_success_count > 0
            else 0
        )

        return {
            "failures_detected": len(self.failure_history),
            "successful_recoveries": self.recovery_success_count,
            "average_recovery_time_ms": avg_recovery_time,
            "total_recovery_time_ms": self.recovery_time_total,
        }


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1~6: 글로벌 시뮬레이션
# ═══════════════════════════════════════════════════════════════════════════


def main():
    """메인 프로그램 — 행성급 분산 합의 시뮬레이션"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║   【 v9.3: 행성급 분산 합의 시스템 】                      ║")
    print("║   포스트 닥터 연구 — 글로벌 인프라 설계                    ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    # SECTION 1: 글로벌 데이터센터 초기화
    print("[SECTION 1] 글로벌 데이터센터 초기화 (5대륙, 5개 노드)")
    datacenter = GlobalDatacenter(5)
    print(f"✓ 5개 지역에 5개 노드 배포")
    print(f"✓ 네트워크 지연: 50~300ms\n")

    # SECTION 2: 리더 선출
    print("[SECTION 2] 리더 선출 (Raft Election)")
    election = LeaderElection()
    leader_selected = election.start_election("node_0", 5)
    print(f"✓ 리더 선출: {leader_selected}")
    print(f"✓ 현재 리더: {election.current_leader}")
    print(f"✓ 현재 Term: {election.term}\n")

    # SECTION 3: 글로벌 합의 도달
    print("[SECTION 3] 글로벌 합의 도달 (3개 트랜잭션)")
    for i in range(3):
        data = {"transaction_id": f"GLOBAL-{i}", "amount": 1000000 * (i + 1)}
        results = datacenter.broadcast_consensus_request(data)
        success_count = sum(1 for v in results.values() if v)
        print(f"  트랜잭션 {i+1}: {success_count}/5 노드 합의 완료")

    print(f"✓ 총 글로벌 합의: {datacenter.global_consensus_achieved}회\n")

    # SECTION 4: 네트워크 지연 분석
    print("[SECTION 4] 네트워크 지연 분석")
    latencies = []
    for (from_n, to_n), latency in datacenter.network_latencies.items():
        latencies.append(latency)

    if latencies:
        print(f"✓ 평균 지연: {sum(latencies) / len(latencies):.1f}ms")
        print(f"✓ 최소 지연: {min(latencies):.1f}ms")
        print(f"✓ 최대 지연: {max(latencies):.1f}ms\n")

    # SECTION 5: 지역 장애 복구
    print("[SECTION 5] 지역 장애 처리 (Asia 지역 실패)")
    recovery = DisasterRecovery()
    failure = recovery.detect_failure("node_2", "crash")
    recovery_success = recovery.initiate_recovery(failure)
    recovery_status = recovery.get_recovery_status()

    print(f"✓ 장애 감지: {failure['failure_type']}")
    print(f"✓ 복구 성공: {recovery_success}")
    print(f"✓ 복구 시간: {recovery_status['average_recovery_time_ms']:.1f}ms\n")

    # SECTION 6: 글로벌 상태 확인
    print("[SECTION 6] 글로벌 시스템 상태")
    global_status = datacenter.get_global_status()
    print(f"✓ 총 노드: {global_status['num_nodes']}")
    print(f"✓ 달성한 글로벌 합의: {global_status['global_consensus_achieved']}")

    for metric in global_status["node_metrics"]:
        print(
            f"  {metric['node_id']}: {metric['state']} "
            f"(합의 라운드: {metric['consensus_rounds']})"
        )

    print("\n[SECTION 7] 포스트 닥터 연구 철학")
    print(
        """
    지구는 더 이상 물리적 거리로 나뉘지 않는다.

    네트워크 지연은 피할 수 없지만, Quorum 기반 합의로 극복한다.
    1개 대륙이 죽어도 4개 대륙이 살아있으면 서비스는 계속된다.

    이것이 진정한 글로벌 인프라다:
    - Raft 알고리즘: 분산 합의의 정수
    - 로그 복제: 장애 복구의 근간
    - 상태 기계: 모든 노드의 일관성 보장
    - 재해 복구: 0초 다운타임의 목표

    v9.3은 우리가 지구 규모의 시스템을 설계할 수 있음을 증명한다.
    """
    )

    print("\n저장 필수 너는 기록이 증명이다 gogs 🌍\n")


if __name__ == "__main__":
    main()
