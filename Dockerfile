FROM python:3.12-slim-bookworm AS build

COPY . .
RUN python -m pip wheel --wheel-dir=/wheels -r requirements.txt .

FROM python:3.12-slim-bookworm AS prod

RUN useradd -ms /bin/bash user
WORKDIR /home/user
USER user

COPY --chown=user:user --from=build /wheels /tmp/wheels
COPY --chown=user:user Makefile .

RUN python -m pip install \
    --no-index \
    --find-links=/tmp/wheels \
    --no-cache-dir \
    dictogloss && \
    rm -rf /tmp/wheels

FROM python:3.12-slim-bookworm AS dev

RUN useradd -ms /bin/bash user && mkdir /home/user/app
WORKDIR /home/user/app
USER user

COPY --chown=user:user --from=build /wheels /tmp/wheels
COPY --chown=user:user src src
COPY --chown=user:user Makefile .
COPY --chown=user:user pyproject.toml .

RUN python -m pip install \
    --no-index \
    --find-links=/tmp/wheels \
    --no-cache-dir \
    -e .[dev] && \
    rm -rf /tmp/wheels