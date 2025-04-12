import numpy as np
import pandas as pd
from umap import umap_

import ot
from ot.gromov import fused_gromov_wasserstein, fgw_barycenters
from sklearn.cluster import AgglomerativeClustering

import matplotlib.pyplot as plt
from matplotlib import patches as mpatches
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import networkx as nx

from stardust.utils import *

class Stardust():

    def __init__(self,
                 data):
        '''
        Data should be provided as a DataFrame with columns
        - cell: cell ID
        - gene: gene of the transcript
        - x: x coordinate of the transcript
        - y: y coordinate of the transcript

        '''
        self.data = data
    
    def prep_for_de_novo(self, cells, genes_of_interest, num_outline_points):
        '''
        Prepares the data for the FGW algorithm by
        - getting convex hull outline and outline points
        - scaling cell to unit circle
        - separating RNA transcripts by gene of interest
        
        Parameters
        data : pd.DataFrame
            DataFrame containing the RNA transcripts.
 
        Returns
        rnas : list
            len(rnas) = len(genes_of_interest)
                rnas[i] = list of RNA transcripts for gene i
                len(rnas[i]) = len(cells)
                    rnas[i][j] = np.array of RNA transcripts for gene i in cell j
        outlines : list
            len(outlines) = len(cells)
                outlines[i] = np.array of outline points for cell i
        sep_idxs : list
            len(sep_idxs) = len(cells)
                sep_idxs[i] = list of indices separating RNA transcripts for each
                gene in cell i
            '''
        
        data = self.data

        num_genes_of_interest = len(genes_of_interest)
        rnas = [[] for _ in range(num_genes_of_interest)]
        outlines = []
        sep_idxs = []

        for cell_id in cells:
            # convex hull
            cell_data = data[data['cell']==cell_id]
            points = cell_data[['x', 'y']].values
            outline = get_evenly_spaced_outline(points, num_outline_points=num_outline_points)

            # sep_idx between types of points
            concat_rna = []
            sep_idx = [0]

            for gene in genes_of_interest:
                concat_rna.extend(cell_data.loc[(cell_data['gene'] == gene), ['x', 'y']].values)
                sep_idx.append(len(concat_rna))
            # scale both
            scaled_rna_coords, scaled_outline, fit, circle = scale_cell_SVD(np.array(concat_rna), outline)
            # add to lists
            for _ in range(num_genes_of_interest):
                rnas[_].append(scaled_rna_coords[sep_idx[_]:sep_idx[_+1]])
            outlines.append(scaled_outline)
            # save sep_idx
            sep_idxs.append(sep_idx)
        
        self.cells = cells
        self.genes_of_interest = genes_of_interest
        self.rnas = rnas
        self.outlines = outlines
        self.sep_idxs = sep_idxs

        return rnas, outlines, sep_idxs


    def de_novo_analysis(self, cells, genes_of_interest, num_outline_points = 50, alpha = 1e-1):
        '''
        Get a cell-cell distance matrix showing how similar cells are in their subcellular transcript distributions. 
        The function distinguishes between different genes' transcripts and accounts for gene-gene spatial correlation patterns.
        
        Parameters
        cells : list
            List of cell IDs to analyze
        genes_of_interest : list
            List of genes to analyze
        num_outline_points : int
            Number of points to use for the outline

        Returns
        dist_mat : np.array
            Cell-cell distance matrix
        transport_plans : list
            all pairwise transport plans between cells, visualize with heatmap to make sure outline points and RNA points transport within their types
            len(transport_plans) = num_cells * (num_cells - 1) / 2
        ''' 
        self.prep_for_de_novo(cells, genes_of_interest, num_outline_points)          
        rnas, outlines, sep_idxs = self.rnas, self.outlines, self.sep_idxs

        # prep for indexing upper triangle
        num_cells = len(outlines)
        num_genes_of_interest = len(rnas)
        upper_triangular_ind = np.stack(np.triu_indices(num_cells, 1), axis = 1)
        out = []
        transport_plans = []

        # get everything needed for FGW
        all_Ys = []
        all_Cs = []
        all_ps = []
        for i in range(num_cells):
            xs = np.concatenate([rnas[_][i] for _ in range(num_genes_of_interest)] + [outlines[i]])
            ys = np.zeros(len(xs)) 
            for k in range(num_genes_of_interest):
                ys[sep_idxs[i][k]: sep_idxs[i][k+1]] = k+1
            ys = np.array(ys).reshape(-1,1)
            p = np.concatenate(
                [1/(num_genes_of_interest+1) * ot.unif(len(rnas[_][i])) for _ in range(num_genes_of_interest)] 
                + [1/(num_genes_of_interest+1) * ot.unif(len(outlines[i]))])
            C1 = ot.dist(xs)    
            all_Ys.append(ys)
            all_Cs.append(C1)
            all_ps.append(p)

        # create dist matrix
        dist_mat = np.zeros((num_cells, num_cells))
        # compute pairwise GW dists
        for i,j in upper_triangular_ind:
            M = ot.dist(all_Ys[i], all_Ys[j]) # dist mat between ys and yt (across-features distance matrix)
            # Compute FGW
            Gwg, logw = fused_gromov_wasserstein(M, all_Cs[i], all_Cs[j], all_ps[i], all_ps[j], loss_fun='square_loss', alpha=alpha, verbose=False, log=True)
            transport_plans.append(Gwg)
            dist_mat[i, j] = logw['cost']
            dist_mat[j, i] = dist_mat[i, j] 

        self.dist_mat = dist_mat
        self.transport_plans = transport_plans
        self.all_Ys = all_Ys
        self.all_Cs = all_Cs
        self.all_ps = all_ps

    def UMAP_de_novo_analysis_output(self, inset_size = 0.05, fig_size = (27, 23), cmap='Set1'):
        '''
        Visualize the FGW dist matrix output using UMAP.
        Each cell is represented by a small image in the 2D UMAP.
        The color of the points represents the genes of interest.
        The outline of the cell is shown in black.
        
        Parameters
        inset_size : float
            Size of the inset plots as a fraction of figure size
        '''
        dist_mat, rnas, outlines, genes_of_interest = self.dist_mat, self.rnas, self.outlines, self.genes_of_interest
        
        if hasattr(self, 'embedding'):
            embedding = self.embedding
        else:
            embedding = umap_.UMAP(metric="precomputed").fit_transform(dist_mat)

        fig, ax = plt.subplots()
        fig.set_size_inches(fig_size)

        # Create legend with gene colors
        colormap = cm.get_cmap(cmap, 10)
        handles = [mpatches.Patch(color=colormap(idx), label=gene) for idx, gene in enumerate(genes_of_interest)]
        ax.legend(handles=handles, loc='upper right')
        ax.set_axis_off()

        def generate_small_plot(ax, i, colormap, genes_of_interest, rnas, outlines):
            # Plot each gene in a different color
            for gene_i, gene in enumerate(genes_of_interest):
                ax.scatter(rnas[gene_i][i][:,0], rnas[gene_i][i][:,1], c=[colormap(gene_i) for _ in range(len(rnas[gene_i][i]))], s=3, label=gene)
            ax.plot(outlines[i][:, 0], outlines[i][:, 1], c='k')
            ax.plot([outlines[i][-1, 0], outlines[i][0, 0]], [outlines[i][-1, 1], outlines[i][0, 1]], c='k')  # draw line from last of outline to first of outline
            ax.set_xticks([])
            ax.set_yticks([])
            if hasattr(self, 'cluster_labels'):
                ax.text(0.95, 0.95, f"{self.cluster_labels[i]}",
                transform=ax.transAxes,    # So x=0.95, y=0.95 is 95% of the inset Axes
                ha='right', va='top',
                fontsize=8)

        # Create subplots
        x_max = np.max(embedding[:, 0])
        x_min = np.min(embedding[:, 0])
        y_max = np.max(embedding[:, 1])
        y_min = np.min(embedding[:, 1])
        for i, (xi, yi) in enumerate(embedding):
            inset_ax = ax.inset_axes([(xi-x_min) / (x_max-x_min), (yi-y_min) / (y_max-y_min + .5), inset_size, inset_size])
            generate_small_plot(inset_ax, i, colormap, genes_of_interest, rnas, outlines)
        
        self.embedding = embedding
        self.colormap = colormap
        self.UMAP_using_FGW_output_fig = fig


    def barycenters(self, n_clusters=10, sizebary = 200, alpha=1e-1, figsize=None, nrows=None, ncols = None):
        '''
        Cluster cells based on their subcellular distribution and generate a barycenter (archetype) for each cluster.

        Parameters
        n_clusters : int
            Number of clusters to generate
        '''
        dist_mat, all_Ys, all_Cs, all_ps, colormap = self.dist_mat, self.all_Ys, self.all_Cs, self.all_ps, self.colormap
        
        # cluster cells based on dist_mat
        clustering = AgglomerativeClustering(n_clusters=n_clusters, metric="precomputed", linkage='average').fit(dist_mat)
        labels = clustering.labels_.astype(str)
        clusters = sorted(set(labels), key=int)

        if not figsize:
            figsize = (5 * n_clusters, 5)
        if not nrows or not ncols:
            nrows = 1
            ncols = n_clusters

        fig, ax = plt.subplots(figsize=figsize)

        # generate barycenter for each cluster
        for idx in range(n_clusters):
            print(f"Generating barycenter for cluster {idx+1} / {n_clusters}...")
            cluster_id = clusters[idx]
            indices = np.where(labels == cluster_id)[0]    

            Ys = [all_Ys[i] for i in indices]
            Cs = [all_Cs[i] for i in indices]
            ps = [all_ps[i] for i in indices]

            A, C, log = fgw_barycenters(sizebary, Ys, Cs, ps, alpha=alpha, log=True)
            bary = nx.from_numpy_array(sp_to_adjacency(C, threshinf=0, threshsup=find_thresh(C, sup=100, step=100)[0]))
            for i, v in enumerate(A.ravel()):
                bary.add_node(i, attr_name=v)

            pos = nx.kamada_kawai_layout(bary)
            xy = np.array(list(pos.values())) # position
            vals = [round(val) for val in nx.get_node_attributes(bary, 'attr_name').values()] # color

            point_colors = ["k" if val==0 else colormap(val-1) for val in vals]

            plt.subplot(nrows, ncols, idx+1)
            plt.scatter(xy[:,0], xy[:,1], color = point_colors, s=30)

        self.cluster_labels = labels
        self.barycenter_fig = fig


    def cells_in_barycenter_clusters(self):
        ''' 
        See which cells are in each barycenter cluster.
        Returns a dictionary where keys are barycenter labels and values are the IDs of the cells used to generate each barycenter. 
        '''
        labels = sorted(set(self.cluster_labels))
        return dict(zip(labels, [self.cells[self.cluster_labels==i] for i in labels]))


    def prep_for_canonical(self, cells, genes_of_interest, num_outline_points):
        data = self.data

        num_genes_of_interest = len(genes_of_interest)
        rnas = []
        outlines = []
        names = []

        for cell_id in cells:
            # convex hull
            cell_data = data[data['cell']==cell_id]
            points = cell_data[['x', 'y']].values
            outline = get_evenly_spaced_outline(points, num_outline_points=num_outline_points)

            # sep_idx between types of points
            concat_rna = []
            sep_idx = [0]
            for gene in genes_of_interest:
                concat_rna.extend(cell_data.loc[(cell_data['gene'] == gene), ['x', 'y']].values)
                sep_idx.append(len(concat_rna))
                names.append(f'{gene}_{cell_id}')
            # scale both
            scaled_rna_coords, scaled_outline, fit, circle = scale_cell_SVD(np.array(concat_rna), outline)
            # add to lists
            for _ in range(num_genes_of_interest):
                rnas.append(scaled_rna_coords[sep_idx[_]:sep_idx[_+1]])
                outlines.append(scaled_outline)
        
        self.cells_genes_c = names
        self.rnas_c = rnas
        self.outlines_c = outlines
        return rnas, outlines, names
    

    def canonical_analysis(self, cells, genes_of_interest, templates_path, canonical_patterns, canonical_rnas = None, canonical_outlines = None, canonical_n_cells = 1, canonical_n_spots=40, canonical_proportion_pattern=0.9, num_outline_points=50, return_canonicals=False):
        '''
        See how similar transcript distributions are to user-specified canonical patterns.
        
        Parameters
        cells : list
            List of cell IDs to analyze
        genes_of_interest : list
            List of genes to analyze. Unlike de novo analysis, canonical analysis compares each gene in each cell separately.
        canonical_patterns : list
            List of canonical patterns to compare to. Valid patterns include 'intranuclear', 'perinuclear', 'nuclear_edge', 'extranuclear', 'pericellular', 'cell_edge', 'foci', and 'protrusion'.
            
        Returns
        scores_df : pd.DataFrame
            Similarity score of each gene in each cell to the canonical distribution patterns.
        ''' 
        rnas, outlines, names = self.prep_for_canonical(cells, genes_of_interest, num_outline_points)  
        

        if canonical_rnas is None or canonical_outlines is None:
            canonical_rnas, canonical_outlines = simulate_data(templates_path, n_cells = canonical_n_cells, n_spots = canonical_n_spots, proportion_pattern = canonical_proportion_pattern, patterns = canonical_patterns, return_raw=True)

        # prep for FGW
        canonical_Ys = []
        canonical_Cs = []
        canonical_ps = []

        data_Ys = []
        data_Cs = []
        data_ps = []

        for i in range(len(canonical_rnas)): 
            len_rna_i = len(canonical_rnas[i])
            len_outline_i = len(canonical_outlines[i])
            xs = np.concatenate([canonical_rnas[i], canonical_outlines[i]])
            ys = np.concatenate([np.zeros(len_rna_i), np.ones(len_outline_i)]).reshape(-1, 1)
            p = np.concatenate([0.6 * ot.unif(len_rna_i), 0.4 * ot.unif(len_outline_i)])
            C1 = ot.dist(xs)    
            canonical_Ys.append(ys)
            canonical_Cs.append(C1)
            canonical_ps.append(p)
    

        for j in range(len(rnas)):      
            len_rna_j = len(rnas[j])
            len_outline_j = len(outlines[j])
            xt = np.concatenate([rnas[j], outlines[j]])
            yt = np.concatenate([np.zeros(len_rna_j), np.ones(len_outline_j)]).reshape(-1, 1)
            q = np.concatenate([0.6 * ot.unif(len_rna_j), 0.4 * ot.unif(len_outline_j)])  # weighting so that same mass for rna and reference, not forced to transport across types
            C2 = ot.dist(xt)    
            data_Ys.append(yt)
            data_Cs.append(C2)
            data_ps.append(q)
        
        distT = np.zeros((len(canonical_rnas), len(rnas)))
        for i in range(len(canonical_rnas)):  
            ys = canonical_Ys[i]
            C1 = canonical_Cs[i]
            p = canonical_ps[i] 
            for j in range(len(rnas)):
                yt = data_Ys[j]
                C2 = data_Cs[j]
                q = data_ps[j]

                # Compute FGW
                M = ot.dist(ys, yt)  # dist mat between ys and yt (across-features distance matrix)
                Gwg, logw = fused_gromov_wasserstein(M, C1, C2, p, q, loss_fun='square_loss', alpha=1e-1, verbose=False, log=True)
                distT[i,j] =logw['cost']
        
        # Transpose, demean to remove effects of transcript abundance
        dist_raw = distT.T
        dist_demeaned_row = dist_raw - np.mean(dist_raw, axis=0)
        dist = dist_demeaned_row - np.mean(dist_demeaned_row, axis=1).reshape(-1, 1)

        self.dist_c = dist

        # Save as df, take negative so it's a similarity score
        scores_df = pd.DataFrame(-dist, columns=canonical_patterns)
        cell_index = np.repeat(cells, len(genes_of_interest))
        gene_index = np.tile(genes_of_interest, len(cells))
        scores_df.insert(0, 'cell', cell_index)
        scores_df.insert(1, 'gene', gene_index)

        self.canonical_rnas = canonical_rnas
        self.canonical_outlines = canonical_outlines
        self.canonical_patterns = canonical_patterns


        if return_canonicals == True:
            return scores_df, (canonical_rnas, canonical_outlines)
        
        return scores_df
    
    def show_canonicals(self, s = 50):
        '''
        Visualize the canonical patterns.
        '''
        rnas = self.canonical_rnas
        outlines = self.canonical_outlines
        patterns = self.canonical_patterns
        n_canonicals = len(rnas)

        fig = plt.figure(figsize=(12 * n_canonicals, 12))
        for i in range(n_canonicals):
            plt.subplot(1, n_canonicals, i+1)
            plt.title(patterns[i])
            plt.scatter(rnas[i][:,0], rnas[i][:,1], c='dodgerblue', s=s)
            plt.plot(outlines[i][:, 0], outlines[i][:, 1], c='k')
            plt.plot([outlines[i][-1, 0], outlines[i][0, 0]], [outlines[i][-1, 1], outlines[i][0, 1]], c='k')  
            plt.xticks([])
            plt.yticks([])
        return fig


    