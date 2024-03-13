# Variables
CXX = g++
CC = gcc   # Adding a variable for the C compiler
CXXFLAGS = -std=c++17 -Iinclude
CFLAGS = -Iinclude  # Flags for C compilation
SRCDIR = src
INCDIR = include
OBJS = $(SRCDIR)/main.o $(SRCDIR)/account.o  $(SRCDIR)/expressage.o $(SRCDIR)/logistics.o
TARGET = logistics

# Default target
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(SRCDIR)/%.o: $(SRCDIR)/%.cpp $(INCDIR)/%.h
	$(CXX) $(CXXFLAGS) -c -o $@ $<

$(SRCDIR)/main.o: $(SRCDIR)/main.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
