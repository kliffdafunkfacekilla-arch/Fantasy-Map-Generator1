import { describe, it, expect } from "vitest";
import { initializeEcology, simulateEcologyStep, EcologyRates } from "./ecology-simulator";

describe("Ecology Simulation", () => {
  it("initializes ecology with correct array types and default values", () => {
    const cellsCount = 10;
    const state = initializeEcology(cellsCount);

    expect(state.plants).toBeInstanceOf(Float32Array);
    expect(state.herbivores).toBeInstanceOf(Float32Array);
    expect(state.predators).toBeInstanceOf(Float32Array);

    expect(state.plants.length).toBe(cellsCount);
    expect(state.herbivores.length).toBe(cellsCount);
    expect(state.predators.length).toBe(cellsCount);

    expect(state.plants[0]).toBe(100.0);
    expect(state.herbivores[0]).toBe(20.0);
    expect(state.predators[0]).toBe(5.0);
  });

  it("simulates predator-prey cyclical logic correctly", () => {
    const cellsCount = 1;
    const state = initializeEcology(cellsCount);

    const rates: EcologyRates = {
      plantGrowthRate: 0.1,
      herbivoreGrazingRate: 0.001,
      herbivoreReproductionRate: 0.0005,
      herbivoreDeathRate: 0.05,
      predatorHuntingRate: 0.002,
      predatorReproductionRate: 0.001,
      predatorDeathRate: 0.1,
    };

    const initialPlants = state.plants[0];
    const initialHerbivores = state.herbivores[0];
    const initialPredators = state.predators[0];

    simulateEcologyStep(state, cellsCount, rates);

    const P = initialPlants;
    const H = initialHerbivores;
    const C = initialPredators;

    // Plant dynamics
    const K = 1000.0;
    const plantGrowth = rates.plantGrowthRate * P * (1 - P / K);
    const plantLoss = rates.herbivoreGrazingRate * P * H;
    const expectedPlants = Math.max(0, P + plantGrowth - plantLoss);

    // Herbivore dynamics
    const herbivoreGrowth = rates.herbivoreReproductionRate * P * H;
    const herbivoreLoss = rates.herbivoreDeathRate * H + rates.predatorHuntingRate * H * C;
    const expectedHerbivores = Math.max(0, H + herbivoreGrowth - herbivoreLoss);

    // Predator dynamics
    const predatorGrowth = rates.predatorReproductionRate * H * C;
    const predatorLoss = rates.predatorDeathRate * C;
    const expectedPredators = Math.max(0, C + predatorGrowth - predatorLoss);

    // Because we use Float32, there might be slight precision differences
    expect(state.plants[0]).toBeCloseTo(expectedPlants, 4);
    expect(state.herbivores[0]).toBeCloseTo(expectedHerbivores, 4);
    expect(state.predators[0]).toBeCloseTo(expectedPredators, 4);
  });

  it("prevents populations from dropping below 0", () => {
    const cellsCount = 1;
    const state = initializeEcology(cellsCount);

    // Set up a scenario where populations would drop significantly
    state.plants[0] = 1;
    state.herbivores[0] = 1000;
    state.predators[0] = 1000;

    const rates: EcologyRates = {
      plantGrowthRate: 0.1,
      herbivoreGrazingRate: 0.5, // High grazing
      herbivoreReproductionRate: 0.01,
      herbivoreDeathRate: 0.5,
      predatorHuntingRate: 0.5, // High hunting
      predatorReproductionRate: 0.01,
      predatorDeathRate: 0.5,
    };

    simulateEcologyStep(state, cellsCount, rates);

    expect(state.plants[0]).toBeGreaterThanOrEqual(0);
    expect(state.herbivores[0]).toBeGreaterThanOrEqual(0);
    expect(state.predators[0]).toBeGreaterThanOrEqual(0);
  });
});
