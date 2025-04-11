import pytest

from kvmm.models import cait
from kvmm.tests.test_backbone_modeling import BackboneTest, ModelConfig


class TestCaiT(BackboneTest):
    @pytest.fixture
    def model_config(self) -> ModelConfig:
        return ModelConfig(model_cls=cait.CaiTXXS24, input_shape=(32, 32, 3))

    def get_default_kwargs(self) -> dict:
        return {
            "include_normalization": True,
            "normalization_mode": "imagenet",
            "classifier_activation": "softmax",
            "weights": None,
        }

    def test_backbone_features(self, model_config):
        model = self.create_model(model_config, include_top=False, as_backbone=True)
        input_data = self.get_input_data(model_config)
        features = model(input_data)

        assert isinstance(features, list), (
            "Backbone output should be a list of feature maps"
        )

        assert len(features) >= 2, "Backbone should output at least 2 feature maps"

        for i, feature_map in enumerate(features):
            is_transformer_output = len(feature_map.shape) == 3

            assert len(feature_map.shape) in (3, 4), (
                f"Feature map {i} should be a 3D (transformer) or 4D (CNN) tensor, "
                f"got shape {feature_map.shape}"
            )

            assert feature_map.shape[0] == model_config.batch_size, (
                f"Feature map {i} has incorrect batch size. "
                f"Expected {model_config.batch_size}, got {feature_map.shape[0]}"
            )

            if is_transformer_output:
                seq_len, channels = feature_map.shape[1:]
                assert seq_len > 0 and channels > 0, (
                    f"Feature map {i} has invalid dimensions: "
                    f"sequence_length={seq_len}, channels={channels}"
                )

                if i > 0:
                    prev_map = features[i - 1]
                    prev_seq_len = prev_map.shape[1]

                    # Special case for CaiT models:
                    # The last feature map in CaiT may have the class token added
                    # which increases sequence length from 196 to 197
                    if i == len(features) - 1 and seq_len == prev_seq_len + 1:
                        # This is expected for CaiT's final feature map with class token
                        continue

                    assert seq_len <= prev_seq_len, (
                        f"Feature map {i} has larger sequence length than previous feature map. "
                        f"Got {seq_len}, previous was {prev_seq_len}"
                    )
