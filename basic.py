import sys
import vtk
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot




class Form(QtWidgets.QDialog):
    def __init__(self,skull_actor,skull_cut_actor,brain_actor,focus_actor,transducer_actor,a_range_actor,centerline_actor, interactor, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("switch.ui", self)
        self.ui.show()
        self.iren = interactor
        self.skull_actor = skull_actor
        self.skull_cut_actor = skull_cut_actor
        self.brain_actor= brain_actor
        self.focus_actor = focus_actor
        self.transducer_actor =transducer_actor
        self.a_range_actor = a_range_actor
        self.centerline_actor = centerline_actor


        self.skull = True
        self.skull_cut = True
        self.brain = True
        self.target = True
        self.transducer = True
        self.a_range = True
        self.centerline = True
        self.all =True

    @pyqtSlot()
    def All(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.all:
            renderer.AddActor(self.skull_actor)
            renderer.AddActor(self.skull_cut_actor)
            renderer.AddActor(self.brain_actor)
            renderer.AddActor(self.focus_actor)
            renderer.AddActor(self.transducer_actor)
            renderer.AddActor(self.a_range_actor)
            renderer.AddActor(self.centerline_actor)

            print("All on")
            self.all = False
            self.skull = False
            self.skull_cut = False
            self.brain = False
            self.target = False
            self.transducer = False
            self.a_range = False
            self.centerline = False
            self.all = False

        else:
            renderer.RemoveActor(self.skull_actor)
            renderer.RemoveActor(self.skull_cut_actor)
            renderer.RemoveActor(self.brain_actor)
            renderer.RemoveActor(self.focus_actor)
            renderer.AddActor(self.transducer_actor)
            renderer.RemoveActor(self.a_range_actor)
            renderer.RemoveActor(self.centerline_actor)

            print("All off")
            self.skull = True
            self.skull_cut = True
            self.brain = True
            self.target = True
            self.transducer = True
            self.a_range = True
            self.centerline = True
            self.all = True

    @pyqtSlot()
    def Skull(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.skull:
            renderer.AddActor(self.skull_actor)
            print("Skull on")
            self.skull = False
        else:
            renderer.RemoveActor(self.skull_actor)
            print("Skull off")
            self.skull = True



    @pyqtSlot()
    def Skull_Part(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.skull_cut:

            renderer.AddActor(self.skull_cut_actor)
            print("Skull_Part on")
            self.skull_cut = False
        else:
            renderer.RemoveActor(self.skull_cut_actor)

            print("Skull_Part off")
            self.skull_cut = True



    @pyqtSlot()
    def Brain(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.brain:
            renderer.AddActor(self.brain_actor)
            print("Brain on")
            self.brain = False
        else:
            renderer.RemoveActor(self.brain_actor)


            print("Brain off")
            self.brain = True




    @pyqtSlot()
    def Target(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.target:
            renderer.AddActor(self.focus_actor)
            print("Target on")
            self.target = False
        else:
            renderer.RemoveActor(self.focus_actor)
            print("Target off")
            self.target = True




    @pyqtSlot()
    def Transducer(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.transducer:
            renderer.AddActor(self.transducer_actor)
            print("Transducer on")
            self.transducer = False
        else:
            renderer.RemoveActor(self.transducer_actor)
            print("Transducer off")
            self.transducer = True




    @pyqtSlot()
    def Analysis_range(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.a_range:
            renderer.AddActor(self.a_range_actor)

            print("a_range on ")
            self.a_range = False
        else:
            renderer.RemoveActor(self.a_range_actor)
            print("a_range off")
            self.a_range = True




    @pyqtSlot()
    def Center_line(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.centerline:
            renderer.AddActor(self.centerline_actor)
            print("centerline on")
            self.centerline = False
        else:
            renderer.RemoveActor(self.centerline_actor)
            print("centerline off")
            self.centerline = True


    #
    # @pyqtSlot()
    # def All(self):
    #     renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()
    #
    #     if self.push:
    #         renderer.AddActor(self.skull_actor)
    #         renderer.AddActor(self.skull_cut_actor)
    #         renderer.AddActor(self.brain_actor)
    #         renderer.AddActor(self.focus_actor)
    #         renderer.AddActor(self.transducer_actor)
    #         renderer.AddActor(self.a_range_actor)
    #         renderer.AddActor(self.a_range_actor)
    #         renderer.AddActor(self.centerline_actor)
    #
    #         print("All on")
    #         self.push = False
    #     else:
    #         renderer.RemoveActor(self.skull_actor)
    #         renderer.RemoveActor(self.skull_cut_actor)
    #         renderer.RemoveActor(self.brain_actor)
    #         renderer.RemoveActor(self.focus_actor)
    #         renderer.AddActor(self.transducer_actor)
    #         renderer.RemoveActor(self.a_range_actor)
    #         renderer.RemoveActor(self.centerline_actor)
    #
    #         print("All off")
    #         self.push = True
    #
    #
    #
    # @pyqtSlot()
    # def All(self):
    #     renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()
    #
    #     if self.push:
    #         renderer.AddActor(self.skull_actor)
    #         renderer.AddActor(self.skull_cut_actor)
    #         renderer.AddActor(self.brain_actor)
    #         renderer.AddActor(self.focus_actor)
    #         renderer.AddActor(self.transducer_actor)
    #         renderer.AddActor(self.a_range_actor)
    #         renderer.AddActor(self.a_range_actor)
    #         renderer.AddActor(self.centerline_actor)
    #
    #         print("All on")
    #         self.push = False
    #     else:
    #         renderer.RemoveActor(self.skull_actor)
    #         renderer.RemoveActor(self.skull_cut_actor)
    #         renderer.RemoveActor(self.brain_actor)
    #         renderer.RemoveActor(self.focus_actor)
    #         renderer.AddActor(self.transducer_actor)
    #         renderer.RemoveActor(self.a_range_actor)
    #         renderer.RemoveActor(self.centerline_actor)
    #
    #         print("All off")
    #         self.push = True
