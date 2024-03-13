#include <gtest/gtest.h>
#include <iostream>

#include "archive.h"

using namespace my_xlsx::xlsx_reader;

class ArchiveTest : public ::testing::Test {
public:
    void SetUp() override {
        // Initialize the archive for testing.
        filename = "./inputs/test001.xlsx";
        archive_ = std::make_unique<archive>(filename);
    }

    void TearDown() override {
        // Clean up after testing.
        archive_.reset();
    }

protected:
    std::unique_ptr<archive> archive_;
    std::string filename;
};

TEST_F(ArchiveTest, GetSheetRelations) {
    std::vector<sheet_desc> sheet_relations = archive_->get_sheet_relations();
    // Check that the sheet relations are not empty.
    ASSERT_FALSE(sheet_relations.empty());
}

TEST_F(ArchiveTest, GetSheetXML) {
    std::shared_ptr<tinyxml2::XMLDocument> sheet_xml = archive_->get_sheet_xml("xl/worksheets/sheet1.xml");
    // Check that the sheet XML is not null.
    ASSERT_NE(sheet_xml, nullptr);
}

TEST_F(ArchiveTest, GetSharedStrings) {
    std::vector<std::string> shared_strings = archive_->get_shared_strings();
    // Check that the shared strings are not empty.
    ASSERT_FALSE(shared_strings.empty());
}