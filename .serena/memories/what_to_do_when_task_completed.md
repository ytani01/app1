# What to do when a task is completed

When a task is completed, ensure the following steps are performed to maintain code quality and project standards:

1.  **Run Tests:** Execute `uv run pytest` to ensure all existing tests pass and no regressions have been introduced.
2.  **Run Linter:** Execute `uv run ruff check .` to identify and fix any linting issues.
3.  **Run Formatter:** Execute `uv run ruff format .` to ensure the code adheres to the project's formatting guidelines.
4.  **Run Type Checker:** Execute `uv run mypy src/` to verify type consistency and catch potential type-related bugs.
5.  **Commit Changes:** Commit your changes with a clear and concise commit message.
