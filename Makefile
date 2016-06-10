CC = gcc
CXX = g++
SWIG = swig
CFLAGS = -g $(shell pkg-config --cflags python3)
# For warnings
#CFLAGS += -Wall -Wextra
# Disable optimisations
#CFLAGS += -O0
LDFLAGS = $(shell pkg-config --cflags --libs python3)

all: _partitionize.so

%.o: %.c
	$(CC) $(CFLAGS) -fPIC -c $<

%_wrap.c: %.i
	$(SWIG) -python -py3 $<

_%.so: %.o %_wrap.o 
	$(CC) -shared $(LDFLAGS) $+ -o $@
clean:
	rm -r *.o  *_wrap.c
	
