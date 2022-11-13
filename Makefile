all: build

build:
	podman run --rm -v ${PWD}:/opt docker://docker.io/tonsky/firacode:latest ./script/build.sh

package:
	./script/package.sh
