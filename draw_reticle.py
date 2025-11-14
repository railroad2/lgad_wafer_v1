import os
import sys
import json

import pylab as plt
import lgad_draw as lg

def draw_reticle(jsonname):
    with open(jsonname, "r", encoding="utf-8") as f:
        jdata = json.load(f)

    reticle_name = jdata['RETICLENAME']

    reticle = lg.DrawReticle(reticle_name)
    
    d_reticle = reticle.Draw_from_json(jsonname)

    return d_reticle


if __name__=="__main__":
    if len(sys.argv) > 1:
        jsonname = sys.argv[1]
    else:
        jsonname = './reticle_json/reticle_template.json'
        print (f'[INFO] Using json file : {jsonname}', file=sys.stderr)

    gdspath = './reticle_gds'
    gdsname = os.path.join(gdspath, os.path.splitext(os.path.split(jsonname)[-1])[0]+'.gds')

    d_reticle = draw_reticle(jsonname)
    d_reticle.write_gds(gdsname) 
    print (f'gds file is written in {gdsname}')

    #lg.qp(d_reticle)
    #plt.show()
    
