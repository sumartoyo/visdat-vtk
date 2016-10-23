import vtk
from vtk.util.colors import tomato
import visdat
import numpy as np

def draw_wells(surface_scale=0.5, depth_scale=50.0):
    #config.parse()
    #p = slurp.get_bores(soilmap=config.config['soil'])
    # axis scaling
    #p.x *= surface_scale
    #p.y *= surface_scale
    #p.z *= depth_scale
    #p.r *= depth_scale

    p = visdat.read()

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

    #top = p.groupby(p.index.get_level_values(0)).first()
    #btm = p.groupby(p.index.get_level_values(0)).z.last().tolist()

    """
    for n in xrange(len(top)):
        ca = vtk.vtkActor()
        ca.SetMapper(cm)
        ca.GetProperty().SetColor(0.1, 0.8, 0.2)
        x, y, z0 = top.ix[n, :3].tolist()
        z1 = btm[n]
        h = z0-z1
        ca.SetPosition(x, z0-h, y)
        ca.SetScale(1.0, 2.0*h, 1.0)
        ren.AddActor(ca)
    """

    colormap = make_colormap()
    for n in xrange(len(p)):
        ca = vtk.vtkActor()
        ca.SetMapper(cm)
        x, y, z0, z1, t, _, _ = p[n]
        z0 *= depth_scale
        z1 *= depth_scale

        ca.GetProperty().SetColor(colormap[t])
        r = z0 - z1
        ca.SetPosition(x, z0-0.5*r, y)
        ca.SetScale(1.0, r, 1.0)
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

    ren.AddActor(legend)

    ren.SetBackground(1.0, 1.0, 1.0)
    win.SetSize(800, 600)

    iren.Initialize()
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.0)
    win.Render()
    iren.Start()

def make_colormap():
    colormap = {
        'gravel': [255, 255, 0],
        'sand': [255, 255, 1],
        'carbonate': [0, 0, 2],
        'clay': [0, 128, 0],
        'sandy_clay': [128, 255, 1],
        'clayey_tuff': [196, 0, 9],
        'sandy_tuff': [255, 183, 2],
        'tuff': [255, 0, 2],
        'else': [192, 192, 1],
    }
    for t in colormap:
        colormap[t] = (np.array(colormap[t], dtype=np.float64) / 255.).tolist()
    return colormap
