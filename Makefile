MICROPYTHON_VERSION=v1.10

run-docker:
	docker run -it --rm -v ${PWD}:/app registry.gitlab.com/janpoboril/micropython-docker-build/esp8266:$(MICROPYTHON_VERSION) make build-firmware

build-firmware:
	cp -R lib/* src/modules/* /micropython/ports/esp8266/modules
	cd /micropython/ports/esp8266 && make
	mv /micropython/ports/esp8266/build/firmware-combined.bin /app

install: firmware-combined.bin
	esptool.py erase_flash
	esptool.py -b 115200 write_flash 0 firmware-combined.bin
