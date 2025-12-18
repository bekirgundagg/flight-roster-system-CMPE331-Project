// src/Services/apiService.js

import { mockPilots, mockCrew } from "../mockData";

export function getPilots() {
  return new Promise((resolve) => {
    setTimeout(() => resolve(mockPilots), 300);
  });
}

export function getFlightCrew() {
  return new Promise((resolve) => {
    setTimeout(() => resolve(mockCrew), 300);
  });
}
