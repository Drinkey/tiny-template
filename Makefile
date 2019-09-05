test:
	pytest --cov-config .coveragerc -vv --cov-report term --cov-report xml --cov=src/ tests/*

report:
	coverage html && open htmlcov/index.html  