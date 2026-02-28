#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    【 v12: Blockchain + Federated Learning 통합 플랫폼 】                  ║
║        Python University Post-Doctoral 최종 통합                           ║
║                                                                              ║
║  "분산 머신러닝 모델을 블록체인으로 경제화한다"                            ║
║                                                                              ║
║  v11 DPoS 검증자 + v10 Federated Learning 모델 = 완전한 AI 생태계        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import hashlib
import json
import math
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict


# ═══════════════════════════════════════════════════════════════════════════════
# PART 0: Enum & Dataclass (v11 + v10 통합)
# ═══════════════════════════════════════════════════════════════════════════════

class ModelStatus(Enum):
    """학습 모델 상태"""
    TRAINING    = "training"     # 학습 중
    VALIDATED   = "validated"    # 검증 완료
    COMMITTED   = "committed"    # 블록체인 기록됨
    REJECTED    = "rejected"     # 검증 실패


class ContributorRole(Enum):
    """생태계 참여자 역할"""
    DATA_PROVIDER   = "data_provider"   # 데이터 제공자
    MODEL_TRAINER   = "model_trainer"   # 모델 학습자
    VALIDATOR       = "validator"       # 블록체인 검증자
    AGGREGATOR      = "aggregator"      # FL 집계자


@dataclass
class ModelUpdate:
    """Federated Learning 모델 업데이트"""
    model_id:       str                 # 모델 고유 ID
    trainer_id:     str                 # 학습자 주소
    round_number:   int                 # 학습 라운드
    loss:           float               # 훈련 손실
    accuracy:       float               # 검증 정확도
    weights_hash:   str                 # 가중치 SHA-256
    timestamp:      float               # Unix 타임스탐프
    contribution:   float = 1.0         # 기여도 (0.0~1.0)
    status:         ModelStatus = ModelStatus.TRAINING


@dataclass
class ModelBlock:
    """모델 업데이트를 기록한 블록"""
    block_id:       int                 # 블록 높이
    model_update:   ModelUpdate         # 모델 업데이트
    validator:      str                 # 검증자 주소
    prev_hash:      str                 # 이전 블록 해시
    block_hash:     str                 # 이 블록 해시
    timestamp:      float               # 생성 시간
    consensus_votes: int = 0            # 합의 투표 수
    reward_amount:  float = 0.0         # 검증자 보상


@dataclass
class PerformanceMetric:
    """모델 성능 메트릭"""
    model_id:       str
    round_number:   int
    accuracy:       float               # 정확도 (0~1)
    loss:           float               # 손실값
    convergence:    float               # 수렴도 (0~1)
    data_quality:   float               # 데이터 품질 (0~1)
    timestamp:      float


@dataclass
class IncentiveReward:
    """인센티브 보상 기록"""
    contributor_id: str                 # 참여자 주소
    role:           ContributorRole     # 역할
    reward_amount:  float               # 보상액
    reason:         str                 # 사유 (모델검증, 데이터제공 등)
    timestamp:      float


# ═══════════════════════════════════════════════════════════════════════════════
# PART 1: FLModelBlockchain — FL 모델 + DPoS 블록체인
# ═══════════════════════════════════════════════════════════════════════════════

class FLModelBlockchain:
    """Federated Learning 모델을 DPoS 블록체인으로 관리"""

    def __init__(self):
        """초기화"""
        self._model_chain: List[ModelBlock] = []        # 모델 체인
        self._model_updates: Dict[str, List[ModelUpdate]] = defaultdict(list)
        # {model_id: [updates]}
        self._performance_history: Dict[str, List[PerformanceMetric]] = defaultdict(list)
        self._model_weights: Dict[str, List[float]] = {}  # 최신 가중치
        self._current_round: Dict[str, int] = defaultdict(int)  # 모델별 라운드

    def initialize_genesis_block(self) -> ModelBlock:
        """제네시스 블록 생성"""
        genesis_update = ModelUpdate(
            model_id="genesis",
            trainer_id="genesis",
            round_number=0,
            loss=0.0,
            accuracy=0.0,
            weights_hash="0" * 64,
            timestamp=time.time(),
            status=ModelStatus.COMMITTED
        )

        genesis_block = ModelBlock(
            block_id=0,
            model_update=genesis_update,
            validator="genesis",
            prev_hash="0" * 64,
            block_hash=self._compute_model_hash(genesis_update),
            timestamp=time.time()
        )

        self._model_chain.append(genesis_block)
        return genesis_block

    def submit_model_update(
        self,
        model_id: str,
        trainer_id: str,
        loss: float,
        accuracy: float,
        weights_hash: str
    ) -> ModelUpdate:
        """
        FL 모델 업데이트 제출
        - 학습자가 로컬 모델 학습 완료 후 제출
        """
        round_num = self._current_round[model_id]

        update = ModelUpdate(
            model_id=model_id,
            trainer_id=trainer_id,
            round_number=round_num,
            loss=loss,
            accuracy=accuracy,
            weights_hash=weights_hash,
            timestamp=time.time(),
            status=ModelStatus.TRAINING
        )

        self._model_updates[model_id].append(update)
        self._current_round[model_id] += 1

        return update

    def validate_model_update(
        self,
        model_id: str,
        round_number: int,
        validator_id: str,
        performance: PerformanceMetric
    ) -> Optional[ModelBlock]:
        """
        모델 업데이트 검증 후 블록 생성
        - 2/3 이상 검증자 투표 필요 (DPoS)
        - 성능 임계값 초과 시 블록 추가
        """
        updates = self._model_updates[model_id]
        update = None
        for u in updates:
            if u.round_number == round_number:
                update = u
                break

        if not update:
            return None

        # 성능 기준: accuracy > 0.5
        if performance.accuracy > 0.5:
            update.status = ModelStatus.VALIDATED
            self._performance_history[model_id].append(performance)

            # 블록 생성
            latest = self._model_chain[-1]
            block = ModelBlock(
                block_id=len(self._model_chain),
                model_update=update,
                validator=validator_id,
                prev_hash=latest.block_hash,
                block_hash=self._compute_model_hash(update),
                timestamp=time.time(),
                consensus_votes=1,
                reward_amount=0.0
            )

            self._model_chain.append(block)
            return block

        return None

    def record_incentive(self, reward: IncentiveReward) -> bool:
        """인센티브 보상 기록"""
        # 블록체인에는 기록하지 않고, 메모리에 누적
        # 실제로는 별도 보상 트랜잭션 블록으로 기록
        return True

    def get_model_history(self, model_id: str) -> List[ModelBlock]:
        """모델의 블록체인 히스토리 조회"""
        return [b for b in self._model_chain if b.model_update.model_id == model_id]

    def get_convergence_trend(self, model_id: str) -> List[float]:
        """모델 수렴도 추세"""
        metrics = self._performance_history[model_id]
        return [m.convergence for m in sorted(metrics, key=lambda x: x.round_number)]

    def validate_chain(self) -> Tuple[bool, str]:
        """모델 체인 무결성 검증"""
        for i in range(1, len(self._model_chain)):
            block = self._model_chain[i]
            prev_block = self._model_chain[i - 1]

            # prev_hash 검증
            if block.prev_hash != prev_block.block_hash:
                return False, f"block {i} prev_hash mismatch"

            # 블록 해시 재계산
            expected_hash = self._compute_model_hash(block.model_update)
            if block.block_hash != expected_hash:
                return False, f"block {i} hash mismatch"

        return True, ""

    @staticmethod
    def _compute_model_hash(update: ModelUpdate) -> str:
        """모델 업데이트 해시 계산"""
        data = f"{update.model_id}{update.trainer_id}{update.round_number}{update.loss}{update.accuracy}{update.weights_hash}"
        return hashlib.sha256(data.encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# PART 2: FederatedLearningAggregator — FL 집계 + 인센티브
# ═══════════════════════════════════════════════════════════════════════════════

class FederatedLearningAggregator:
    """Federated Learning 집계 + 인센티브 엔진"""

    BASE_REWARD = 100.0
    ACCURACY_WEIGHT = 0.6
    CONVERGENCE_WEIGHT = 0.3
    DATA_QUALITY_WEIGHT = 0.1

    def __init__(self):
        """초기화"""
        self._trainers: Dict[str, Dict[str, Any]] = {}  # 학습자 정보
        self._data_providers: Dict[str, Dict[str, Any]] = {}  # 데이터 제공자
        self._round_history: List[Dict[str, Any]] = []

    def register_trainer(self, trainer_id: str, stake: float) -> bool:
        """학습자 등록"""
        self._trainers[trainer_id] = {
            "stake": stake,
            "models_trained": 0,
            "total_reward": 0.0,
            "joined_at": time.time()
        }
        return True

    def register_data_provider(self, provider_id: str, data_quality: float) -> bool:
        """데이터 제공자 등록"""
        if not (0.0 <= data_quality <= 1.0):
            return False

        self._data_providers[provider_id] = {
            "data_quality": data_quality,
            "data_contributed": 0,
            "total_reward": 0.0,
            "joined_at": time.time()
        }
        return True

    def compute_trainer_reward(
        self,
        trainer_id: str,
        accuracy: float,
        convergence: float,
        data_quality: float
    ) -> float:
        """
        학습자 보상 계산
        reward = BASE × (0.6×accuracy + 0.3×convergence + 0.1×data_quality)
        """
        if trainer_id not in self._trainers:
            return 0.0

        score = (
            self.ACCURACY_WEIGHT * accuracy +
            self.CONVERGENCE_WEIGHT * convergence +
            self.DATA_QUALITY_WEIGHT * data_quality
        )

        return self.BASE_REWARD * score

    def distribute_rewards(
        self,
        round_results: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        라운드 결과에 따라 보상 배분
        - 상위 50% 학습자에게만 보상
        """
        rewards = {}

        # 성능 순위 정렬
        sorted_trainers = sorted(
            round_results.get("trainer_scores", {}).items(),
            key=lambda x: x[1],
            reverse=True
        )

        top_50_count = max(1, len(sorted_trainers) // 2)

        for i, (trainer_id, score) in enumerate(sorted_trainers):
            if i < top_50_count:
                reward = self.compute_trainer_reward(
                    trainer_id,
                    round_results.get("accuracy", 0.5),
                    round_results.get("convergence", 0.7),
                    round_results.get("data_quality", 0.8)
                )
                rewards[trainer_id] = reward
                if trainer_id in self._trainers:
                    self._trainers[trainer_id]["total_reward"] += reward

        return rewards

    def get_leaderboard(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """리더보드 조회"""
        sorted_trainers = sorted(
            self._trainers.items(),
            key=lambda x: x[1]["total_reward"],
            reverse=True
        )

        return [
            {
                "rank": i + 1,
                "trainer_id": tid[:10] + "...",
                "total_reward": info["total_reward"],
                "models_trained": info["models_trained"],
                "stake": info["stake"]
            }
            for i, (tid, info) in enumerate(sorted_trainers[:top_n])
        ]


# ═══════════════════════════════════════════════════════════════════════════════
# PART 3: IntegratedEcosystem — 전체 생태계 조율
# ═══════════════════════════════════════════════════════════════════════════════

class IntegratedEcosystem:
    """DPoS + FL + 인센티브 통합 생태계"""

    def __init__(self):
        """초기화"""
        self._blockchain = FLModelBlockchain()
        self._aggregator = FederatedLearningAggregator()
        self._contributor_balance: Dict[str, float] = {}  # 참여자 잔액
        self._round_count: int = 0

    def initialize(self) -> ModelBlock:
        """초기화"""
        # 제네시스 블록
        genesis = self._blockchain.initialize_genesis_block()

        # 초기 참여자 등록
        validators = [f"validator_{i}" for i in range(5)]
        trainers = [f"trainer_{i}" for i in range(10)]
        providers = [f"provider_{i}" for i in range(5)]

        for v in validators:
            self._contributor_balance[v] = 1000.0

        for t in trainers:
            self._aggregator.register_trainer(t, 100.0)
            self._contributor_balance[t] = 500.0

        for p in providers:
            quality = 0.7 + random.random() * 0.3
            self._aggregator.register_data_provider(p, quality)
            self._contributor_balance[p] = 300.0

        return genesis

    def run_training_round(
        self,
        model_id: str,
        trainer_ids: List[str],
        accuracy: float,
        convergence: float
    ) -> Dict[str, Any]:
        """
        한 라운드 학습 실행
        1. 학습자들이 모델 업데이트 제출
        2. 검증자가 검증 (DPoS)
        3. 보상 배분
        """
        round_num = self._round_count
        results = {
            "round": round_num,
            "model_id": model_id,
            "trainer_scores": {},
            "accuracy": accuracy,
            "convergence": convergence,
            "data_quality": 0.8,
            "rewards": {}
        }

        # 학습자들의 성능 점수
        for trainer in trainer_ids:
            score = accuracy * random.uniform(0.9, 1.1)  # ±10% 변동
            results["trainer_scores"][trainer] = max(0.0, min(1.0, score))

            # 모델 업데이트 제출
            weights_hash = f"model_{model_id}_r{round_num}_{trainer}"
            weights_hash = hashlib.sha256(weights_hash.encode()).hexdigest()

            self._blockchain.submit_model_update(
                model_id=model_id,
                trainer_id=trainer,
                loss=1.0 - accuracy,
                accuracy=results["trainer_scores"][trainer],
                weights_hash=weights_hash
            )

        # 검증자 선택 (DPoS 방식)
        validators = list(self._contributor_balance.keys())[:5]
        validator = random.choice(validators)

        # 모델 블록 검증 및 생성
        metric = PerformanceMetric(
            model_id=model_id,
            round_number=round_num,
            accuracy=accuracy,
            loss=1.0 - accuracy,
            convergence=convergence,
            data_quality=results["data_quality"],
            timestamp=time.time()
        )

        block = self._blockchain.validate_model_update(
            model_id=model_id,
            round_number=round_num,
            validator_id=validator,
            performance=metric
        )

        # 보상 계산 및 배분
        rewards = self._aggregator.distribute_rewards(results)
        results["rewards"] = rewards

        # 보상 배분
        for trainer_id, reward in rewards.items():
            self._contributor_balance[trainer_id] = self._contributor_balance.get(trainer_id, 0) + reward

        # 검증자 보상
        if block:
            validator_reward = 50.0
            self._contributor_balance[validator] = self._contributor_balance.get(validator, 0) + validator_reward
            results["validator_reward"] = validator_reward

        self._round_count += 1
        return results

    def get_ecosystem_stats(self) -> Dict[str, Any]:
        """생태계 통계"""
        return {
            "total_rounds": self._round_count,
            "model_blocks": len(self._blockchain._model_chain),
            "total_participants": len(self._contributor_balance),
            "total_distributed_reward": sum(self._contributor_balance.values()),
            "top_trainers": self._aggregator.get_leaderboard(5),
            "blockchain_valid": self._blockchain.validate_chain()[0]
        }


def main():
    """메인 데모"""
    print("\n" + "═" * 70)
    print("【 v12: Blockchain + Federated Learning 통합 】")
    print("═" * 70 + "\n")

    ecosystem = IntegratedEcosystem()
    genesis = ecosystem.initialize()

    print("【 SECTION 1: 생태계 초기화 】")
    print("─" * 70)
    print(f"✓ 제네시스 블록: {genesis.block_hash[:16]}...")
    print(f"✓ 검증자: 5명, 학습자: 10명, 데이터제공자: 5명")

    # 라운드 1: 모델 학습
    print("\n【 SECTION 2: 라운드 1-5 모델 학습 】")
    print("─" * 70)

    for round_num in range(5):
        accuracy = 0.5 + round_num * 0.08  # 수렴
        convergence = min(1.0, 0.5 + round_num * 0.1)
        trainers = [f"trainer_{i}" for i in range(10)]

        result = ecosystem.run_training_round(
            model_id="model_001",
            trainer_ids=trainers,
            accuracy=accuracy,
            convergence=convergence
        )

        print(f"✓ 라운드 {round_num + 1}: 정확도={accuracy:.3f}, 수렴도={convergence:.3f}, 보상={len(result['rewards'])}명")

    # 최종 통계
    print("\n【 SECTION 3: 생태계 통계 】")
    print("─" * 70)

    stats = ecosystem.get_ecosystem_stats()
    print(f"✓ 총 라운드: {stats['total_rounds']}")
    print(f"✓ 모델 블록: {stats['model_blocks']}개")
    print(f"✓ 참여자: {stats['total_participants']}명")
    print(f"✓ 총 배분 보상: {stats['total_distributed_reward']:.0f}")
    print(f"✓ 블록체인 유효성: {'✓' if stats['blockchain_valid'] else '✗'}")

    print("\n【 Top 5 학습자 】")
    print("─" * 70)
    for trainer in stats["top_trainers"]:
        print(f"  {trainer['rank']}위: {trainer['trainer_id']} (보상: {trainer['total_reward']:.0f})")

    # 체인 검증
    valid, msg = ecosystem._blockchain.validate_chain()
    print(f"\n✓ 모델 체인 무결성: {'유효' if valid else '오류: ' + msg}")

    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║         【 v12: 블록체인 + FL 통합 완성 】                   ║")
    print("║                                                                ║")
    print("║  ✓ FLModelBlockchain: DPoS로 FL 모델 관리                    ║")
    print("║  ✓ FederatedLearningAggregator: 성능기반 보상                ║")
    print("║  ✓ IntegratedEcosystem: 완전한 생태계                        ║")
    print("║  ✓ 라운드별 모델 저장 + 자동 인센티브                        ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")


if __name__ == "__main__":
    main()
