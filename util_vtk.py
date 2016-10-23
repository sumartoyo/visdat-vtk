import vtk
from vtk.util.colors import tomato
import slurp
import config

def draw_wells(surface_scale=0.5, depth_scale=5.0):
    config.parse()
    p = slurp.get_bores(soilmap=config.config['soil'])
    # axis scaling
    #p.x *= surface_scale
    #p.y *= surface_scale
    #p.z *= depth_scale
    #p.r *= depth_scale

    ren = vtk.vtkRenderer()
    win = vtk.vtkRenderWindow()
    win.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(win)

    c = vtk.vtkCylinderSource()
    c.SetResolution(16)
    c.SetRadius(25.0)
    cm = vtk.vtkPolyDataMapper()
    cm.SetInputConnection(c.GetOutputPort())

    top = p.groupby(p.index.get_level_values(0)).first()
    btm = p.groupby(p.index.get_level_values(0)).z.last().tolist()

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

    for n in xrange(len(p)):
        ca = vtk.vtkActor()
        ca.SetMapper(cm)
        ca.GetProperty().SetColor(tomato)
        x, y, z, r = p.ix[n, :].tolist()
        ca.SetPosition(x, z, y)
        ca.SetScale(1.0, r, 1.0)
        ren.AddActor(ca)

    ren.SetBackground(1.0, 1.0, 1.0)
    win.SetSize(800, 800)

    iren.Initialize()
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(10.0)
    win.Render()
    iren.Start()

