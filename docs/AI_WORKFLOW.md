# AI-Assisted Workflow

## How AI Was Used
AI assistance was used to parse the assignment requirements, design a compact SDK-based architecture, generate initial code and tests, and perform an audit pass against the homework and professional-submission checklist.

## Prompt Categories
- Requirements extraction from homework and lecture material.
- Architecture planning for SDK, data, environment, model, training, evaluation, and GUI layers.
- Test planning for data fallback, feature shape, environment behavior, replay buffer, network forward pass, training, checkpointing, and SDK flow.
- Documentation drafting for README, PRD, PLAN, TODO, and mechanism-specific PRDs.
- Audit prompts focused on configuration, security, research analysis, cost/resource awareness, and extensibility.

## Manual Review
The generated implementation was reviewed by running Ruff and pytest with coverage. Obvious gaps found during review were fixed, including richer backtest metrics and clearer documentation that no real experiments have been run yet.

## Limitations
AI-generated code can miss edge cases, overstate completeness, or produce plausible but unverified explanations. For that reason, this repository includes tests, explicit known limitations, and placeholder experiment documentation rather than fabricated results.
