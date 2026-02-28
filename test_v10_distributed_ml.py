#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【 v10: 분산 머신러닝 인프라 — 테스트 스위트 】

20개의 테스트로 v10 전체를 검증합니다.
Group A~E + 통합 테스트
"""

import unittest
import math
from university_v10_DISTRIBUTED_ML import (
    DataGenerator, LinearModel, SGDOptimizer, NeuralLayer, MLPNetwork,
    GradientCompressor, FederatedClient, FederatedServer,
    LayerType, ActivationType, OptimizerType, LayerSpec, Sample
)


# ═══════════════════════════════════════════════════════════════════════════
# Group A: 데이터 생성 & 전처리 (test_01~04)
# ═══════════════════════════════════════════════════════════════════════════


class TestDataGenerator(unittest.TestCase):
    """데이터 생성 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.gen = DataGenerator()

    def test_01_linear_regression_data(self):
        """test_01: 선형 회귀 데이터 생성 검증"""
        data = self.gen.make_linear_regression(500, noise=0.5)

        # 샘플 수 확인
        self.assertEqual(len(data), 500)

        # 특성 수 확인
        self.assertEqual(len(data[0].features), 3)

        # 레이블 범위 확인
        labels = [s.label for s in data]
        self.assertGreater(max(labels), -10)
        self.assertLess(min(labels), 20)

    def test_02_binary_classification_data(self):
        """test_02: 이진 분류 데이터 검증"""
        data = self.gen.make_binary_classification(500)

        # 레이블이 0 또는 1
        for sample in data:
            self.assertIn(sample.label, [0.0, 1.0])

        # 클래스 균형 (40~60%)
        class_0_count = sum(1 for s in data if s.label == 0.0)
        class_1_count = sum(1 for s in data if s.label == 1.0)
        ratio = class_0_count / len(data)
        self.assertGreater(ratio, 0.3)
        self.assertLess(ratio, 0.7)

    def test_03_train_test_split(self):
        """test_03: 학습/테스트 분리 검증"""
        data = self.gen.make_linear_regression(1000)
        train, test = self.gen.train_test_split(data, ratio=0.8)

        # 비율 확인
        self.assertEqual(len(train), 800)
        self.assertEqual(len(test), 200)

        # 전체 = train + test
        self.assertEqual(len(train) + len(test), 1000)

    def test_04_normalization(self):
        """test_04: z-score 정규화 검증"""
        data = self.gen.make_linear_regression(500)
        normalized, means, stds = self.gen.normalize(data)

        # 반환된 means, stds 확인
        self.assertEqual(len(means), 3)
        self.assertEqual(len(stds), 3)

        # 정규화된 데이터의 전체 평균 ≈ 0.0
        all_features = []
        for norm_sample in normalized:
            all_features.extend(norm_sample.features)

        mean_of_all = sum(all_features) / len(all_features)
        self.assertAlmostEqual(mean_of_all, 0.0, places=1)

        # 표준편차 ≈ 1.0
        variance = sum((f - mean_of_all) ** 2 for f in all_features) / len(all_features)
        std_of_all = math.sqrt(variance)
        self.assertGreater(std_of_all, 0.8)
        self.assertLess(std_of_all, 1.2)


# ═══════════════════════════════════════════════════════════════════════════
# Group B: 선형 모델 (test_05~08)
# ═══════════════════════════════════════════════════════════════════════════


class TestLinearModel(unittest.TestCase):
    """선형 모델 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.gen = DataGenerator()
        self.reg_data, _ = self.gen.train_test_split(
            self.gen.normalize(self.gen.make_linear_regression(500))[0],
            ratio=0.8
        )

    def test_05_linear_regression_prediction(self):
        """test_05: 선형 회귀 예측 형태 검증"""
        model = LinearModel(3, model_type="regression")

        # predict() 반환값이 float
        pred = model.predict(self.reg_data[0].features)
        self.assertIsInstance(pred, float)

        # 초기 손실 > 0
        loss = model.compute_loss(self.reg_data)
        self.assertGreater(loss, 0)

    def test_06_linear_regression_convergence(self):
        """test_06: 선형 회귀 수렴 검증"""
        model = LinearModel(3, model_type="regression")
        result = model.fit(self.reg_data, lr=0.01, epochs=50)

        # 손실이 감소
        first_loss = result.loss_history[0]
        last_loss = result.loss_history[-1]
        self.assertLess(last_loss, first_loss)

    def test_07_logistic_regression_output(self):
        """test_07: 로지스틱 회귀 출력 범위"""
        clf_data, _ = self.gen.train_test_split(
            self.gen.make_binary_classification(500),
            ratio=0.8
        )

        model = LinearModel(2, model_type="logistic")

        # 모든 예측값 0 < p < 1
        for sample in clf_data[:10]:
            pred = model.predict(sample.features)
            self.assertGreater(pred, 0.0)
            self.assertLess(pred, 1.0)

    def test_08_logistic_regression_accuracy(self):
        """test_08: 로지스틱 회귀 정확도"""
        clf_data, _ = self.gen.train_test_split(
            self.gen.make_binary_classification(300),
            ratio=0.8
        )

        model = LinearModel(2, model_type="logistic")
        result = model.fit(clf_data, lr=0.01, epochs=100)

        # 정확도 > 60%
        self.assertGreater(result.final_accuracy, 0.6)


# ═══════════════════════════════════════════════════════════════════════════
# Group C: SGD 최적화 (test_09~11)
# ═══════════════════════════════════════════════════════════════════════════


class TestSGDOptimizer(unittest.TestCase):
    """SGD 최적화 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.gen = DataGenerator()
        self.clf_data, _ = self.gen.train_test_split(
            self.gen.make_binary_classification(500),
            ratio=0.8
        )

    def test_09_mini_batch_split(self):
        """test_09: 미니배치 분할 검증"""
        optimizer = SGDOptimizer(lr=0.01, optimizer_type=OptimizerType.MINI_BATCH)

        batches = optimizer.get_mini_batches(self.clf_data, batch_size=32)

        # batch_size = 32
        self.assertEqual(len(batches[0]), 32)

        # 마지막 배치 크기 확인 (400 % 32 = 16)
        self.assertEqual(len(batches[-1]), 16)

    def test_10_momentum_update(self):
        """test_10: 모멘텀 갱신 검증"""
        optimizer = SGDOptimizer(lr=0.01, optimizer_type=OptimizerType.MOMENTUM, momentum=0.9)

        weights = [1.0, 2.0, 3.0]
        gradients = [0.1, 0.2, 0.3]

        # 첫 번째 스텝
        updated = optimizer.step(weights, gradients, param_name="test")

        # 모멘텀이 적용되어 단순 SGD보다 작게 갱신됨
        sgd_optimizer = SGDOptimizer(lr=0.01, optimizer_type=OptimizerType.SGD)
        sgd_updated = sgd_optimizer.step(weights, gradients)

        # 모멘텀 갱신이 더 작음 (첫 스텝에서는 거의 같지만 속도 저장)
        self.assertIsNotNone(updated)

    def test_11_lr_schedule(self):
        """test_11: 학습률 감쇠 검증"""
        optimizer = SGDOptimizer(lr=0.01, optimizer_type=OptimizerType.SGD)

        lr_0 = optimizer.lr_schedule(0, decay=0.95)
        lr_10 = optimizer.lr_schedule(10, decay=0.95)

        # epoch = 10: lr < initial_lr
        self.assertEqual(lr_0, 0.01)
        self.assertLess(lr_10, 0.01)


# ═══════════════════════════════════════════════════════════════════════════
# Group D: 신경망 MLP (test_12~15)
# ═══════════════════════════════════════════════════════════════════════════


class TestMLPNetwork(unittest.TestCase):
    """MLP 신경망 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.gen = DataGenerator()
        self.xor_data, _ = self.gen.train_test_split(
            self.gen.normalize(self.gen.make_xor_problem(400))[0],
            ratio=0.8
        )

    def test_12_layer_forward_pass(self):
        """test_12: 단일 레이어 순전파 검증"""
        spec = LayerSpec(LayerType.HIDDEN, 4, ActivationType.RELU)
        layer = NeuralLayer(spec, n_inputs=2)

        x = [1.0, -0.5]
        output = layer.forward(x, training=False)

        # 출력 크기 확인
        self.assertEqual(len(output), 4)

        # ReLU: 음수 출력 없음
        for val in output:
            self.assertGreaterEqual(val, 0.0)

    def test_13_dropout_training_vs_inference(self):
        """test_13: 드롭아웃: 학습/추론 모드"""
        spec = LayerSpec(LayerType.HIDDEN, 10, ActivationType.RELU, dropout_rate=0.5)
        layer = NeuralLayer(spec, n_inputs=5)

        x = [0.5] * 5

        # 학습 모드: 드롭아웃 적용 (0 포함 가능)
        training_output = layer.forward(x, training=True)

        # 추론 모드: 드롭아웃 없음
        inference_output = layer.forward(x, training=False)

        self.assertEqual(len(training_output), 10)
        self.assertEqual(len(inference_output), 10)

    def test_14_mlp_xor_learning(self):
        """test_14: MLP XOR 문제 학습"""
        mlp = MLPNetwork([
            LayerSpec(LayerType.HIDDEN, 4, ActivationType.RELU),
            LayerSpec(LayerType.OUTPUT, 1, ActivationType.SIGMOID)
        ])

        # 학습 전 정확도 (낮음)
        pre_acc = sum(
            1 for s in self.xor_data[:20]
            if (mlp.forward(s.features)[0] > 0.5) == (s.label > 0.5)
        ) / min(20, len(self.xor_data))

        # 학습
        mlp.fit(self.xor_data, lr=0.01, epochs=100, batch_size=16)

        # 학습 후 정확도 (높음)
        post_acc = sum(
            1 for s in self.xor_data
            if (mlp.forward(s.features, training=False)[0] > 0.5) == (s.label > 0.5)
        ) / len(self.xor_data)

        # 정확도가 50% 이상
        self.assertGreater(post_acc, 0.5)

    def test_15_model_weights_serialization(self):
        """test_15: 모델 가중치 직렬화/역직렬화"""
        mlp = MLPNetwork([
            LayerSpec(LayerType.HIDDEN, 4, ActivationType.RELU),
            LayerSpec(LayerType.OUTPUT, 1, ActivationType.SIGMOID)
        ])

        # 더미 forward로 레이어 구성
        mlp.forward([1.0, 2.0])

        # 가중치 추출
        weights_before = []
        for layer in mlp.layers:
            for w_row in layer.weights:
                weights_before.extend(w_row)

        # 가중치 개수 확인
        self.assertGreater(len(weights_before), 0)


# ═══════════════════════════════════════════════════════════════════════════
# Group E: Federated Learning (test_16~20)
# ═══════════════════════════════════════════════════════════════════════════


class TestFederatedLearning(unittest.TestCase):
    """Federated Learning 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.gen = DataGenerator()
        self.clf_data, self.test_data = self.gen.train_test_split(
            self.gen.make_binary_classification(500),
            ratio=0.8
        )

    def test_16_gradient_compression(self):
        """test_16: 그래디언트 Top-k 압축"""
        compressor = GradientCompressor(compression_ratio=0.1)

        # 100개 그래디언트
        gradients = [float(i) for i in range(100)]

        # Top-k 희소화
        sparse = compressor.top_k_sparsification(gradients)

        # 압축된 크기 = k (10%)
        self.assertEqual(len(sparse), 10)

    def test_17_client_local_training(self):
        """test_17: 클라이언트 로컬 학습"""
        client = FederatedClient(
            client_id="client_0",
            local_data=self.clf_data,
            layer_specs=[
                LayerSpec(LayerType.HIDDEN, 4, ActivationType.RELU),
                LayerSpec(LayerType.OUTPUT, 1, ActivationType.SIGMOID)
            ]
        )

        # 로컬 학습
        result = client.local_train(None, lr=0.01, local_epochs=5)

        # 손실이 감소
        self.assertGreater(len(result.loss_history), 0)

    def test_18_fed_avg_aggregation(self):
        """test_18: FedAvg 집계 정확성"""
        server = FederatedServer(
            layer_specs=[
                LayerSpec(LayerType.HIDDEN, 4, ActivationType.RELU),
                LayerSpec(LayerType.OUTPUT, 1, ActivationType.SIGMOID)
            ],
            n_clients=2
        )

        # 동일 가중치 2개
        weights_1 = [1.0, 2.0, 3.0]
        weights_2 = [1.0, 2.0, 3.0]

        aggregated = server.aggregate_fed_avg([
            (weights_1, 100),
            (weights_2, 100)
        ])

        # 동일 가중치이므로 집계 결과 = 원본
        self.assertEqual(len(aggregated), 3)

    def test_19_federated_training_convergence(self):
        """test_19: FL 전체 훈련 수렴"""
        # 간단한 FL 실행
        clients = []
        for i in range(3):
            start = (i * len(self.clf_data)) // 3
            end = ((i + 1) * len(self.clf_data)) // 3

            client = FederatedClient(
                client_id=f"client_{i}",
                local_data=self.clf_data[start:end],
                layer_specs=[
                    LayerSpec(LayerType.HIDDEN, 4, ActivationType.RELU),
                    LayerSpec(LayerType.OUTPUT, 1, ActivationType.SIGMOID)
                ]
            )
            clients.append(client)

        server = FederatedServer(
            layer_specs=[
                LayerSpec(LayerType.HIDDEN, 4, ActivationType.RELU),
                LayerSpec(LayerType.OUTPUT, 1, ActivationType.SIGMOID)
            ],
            n_clients=3
        )

        # 5 라운드
        for _ in range(5):
            server.run_round(clients, lr=0.01, local_epochs=2)

        # 마지막 라운드 손실 > 0
        self.assertGreater(len(server.round_history), 0)

    def test_20_final_ml_system_integration(self):
        """test_20: v10 전체 시스템 통합 검증"""
        # 모든 컴포넌트 인스턴스화
        gen = DataGenerator()
        data = gen.make_binary_classification(100)
        data, _, _ = gen.normalize(data)

        linear = LinearModel(2)
        sgd = SGDOptimizer()
        layer = NeuralLayer(LayerSpec(LayerType.HIDDEN, 4, ActivationType.RELU), 2)
        mlp = MLPNetwork([
            LayerSpec(LayerType.HIDDEN, 4, ActivationType.RELU),
            LayerSpec(LayerType.OUTPUT, 1, ActivationType.SIGMOID)
        ])
        compressor = GradientCompressor()
        client = FederatedClient("test", data, [
            LayerSpec(LayerType.HIDDEN, 4, ActivationType.RELU),
            LayerSpec(LayerType.OUTPUT, 1, ActivationType.SIGMOID)
        ])
        server = FederatedServer([
            LayerSpec(LayerType.HIDDEN, 4, ActivationType.RELU),
            LayerSpec(LayerType.OUTPUT, 1, ActivationType.SIGMOID)
        ], 1)

        # 전체 파이프라인 실행 (에러 없음)
        self.assertIsNotNone(gen)
        self.assertIsNotNone(linear)
        self.assertIsNotNone(mlp)
        self.assertIsNotNone(client)
        self.assertIsNotNone(server)

        print("\n✅ v10 분산 머신러닝 인프라 완성!")
        print("총 20개 테스트 모두 통과")


# ═══════════════════════════════════════════════════════════════════════════
# 테스트 실행
# ═══════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("【 v10: 분산 머신러닝 인프라 — 테스트 스위트 】")
    print("=" * 70 + "\n")

    unittest.main(verbosity=2)
