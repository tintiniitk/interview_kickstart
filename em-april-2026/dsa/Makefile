CXX          := g++
CXXFLAGS     := -Wall -Wextra -pedantic
CPP_TARGET   := main
CPP_SRC      := main.cpp

# Default debug to 'on' if not specified on the command line
debug ?= on

# Configure flags based on debug choice
ifeq ($(debug),off)
    CXXFLAGS += -O2
else
    CXXFLAGS += -g -O0
endif

# Default target
all: $(CPP_TARGET)

$(CPP_TARGET): $(CPP_SRC)
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -fv $(CPP_TARGET)

.PHONY: all clean
