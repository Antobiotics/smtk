
setup:
	pip install pipenv
	pipenv lock
	pipenv install --dev


setup-dev: setup
	pipenv run python setup.py develop

install:
	pipenv install
	pipenv run python setup.py install

test:
	pipenv run pytest
