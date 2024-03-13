# Variables
CXX = g++
CC = gcc   # Adding a variable for the C compiler
CXXFLAGS = -std=c++17 -Iinclude
CFLAGS = -Iinclude  # Flags for C compilation
SRCDIR = src
INCDIR = include
OBJS = $(SRCDIR)/archive.o $(SRCDIR)/miniz.c.o $(SRCDIR)/tinyxml2.o $(SRCDIR)/utils.o $(SRCDIR)/workbook.o $(SRCDIR)/worksheet.o $(SRCDIR)/main.o
TARGET = xlsx2csv

# Default target
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(SRCDIR)/%.o: $(SRCDIR)/%.cpp $(INCDIR)/%.h
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# Add a rule for miniz.c
$(SRCDIR)/miniz.c.o: $(SRCDIR)/miniz.c
	$(CC) $(CFLAGS) -c -o $@ $<

# Add a rule for tinyxml2.cpp
$(SRCDIR)/tinyxml2.o: $(SRCDIR)/tinyxml2.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

$(SRCDIR)/main.o: $(SRCDIR)/main.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
