MICROPYTHON_VERSION=v2.11.0.2
FLASHING_PORT=cu.usbserial

run-docker:
	docker run -it --rm -v ${PWD}:/app registry.gitlab.com/janpoboril/micropython-docker-build/pycopy/esp8266:$(MICROPYTHON_VERSION) make build-firmware

build-firmware:
	cp -R lib/* src/modules/* /micropython/ports/esp8266/modules
	cd /micropython/ports/esp8266 && make
	mv /micropython/ports/esp8266/build/firmware-combined.bin /app

install: firmware-combined.bin
	esptool.py -p /dev/$(FLASHING_PORT) erase_flash
	esptool.py -p /dev/$(FLASHING_PORT) -b 115200 write_flash 0 firmware-combined.bin
	mpfshell -o $(FLASHING_PORT) -c lcd src; put main.py; put config.py; put networks.json; put webrepl_cfg.py
