# Makefile fallback — para ambientes sem CMake.
# Build equivalente ao CMakeLists.txt. Saida: ./valen
#
#   make            # compila
#   make run        # compila e roda 'valen stats' na raiz do vault
#   make clean

CXX      ?= g++
CXXFLAGS ?= -std=c++20 -O2 -Wall -Wextra -Iinclude
SRC      := src/main.cpp src/vault_engine.cpp src/note.cpp src/link_resolver.cpp src/indexer.cpp
BIN      := valen

.PHONY: all run clean

all: $(BIN)

$(BIN): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(BIN)

run: $(BIN)
	cd .. && core/$(BIN) stats

clean:
	rm -f $(BIN)
