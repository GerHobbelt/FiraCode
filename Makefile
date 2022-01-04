DOCKER_TAG := firacode-builder:3.10.1-bullseye

all: dep build

.PHONY: dep
dep:
	docker build --progress plain -t $(DOCKER_TAG) ./docker

.PHONY: build
build:
	docker run --rm -v ${PWD}:/opt -e DK_UID=$(shell id -u) -e DK_GID=$(shell id -g) $(DOCKER_TAG) ./script/build.sh
