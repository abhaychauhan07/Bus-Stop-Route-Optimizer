#pragma once
#include <vector>
#include <queue>
#include <limits>
#include <unordered_map>
#include <string>

struct BusStop {
    int id;
    std::string name;
    double latitude;
    double longitude;
};

struct Edge {
    int destination;
    double weight;
};

class Graph {
private:
    std::vector<std::vector<Edge>> adjacencyList;
    std::vector<BusStop> busStops;
    int numVertices;

public:
    Graph(int vertices);
    void addEdge(int source, int destination, double weight);
    void addBusStop(int id, const std::string& name, double lat, double lon);
    std::vector<int> shortestPath(int start, int end);
    double getPathDistance(const std::vector<int>& path);
    BusStop getBusStop(int id) const;
}; 