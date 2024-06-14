import streamlit as st
import matplotlib.pyplot as plt
from sortedcontainers import SortedList
import numpy as np

# Event class and Bentley-Ottmann algorithm
class Event:
    def __init__(self, x, segment, event_type):
        self.x = x
        self.segment = segment
        self.event_type = event_type  

    def __lt__(self, other):
        return self.x < other.x

def handle_event(event, status, intersections):
    if event.event_type == 'left':
        status.add(event.segment)
        above, below = status.bisect_right(event.segment), status.bisect_left(event.segment)
        if above < len(status) and below > 0 and find_intersection(status[above], status[below]):
            intersections.append((event.x, find_intersection_point(status[above], status[below])))
    elif event.event_type == 'right':
        index = status.bisect_left(event.segment)
        if index > 0 and index < len(status) and find_intersection(status[index - 1], status[index]):
            intersections.append((event.x, find_intersection_point(status[index - 1], status[index])))
        status.discard(event.segment)

def find_intersection(segment1, segment2):
    x1, y1, x2, y2 = segment1
    x3, y3, x4, y4 = segment2

    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if det == 0:
        return False  # Lines don't intersect

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

    if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2) and \
       min(x3, x4) <= px <= max(x3, x4) and min(y3, y4) <= py <= max(y3, y4):
        return True
    else:
        return False

def find_intersection_point(segment1, segment2):
    x1, y1, x2, y2 = segment1
    x3, y3, x4, y4 = segment2

    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

    return px, py

def visualize_line_segments(segments):
    fig, ax = plt.subplots()

    for segment in segments:
        ax.plot([segment[0], segment[2]], [segment[1], segment[3]], 'b-')

    ax.set_xlim(min(segment[0] for segment in segments) - 1, max(segment[2] for segment in segments) + 1)
    ax.set_ylim(min(segment[1] for segment in segments) - 1, max(segment[3] for segment in segments) + 1)

    return fig, ax

def bentley_ottmann_algorithm(segments):
    events = []
    for segment in segments:
        events.append(Event(segment[0], segment, 'left'))
        events.append(Event(segment[2], segment, 'right'))

    events.sort()

    status = SortedList()
    intersections = []

    for event in events:
        handle_event(event, status, intersections)

    return intersections

def graham_scan(points):
    points = sorted(points, key=lambda x: (x[0], x[1]))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return np.array(lower[:-1] + upper[:-1])

def jarvis_march(points):
    hull = []
    start = points[np.argmin(points[:, 0])]
    point = start
    while True:
        hull.append(point)
        endpoint = points[0]
        for candidate in points:
            if (endpoint == point).all() or np.cross(candidate - point, endpoint - point) > 0:
                endpoint = candidate
        point = endpoint
        if (endpoint == start).all():
            break
    return np.array(hull)

def brute_force(points):
    def is_right_turn(p1, p2, p3):
        return (p3[1] - p1[1]) * (p2[0] - p1[0]) < (p2[1] - p1[1]) * (p3[0] - p1[0])

    n = len(points)
    if n < 3:
        return points

    hull = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            left = True
            for k in range(n):
                if k == i or k == j:
                    continue
                if is_right_turn(points[i], points[j], points[k]):
                    left = False
                    break
            if left:
                hull.append((points[i], points[j]))

    hull = np.unique(np.array(hull).reshape(-1, 2), axis=0)
    hull = hull[hull[:, 0].argsort()]
    return hull

def quickhull(points):
    def add_hull_points(p1, p2, points, hull):
        if not points:
            return
        dist = -1
        for p in points:
            d = np.cross(p2 - p1, p - p1)
            if d > dist:
                dist = d
                farthest = p
        hull.append(farthest)
        points = [p for p in points if np.cross(farthest - p1, p - p1) > 0 or np.cross(p2 - farthest, p - farthest) > 0]
        add_hull_points(p1, farthest, [p for p in points if np.cross(farthest - p1, p - p1) > 0], hull)
        add_hull_points(farthest, p2, [p for p in points if np.cross(p2 - farthest, p - farthest) > 0], hull)

    if len(points) < 3:
        return points

    points = sorted(points, key=lambda p: (p[0], p[1]))
    p1, p2 = points[0], points[-1]
    hull = [p1, p2]

    left_set = [p for p in points if np.cross(p2 - p1, p - p1) > 0]
    right_set = [p for p in points if np.cross(p2 - p1, p - p1) < 0]

    add_hull_points(p1, p2, left_set, hull)
    add_hull_points(p2, p1, right_set, hull)

    hull = np.array(hull)
    hull = hull[hull[:, 0].argsort()]
    return hull

# def monotone_chain(points):
#     points = sorted(points.tolist())
    
#     if len(points) <= 1:
#         return points

#     lower = []
#     for p in points:
#         while len(lower) >= 2 and np.cross(lower[-1] - lower[-2], p - lower[-1]) <= 0:
#             lower.pop()
#         lower.append(p)

#     upper = []
#     for p in reversed(points):
#         while len(upper) >= 2 and np.cross(upper[-1] - upper[-2], p - upper[-1]) <= 0:
#             upper.pop()
#         upper.append(p)

#     return np.array(lower[:-1] + upper[:-1])

def monotone_chain(points):
    points = sorted(map(tuple, points))  # Ensure points are tuples and sorted

    if len(points) <= 1:
        return points

    def to_array(p):
        return np.array(p)

    lower = []
    for p in points:
        while len(lower) >= 2 and np.cross(to_array(lower[-1]) - to_array(lower[-2]), to_array(p) - to_array(lower[-1])) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and np.cross(to_array(upper[-1]) - to_array(upper[-2]), to_array(p) - to_array(upper[-1])) <= 0:
            upper.pop()
        upper.append(p)

    return np.array(lower[:-1] + upper[:-1])

def visualize_hull(points, hull):
    fig, ax = plt.subplots()
    ax.plot(points[:, 0], points[:, 1], 'o')
    if len(hull) > 0:
        hull = np.append(hull, [hull[0]], axis=0)  # Closing the hull loop
        ax.plot(hull[:, 0], hull[:, 1], 'r--', lw=2)
    return fig

def main():
    st.title("Convex Hull and Line Segment Intersection Visualizer")

    option = st.sidebar.selectbox(
        "Select an option",
        ("Line Segment Intersection", "Visualize Graham Scan", "Visualize Jarvis March",
         "Visualize Brute Force", "Visualize Quickhull", "Visualize Monotone Chain")
    )

    if option == "Line Segment Intersection":
        st.subheader("Line Segment Intersection Visualization")
        st.write("Enter the coordinates for each line segment:")
        
        segments = []
        num_segments = st.number_input("Number of line segments", min_value=1, value=1, step=1)

        for i in range(num_segments):
            col1, col2, col3, col4 = st.columns(4)
            x1 = col1.number_input(f"x1-{i+1}", value=0.0)
            y1 = col2.number_input(f"y1-{i+1}", value=0.0)
            x2 = col3.number_input(f"x2-{i+1}", value=1.0)
            y2 = col4.number_input(f"y2-{i+1}", value=1.0)

            segments.append((x1, y1, x2, y2))

        if st.button("Visualize"):
            fig, ax = visualize_line_segments(segments)
            intersections = bentley_ottmann_algorithm(segments)
            for intersection in intersections:
                ax.plot(intersection[0], intersection[1], 'ro')
            st.pyplot(fig)

    else:
        st.subheader("Convex Hull Visualization")
        st.write("Click on the canvas to add points for visualization.")

        # Placeholder for canvas interaction (Replace with actual canvas implementation)
        canvas_points = []
        canvas_size = st.slider("Canvas Size", 200, 800, 400, step=100)
        if st.button("Clear Canvas"):
            canvas_points.clear()

        st.write("Choose one of the algorithms to visualize:")

        if st.button("Add Random Points"):
            new_points = np.random.rand(10, 2) * canvas_size
            canvas_points.extend(new_points.tolist())
        
        points = np.array(canvas_points)

        if len(points) > 0:
            st.write("Number of points:", len(points))
            st.write(points)

            if option == "Visualize Graham Scan":
                hull = graham_scan(points)
            elif option == "Visualize Jarvis March":
                hull = jarvis_march(points)
            elif option == "Visualize Brute Force":
                hull = brute_force(points)
            elif option == "Visualize Quickhull":
                hull = quickhull(points)
            elif option == "Visualize Monotone Chain":
                hull = monotone_chain(points)

            fig = visualize_hull(points, hull)
            st.pyplot(fig)

if __name__ == "__main__":
    main()