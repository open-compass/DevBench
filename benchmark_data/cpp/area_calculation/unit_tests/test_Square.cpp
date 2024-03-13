#include <gtest/gtest.h>
#include "Square.hpp"
#include <math.h>

class TestSquare : public ::testing::Test {
public:
    void SetUp() override {
    }

    void TearDown() override {
    }

    protected:
};

TEST_F(TestSquare, CalcArea) {
    Square square(4.0);
    ASSERT_TRUE(fabs(square.calcArea() - 16.0) < 0.001);
}