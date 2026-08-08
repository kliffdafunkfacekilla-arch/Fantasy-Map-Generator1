import { store } from "../../state/store";
import { TickSystem } from "./tick-system";
import { generateClimate, ClimateOptions } from "../climate/climate-generator";
import { generateBiomes } from "../biomes/biomes-generator";

export class SimulationLoop {
  private tickSystem: TickSystem;
  private climateOptions: ClimateOptions;

  constructor(initialOptions: ClimateOptions) {
    this.tickSystem = new TickSystem();
    this.climateOptions = { ...initialOptions };
  }

  public advanceTick(ticks: number = 1): void {
    const calendar = this.tickSystem.advance(ticks);
    const currentState = store.getState();

    // We only simulate dynamically if we have the prerequisite layers
    if (!currentState.grid || !currentState.heights || !currentState.rivers) {
      store.updateState({
        tick: calendar.tick,
        calendar
      });
      return;
    }

    // Apply season shift and re-run generators
    this.climateOptions.seasonOffset = calendar.seasonOffset;

    const { temp, prec } = generateClimate(
      currentState.grid,
      currentState.heights,
      currentState.width,
      currentState.height,
      this.climateOptions
    );

    const biomes = generateBiomes(
      currentState.grid,
      currentState.heights,
      temp,
      prec,
      currentState.rivers
    );

    store.updateState({
      tick: calendar.tick,
      calendar,
      temp,
      prec,
      biomes
    });
  }

  public getCalendar() {
    return this.tickSystem.getState();
  }
}
