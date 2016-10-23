import os
import vtk
from vtk.util.colors import tomato
import config
import slurp
import pickle

def test():
    # config.parse()
    # p = slurp.get_bores(soilmap=config.config['soil'])
    # with open('bores.pkl', 'r') as f:
    #     p = pickle.load(f)

    data = read()

    ren = vtk.vtkRenderer()
    win = vtk.vtkRenderWindow()
    win.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(win)

    c = vtk.vtkCylinderSource()
    c.SetResolution(8)
    c.SetRadius(2.0)
    cm = vtk.vtkPolyDataMapper()
    cm.SetInputConnection(c.GetOutputPort())

    # for n in xrange(len(p)):
    #     ca = vtk.vtkActor()
    #     ca.SetMapper(cm)
    #     ca.GetProperty().SetColor(tomato)
    #     x, y, z, r = p.ix[n, :].tolist()
    #     ca.SetPosition(x, y, z)
    #     ca.SetScale(1.0, r, 1.0)
    #     ren.AddActor(ca)

    x_min, x_max = 9999999, -9999999
    y_min, y_max = 9999999, -9999999
    z_min, z_max = 9999999, -9999999
    for x, y, z1, z2, _ in data:
        if x < x_min: x_min = x
        if x > x_max: x_max = x
        if y < y_min: y_min = y
        if y > y_max: y_max = y
        if z1 < z_min: z_min = z1
        if z1 > z_max: z_max = z1
        if z2 < z_min: z_min = z2
        if z2 > z_max: z_max = z2

    def normalize(x, y, z1, z2):
        x_new = 100 * (x - x_min) / (x_max - x_min)
        y_new = 100 * (y - y_min) / (y_max - y_min)
        z1_new = 100 * (z1 - z_min) / (z_max - z_min)
        z2_new = 100 * (z2 - z_min) / (z_max - z_min)
        return x_new, y_new, z1_new, z2_new

    for i in xrange(len(data)):
        ca = vtk.vtkActor()
        ca.SetMapper(cm)
        ca.GetProperty().SetColor(tomato)
        x, y, z1, z2, jenis = data[i]
        x, y, z1, z2 = normalize(x, y, z1, z2)
        ca.SetPosition(x, y, z1)
        ca.SetScale(1.0, z2-z1, 1.0)
        ren.AddActor(ca)

    ren.SetBackground(0.1, 0.2, 0.4)
    win.SetSize(800, 600)

    iren.Initialize()
    print 'iren initialized'
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.0)
    win.Render()
    iren.Start()

def read():
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
                        data.append((float(x), float(y), float(z_old), float(z), jenis_old))
                    z_old, jenis_old = z, jenis
    return data

if __name__ == '__main__':
    test()
