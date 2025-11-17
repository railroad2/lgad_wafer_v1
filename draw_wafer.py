import sys
import json 

import lgad_draw as lg
import pylab as plt
import phidl.utilities as pu

def draw_wafer(jsonname):
    with open(jsonname, 'r') as f:
        js = json.load(f)

    wn = js['WAFERNAME'].replace(' ', '_')

    wafer = lg.DrawWafer()
    d_wafer = wafer.DrawBoundary()
    d_wafer.name = wn

    d_wafer << wafer.PlaceReticles_from_json(jsonname)
    d_wafer << wafer.PlaceAlignkeys_from_json(jsonname)
    d_wafer << wafer.DrawLayerNames()

    ofname = f'./wafer_gds/wafer_{wn}'

    d_wafer.write_gds(f'{ofname}.gds')
    print (f'The wafer drawing is written in {ofname}.gds')
    pu.write_lyp(f'{ofname}.lyp', layerset=wafer.layerset)
    print (f'The KLayout layer info is written in {ofname}.lyp.')



if __name__=="__main__":
    jsonname = sys.argv[1] 
    draw_wafer(jsonname)        

