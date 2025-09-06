MANAGE = python manage.py
WORKER = celery -A config worker -l info

collect_static:
	$(MANAGE) collectstatic --noinput

migrate:
	$(MANAGE) migrate --noinput

init:
	$(MANAGE) init_project

server:
	python -m daphne -b 0.0.0.0 -p 8000 config.asgi:application

beat:
	celery -A config beat

worker_trade:
	$(WORKER) -Q trade

worker_warehouse:
	$(WORKER) -Q warehouse -c 1

worker_jokes:
	$(WORKER) -Q jokes

worker_audit:
	$(WORKER) -Q audit -c 1

worker_balance:
	$(WORKER) -Q balance