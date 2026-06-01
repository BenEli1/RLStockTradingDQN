# PRD: Reward Function

## Requirement
The reward must reflect portfolio value change and must support comparison between a simple reward and a cost/risk adjusted reward.

## Variants
- Basic: normalized portfolio value change.
- Risk adjusted: value change minus transaction cost, slippage, and volatility penalty.

## Acceptance Tests
- Trading costs reduce reward for otherwise identical portfolio value changes.
- Invalid actions in the environment receive an additional penalty.
