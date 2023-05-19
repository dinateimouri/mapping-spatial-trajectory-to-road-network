import matplotlib.pyplot as plt
import os


def visualize_matched_path(trajectory_gdf, matched_path_gdf, edges_proj, result_dir, result_filename):
    fig = plt.figure(1, (8, 8), dpi=100)
    ax = plt.subplot(111)
    plt.sca(ax)
    fig.tight_layout(rect=(0.05, 0.1, 1, 0.9))

    # Plot the road network geometry
    edges_proj.plot(ax=ax, color='#D9D9D9', lw=0.1)

    # Plot the trajectory points
    trajectory_gdf.to_crs(4326).plot(ax=ax, color='#FFA500', markersize=8, zorder=1, linestyle='solid')

    # Plot the matched path
    matched_path_gdf.plot(ax=ax, zorder=2, markersize=8, color='#008000', linestyle='dashed')

    plt.axis('off')
    plt.xlim(edges_proj.total_bounds[0], edges_proj.total_bounds[2])
    plt.ylim(edges_proj.total_bounds[1], edges_proj.total_bounds[3])

    plt.tight_layout()
    plt.savefig(os.path.join(result_dir, result_filename + '.pdf'), format='pdf', dpi=300, bbox_inches='tight')
    plt.close()
