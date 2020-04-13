MICROPYTHON_IMAGE=registry.gitlab.com/janpoboril/micropython-docker-build/pycopy/esp8266:v3.0.6
FLASHING_PORT=cu.SLAB_USBtoUART

run-docker-build:
	docker run -it --rm -v ${PWD}:/app $(MICROPYTHON_IMAGE) make build-firmware

build-firmware:
	cp -R lib/* src/modules/* /micropython/ports/esp8266/modules
	cd /micropython/ports/esp8266 && make
	mv /micropython/ports/esp8266/build-GENERIC/firmware-combined.bin /app

flash: firmware-combined.bin
	read -n 1 -s -r -p "Reboot ESP to flashing mode and press any key"
	esptool.py -p /dev/$(FLASHING_PORT) erase_flash
	read -n 1 -s -r -p "Reboot ESP to flashing mode and press any key"
	esptool.py -p /dev/$(FLASHING_PORT) -b 115200 write_flash 0 firmware-combined.bin

copyfiles:
	read -n 1 -s -r -p "Reboot ESP to normal mode and press any key"
	mpfshell -o $(FLASHING_PORT) -c 'lcd src; mput ^(?!example).*\.py; put networks.json'

install: run-docker-build flash copyfiles
