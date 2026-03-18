import sys
import json5
import re

centers = [
    [	-8520	,	 8520	],
    [	-6320	,	 8520	],
    [	-4120	,	 8520	],
    [	-1920	,	 8520	],
    [	  920	,	 8520	],
    [	 4400	,	 8520	],
    [	 7880	,	 8520	],
    [	-8520	,	 6320	],
    [	-6320	,	 6320	],
    [	-4120	,	 6320	],
    [	-1920	,	 6320	],
    [	  920	,	 6320	],
    [	 4400	,	 6320	],
    [	 7880	,	 6320	],
    [	-8520	,	 4120	],
    [	-6320	,	 4120	],
    [	-4120	,	 4120	],
    [	-1920	,	 4120	],
    [	  920	,	 4120	],
    [	 4400	,	 4120	],
    [	 7880	,	 4120	],
    [	-8520	,	 1920	],
    [	-6320	,	 1920	],
    [	-4120	,	 1920	],
    [	-1920	,	 1920	],
    [	  920	,	 1920	],
    [	 4400	,	 1920	],
    [  	 7880	,	 1920	],
    [	-8520	,	 -920	],
    [	-6320	,	 -920	],
    [	-4120	,	 -920	],
    [	-1920	,	 -920	],
    [	  920	,	 -920	],
    [	 4400	,	 -920	],
    [	 7880	,	 -920	],
    [	-8520	,	-4400	],
    [	-6320	,	-4400	],
    [	-4120	,	-4400	],
    [	-1920	,	-4400	],
    [	  920	,	-4400	],
    [	 4400	,	-4400	],
    [	 7880	,	-4400	],
    [	-8520	,	-7880	],
    [	-6320	,	-7880	],
    [	-4120	,	-7880	],
    [	-1920	,	-7880	],
    [	  920	,	-7880	],
    [	 4400	,	-7880	],
    [	 7880	,	-7880	],
]


def make():
    if len(sys.argv) > 1:
        sensor_prefix = sys.argv[1]
    else:
        sensor_prefix = "KNU LGAD v1"

    dic = {}
    dic["RETICLENAME"] = "template"
    dic["DESCRIPTION"] = "Template"
    dic["RETICLESIZE"] = [19140, 19140]
    dic["BOUNDMARGIN"] = [250, 250]
    dic["BLANKNAME"]   = True
    dic["BLANKSIZE"]   = [1500, 150]
    dic["PADGAP"]      = [100, 100]
    dic["PARAMDEFAULT"] = {
            "nx"         : 1,
            "ny"         : 1,
            "center"     : [0, 0],
            "jte_width"  : 20,
            "auto_pstop_gap": False,
            "pstop_gap"  : 25,
            "pstop_width": 10,
            "auto_gr_gap": False,
            "gr_gap"     : 25,
            "gr_width"   : [65, 105],
            "Nfg"        : 0,
            "fg_gap"     : [40, 20],
            "fg_width"   : 30,
            "edge_gap"   : 80,
            "ild_offset" : 2,
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
    dic["SENSORPREFIX"] = sensor_prefix
    dic["NSENSORS"] = 49
    dic["NHORI"] = 7
    dic["NVERT"] = 7
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
                "jte_width": 20,
                "pstop_gap": 25,
                "gr_gap": 25
            },
            "LAYEROPTOUT": {
            }
        }

    num = 0
    for i in range(dic["NHORI"]):
        for j in range(dic["NVERT"]):
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
                "center": dic_sensor["CENTER"],
                "pstop_gap": dic["PARAMDEFAULT"]["pstop_gap"],
                "gr_gap": dic["PARAMDEFAULT"]["gr_gap"]
            }

            if rotation:
                dic_sensor["PARAMETERS"]["rotation"] = 90

            dic["SENSORS"].append(dic_sensor.copy()) 

    js = json5.dumps(dic, indent=4) 

    pattern = r"\[\s*(-?\d+)\s*,\s*(-?\d+)\s*,?\s*\]"
    js1 = re.sub(pattern, r"[ \1, \2 ]", js)

    #js1 = re.sub(pattern, replacement, js)
    print (js1)

    with open("reticle_template.json5", "w", encoding="utf-8") as f:
        f.write(js1) 

if __name__=="__main__":
    make()
