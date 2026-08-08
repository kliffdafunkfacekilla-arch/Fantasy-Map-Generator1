export interface EcologyState {
  plants: Float32Array;
  herbivores: Float32Array;
  predators: Float32Array;
}

export function initializeEcology(cellsCount: number): EcologyState {
  const plants = new Float32Array(cellsCount);
  const herbivores = new Float32Array(cellsCount);
  const predators = new Float32Array(cellsCount);

  for (let i = 0; i < cellsCount; i++) {
    plants[i] = 100.0; // Initial plant population
    herbivores[i] = 20.0; // Initial herbivore population
    predators[i] = 5.0; // Initial predator population
  }

  return { plants, herbivores, predators };
}

export interface EcologyRates {
  plantGrowthRate: number;
  herbivoreGrazingRate: number;
  herbivoreReproductionRate: number;
  herbivoreDeathRate: number;
  predatorHuntingRate: number;
  predatorReproductionRate: number;
  predatorDeathRate: number;
}

export function simulateEcologyStep(
  state: EcologyState,
  cellsCount: number,
  rates: EcologyRates
): void {
  for (let i = 0; i < cellsCount; i++) {
    const P = state.plants[i];
    const H = state.herbivores[i];
    const C = state.predators[i]; // Carnivores/Predators

    // Plant dynamics: logistical growth minus grazing by herbivores
    // Assume carrying capacity for plants is around 1000 for logistical growth
    const K = 1000.0;
    const plantGrowth = rates.plantGrowthRate * P * (1 - P / K);
    const plantLoss = rates.herbivoreGrazingRate * P * H;

    // Herbivore dynamics: gain from eating plants, loss from natural death and predation
    const herbivoreGrowth = rates.herbivoreReproductionRate * P * H;
    const herbivoreLoss = rates.herbivoreDeathRate * H + rates.predatorHuntingRate * H * C;

    // Predator dynamics: gain from eating herbivores, loss from natural death
    const predatorGrowth = rates.predatorReproductionRate * H * C;
    const predatorLoss = rates.predatorDeathRate * C;

    // Update populations (Euler method integration step, dt=1)
    let nextP = P + plantGrowth - plantLoss;
    let nextH = H + herbivoreGrowth - herbivoreLoss;
    let nextC = C + predatorGrowth - predatorLoss;

    // Ensure populations don't drop below 0
    state.plants[i] = Math.max(0, nextP);
    state.herbivores[i] = Math.max(0, nextH);
    state.predators[i] = Math.max(0, nextC);
  }
}
