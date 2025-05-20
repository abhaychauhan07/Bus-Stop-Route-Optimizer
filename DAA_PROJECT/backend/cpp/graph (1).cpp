#include "graph.hpp"
#include <queue>
#include <limits>
#include <algorithm>

Graph::Graph(int vertices) : numVertices(vertices) {
    adjacencyList.resize(vertices);
    busStops.resize(vertices);
}

void Graph::addEdge(int source, int destination, double weight) {
    adjacencyList[source].push_back({destination, weight});
    adjacencyList[destination].push_back({source, weight}); // Undirected graph
}

void Graph::addBusStop(int id, const std::string& name, double lat, double lon) {
    if (id < numVertices) {
        busStops[id] = {id, name, lat, lon};
    }
}

std::vector<int> Graph::shortestPath(int start, int end) {
    std::vector<double> distances(numVertices, std::numeric_limits<double>::infinity());
    std::vector<int> previous(numVertices, -1);
    std::vector<bool> visited(numVertices, false);
    
    distances[start] = 0;
    
    // Priority queue to store {distance, vertex}
    std::priority_queue<std::pair<double, int>, 
                       std::vector<std::pair<double, int>>,
                       std::greater<std::pair<double, int>>> pq;
    
    pq.push({0, start});
    
    while (!pq.empty()) {
        int current = pq.top().second;
        pq.pop();
        
        if (visited[current]) continue;
        visited[current] = true;
        
        if (current == end) break;
        
        for (const Edge& edge : adjacencyList[current]) {
            int next = edge.destination;
            double newDist = distances[current] + edge.weight;
            
            if (newDist < distances[next]) {
                distances[next] = newDist;
                previous[next] = current;
                pq.push({newDist, next});
            }
        }
    }
    
    // Reconstruct path
    std::vector<int> path;
    if (distances[end] == std::numeric_limits<double>::infinity()) {
        return path; // No path exists
    }
    
    for (int current = end; current != -1; current = previous[current]) {
        path.push_back(current);
    }
    std::reverse(path.begin(), path.end());
    return path;
}

double Graph::getPathDistance(const std::vector<int>& path) {
    double totalDistance = 0;
    for (size_t i = 0; i < path.size() - 1; i++) {
        int current = path[i];
        int next = path[i + 1];
        
        for (const Edge& edge : adjacencyList[current]) {
            if (edge.destination == next) {
                totalDistance += edge.weight;
                break;
            }
        }
    }
    return totalDistance;
}

BusStop Graph::getBusStop(int id) const {
    if (id < numVertices) {
        return busStops[id];
    }
    return {-1, "", 0, 0};
} 