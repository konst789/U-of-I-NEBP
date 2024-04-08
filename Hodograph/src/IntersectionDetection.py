# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 16:16:51 2024

@author: lkear
"""

import pandas as pd
from shapely.geometry import Point
from shapely.geometry import LineString


df4 = pd.read_csv(r'C:/Users/konge/OneDrive - University of Idaho/Documents/Logan_Code-7-25-23/fkight24/uid24.csv')
df2=pd.DataFrame([df4.Ufiltered,df4.Vfiltered,df4.Alt]).transpose()
df2=df2.rename(columns={'Ufiltered':'x','Vfiltered':'y','Alt':'z'})
data_xyz = df2[['x', 'y','z']].values.tolist()


min_z_distance = 100
max_z_distance = 1800

# Create a list to store intersection points and their z values
crossing_points = []

# Convert (x, y, z) coordinates to Point objects
points = [Point(x, y, z) for x, y, z in data_xyz]

# Check for intersections while considering the z distance criteria
for i in range(len(points) - 1):
    line1 = LineString([points[i], points[i + 1]])

    for j in range(i + 2, len(points)):
        line2 = LineString([points[j], points[j - 1]])

        if line1.intersects(line2):
            intersection = line1.intersection(line2)
            if intersection.geom_type == 'Point':
                x_intersection, y_intersection = intersection.x, intersection.y
                z_intersection1 = points[i].z
                z_intersection2 = points[j].z

                z_distance1 = abs(z_intersection1 - z_intersection2)
                if min_z_distance <= z_distance1 <= max_z_distance:
                    crossing_points.append((x_intersection, y_intersection, z_intersection1, z_intersection2))

# Print the intersection points and their z values
for x, y, z1, z2 in crossing_points:
    print(f"Intersection at ({x}, {y}), z1: {z1}, z2: {z2}")
    columns = ['x', 'y','z1','z2']
    df1 = pd.DataFrame(crossing_points, columns=columns)
    df1.to_csv(r'C:/Users/konge/OneDrive - University of Idaho/Documents/Logan_Code-7-25-23/fkight24/uid24_intersections.csv', encoding='utf-8')
