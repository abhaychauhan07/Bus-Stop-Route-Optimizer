// Initialize map
const map = L.map('map').setView([18.5204, 73.8567], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Store bus stops and markers
let busStops = [];
let markers = [];
let pathLayer = null;

// DOM elements
const startSelect = document.getElementById('start');
const endSelect = document.getElementById('end');
const findPathButton = document.getElementById('findPath');
const distanceElement = document.getElementById('distance');
const pathList = document.getElementById('path-list');

// Fetch bus stops from API
async function fetchBusStops() {
    try {
        const response = await fetch('http://localhost:5000/api/bus-stops');
        busStops = await response.json();
        
        // Add markers to map
        busStops.forEach(stop => {
            const marker = L.marker([stop.latitude, stop.longitude])
                .bindPopup(stop.name)
                .addTo(map);
            markers.push(marker);
            
            // Add options to select elements
            const option = document.createElement('option');
            option.value = stop.id;
            option.textContent = stop.name;
            startSelect.appendChild(option.cloneNode(true));
            endSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching bus stops:', error);
    }
}

// Find shortest path
async function findShortestPath() {
    const startId = parseInt(startSelect.value);
    const endId = parseInt(endSelect.value);
    
    if (startId === endId) {
        alert('Please select different start and end locations');
        return;
    }
    
    try {
        const response = await fetch('http://localhost:5000/api/shortest-path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start: startId,
                end: endId
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }
        
        displayPath(data);
    } catch (error) {
        console.error('Error finding path:', error);
        alert('Error finding path. Please try again.');
    }
}

// Display path on map and in sidebar
function displayPath(data) {
    // Clear previous path
    if (pathLayer) {
        map.removeLayer(pathLayer);
    }
    
    // Create path coordinates
    const coordinates = data.path.map(stop => [stop.latitude, stop.longitude]);
    
    // Draw path on map
    pathLayer = L.polyline(coordinates, {
        color: 'blue',
        weight: 3
    }).addTo(map);
    
    // Fit map to path
    map.fitBounds(pathLayer.getBounds(), {
        padding: [50, 50]
    });
    
    // Update distance
    distanceElement.textContent = `Total Distance: ${data.distance.toFixed(2)} km`;
    
    // Update path list
    pathList.innerHTML = '';
    data.path.forEach((stop, index) => {
        const li = document.createElement('li');
        li.textContent = `${index + 1}. ${stop.name}`;
        pathList.appendChild(li);
    });
}

// Event listeners
findPathButton.addEventListener('click', findShortestPath);

// Initialize
fetchBusStops(); 