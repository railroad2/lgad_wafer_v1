import sys
import json
import re

import numpy as np

centers = [
  [ [-58920,  58920 ],
    [-39280,  58920 ],
    [-19640,  58920 ],
    [     0,  58920 ],
    [ 19640,  58920 ],
    [ 39280,  58920 ],
    [ 58920,  58920 ], ], 
  [ [-58920,  39280 ],
    [-39280,  39280 ],
    [-19640,  39280 ],
    [     0,  39280 ],
    [ 19640,  39280 ],
    [ 39280,  39280 ],
    [ 58920,  39280 ], ],
  [ [-58920,  19640 ],
    [-39280,  19640 ],
    [-19640,  19640 ],
    [     0,  19640 ],
    [ 19640,  19640 ],
    [ 39280,  19640 ],
    [ 58920,  19640 ], ],
  [ [-58920,      0 ],
    [-39280,      0 ],
    [-19640,      0 ],
    [     0,      0 ],
    [ 19640,      0 ],
    [ 39280,      0 ],
    [ 58920,      0 ], ],
  [ [-58920, -19640 ],
    [-39280, -19640 ],
    [-19640, -19640 ],
    [     0, -19640 ],
    [ 19640, -19640 ],
    [ 39280, -19640 ],
    [ 58920, -19640 ], ],
  [ [-58920, -39280 ], 
    [-39280, -39280 ],
    [-19640, -39280 ],
    [     0, -39280 ],
    [ 19640, -39280 ],
    [ 39280, -39280 ],
    [ 58920, -39280 ], ],
  [ [ 58920, -58920 ],
    [-39280, -58920 ],
    [-19640, -58920 ],
    [     0, -58920 ],
    [ 19640, -58920 ],
    [ 39280, -58920 ],
    [ 58920, -58920 ], ],
]


def make():
    dic = {}
    dic["WAFERNAME"]   = "KNU LGAD v1"
    dic["DESCRIPTION"] = "Template"
    dic["WAFERSIZE"]   = 150*1000    # mm -> um
    dic["EBRWIDTH"]    = 5000
    dic["JSONPATH"]    = "./reticle_json"
    dic["GDSPATH"]     = "./reticle_gds"
    dic["BLANKSIZE"]   = [1500, 150]
    dic["ALIGNKEYS"]   = [
        {
            "NUM": 1,
            "SRCFILE": "align_keys/akey1.gds",
            "CENTER" : [-39280, 0]
        },
        {
            "NUM": 2,
            "SRCFILE": "align_keys/akey1.gds",
            "CENTER" : [39280, 0] 
        }
    ]
    dic["NRETICLES"]   = 45
    dic["RETICLES"]    = []

    i_blank  = [(0, 0), (0, 6), (6, 0), (6, 6)]
    i_RI = [tuple(s) for s in np.concatenate(np.array(np.meshgrid(np.arange(1,6), np.arange(1,6))).T)]
    i_RE = []

    # default
    i_typeA = [tuple(s) for s in np.concatenate(np.array(np.meshgrid(np.arange(0,5), np.arange(2,5))).T)] 
    # opt-in test
    i_typeB = [] 
    # partial dicing
    i_typeC = [tuple(s) for s in np.concatenate(np.array(np.meshgrid([5], np.arange(0,7))).T)] \
              +[tuple(s) for s in np.concatenate(np.array(np.meshgrid(np.arange(0,7), [5])).T)] 
    # AKEY
    i_typeD = [(3, 1), (3, 5)] 
    # 16x16
    i_typeE = [(5, 5)] 

    dic_reticle = {
            "NUM"        : 1,
            "NAME"       : "RI-01",
            "TYPE"       : "Reticle_B",
            "INDEX"      : [1, 1],
            "SIZE"       : [0, 0],
            "CENTER"     : [0, 0],
            "NFG"        : 0,
            "SRCFILE"    : ""
        }

    # inner reticles
    num = 0
    NRI = 0
    NRE = 0

    for i in range(7):
        for j in range(7):
            if (i, j) in i_blank: 
                continue
            elif (i, j) in i_RI:
                NRI += 1
                rname = f"RI-{NRI}"
            else:
                NRE += 1
                rname = f"RE-{NRE}"

            nfg = 0
            if (i, j) in i_typeE:
                rtype = "E"
            elif (i, j) in i_typeD:
                rtype = "D"
            elif (i, j) in i_typeC:
                rtype = "C"
            elif (i, j) in i_typeA:
                rtype = "A"
                if j == 2:
                    nfg = 1
                    rtype += "-FG1"
                elif j == 4:
                    nfg = 2
                    rtype += "-FG2"
                else:
                    nfg = 0
                    rtype += "-FG0"
            else:
                rtype = "B"


            num += 1 
            sizex = sizey = 19140

            dic_reticle["NUM"]     = int(num)
            dic_reticle["NAME"]    = rname
            dic_reticle["TYPE"]    = rtype
            dic_reticle["INDEX"]   = f"({i+1}, {j+1})"
            dic_reticle["SIZE"]    = [sizex, sizey]
            dic_reticle["CENTER"]  = centers[i][j]
            dic_reticle["NFG"]     = nfg
            dic_reticle["SRCFILE"] = (dic["WAFERNAME"]).replace(' ', '_') + "_" + dic_reticle["TYPE"] 

            dic["RETICLES"].append(dic_reticle.copy()) 

        # end of for j
    # end of for i

    js = json.dumps(dic, indent=4) 

    pattern = r'\[\s*(-?\d+)\s*,\s*(-?\d+)\s*\]'
    replacement = r'[\1, \2]'

    js1 = re.sub(pattern, replacement, js)
    print (js1)

    with open("wafer_template.json", "w", encoding="utf-8") as f:
        f.write(js1) 


if __name__=="__main__":
    make()

