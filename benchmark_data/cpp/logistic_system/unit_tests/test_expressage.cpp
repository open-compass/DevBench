#include "expressage.h"
#include <gtest/gtest.h>

// Test the default constructor of ExpressageNode
TEST(ExpressageNodeTest, DefaultConstructor) {
    ExpressageNode node;
    EXPECT_EQ("", node.id);
    EXPECT_EQ("", node.sendUser);
    EXPECT_EQ("", node.receiveUser);
    EXPECT_EQ("", node.assignTime);
    EXPECT_EQ("", node.signTime);
    EXPECT_EQ("", node.remark);
    EXPECT_FALSE(node.Flag);
}

// Test the full parameterized constructor of ExpressageNode
TEST(ExpressageNodeTest, ParameterizedConstructorFull) {
    ExpressageNode node("ID", "Sender", "Recipient", "AssignTime", "SignTime", "Remark", true);
    EXPECT_EQ("ID", node.id);
    EXPECT_EQ("Sender", node.sendUser);
    EXPECT_EQ("Recipient", node.receiveUser);
    EXPECT_EQ("AssignTime", node.assignTime);
    EXPECT_EQ("SignTime", node.signTime);
    EXPECT_EQ("Remark", node.remark);
    EXPECT_TRUE(node.Flag);
}

// Test the Sign() method of ExpressageNode
TEST(ExpressageNodeTest, Sign) {
    ExpressageNode node;
    EXPECT_TRUE(node.Sign("2020-01-01"));
    EXPECT_FALSE(node.Sign("2020-01-01"));
}

// Test the output stream operator of ExpressageNode
TEST(ExpressageNodeTest, OutputOperator) {
    ExpressageNode node("ID", "Sender", "Recipient", "2020-01-01", "2020-01-01", "Remark", true);
    std::stringstream ss;
    ss << node;
    std::string expectedOutput = "Expressage id: " + node.id + "\n"
                                 "Sender: " + node.sendUser + "\n"
                                 "Recipient: " + node.receiveUser + "\n"
                                 "Send Time: " + node.assignTime + "\n"
                                 "Status: Signed\n"
                                 "Sign Time: " + node.signTime + "\n"
                                 "Remark: " + node.remark + "\n";
    EXPECT_EQ(expectedOutput, ss.str());
}
