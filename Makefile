DC=/home/w0rp/bin/arm-none-eabi-gdc/bin/arm-none-eabi-gdc
DRUNTIME=/home/w0rp/git/personal/pebble-druntime/src
DPEBBLE=/home/w0rp/git/personal/dpebble/src
DFLAGS=-mthumb -mcpu=cortex-m4 -fno-emit-moduleinfo -fdata-sections -fno-exceptions
LDFLAGS=
SOURCES=src/app.d
ODIR=obj
OBJECTS=obj/app.o
LIBRARY=lib/libpebbleapp.a

all: $(SOURCES) $(LIBRARY)

$(LIBRARY): lib obj $(OBJECTS)
	ar -cvq $(LIBRARY) $(OBJECTS)

lib:
	mkdir lib

obj:
	mkdir obj

obj/app.o: obj
	$(DC) -I $(DRUNTIME) -I $(DPEBBLE) $(DFLAGS) -c src/app.d -o $@

clean:
	rm $(LIBRARY) $(OBJECTS)

