<script lang="ts">
    import {onMount, createEventDispatcher} from "svelte";
    import "leaflet-draw/dist/leaflet.draw.css";
    import type {Map as LeafletMap, FeatureGroup, DrawEvents, Layer, GeoJSON} from "leaflet";

    const dispatch = createEventDispatcher();

    export let initialPolygon: GeoJSON | null = null;

    let map: LeafletMap;
    let drawnItems: FeatureGroup;

    onMount(async () => {
        const L = await import("leaflet");
        const {default: leafletDraw} = await import("leaflet-draw");

        // Create map centered on user's location
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    initializeMap(L, position.coords.latitude, position.coords.longitude);
                },
                error => {
                    console.error("Error getting location:", error);
                    initializeMap(L, 40.416775, -3.703790); // Default to Spain if geolocation fails
                }
            );
        } else {
            initializeMap(L, 40.416775, -3.703790); // Default to Spain if geolocation not available
        }
    });

    function initializeMap(L: any, lat: number, lng: number) {
        map = L.map("map").setView([lat, lng], 13);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        const sigpacLayer = L.tileLayer.wms("https://wms.mapa.gob.es/sigpac/wms", {
            layers: "AU.Sigpac:recinto",
            format: "image/png",
            transparent: true,
            attribution: "© SIGPAC"
        });

        sigpacLayer.addTo(map);

        drawnItems = new L.FeatureGroup();
        map.addLayer(drawnItems);

        const drawControl = new L.Control.Draw({
            edit: {
                featureGroup: drawnItems
            },
            draw: {
                polygon: true,
                polyline: false,
                rectangle: false,
                circle: false,
                marker: false,
                circlemarker: false
            }
        });

        map.addControl(drawControl);

        map.on(L.Draw.Event.CREATED, (e: DrawEvents.Created) => {
            const layer = e.layer;
            drawnItems.addLayer(layer);
            savePolygon();
        });

        map.on(L.Draw.Event.EDITED, () => {
            savePolygon();
        });

        map.on(L.Draw.Event.DELETED, () => {
            savePolygon();
        });

        if (initialPolygon) {
            L.geoJSON(initialPolygon).addTo(drawnItems);
        }
    }

    function savePolygon() {
        let polygon: GeoJSON | null = null;
        drawnItems.eachLayer(layer => {
            if (layer instanceof L.Polygon) {
                polygon = layer.toGeoJSON() as GeoJSON;
            }
        });
        dispatch('polygonUpdated', {polygon});
    }
</script>

<style>
    @import "https://unpkg.com/leaflet@1.7.1/dist/leaflet.css";
    @import "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css";

    #map {
        height: 400px;
        width: 100%;
    }
</style>

<div id="map"></div>