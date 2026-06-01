# PRD: Trading Environment

## Requirement
The environment must expose clear Gymnasium-like `reset()` and `step(action)` behavior while staying independent of GUI, model, and training code.

## Behavior
- State is a rolling `(30, 10)` feature window.
- Actions are exactly `SELL=0`, `HOLD=1`, `BUY=2`.
- Positions are all-in/all-out for educational clarity.
- Invalid active actions receive `invalid_action_penalty`.
- `step()` returns `(next_state, reward, done, info)`.

## Acceptance Tests
- `reset()` returns the correct state shape.
- `SELL` without a position is penalized.
- Portfolio value remains available in the `info` dictionary.
