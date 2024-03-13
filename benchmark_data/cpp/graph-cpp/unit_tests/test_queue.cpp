//
// Created by defense227 on 2023/12/2.
//
#include <gtest/gtest.h>
#include "../include/queue.hpp"

TEST(QueueTest, IsEmptyOnInitialization) {
Queue<int> q;
ASSERT_TRUE(q.empty());
}

TEST(QueueTest, PushAndFront) {
Queue<int> q;
q.push(1);
ASSERT_FALSE(q.empty());
EXPECT_EQ(q.front(), 1);
}

TEST(QueueTest, Pop) {
Queue<int> q;
q.push(1);
q.pop();
ASSERT_TRUE(q.empty());
}
TEST(QueueTest, PushDouble) {
Queue<int> q;
q.push(1);
q.push(2);
ASSERT_FALSE(q.empty());
EXPECT_EQ(q.front(), 1);
}
TEST(QueueTest, FrontThrowsWhenEmpty) {
    Queue<int> q;
    EXPECT_THROW(q.front(), std::out_of_range);
}

TEST(QueueTest, PopThrowsWhenEmpty) {
    Queue<int> q;
    EXPECT_THROW(q.pop(), std::out_of_range);
}
