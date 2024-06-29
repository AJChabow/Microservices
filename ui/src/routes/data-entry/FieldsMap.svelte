<script lang="ts">
    import {onMount, createEventDispatcher} from "svelte";
    import "leaflet/dist/leaflet.css";
    import "leaflet-draw/dist/leaflet.draw.css";
    import type {Map as LeafletMap, FeatureGroup, DrawEvents, Layer, GeoJSON} from "leaflet";
    import type {Field} from "../"

    const dispatch = createEventDispatcher();

    export let fields: Field[] = [];
    export let selectedField: Field | null = null;

    let map: LeafletMap;
    let drawnItems: FeatureGroup;
    let fieldLayers: { [id: string]: Layer } = {};

    onMount(async () => {
        const L = await import("leaflet");
        await import("leaflet-draw");

        initializeMap(L);
    });

    function initializeMap(L: any) {
        map = L.map("map").setView([40.416775, -3.703790], 6); // Default view of Spain

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
            dispatch('fieldCreated', {polygon: layer.toGeoJSON()});
        });

        map.on(L.Draw.Event.EDITED, (e: DrawEvents.Edited) => {
            e.layers.eachLayer((layer: Layer) => {
                if (layer instanceof L.Polygon) {
                    const fieldId = Object.keys(fieldLayers).find(id => fieldLayers[id] === layer);
                    if (fieldId) {
                        dispatch('fieldUpdated', {id: fieldId, polygon: layer.toGeoJSON()});
                    }
                }
            });
        });

        map.on(L.Draw.Event.DELETED, (e: DrawEvents.Deleted) => {
            e.layers.eachLayer((layer: Layer) => {
                const fieldId = Object.keys(fieldLayers).find(id => fieldLayers[id] === layer);
                if (fieldId) {
                    dispatch('fieldDeleted', {id: fieldId});
                    delete fieldLayers[fieldId];
                }
            });
        });

        renderFields(L);
    }

    function renderFields(L: any) {
        fields.forEach(field => {
            if (field.polygon) {
                const layer = L.geoJSON(field.polygon, {
                    style: {
                        color: getRandomColor(),
                        weight: 2,
                        opacity: 0.65
                    }
                }).addTo(drawnItems);

                layer.bindTooltip(field.crop, {permanent: true, direction: 'center'});

                layer.on('click', () => {
                    selectedField = field;
                    dispatch('fieldSelected', {field});
                });

                fieldLayers[field.id] = layer;
            }
        });

        if (fields.length > 0) {
            map.fitBounds(drawnItems.getBounds());
        }
    }

    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    export function updateFields(newFields: Field[]) {
        fields = newFields;
        drawnItems.clearLayers();
        fieldLayers = {};
        renderFields(L);
    }

    export function focusOnField(fieldId: string) {
        const layer = fieldLayers[fieldId];
        if (layer) {
            map.fitBounds(layer.getBounds());
        }
    }
</script>

<style>
    #map {
        height: 600px;
        width: 100%;
    }
</style>

<div id="map"></div>