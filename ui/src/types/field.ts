// src/types/field.ts
export interface Field {
    id: string;
    crop: string;
    area: number;
    lastWatered: string;
    soilType: string;
    polygon: {
        type: string;
        coordinates: number[][][];
    };
}