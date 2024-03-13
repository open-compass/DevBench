#include <common.h>
#include <people_management.h>
#include <utils.h>

#include <gtest/gtest.h>

// Mock database file
const char* test_db_name = "test_database.sqlite3";

class PeopleManagementTest : public testing::Test {
protected:
    PeopleManagementTest() {}
    virtual ~PeopleManagementTest() {}
    virtual void SetUp() {
        people_management = new PeopleManagement();
    }
    virtual void TearDown() {
        delete people_management;
        system("rm database.sqlite3");
    }

public:
    PeopleManagement* people_management;
};

TEST_F(PeopleManagementTest, TEST_CONTAINS) {
    std::vector<std::string> values = {"value1", "value2"};
    std::string value = "value1";
    EXPECT_TRUE(contains(values, value));
    value = "value3";
    EXPECT_FALSE(contains(values, value));
}

TEST_F(PeopleManagementTest, TEST_VALIDATE_OPTIONS) {
    EXPECT_FALSE(validate_options("subcommand", "target"));
    EXPECT_TRUE(validate_options("mentor", "assign"));
    EXPECT_TRUE(validate_options("mentor", "lookup"));
    EXPECT_FALSE(validate_options("mentor", "target"));
    EXPECT_FALSE(validate_options("add", "target"));
    EXPECT_TRUE(validate_options("add", "person"));
}

TEST_F(PeopleManagementTest, TEST_BUILD_OPTIONS) {
    ASSERT_DEATH( {build_options({"add", "person", "-name", "-age", "30"}); }, "Option -name does not have a value\n");
    ASSERT_DEATH( {build_options({"add", "person", "-name", "John", "-age"}); }, "Option -age does not have a value\n");
    ASSERT_DEATH( {build_options({"add", "person", "name", "-age", "30"}); }, "Option name does not start with '-'\n");
    ASSERT_DEATH( {build_options({"add", "person"}); }, "Odd number of arguments\n");
    std::map<std::string, std::string> options = build_options({"add", "person", "-name", "John", "-age", "30"});
    EXPECT_EQ(options["-name"], "John");
    EXPECT_EQ(options["-age"], "30");
}

TEST_F(PeopleManagementTest, TEST_HANDLE_OPTIONS) {
    EXPECT_EQ(handle_options("invalid", "", {}, *people_management), INVALID_OPTION);

    std::string subcommand = "add";
    std::string target = "school";
    std::map<std::string, std::string> options = {{"-name", "Maths"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), SUCCESS);

    subcommand = "add";
    target = "school";
    options = {{"-n", "Maths"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), FAILURE);

    subcommand = "add";
    target = "person";
    options = {{"-name", "John"}, {"-age", "30"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), FAILURE);

    options["-school"] = "1";
    options["-type"] = "1";
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), SUCCESS);

    subcommand = "search";
    target = "school";
    options = {{"-name", "Math"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), SUCCESS);

    subcommand = "search";
    target = "school";
    options = {{"-n", "Math"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), FAILURE);

    subcommand = "delete";
    target = "school";
    options = {{"-n", "Math"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), FAILURE);

    subcommand = "update";
    target = "school";
    options = {{"-n", "Math"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), FAILURE);

    subcommand = "update";
    target = "school";
    options = {{"-id", "1"}, {"-name", "Arts"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), SUCCESS);

    subcommand = "add";
    target = "person";
    options = {{"-name", "Tom"}, {"-age", "50"}, {"-school", "1"}, {"-type", "2"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), SUCCESS);

    subcommand = "mentor";
    target = "assign";
    options = {{"-student", "1"}, {"-mentor", "2"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), SUCCESS);

    subcommand = "mentor";
    target = "assign";
    options = {{"-student", "3"}, {"-mentor", "2"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), FAILURE);

    subcommand = "delete";
    target = "school";
    options = {{"-id", "1"}};
    EXPECT_EQ(handle_options(subcommand, target, options, *people_management), SUCCESS);
}

TEST_F(PeopleManagementTest, TEST_ADD) {
    std::map<std::string, std::string> options;

    options = {{"-n", "Tim"}};
    EXPECT_EQ(people_management->add("person", options), INVALID_OPTION);

    options = {{"-name", "Tim"}, {"-age", "30"}};
    EXPECT_EQ(people_management->add("person", options), NOT_ENOUGH_OPTIONS);

    options = {{"-name", "Tim"}, {"-age", "30"}, {"-school", "999"}, {"-type", "1"}};
    EXPECT_EQ(people_management->add("person", options), RECORD_NOT_EXISTS);

    options = {};
    EXPECT_EQ(people_management->add("school", options), NOT_ENOUGH_OPTIONS);

    options = {{"-name", "Physics"}};
    EXPECT_EQ(people_management->add("school", options), SUCCESS);

    options = {{"-name", "Tim"}, {"-age", "30"}, {"-school", "1"}, {"-type", "1"}};
    EXPECT_EQ(people_management->add("person", options), SUCCESS);

    options = {{"-name", "David"}, {"-age", "30"}, {"-school", "1"}, {"-type", "2"}};
    EXPECT_EQ(people_management->add("person", options), SUCCESS);
}

TEST_F(PeopleManagementTest, TEST_SEARCH) {
    std::string target;
    std::map<std::string, std::string> options;

    EXPECT_EQ(people_management->search(target, options), NOT_ENOUGH_OPTIONS);

    target = "person";
    options = {{"-n", "Tim"}};
    EXPECT_EQ(people_management->search(target, options), INVALID_OPTION);

    options = {{"-name", "David"}};
    EXPECT_EQ(people_management->search(target, options), SUCCESS);

    options = {{"-type", "1"}};
    EXPECT_EQ(people_management->search(target, options), SUCCESS);

    target = "school";
    options = {{"-n", "Physics"}};
    EXPECT_EQ(people_management->search(target, options), INVALID_OPTION);

    options = {{"-name", "Physics"}};
    EXPECT_EQ(people_management->search(target, options), SUCCESS);

    options = {{"-id", "1"}};
    EXPECT_EQ(people_management->search(target, options), SUCCESS);

    options = {{"-id", "1"}, {"-name", "Physics"}};
    EXPECT_EQ(people_management->search(target, options), SUCCESS);
}

TEST_F(PeopleManagementTest, TEST_DELETE) {
    std::string target;
    std::map<std::string, std::string> options;

    EXPECT_EQ(people_management->delete_record(target, options), NOT_ENOUGH_OPTIONS);

    target = "person";
    options = {{"-id", "10000"}};
    EXPECT_EQ(people_management->delete_record(target, options), RECORD_NOT_EXISTS);

    target= "school";
    options = {{"-id", "100000"}};
    EXPECT_EQ(people_management->delete_record(target, options), RECORD_NOT_EXISTS);

    options = {{"-name", "Physics"}};
    handle_options("add", "school", options, *people_management);
    options = {{"-name", "David"}, {"-age", "30"}, {"-school", "1"}, {"-type", "1"}};
    handle_options("add", "person", options, *people_management);

    target = "person";
    options = {{"-id", "1"}};
    EXPECT_EQ(people_management->delete_record(target, options), SUCCESS);

    target = "school";
    options = {{"-id", "1"}};
    EXPECT_EQ(people_management->delete_record(target, options), SUCCESS);
}

TEST_F(PeopleManagementTest, TEST_UPDATE) {
    std::string target = "person";
    std::map<std::string, std::string> options = {{"-name", "David"}};

    EXPECT_EQ(people_management->update(target, options), NOT_ENOUGH_OPTIONS);

    options = {{"-name", "Physics"}};
    handle_options("add", "school", options, *people_management);
    options = {{"-name", "David"}, {"-age", "30"}, {"-school", "1"}, {"-type", "1"}};
    handle_options("add", "person", options, *people_management);

    options = {{"-id", "1"}, {"-mate", "David"}, {"-age", "30"}, {"-school", "1"}, {"-type", "1"}};
    EXPECT_EQ(people_management->update(target, options), INVALID_OPTION);

    options = {{"-id", "1"}};
    EXPECT_EQ(people_management->update(target, options), NOT_ENOUGH_OPTIONS);

    options = {{"-id", "1"}, {"-age", "30"}, {"-school", "1000"}, {"-type", "1"}};
    EXPECT_EQ(people_management->update(target, options), RECORD_NOT_EXISTS);

    options = {{"-id", "1"}, {"-name", "Joe"}, {"-age", "30"}, {"-school", "1"}, {"-type", "1"}};
    EXPECT_EQ(people_management->update(target, options), SUCCESS);
    
    target = "school";
    options = {{"-id", "1"}, {"-name", "Physics"}};
    EXPECT_EQ(people_management->update(target, options), SUCCESS);

    options = {{"-id", "1"}};
    EXPECT_EQ(people_management->update(target, options), NOT_ENOUGH_OPTIONS);
}

TEST_F(PeopleManagementTest, TEST_MENTOR) {
    std::string target;
    std::map<std::string, std::string> options;

    options = {{"-name", "Physics"}};
    handle_options("add", "school", options, *people_management);
    options = {{"-name", "David"}, {"-age", "30"}, {"-school", "1"}, {"-type", "1"}};
    handle_options("add", "person", options, *people_management);
    options = {{"-name", "Tom"}, {"-age", "30"}, {"-school", "1"}, {"-type", "2"}};
    handle_options("add", "person", options, *people_management);

    options = {{"-student", "1000"}, {"-mentor", "2"}};
    EXPECT_EQ(people_management->mentor(target, options), RECORD_NOT_EXISTS);

    options = {{"-student", "1"}, {"-mentor", "1000"}};
    EXPECT_EQ(people_management->mentor(target, options), RECORD_NOT_EXISTS);

    target = "assign";
    options = {{"-student", "1"}, {"-mentor", "2"}};
    EXPECT_EQ(people_management->mentor(target, options), SUCCESS);

    options = {{"-student", "1"}, {"-mentor", "2"}};
    EXPECT_EQ(people_management->mentor(target, options), SUCCESS);

    options = {{"-student", "1"}};
    EXPECT_EQ(people_management->mentor(target, options), NOT_ENOUGH_OPTIONS);

    target = "lookup";
    options = {{"-student", "1"}, {"-mentor", "2"}};
    EXPECT_EQ(people_management->mentor(target, options), INVALID_OPTION);

    options = {{"-student", ""}, {"-mentor", ""}};
    EXPECT_EQ(people_management->mentor(target, options), NOT_ENOUGH_OPTIONS);

    options = {{"-student", "1"}};
    EXPECT_EQ(people_management->mentor(target, options), SUCCESS);

    options = {{"-mentor", "2"}};
    EXPECT_EQ(people_management->mentor(target, options), SUCCESS);
}


int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
