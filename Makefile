.PHONY: run test test-k lint format migrate makemigrations shell

run:
	uv run python backend/manage.py runserver

test:
	uv run pytest backend/

test-k:
	uv run pytest backend/ -k $(k)

lint:
	uv run ruff check backend/

format:
	uv run ruff format backend/

migrate:
	uv run python backend/manage.py migrate

makemigrations:
	uv run python backend/manage.py makemigrations

shell:
	uv run python backend/manage.py shell
