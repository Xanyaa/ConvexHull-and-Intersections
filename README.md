# Convex Hull and Line Segment Intersection Visualizer

## Overview
This Streamlit application visualizes convex hulls and line segment intersections using advanced computational geometry algorithms. It includes Bentley-Ottmann for intersection detection and Graham Scan, Jarvis March, Brute Force, Quickhull, and Monotone Chain for convex hull construction. Users can interactively add points and segments to see the algorithms in action.

## Features

1. **User Interface**
   - Interactive web interface powered by Streamlit for intuitive user interaction.
   - Supports two main functionalities: Line Segment Intersection and Convex Hull Visualization.

2. **Line Segment Intersection**
   - **Bentley-Ottmann Algorithm**: Efficiently detects intersections among line segments using a sweep line technique.
   - Visualizes the line segments and their intersections dynamically.

3. **Convex Hull Algorithms**
   - **Graham Scan**: Constructs the convex hull by sorting points and using a stack to detect and remove concavities.
   - **Jarvis March (Gift Wrapping)**: Finds the convex hull by wrapping points around the set of points.
   - **Brute Force**: Simple method that checks all combinations of points to form the convex hull.
   - **Quickhull**: Divides the set of points into subsets, recursively finding the hull points.
   - **Monotone Chain**: Constructs the convex hull by sorting points and building lower and upper hulls.

4. **Visualization**
   - Visualizes convex hulls and line segment intersections with matplotlib.
   - Interactive point and segment manipulation for dynamic visualization.

## Algorithms Explained

1. **Bentley-Ottmann Algorithm**
   - Efficient line segment intersection detection using a sweep line and event queue.
   - Handles events for segment endpoints and intersections.

2. **Graham Scan**
   - Sorts points by polar angle and processes them to form the convex hull using a stack.
   - Efficient O(n log n) complexity.

3. **Jarvis March (Gift Wrapping)**
   - Iteratively selects the most counterclockwise point to construct the convex hull.
   - Simple O(nh) complexity, where h is the number of hull points.

4. **Brute Force**
   - Checks every combination of points to determine if they form part of the convex hull.
   - Inefficient but straightforward method.

5. **Quickhull**
   - Recursively finds hull points by partitioning the set of points.
   - Combines elements of quicksort with convex hull construction.

6. **Monotone Chain**
   - Sorts points and constructs the lower and upper hulls separately.
   - Efficient and straightforward method.

## How to Use

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the App
1. Launch the app using Streamlit:
   ```sh
   streamlit run convex-lineintersection.py
   ```
2. Access the application through the provided local URL (typically `http://localhost:8501`).

### Usage
- Choose between Line Segment Intersection or Convex Hull Visualization.
- For Line Segment Intersection:
  - Input coordinates for line segments.
  - Visualize intersections dynamically.
- For Convex Hull Visualization:
  - Add points to the canvas.
  - Select an algorithm to visualize the convex hull.

## Conclusion
This geometry visualization tool leverages Streamlit to offer a seamless user experience for exploring computational geometry algorithms. It provides powerful visualizations and interactive manipulation, making it ideal for both educational and practical applications in geometry.

## License
This project is licensed under the MIT License.

## Contact
For inquiries or issues, please contact saniahasan167@gmail.com.

## Acknowledgements
- Streamlit: https://streamlit.io/
- Matplotlib: https://matplotlib.org/
- NumPy: https://numpy.org/
- SortedContainers: http://www.grantjenks.com/docs/sortedcontainers/
