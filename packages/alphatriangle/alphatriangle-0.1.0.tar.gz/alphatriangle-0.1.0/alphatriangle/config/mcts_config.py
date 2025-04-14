# File: src/config/mcts_config.py
from pydantic import BaseModel, Field, field_validator


class MCTSConfig(BaseModel):
    """
    Configuration for Monte Carlo Tree Search (Pydantic model).
    --- SERIOUS CONFIGURATION ---
    """

    # Significantly more simulations for better policy evaluation
    num_simulations: int = Field(default=512, ge=1)
    # PUCT coefficient balances exploration/exploitation. 1.0-2.5 is common.
    puct_coefficient: float = Field(default=1.2, gt=0)
    # Temperature controls exploration in action selection
    temperature_initial: float = Field(default=1.0, ge=0)  # High exploration initially
    temperature_final: float = Field(default=0.1, ge=0)  # Lower exploration later
    # Anneal temperature over more steps/episodes
    temperature_anneal_steps: int = Field(
        default=10_000, ge=0
    )  # Anneal over first 10k game steps
    # Dirichlet noise for root exploration
    dirichlet_alpha: float = Field(
        default=0.3, gt=0
    )  # Standard value, depends on action space size
    dirichlet_epsilon: float = Field(
        default=0.25, ge=0, le=1.0
    )  # Weight of noise vs prior
    # Slightly increased search depth
    max_search_depth: int = Field(default=64, ge=1)

    @field_validator("temperature_final")
    @classmethod
    def check_temp_final_le_initial(cls, v: float, info) -> float:
        # info.data might not be available during initial validation in Pydantic v2
        # Check 'values' if info.data is empty
        data = info.data if info.data else info.values
        initial_temp = data.get("temperature_initial")
        if initial_temp is not None and v > initial_temp:
            raise ValueError(
                "temperature_final cannot be greater than temperature_initial"
            )
        return v


# Ensure model is rebuilt after changes
MCTSConfig.model_rebuild(force=True)
