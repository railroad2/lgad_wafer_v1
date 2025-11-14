import json

import phidl.geometry as pg
from phidl import Device

import lgad_draw as lg

class DrawReticle:
    boundary_size   = (19140, 19140)
    boundary_margin = (250, 250)
    pad_gap         = (100, 100)

    d_reticle = None
    
    def __init__(self, dname='reticle'):
        self.d_reticle = Device(dname)

    def Draw_raw(self):
        from .reticle_setup import ssetup
        boundary_margin = self.boundary_margin
        pad_gap = self.pad_gap
        rect_boundary = pg.rectangle(self.boundary_size, layer=80)
        rect_boundary.center = (self.boundary_size[0]/2, -self.boundary_size[1]/2)

        self.d_reticle.add(rect_boundary)

        pos = [boundary_margin[0], -boundary_margin[1]]

        for i, row in enumerate(ssetup[:]):
            for j, col in enumerate(row):
                sensor = lg.DrawSensor(**col)

                if j == 0:
                    pos[0] += sensor.xsize/2
                    pos[1] -= sensor.ysize/2
                else:
                    pos[0] += sensor0.xsize/2 + sensor.xsize/2 + pad_gap[0]

                sensor.center = pos
                print (i, j, sensor.center, self.d_reticle.center)
                self.d_reticle.add(sensor)
                sensor0 = sensor

            pos[1] = pos[1] - sensor.ysize/2 - pad_gap[1]
            pos[0] = boundary_margin[0] 
        
        self.d_reticle.center = (0, 0)
        return self.d_reticle
             
    def Draw_from_json(self, fname):
        jdata = self.ReadJson(fname)

        reticle_name    = jdata["RETICLENAME"]
        boundary_size   = jdata["RETICLESIZE"]
        boundary_margin = jdata["BOUNDMARGIN"]
        pad_gap         = jdata["PADGAP"]
        LAYERS          = jdata["LAYERNUM"]
        paramdefault    = jdata["PARAMDEFAULT"]
        layerdefault    = jdata["LAYERDEFAULT"]
        prefix          = jdata["SENSORPREFIX"]
    
        sensors_info    = jdata["SENSORS"]

        rect_boundary = pg.rectangle(self.boundary_size, layer=LAYERS['AUX'])
        rect_out = pg.rectangle((self.boundary_size[0]+self.boundary_margin[0]*2, 
                                self.boundary_size[1]+self.boundary_margin[1]*2), layer=99)
        rect_out.center = (0, 0)
        rect_boundary.center = (0, 0)
        rect_boundary = pg.boolean(rect_out, rect_boundary, operation='not', layer=LAYERS['AUX'])

        self.d_reticle.add(rect_boundary)

        for i, info in enumerate(sensors_info):
            num = info["NUM"]
            idx = info["INDEX"]

            if i != num - 1:
                print (f"[WARNING] the index ({i}) and the sensor number ({num}-1) are inconsistent!")

            center = info["CENTER"]
            sensor_name = info["NAME"]

            params = paramdefault.copy()
            layeropt = layerdefault.copy()

            for key, val in info['PARAMETERS'].items():
                params[key] = val
             
            for key, val in info['LAYEROPTOUT'].items():
                layeropt[key] = val

            if sensor_name == "":
                sensor_name = self.ConstructSensorName(prefix, params, layeropt)

            # draw the sensor!
            sensor = lg.DrawSensor(**params, **layeropt, 
                                   sensor_name=sensor_name, reticle_name=reticle_name,
                                   layers=LAYERS)

            sensor.center = center
            self.d_reticle.add(sensor)

            print (f"Sensor #{num} of {idx} is added at {center}")
        
        self.d_reticle.center = (0, 0)
        return self.d_reticle

    def Draw(self, fname=None):
        return self.Draw_from_json(fname)

    def ReadJson(self, fname):
        with open(fname, "r", encoding="utf-8") as f:
            jdata = json.load(f)
        return jdata

    def ConstructSensorName(self, prefix, params, layeropt): 
        nx = params["nx"]
        ny = params["ny"]
        Nfg = params["Nfg"]
        lgadpin = "L" if layeropt["gain"] else "P"
        jte_width = params["jte_width"]
        pstop_width = params["pstop_width"]

        sname = prefix
        sname += f' -{nx}x{ny}'
        sname += f' -{lgadpin}'
        sname += f' -F{Nfg}'
        sname += f' -J{jte_width}'
        sname += f' -P{pstop_width}'

        return sname

