# STARDUST
Imaging-based spatial transcriptomics technologies capture the location of transcripts at subcellular resolution, but established methods represent data at the cell level, ignoring subcellular structure.

STARDUST (Subcellular-level Tool for Analyzing RNA Distribution USing optimal Transport) is a method for analyzing the subcellular spatial distribution of RNA molecules. STARDUST uses the Fused Gromov-Wasserstein distance from optimal transport to model gene transcripts in relation to the cell outline.

STARDUST functionalities include:

- de_novo_analysis - Identifies the axes of variation in how one or more genes' transcripts are distributed in cells in a dataset. When multiple genes of interest are given, the model distinguishes between transcripts from differen genes and takes into account gene-gene spatial correlations.
    - UMAP_de_novo_analysis_output - Generates an embedding of cells based on the similarity of their subcellular transcript distributions. 
    - barycenters - Cluster cells based on their subcellular transcript distributions and generate barycenters that are representative of each cluster.

- canonical_analysis - Scores cells based on how similar their transcript distributions (for a specific gene of interest) are to user-specified canonical patterns to look for.
