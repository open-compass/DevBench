#include <gtest/gtest.h>
#include <memory>
#include "../include/al_graph.hpp" // Include your graph class header

class GraphTest : public ::testing::Test {
protected:
    std::unique_ptr<AdjacencyListGraph<int>> graph;
    bool flag_vexes, flag_arcs;

    void SetUp() override {
        std::vector<std::tuple<int, int, int>> arcs = {{1, 2, 1}, {1, 3, 1}, {2, 4, 1},{2,5,1},{3,6,1},{3, 7, 1},{4, 8, 1},{5, 8, 1},{6, 8, 1},{7, 8, 1}};
        std::vector<int> vexes = {1, 2, 3,4,5,6,7,8 /*... other vertices ...*/};
        graph = std::make_unique<AdjacencyListGraph<int>>(vexes.size(), arcs.size(), false);
        flag_vexes = graph->setVexes(vexes);
        flag_arcs = graph->setArcs(arcs);
    }
};

    TEST_F(GraphTest, VertexNumberTest) {
        ASSERT_EQ(flag_vexes, true);
    }

    TEST_F(GraphTest, ArcNumberTest) {
        ASSERT_EQ(flag_arcs, true);
    }

    TEST_F(GraphTest, TestDFSNoRecursionAdjacencyList) {
        std::vector<int> expectedDFSNoRec = {1, 2, 4,8,5,7,3,6}; // Expected non-recursive DFS order
        std::vector<int> resultDFSNoRec = graph->dfs_noRes();
        ASSERT_EQ(resultDFSNoRec, expectedDFSNoRec);
    }

    TEST_F(GraphTest, TestBFSAdjacencyList) {
        std::vector<int> expectedBFS = {1, 2, 3,4,5,6,7,8}; // Expected BFS order
        std::vector<int> resultBFS = graph->bfs();
        ASSERT_EQ(resultBFS, expectedBFS);
    }

    TEST_F(GraphTest, SetVexesAndLocateVex) {
        int expectedLocate = {2}; // init
        int resultLocate = graph->locateVex(3);
        ASSERT_EQ(resultLocate, expectedLocate);
    }

TEST_F(GraphTest, LocateVexNonExisting) {
    ASSERT_EQ(graph->locateVex(10), -1);
}

TEST_F(GraphTest, SetVexesInvalidInput) {
    std::vector<int> invalidVexes = {1,2,3,4,5,6,7,8,9,10,11};
    EXPECT_THROW(graph->setVexes(invalidVexes), std::out_of_range);
}

