from fmg_python.fmg_core.generators.voronoi import VoronoiGenerator

def test_voronoi_generator_initialization():
    gen = VoronoiGenerator(seed=42)
    assert gen.rng.seed_value == 42

    grid = gen.generate_grid(desired_cells=100)
    assert grid.cellsDesired == 100
    assert grid.spacing == 1.0
