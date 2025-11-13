import sys

import pylab as plt
import lgad_draw as lg

def draw_reticle():

    reticle = lg.DrawReticle('test')
    
    if len(sys.argv) > 1:
        jsonname = sys.argv[1]
    else:
        jsonname = './reticle_template.json'

    d_reticle = reticle.Draw_from_json(jsonname)

    d_reticle.write_gds('example.gds') 
    lg.qp(d_reticle)
    plt.show()


if __name__=="__main__":
    draw_reticle()
