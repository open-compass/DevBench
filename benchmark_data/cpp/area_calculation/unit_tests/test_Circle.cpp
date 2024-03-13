#include <gtest/gtest.h>
#include "Circle.hpp"
#include <math.h>

class TestCircle : public ::testing::Test {
public:
    void SetUp() override {

    }

    void TearDown() override {

    }

    protected:
};

TEST_F(TestCircle, CalcArea) {
    Circle circle(5.0);
    ASSERT_TRUE(fabs(circle.calcArea() - 3.14159 * 5.0 * 5.0) < 0.001);
}