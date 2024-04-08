# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 16:03:57 2024

@author: gera2396
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
import metpy 
import metpy.calc

flight_number='01'

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




#df = pd.read_csv(r'C:/Users/gera2396/OneDrive - University of Idaho/NASA Ballonn/Lakeview oregon data/intersections/Flight07_intersections.csv')
df = pd.read_csv(fr'C:\Users\konge\OneDrive - University of Idaho\NASA Ballonn\North Springfield pennsylvania data\filtered profiles\Flight_{flight_number}.csv')

intersections = pd.read_csv(fr'C:\Users\konge\OneDrive - University of Idaho\NASA Ballonn\North Springfield pennsylvania data\intersections/Flight{flight_number}.csv')

#intersections = pd.read_csv(r'C:/Users/gera2396/OneDrive - University of Idaho/NASA Ballonn/Lakeview oregon data/intersections/Flight07_intersections.csv')
results_dir = r'C:\Users\konge\OneDrive - University of Idaho\NASA Ballonn\North Springfield pennsylvania data\Hodograph results/'

# if(not os.path.exists(results_dir)):
#     os.mkdir(results_dir)

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
    time_start=section['Time'].iloc[0]
    time_end=section['Time'].iloc[-1]
   #  #legetitle=['Hodograph Analysis ']
   #  #legetitle=['the bv2 is:',meanbv2]
   #  plt.plot(section.Ufiltered,section.Vfiltered)
   #  plt.xlabel ('U wind Pertubations')
   #  plt.ylabel('V wind pertubations')
   #  #legetitle=['BV^2 is:',meanbv2]
   #  #plt.legend(title=legetitle)
   # #plt.xlim([-4,4])
   #  #plt.ylim([-4,4])
   #  plt.title("The height is: {:.3f}-{:.3f} meters".format(lower,upper))
    
   #  plt.show() 
    
    y_data=section['Vfiltered']
    x_data=section['Ufiltered']

    
    data = np.column_stack((x_data, y_data))
    
    # Fit an ellipse to the data using OpenCV's fitEllipse function
    ellipse = cv2.fitEllipseDirect(data.astype(np.float32))
    
    # Extract the ellipse parameters
    center = ellipse[0]
    axes = ellipse[1]
    angle = ellipse[2]
    
    #Create a figure and axis for plotting
    # fig, ax = plt.subplots()
    
    # # Plot the original data
    # ax.scatter(x_data, y_data, label='Data')
    
    # # Plot the fitted ellipse
    # ax.add_patch(plt.matplotlib.patches.Ellipse(center, *axes, angle, fill=False, color='red', label='Fitted Ellipse'))
    
    # # Set axis limits to ensure the ellipse fits within the plot
    # x_min = min(x_data) - 1
    # x_max = max(x_data) + 1
    # y_min = min(y_data) - 1
    # y_max = max(y_data) + 1
    # ax.set_xlim(x_min, x_max)
    # ax.set_ylim(y_min, y_max)
    
    # #Set axis labels and legend
    # ax.set_xlabel('u Wind Perturbations')
    # ax.set_ylabel('v Wind Perturbations')
    # ax.legend()
    
    # plt.grid()
    # plt.axis('equal')
    # #plt.title("The height is: {:.3f}-{:.3f} meters".format(lower,upper))
    # plt.show()
    # print(center)
    # print(axes)
    # print(angle)
    
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
        orientation = "upward"
    else:
        orientation = "downward"
    
    #print(orientation)
    
    #Temp vs wind
    x_data1=section['Ufiltered']+section['Vfiltered']
    y_data1=section['TemperatureFiltered']
    #plt.plot(y_data1, x_data1)
    # Calculate the covariance matrix
    cov_matrix1 = np.cov(x_data1, y_data1)
    
    # Calculate the eigenvalues and eigenvectors of the covariance matrix
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix1)
    
    # Find the index of the eigenvalue corresponding to the major axis
    major_index1 = np.argmax(eigenvalues)
    
    # Get the corresponding eigenvector
    major_axis_vector1 = eigenvectors[:, major_index1]
    
    # Calculate the angle of the major axis (in radians) relative to the horizontal axis
    angle_radians1 = np.arctan2(major_axis_vector1[1], major_axis_vector1[0])
    
    # Convert the angle to degrees
    angle_degrees1 = np.degrees(angle_radians1)
    
    # Determine if the ellipse is clockwise or counterclockwise
    if angle_degrees1 < 0:
        orientation1 = "Eastward"
    else:
        orientation1 = "Westward"
    
    #print(orientation1)   
    
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
    # ggg=np.array(df['Lat'].head(1))
    # hj=np.array(-metpy.calc.coriolis_parameter(ggg))
    # print(hj)
    bigax=axes[1]
    smallax=axes[0]
    axesratio=bigax/smallax
    intrinsic=coriollisFreq*axesratio
    energy=(((section['Ufiltered'].abs().mean())**2)+((section['Vfiltered'].abs().mean())**2))*.5#needs reorganize to get right answer
    #intrinsic=to_float(intrinsic1)
    
    results.append({
        'z1': lower,
        'z2': upper,
        'center_U': center[0],
        'center_V': center[1],
        'semi major axis length': axes[1],
        'semi minor axis length': axes[0],
        'axes ratio':axesratio,
        'angle from x axis clockwise rotation': angle,
        'direction': orientation,
        'east west reverse if downward propagation': orientation1,
        'intrinsic rads/day': intrinsic,
        'kinetic energy m^2/s^2': energy,
        'fit_accuracy': statistics.mean(bootstrap_results),
        'time begin': time_start,
        'time end': time_end
        }) 
    # Assess the quality of fit (e.g., confidence interval, etc.) using bootstrap_results
    # You can calculate confidence intervals, mean, or other statistics from the bootstrap results

df_results = pd.DataFrame(results)

print(df_results)
df_results.to_csv(results_dir + f'flight{flight_number}.csv', sep=',', index=False, encoding='utf-8')

#df_results.to_csv(results_dir + 'flight11.csv', sep=',', index=False, encoding='utf-8')