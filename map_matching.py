import geopandas as gpd
import pandas as pd
from leuvenmapmatching.matcher.distance import DistanceMatcher
from leuvenmapmatching.map.inmem import InMemMap
import similaritymeasures
from visualization import visualize_matched_path


def create_map_matching_map(edges_proj):
    map_con = InMemMap(name='map', use_latlon=False)
    for _, row in edges_proj.iterrows():
        map_con.add_node(row['u'], (row['y'], row['x']))
        map_con.add_node(row['v'], (row['y'], row['x']))
        map_con.add_edge(row['u'], row['v'])
    return map_con


def create_distance_matcher(map_con, grid_size):
    matcher = DistanceMatcher(
        map_con,
        max_dist=grid_size,
        max_dist_init=int(grid_size / 2),
        min_prob_norm=0.0001,
        non_emitting_length_factor=0.95,
        obs_noise=5,
        obs_noise_ne=5,
        dist_noise=50,
        max_lattice_width=20,
        non_emitting_states=True
    )
    return matcher


def visualize_and_save_result(trajectory_gdf, matched_path_gdf, edges_proj, result_dir, result_filename):
    visualize_matched_path(trajectory_gdf, matched_path_gdf, edges_proj, result_dir, result_filename)


def process_trajectory(trajectory, matcher, edges_proj, result_dir, result_filename):
    trajectory_gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(trajectory['lon'], trajectory['lat']))
    trajectory_gdf.crs = {'init': 'epsg:4326'}

    path = list(zip(trajectory_gdf.geometry.y, trajectory_gdf.geometry.x))
    normal_path = list(zip(trajectory_gdf.geometry.x, trajectory_gdf.geometry.y))

    states, _ = matcher.match(path, unique=False)

    path_df = pd.DataFrame(matcher.path_pred_onlynodes, columns=['u'])
    path_df['v'] = path_df['u'].shift(-1)
    path_df = path_df[-path_df['v'].isnull()]

    matched_path_gdf = pd.merge(path_df, edges_proj.reset_index())
    matched_path_gdf = gpd.GeoDataFrame(matched_path_gdf)
    matched_path_gdf.crs = {'init': 'epsg:4326'}

    matched_path = []
    for coord in matched_path_gdf.geometry:
        matched_path.append(list(coord.coords)[0])

    dtw, _ = similaritymeasures.dtw(matched_path, normal_path)
    fd = similaritymeasures.frechet_dist(matched_path, normal_path)

    visualize_and_save_result(trajectory_gdf, matched_path_gdf, edges_proj, result_dir, result_filename)

    return matched_path, dtw, fd


