#include <gtest/gtest.h>
#include "Rectangle.h"
#include <math.h>

class TestRectangle : public ::testing::Test {
public:
    void SetUp() override {

    }

    void TearDown() override {

    }

    protected:
};

TEST_F(TestRectangle, CalcArea) {
    Rectangle rectangle(4.0, 5.0);
    ASSERT_TRUE(fabs(rectangle.calcArea() - 20.0) < 0.001);
    Rectangle rectangle_1;
    ASSERT_TRUE(fabs(rectangle_1.calcArea() - 0.0) < 0.001);
}