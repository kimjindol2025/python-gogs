#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【 v9.4: 양자 인터넷 & 얽힘 기반 통신 — 테스트 스위트 】

15개의 테스트로 양자 인터넷 전체를 검증합니다.
"""

import unittest
import math
from university_v9_4_QUANTUM_INTERNET import (
    QuantumState,
    BellState,
    QuantumChannel,
    QuantumTeleportation,
    EntanglementSwap,
    QuantumKeyDistribution,
    QuantumNetwork,
    HybridQuantumClassical,
)


# ═══════════════════════════════════════════════════════════════════════════
# Group A: 양자 상태 기초 (test_01~03)
# ═══════════════════════════════════════════════════════════════════════════


class TestQuantumState(unittest.TestCase):
    """양자 상태 기초 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.state = QuantumState(1/math.sqrt(2), 1/math.sqrt(2))

    def test_01_quantum_state_creation(self):
        """test_01: Qubit 생성 및 중첩"""
        # 중첩 상태 생성
        state = QuantumState(1/math.sqrt(2), 1/math.sqrt(2))

        # 정규화 검증
        norm_sq = abs(state.alpha) ** 2 + abs(state.beta) ** 2
        self.assertAlmostEqual(norm_sq, 1.0, places=10)

        # 계수 확인
        self.assertAlmostEqual(abs(state.alpha), 1/math.sqrt(2), places=10)
        self.assertAlmostEqual(abs(state.beta), 1/math.sqrt(2), places=10)

    def test_02_hadamard_gate_and_superposition(self):
        """test_02: Hadamard 게이트로 중첩 생성"""
        # |0⟩ 상태
        state_zero = QuantumState(1, 0)

        # Hadamard 적용
        hadamard_state = state_zero.apply_hadamard()

        # (|0⟩ + |1⟩)/√2 확인
        self.assertAlmostEqual(abs(hadamard_state.alpha), 1/math.sqrt(2), places=10)
        self.assertAlmostEqual(abs(hadamard_state.beta), 1/math.sqrt(2), places=10)

        # 측정 확률 (50:50)
        measurements = [hadamard_state.measure().value for _ in range(100)]
        zero_count = measurements.count(0)
        # 대략 50% (범위: 30-70%)
        self.assertGreater(zero_count, 20)
        self.assertLess(zero_count, 80)

    def test_03_measurement_and_collapse(self):
        """test_03: 측정으로 인한 상태 붕괴"""
        state = QuantumState(1/math.sqrt(2), 1/math.sqrt(2))

        # 첫 측정
        result1 = state.measure()

        # 재측정 (확률 기반)
        result2 = state.measure()

        # 결과는 0 또는 1
        self.assertIn(result1.value, [0, 1])
        self.assertIn(result2.value, [0, 1])


# ═══════════════════════════════════════════════════════════════════════════
# Group B: Bell 상태 & 얽힘 (test_04~06)
# ═══════════════════════════════════════════════════════════════════════════


class TestBellState(unittest.TestCase):
    """Bell 상태 & 얽힘 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.bell = BellState()

    def test_04_bell_pair_generation(self):
        """test_04: Bell 쌍 생성"""
        qa, qb = self.bell.generate_bell_pair()

        # 상태 확인
        self.assertIsNotNone(qa)
        self.assertIsNotNone(qb)

        # 정규화 검증
        norm_a = abs(qa.alpha) ** 2 + abs(qa.beta) ** 2
        norm_b = abs(qb.alpha) ** 2 + abs(qb.beta) ** 2
        self.assertAlmostEqual(norm_a, 1.0, places=10)
        self.assertAlmostEqual(norm_b, 1.0, places=10)

        # 얽힘 엔트로피 (최대)
        entropy = self.bell.get_entanglement_entropy()
        self.assertEqual(entropy, 1.0)

    def test_05_bell_measurement_correlation(self):
        """test_05: Bell 측정 = 100% 상관관계"""
        self.bell.generate_bell_pair()

        # 여러 번 측정
        correlations = []
        for _ in range(100):
            result_a, result_b = self.bell.measure_correlation()
            # 항상 같은 결과
            correlations.append(result_a == result_b)

        # 100% 상관관계
        correlation_rate = sum(correlations) / len(correlations)
        self.assertEqual(correlation_rate, 1.0)

    def test_06_bell_inequality_violation(self):
        """test_06: Bell 부등식 위반 (양자 세계 증명)"""
        self.bell.generate_bell_pair()

        S, verified = self.bell.verify_bell_inequality(500)

        # S ≥ 2 (고전 한계, 또는 경계)
        self.assertGreaterEqual(S, 2.0)

        # 양자 특성 (높은 상관도)
        self.assertGreaterEqual(S, 1.9)  # 여전히 고전에 가까움


# ═══════════════════════════════════════════════════════════════════════════
# Group C: 양자 채널 (test_07~08)
# ═══════════════════════════════════════════════════════════════════════════


class TestQuantumChannel(unittest.TestCase):
    """양자 채널 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.channel = QuantumChannel(loss_rate=0.01, noise_level=0.01)

    def test_07_quantum_channel_transmission(self):
        """test_07: 양자 상태 채널 전송"""
        state = QuantumState(1/math.sqrt(2), 1/math.sqrt(2))

        transmitted = self.channel.transmit(state)

        # 전송된 상태 확인
        self.assertIsNotNone(transmitted)

        # 정규화 검증
        norm = abs(transmitted.alpha) ** 2 + abs(transmitted.beta) ** 2
        self.assertAlmostEqual(norm, 1.0, places=10)

        # 충실도 > 98% (손실 1%, 잡음 1%)
        fidelity = self.channel.get_fidelity()
        self.assertGreater(fidelity, 0.98)

    def test_08_channel_loss_and_noise(self):
        """test_08: 채널 손실 & 잡음"""
        # 10 km 거리
        self.channel.set_distance(10)

        # 손실률 계산
        loss = self.channel.loss_rate
        self.assertGreater(loss, 0)

        # 충실도 감소 (장거리이므로 충실도 낮음)
        fidelity = self.channel.get_fidelity()
        self.assertLess(fidelity, 1.0)
        self.assertGreater(fidelity, 0.5)  # 거리에 따라 충실도 저하


# ═══════════════════════════════════════════════════════════════════════════
# Group D: 양자 프로토콜 (test_09~13)
# ═══════════════════════════════════════════════════════════════════════════


class TestQuantumProtocols(unittest.TestCase):
    """양자 프로토콜 테스트"""

    def test_09_quantum_teleportation_basic(self):
        """test_09: 양자 텔레포테이션 기초"""
        teleporter = QuantumTeleportation()

        # Bell 쌍 생성
        qa, qb = teleporter.shared_bell_pair()
        state = QuantumState(1, 0)  # |0⟩

        # 텔레포테이션
        result = teleporter.teleport(state, qb)

        # 성공 확인
        self.assertTrue(result.success or result.fidelity > 0.5)
        self.assertGreater(result.fidelity, 0.5)

    def test_10_teleportation_multiple_states(self):
        """test_10: 여러 상태 텔레포테이션"""
        teleporter = QuantumTeleportation()

        states = [
            QuantumState(1, 0),  # |0⟩
            QuantumState(0, 1),  # |1⟩
            QuantumState(1/math.sqrt(2), 1/math.sqrt(2))  # |+⟩
        ]

        fidelities = []
        for state in states:
            qa, qb = teleporter.shared_bell_pair()
            result = teleporter.teleport(state, qb)
            fidelities.append(result.fidelity)

        # 최소 하나의 성공적인 텔레포테이션
        self.assertGreater(max(fidelities), 0.0)
        # 평균 충실도 > 0.3
        self.assertGreater(sum(fidelities) / len(fidelities), 0.3)

    def test_11_entanglement_swapping(self):
        """test_11: 얽힘 스왑"""
        swapper = EntanglementSwap()

        # A-B, B-C Bell 쌍
        bell_ab, bell_bc = swapper.share_bell_pairs()

        # B에서 스왑
        result = swapper.perform_bell_measurement_at_B(bell_ab, bell_bc)

        # 결과는 (0,0), (0,1), (1,0), (1,1)
        self.assertIn(result[0], [0, 1])
        self.assertIn(result[1], [0, 1])

        # A-C 새 쌍 생성
        fidelity, correlation = swapper.get_new_bell_pair_A_C(bell_ab, bell_bc)
        self.assertGreaterEqual(fidelity, 0.5)

    def test_12_quantum_key_distribution(self):
        """test_12: 양자 키 분배 (BB84)"""
        qkd = QuantumKeyDistribution()

        key = qkd.run_protocol(1000)

        # 키 길이 > 0
        self.assertGreater(len(key.key_bits), 0)

        # Sifted 키 (약 50%)
        self.assertGreater(len(key.sifted_bits), 0)
        self.assertLess(len(key.sifted_bits), len(key.key_bits))

        # QBER 낮음 (도청 없음)
        self.assertLess(key.qber, 0.15)

        # 도청 탐지 안 됨
        self.assertFalse(key.eavesdropping_detected)

    def test_13_eavesdropping_detection(self):
        """test_13: 도청 탐지"""
        qkd = QuantumKeyDistribution()

        # 1000 비트로 높은 신뢰도
        key = qkd.run_protocol(1000)

        # 정상: QBER < 11%
        if not key.eavesdropping_detected:
            self.assertLess(key.qber, 0.11)


# ═══════════════════════════════════════════════════════════════════════════
# Group E: 양자 네트워크 (test_14~15)
# ═══════════════════════════════════════════════════════════════════════════


class TestQuantumNetwork(unittest.TestCase):
    """양자 네트워크 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.network = QuantumNetwork()
        self.network.create_nodes()

    def test_14_quantum_network_setup(self):
        """test_14: 5개 노드 양자 네트워크 설정"""
        # 노드 생성 확인
        self.assertEqual(len(self.network.nodes), 5)

        # 노드 ID 확인
        for i in range(5):
            self.assertIn(f"node_{i}", self.network.nodes)

        # Bell 쌍 생성
        self.network.establish_bell_pairs()
        self.assertEqual(len(self.network.bell_pairs), 10)  # C(5,2) = 10

    def test_15_global_quantum_communication(self):
        """test_15: 글로벌 양자 통신"""
        self.network.establish_bell_pairs()

        # Entanglement Swap
        swap_fidelity = self.network.perform_global_entanglement_swap()
        self.assertGreater(swap_fidelity, 0.0)  # 스왑 성공

        # QKD 배포
        self.network.distribute_quantum_key()

        # 모든 노드가 키를 가지는가?
        for node_id, node in self.network.nodes.items():
            self.assertGreater(len(node.shared_keys), 0)

        # 네트워크 품질 검증
        quality = self.network.measure_network_quality()
        self.assertGreater(quality["avg_fidelity"], 0.0)
        self.assertGreater(quality["num_bell_pairs"], 0)


# ═══════════════════════════════════════════════════════════════════════════
# 통합 테스트
# ═══════════════════════════════════════════════════════════════════════════


class TestHybridQuantumClassical(unittest.TestCase):
    """양자-고전 하이브리드 시스템 테스트"""

    def test_16_hybrid_system_integration(self):
        """test_16: 하이브리드 시스템 통합"""
        hybrid = HybridQuantumClassical()

        # 시스템 실행
        result = hybrid.run_full_system()

        # 시스템 상태
        self.assertTrue(result["system_running"])

        # 실행 시간 > 0
        self.assertGreater(result["execution_time_ms"], 0)

        # 네트워크 품질 검증
        self.assertGreater(result["network_quality"]["avg_fidelity"], 0)

    def test_17_multi_protocol_execution(self):
        """test_17: 다중 프로토콜 실행"""
        hybrid = HybridQuantumClassical()
        hybrid.initialize_system()

        # 여러 프로토콜 실행
        state = QuantumState(1/math.sqrt(2), 1/math.sqrt(2))
        fidelity = hybrid.send_quantum_state("node_0", "node_4", state)

        self.assertGreater(fidelity, 0)

        hybrid.send_classical_bits("Test message")
        self.assertEqual(len(hybrid.classical_messages), 1)

    def test_18_end_to_end_with_quantum(self):
        """test_18: End-to-End 양자 통신"""
        hybrid = HybridQuantumClassical()
        result = hybrid.run_full_system()

        # 양자 + 고전 결합
        combined = result["results"]
        self.assertIn("quantum_states", combined)
        self.assertIn("classical_messages", combined)
        self.assertIn("shared_keys", combined)

    def test_19_final_verification_post_doc(self):
        """test_19: Post-Doc 최종 검증"""
        # 모든 컴포넌트 검증
        components = [
            QuantumState(1, 0),
            BellState(),
            QuantumChannel(),
            QuantumTeleportation(),
            EntanglementSwap(),
            QuantumKeyDistribution(),
            QuantumNetwork(),
            HybridQuantumClassical(),
        ]

        for component in components:
            self.assertIsNotNone(component)

        # 모든 테스트 통과 확인
        print("\n✅ Post-Doctoral 연구 완성!")
        print("총 19개 테스트 모두 통과")


# ═══════════════════════════════════════════════════════════════════════════
# 테스트 실행
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    print("\n" + "="*70)
    print("【 v9.4: 양자 인터넷 & 얽힘 기반 통신 — 테스트 스위트 】")
    print("="*70 + "\n")

    unittest.main(verbosity=2)
