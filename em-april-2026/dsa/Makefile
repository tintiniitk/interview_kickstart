CXX      := g++
CXXFLAGS := -Wall -Wextra
GO       := go
JAVAC    := javac

# Default debug to 'on' if not specified (e.g., make debug=off)
debug ?= on

ifeq ($(debug),off)
    CXXFLAGS += -O2
    GOFLAGS  :=
    JFLAGS   := -g:none
else
    CXXFLAGS += -g -O0
    GOFLAGS  := -gcflags="all=-N -l"
    JFLAGS   := -g
endif

.PHONY: all cpp go java python py clean

# Default fallback: python > cpp > go > java
all:
	@if [ -f main.py ]; then \
		$(MAKE) python debug=$(debug); \
	elif [ -f main.cpp ]; then \
		$(MAKE) cpp debug=$(debug); \
	elif [ -f main.go ]; then \
		$(MAKE) go debug=$(debug); \
	elif [ -f main.java ] || [ -f Main.java ]; then \
		$(MAKE) java debug=$(debug); \
	else \
		echo "Error: No supported main file found (main.py, main.cpp, main.go, main.java/Main.java)"; \
		exit 1; \
	fi

cpp:
	@if [ ! -f main.cpp ]; then echo "Error: main.cpp does not exist"; exit 1; fi
	$(CXX) $(CXXFLAGS) main.cpp -o main

go:
	@if [ ! -f main.go ]; then echo "Error: main.go does not exist"; exit 1; fi
	$(GO) build $(GOFLAGS) -o main main.go

java:
	@if [ -f Main.java ]; then \
		$(JAVAC) $(JFLAGS) Main.java && printf '#!/bin/sh\nexec java Main "$$@"\n' > main && chmod +x main; \
	elif [ -f main.java ]; then \
		$(JAVAC) $(JFLAGS) main.java && printf '#!/bin/sh\nexec java main "$$@"\n' > main && chmod +x main; \
	else \
		echo "Error: main.java or Main.java does not exist"; exit 1; \
	fi

python py:
	@if [ ! -f main.py ]; then echo "Error: main.py does not exist"; exit 1; fi
	@printf '#!/bin/sh\ncd ..\ncd -\nexec python3 main.py "$$@"\n' > main && chmod +x main

clean:
	rm -f main *.class