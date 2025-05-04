import numpy as np
import open3d as o3d
import copy
import random

def generate_random_colors(n):
    colors = []
    for _ in range(n):
        color = np.random.rand(3)
        colors.append(color)
    return colors

def main(file,colors):
    data = use_o3d(file,colors)

    cleanUp(data)

def use_o3d(file,colors):
    pcd = o3d.geometry.PointCloud()
    #pcd.points = o3d.utility.Vector3dVector(pts)

    # read ply file
    pcd = o3d.io.read_point_cloud(file)

    #Converting pcd.points to array
    pointCloudPoints = np.array(pcd.points)

    #Get rid of NaN values
    pointCloudPointMasking = np.isfinite(pointCloudPoints).all(axis=1)
    pointCloudPointFiltered = pointCloudPoints[pointCloudPointMasking]

    pointCloudPoints = o3d.geometry.PointCloud()
    pointCloudPoints.points = o3d.utility.Vector3dVector(pointCloudPointFiltered) #XYZ coordinates

    #Add the colors
    if(colors):pointCloudPointsColors= np.asarray(pcd.colors)
    if(colors):pointCloudPointsColorsFiltered = pointCloudPointsColors[pointCloudPointMasking]

    if(colors):pointCloudPoints.colors=o3d.utility.Vector3dVector(pointCloudPointsColorsFiltered) #Colors

    #Show the scan
    #o3d.visualization.draw_geometries([pointCloudPoints])

    return(pointCloudPoints)

def cleanUp(pointCloud):
    pcd = pointCloud

    number_of_planes = 10
    planes = []
    planes_withColors = []
    planes_combined = o3d.geometry.PointCloud()
    planes_combined_withColors = o3d.geometry.PointCloud()
    colors = generate_random_colors(number_of_planes)

    # Detect multiple planes
    for i in range(number_of_planes):
        plane_model, detected_plane = pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)

        if len(detected_plane) < 100:
            break

        # Extract points with original color
        plane_points = pcd.select_by_index(detected_plane, invert=False)
        planes.append(plane_points)

        # Create a new point cloud for visualization with color
        plane_visualColor = o3d.geometry.PointCloud()
        plane_visualColor.points = plane_points.points
        plane_visualColor.paint_uniform_color(colors[i % len(colors)])
        planes_withColors.append(plane_visualColor)

        # Remove detected plane from the input
        pcd = pcd.select_by_index(detected_plane, invert=True)

    # Combine all planes
    for plane in planes:
        planes_combined += plane

    for colored_plane in planes_withColors:
        planes_combined_withColors += colored_plane

    planes_combined = planes_combined.remove_duplicated_points()
    planes_combined_withColors = planes_combined_withColors.remove_duplicated_points()

    #Removing outliers
    planes_combined, _ = planes_combined.remove_radius_outlier(nb_points=16, radius=0.05)
    planes_combined_withColors, _ = planes_combined_withColors.remove_radius_outlier(nb_points=16, radius=0.05)

    #Visualization
    o3d.visualization.draw_geometries([planes_combined_withColors],"Planes selected")
    o3d.visualization.draw_geometries([planes_combined], "Filtered point cloud")  # Display planes

    return(planes_combined)

main('output.pcd',True)