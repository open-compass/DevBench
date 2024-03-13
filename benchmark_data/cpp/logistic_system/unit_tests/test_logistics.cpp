#include <gtest/gtest.h>
#include <filesystem>
#include <fstream>
#include "logistics.h"

void initDataFiles() {
    std::ofstream accountFile("data/account.txt");
    accountFile << "5\n";
    accountFile << "root_id root_pwd RootUser 1234567890 100 RootAddress 0\n";
    accountFile << "admin_id admin_pwd AdminUser 1234567890 100 AdminAddress 1\n";
    accountFile << "test_id_1 test_pwd TestUser1 1234567890 100 TestAddress1 2\n";
    accountFile << "test_id_2 test_pwd TestUser2 1234567890 100 TestAddress2 2\n";
    accountFile << "test_id_3 test_pwd TestUser3 1234567890 0 TestAddress3 2\n";
    accountFile.close();

    std::ofstream expressageFile("data/expressage.txt");
    expressageFile << "2\n";
    expressageFile << "test_expressage_id_1 test_id_1 test_id_2 2020-01-01 NULL 0 TestRemark\n";
    expressageFile << "test_expressage_id_2 test_id_1 test_id_2 2020-01-01 NULL 1 TestRemark\n";
    expressageFile.close();
}

void equalAccountNode(AccountNode a, AccountNode b) {
    EXPECT_EQ(a.id, b.id);
    EXPECT_EQ(a.password, b.password);
    EXPECT_EQ(a.name, b.name);
    EXPECT_EQ(a.phone, b.phone);
    EXPECT_EQ(a.money, b.money);
    EXPECT_EQ(a.address, b.address);
    EXPECT_EQ(a.type, b.type);
}

void equalExpressageNode(ExpressageNode a, ExpressageNode b) {
    EXPECT_EQ(a.id, b.id);
    EXPECT_EQ(a.sendUser, b.sendUser);
    EXPECT_EQ(a.receiveUser, b.receiveUser);
    EXPECT_EQ(a.assignTime, b.assignTime);
    EXPECT_EQ(a.signTime, b.signTime);
    EXPECT_EQ(a.remark, b.remark);
    EXPECT_EQ(a.Flag, b.Flag);
}

// Test fixture for LogisticSys class
class LogisticSysTest : public ::testing::Test {
protected:
    LogisticSys logistics;
    AccountNode accountRoot, accountAdmin, accountUser1, accountUser2, accountUser3, accountInvalid;
    ExpressageNode expressage1, expressage2, expressageInvalid;

    void SetUp() override {
        // Initialize the logistics object before each test
        initDataFiles();
        accountRoot = AccountNode("root_id", "root_pwd", "RootUser", "1234567890", 100.0, "RootAddress", authority::root);
        accountAdmin = AccountNode("admin_id", "admin_pwd", "AdminUser", "1234567890", 100.0, "AdminAddress", authority::admin);
        accountUser1 = AccountNode("test_id_1", "test_pwd", "TestUser1", "1234567890", 100.0, "TestAddress1", authority::user);
        accountUser2 = AccountNode("test_id_2", "test_pwd", "TestUser2", "1234567890", 100.0, "TestAddress2", authority::user);
        accountUser3 = AccountNode("test_id_3", "test_pwd", "TestUser3", "1234567890", 0.0, "TestAddress3", authority::user);
        accountInvalid = AccountNode();
        expressage1 = ExpressageNode("test_expressage_id_1", "test_id_1", "test_id_2", "2020-01-01", "NULL", "TestRemark", 0);
        expressage2 = ExpressageNode("test_expressage_id_2", "test_id_1", "test_id_2", "2020-01-01", "NULL", "TestRemark", 1);
        expressageInvalid = ExpressageNode();
        logistics.init("data/account.txt", "data/expressage.txt");
    }

    void TearDown() override {
        // Clean up the logistics object after each test
        std::filesystem::remove("data/account_new.txt");
        std::filesystem::remove("data/expressage_new.txt");
    }
};

// Test case for the save function
TEST_F(LogisticSysTest, SaveTest) {
    // save to new files
    logistics.save("data/account_new.txt", "data/expressage_new.txt");
    // diff the new files with the original files
    std::ifstream accountFile("data/account.txt");
    std::ifstream accountFileNew("data/account_new.txt");
    std::ifstream expressageFile("data/expressage.txt");
    std::ifstream expressageFileNew("data/expressage_new.txt");
    std::string accountLine, accountLineNew, expressageLine, expressageLineNew;
    while (std::getline(accountFile, accountLine) && std::getline(accountFileNew, accountLineNew)) {
        EXPECT_EQ(accountLine, accountLineNew);
    }
    while (std::getline(expressageFile, expressageLine) && std::getline(expressageFileNew, expressageLineNew)) {
        EXPECT_EQ(expressageLine, expressageLineNew);
    }
    accountFile.close();
    accountFileNew.close();
    expressageFile.close();
    expressageFileNew.close();
}

// Test case for the Regist function
TEST_F(LogisticSysTest, RegistTest) {
    // Test registration with valid account details
    EXPECT_TRUE(logistics.Regist("test_id", "test_pwd", "TestUser", "1234567890", 100.0, "TestAddress"));

    // Test registration with existing account ID
    EXPECT_FALSE(logistics.Regist("test_id", "test_pwd", "TestUser", "1234567890", 100.0, "TestAddress"));
}

// Test case for the Login function
TEST_F(LogisticSysTest, LoginTest) {
    // Test login with valid account ID and password
    EXPECT_EQ(logistics.Login("test_id_1", "test_pwd"), 2);

    // Test login with invalid account ID
    EXPECT_EQ(logistics.Login("invalid_id", "test_pwd"), -1);

    // Test login with invalid password
    EXPECT_EQ(logistics.Login("test_id_1", "invalid_pwd"), -1);
}

// Test case for the queryInfo function
TEST_F(LogisticSysTest, QueryInfoTest) {
    // Test querying info with valid account
    // EXPECT_EQ(logistics.queryInfo(0), accountRoot);
    equalAccountNode(logistics.queryInfo(0), accountRoot);

    // Test querying info with invalid account
    // EXPECT_EQ(logistics.queryInfo(-1), accountInvalid);
    equalAccountNode(logistics.queryInfo(-1), accountInvalid);

}

// Test case for the changePassword function
TEST_F(LogisticSysTest, ChangePasswordTest) {
    // Test changing password with correct old password
    EXPECT_TRUE(logistics.changePassword(0, "root_pwd", "new_pwd"));

    // Test changing password with incorrect old password
    EXPECT_FALSE(logistics.changePassword(0, "invalid_pwd", "new_pwd"));

    // Test changing password with invalid account
    EXPECT_FALSE(logistics.changePassword(-1, "root_pwd", "new_pwd"));

    // Test changing password with invalid account and incorrect old password
    EXPECT_FALSE(logistics.changePassword(-1, "invalid_pwd", "new_pwd"));
}

// Test case for the queryMoney function
TEST_F(LogisticSysTest, QueryMoneyTest) {
    // Test querying money with valid account
    EXPECT_EQ(logistics.queryMoney(0), 100.0);

    // Test querying money with invalid account
    EXPECT_EQ(logistics.queryMoney(-1), -1.0);
}

// Test case for the addMoney function
TEST_F(LogisticSysTest, AddMoneyTest) {
    // Test adding money with valid account
    EXPECT_EQ(logistics.addMoney(0, 100.0), 200.0);

    // Test adding money with a negative amount
    EXPECT_EQ(logistics.addMoney(1, -100.0), 0.0);

    // Test adding money with invalid account
    EXPECT_EQ(logistics.addMoney(-1, 100.0), -1.0);
}

// Test case for the assignExpressage function
TEST_F(LogisticSysTest, AssignExpressageTest) {
    // Test assigning expressage with valid account and valid receiver ID
    EXPECT_TRUE(logistics.assignExpressage(2, "test_id_3", "TestRemark", "2020-01-01"));

    // Test assigning expressage with valid account and invalid receiver ID
    EXPECT_FALSE(logistics.assignExpressage(2, "invalid_id", "TestRemark", "2020-01-01"));

    // Test assigning expressage with invalid account and valid receiver ID
    EXPECT_FALSE(logistics.assignExpressage(-1, "test_id_3", "TestRemark", "2020-01-01"));

    // Test assigning expressage with invalid account and invalid receiver ID
    EXPECT_FALSE(logistics.assignExpressage(-1, "invalid_id", "TestRemark", "2020-01-01"));

    // Test assigning expressage with valid account and receiver ID but is the same user
    EXPECT_FALSE(logistics.assignExpressage(2, "test_id_1", "TestRemark", "2020-01-01"));

    // Test assigning expressage with valid account and receiver ID but is the root user
    EXPECT_FALSE(logistics.assignExpressage(2, "root_id", "TestRemark", "2020-01-01"));

    // Test assigning expressage with valid account and receiver ID but money is not enough
    EXPECT_FALSE(logistics.assignExpressage(5, "test_id_1", "TestRemark", "2020-01-01"));
}

// Test case for the signExpressage function
TEST_F(LogisticSysTest, SignExpressageTest) {

    // Test signing expressage with valid account and invalid expressage ID
    EXPECT_FALSE(logistics.signExpressage(3, "invalid_expressage_id", "2020-01-01"));

    // Test signing expressage with invalid account and valid expressage ID
    EXPECT_FALSE(logistics.signExpressage(-1, "test_expressage_id_1", "2020-01-01"));

    // Test signing expressage with invalid account and invalid expressage ID
    EXPECT_FALSE(logistics.signExpressage(-1, "invalid_expressage_id", "2020-01-01"));

    // Test signing expressage with valid account and expressage ID but is not the receiver
    EXPECT_FALSE(logistics.signExpressage(2, "test_expressage_id_1", "2020-01-01"));

    // Test signing expressage with valid account and expressage ID
    EXPECT_TRUE(logistics.signExpressage(3, "test_expressage_id_1", "2020-01-01"));

    // Test signing expressage with valid account and expressage ID that has already been signed
    EXPECT_FALSE(logistics.signExpressage(3, "test_expressage_id_2", "2020-01-01"));
}

// Test case for the queryAllExpressage function
TEST_F(LogisticSysTest, QueryAllExpressageTest) {
    // Test querying all expressage with root account
    auto expressages = logistics.queryAllExpressage(0);
    EXPECT_EQ(expressages.size(), 2);
    // EXPECT_EQ(expressages[0], expressage1);
    // EXPECT_EQ(expressages[1], expressage2);
    equalExpressageNode(expressages[0], expressage1);
    equalExpressageNode(expressages[1], expressage2);

    // Test querying all expressage with admin account
    expressages = logistics.queryAllExpressage(1);
    EXPECT_EQ(expressages.size(), 2);
    // EXPECT_EQ(expressages[0], expressage1);
    // EXPECT_EQ(expressages[1], expressage2);
    equalExpressageNode(expressages[0], expressage1);
    equalExpressageNode(expressages[1], expressage2);

    // Test querying all expressage with user account
    expressages = logistics.queryAllExpressage(2);
    EXPECT_EQ(expressages.size(), 2);
    // EXPECT_EQ(expressages[0], expressage1);
    // EXPECT_EQ(expressages[1], expressage2);
    equalExpressageNode(expressages[0], expressage1);
    equalExpressageNode(expressages[1], expressage2);

    // Test querying all expressage with another user account
    expressages = logistics.queryAllExpressage(4);
    EXPECT_EQ(expressages.size(), 0);

    // Test querying all expressage with invalid account
    expressages = logistics.queryAllExpressage(-1);
    EXPECT_EQ(expressages.size(), 0);
}

// Test case for the queryExpressage function
TEST_F(LogisticSysTest, QueryExpressageTest) {
    // Test querying expressage with valid account and valid expressage ID
    // EXPECT_EQ(logistics.queryExpressage(2, "test_expressage_id_1"), expressage1);
    equalExpressageNode(logistics.queryExpressage(2, "test_expressage_id_1"), expressage1);

    // Test querying expressage with valid account and invalid expressage ID
    // EXPECT_EQ(logistics.queryExpressage(0, "invalid_expressage_id"), expressageInvalid);
    equalExpressageNode(logistics.queryExpressage(0, "invalid_expressage_id"), expressageInvalid);

    // Test querying expressage with valid expressage ID but is not the related user
    // EXPECT_EQ(logistics.queryExpressage(4, "test_expressage_id_1"), expressageInvalid);
    equalExpressageNode(logistics.queryExpressage(4, "test_expressage_id_1"), expressageInvalid);

    // Test querying expressage with valid expressage ID and admin or root account
    // EXPECT_EQ(logistics.queryExpressage(0, "test_expressage_id_1"), expressage1);
    equalExpressageNode(logistics.queryExpressage(0, "test_expressage_id_1"), expressage1);
    // EXPECT_EQ(logistics.queryExpressage(1, "test_expressage_id_1"), expressage1);
    equalExpressageNode(logistics.queryExpressage(1, "test_expressage_id_1"), expressage1);

    // Test querying expressage with invalid account and valid expressage ID
    // EXPECT_EQ(logistics.queryExpressage(-1, "test_expressage_id_1"), expressageInvalid);
    equalExpressageNode(logistics.queryExpressage(-1, "test_expressage_id_1"), expressageInvalid);

    // Test querying expressage with invalid account and invalid expressage ID
    // EXPECT_EQ(logistics.queryExpressage(-1, "invalid_expressage_id"), expressageInvalid);
    equalExpressageNode(logistics.queryExpressage(-1, "invalid_expressage_id"), expressageInvalid);
}