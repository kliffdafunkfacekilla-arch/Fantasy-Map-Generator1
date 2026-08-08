export interface CalendarState {
  tick: number;         // Master tick counter
  day: number;          // Current day of the year
  month: number;        // Current month
  year: number;         // Current year
  seasonOffset: number; // Values from -1.0 to 1.0 (e.g. -1 is deep winter, 1 is peak summer in northern hemisphere)
}

export interface PlanetaryCycles {
  ticksPerDay: number;
  daysPerMonth: number;
  monthsPerYear: number;
}

export class TickSystem {
  private cycles: PlanetaryCycles;
  private state: CalendarState;

  constructor(
    cycles: PlanetaryCycles = { ticksPerDay: 24, daysPerMonth: 30, monthsPerYear: 12 },
    initialState?: CalendarState
  ) {
    this.cycles = cycles;
    this.state = initialState || {
      tick: 0,
      day: 0,
      month: 0,
      year: 0,
      seasonOffset: 0
    };
  }

  public getState(): CalendarState {
    return { ...this.state };
  }

  public advance(ticks: number = 1): CalendarState {
    this.state.tick += ticks;

    // Calculate days passed from total ticks
    const totalDays = Math.floor(this.state.tick / this.cycles.ticksPerDay);

    // Calculate years passed
    const daysPerYear = this.cycles.daysPerMonth * this.cycles.monthsPerYear;
    this.state.year = Math.floor(totalDays / daysPerYear);

    // Day of the current year
    const dayOfYear = totalDays % daysPerYear;
    this.state.day = dayOfYear;

    // Current month
    this.state.month = Math.floor(dayOfYear / this.cycles.daysPerMonth);

    // Season offset (assuming sinusoidal orbit mapping, starting at 0)
    // 0 = equinox, 1 = summer solstice (NH), 0 = equinox, -1 = winter solstice (NH)
    // Let's use a sine wave where a full year is 2*PI radians
    const yearProgress = dayOfYear / daysPerYear;
    this.state.seasonOffset = Math.sin(yearProgress * Math.PI * 2);

    return this.getState();
  }
}
