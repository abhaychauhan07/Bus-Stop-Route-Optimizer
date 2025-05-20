from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import sqlite3
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

app = Flask(__name__)
CORS(app)

def get_db_connection():
    # Get the absolute path to the database
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'bus_routes.db')
    print(f"Attempting to connect to database at: {db_path}")  # Debug print
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {str(e)}")  # Debug print
        raise

@app.route('/')
def home():
    return "Bus Route Optimizer API is running!"

@app.route('/api/bus-stops', methods=['GET'])
def get_bus_stops():
    try:
        conn = get_db_connection()
        stops = conn.execute('SELECT * FROM bus_stops').fetchall()
        conn.close()
        result = [dict(stop) for stop in stops]
        print(f"Retrieved {len(result)} bus stops")  # Debug print
        return jsonify(result)
    except Exception as e:
        print(f"Error in get_bus_stops: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 500

@app.route('/api/routes', methods=['GET'])
def get_routes():
    try:
        conn = get_db_connection()
        routes = conn.execute('SELECT * FROM routes').fetchall()
        conn.close()
        result = [dict(route) for route in routes]
        print(f"Retrieved {len(result)} routes")  # Debug print
        return jsonify(result)
    except Exception as e:
        print(f"Error in get_routes: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 500

@app.route('/api/shortest-path', methods=['POST'])
def find_shortest_path():
    try:
        data = request.get_json()
        start_id = data.get('start')
        end_id = data.get('end')
        
        print(f"Finding path from {start_id} to {end_id}")  # Debug print
        
        if start_id is None or end_id is None:
            return jsonify({'error': 'Start and end points are required'}), 400
        
        # Import the C++ module
        from cpp.graph_module import Graph
        
        # Create graph from database
        conn = get_db_connection()
        stops = conn.execute('SELECT * FROM bus_stops').fetchall()
        routes = conn.execute('SELECT * FROM routes').fetchall()
        
        # Initialize graph
        graph = Graph(len(stops))
        
        # Add bus stops
        for stop in stops:
            graph.addBusStop(stop['id'], stop['name'], stop['latitude'], stop['longitude'])
        
        # Add routes
        for route in routes:
            graph.addEdge(route['source'], route['destination'], route['distance'])
        
        # Find shortest path
        path = graph.shortestPath(start_id, end_id)
        
        if not path:
            return jsonify({'error': 'No path found'}), 404
        
        # Get path details
        path_stops = []
        for stop_id in path:
            stop = conn.execute('SELECT * FROM bus_stops WHERE id = ?', (stop_id,)).fetchone()
            path_stops.append(dict(stop))
        
        distance = graph.getPathDistance(path)
        
        conn.close()
        print(f"Found path with {len(path_stops)} stops and distance {distance}")  # Debug print
        return jsonify({
            'path': path_stops,
            'distance': distance
        })
        
    except Exception as e:
        print(f"Error in find_shortest_path: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")  # Debug print
    app.run(debug=True, host='0.0.0.0') 