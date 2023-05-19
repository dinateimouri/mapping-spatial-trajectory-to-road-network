# This code relies on the functionality provided by another repository.
# You can find the code at: https://github.com/ni1o1/transbigdata


import map_matching
import osmnx as ox
import pandas as pd
import ast
import osmnx as ox


def main(graphml_filename, trajectory_csv, result_dir, grid_size):
    graph = ox.load_graphml(graphml_filename)
    edges = ox.graph_to_gdfs(graph)
    edges_proj = ox.project_gdf(edges)

    map_con = map_matching.create_map_matching_map(edges_proj)

    matcher = map_matching.create_distance_matcher(map_con, grid_size)

    trajectory_df = pd.read_csv(trajectory_csv)

    for idx, row in trajectory_df.iterrows():
        trajectory = ast.literal_eval(row['trajectory'])
        result_filename = f"result_{idx}"
        map_matching.process_trajectory(trajectory, matcher, edges_proj, result_dir, result_filename)


if __name__ == '__main__':
    graphml_filename = 'beijing.graphml'
    trajectory_csv = 'trajectories.csv'
    result_dir = 'result'
    grid_size = 50

main(graphml_filename, trajectory_csv, result_dir, grid_size)

