import numpy as np
import open3d as o3d
import copy
import random
from sklearn.cluster import Birch
from sklearn.cluster import DBSCAN

def generate_random_colors(n):
    colors = []
    for _ in range(n):
        color = np.random.rand(3)
        colors.append(color)
    return colors
  
  
############################################################################################################################################################

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

def k_means(X, k, max_iters=100):
    n_samples, n_features = X.shape
    np.random.seed(42)
    initial_indices = np.random.choice(n_samples, k, replace=False)
    centers = X[initial_indices]

    for _ in range(max_iters):
        clusters = [[] for _ in range(k)]
        for point in X:
            distances = [euclidean_distance(point, center) for center in centers]
            cluster_idx = np.argmin(distances)
            clusters[cluster_idx].append(point)

        new_centers = np.zeros((k, n_features))
        for idx, cluster in enumerate(clusters):
            if cluster:
                new_centers[idx] = np.mean(cluster, axis=0)
            else:
                new_centers[idx] = X[np.random.randint(n_samples)]

        if np.allclose(centers, new_centers):
            break
        centers = new_centers

    labels = np.zeros(n_samples, dtype=int)
    for idx, point in enumerate(X):
        distances = [euclidean_distance(point, center) for center in centers]
        labels[idx] = np.argmin(distances)

    return centers, labels

def apply_k_means_to_pcd(pcd, k):
    points = np.asarray(pcd.points)
    centers, labels = k_means(points, k)
    colors = generate_random_colors(k)

    # Pridanie farieb podla klastrov
    cluster_colors = np.array([colors[label] for label in labels])
    pcd.colors = o3d.utility.Vector3dVector(cluster_colors)

    # Vizualizacia
    o3d.visualization.draw_geometries([pcd], window_name="K-means clustering")
    
############################################################################################################################################################
    
def main(file,colors):
    data = use_o3d(file,colors)
    #o3d.visualization.draw_geometries([data], "Loaded Point Cloud")

    dataClean = cleanUp(data,True,True)

    dbscanAlgorithm(dataClean)
    #birchAlgorithm(dataClean)

    #apply_k_means_to_pcd(data, 4) ???????????????

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

def dbscanAlgorithm(pointCloud):
    pcd = pointCloud
    #o3d.visualization.draw_geometries([pcd], "Test view")

    #clusters = np.asarray(pcd.cluster_dbscan(eps=0.08, min_points=20, print_progress=True))

    PcdXYZandRGB = np.hstack((np.asarray(pcd.points), np.asarray(pcd.colors)))

    clusters = DBSCAN(eps=0.075, min_samples=20).fit_predict(PcdXYZandRGB)

    numberOfclusters = len(set(clusters)) - (1 if -1 in clusters else 0)
    print(numberOfclusters)

    colorsForClusters = generate_random_colors(numberOfclusters)

    pcdClusters = [o3d.geometry.PointCloud() for _ in range(numberOfclusters)]

    pcdNpPoints = np.asarray(pcd.points)

    for i in range(numberOfclusters):
        pcdClusters[i].points = o3d.utility.Vector3dVector(pcdNpPoints[clusters == i])
        pcdClusters[i].paint_uniform_color(colorsForClusters[i])

    #Combine the cluster to one point cloud
    pcdClustersCombined = o3d.geometry.PointCloud()
    for i in range(numberOfclusters):
        pcdClustersCombined += pcdClusters[i]

    #Visualization
    o3d.visualization.draw_geometries([pcdClustersCombined], "Segmented space")

def birchAlgorithm(pointCloud):
    # Convert point cloud to NumPy
    points = np.asarray(pointCloud.points)

    threshold=1.2
    n_clusters=20


    #The Birch algo
    birch = Birch(threshold=threshold, n_clusters=n_clusters)
    labels = birch.fit_predict(points)

    #Colors yessss
    unique_labels = np.unique(labels)
    num_clusters = len(unique_labels)
    print(f"Clusters found: {num_clusters}")

    #Create the colors yessss
    color_map = generate_random_colors(num_clusters)
    color_array = np.array([color_map[label] for label in labels])


    colored_pcd = o3d.geometry.PointCloud()
    colored_pcd.points = o3d.utility.Vector3dVector(points)
    colored_pcd.colors = o3d.utility.Vector3dVector(color_array)

    # Visualize result
    o3d.visualization.draw_geometries([colored_pcd], window_name="BIRCH Clustering")

def cleanUp(pointCloud,duplicatesRemove,outlierRemove):
    pcd = pointCloud

    number_of_bigPlanes = 10
    number_of_smallPlanes = 20
    planes = []
    planes_withColors = []
    planes_combined = o3d.geometry.PointCloud()
    planes_combined_withColors = o3d.geometry.PointCloud()
    colors = generate_random_colors(number_of_bigPlanes+number_of_smallPlanes)

    # Detect multiple planes
    print("Detecting Big planes...")
    for i in range(number_of_bigPlanes):
        print(f"Big Plane {i+1}...")
        plane_model, detected_plane = pcd.segment_plane(distance_threshold=0.075, ransac_n=3, num_iterations=1000)

        if len(detected_plane) < 100:
            break

        # Extract points with original color
        plane_points = pcd.select_by_index(detected_plane, invert=False)
        if(outlierRemove):
            plane_points, _ = plane_points.remove_radius_outlier(nb_points=16, radius=0.05)
        planes.append(plane_points)

        # Create a new point cloud for visualization with color
        plane_visualColor = o3d.geometry.PointCloud()
        plane_visualColor.points = plane_points.points
        plane_visualColor.paint_uniform_color(colors[i % len(colors)])
        planes_withColors.append(plane_visualColor)

        # Remove detected plane from the input
        pcd = pcd.select_by_index(detected_plane, invert=True)

    print("Big planes Done!")

    print("Detecting Small planes...")
    for i in range(number_of_smallPlanes):
        print(f"Small Plane {i + 1}...")
        plane_model, detected_plane = pcd.segment_plane(distance_threshold=0.001, ransac_n=3, num_iterations=1000)

        if len(detected_plane) < 100:
            break

        # Extract points with original color
        plane_points = pcd.select_by_index(detected_plane, invert=False)
        if(outlierRemove):
            plane_points, _ = plane_points.remove_radius_outlier(nb_points=16, radius=0.05)
        planes.append(plane_points)

        # Create a new point cloud for visualization with color
        plane_visualColor = o3d.geometry.PointCloud()
        plane_visualColor.points = plane_points.points
        plane_visualColor.paint_uniform_color(colors[i % len(colors)])
        planes_withColors.append(plane_visualColor)

        # Remove detected plane from the input
        pcd = pcd.select_by_index(detected_plane, invert=True)

    print("Small planes Done!")

    # Combine all planes
    for plane in planes:
        planes_combined += plane

    for colored_plane in planes_withColors:
        planes_combined_withColors += colored_plane
    print("Combining planes...Done")

    if(duplicatesRemove):
        planes_combined = planes_combined.remove_duplicated_points()
        planes_combined_withColors = planes_combined_withColors.remove_duplicated_points()
        print("Removing duplicated points...Done")

    #Removing outliers
    #if(outlierRemove):
    #    planes_combined, _ = planes_combined.remove_radius_outlier(nb_points=16, radius=0.05)
    #    planes_combined_withColors, _ = planes_combined_withColors.remove_radius_outlier(nb_points=16, radius=0.05)
    #    print("Removing outliers...Done")

    #Visualization
    o3d.visualization.draw_geometries([planes_combined_withColors],"Planes selected")
    o3d.visualization.draw_geometries([planes_combined], "Filtered point cloud")  # Display planes

    #TODO Add saving the result
    return(planes_combined)



main('example4.ply', True)