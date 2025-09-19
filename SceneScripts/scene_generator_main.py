from setup_scene import initialize_scene
from terrain import generate_terrain
from forest import generate_forest
from town import generate_town


def main():
    col = initialize_scene()

    all_positions = []

    terrain_obj = generate_terrain(col)
    generate_forest(col, terrain_obj, all_positions)
    generate_town(col, terrain_obj, all_positions)


if __name__ == "__main__":
    main()


