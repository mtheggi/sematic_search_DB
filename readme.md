# 🌲 KD-Tree: Spatial Indexing for Efficient Data Retrieval

![vectorDB](docs/vectorDB.gif)


## 📰 Introduction 
This project objective is to have Sematic Search Database System that can create indexing on large amount of data, besides it is able to search in the created index for query vectors in a fast
and accurate method.

## 📋Project description

The project focuses on developing an indexing system that efficiently stores and retrieves data utilizing vector space embeddings. Key requirements include:

- **Two-column Database Structure:**
  - Columns: ID, Embedding (vector of dim 70).

- **Top-k Similarity Retrieval:**
  - Retrieve the top-k most similar rows to a given input.

- **Scalability:**
  - Handle large datasets, up to 20 million records.

- **Efficient Query Retrieval:**
  - Quickly retrieve the top 'k' results for a given query (k up to 10).

- **Responsive Performance:**
  - Ensure the system responds within a reasonable time.


## 👀 Overview on the Indexing idea with KD-tree and implementation

### Build Operation:

- **Disk Usage:**
  - Large vector operations on disk due to memory constraints.
  - Memory-constrained operations in-memory.

- **Clustering:**
  - Nodes clustered on disk.
  - Global directory ("output") as the first level of indexing.

- **Algorithm:**
  - External sorting for large datasets.
  - Recursive partitioning and sorting.
  - Switch to internal build for in-memory partitions.
  - Cluster creation at a size threshold.
  - Nodes stored in both internal and leaf nodes.

### Search Operation:

- **Global Directory Search:**
  - Binary search algorithm on the global directory.
  - Multiple clusters may be required.

- **Binary Search-Like:**
  - Compares specific dimensions at each tree level.
  - May result in both right and left nodes being applicable.

- **Cluster Loading:**
  - One cluster loaded at a time.
  - Released when not needed.

### General Notes:
- **Insertion:**
  - Inserted nodes find correct position in the cluster.

- **Thresholds:**
  - Cluster size threshold determined for memory efficiency.

- **Memory Management:**
  - Efficient loading of necessary clusters.



## 🚀 results
<img src="./docs/results.png" alt="result" width="500" >

## Reference
[Project description in more details](https://drive.google.com/file/d/1FkgCurVRJqMou8lOEANdfD2rqZEC6VqC/view)
## contributors
- mohamed Tarek 
- mohamed elsayed 
- salah abotaleb 
- moaz tarek 
- ahmed yasser