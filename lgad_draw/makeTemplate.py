import json
import re

centers = [
    [	-8520	,	8520	],
    [	-6320	,	8520	],
    [	-4120	,	8520	],
    [	-1920	,	8520	],
    [	 920	,	8520	],
    [	4400	,	8520	],
    [	7880	,	8520	],
    [	-8520	,	6320	],
    [	-6320	,	6320	],
    [	-4120	,	6320	],
    [	-1920	,	6320	],
    [	 920	,	6320	],
    [	4400	,	6320	],
    [	7880	,	6320	],
    [	-8520	,	4120	],
    [	-6320	,	4120	],
    [	-4120	,	4120	],
    [	-1920	,	4120	],
    [	 920	,	4120	],
    [	4400	,	4120	],
    [	7880	,	4120	],
    [	-8520	,	1920	],
    [	-6320	,	1920	],
    [	-4120	,	1920	],
    [	-1920	,	1920	],
    [	 920	,	1920	],
    [	4400	,	1920	],
    [	7880	,	1920	],
    [	-8520	,	-920	],
    [	-6320	,	-920	],
    [	-4120	,	-920	],
    [	-1920	,	-920	],
    [	 920	,	-920	],
    [	4400	,	-920	],
    [	7880	,	-920	],
    [	-8520	,	-4400	],
    [	-6320	,	-4400	],
    [	-4120	,	-4400	],
    [	-1920	,	-4400	],
    [	 920	,	-4400	],
    [	4400	,	-4400	],
    [	7880	,	-4400	],
    [	-8520	,	-7880	],
    [	-6320	,	-7880	],
    [	-4120	,	-7880	],
    [	-1920	,	-7880	],
    [	 920	,	-7880	],
    [	4400	,	-7880	],
    [	7880	,	-7880	],
]


def make():
    dic = {}
    dic["RETICLENAME"] = "template"
    dic["DESCRIPTION"] = "Template"
    dic["RETICLESIZE"] = [19640, 19640]
    dic["BOUNDMARGIN"] = [250, 250]
    dic["PADGAP"]      = [100, 100]
    dic["LAYERNUM"] = {
            "JTE"  : 1,
            "GR"   : 1, 
            "FGR"  : 1, 
            "GAIN" : 2,
            "PSTOP": 3,
            "METAL": 4,
            "NPLUS": 5,
            "OXIDE": 6,
            "AUX"  : 80,
            "WAFER": 81
        }
    dic["PARAMDEFAULT"] = {
            "nx"         : 1,
            "ny"         : 1,
            "center"     : [0, 0],
            "jte_width"  : 20,
            "pstop_gap"  : 25,
            "pstop_width": 10,
            "gr_gap"     : 25,
            "gr_width"   : [65, 105],
            "Nfg"        : 0,
            "fg_gap"     : [40, 20],
            "fg_width"   : 30,
            "edge_gap"   : 80,
            "rounding"   : True,
            "rotation"   : 0
        }
    dic["LAYERDEFAULT"] = {
            "gain": True,
            "nplus": True,
            "jte": True,
            "padmetal": True,
            "padoxide": True,
            "pstop": True,
            "guardring": True,
            "edge": True
        }

    dic["SENSORS"] = []

    dic_sensor = {
            "NUM"        : 1,
            "NAME"       : "",
            "INDEX"      : "(1, 1)",
            "SIZE"       : [0, 0],
            "CENTER"     : [0, 0],
            "PARAMETERS" : {
                "nx": 1,
                "ny": 1,
                "center": [0, 0],
                "jte_width": 20
            },
            "LAYEROPTOUT": {
            }
        }

    num = 0
    for i in range(7):
        for j in range(7):
            num += 1 

            nx = 2 if j > 3 else 1
            ny = 2 if i > 3 else 1

            if (nx, ny) == (1, 2):
                nx, ny = 2, 1
                rotation = 90
            else:
                rotation = 0

            sizex = 820 + 1280*nx
            sizey = 820 + 1280*ny

            dic_sensor["NUM"] = int(num)
            dic_sensor["NAME"] = ""
            dic_sensor["INDEX"] = f"({i+1}, {j+1})"
            dic_sensor["SIZE"] = [sizex, sizey]
            dic_sensor["CENTER"] = centers[num-1]
            dic_sensor["PARAMETERS"] = {
                "nx": nx,
                "ny": ny,
                "center": dic_sensor["CENTER"]
            }
            if rotation:
                dic_sensor["PARAMETERS"]["rotation"] = 90
            dic["SENSORS"].append(dic_sensor.copy()) 

    js = json.dumps(dic, indent=4) 

    pattern = r'\[\s*(-?\d+)\s*,\s*(-?\d+)\s*\]'
    replacement = r'[\1, \2]'

    js1 = re.sub(pattern, replacement, js)

    with open("reticle_template.json", "w", encoding="utf-8") as f:
        f.write(js1) 


if __name__=="__main__":
    make()

