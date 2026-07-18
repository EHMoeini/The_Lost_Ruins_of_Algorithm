# The Lost Ruins of Algorithmia

> Solutions to the **Algorithm Design Final Project** at Iran University of Science and Technology, implemented in **Python**.

This repository contains solutions to four independent algorithmic problems set in a common grid-based environment. Each problem focuses on a different algorithmic concept, ranging from graph traversal to network flow.

The full project specification is available in **`project.pdf`**, and a detailed explanation of the implementation, correctness proofs, and complexity analysis is provided in **`report.pdf`**.

---

## Problems

| Problem | Description | Main Algorithm |
|---------|-------------|----------------|
| **Problem 1 – The Time-Limited Expedition** | Maximize collected treasures under a move limit. | **BFS over a 4D state space (Bitmask)** |
| **Problem 2 – Mapping the Ruins** | Compute the average shortest distance between all reachable cells. | **Repeated BFS (All-Pairs Shortest Paths)** |
| **Problem 3 – The Mandatory Collection** | Find the shortest path while collecting at least **K** treasures. | **BFS over a 3D state space (Bitmask)** |
| **Problem 4 – The Rescue Mission** | Compute the maximum number of vertex-disjoint paths. | **Maximum Flow (Edmonds–Karp with Node Splitting)** |

---

## Features

- Python implementation
- Independent implementation for each problem
- Organized test cases for every solution
- Detailed implementation report
- Complexity analysis for every algorithm
- Clean and modular project structure

---

## Running the Code

Each problem is implemented independently.

```python
from solutions.p1 import solve
```

or run the corresponding test script:

```bash
python tests/test_p1.py
```

Replace `p1` with `p2`, `p3`, or `p4` as needed.

---

## Included Documents

- **project.pdf** – Original assignment specification.
- **report.pdf** – Explanation of the implemented algorithms, correctness proofs, design decisions, and complexity analysis.

---

## Author

**Ehsan Moeini**

Computer Science Student  
Iran University of Science and Technology