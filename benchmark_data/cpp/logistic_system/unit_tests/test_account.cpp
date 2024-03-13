#include <gtest/gtest.h>
#include "account.h"

// Test fixture for AccountNode class
class AccountNodeTest : public ::testing::Test {
protected:
    AccountNode account;

    void SetUp() override {
        // Set up the account object before each test
        account = AccountNode("123", "password", "John Doe", "1234567890", 100.0, "123 Main St", authority::user);
    }
};

// Test the AccountNode constructor
TEST_F(AccountNodeTest, ConstructorTest) {
    EXPECT_EQ(account.id, "123");
    EXPECT_EQ(account.password, "password");
    EXPECT_EQ(account.name, "John Doe");
    EXPECT_EQ(account.phone, "1234567890");
    EXPECT_EQ(account.money, 100.0);
    EXPECT_EQ(account.address, "123 Main St");
    EXPECT_EQ(account.type, authority::user);
}

// Test the << operator overload
TEST_F(AccountNodeTest, OutputOperatorTest) {
    std::stringstream output;
    output << account;
    std::string expectedOutput = "AccountId: 123\n";
    expectedOutput += "UserName: John Doe\n";
    expectedOutput += "UserPhone: 1234567890\n";
    expectedOutput += "Money: 100\n";
    expectedOutput += "Address: 123 Main St\n";
    expectedOutput += "UserType: normal user\n";
    // expectedOutput += "----------------------------\n";
    EXPECT_EQ(output.str(), expectedOutput);
}
