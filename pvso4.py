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
    planes =[]
    colors = generate_random_colors(number_of_planes)
    planeMemory = o3d.geometry.PointCloud()
    planes_combined = o3d.geometry.PointCloud()

    #Detect multiply planes
    for i in range(number_of_planes):
        plane_model, plane = pcd.segment_plane(0.01, 3, 1000)

        plane_points = pcd.select_by_index(plane, invert=False)

        planeMemory.points = plane_points.points
        planeMemory.colors = plane_points.colors
        #Color unifi
        #plane_points.paint_uniform_color(colors[i % len(colors)])

        planes.append(plane_points)

        # Remove inliers for next iteration
        pcd = pcd.select_by_index(plane, invert=True)

        planes_combined += planeMemory


    #pcd.paint_uniform_color([0.5, 0.5, 0.5])  # Gray for remaining points

    o3d.visualization.draw_geometries([planeMemory]) #Display planes

    #o3d.visualization.draw_geometries([pcd])



main('output_big.pcd',False)