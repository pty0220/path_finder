import vtk
import numpy as np
from vtk.util import numpy_support as ns
import tkinter.filedialog as tk
import os
import helpfunction as hlp



l2n = lambda l: np.array(l)
n2l = lambda n: list(n)
ren = vtk.vtkRenderer()
def Data_arange(vtk_filename):

    #simulation_result_file_name = tk.askdirectory()

    reader = vtk.vtkRectilinearGridReader()
    reader.SetFileName(vtk_filename)
    reader.Update()
    grid = reader.GetOutput()
    bounds = grid.GetBounds()


    celldata = grid.GetCellData()
    pointnumber = grid.GetNumberOfPoints()
    Array0 = celldata.GetArray(0)
    Array1 = celldata.GetArray(1)

    Re = ns.vtk_to_numpy(Array0)
    Im = ns.vtk_to_numpy(Array1)

    pressure = np.absolute(Re+1j*Im)
    pressure[np.isnan(pressure)] = 0


    #maximum_pressure = max(pressure)
    pressure = pressure/343397.20665388 ### maximum value M1 targeting normalize
    maximum_pressure = max(pressure)

    pressure_vtk = ns.numpy_to_vtk(pressure,deep=True, array_type=vtk.VTK_FLOAT)

    grid.GetCellData().SetScalars(pressure_vtk)
    # writer = vtk.vtkRectilinearGridWriter()
    # writer.SetInputData(grid)
    # writer.SetFileName("result_rest900.vtk")
    # writer.Write()
    #

    c2p = vtk.vtkCellDataToPointData()
    c2p.SetInputData(grid)


    return grid, c2p, bounds, maximum_pressure, pointnumber



def isosurface(c2p,pointnumber,maximum_pressure,contour_percentage,opacity,color):


    #contour = vtk.vtkMarchingCubes()
    contour = vtk.vtkContourFilter()
    contour.SetInputConnection(c2p.GetOutputPort())
    contour.ComputeNormalsOn()
    contour.SetValue(1,maximum_pressure*contour_percentage/100)

    transform = vtk.vtkTransform()
    transform.Scale(1000,1000,1000)

    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputConnection(contour.GetOutputPort())
    transform_filter.SetTransform(transform)
    poly = transform_filter.GetOutput()

    STL = vtk.vtkPolyDataWriter()
    STL.SetFileName(str(contour_percentage)+'_test.stl')
    STL.SetInputData(poly)
    STL.Write()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtk.vtkLODActor()
    actor.SetNumberOfCloudPoints(pointnumber)
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetOpacity(opacity)

    return  poly,  actor

def pressure_plane_maker_rotate(output, x1, x2, y1, y2, z1, z2, opacity, ROC, width, length_transducer2target, dir_vector, Target):
    plane = vtk.vtkRectilinearGridGeometryFilter()
    plane.SetInputData(output)
    plane.SetExtent(x1, x2, y1, y2, z1, z2)

    plane, dummy = hlp.rotate(ren, [1, 0, 0], 180, plane, 1, [1, 1, 1])
    plane, dummy = hlp.translate(ren, [0, 0, 74], plane, 1, [0.5, 0.5, 0.9])

    plane, dummy, xy_angle, z_angle = \
        hlp.make_transducer(plane, ROC, width, length_transducer2target, dir_vector, Target, 1, [0.5, 0.5, 0.8])



    transform = vtk.vtkTransform()
    transform.Scale(1000, 1000, 1000)


    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(plane)
    transform_filter.SetTransform(transform)

    lut = vtk.vtkLookupTable()
    lutNum = 256
    lut.SetNumberOfTableValues(lutNum)

    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToLab()
    #ctf.SetColorSpaceToDiverging()
    ctf.AddRGBPoint(0.0 , 0.0, 0.3, 1.0)
    ctf.AddRGBPoint(0.125, 0.0, 0.5, 1.0)
    ctf.AddRGBPoint(0.25 , 0.0, 1.0, 0.0)
    ctf.AddRGBPoint(0.5, 1.0, 1.0, 0.0)
    ctf.AddRGBPoint(1.0, 1.0,0.0, 0.0)
    for ii, ss in enumerate([float(xx) / float(lutNum) for xx in range(lutNum)]):
        cc = ctf.GetColor(ss)
        lut.SetTableValue(ii, cc[0], cc[1], cc[2], 1.0)

    lut.SetTableRange(0,1)
    lut.SetNanColor(0,0,0,0)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())

    mapper.SetScalarRange((0, 1))
    mapper.SetColorMode(10)
    mapper.SetLookupTable(lut)



    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(opacity)

    return lut, mapper, actor


def pressure_plane_maker(output, p, x1, x2, y1, y2, z1, z2, opacity):
    plane = vtk.vtkRectilinearGridGeometryFilter()
    plane.SetInputData(output)
    plane.SetExtent(x1, x2, y1, y2, z1, z2)

    transform = vtk.vtkTransform()
    transform.Scale(1000, 1000, 1000)

    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputConnection(plane.GetOutputPort())
    transform_filter.SetTransform(transform)

    lut = vtk.vtkLookupTable()
    lutNum = 256
    lut.SetNumberOfTableValues(lutNum)

    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToLab()
    #ctf.SetColorSpaceToDiverging()
    ctf.AddRGBPoint(0.0 , 0.0, 0.3, 1.0)
    ctf.AddRGBPoint(0.125, 0.0, 0.5, 1.0)
    ctf.AddRGBPoint(0.25 , 0.0, 1.0, 0.0)
    ctf.AddRGBPoint(0.5, 1.0, 1.0, 0.0)
    ctf.AddRGBPoint(1.0, 1.0,0.0, 0.0)
    for ii, ss in enumerate([float(xx) / float(lutNum) for xx in range(lutNum)]):
        cc = ctf.GetColor(ss)
        lut.SetTableValue(ii, cc[0], cc[1], cc[2], 1.0)

    lut.SetTableRange(0,1)
    lut.SetNanColor(0,0,0,0)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())

    mapper.SetScalarRange((0, 1))
    mapper.SetColorMode(10)
    mapper.SetLookupTable(lut)



    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(opacity)

    return lut, mapper, actor



def isosurface_FWHM(vtk_filename,contour_percentage,opacity,color):

    reader = vtk.vtkRectilinearGridReader()
    reader.SetFileName(vtk_filename)
    reader.Update()
    grid = reader.GetOutput()
    bounds = grid.GetBounds()

    cellnumber = grid.GetNumberOfCells()
    pointnumber = grid.GetNumberOfPoints()
    celldata = grid.GetCellData()
    Array0 = celldata.GetArray(0)
    Array1 = celldata.GetArray(1)


    pressure  = np.zeros((cellnumber,1))
    pressure_vtk = vtk.vtkFloatArray()
    pressure_vtk.SetNumberOfTuples(cellnumber)

    for i in range(cellnumber):
        Re   = l2n(Array0.GetTuple(i))
        im   = l2n(Array1.GetTuple(i))
        pressure[i] = np.absolute(complex(Re,im))
        pressure_vtk.SetValue(i,pressure[i])

    pressure[np.isnan(pressure)] = 0
    grid.GetCellData().SetScalars(pressure_vtk)

    c2p = vtk.vtkCellDataToPointData()
    c2p.SetInputData(grid)




    #contour = vtk.vtkMarchingCubes()
    contour = vtk.vtkContourFilter()
    contour.SetInputConnection(c2p.GetOutputPort())
    contour.ComputeNormalsOn()
    contour.SetValue(1,max(pressure)*contour_percentage/100)

    transform = vtk.vtkTransform()
    transform.Scale(1000,1000,1000)

    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputConnection(contour.GetOutputPort())
    transform_filter.SetTransform(transform)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtk.vtkLODActor()
    actor.SetNumberOfCloudPoints(pointnumber)
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetOpacity(opacity)

    return actor







