#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║       【 v12: Decentralized AI Training Platform (DApp) 】                 ║
║                  완전한 분산 머신러닝 생태계                               ║
║                                                                              ║
║  DataProvider → ModelTrainer → ModelValidator → IncentiveEngine            ║
║       ↓              ↓               ↓               ↓                      ║
║   데이터제공    로컬학습      블록체인검증      자동보상                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import hashlib
import json
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict


# ═══════════════════════════════════════════════════════════════════════════════
# PART 0: Data Models
# ═══════════════════════════════════════════════════════════════════════════════

class DataQuality(Enum):
    """데이터 품질 등급"""
    LOW     = "low"        # < 0.6
    MEDIUM  = "medium"     # 0.6~0.8
    HIGH    = "high"       # > 0.8


@dataclass
class Dataset:
    """학습 데이터셋"""
    dataset_id:     str
    provider_id:    str
    num_samples:    int
    feature_dim:    int
    quality_score:  float              # 0.0~1.0
    data_hash:      str                # SHA-256
    timestamp:      float


@dataclass
class ModelGradient:
    """모델 그래디언트"""
    trainer_id:     str
    model_id:       str
    round_number:   int
    gradient_norm:  float
    timestamp:      float


@dataclass
class ValidationResult:
    """검증 결과"""
    validator_id:   str
    model_id:       str
    round_number:   int
    accuracy:       float
    loss:           float
    is_valid:       bool               # 기준 초과 여부
    timestamp:      float


@dataclass
class Transaction:
    """인센티브 트랜잭션"""
    tx_id:          str
    from_addr:      str
    to_addr:        str
    amount:         float
    reason:         str                # "model_validation", "data_provision"
    timestamp:      float


# ═══════════════════════════════════════════════════════════════════════════════
# PART 1: DataProvider — 데이터 제공 시스템
# ═══════════════════════════════════════════════════════════════════════════════

class DataProvider:
    """데이터 제공자"""

    def __init__(self, provider_id: str):
        """초기화"""
        self.provider_id = provider_id
        self._datasets: Dict[str, Dataset] = {}
        self._reputation = 0.8  # 0~1 신뢰도
        self._datasets_provided = 0
        self._total_reward = 0.0

    def create_dataset(
        self,
        num_samples: int,
        feature_dim: int,
        quality_score: float
    ) -> Dataset:
        """
        데이터셋 생성
        - 실제로는 데이터를 생성하거나 업로드
        """
        dataset_id = f"data_{self.provider_id}_{self._datasets_provided}"
        data_hash = hashlib.sha256(
            f"{dataset_id}{time.time()}".encode()
        ).hexdigest()

        dataset = Dataset(
            dataset_id=dataset_id,
            provider_id=self.provider_id,
            num_samples=num_samples,
            feature_dim=feature_dim,
            quality_score=quality_score,
            data_hash=data_hash,
            timestamp=time.time()
        )

        self._datasets[dataset_id] = dataset
        self._datasets_provided += 1
        return dataset

    def get_reputation(self) -> float:
        """신뢰도 조회"""
        return self._reputation

    def update_reputation(self, feedback: float) -> None:
        """신뢰도 업데이트 (피드백 기반)"""
        self._reputation = 0.9 * self._reputation + 0.1 * feedback
        self._reputation = max(0.0, min(1.0, self._reputation))

    def receive_reward(self, amount: float) -> None:
        """보상 수령"""
        self._total_reward += amount


# ═══════════════════════════════════════════════════════════════════════════════
# PART 2: ModelTrainer — 로컬 모델 학습
# ═══════════════════════════════════════════════════════════════════════════════

class ModelTrainer:
    """모델 학습자"""

    def __init__(self, trainer_id: str):
        """초기화"""
        self.trainer_id = trainer_id
        self._models: Dict[str, Dict[str, Any]] = {}
        self._gradient_history: List[ModelGradient] = []
        self._accuracy_history: List[float] = []
        self._total_reward = 0.0
        self._rounds_trained = 0

    def local_train(
        self,
        model_id: str,
        round_number: int,
        learning_rate: float = 0.01
    ) -> ModelGradient:
        """
        로컬 모델 학습
        - Simulated SGD update
        """
        if model_id not in self._models:
            self._models[model_id] = {"weights": [random.random() for _ in range(10)]}

        # 그래디언트 계산 (시뮬레이션)
        gradient_norm = learning_rate * random.uniform(0.1, 1.0)

        gradient = ModelGradient(
            trainer_id=self.trainer_id,
            model_id=model_id,
            round_number=round_number,
            gradient_norm=gradient_norm,
            timestamp=time.time()
        )

        self._gradient_history.append(gradient)
        self._rounds_trained += 1

        return gradient

    def report_accuracy(self, accuracy: float) -> None:
        """정확도 보고"""
        self._accuracy_history.append(accuracy)

    def get_average_accuracy(self) -> float:
        """평균 정확도"""
        if not self._accuracy_history:
            return 0.0
        return sum(self._accuracy_history) / len(self._accuracy_history)

    def receive_reward(self, amount: float) -> None:
        """보상 수령"""
        self._total_reward += amount


# ═══════════════════════════════════════════════════════════════════════════════
# PART 3: ModelValidator — 블록체인 검증자
# ═══════════════════════════════════════════════════════════════════════════════

class ModelValidator:
    """블록체인 검증자 (DPoS)"""

    VALIDATION_THRESHOLD = 0.5  # 정확도 기준

    def __init__(self, validator_id: str, stake: float):
        """초기화"""
        self.validator_id = validator_id
        self.stake = stake
        self._validations: List[ValidationResult] = []
        self._blocks_validated = 0
        self._total_reward = 0.0

    def validate_model(
        self,
        model_id: str,
        round_number: int,
        reported_accuracy: float
    ) -> ValidationResult:
        """
        모델 검증 (DPoS 방식)
        - 기준값 초과 시 유효
        """
        # 검증 시뮬레이션: 보고된 정확도에 노이즈 추가
        actual_accuracy = reported_accuracy * random.uniform(0.95, 1.05)
        actual_accuracy = max(0.0, min(1.0, actual_accuracy))

        is_valid = actual_accuracy > self.VALIDATION_THRESHOLD

        result = ValidationResult(
            validator_id=self.validator_id,
            model_id=model_id,
            round_number=round_number,
            accuracy=actual_accuracy,
            loss=1.0 - actual_accuracy,
            is_valid=is_valid,
            timestamp=time.time()
        )

        self._validations.append(result)
        if is_valid:
            self._blocks_validated += 1

        return result

    def get_validation_rate(self) -> float:
        """검증 성공률"""
        if not self._validations:
            return 0.0
        valid_count = sum(1 for v in self._validations if v.is_valid)
        return valid_count / len(self._validations)

    def receive_reward(self, amount: float) -> None:
        """보상 수령"""
        self._total_reward += amount


# ═══════════════════════════════════════════════════════════════════════════════
# PART 4: IncentiveEngine — 인센티브 배분 엔진
# ═══════════════════════════════════════════════════════════════════════════════

class IncentiveEngine:
    """자동 인센티브 배분"""

    TOTAL_POOL = 1000.0  # 라운드별 보상 풀
    DATA_SHARE = 0.15     # 데이터 제공 15%
    TRAINER_SHARE = 0.50  # 학습 50%
    VALIDATOR_SHARE = 0.35  # 검증 35%

    def __init__(self):
        """초기화"""
        self._transactions: List[Transaction] = []
        self._wallet: Dict[str, float] = defaultdict(float)
        self._round_metrics: List[Dict[str, Any]] = []

    def distribute_round_rewards(
        self,
        round_number: int,
        data_providers: List[DataProvider],
        trainers: List[ModelTrainer],
        validators: List[ModelValidator],
        model_accuracies: Dict[str, float]
    ) -> Dict[str, float]:
        """
        라운드별 보상 배분
        1. 데이터 제공자: 품질 기반
        2. 학습자: 정확도 기반
        3. 검증자: 검증 성공률 기반
        """
        rewards = {}
        distributed = 0.0

        # 1. 데이터 제공자 보상
        if data_providers:
            data_pool = self.TOTAL_POOL * self.DATA_SHARE
            total_quality = sum(p.get_reputation() for p in data_providers)

            for provider in data_providers:
                if total_quality > 0:
                    reward = data_pool * (provider.get_reputation() / total_quality)
                    rewards[provider.provider_id] = reward
                    self._wallet[provider.provider_id] += reward
                    provider.receive_reward(reward)
                    distributed += reward

        # 2. 학습자 보상 (상위 50%)
        if trainers:
            trainer_pool = self.TOTAL_POOL * self.TRAINER_SHARE
            sorted_trainers = sorted(
                trainers,
                key=lambda t: t.get_average_accuracy(),
                reverse=True
            )
            top_50 = sorted_trainers[:max(1, len(sorted_trainers) // 2)]

            for trainer in top_50:
                reward = trainer_pool / len(top_50)
                rewards[trainer.trainer_id] = reward
                self._wallet[trainer.trainer_id] += reward
                trainer.receive_reward(reward)
                distributed += reward

        # 3. 검증자 보상 (성공률 기반)
        if validators:
            validator_pool = self.TOTAL_POOL * self.VALIDATOR_SHARE
            total_rate = sum(v.get_validation_rate() for v in validators)

            for validator in validators:
                if total_rate > 0:
                    reward = validator_pool * (validator.get_validation_rate() / total_rate)
                    rewards[validator.validator_id] = reward
                    self._wallet[validator.validator_id] += reward
                    validator.receive_reward(reward)
                    distributed += reward

        # 메트릭 기록
        self._round_metrics.append({
            "round": round_number,
            "distributed": distributed,
            "participant_count": len(data_providers) + len(trainers) + len(validators),
            "avg_accuracy": sum(model_accuracies.values()) / len(model_accuracies) if model_accuracies else 0.0
        })

        return rewards

    def get_wallet_balance(self, address: str) -> float:
        """지갑 잔액 조회"""
        return self._wallet.get(address, 0.0)

    def get_ecosystem_stats(self) -> Dict[str, Any]:
        """생태계 통계"""
        if not self._round_metrics:
            return {}

        total_distributed = sum(m["distributed"] for m in self._round_metrics)
        avg_accuracy = sum(m["avg_accuracy"] for m in self._round_metrics) / len(self._round_metrics)

        return {
            "total_rounds": len(self._round_metrics),
            "total_distributed": total_distributed,
            "avg_accuracy": avg_accuracy,
            "active_participants": len(self._wallet),
            "avg_per_round": total_distributed / len(self._round_metrics) if self._round_metrics else 0.0
        }


# ═══════════════════════════════════════════════════════════════════════════════
# PART 5: DecentralizedAIPlatform — 완전한 DApp
# ═══════════════════════════════════════════════════════════════════════════════

class DecentralizedAIPlatform:
    """완전한 분산 AI 플랫폼 DApp"""

    def __init__(self):
        """초기화"""
        self._data_providers: Dict[str, DataProvider] = {}
        self._trainers: Dict[str, ModelTrainer] = {}
        self._validators: Dict[str, ModelValidator] = {}
        self._incentive_engine = IncentiveEngine()
        self._round_count = 0
        self._model_accuracies: Dict[str, List[float]] = defaultdict(list)

    def register_data_provider(self, provider_id: str) -> DataProvider:
        """데이터 제공자 등록"""
        provider = DataProvider(provider_id)
        self._data_providers[provider_id] = provider
        return provider

    def register_trainer(self, trainer_id: str) -> ModelTrainer:
        """학습자 등록"""
        trainer = ModelTrainer(trainer_id)
        self._trainers[trainer_id] = trainer
        return trainer

    def register_validator(self, validator_id: str, stake: float) -> ModelValidator:
        """검증자 등록 (DPoS)"""
        validator = ModelValidator(validator_id, stake)
        self._validators[validator_id] = validator
        return validator

    def run_training_round(
        self,
        model_id: str,
        round_number: int
    ) -> Dict[str, Any]:
        """
        한 라운드 전체 실행
        1. 데이터 제공자가 데이터 제공
        2. 학습자가 로컬 학습
        3. 검증자가 검증
        4. 인센티브 배분
        """
        round_results = {
            "round": round_number,
            "model_id": model_id,
            "phases": {}
        }

        # Phase 1: 데이터 제공
        datasets_provided = 0
        for provider in self._data_providers.values():
            dataset = provider.create_dataset(
                num_samples=1000,
                feature_dim=50,
                quality_score=0.7 + random.random() * 0.3
            )
            datasets_provided += 1

        round_results["phases"]["data_provision"] = f"{datasets_provided}개 데이터셋"

        # Phase 2: 로컬 학습
        trainers_trained = 0
        for trainer in self._trainers.values():
            gradient = trainer.local_train(
                model_id=model_id,
                round_number=round_number,
                learning_rate=0.01
            )
            # 시뮬레이션된 정확도
            accuracy = 0.5 + round_number * 0.05 + random.random() * 0.1
            trainer.report_accuracy(accuracy)
            self._model_accuracies[model_id].append(accuracy)
            trainers_trained += 1

        round_results["phases"]["local_training"] = f"{trainers_trained}명 학습"

        # Phase 3: 모델 검증
        validations = {}
        for validator in self._validators.values():
            # 모델 정확도 선택
            model_accuracy = random.choice(self._model_accuracies[model_id])
            result = validator.validate_model(
                model_id=model_id,
                round_number=round_number,
                reported_accuracy=model_accuracy
            )
            validations[validator.validator_id] = result

        valid_count = sum(1 for r in validations.values() if r.is_valid)
        round_results["phases"]["validation"] = f"{valid_count}/{len(self._validators)}명 검증 성공"

        # Phase 4: 인센티브 배분
        model_accuracies = {
            model_id: sum(self._model_accuracies[model_id]) / len(self._model_accuracies[model_id])
        }

        rewards = self._incentive_engine.distribute_round_rewards(
            round_number=round_number,
            data_providers=list(self._data_providers.values()),
            trainers=list(self._trainers.values()),
            validators=list(self._validators.values()),
            model_accuracies=model_accuracies
        )

        round_results["phases"]["incentive"] = f"{len(rewards)}명 보상"
        round_results["total_distributed"] = sum(rewards.values())

        self._round_count += 1
        return round_results

    def get_leaderboard(self) -> Dict[str, List[Dict[str, Any]]]:
        """리더보드"""
        return {
            "trainers": [
                {
                    "rank": i + 1,
                    "trainer_id": t.trainer_id[:10] + "...",
                    "accuracy": t.get_average_accuracy(),
                    "reward": t._total_reward,
                    "rounds": t._rounds_trained
                }
                for i, t in enumerate(
                    sorted(self._trainers.values(), key=lambda x: x.get_average_accuracy(), reverse=True)[:5]
                )
            ],
            "validators": [
                {
                    "rank": i + 1,
                    "validator_id": v.validator_id[:10] + "...",
                    "stake": v.stake,
                    "validation_rate": f"{v.get_validation_rate():.1%}",
                    "reward": v._total_reward,
                    "blocks_validated": v._blocks_validated
                }
                for i, v in enumerate(
                    sorted(self._validators.values(), key=lambda x: x.get_validation_rate(), reverse=True)[:5]
                )
            ]
        }

    def get_platform_stats(self) -> Dict[str, Any]:
        """플랫폼 통계"""
        incentive_stats = self._incentive_engine.get_ecosystem_stats()

        return {
            "rounds_completed": self._round_count,
            "participants": {
                "data_providers": len(self._data_providers),
                "trainers": len(self._trainers),
                "validators": len(self._validators),
                "total": len(self._data_providers) + len(self._trainers) + len(self._validators)
            },
            "incentives": incentive_stats,
            "total_rewards_distributed": sum(
                p._total_reward for p in self._data_providers.values()
            ) + sum(
                t._total_reward for t in self._trainers.values()
            ) + sum(
                v._total_reward for v in self._validators.values()
            )
        }


def main():
    """메인 데모"""
    print("\n" + "═" * 70)
    print("【 v12: Decentralized AI Platform (완전한 DApp) 】")
    print("═" * 70 + "\n")

    platform = DecentralizedAIPlatform()

    # 참여자 등록
    print("【 SECTION 1: DApp 참여자 등록 】")
    print("─" * 70)

    for i in range(3):
        platform.register_data_provider(f"provider_{i}")
    print(f"✓ 데이터 제공자: 3명")

    for i in range(10):
        platform.register_trainer(f"trainer_{i}")
    print(f"✓ 모델 학습자: 10명")

    for i in range(5):
        platform.register_validator(f"validator_{i}", stake=1000.0)
    print(f"✓ 블록체인 검증자: 5명 (총 5,000 GOG 스테이킹)")

    # 라운드 실행
    print("\n【 SECTION 2: 10라운드 분산 학습 】")
    print("─" * 70)

    for round_num in range(10):
        result = platform.run_training_round("model_001", round_num)
        phases = result["phases"]
        print(f"✓ 라운드 {round_num + 1}: {phases['data_provision']} → {phases['local_training']} → {phases['validation']} → 보상 {phases['incentive']}")

    # 통계
    print("\n【 SECTION 3: 플랫폼 통계 】")
    print("─" * 70)

    stats = platform.get_platform_stats()
    print(f"✓ 완료된 라운드: {stats['rounds_completed']}")
    print(f"✓ 총 참여자: {stats['participants']['total']}명")
    print(f"✓ 총 배분 보상: {stats['total_rewards_distributed']:.0f} GOG")
    print(f"✓ 평균 모델 정확도: {stats['incentives']['avg_accuracy']:.2%}")

    # 리더보드
    print("\n【 Top 5 학습자 】")
    print("─" * 70)

    leaderboard = platform.get_leaderboard()
    for trainer in leaderboard["trainers"]:
        print(f"  {trainer['rank']}위: {trainer['trainer_id']} (정확도 {trainer['accuracy']:.2%}, 보상 {trainer['reward']:.0f})")

    print("\n【 Top 5 검증자 】")
    print("─" * 70)

    for validator in leaderboard["validators"]:
        print(f"  {validator['rank']}위: {validator['validator_id']} (검증 {validator['validation_rate']}, 보상 {validator['reward']:.0f})")

    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║       【 v12: 분산 AI 플랫폼 DApp 완성 】                   ║")
    print("║                                                                ║")
    print("║  ✓ DataProvider: 데이터 제공 + 품질 관리                     ║")
    print("║  ✓ ModelTrainer: 로컬 학습 + 그래디언트 업로드                ║")
    print("║  ✓ ModelValidator: DPoS 검증 + 블록 기록                     ║")
    print("║  ✓ IncentiveEngine: 자동 보상 배분                           ║")
    print("║  ✓ 10라운드 완료 + 리더보드 + 통계                           ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")


if __name__ == "__main__":
    main()
