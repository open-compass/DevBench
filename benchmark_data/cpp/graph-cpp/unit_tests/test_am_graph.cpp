#include <gtest/gtest.h>
#include <memory>
#include "../include/am_graph.hpp" // Include your graph class header

class MatrixGraphTest : public ::testing::Test {
protected:
    std::unique_ptr<AdjacencyMatrixGraph<int>> graph;
    bool flag_vexes, flag_arcs;
    void SetUp() override {
        std::vector<std::tuple<int, int, int>> arcs = {{1, 2, 1}, {2, 3, 1}, /*... other arcs ...*/};
        std::vector<int> vexes = {1, 2, 3, /*... other vertices ...*/};
        graph = std::make_unique<AdjacencyMatrixGraph<int>>(vexes.size()+1, arcs.size()+1, false);
        flag_vexes = graph->setVexes(vexes);
        flag_arcs = graph->setArcs(arcs);
    }
};
    TEST_F(MatrixGraphTest, VertexSetTest) {
        ASSERT_EQ(flag_vexes, true);
    }

// Test case for verifying the number of arcs
    TEST_F(MatrixGraphTest, ArcSetTest) {
        ASSERT_EQ(flag_arcs, true);
    }
TEST_F(MatrixGraphTest, LocateVexTest) {
    int expectedIndex = 1; // Assuming vertex '1' is at index 1
    ASSERT_EQ(graph->locateVex(1), expectedIndex);
    ASSERT_EQ(graph->locateVex(6), -1); // Replace NON_EXISTING_VERTEX with a suitable value
}

// You can add similar tests for setVexes and memory allocation/deallocation.

