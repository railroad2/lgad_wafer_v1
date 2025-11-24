import pylab as plt
import lgad_draw as lg

def main():
    nx, ny = 16, 16
    tol = 0.01
    pars  = {
             'jte_width': 10, 
             'gr_gap' : 10,
             'pstop_width': 10,
             'gr_width' : (60, 115),
             'Nfg': 0,
             'rotation': 0,
             'pad_offset':1300,
             'edge_gap' : 80,
             'pad_edge' : 1800,
            }

    optout = {}
    dim_pad = lg.DimPad()
    dim_per = lg.DimPeriphery(nx, ny, dim_pad)

    dim_pad.jte_width = 20
    dim_pad.pstop_width = 10
    dim_pad.optwin_N = 1
    dim_pad.optwin_size = [(100, 100)]
    dim_pad.optwin_pos  = [(400, 0)]
    dim_pad.ild_offset = 5

    dim_per.gr_gap = 10
    dim_per.gr_width, dim_per.gr_widthb = (60, 110)
    dim_per.pad_off_x = 1300
    dim_per.pad_off_y = 1300
    dim_per.pad_edge_x = 1900
    dim_per.pad_edge_y = 1900
    dim_per.edge_gap = 80
    dim_per.ild_offset = 5

    sensor = lg.DrawSensor(nx, ny,
                           dim_pad=dim_pad, dim_per=dim_per,
                           rounding=True, tol=tol, 
                           reticle_name="")

    sensor.write_gds('reticle_gds/KNU_lgad_v1_E.gds') 
    lg.qp(sensor)
    plt.show()

if __name__=="__main__":
    main()

