MANAGE = python manage.py
WORKER = celery -A config worker -l info

shell:
	$(MANAGE) shell

beat:
	celery -A config beat

worker_trade:
	$(WORKER) -q trade

worker_warehouse:
	$(WORKER) -q warehouse -c 1

worker_jokes:
	$(WORKER) -q jokes

worker_audit:
	$(WORKER) -q audit -c 1

worker_balance:
	$(WORKER) -q balance