from phidl import Device
import phidl.geometry as pg
import sys

def invert_wafer(fname):
    d_wafer = pg.import_gds(fname) 
    d_wafer_inverted = Device('wafer1')

    for i in [1, 2, 3, 4, 5, 6, 8]:
        d_wafer_inverted.add_ref(pg.invert(pg.extract(d_wafer, [i]), border=1000, layer=i))
    
    d_wafer_inverted.add_ref(pg.extract(d_wafer, [7]))

    d_wafer_inverted.write_gds('wafer_inverted.gds')


if __name__=="__main__":
    invert_wafer(sys.argv[1])
    
    

