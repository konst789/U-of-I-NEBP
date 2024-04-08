# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 16:18:28 2024

@author: lkear
"""

import pandas as pd
import glob
import os

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy.optimize import curve_fit
from skimage.measure import EllipseModel
from scipy.optimize import minimize
import cv2
import statistics


flight=29 #loop this to do more than one intersection at a time

def bootstrap_fit_ellipse(x_data, y_data, num_iterations=1000):
    num_points = len(x_data)
    bootstrap_results = []

    for _ in range(num_iterations):
        # Randomly sample data with replacement
        indices = np.random.choice(num_points, num_points, replace=True)
        sampled_x_data = x_data.iloc[indices]  # Use iloc to index the data
        sampled_y_data = y_data.iloc[indices]  # Use iloc to index the data

        # Calculate least squares fit for the sampled data
        fit_params = least_squares_fit(sampled_x_data, sampled_y_data)

        # Check the quality of least squares fit (example criteria)
        if len(sampled_x_data) >= 1000:
            print("False")
            continue  # Skip further analysis for this iteration

        # Fit an ellipse to the sampled data using OpenCV's fitEllipse function
        data = np.column_stack((sampled_x_data, sampled_y_data))
        ellipse = cv2.fitEllipseDirect(data.astype(np.float32))

        # Calculate residuals for each point to the fitted ellipse
        center = ellipse[0]
        axes = ellipse[1]
        angle = ellipse[2]
        fitted_ellipse = mpatches.Ellipse(center, *axes, angle, fill=False)

        # Calculate distances between points and the ellipse path
        ellipse_path = fitted_ellipse.get_path()
        points_on_ellipse = ellipse_path.contains_points(data)

        distances = np.linalg.norm(data - points_on_ellipse[:, None], axis=1)
        residuals = np.sum(distances)

        # Store the residuals
        bootstrap_results.append(residuals)

    return bootstrap_results

def least_squares_fit(x_data, y_data):
    # Function to calculate the least squares fit
    # Define your least squares fitting algorithm here
    # Return the fitting parameters or statistics

    # For example:
    params = np.polyfit(x_data, y_data, 1)
    return params




df = pd.read_csv(r'C:/Users/gera2396/OneDrive - University of Idaho/Documents/Logan_Code-7-25-23/fkight24/uid24.csv')
intersections = pd.read_csv(r'C:/Users/gera2396/OneDrive - University of Idaho/Documents/Logan_Code-7-25-23/fkight24/uid24_intersections.csv')
results_dir = r'C:/Users/gera2396/OneDrive - University of Idaho/Documents/Logan_Code-7-25-23/fkight24/results1/'

if(not os.path.exists(results_dir)):
    os.mkdir(results_dir)

print("Number of intersections" + str(intersections.shape[0]))

results = []

num_intersections = intersections.shape[0]
for flight in range(num_intersections):

    start_alt=df['Alt'].iloc[0]# grab starting altitude for indexing
    
    intersection=intersections.iloc[flight]
    upper=intersection['z2']
    indexhigh=round(((upper-start_alt)/5))
    
    lower=intersection['z1']
    indexlow=round(((lower-start_alt)/5))
    
    
    section=df.iloc[indexlow:indexhigh]
    
    meanbv2=section['bv2'].mean()
    
    legetitle=['the bv2 is:',meanbv2]
    
    plt.plot(section.Ufiltered,section.Vfiltered)
    plt.xlabel ('U wind Pertubations')
    plt.ylabel('V wind pertubations')
    #legetitle=['BV^2 is:',meanbv2]
    plt.legend(title=legetitle)
    #plt.title("The height is: {:.3f}-{:.3f} meters".format(lower,upper))
    
    plt.show() 
    
    y_data=section['Vfiltered']
    x_data=section['Ufiltered']
    # Generate some example x and y data
    
    data = np.column_stack((x_data, y_data))
    
    # Fit an ellipse to the data using OpenCV's fitEllipse function
    ellipse = cv2.fitEllipseDirect(data.astype(np.float32))
    
    # Extract the ellipse parameters
    center = ellipse[0]
    axes = ellipse[1]
    angle = ellipse[2]
    
    # Create a figure and axis for plotting
    fig, ax = plt.subplots()
    
    # Plot the original data
    ax.scatter(x_data, y_data, label='Data')
    
    # Plot the fitted ellipse
    ax.add_patch(plt.matplotlib.patches.Ellipse(center, *axes, angle, fill=False, color='red', label='Fitted Ellipse'))
    
    # Set axis limits to ensure the ellipse fits within the plot
    x_min = min(x_data) - 1
    x_max = max(x_data) + 1
    y_min = min(y_data) - 1
    y_max = max(y_data) + 1
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    
    # Set axis labels and legend
    ax.set_xlabel('Zonal Wind Perturbations')
    ax.set_ylabel('Meridional Wind Perturbations')
    ax.legend()
    
    plt.grid()
    plt.axis('equal')
    plt.title("The height is: {:.3f}-{:.3f} meters".format(lower,upper))
    plt.show()
    print(center)
    print(axes)
    print(angle)
    
    # Calculate the covariance matrix
    cov_matrix = np.cov(x_data, y_data)
    
    # Calculate the eigenvalues and eigenvectors of the covariance matrix
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    
    # Find the index of the eigenvalue corresponding to the major axis
    major_index = np.argmax(eigenvalues)
    
    # Get the corresponding eigenvector
    major_axis_vector = eigenvectors[:, major_index]
    
    # Calculate the angle of the major axis (in radians) relative to the horizontal axis
    angle_radians = np.arctan2(major_axis_vector[1], major_axis_vector[0])
    
    # Convert the angle to degrees
    angle_degrees = np.degrees(angle_radians)
    
    # Determine if the ellipse is clockwise or counterclockwise
    if angle_degrees < 0:
        orientation = "Clockwise"
    else:
        orientation = "Counterclockwise"
    
    print(orientation)
    
    
    # Your existing code here...
    
    # Extracting x_data and y_data from section DataFrame
    x_data = section['Ufiltered']
    y_data = section['Vfiltered']
    
    # Perform bootstrap to assess the fit quality
    bootstrap_results = bootstrap_fit_ellipse(x_data, y_data)
    
    # Plotting the bootstrap results
    # plt.hist(bootstrap_results, bins=30, edgecolor='black')
    # plt.xlabel('Sum of squared residuals')
    # plt.ylabel('Frequency')
    # plt.title('Bootstrap Results for Fitted Ellipse')
    # plt.show()
    
    print(statistics.mean(bootstrap_results))
    coriollisFreq=float(np.sin(df['Lat'].head(1)*np.pi/180)*4*np.pi/24)
    bigax=axes[1]
    smallax=axes[0]
    axesratio=bigax/smallax
    intrinsic=coriollisFreq*axesratio
    #intrinsic=to_float(intrinsic1)
    results.append({
        'z1': lower,
        'z2': upper,
        'center_x': center[0],
        'center_y': center[1],
        'a': axes[0],
        'b': axes[1],
        'angle': angle,
        'direction': orientation,
        'intrinsic rads/day': intrinsic,
        'fit_accuracy': statistics.mean(bootstrap_results)
        }) 
    # Assess the quality of fit (e.g., confidence interval, etc.) using bootstrap_results
    # You can calculate confidence intervals, mean, or other statistics from the bootstrap results

df_results = pd.DataFrame(results)

print(df_results)

df_results.to_csv(results_dir + 'flight24.csv', sep=',', index=False, encoding='utf-8')
