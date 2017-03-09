PACKAGE_NAME=flashpolicies
TESTING_VIRTUALENV_NAME=${PACKAGE_NAME}_test

ifndef PYTHON_VERSION
PYTHON_VERSION=3.6.0
endif

ifndef DJANGO_VERSION
DJANGO_VERSION=1.10
endif

.PHONY: clean
clean:
	python setup.py clean
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg*/
	rm -rf ${PACKAGE_NAME}/__pycache__/
	rm -rf ${PACKAGE_NAME}/tests/__pycache__/
	find ${PACKAGE_NAME} -type f -name '*.pyc' -delete
	rm -f MANIFEST
	rm -rf coverage .coverage .coverage*
	pip uninstall -y Django

.PHONY: env
env:
	[ -e ~/.pyenv/versions/${TESTING_VIRTUALENV_NAME} ] && echo "Skipping pyenv creation" || pyenv virtualenv ${PYTHON_VERSION} ${TESTING_VIRTUALENV_NAME}
	pyenv local ${TESTING_VIRTUALENV_NAME}
	pip install --upgrade pip setuptools
	pip install -e .

.PHONY: teardown
teardown: clean
	pyenv uninstall -f ${TESTING_VIRTUALENV_NAME}
	rm .python-version

.PHONY: django
django:
	pip install Django~=${DJANGO_VERSION}.0

.PHONY: test_deps
test_deps:
	pip install -r test_requirements.txt

.PHONY: lint
lint: test_deps
	flake8 ${PACKAGE_NAME}

.PHONY: test
test: django test_deps
	coverage run ${PACKAGE_NAME}/runtests.py
	coverage report -m
