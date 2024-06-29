<script lang="ts">
    import {onMount} from 'svelte';

    interface Field {
        id: number;
        name: string;
        crop: string;
        area: number;
        lastWatered: string;
        soilType: string;
        color: string;
        coordinates: [number, number][];
    }

    let fields: Field[] = [
        {
            id: 1,
            name: "North Field",
            crop: "Wheat",
            area: 10.5,
            lastWatered: "2023-06-28",
            soilType: "Loam",
            color: "#FF0000",
            coordinates: [[40.416775, -3.703790], [40.417, -3.704], [40.418, -3.703]]
        },
        {
            id: 2,
            name: "South Field",
            crop: "Corn",
            area: 8.3,
            lastWatered: "2023-06-27",
            soilType: "Clay",
            color: "#00FF00",
            coordinates: [[40.415, -3.705], [40.416, -3.706], [40.417, -3.705]]
        },
        {
            id: 3,
            name: "East Field",
            crop: "Soybeans",
            area: 12.7,
            lastWatered: "2023-06-26",
            soilType: "Sandy",
            color: "#0000FF",
            coordinates: [[40.418, -3.701], [40.419, -3.702], [40.420, -3.701]]
        }
    ];

    let selectedField: Field | null = null;
    let map: google.maps.Map;
    let fieldPolygons: google.maps.Polygon[] = [];

    onMount(() => {
        initializeMap();
    });

    function initializeMap() {
        const mapOptions = {
            center: {lat: 40.416775, lng: -3.703790},
            zoom: 14
        };
        map = new google.maps.Map(document.getElementById('map'), mapOptions);

        fields.forEach(field => addFieldToMap(field));
    }

    function addFieldToMap(field: Field) {
        const polygon = new google.maps.Polygon({
            paths: field.coordinates.map(coord => ({lat: coord[0], lng: coord[1]})),
            strokeColor: field.color,
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: field.color,
            fillOpacity: 0.35
        });

        polygon.setMap(map);
        fieldPolygons.push(polygon);

        polygon.addListener('click', () => selectField(field));
    }

    function selectField(field: Field) {
        selectedField = field;
        // Center the map on the selected field
        const bounds = new google.maps.LatLngBounds();
        field.coordinates.forEach(coord => bounds.extend(new google.maps.LatLng(coord[0], coord[1])));
        map.fitBounds(bounds);
    }
</script>

<svelte:head>
    <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY"></script>
</svelte:head>

<div class="flex h-screen">
    <div class="w-1/3 p-4 overflow-y-auto">
        <h1 class="text-2xl font-bold mb-4">My Fields</h1>
        {#each fields as field}
            <div class="mb-3 p-4 border rounded cursor-pointer hover:bg-gray-100" on:click={() => selectField(field)}>
                <h2 class="text-xl font-semibold">{field.name}</h2>
                <p>Crop: {field.crop}</p>
                <p>Area: {field.area} hectares</p>
            </div>
        {/each}
        <button class="mt-4 bg-blue-500 text-white px-4 py-2 rounded">Add New Field</button>
    </div>
    <div class="w-2/3 p-4">
        <div id="map" class="h-2/3 w-full"></div>
        {#if selectedField}
            <div class="mt-4">
                <h2 class="text-2xl font-bold mb-2">{selectedField.name}</h2>
                <p>Crop: {selectedField.crop}</p>
                <p>Area: {selectedField.area} hectares</p>
                <p>Last Watered: {selectedField.lastWatered}</p>
                <p>Soil Type: {selectedField.soilType}</p>
                <button class="mt-2 bg-green-500 text-white px-4 py-2 rounded mr-2">Edit Field</button>
                <button class="mt-2 bg-red-500 text-white px-4 py-2 rounded">Delete Field</button>
            </div>
        {/if}
    </div>
</div>