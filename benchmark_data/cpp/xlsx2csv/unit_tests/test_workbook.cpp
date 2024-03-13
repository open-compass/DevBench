#include <gtest/gtest.h>

#include "workbook.h"
#include <fstream>
#include <unistd.h>
#include <string>
#include <iostream>

using namespace my_xlsx::xlsx_reader;

class WorkbookTest : public ::testing::Test {
public:
    void SetUp() override {
        filename = "./inputs/test001.xlsx";
        workbook_ = std::make_unique<workbook>(filename);
        // Initialize the workbook for testing.
    }

    void TearDown() override {
        workbook_.reset();
        // Clean up after testing.
    }

protected:

    bool compareCSVFiles(const std::string& file1, const std::string& file2) {
        std::ifstream csv1(file1), csv2(file2);
        if (!csv1.is_open() || !csv2.is_open()) {
            return false;
        }

        std::string line1, line2;
        while (true) {
            bool gotLine1 = static_cast<bool>(std::getline(csv1, line1));
            bool gotLine2 = static_cast<bool>(std::getline(csv2, line2));

            // If one file ended but the other didn't, they're not the same
            if (gotLine1 != gotLine2) return false;

            // If both files ended, they're the same
            if (!gotLine1 && !gotLine2) return true;

            // Compare the two lines
            if (line1 != line2) return false;
        }
    }

    bool compareCSVString(const std::string& file, const std::string& str) {
        std::ifstream csv(file);

        std::string line;
        std::string csv_string = "";
        while (true) {
            bool gotLine = static_cast<bool>(std::getline(csv, line));
            if (!gotLine) break;
            csv_string += line;
        }
        std::cout << csv_string << std::endl;
        std::cout << str << std::endl;
        return (csv_string == str);
    }

    std::unique_ptr<workbook> workbook_;
    std::string filename;
};

TEST_F(WorkbookTest, GetSharedString) {
    std::string shared_string_0 = workbook_->get_shared_string(0);
    std::string shared_string_1 = workbook_->get_shared_string(1);
    std::string shared_string_2 = workbook_->get_shared_string(2);
    std::string shared_string_3 = workbook_->get_shared_string(3);
    std::string shared_string_4 = workbook_->get_shared_string(4);
    std::string shared_string_5 = workbook_->get_shared_string(5);
    std::string shared_string_6 = workbook_->get_shared_string(6);
    std::string shared_string_7 = workbook_->get_shared_string(7);
    std::string shared_string_8 = workbook_->get_shared_string(8);
    std::string shared_string_9 = workbook_->get_shared_string(9);
    std::string shared_string_10 = workbook_->get_shared_string(10);
    std::string shared_string_11 = workbook_->get_shared_string(11);
    std::string shared_string_12 = workbook_->get_shared_string(12);
    std::string shared_string_13 = workbook_->get_shared_string(13);
    std::string shared_string_14 = workbook_->get_shared_string(14);
    std::string shared_string_15 = workbook_->get_shared_string(15);
    std::string shared_string_16 = workbook_->get_shared_string(16);
    std::string shared_string_17 = workbook_->get_shared_string(17);
    std::string shared_string_18 = workbook_->get_shared_string(18);
    
    // Check that the shared strings are correct.
    ASSERT_EQ(shared_string_0, "");
    ASSERT_EQ(shared_string_1, "column 1");
    ASSERT_EQ(shared_string_2, "column_2");
    ASSERT_EQ(shared_string_3, "c3");
    ASSERT_EQ(shared_string_4, "test endl");
    ASSERT_EQ(shared_string_5, "document");
    ASSERT_EQ(shared_string_6, "1");
    ASSERT_EQ(shared_string_7, "2");
    ASSERT_EQ(shared_string_8, "3");
    ASSERT_EQ(shared_string_9, "6");
    ASSERT_EQ(shared_string_10, "5");
    ASSERT_EQ(shared_string_11, "4");
    ASSERT_EQ(shared_string_12, "7");
    ASSERT_EQ(shared_string_13, "8");
    ASSERT_EQ(shared_string_14, "999");
    ASSERT_EQ(shared_string_15, "111");
    ASSERT_EQ(shared_string_16, "222");
    ASSERT_EQ(shared_string_17, "333");
    ASSERT_EQ(shared_string_18, "444");

}

TEST_F(WorkbookTest, WriteToCSV) {
    std::string output_path = "./outputs/test001";
    std::string gold_path = "./expected_outputs/test001";
    workbook_->write_to_csv(output_path);

    ASSERT_TRUE(compareCSVFiles(output_path + "/Sheet1.csv", gold_path + "/Sheet1.csv"));
    ASSERT_TRUE(compareCSVFiles(output_path + "/testsheet.csv", gold_path + "/testsheet.csv"));
    ASSERT_TRUE(compareCSVFiles(output_path + "/s3.csv", gold_path + "/s3.csv"));
}
