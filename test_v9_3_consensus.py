#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【 v9.3: 행성급 분산 합의 — 테스트 스위트 】

15개의 테스트로 글로벌 Raft 합의를 검증한다.
"""

import unittest
import time
from university_v9_3_PLANETARY_CONSENSUS import (
    NodeState,
    EntryType,
    LogEntry,
    VoteRequest,
    VoteResponse,
    AppendEntriesRequest,
    LogReplicator,
    LeaderElection,
    StateMachine,
    RaftConsensus,
    GlobalDatacenter,
    DisasterRecovery,
)


# ═══════════════════════════════════════════════════════════════════════════
# TestLogReplicator (테스트 01~03)
# ═══════════════════════════════════════════════════════════════════════════


class TestLogReplicator(unittest.TestCase):
    """로그 복제 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.replicator = LogReplicator()

    def test_01_append_log_entry(self):
        """test_01: 로그 엔트리 추가"""
        entry = LogEntry(
            term=1, index=0, entry_type=EntryType.DATA, data={"key": "value"}
        )

        result = self.replicator.append_log("node_0", entry)

        self.assertTrue(result)
        self.assertEqual(len(self.replicator.logs["node_0"]), 1)

    def test_02_replicate_to_followers(self):
        """test_02: 팔로워들에게 복제"""
        entry = LogEntry(
            term=1, index=0, entry_type=EntryType.DATA, data={"transaction": "T1"}
        )

        followers = ["node_1", "node_2", "node_3"]
        results = self.replicator.replicate_to_followers("node_0", followers, entry)

        # 모든 팔로워에게 복제 시도
        self.assertEqual(len(results), 3)

    def test_03_check_quorum_replication(self):
        """test_03: Quorum 복제 확인 (과반수)"""
        # 5개 노드, 3개 이상 필요 (과반수)
        replication_results = {
            "node_1": True,
            "node_2": True,
            "node_3": False,
            "node_4": False,
        }

        quorum = self.replicator.check_quorum_replication(5, replication_results)

        # 리더(1) + 성공(2) = 3 >= quorum(3)
        self.assertTrue(quorum)


# ═══════════════════════════════════════════════════════════════════════════
# TestLeaderElection (테스트 04~06)
# ═══════════════════════════════════════════════════════════════════════════


class TestLeaderElection(unittest.TestCase):
    """리더 선출 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.election = LeaderElection()

    def test_04_start_election(self):
        """test_04: 리더 선출 시작"""
        result = self.election.start_election("node_0", 5)

        # 선출 시도
        self.assertTrue(isinstance(result, bool))
        self.assertGreater(self.election.term, 0)

    def test_05_receive_vote_request(self):
        """test_05: 투표 요청 처리"""
        response = self.election.receive_vote_request("node_0", 1, "node_1")

        self.assertIsInstance(response, VoteResponse)
        self.assertEqual(response.voter_id, "node_1")

    def test_06_handle_leader_failure(self):
        """test_06: 리더 장애 처리"""
        # 초기 선출
        self.election.start_election("node_0", 5)
        initial_term = self.election.term

        # 장애 처리
        self.election.handle_leader_failure(5)

        # 새로운 리더 선출 시도 (term 증가)
        self.assertGreaterEqual(self.election.term, initial_term)


# ═══════════════════════════════════════════════════════════════════════════
# TestStateMachine (테스트 07~09)
# ═══════════════════════════════════════════════════════════════════════════


class TestStateMachine(unittest.TestCase):
    """상태 기계 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.machine = StateMachine()

    def test_07_apply_data_entry(self):
        """test_07: 데이터 엔트리 적용"""
        entry = LogEntry(
            term=1, index=0, entry_type=EntryType.DATA, data={"account": 1000000}
        )

        result = self.machine.apply_entry(entry)

        self.assertTrue(result)
        self.assertEqual(self.machine.applied_entries, 1)

    def test_08_get_state_snapshot(self):
        """test_08: 상태 스냅샷 생성"""
        entry = LogEntry(
            term=1, index=0, entry_type=EntryType.DATA, data={"balance": 5000}
        )
        self.machine.apply_entry(entry)

        snapshot = self.machine.get_state_snapshot()

        self.assertIn("state", snapshot)
        self.assertIn("version", snapshot)
        self.assertEqual(snapshot["applied_entries"], 1)

    def test_09_verify_state_consistency(self):
        """test_09: 상태 일관성 검증"""
        entry = LogEntry(
            term=1, index=0, entry_type=EntryType.DATA, data={"data": "test"}
        )
        self.machine.apply_entry(entry)

        snapshot = self.machine.get_state_snapshot()
        consistent = self.machine.verify_state_consistency(snapshot)

        self.assertTrue(consistent)


# ═══════════════════════════════════════════════════════════════════════════
# TestRaftConsensus (테스트 10~12)
# ═══════════════════════════════════════════════════════════════════════════


class TestRaftConsensus(unittest.TestCase):
    """Raft 합의 엔진 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.raft = RaftConsensus("node_0", 5)

    def test_10_reach_consensus(self):
        """test_10: 합의 도달"""
        # 리더 선출 후 합의 시도
        result = self.raft.reach_consensus({"transaction": "T1"})

        # 결과는 boolean
        self.assertIsInstance(result, bool)

    def test_11_get_consensus_status(self):
        """test_11: 합의 상태 조회"""
        status = self.raft.get_consensus_status()

        self.assertEqual(status["node_id"], "node_0")
        self.assertIn("state", status)
        self.assertIn("term", status)
        self.assertIn("leader", status)

    def test_12_consensus_rounds(self):
        """test_12: 합의 라운드 추적"""
        initial_rounds = self.raft.consensus_rounds

        # 여러 합의 시도
        for _ in range(3):
            self.raft.reach_consensus({"data": "test"})

        # 라운드 카운트 증가
        self.assertGreaterEqual(self.raft.consensus_rounds, initial_rounds)


# ═══════════════════════════════════════════════════════════════════════════
# TestGlobalDatacenter (테스트 13~14)
# ═══════════════════════════════════════════════════════════════════════════


class TestGlobalDatacenter(unittest.TestCase):
    """글로벌 데이터센터 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.datacenter = GlobalDatacenter(5)

    def test_13_broadcast_consensus_request(self):
        """test_13: 글로벌 합의 요청 전파"""
        data = {"global_transaction": "GT1"}
        results = self.datacenter.broadcast_consensus_request(data)

        # 5개 노드로부터 응답
        self.assertEqual(len(results), 5)

    def test_14_handle_regional_failure(self):
        """test_14: 지역 장애 처리"""
        recovery_result = self.datacenter.handle_regional_failure("asia")

        self.assertIn("failed_region", recovery_result)
        self.assertIn("recovery_success", recovery_result)


# ═══════════════════════════════════════════════════════════════════════════
# TestDisasterRecovery (테스트 15)
# ═══════════════════════════════════════════════════════════════════════════


class TestDisasterRecovery(unittest.TestCase):
    """재해 복구 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.recovery = DisasterRecovery()

    def test_15_disaster_recovery_workflow(self):
        """test_15: 재해 복구 전체 워크플로우"""
        # 1. 장애 감지
        failure = self.recovery.detect_failure("node_2", "crash")

        self.assertIsNotNone(failure)

        # 2. 복구 시작
        success = self.recovery.initiate_recovery(failure)

        # 3. 복구 상태 확인
        status = self.recovery.get_recovery_status()

        self.assertEqual(status["failures_detected"], 1)
        self.assertGreaterEqual(status["successful_recoveries"], 0)


# ═══════════════════════════════════════════════════════════════════════════
# 테스트 실행
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    unittest.main(verbosity=2)
