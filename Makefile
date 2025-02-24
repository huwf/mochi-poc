.PHONY : init compile-reqs install docker-build docker-build-dev docker-build-prod compose-up compose-down

PYMAIN=/usr/bin/python3

VENV=./.venv
PYBIN=${VENV}/bin/python
PIPBIN=${VENV}/bin/pip
TARGET=dev


init:
	${PYMAIN} -m venv ${VENV}
	${PYBIN} -m pip install --upgrade pip pip-tools

compile-reqs:
	${PYBIN} -m piptools compile \
	--extra dev \
	-o requirements.txt pyproject.toml && \
	${PIPBIN} install -r requirements.txt


install:
	${PYBIN} -m pip install -r requirements.txt -e .

docker-build:
	DOCKER_BUILDKIT=1 docker build --target=${TARGET} -t huwf/dictogloss:${TARGET} .


docker-build-dev:
	make docker-build TARGET=dev

docker-build-prod:
	make docker-build TARGET=prod

compose-up:
	docker-compose up

compose-down:
	docker-compose down