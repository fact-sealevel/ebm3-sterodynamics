format:
	uv run ruff format

lint:
	uv run ruff check --fix --ignore E722,F841

validate: format lint