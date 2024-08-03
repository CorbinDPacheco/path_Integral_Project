import dearpygui.dearpygui as dpg
import math 
from math import exp
import random as rand
import pickle
import pathBuilder

def main():

    test()

    particle = Particle(.5,[0,400])
    all_paths = []

    with open('paths.pckl', "rb") as file:
        reader = pickle.load(file)

    sumOverPaths = 0
    for path in reader:
        sumOverPaths += particle.SMatrixElement2D(path)[0]**2 + particle.SMatrixElement2D(path)[1]**2
    
    normalizationConstant = 1/sumOverPaths
    
    dpg.create_context()
    dpg.create_viewport(title='Custom Title')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    #demo.show_demo()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    while dpg.is_dearpygui_running:
        with dpg.window(label = "Path integral", on_close= onClose, width=800, height=800, pos=(200, 0)):
            draw_thickness = 3.0
            draw_size = 36
            draw_spacing = 10
            draw_rounding = draw_size/5.0
            horizontal_slices = 100
            paths_Shown = 8
            


            i = 0
            for path in reader:
                if paths_Shown < i: 
                    break
                
                probabilityDeterminant = normalizationConstant*(particle.SMatrixElement2D(path)[0]*particle.SMatrixElement2D(path)[0] + particle.SMatrixElement2D(path)[1]*particle.SMatrixElement2D(path)[1])
                if probabilityDeterminant > 0.2:
                    for point in path:
                        p1 = [int(point[0][0]),int(point[0][1])]
                        p2 = [int(point[1][0]),point[1][1]]
                        dpg.draw_line(p1,p2)
                    i += 1
                print(probabilityDeterminant)


            '''
            for path in reader:
                for point in path:
                    p1 = [int(point[0][0]),int(point[0][1])]
                    p2 = [int(point[1][0]),point[1][1]]
                    dpg.draw_line(p1,p2)
                print(particle.SMatrixElement2D(path))'''
            


            
            dpg.render_dearpygui_frame()
    dpg.destroy_context()

def test():
    particle = Particle(5,[0,400])
    lineAsFuck = [[[0,400],[800,400]]]
    print("LINE HERE")
    print(particle.Probability2D(lineAsFuck))

def freeLagrangian(mass, vel, dt = 0.1):
    return mass * (vel)^2/ dt^2

def onClose(sender,app_data,user_data):
    dpg.delete_item(sender)
    exit

def pathBuilder(particle, numOf_paths):
    out = []
    for i in range(numOf_paths):
        out.append(particle.createPath_vertical(100,200,800))
    return out

class Particle:

    def __init__(self, mass, position):
        self.mass = mass
        self.position = position

    def createPath_verticalGauss(self,horizontal_slices, horizontal_range, vertical_midpoint, sigma):
        slice_width = horizontal_range/horizontal_slices
        sigma = 50 #how far away the paths are distributed to the middle
        path_out = [[[self.position[0],self.position[1]]]]
        for i in range(horizontal_slices-1):
            path_out[i].append([self.position[0] + (i+1)*slice_width,vertical_midpoint/2 + rand.gauss(0,sigma)])
            path_out.append([path_out[i][1]])
        path_out[horizontal_slices-1].append([horizontal_range,vertical_midpoint])
        return path_out

    def createPath_vertical(self,horizontal_slices, horizontal_range, vertical_midpoint):
        slice_width = horizontal_range/horizontal_slices

        squish_factor = 1/50 #how closely the paths are distributed to the middle
        while True:
            path_out = [[[self.position[0],self.position[1]]]]
            for i in range(horizontal_slices-1):
                path_out[i].append([self.position[0] + (i+1)*slice_width,vertical_midpoint/2 + rand.randint(-math.floor(vertical_midpoint*squish_factor),math.floor(vertical_midpoint*squish_factor))])
                path_out.append([path_out[i][1]])
            path_out[horizontal_slices-1].append([horizontal_range,vertical_midpoint])

            SMat = self.SMatrixElement2D(path_out)
            if math.isnan(SMat[0]) or math.isnan(SMat[1]):
                continue
            break
        return path_out
            

    def SMatrixElement2D(self, path): # path should be a list of pairs of 2D points 
        dt = 0.1
        out = 1
        CD1 = [1,0]
        
        #theoretically - quantifies "quantumness". classical dynamics as scale_factor -> infinity
        #practically - 1/zoom. smaller values zoom closer.
        scale_factor = 0.000001


        for slice in path:
            dy = slice[1][1] - slice[0][1]
            dx = slice[1][0] - slice[0][0]
            #python complex numbers weren't working correctly so I'm employing the cayley dickenson construction here. in retrospect, the problem had nothing to do with complex numbers 
            #too lazy to change back
            CD2 = [1, scale_factor*(dx*dx + dy*dy)/(2*self.mass*dt)]
            CD1 = [CD1[0]*CD2[0] - CD1[1]*CD2[1], CD1[1]*CD2[0] + CD1[0]*CD2[1]]
        return CD1
    
    def Probability2D(self, path): # path should be a list of pairs of 2D points 
        dt = 0.1
        out = 1
        CD1 = [1,0]
        for slice in path:
            dy = slice[1][1] - slice[0][1]
            dx = slice[1][0] - slice[0][0]
            #python complex numbers weren't working correctly so I'm employing the cayley dickenson construction here. 
            CD2 = [1, (dx*dx + dy*dy)/(2*self.mass*dt)]
            CD1 = [CD1[0]*CD2[0] - CD1[1]*CD2[1], CD1[1]*CD2[0] + CD1[0]*CD2[1]]
        return CD1[0]*CD1[0] + CD1[1]*CD1[1]



 
if __name__ == "__main__":
    main()






 