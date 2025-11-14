import lgad_draw as lg
import pylab as plt

def draw_wafer():
    wafer = lg.DrawWafer()
    d_wafer = wafer.DrawBoundary()
    ##d_wafer << wafer.DrawReticleBoundaries()

    d_wafer << wafer.PlaceReticles()
    d_wafer << wafer.DrawNames()

    d_wafer.write_gds('wafer.gds')
    #lg.qp(d_wafer)
    #plt.show()

if __name__=="__main__":
    draw_wafer()        
