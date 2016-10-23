import vtk
from vtk.util.colors import tomato
import slurp
import config

def draw_cylinder():
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetResolution(1024)
    cylinder.SetRadius(2.0)

    cylinder_mapper = vtk.vtkPolyDataMapper()
    cylinder_mapper.SetInputConnection(cylinder.GetOutputPort())

    cylinder_actor = vtk.vtkActor()
    cylinder_actor.SetMapper(cylinder_mapper)
    cylinder_actor.GetProperty().SetColor(tomato)
    cylinder_actor.RotateX(30.0)
    cylinder_actor.RotateY(-45.0)
    cylinder_actor.SetPosition(1, 2, 3)

    ca = vtk.vtkActor()
    ca.SetMapper(cylinder_mapper)
    ca.GetProperty().SetColor(tomato)
    ca.RotateX(30.0)
    ca.RotateY(-45.0)
    ca.SetPosition(5, 7, -3)
    ca.SetScale(1.0, 5.0, 1.0)

    ren = vtk.vtkRenderer()
    win = vtk.vtkRenderWindow()
    win.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(win)

    ren.AddActor(cylinder_actor)
    ren.AddActor(ca)
    ren.SetBackground(0.1, 0.2, 0.4)
    win.SetSize(600, 600)

    iren.Initialize()
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.5)
    win.Render()
    iren.Start()

def read_data():
    with open(os.path.join('data', 'Imod Jakarta', 'Boreholes_Jakarta.ipf'), 'r') as f:
        ipf = f.read()
        ipf = ipf.replace('\r', '')
        sumurs = ipf.split('\n')

        data = []
        for i in range(10, len(sumurs)):
            if sumurs[i] != '':
                x, y, filename, _, _, _, _ = sumurs[i].split(',')
                with open('data\\Imod Jakarta\\'+filename+'.txt', 'r') as f:
                    detail = f.read()
                detail = detail.replace('\r', '')
                lapisans = detail.split('\n')
                z_old, jenis_old = None, None
                for j in range(4, len(lapisans)):
                    if lapisans[j] != '':
                        z, jenis = lapisans[j].split(',')
                        if z_old != None and jenis_old != None:
                            data.append((x, y, z_old, z, jenis_old))
                        z_old, jenis_old = z, jenis

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

