# applied-math-thesis
## Genetic Algorithms for Cluster Analysis: Health Insurance Coverage and Pollution
<p><sub>Note: This program was intended to accompany research rather than being for personal execution.<sub><p>

### Description of files
**final_paper.pdf**: Final research paper. Includes background information on clustering methods, the mathematics and algorithms behind the specific clustering methods used, and the results from each method on census health insurance coverage data.

**research_poster.pdf**: Poster that I presented at the Nebraska Conference for Undergraduate Women in Mathematics (NCUWM). Summarizes the research and results.

**getCensusData.py**: Pulls health insurance coverage data using the Census API. Includes descriptions of each variable collected.

**cleaning_env_data.py**: Joins environmental pollution data previously downloaded from the CDC. Decides which variables to include by trying to maximize counties with no missing data.

**kmeans_gmm.py**: Performs both k-Means and Gaussian Mixture Model clustering with 2-50 clusters of health insurance census data. Compares Davies-Bouldin Index and Silhouette Index for k-Means and GMM by plotting.

**final_genetic_algorithm**: Creates custom genetic algorithm, with functions divided into the standard algorithm components. Further information and justification for algorithm decisions can be found in **final_paper.pdf**. For personal use, decrease number of chromosomes and generations.

**anova_analysis.Rmd**: Basic ANOVA performed on environmental pollutants of the final clusters from execution of genetic algorithm.
