import numpy as np
import vtk
import time
import main_loop

import os
import pressure_plot as pp
import isosurface as iso


from   brain_target import *  ## developer made help function
from F_interactorstyle import FStyle


import calculator as cal    ## developer made help function
import helpfunction as pty  ## developer made help function

l2n = lambda l: np.array(l)
n2l = lambda n: list(n)


############################################################
############################################################
############################################################
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from GUI_main import Form
from GUI_main_loop import Form2


############################################################
############################################################
############################################################



startTime = time.time()

# select running version 0 is calculation 1 is plotting
running_version   = 1

Transducer_number = 0

#######################################################################################
###############################################Polting spec




skull_plot           = 'off'
skull_whole          = 'off'
skull_part           = 'off'
center_line          = 'off'
analysis_range       = 'off'
transducer_plot      = 'off'
target_plot          = 'off'
first_beamline_plot  = 'off'
second_beamline_plot = 'off'
final_beamline_plot  = 'off'

layer1_final_plot    = 'off'
##############################################################################################################################################################################
##############################################################################################################################################################################
ren     = vtk.vtkRenderer()


skull_file_name  = "skull-smooth2.stl"
phantom, phantom_actor = pty.read_skull("Calvaria_good coordinates_v2 (2).STL", 0.2,[0.8,0.8,0.8])
skull      , skull_actor      = pty.read_skull(skull_file_name, 0.6,[0.8,0.8,0.8])
brain      , brain_actor      = pty.read_skull("brain.stl", 1,[0.8,0.5,0.5])



transducer_plot, transducer_plot_actor = pty.read_skull('transducer.STL', 1,[0.5,0.5,0.9])
transducer_plot, transducer_plot_actor = pty.translate(ren, [-65 / 2, -65 / 2, 0], transducer_plot, 1,[0.5,0.5,0.9])
transducer_plot, transducer_plot_actor = pty.rotate(ren,[1,0,0],180,transducer_plot, 1,[1,1,1])
transducer_plot, transducer_plot_actor = pty.translate(ren, [0, 0, 74], transducer_plot, 1,[0.5,0.5,0.9])



#######################################################################################
########################################Target and Sonication spec
##thalamus validation spec focal length 70.92, ROC 80 width =63

Target                   = SMA
Target_name              = "SMA"
focal_length             = 55.22
ROC                      = 71
width                    = 65
length_transducer2target = 55.22

number_of_trandcuer      = 950                  ### 950 -> 3mm
range_angle              = 60  ### analysis range as angle (degree)
number_of_beamlines      = 50


#######################################################################################
########################################Properties
water_density      = 998.2
water_speed        = 1482.0

skull_density      = 1732.0
skull_speed        = 2850.0


random_density     = water_density
random_speed       = water_speed#####(transducer to skull properties )




skull_properties  = skull_density , skull_speed
water_properties  = water_density , water_speed
random_properties = random_density, random_speed



#######################################################################################
################################################calculating spec
raycasting_length = 35
centerline_length = 65





"""""
####################################################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################################################
make vtk poly data for calculation (this is not user define parameter)
####################################################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################################################
"""""


# error message turn off
errOut = vtk.vtkFileOutputWindow()
errOut.SetFileName("VTK Error Out.txt")
vtkStdErrOut = vtk.vtkOutputWindow()
vtkStdErrOut.SetInstance(errOut)

# vtk render and xyz axes
axes    = vtk.vtkAxesActor()
axes.SetTotalLength(10, 10, 10)
axes.AxisLabelsOff()

# make point at target
focus  , focus_actor   = pty.addPoint(ren, Target, [1, 0, 0], 4)
focus.Update() #### it is very important!! do not remove !!

# find center line of analysis range
centerline_target, centerline_vector, point_s, middle_target, deep_target = pty.make_centerline_target(skull, Target, centerline_length)

# closest point from skull
c_point, c_point_actor = pty.addPoint(ren, point_s)

# make center line
centerline    , centerline_actor     = pty.addLine(ren, Target, centerline_target)  # make center line target to skull

#cut skull for analysis range
frist_cutskull, first_cutskull_actor = pty.cut_skull(skull, Target, centerline_vector, opacity=0.8)

# make evenly distributed sphere_poly for transducer
spherePoly, beamline_mesh_mean, beamline_mesh_dis = pty.make_evencirle(number_of_beamlines, ROC, width, focal_length)


"""""
##########################################################################################################################################################
##########################################################################################################################################################
Running for calculation and plotting
##########################################################################################################################################################
##########################################################################################################################################################
"""""





# place holder for vtk files
transducer             = {}
transducer_actor       = {}
out_intersection_point = {}
in_intersection_point  = {}
final_beam_end         = {}
layer1_beam_end        = {}
result                 = {}
result_layer1          = {}
ARC                    = {}
ARC_layer1             = {}


if running_version == 0:

    main_loop.loop(number_of_trandcuer, length_transducer2target, range_angle, centerline_vector, Target, spherePoly, ROC, width,
         frist_cutskull
         , focus, raycasting_length, skull_properties, water_properties, random_properties, startTime, Target_name,
         number_of_beamlines, beamline_mesh_mean
         , focal_length, skull_file_name)



##############################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################
####################################Running for plotting ##################################################################################################################################################################################

else:
    # make analysis area as vtk data (computational range)
    a_range, a_range_actor, transducer_mesh_mean, transducer_mesh_dis = \
         pty.make_analysis_rage2(number_of_trandcuer, length_transducer2target, range_angle, 0.2, centerline_vector, Target)  # analysis range area

    # get number of point of transducer center (from computational range)
    number_position = a_range.GetNumberOfPoints()

    # transducer number (from computational range vertices naming)
    i = Transducer_number

    # get transducer center point from computational range
    top_point = a_range.GetPoint(i)

    # get vector between transducer and target
    vector = l2n(top_point) - l2n(Target)
    dir_vector = (vector / np.linalg.norm(vector))

    # make transducer as vtk data
    transducer, transducer_actor, xy_angle, z_angle = \
        pty.make_transducer(spherePoly, ROC, width, length_transducer2target, dir_vector, Target, 0.7, [1, 0, 0])


    # stl file for just plot
    transducer_plot, transducer_plot_actor, xy_angle, z_angle = \
        pty.make_transducer(transducer_plot, ROC, width, length_transducer2target, dir_vector, Target, 1, [0.5, 0.5, 0.8])


    intersectionPolyFilter = vtk.vtkIntersectionPolyDataFilter()
    intersectionPolyFilter.SetInputData(0, frist_cutskull)
    intersectionPolyFilter.SetInputData(1, transducer)
    intersectionPolyFilter.Update()
    test_intersection = intersectionPolyFilter.GetOutput()


    # cut skull for speed
    skull_cut, skull_cut_actor = pty.cut_skull_loop(frist_cutskull, Target, dir_vector)

    # find intersection point at each beam lines with skull
    out_intersection_point, in_intersection_point, final_beam_end, layer1_beam_end, result,result_layer1, ARC, ARC_out,out_vector_actor, in_vector_actor =\
        cal.calculator(skull_cut, focus, transducer, Target, raycasting_length, skull_properties, water_properties, random_properties)

    # percentage
    percentage = (np.sum(result) / transducer.GetNumberOfPoints()) * 100
    percentage_layer1 = (np.sum(result_layer1) / transducer.GetNumberOfPoints()) * 100
    # for print result
    textActor = vtk.vtkTextActor()
    textActor2 = vtk.vtkTextActor()
    print("###########################################################################")
    print("This is plotting version ##################################################")
    print("###########################################################################")
    print("")
    print("")
    if test_intersection.GetNumberOfPoints() > 0  :
        print ("This transducer location is invalid")
        textActor2.SetInput("Warning: This transducer location is invalid")
    a = test_intersection.GetNumberOfPoints()
    print("Number of beam lines is " + str(number_of_beamlines))
    print("Distance between beam lines: " + str(beamline_mesh_mean))
    print("Distance between transducer: " + str(transducer_mesh_mean))
    print("Both layer result percentage (ray tracking result) " + str(percentage) + "%")
    print("one layer result percentage (ray tracking result) " + str(percentage_layer1) + "%")
    print("Average reflection coefficient is " + str(ARC))
    print("One layer Average reflection coefficient is " + str(ARC_out))
    print("xy plane angle is " + str(xy_angle))
    print("z plane angle is " + str(z_angle))

    header = '{0:^5s}\n{1:^5s} \n{2:^5s} \n{3:^5s}\n{4:^5s}' \
        .format('Target: ' + str(Target_name) + ',  coordinate: ' + str(Target),
                'Number of beam lines ' + str(number_of_beamlines),
                'Distance between beam lines: ' + str(beamline_mesh_mean) + ' mm',
                'ROC: ' + str(ROC) + ',  width: ' + str(width) + ',  focal length: ' + str(focal_length),
                '')

    textActor.SetInput(header)
    textActor.GetTextProperty().SetFontSize(18)
    textActor2.GetTextProperty().SetFontSize(24)
    textActor2.GetTextProperty().SetColor(1,0,0)

    firstline_actor = {}
    secondline_actor = {}
    finalline_actor = {}


    # for plotting beam lines (first, second and final)
    # iterate as number of beam lines
    for idx in range(number_of_beamlines):

        # draw line transducer to out skull surface
        if np.any(out_intersection_point[idx][:] != 0):

            firstline, firstline_actor[str(idx)] = \
                pty.addLine(ren, transducer.GetPoint(idx), n2l(out_intersection_point[idx][:]), [1, 1, 0])

            # if you want to draw first beam, draw (add vtk render)
            if first_beamline_plot == 'on':
                ren.AddActor(firstline_actor[str(idx)])

            # draw line out skull surface to in skull surface
            if np.any(in_intersection_point[idx][:] != 0):
                secondline, secondline_actor[str(idx)] = \
                    pty.addLine(ren, n2l(out_intersection_point[idx][:]), n2l(in_intersection_point[idx][:]), [0, 0, 1])

                layer1_finish, layer1_finish_actor = \
                    pty.addLine(ren, n2l(out_intersection_point[idx][:]), n2l(layer1_beam_end[idx][:]),[0,0.5,1])


                # if you want to draw second beam, draw (add vtk render)
                if second_beamline_plot == 'on':
                    ren.AddActor(secondline_actor[str(idx)])

                if layer1_final_plot == 'on':
                    ren.AddActor(layer1_finish_actor)

                if np.any(final_beam_end[idx][:] != 0):
                    finalline, finalline_actor[str(idx)]  = pty.addLine(ren, n2l(in_intersection_point[idx][:]),
                                                             n2l(final_beam_end[idx][:]), [1, 0.5, 0])
                    if final_beamline_plot == 'on':
                        ren.AddActor(finalline_actor[str(idx)])








    # add render if you want draw something
    if skull_plot == 'on':
        ren.AddActor(phantom_actor)
    if skull_whole == 'on':
        ren.AddActor(skull_actor)
    if target_plot == 'on':
        ren.AddActor(focus_actor)
    if analysis_range == 'on':
        ren.AddActor(a_range_actor)
    if center_line == 'on':
        ren.AddActor(centerline_actor)
    if skull_part == 'on':
        ren.AddActor(skull_cut_actor)
    if transducer_plot == 'on':
        ren.AddActor(transducer_actor)
    ren.AddActor2D(textActor)
    ren.AddActor2D(textActor2)
    textActor2.SetPosition2(10, 40)
    ren.AddActor(axes)


    #grid, c2p, bounds, maximum_pressure, pointnumber = iso.Data_arange('S1_result_full_vtk0.vtk')
    #lut, pressure_map_mapper, pressure_map_actor =  iso.pressure_plane_maker_rotate(grid,0,137,68,68,0,191,0.7,ROC, width, length_transducer2target, dir_vector, Target)
    #ren.AddActor(pressure_map_actor)

    camera = vtk.vtkCamera()
    camera.SetPosition(356.5634441980953, 525.6970828918022, 155.1067789534897)
    camera.SetFocalPoint(-1.4043141566961168, 9.01218191499613, -34.575235404784806)
    camera.SetViewUp(-0.10006989292731805, -0.27222123756029304, 0.9570170397389264)

    ren.SetBackground(0.2, 0.2, 0.2)
    ren.SetActiveCamera(camera)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(1000,800)

    iren = vtk.vtkRenderWindowInteractor()

    #open GUI switch
    #app = QtWidgets.QApplication(sys.argv)
    app = QtWidgets.QApplication(sys.argv)

    w = Form2(number_of_trandcuer, length_transducer2target, range_angle, centerline_vector, Target, spherePoly, ROC, width,
         frist_cutskull
         , focus, raycasting_length, skull_properties, water_properties, random_properties, startTime, Target_name,
         number_of_beamlines, beamline_mesh_mean
         , focal_length, skull_file_name,iren)


    a = Form(skull_actor,first_cutskull_actor,brain_actor,focus_actor,transducer_plot_actor,a_range_actor,centerline_actor,firstline_actor,secondline_actor,finalline_actor,
             out_vector_actor,in_vector_actor,iren)



    iren.SetInteractorStyle(FStyle(focus_actor,transducer_plot_actor,iren))
    iren.SetRenderWindow(renWin)

    iren.Initialize()
    renWin.Render()

    iren.Start()





