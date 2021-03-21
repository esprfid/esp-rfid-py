MICROPYTHON_IMAGE=dcmorton/esp32-micropython-image-builder:local
FLASHING_PORT=cu.usbserial-1420

run-docker-build:
	docker run -it --rm -v ${PWD}:/app --workdir /app $(MICROPYTHON_IMAGE) make build-firmware

build-firmware:
	cp -R lib/* src/modules/* /data/micropython/ports/esp32/modules
	cd /data/micropython/ports/esp32 && make
	mv /data/micropython/ports/esp32/build-GENERIC/firmware.bin /app

flash: firmware.bin
	esptool.py -p /dev/$(FLASHING_PORT) erase_flash
	esptool.py -p /dev/$(FLASHING_PORT) write_flash -z 0x1000 firmware.bin

copyfiles:
	sleep 2
	mpfshell -o $(FLASHING_PORT) -c 'lcd src; mput ^(?!example).*\.py; put networks.json; repl'

repl:
	mpfshell -o $(FLASHING_PORT) -c repl

install: run-docker-build flash copyfiles
