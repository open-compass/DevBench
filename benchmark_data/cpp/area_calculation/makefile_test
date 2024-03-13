# gcov
COVFLAGS = -fprofile-arcs -ftest-coverage

# Variables
CXX = g++
CXXFLAGS = -std=c++17 -Iinclude
CFLAGS = -Iinclude  # Flags for C compilation
SRCDIR = src
INCDIR = include
INCDIR_TEST = .
OBJS = $(SRCDIR)/main.o $(SRCDIR)/Shape.o $(SRCDIR)/Rectangle.o
TARGET = area_calculation

TEST_DIR = ./unit_tests
TEST_OBJS = ${TEST_DIR}/test_Circle.o ${TEST_DIR}/test_Rectangle.o ${TEST_DIR}/test_Square.o
TEST_TARGET = run_tests
GTEST_LIB = -lgtest -lgtest_main -pthread

# Default target
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(COVFLAGS) -o $@ $^ -lgcov 

$(SRCDIR)/%.o: $(SRCDIR)/%.cpp $(INCDIR)/%.h
	$(CXX) $(CXXFLAGS) $(COVFLAGS) -c -o $@ $<

$(SRCDIR)/main.o: $(SRCDIR)/main.cpp
	$(CXX) $(CXXFLAGS) $(COVFLAGS) -c -o $@ $<

# Test targets

PROD_OBJS = $(filter-out $(SRCDIR)/main.o, $(OBJS))

$(TEST_TARGET): $(PROD_OBJS) $(TEST_OBJS)
	$(CXX) $(CXXFLAGS) $(COVFLAGS) -o $@ $^ $(GTEST_LIB) -lgcov

$(TESTDIR)/%.o: $(TESTDIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(COVFLAGS) -c -o $@ $<

test: $(TEST_TARGET)
	./$(TEST_TARGET)

coverage: test
	gcov -r -b $(SRCDIR)/Rectangle.cpp $(SRCDIR)/Shape.cpp

clean:
	rm -f $(OBJS) $(TARGET) $(TEST_TARGET) $(TEST_OBJS) src/*.gcda src/*.gcno src/*.gcov *.gcda *.gcno *.gcov unit_tests/*.gcda unit_tests/*.gcno unit_tests/*.gcov

.PHONY: all clean
