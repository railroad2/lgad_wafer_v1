import pylab as plt
import lgad_draw as lg

def main_v1():
    dim_pad = lg.DimPad()
    dpad = lg.DrawPad(dim_pad)

    nx = 1
    ny = 1

    dim_per = lg.DimPeriphery(nx, ny, [dim_pad, dim_pad])
    dper = lg.DrawPeriphery(dim_per)
    
    per = dper.Draw()

    k = 0
    for i in range(ny):
        for j in range(nx):
            pad0 = dpad.Draw(center = dim_per.c_pads[k])
            per << pad0
            k += 1

    per.write_gds('example.gds') 
    per.center = (0, 0)

    lg.qp(per)

    plt.show()

def main_v2():
    nx, ny = 2,1
    tol = 0.1
    pars  = {
             'jte_width': 20, 
             'gr_gap' : 50,
             'pstop_width': 100,
             'pstop_gap' : 50,
             'gr_width' : (65, 105),
             'Nfg': 2,
             'rotation': 90,
            }
    optout = { 
              'gain' : False,
             }
    sensor = lg.DrawSensor(nx, ny,
                           **pars, **optout,
                           rounding=True, tol=tol, 
                           reticle_name="default reticle")

    sensor.write_gds('example.gds') 
    lg.qp(sensor)
    plt.show()

if __name__=="__main__":
    main_v2()

