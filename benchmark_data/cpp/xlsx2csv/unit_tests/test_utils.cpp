#include <gtest/gtest.h>

#include "utils.h"

using namespace my_xlsx::xlsx_reader;

class UtilsTest : public ::testing::Test {
public:
    void SetUp() override {
    }

    void TearDown() override {
    }

protected:

};

TEST_F(UtilsTest, StringToIdx) {
    std::uint32_t idx1 = string_to_idx("A");
    std::uint32_t idx2 = string_to_idx("B");
    std::uint32_t idx3 = string_to_idx("C");

    ASSERT_EQ(idx1, 1);
    ASSERT_EQ(idx2, 2);
    ASSERT_EQ(idx3, 3);
}

TEST_F(UtilsTest, StringToRowColumn) {
    std::pair<std::uint32_t, std::uint32_t> row_column1 = string_to_row_column("A1");
    std::pair<std::uint32_t, std::uint32_t> row_column2 = string_to_row_column("B2");
    std::pair<std::uint32_t, std::uint32_t> row_column3 = string_to_row_column("C3");

    ASSERT_EQ(row_column1.first, 1);
    ASSERT_EQ(row_column1.second, 1);
    ASSERT_EQ(row_column2.first, 2);
    ASSERT_EQ(row_column2.second, 2);
    ASSERT_EQ(row_column3.first, 3);
    ASSERT_EQ(row_column3.second, 3);
}

TEST_F(UtilsTest, Strip) {
    std::string stripped1 = strip("  A\t");
    std::string stripped2 = strip(" \nB  ");

    ASSERT_EQ(stripped1, "A");
    ASSERT_EQ(stripped2, "B");
}