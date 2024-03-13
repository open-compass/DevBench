//
// Created by defense227 on 2023/12/2.
//
#include <gtest/gtest.h>
#include "../include/stack.hpp"

TEST(StackTest, IsEmptyOnInitialization) {
Stack<int> s;
ASSERT_TRUE(s.empty());
}

TEST(StackTest, PushAndTop) {
Stack<int> s;
s.push(1);
ASSERT_FALSE(s.empty());
EXPECT_EQ(s.top(), 1);
}

TEST(StackTest, Pop) {
Stack<int> s;
s.push(1);
s.pop();
ASSERT_TRUE(s.empty());
}
TEST(StackTest, TopThrowsWhenEmpty) {
    Stack<int> s;
    EXPECT_THROW(s.top(), std::out_of_range);
}

TEST(StackTest, PopThrowsWhenEmpty) {
    Stack<int> s;
    EXPECT_THROW(s.pop(), std::out_of_range);
}

TEST(StackTest, PushOverflow) {
    Stack<int> s;
    try {
        for (int i = 0; i < 100; ++i) {
            s.push(i);
        }
        // You may need to define VERY_LARGE_NUMBER to be sufficiently large
        // to trigger a reallocation failure, based on the system's memory availability.
    } catch (const std::overflow_error& e) {
        EXPECT_EQ(e.what(), std::string("stack overflow"));
    }
}
