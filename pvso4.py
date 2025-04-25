import numpy as np
import open3d as o3d

def main(file):
    # use open3d
    use_o3d(file)


def use_o3d(file):
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
    pointCloudPointsColors= np.asarray(pcd.colors)
    pointCloudPointsColorsFiltered = pointCloudPointsColors[pointCloudPointMasking]

    #Here are the colors added to the whole
    pointCloudPoints.colors=o3d.utility.Vector3dVector(pointCloudPointsColorsFiltered) #Colors

    #Show the scan
    o3d.visualization.draw_geometries([pointCloudPoints])


main('output.pcd')