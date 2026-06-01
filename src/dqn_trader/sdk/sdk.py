"""Single entry point for data, training, evaluation, and inference."""

from pathlib import Path

import torch

from dqn_trader.config.manager import ConfigManager
from dqn_trader.data.client import YFinanceDataClient
from dqn_trader.data.features import FeatureEngineer
from dqn_trader.env.reward import RewardFunction
from dqn_trader.env.trading_env import TradingEnv
from dqn_trader.evaluation.backtest import BacktestResult, BacktestService, InferenceService
from dqn_trader.model.network import DuelingDQNNetwork
from dqn_trader.training.service import TrainingResult, TrainingService


class TradingSDK:
    def __init__(self, config_path: Path = Path("config/setup.yaml")) -> None:
        self.config = ConfigManager(config_path).load()

    def prepare_data(self, ticker: str | None = None):
        data_cfg = self.config["data"]
        feature_cfg = self.config["features"]
        ticker = ticker or data_cfg["ticker"]
        raw = YFinanceDataClient(Path(data_cfg["cache_dir"])).load_daily(
            ticker, data_cfg["start"], data_cfg["end"], data_cfg["interval"]
        )
        engineer = FeatureEngineer(feature_cfg["window_size"])
        features = engineer.transform(raw)
        split = self.config["split"]
        return (
            raw,
            features,
            engineer.chronological_split(features, split["train"], split["validation"]),
        )

    def make_env(self, features, raw, reward_mode: str = "risk_adjusted") -> TradingEnv:
        env_cfg = self.config["environment"]
        reward_cfg = self.config["reward"] if reward_mode == "risk_adjusted" else {}
        reward = RewardFunction(**reward_cfg)
        aligned_prices = raw.loc[features.index, "Close"]
        return TradingEnv(
            features, aligned_prices, self.config["features"]["window_size"], reward, **env_cfg
        )

    def train(
        self, ticker: str | None = None, reward_mode: str = "risk_adjusted"
    ) -> TrainingResult:
        raw, features, _splits = self.prepare_data(ticker)
        env = self.make_env(features, raw, reward_mode)
        checkpoint = Path(self.config["training"]["checkpoint_path"])
        return TrainingService(self.config["training"]).train(env, checkpoint)

    def backtest(
        self, ticker: str | None = None, output_dir: Path = Path("results")
    ) -> BacktestResult:
        raw, features, _splits = self.prepare_data(ticker)
        env = self.make_env(features, raw)
        model = self._load_model()
        result = BacktestService().run(env, model)
        BacktestService.save(result, output_dir)
        return result

    def predict_latest(self, ticker: str | None = None) -> tuple[int, list[float]]:
        raw, features, _splits = self.prepare_data(ticker)
        env = self.make_env(features, raw)
        model = self._load_model()
        return InferenceService.predict(model, env.reset())

    def _load_model(self) -> DuelingDQNNetwork:
        model = DuelingDQNNetwork(
            self.config["features"]["window_size"], self.config["features"]["feature_count"]
        )
        checkpoint = Path(self.config["training"]["checkpoint_path"])
        if checkpoint.exists():
            state = torch.load(checkpoint, map_location="cpu")
            model.load_state_dict(state["model_state"])
        return model
