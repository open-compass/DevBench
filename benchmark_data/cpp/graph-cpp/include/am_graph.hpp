#ifndef GRAPH_AM_GRAPH_HPP
#define GRAPH_AM_GRAPH_HPP

#include <stdexcept>
#include <cstring>
#include <ostream>
#include <tuple>
#include <vector>

template <typename VertexType>
class AdjacencyMatrixGraph{
    int **arcMatrix = nullptr;
    VertexType *vexList = nullptr;
    int _vexNum=0,_arcNum=0;
    bool _isDirected = false;
public:
    AdjacencyMatrixGraph(int vexNum, int arcNum, bool isDirected) : _vexNum(vexNum), _arcNum(arcNum), _isDirected(isDirected) {
        arcMatrix = new int*[vexNum];
        for (int i=0;i<vexNum;i++) {
            arcMatrix[i]=new int[vexNum];
            memset(arcMatrix[i],0, sizeof(int)*vexNum);
        }
        vexList = new VertexType[vexNum];
        memset(vexList,0, sizeof(int)*vexNum);
    }

    virtual ~AdjacencyMatrixGraph() {
        for (int i=0;i<_vexNum;i++) delete [] arcMatrix[i];
        delete [] arcMatrix;
        delete [] vexList;
    }

    int locateVex(VertexType target){
        /**
 * Locates the index of a specified vertex in the graph.
 *
 * This function searches through the graph's vertex list to find the given target vertex.
 * It iterates over the list and compares each vertex with the target. If a match is found,
 * the function returns the index of that vertex.
 *
 * Args:
 *    target (VertexType): The vertex to be located in the graph. The type of this vertex
 *    (VertexType) depends on how vertices are defined in the graph.
 *
 * Returns:
 *    int: The index of the target vertex in the graph's vertex list. Returns -1 if the
 *    vertex is not found in the graph.
 */
        for (int i=0;i<_vexNum;i++) {
            if(vexList[i]==target)return vexList[i];
        }
        return -1;
    }

    bool setVexes(std::vector<VertexType> list){
        /**
 * Sets the list of vertices in the graph.
 *
 * This function updates the graph's internal list of vertices to match the provided list.
 * It is used to initialize or modify the vertices of the graph. Each vertex in the list
 * is of type VertexType, which should match the graph's vertex type definition.
 *
 * Args:
 *    list (std::vector<VertexType>): The list of vertices to set in the graph. The type
 *    of each vertex in the list (VertexType) depends on how vertices are defined in the graph.
 *
 * Returns:
 *    bool: This function returns the result.
 */
        int i=-1;
        for (const auto &item : list) {
            if(i+1==_vexNum)throw std::out_of_range("");
            vexList[++i]=item;
        }
        return true;
    }

    bool setArcs(std::vector<std::tuple<int,int,int>> list){
        /**
 * Sets the list of arcs or edges in the graph.
 *
 * This function updates the graph's internal list of arcs or edges to match the provided list.
 * Each element in the list is a tuple representing an arc or edge, where the first two elements
 * of the tuple are the indices of the vertices connected by the arc, and the third element is
 * an integer representing the weight or cost of the arc. This function can be used to initialize
 * or modify the arcs or edges of the graph.
 *
 * Args:
 *    list (std::vector<std::tuple<int, int, int>>): The list of arcs or edges to set in the graph.
 *    Each tuple consists of two vertex indices and an integer weight.
 *
 * Returns:
 *    bool: This function returns the result.
 */
        for (const auto &[v1,v2,weight] : list) {
            int i=locateVex(v1),j=locateVex(v2);
            arcMatrix[i][j] = weight;
            if(!_isDirected)
                arcMatrix[j][i] = weight;
        }
        return true;
    }

    friend std::ostream &operator<<(std::ostream &os, const AdjacencyMatrixGraph &graph) {
        for(int i=0;i<graph._vexNum;i++){
            for(int j=0;j<graph._vexNum;j++){
                os << graph.arcMatrix[i][j] << ' ';
            }
            os << std::endl;
        }
        return os;
    }
};

#endif //GRAPH_AM_GRAPH_HPP
