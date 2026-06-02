# AI-Assisted Workflow

## How AI Was Used
AI assistance was used to parse the assignment requirements, design a compact SDK-based architecture, generate implementation code, create tests, run audit passes, improve documentation, and respond to observed GUI/backtest issues. The project was not accepted blindly after generation: the outputs were reviewed through tests, linting, Git history, and manual sanity checks.

## Prompt Categories
- Requirements extraction from homework and lecture material.
- Architecture planning for SDK, data, environment, model, training, evaluation, and GUI layers.
- Test planning for data fallback, feature shape, environment behavior, replay buffer, network forward pass, training, checkpointing, and SDK flow.
- Documentation drafting for README, PRD, PLAN, TODO, and mechanism-specific PRDs.
- Audit prompts focused on configuration, security, research analysis, cost/resource awareness, and extensibility.
- GUI improvement prompts focused on making plots readable and giving the lecturer a one-click demonstration path.
- Debugging prompts focused on suspicious trade counts, latest-state prediction behavior, and adjusted-versus-raw price data.

## Manual Review
The generated implementation was reviewed by running Ruff and pytest with coverage. Issues found during review were fixed, including misleading training plots, invalid-action counting during backtest, latest prediction using the wrong state, and a data-cache risk where older adjusted OHLC values could be reused silently.

Manual checks also included comparing local cached AAPL prices against public Yahoo-style historical rows. That review found that the old cache contained adjusted values, so the data client was updated to request `auto_adjust=False` and use a new raw-cache filename.

## Evidence Files
- `docs/AI_CHAT_LOG.md` summarizes the main AI/user conversation steps and corrections.
- `docs/SOURCE_CONTROL.md` records the meaningful Git commits used as source-control evidence.
- `docs/ASSESSMENT_COVERAGE.md` maps feedback/checklist criteria to repository evidence.
- `docs/COST_ANALYSIS.md` documents API, compute, storage, AI-assistance, and scaling costs.

## Limitations
AI-generated code can miss edge cases, overstate completeness, or produce plausible but unverified explanations. For that reason, this repository includes tests, explicit known limitations, committed experiment artifacts, and documentation of failures instead of fabricated results.
