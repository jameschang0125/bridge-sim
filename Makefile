CC_BOOST_LINK	= -I /home/James_Chang/install/boost/include/ -L /home/James_Chang/install/boost/lib/

THREAD_COMPILE	= -fopenmp $(THREAD_LINK)
THREAD_LINK	= $(CC_BOOST_LINK)


COMPILE_FLAGS	= -O3 -flto -fopenmp -mtune=generic -std=c++11 \
		$(WARN_FLAGS) $(THREAD_COMPILE)

CC = g++ $(COMPILE_FLAGS)
TEST_FLAGS = -fsanitize=address
LIB = libdds.a -lboost_system -lboost_thread -lpthread

# TODO: sep compile
LIBFILES = dll.h libdds.a portab.h
OFILES = main.o gen.o

all: $(OFILES)
	$(CC) -o main $(OFILES) $(LIB)

gen: $(LIBFILES) gen.cpp gen.hpp
	$(CC) -c gen.cpp

main: $(LIBFILES) gen.hpp
	$(CC) -c main.cpp
test: 
	$(CC) $(TEST_FLAGS) -o main main.cpp gen.cpp $(LIB) && clear && time ./main

.PHONY: clean
clean:
	rm main *.o dump.txt