import sys
import json 

import lgad_draw as lg
import pylab as plt

def draw_wafer(jsonname):
    with open(jsonname, 'r') as f:
        js = json.load(f)

    wn = js['WAFERNAME'].replace(' ', '_')

    wafer = lg.DrawWafer()
    d_wafer = wafer.DrawBoundary()
    d_wafer.name = wn

    d_wafer << wafer.PlaceReticles_from_json(jsonname)
    d_wafer << wafer.DrawLayerNames()

    ofname = f'./wafer_gds/wafer_{wn}.gds'
    d_wafer.write_gds(ofname)
    print (f'The wafer drawing is written in {ofname}.')

if __name__=="__main__":
    jsonname = sys.argv[1] 
    draw_wafer(jsonname)        

