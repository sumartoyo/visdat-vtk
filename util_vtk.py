import os
import vtk
from vtk.util.colors import tomato
import numpy as np

def read():
    with open(os.path.join('data', 'Imod Jakarta', 'Boreholes_Jakarta.ipf'), 'r') as f:
        ipf = f.read()
    ipf = ipf.replace('\r', '')
    sumurs = ipf.split('\n')

    data = []
    for i in range(10, len(sumurs)):
        if sumurs[i] != '':
            x, y, filename, surface, bottom, _, _ = sumurs[i].split(',')
            _, nama = filename.split('\\')
            with open(os.path.join('data', 'Imod Jakarta', 'Boreholes', nama+'.txt'), 'r') as f:
                detail = f.read()
            detail = detail.replace('\r', '')
            lapisans = detail.split('\n')
            z_old, jenis_old = None, None
            for j in range(4, len(lapisans)):
                if lapisans[j] != '':
                    z, jenis = lapisans[j].split(',')
                    if z_old != None and jenis_old != None:
                        data.append((float(x), float(y), float(z_old), float(z), jenis_old, float(surface), float(bottom)))
                    z_old, jenis_old = z, jenis
    return data

def draw_wells(surface_scale=1.0, depth_scale=50.0):
    p = read()

    ren = vtk.vtkRenderer()
    win = vtk.vtkRenderWindow()
    win.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()

    class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
        def __init__(self):
            self.AddObserver('KeyPressEvent', self.keyPressEvent)

        def keyPressEvent(self, obj, event):
            azimuth, elevation = 0, 0

            key = iren.GetKeySym()
            if key == 'a':
                azimuth = -10
            elif key == 'd':
                azimuth = 10
            elif key == 'w':
                elevation = 10
            elif key == 's':
                elevation = -10

            ren.GetActiveCamera().Azimuth(azimuth)
            ren.GetActiveCamera().Elevation(elevation)
            win.Render()
            return

    iren.SetInteractorStyle(MyInteractorStyle())
    iren.SetRenderWindow(win)

    c = vtk.vtkCylinderSource()
    c.SetResolution(16)
    c.SetRadius(200.0)
    cm = vtk.vtkPolyDataMapper()
    cm.SetInputConnection(c.GetOutputPort())

    colormap = make_colormap()
    for n in xrange(len(p)):
        ca = vtk.vtkActor()
        ca.SetMapper(cm)
        x, y, z0, z1, t, _, _ = p[n]
        x *= surface_scale
        y *= surface_scale
        z0 *= depth_scale
        z1 *= depth_scale
        r = z0 - z1
        ca.SetPosition(x, z0-0.5*r, y)
        ca.SetScale(1.0, r, 1.0)

        ca.GetProperty().SetColor(colormap[t])
        ren.AddActor(ca)

    legend = vtk.vtkLegendBoxActor()
    legend.SetNumberOfEntries(9)
    legendBox = vtk.vtkCubeSource()
    legendBox.Update()
    for i, t in enumerate(colormap):
        legend.SetEntry(i, legendBox.GetOutput(), t, colormap[t])
    legend.GetPositionCoordinate().SetCoordinateSystemToView()
    legend.GetPositionCoordinate().SetValue(.5, -1.0)

    legend.GetPosition2Coordinate().SetCoordinateSystemToView()
    legend.GetPosition2Coordinate().SetValue(1.0, -0.5)

    legend.UseBackgroundOn()
    legend.SetBackgroundColor([1., 1., 1.])
    legend.BorderOn()

    ren.AddActor(legend)

    ren.SetBackground(1.0, 1.0, 1.0)
    win.SetSize(800, 600)

    iren.Initialize()
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.0)
    win.Render()
    iren.Start()

    """
    'gravel': [255, 255, 0],
    'sand': [255, 255, 1],
    'carbonate': [0, 0, 2],
    'clay': [0, 128, 0],
    'sandy_clay': [128, 255, 1],
    'clayey_tuff': [196, 0, 9],
    'sandy_tuff': [255, 183, 2],
    'tuff': [255, 0, 2],
    'else': [192, 192, 1],
    """

def make_colormap():
    colormap = {
        'clay': [196, 0, 0],
        'clayey_tuff': [255, 0, 2],
        'sandy_clay': [255, 183, 2],
        'carbonate': [255, 255, 1],
        'tuff': [255, 255, 0],
        'sandy_tuff': [192, 192, 1],
        'gravel': [128, 255, 1],
        'sand': [0, 128, 0],
        'else': [0, 0, 2],
    }
    for t in colormap:
        colormap[t] = (np.array(colormap[t], dtype=np.float64) / 255.).tolist()
    return colormap

if __name__ == '__main__':
    draw_wells()
