import numpy as np
import vtk
import isosurface as iso
import helpfunction as hlp
import os

l2n = lambda l: np.array(l)
n2l = lambda n: list(n)




def pressure_plot(i,ROC, width, length_transducer2target, dir_vector, Target):


    ren = vtk.vtkRenderer()
    pressure_map_opacity =0.7

    grid, c2p, bounds, maximum_pressure, pointnumber = iso.Data_arange('SMA_pressure_inbrain' + str(i) + '.vtk')
    bounds = n2l(l2n(bounds) * 1000)
    os.chdir('C:/Users/FUS/PycharmProjects/path finder')
    # rescale m -> mm
    # lut, pressure_map_mapper, pressure_map_actor = iso.pressure_plane_maker(grid,maximum_pressure,0,137,68,68,0,191,pressure_map_opacity)
    # lut, lut_actor = hlp.translate(ren, [-65 / 2, -65 / 2, 0], lut, 1,[0.5, 0.5, 0.9])
    # lut, lut_actor = hlp.rotate(ren, [1, 0, 0], 180, lut, 1, [1, 1, 1])
    # lut, lut_actor = hlp.translate(ren, [0, 0, 74], lut, 1, [0.5, 0.5, 0.9])
    # lut, lut_actor, xy_angle, z_angle = \
    #     hlp.make_transducer(lut, ROC, width, length_transducer2target, dir_vector, Target, 1, [0,0,0])
    lut_actor = 0
    FWHM_50, FWHM_actor50 = iso.isosurface(c2p, pointnumber, maximum_pressure, 50, 0.5, [1, 0, 0])
    FWHM_50, FWHM_actor50 = hlp.translate(ren, [-65 / 2, -65 / 2, 0], FWHM_50, 1,[0.5, 0.5, 0.9])
    FWHM_50, FWHM_actor50 = hlp.rotate(ren, [1, 0, 0], 180, FWHM_50, 1, [1, 1, 1])
    FWHM_50, FWHM_actor50 = hlp.translate(ren, [0, 0, 74], FWHM_50, 1, [0.5, 0.5, 0.9])
    FWHM_50, FWHM_actor50, xy_angle, z_angle = \
        hlp.make_transducer(FWHM_50, ROC, width, length_transducer2target, dir_vector, Target, 1, [0,0,0])

    FWHM_70, FWHM_actor70 = iso.isosurface(c2p, pointnumber, maximum_pressure, 70, 0.65, [0.5, 0, 0])
    FWHM_70, FWHM_actor70 = hlp.translate(ren, [-65 / 2, -65 / 2, 0], FWHM_70, 1,[0.5, 0.5, 0.9])
    FWHM_70, FWHM_actor70 = hlp.rotate(ren, [1, 0, 0], 180, FWHM_70, 1, [1, 1, 1])
    FWHM_70, FWHM_actor70 = hlp.translate(ren, [0, 0, 74], FWHM_70, 1, [0.5, 0.5, 0.9])
    FWHM_70, FWHM_actor70, xy_angle, z_angle = \
        hlp.make_transducer(FWHM_70, ROC, width, length_transducer2target, dir_vector, Target, 1, [0,0,0])

    FWHM_90, FWHM_actor90 = iso.isosurface(c2p, pointnumber, maximum_pressure, 90, 1, [1, 0, 0])
    FWHM_90, FWHM_actor90 = hlp.translate(ren, [-65 / 2, -65 / 2, 0], FWHM_90, 1,[0.5, 0.5, 0.9])
    FWHM_90, FWHM_actor90 = hlp.rotate(ren, [1, 0, 0], 180, FWHM_90, 1, [1, 1, 1])
    FWHM_90, FWHM_actor90 = hlp.translate(ren, [0, 0, 74], FWHM_90, 1, [0.5, 0.5, 0.9])
    FWHM_90, FWHM_actor90, xy_angle, z_angle = \
        hlp.make_transducer(FWHM_90, ROC, width, length_transducer2target, dir_vector, Target, 1, [0,0,0])





    cubeAxesActor = vtk.vtkCubeAxesActor()
    cubeAxesActor.SetBounds(bounds)
    cubeAxesActor.SetCamera(ren.GetActiveCamera())
    cubeAxesActor.GetTitleTextProperty(0).SetColor(1.0, 0.0, 0.0)
    cubeAxesActor.GetLabelTextProperty(0).SetColor(1.0, 0.0, 0.0)

    cubeAxesActor.GetTitleTextProperty(1).SetColor(0.0, 1.0, 0.0)
    cubeAxesActor.GetLabelTextProperty(1).SetColor(0.0, 1.0, 0.0)

    cubeAxesActor.GetTitleTextProperty(2).SetColor(0.0, 0.0, 1.0)
    cubeAxesActor.GetLabelTextProperty(2).SetColor(0.0, 0.0, 1.0)

    cubeAxesActor.XAxisLabelVisibilityOff()
    cubeAxesActor.YAxisLabelVisibilityOff()
    cubeAxesActor.ZAxisLabelVisibilityOff()

    cubeAxesActor.DrawXGridlinesOn()
    cubeAxesActor.DrawYGridlinesOn()
    cubeAxesActor.DrawZGridlinesOn()

    #cubeAxesActor.SetGridLineLocation(vtk.VTK_GRID_LINES_FURTHEST)

    cubeAxesActor.SetGridLineLocation(cubeAxesActor.VTK_GRID_LINES_FURTHEST)
    cubeAxesActor.XAxisMinorTickVisibilityOff()
    cubeAxesActor.YAxisMinorTickVisibilityOff()
    cubeAxesActor.ZAxisMinorTickVisibilityOff()

    cubeAxesActor.GetXAxesLinesProperty().SetColor(1, 1, 1)
    cubeAxesActor.GetYAxesLinesProperty().SetColor(1, 1, 1)
    cubeAxesActor.GetZAxesLinesProperty().SetColor(1, 1, 1)

    cubeAxesActor.GetXAxesGridlinesProperty().SetColor(1, 1, 1)
    cubeAxesActor.GetYAxesGridlinesProperty().SetColor(1, 1, 1)
    cubeAxesActor.GetZAxesGridlinesProperty().SetColor(1, 1, 1)


    return lut_actor, FWHM_actor50,FWHM_actor70,FWHM_actor90