import pylab as plt
import lgad_draw as lg

def main():
    nx, ny = 1,1
    tol = 0.01
    pars  = {
             'jte_width': 20, 
             'gr_gap' : 30,
             'pstop_width': 10,
             'pstop_gap' : 10,
             'gr_width' : (65, 105),
             'Nfg': 2,
             'rotation': 90,
            }
    optout = { 
              #'gain' : False,
             }
    sensor = lg.DrawSensor(nx, ny,
                           **pars, **optout,
                           rounding=True, tol=tol, 
                           reticle_name="")

    sensor.write_gds('example.gds') 
    lg.qp(sensor)
    #plt.show()

if __name__=="__main__":
    main()

