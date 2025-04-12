import numpy as np
from scipy  import spatial
from scipy.sparse.csgraph import shortest_path

import jax
import ott
from ott.solvers import linear

import pandas as pd
import simfish
        

def simulate_data(templates_path, n_cells=10, n_spots=15, proportion_pattern=0.9, patterns = ['intranuclear', 'perinuclear', 'pericellular', 'extranuclear', 'foci'], return_raw = False):
    '''
    Generate simulated fish data for a given number of cells and spots per cell
    
    Args:
        templates_path: str
            path to the folder containing the templates
        n_cells: int
            number of cells to simulate
        n_spots: int
            number of spots per cell
        proportion_pattern: float
            proportion of spots that should follow the pattern (0-1)
        patterns: list
            list of patterns to simulate. Valid patterns are 'intranuclear', 'perinuclear', 'nuclear_edge', 'extranuclear', 'pericellular', 'cell_edge', 'foci', and 'protrusion'.
    
    Returns:
        data: pd.DataFrame
            has columns 'cell', 'x', 'y', 'gene'
            the genes are 'simulated' (simulated transcripts) and 'outline' (cell outline for convex hull later)
    '''
    sims = []
    for i in range(len(patterns)):
        for j in range(n_cells):
            sims.append(simfish.simulate_localization_pattern(templates_path, 
                                                            n_spots=n_spots, 
                                                            i_cell=j, 
                                                            pattern=patterns[i],
                                                            proportion_pattern=proportion_pattern
                                                            ))
    # Extract RNA and outline coordinates
    rna = [sims[_]['rna_coord'][:,1:] for _ in range(len(sims))]
    outline = [sims[_]['cell_coord'] for _ in range(len(sims))]

    if return_raw == True:
        return rna, outline
    
    # Assign to cells
    d = np.concatenate([np.concatenate([i * np.ones((len(rna[i]), 1)), rna[i]], axis=1) for i in range(len(rna))])
    o = np.concatenate([np.concatenate([i * np.ones((len(outline[i]), 1)), outline[i]], axis=1) for i in range(len(outline))])
    
    # Create dataframes
    rna_df = pd.DataFrame(d, columns=['cell', 'x', 'y'])
    outline_df = pd.DataFrame(o, columns=['cell', 'x', 'y'])
    rna_df['gene']='simulated'
    outline_df['gene']='outline'
    data = pd.concat([rna_df, outline_df])
    data['cell'] = data['cell'].astype(int)
    return data


def simulate_multi_genes_data(templates_path, n_genes = 2, n_cells=10, n_spots=15, proportion_pattern=0.9, patterns = ['intranuclear', 'perinuclear', 'pericellular', 'extranuclear', 'foci']):
    data = simulate_data(templates_path, n_cells, n_spots, proportion_pattern, patterns)
    data.loc[data['gene'] == 'simulated', 'gene'] = 'simulated_1'
    # for the rest of the genes, only take RNA
    for g in range(n_genes-1):
        d = simulate_data(templates_path, n_cells, n_spots, proportion_pattern, patterns)
        rna = d[d['gene']=='simulated'].copy() # take only RNA
        cell_map = dict(zip(range(n_cells*len(patterns)), np.random.permutation(n_cells*len(patterns))))
        rna['cell'] = rna['cell'].map(cell_map)
        rna['gene']=f'simulated_{g+2}'
        data = pd.concat([data, rna])
    return data


def get_evenly_spaced_outline(points, num_outline_points=50):
    '''add points that are evnely spaced to the outline'''
    # Get convex hull of the points
    hull = spatial.ConvexHull(points)
    outline = points[hull.vertices]

    # Calculate the total perimeter length of the convex hull
    perimeter = np.sum(np.linalg.norm(np.diff(outline, axis=0, append=outline[:1]), axis=1))

    # Calculate the desired spacing
    spacing = perimeter / num_outline_points

    # Function to interpolate points between two points
    def interpolate_points(p1, p2, spacing):
        segment_length = np.linalg.norm(p2 - p1)
        num_new_points = int(segment_length // spacing)
        new_points = np.linspace(p1, p2, num_new_points + 2)[1:-1]
        return new_points

    # Create a list of new points, starting with the original hull points
    new_hull_points = []
    for i in range(len(outline)):
        p1 = outline[i]
        p2 = outline[(i + 1) % len(outline)]
        new_hull_points.append(p1)
        new_hull_points.extend(interpolate_points(p1, p2, spacing))

    # Convert new hull points to a numpy array
    return np.array(new_hull_points)


def scale_cell_SVD(rna, outline):
    ''' scale outline and rna by approximating outline as an ellipse and scaling to unit circle '''
    x, y = outline[:, 0], outline[:, 1]
    rna_x, rna_y = rna[:, 0], rna[:, 1]

    # Mean of the points
    xmean, ymean = x.mean(), y.mean()
    x_centered = x - xmean
    y_centered = y - ymean

    # Perform Singular Value Decomposition
    U, S, Vt = np.linalg.svd(np.stack((x_centered, y_centered)))

    # Generate points for the unit circle
    tt = np.linspace(0, 2 * np.pi, 1000)
    circle = np.stack((np.cos(tt), np.sin(tt)))

    # Transform the unit circle to the ellipse
    transform = np.sqrt(2 / len(x)) * U.dot(np.diag(S))
    fit = transform.dot(circle)
    fit[0, :] += xmean
    fit[1, :] += ymean


    # Rescale transcripts accordingly
    inverse_transform = np.linalg.inv(transform)
    rna_x_centered = rna_x - xmean
    rna_y_centered = rna_y - ymean
    scaled_rna_coords = inverse_transform.dot(np.stack((rna_x_centered, rna_y_centered))).T

    x_centered = x - xmean
    y_centered = y - ymean
    scaled_outline = inverse_transform.dot(np.stack((x_centered, y_centered))).T

    return scaled_rna_coords, scaled_outline, fit, circle







def find_thresh(C, inf=0.5, sup=3, step=10):
    """ Trick to find the adequate thresholds from where value of the C matrix are considered close enough to say that nodes are connected
        The threshold is found by a linesearch between values "inf" and "sup" with "step" thresholds tested.
        The optimal threshold is the one which minimizes the reconstruction error between the shortest_path matrix coming from the thresholded adjacency matrix
        and the original matrix.
    Parameters
    ----------
    C : ndarray, shape (n_nodes,n_nodes)
            The structure matrix to threshold
    inf : float
          The beginning of the linesearch
    sup : float
          The end of the linesearch
    step : integer
            Number of thresholds tested
    """
    dist = []
    search = np.linspace(inf, sup, step)
    for thresh in search:
        Cprime = sp_to_adjacency(C, 0, thresh)
        SC = shortest_path(Cprime, method='D')
        SC[SC == float('inf')] = 100
        dist.append(np.linalg.norm(SC - C))
    return search[np.argmin(dist)], dist

def sp_to_adjacency(C, threshinf=0.2, threshsup=1.8):
    """ Thresholds the structure matrix in order to compute an adjacency matrix.
    All values between threshinf and threshsup are considered representing connected nodes and set to 1. Else are set to 0
    Parameters
    ----------
    C : ndarray, shape (n_nodes,n_nodes)
        The structure matrix to threshold
    threshinf : float
        The minimum value of distance from which the new value is set to 1
    threshsup : float
        The maximum value of distance from which the new value is set to 1
    Returns
    -------
    C : ndarray, shape (n_nodes,n_nodes)
        The threshold matrix. Each element is in {0,1}
    """
    H = np.zeros_like(C)
    np.fill_diagonal(H, np.diagonal(C))
    C = C - H
    C = np.minimum(np.maximum(C, threshinf), threshsup)
    C[C == threshsup] = 0
    C[C != 0] = 1

    return C

def pad_pointclouds(point_clouds, weights, max_shape=-1):
    """
    :meta private:
    """

    if max_shape == -1:
        max_shape = np.max([pc.shape[0] for pc in point_clouds]) + 1
    else:
        max_shape = max_shape + 1
    weights_pad = np.asarray(
        [
            np.concatenate((weight, np.zeros(max_shape - pc.shape[0])), axis=0)
            for pc, weight in zip(point_clouds, weights)
        ]
    )
    point_clouds_pad = np.asarray(
        [
            np.concatenate(
                [pc, np.zeros([max_shape - pc.shape[0], pc.shape[-1]])], axis=0
            )
            for pc in point_clouds
        ]
    )

    weights_pad = weights_pad / weights_pad.sum(axis=1, keepdims=True)

    return (
        point_clouds_pad[:, :-1].astype("float32"),
        weights_pad[:, :-1].astype("float32"),
    )



def S2(x, y, eps, lse_mode = False):                      
    """
    Calculate Sinkhorn Divergnece (S2) between two weighted point clouds

    Params
    x : list
        list with two elements, the first (x[0]) being the point-cloud coordinates and the second (x[1]) being each points weight
    y : list
        list with two elements, the first (y[0]) being the point-cloud coordinates and the second (y[1]) being each points weight
    eps : float
        coefficient of entropic regularization
    lse_mode : bool
        whether to use log-sum-exp mode (if True, more stable for smaller eps, but slower) or kernel mode (default False)
    
    Returns
    S2 : Sinkhorn Divergnece between x and y
    """ 

    x,a = x[0], x[1]
    y,b = y[0], y[1]
        
    ot_solve_xy = linear.solve(
        ott.geometry.pointcloud.PointCloud(x, y, cost_fn=None, epsilon = eps),
        a = a,
        b = b,
        lse_mode=lse_mode,
        min_iterations=0,
        max_iterations=100)

    ot_solve_xx = linear.solve(
    ott.geometry.pointcloud.PointCloud(x, x, cost_fn=None, epsilon = eps),
    a = a,
    b = a,
    lse_mode=lse_mode,
    min_iterations=0,
    max_iterations=100)
    
    ot_solve_yy = linear.solve(
    ott.geometry.pointcloud.PointCloud(y, y, cost_fn=None, epsilon = eps),
    a = b,
    b = b,
    lse_mode=lse_mode,
    min_iterations=0,
    max_iterations=100)
    return(ot_solve_xy.reg_ot_cost - 0.5 * ot_solve_xx.reg_ot_cost - 0.5 * ot_solve_yy.reg_ot_cost)



jit_dist_enc = jax.jit(
            jax.vmap(S2, (0, 0, None, None), 0),
            static_argnums=[2, 3],
        )