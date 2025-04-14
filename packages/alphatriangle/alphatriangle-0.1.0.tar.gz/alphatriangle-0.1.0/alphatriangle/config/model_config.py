# File: src/config/model_config.py
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class ModelConfig(BaseModel):
    """
    Configuration for the Neural Network model (Pydantic model).
    --- SERIOUS CONFIGURATION ---
    """

    GRID_INPUT_CHANNELS: int = Field(
        default=1, gt=0
    )  # Assuming single channel input (occupancy/death)

    # --- CNN Architecture Parameters ---
    # Increased filters for more feature extraction capacity
    CONV_FILTERS: list[int] = Field(default=[64, 128])
    CONV_KERNEL_SIZES: list[int | tuple[int, int]] = Field(default=[3, 3])
    CONV_STRIDES: list[int | tuple[int, int]] = Field(default=[1, 1])
    CONV_PADDING: list[int | tuple[int, int] | str] = Field(default=[1, 1])

    # Added residual blocks for deeper representation learning
    NUM_RESIDUAL_BLOCKS: int = Field(default=4, ge=0)
    RESIDUAL_BLOCK_FILTERS: int = Field(default=128, gt=0)  # Match last conv filter

    # --- Transformer Parameters (Kept Enabled) ---
    USE_TRANSFORMER: bool = Field(default=True)
    # Increased dimensions for Transformer capacity
    TRANSFORMER_DIM: int = Field(default=128, gt=0)  # Match ResNet output
    TRANSFORMER_HEADS: int = Field(default=4, gt=0)  # Needs to divide TRANSFORMER_DIM
    TRANSFORMER_LAYERS: int = Field(default=2, ge=0)  # Moderate number of layers
    TRANSFORMER_FC_DIM: int = Field(default=256, gt=0)  # Increased feedforward dim

    # --- Fully Connected Layers ---
    # Increased dimensions for shared and head layers
    FC_DIMS_SHARED: list[int] = Field(default=[256])
    POLICY_HEAD_DIMS: list[int] = Field(default=[256])  # Output dim added automatically
    VALUE_HEAD_DIMS: list[int] = Field(default=[256, 1])  # Output dim must be 1

    # --- Other Hyperparameters ---
    ACTIVATION_FUNCTION: Literal["ReLU", "GELU", "SiLU", "Tanh", "Sigmoid"] = Field(
        default="ReLU"
    )
    USE_BATCH_NORM: bool = Field(default=True)

    # --- Input Feature Dimension ---
    # This depends on src/features/extractor.py and should match its output.
    # Default calculation: 3 slots * 7 shape feats + 3 avail feats + 6 explicit feats = 30
    OTHER_NN_INPUT_FEATURES_DIM: int = Field(default=30, gt=0)

    @model_validator(mode="after")
    def check_conv_layers_consistency(self) -> "ModelConfig":
        # Ensure attributes exist before checking lengths
        if (
            hasattr(self, "CONV_FILTERS")
            and hasattr(self, "CONV_KERNEL_SIZES")
            and hasattr(self, "CONV_STRIDES")
            and hasattr(self, "CONV_PADDING")
        ):
            n_filters = len(self.CONV_FILTERS)
            if not (
                len(self.CONV_KERNEL_SIZES) == n_filters
                and len(self.CONV_STRIDES) == n_filters
                and len(self.CONV_PADDING) == n_filters
            ):
                raise ValueError(
                    "Lengths of CONV_FILTERS, CONV_KERNEL_SIZES, CONV_STRIDES, and CONV_PADDING must match."
                )
        return self

    @field_validator("VALUE_HEAD_DIMS")
    @classmethod
    def check_value_head_last_dim(cls, v: list[int]) -> list[int]:
        if not v:
            raise ValueError("VALUE_HEAD_DIMS cannot be empty.")
        if v[-1] != 1:
            raise ValueError(
                f"The last dimension of VALUE_HEAD_DIMS must be 1 (got {v[-1]})."
            )
        return v

    @model_validator(mode="after")
    def check_residual_filter_match(self) -> "ModelConfig":
        # Ensure attributes exist before checking
        if (
            hasattr(self, "NUM_RESIDUAL_BLOCKS")
            and self.NUM_RESIDUAL_BLOCKS > 0
            and hasattr(self, "CONV_FILTERS")
            and self.CONV_FILTERS
            and hasattr(self, "RESIDUAL_BLOCK_FILTERS")
            and self.CONV_FILTERS[-1] != self.RESIDUAL_BLOCK_FILTERS
        ):
            # This warning is now handled by the projection layer in the model if needed
            pass  # Model handles projection if needed
        return self

    @model_validator(mode="after")
    def check_transformer_config(self) -> "ModelConfig":
        # Ensure attributes exist before checking
        if hasattr(self, "USE_TRANSFORMER") and self.USE_TRANSFORMER:
            if not hasattr(self, "TRANSFORMER_LAYERS") or self.TRANSFORMER_LAYERS < 0:
                raise ValueError("TRANSFORMER_LAYERS cannot be negative.")
            if self.TRANSFORMER_LAYERS > 0:
                if not hasattr(self, "TRANSFORMER_DIM") or self.TRANSFORMER_DIM <= 0:
                    raise ValueError(
                        "TRANSFORMER_DIM must be positive if TRANSFORMER_LAYERS > 0."
                    )
                if (
                    not hasattr(self, "TRANSFORMER_HEADS")
                    or self.TRANSFORMER_HEADS <= 0
                ):
                    raise ValueError(
                        "TRANSFORMER_HEADS must be positive if TRANSFORMER_LAYERS > 0."
                    )
                if self.TRANSFORMER_DIM % self.TRANSFORMER_HEADS != 0:
                    raise ValueError(
                        "TRANSFORMER_DIM must be divisible by TRANSFORMER_HEADS."
                    )
                if (
                    not hasattr(self, "TRANSFORMER_FC_DIM")
                    or self.TRANSFORMER_FC_DIM <= 0
                ):
                    raise ValueError(
                        "TRANSFORMER_FC_DIM must be positive if TRANSFORMER_LAYERS > 0."
                    )
        return self

    @model_validator(mode="after")
    def check_transformer_dim_consistency(self) -> "ModelConfig":
        # Ensure attributes exist before checking
        if (
            hasattr(self, "USE_TRANSFORMER")
            and self.USE_TRANSFORMER
            and hasattr(self, "TRANSFORMER_LAYERS")
            and self.TRANSFORMER_LAYERS > 0
            and hasattr(self, "CONV_FILTERS")
            and self.CONV_FILTERS
            and hasattr(self, "TRANSFORMER_DIM")
        ):
            cnn_output_channels = (
                self.RESIDUAL_BLOCK_FILTERS
                if hasattr(self, "NUM_RESIDUAL_BLOCKS") and self.NUM_RESIDUAL_BLOCKS > 0
                else self.CONV_FILTERS[-1]
            )
            if cnn_output_channels != self.TRANSFORMER_DIM:
                # This is handled by an input projection layer in the model now
                pass  # Model handles projection
        return self


# Ensure model is rebuilt after changes
ModelConfig.model_rebuild(force=True)
