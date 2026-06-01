"""Reward functions for portfolio-value based learning."""

from dataclasses import dataclass


@dataclass
class RewardFunction:
    transaction_cost_alpha: float = 0.0
    slippage_beta: float = 0.0
    risk_gamma: float = 0.0

    def compute(
        self, previous_value: float, current_value: float, traded: bool, volatility: float
    ) -> float:
        base = (current_value - previous_value) / max(previous_value, 1e-9)
        cost = self.transaction_cost_alpha + self.slippage_beta if traded else 0.0
        risk_penalty = self.risk_gamma * abs(volatility)
        return float(base - cost - risk_penalty)
