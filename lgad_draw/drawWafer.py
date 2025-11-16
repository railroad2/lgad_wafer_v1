import os
import json

import numpy as np

from phidl import geometry as pg
from phidl import Device, LayerSet

import lgad_draw as lg
from .layer_default import LAYERNUM

LAYERS = LAYERNUM

class DrawWafer:
    wafer_diameter   = 150   * 1000 # inch -> mm -> um
    wafer_cut_length =  57.5 * 1000 # mm -> um
    ebr_width        = 5000         # um

    wafer_radius     = wafer_diameter / 2
    wafer_cut_half   = wafer_cut_length / 2
    wafer_cut_dist   = (wafer_radius**2 - wafer_cut_half**2) ** 0.5

    reticle_size = (19140, 19140)
    reticle_margin = (250, 250)

    d_loaded = {}

    def __init__(self):
        pass

    def DrawBoundary(self, layer=LAYERS['WAFER']):
        circ = pg.circle(radius = self.wafer_radius, layer=layer)
        circ.center = (0, 0)

        rect = pg.rectangle((self.wafer_diameter+10, self.wafer_cut_dist+ self.wafer_radius+10), layer=99)
        rect.center = (0, (self.wafer_radius - self.wafer_cut_dist)/2)

        wafer = pg.boolean(rect, circ, operation='and', layer=layer)

        wafer_inner = pg.offset(wafer, distance=-self.ebr_width, layer=99)

        wafer = pg.boolean(wafer, wafer_inner, operation='not', layer=layer)
        return wafer

    def DrawReticleBoundaries(self, layer=LAYERS['AUX']):
        rect_in = pg.rectangle(size=self.reticle_size, layer=99)
        rect_out = pg.offset(rect_in, distance=self.reticle_margin[0], layer=99)
        rect = pg.boolean(rect_out, rect_in, operation='not', layer=layer)

        d_reticles_boundary = Device('reticles')
        reticles = []
        for i in range(7):
            for j in range(7):
                if (i, j) in [(0, 0), (0, 6), (6, 0), (6, 6)]: 
                    continue

                rect1 = d_reticles_boundary.add_ref(rect)
                rect1.center = ((j-3) * (self.reticle_size[0] + 2*self.reticle_margin[0]),
                                (i-3) * (self.reticle_size[1] + 2*self.reticle_margin[1]))

                print (rect1.center)

        return d_reticles_boundary
        
    def PlaceReticles(self):
        d_reticle_A = pg.import_gds('reticle_gds/reticle_KNU_LGAD_v1_RI-01.gds')
        d_reticle_A.name = 'reticle_A'
        D_reticles = Device('reticles')
        reticles = []
        
        k = 0
        for i in range(7):
            for j in range(7):
                if (i, j) in [(0, 0), (0, 6), (6, 0), (6, 6)]: 
                    continue

                k += 1
                rect1 = D_reticles.add_ref(d_reticle_A)
                rect1.name = f'recticle_A_{k:03}'
                rect1.center = ((j-3) * (self.reticle_size[0] + 2*self.reticle_margin[0]),
                                (i-3) * (self.reticle_size[1] + 2*self.reticle_margin[1]))
                print (rect1.center)

        return D_reticles

    def PlaceReticles_from_json(self, jsonname):
        jdata = self.ReadJson(jsonname)
        self.wafername = jdata['WAFERNAME']
        self.jsonpath = jdata['JSONPATH']
        self.gdspath = jdata['GDSPATH']
        self.reticles = jdata['RETICLES']
        self.bsize = jdata['BLANKSIZE']

        D_reticles = Device('reticles')

        for i, ret in enumerate(self.reticles):
            rname = ret['NAME']
            rtype = ret['TYPE']
            rcenter = ret['CENTER']
            srcfile = ret['SRCFILE']
            nfg = ret['NFG']

            rtname = f'{rtype}'
            d_ret = D_reticles.add_ref(self.LoadSrc(srcfile, rtname))
            d_ret.center = rcenter

            wrname = f"{self.wafername} - {rname} {rtype}"
            d_names = D_reticles.add_ref(
                        self.DrawReticleNames(
                            srcfile, wrname, rcenter, self.bsize))

            print (f'[DrawWafer] {i:02} {rname}-{rtype} is placed at {rcenter}')

        return D_reticles

    def PlaceAlignkeys_from_json(self, jsonname, outline_size=None, outline_width=50):
        jdata = self.ReadJson(jsonname)
        akeys = jdata['ALIGNKEYS']

        D_akey = Device('alignkeys')

        for i, key in enumerate(akeys):
            num = key['NUM']
            center = key['CENTER']
            srcfile = key['SRCFILE']

            dname = f'alignkey-{num}'
            d_key = D_akey.add_ref(self.LoadSrc(srcfile, dname))
            d_key.center = center

            print (f'[DrawWafer] {num:02} an align key is placed at {center}')

        ls = LayerSet()
        ls.add_layer(name = 'akey', gds_layer = 1, description='align key 0')
        ls.add_layer(name = 'jte',  gds_layer = 2, description='jte and guardrings')
        ls.add_layer(name = 'gain', gds_layer = 2, description='gain layer')

        if outline_size:
            for i, key in enumerate(akeys):
                center = key['CENTER']

                for j in range(1, 9):
                    rect_in = pg.rectangle(size=outline_size, layer=99)
                    rect_out = pg.offset(rect_in, distance=outline_width, layer=99)
                    rect_out = pg.boolean(rect_out, rect_in, operation='not', layer=j)
                    rect_out.center = center
                    D_akey << rect_out

        return D_akey

    def LoadSrc(self, srcfile, rtname=None):
        print (f'[DrawWafer] Loading {srcfile}')
        if srcfile in self.d_loaded.keys():
            return self.d_loaded[srcfile]

        if os.path.exists(srcfile):
            if os.path.splitext(srcfile)[-1] == '.gds':
                ret = self.LoadSrc_gds(srcfile, rtname)
            elif os.path.splitext(srcfile)[-1] == '.json':
                ret = self.LoadSrc_json(srcfile, rtname)
            else:
                print (f'{os.path.splitext(srcfile)[-1]}')
                raise
        elif os.path.exists(srcfile+'.gds'):
            ret = self.LoadSrc_gds(srcfile+'.gds', rtname)
        elif os.path.exists(srcfile+'.json'):
            ret = self.LoadSrc_json(srcfile+'.json', rtname)
        elif os.path.exists(os.path.join(self.gdspath, srcfile)):
            ret = self.LoadSrc_gds(os.path.join(self.gdspath, srcfile), rtname)
        elif os.path.exists(os.path.join(self.jsonpath, srcfile)):
            ret = self.LoadSrc_json(os.path.join(self.jsonpath, srcfile), rtname)
        elif os.path.exists(os.path.join(self.gdspath, srcfile+'.gds')):
            ret = self.LoadSrc_gds(os.path.join(self.gdspath, srcfile+'.gds'), rtname)
        elif os.path.exists(os.path.join(self.jsonpath, srcfile+'.json')):
            ret = self.LoadSrc_json(os.path.join(self.jsonpath, srcfile+'.json'), rtname)
        else:
            print (f"[ERROR] The source file is not found: {srcfile}")
            raise

        self.d_loaded[srcfile] = ret

        return ret

    def LoadSrc_gds(self, fname, rtname=None):
        d_reticle = pg.import_gds(fname)

        if rtname:
            d_reticle.name = rtname
        else:
            d_reticle.name = fname

        return d_reticle

    def LoadSrc_json(self, fname, rtname=None):
        # draw the reticle and write in a gds file
        jdata = self.ReadJson(fname)
        reticle_name = jdata['RETICLENAME']

        if rtname:
            reticle_name = rtname

        reticle = lg.DrawReticle(reticle_name)
        d_reticle = reticle.Draw_from_json(fname)

        gdsname = os.path.join(self.gdspath, os.path.splitext(os.path.split(fname)[-1])[0]+'.gds')
        d_reticle.write_gds(gdsname)
        return d_reticle

    def DrawReticleNames(self, jsonname, wrname, rcenter, bsize, fontsize=60, layer=LAYERS['METAL']):
        nameplate = pg.rectangle(size=bsize, layer=layer)
        nameplate.center = (0, 0)
        d_name = pg.text(text=wrname, size=fontsize, layer=layer)
        d_name.center = (0, 0)
        nameplate = pg.boolean(nameplate, d_name, operation='not', layer=layer)
        D_names = Device('reticle_names')

        if   os.path.exists(jsonname):
            jsonname1 = jsonname 
        elif os.path.exists(jsonname+'.json'):
            jsonname1 = jsonname + '.json'
        elif os.path.exists(os.path.join(self.jsonpath, jsonname)):
            jsonname1 = os.path.join(self.jsonpath, jsonname)
        elif os.path.exists(os.path.join(self.jsonpath, jsonname+'.json')):
            jsonname1 = os.path.join(self.jsonpath, jsonname+'.json')
        else:
            print (f"[ERROR] The json file is not found: {srcfile}")
            raise
    
        jdata = self.ReadJson(jsonname1)
        sensors = jdata['SENSORS']

        for sensor in sensors:
            ssize   = sensor['SIZE']
            scenter = sensor['CENTER']
            rotation = 90
            rncenter = ssize
            d_nameplate = D_names.add_ref(nameplate)
            d_nameplate.rotate(rotation)
            

            d_nameplate.center = (rcenter[0] + scenter[0] -ssize[0]/2 + bsize[1]/2, 
                                  rcenter[1] + scenter[1])   

            if 'rotation' in sensor['PARAMETERS'].keys():
                rotation1 = sensor['PARAMETERS']['rotation']
                d_nameplate.rotate(rotation1, center=(rcenter[0]+scenter[0], rcenter[1]+scenter[1]))
            elif 'rotation' in jdata['PARAMDEFAULT']:
                rotation1 = jdata['PARAMDEFAULT']['rotation']
                d_nameplate.rotate(rotation1, center=(rcenter[0]+scenter[0], rcenter[1]+scenter[1]))
                
            
             
        return D_names
        

    def DrawLayerNames(self):
        d_texts = Device('texts')
        d_texts1 = Device('texts1')
        d_texts2 = Device('texts2')
        d_texts3 = Device('texts3')

        def _get_text(name, layer, font='Arial'):
            try:
                d_txt = pg.text(text=name, size=4000, font=font, layer=layer)
            except ValueError:
                d_txt = pg.text(text=name, size=4000, layer=layer)

            return d_txt

        d_texts1 << _get_text('#1 AKEY',   LAYERS['AKEY'])
        d_texts1 << _get_text('#2 JTE',    LAYERS['JTE'])
        d_texts1 << _get_text('#3 GAIN',   LAYERS['GAIN'])
        d_texts1 << _get_text('#4 NPLUS',  LAYERS['NPLUS'])
        d_texts2 << _get_text('#5 PSTOP',  LAYERS['PSTOP'])
        d_texts2 << _get_text('#6 ILD',    LAYERS['ILD'])
        d_texts2 << _get_text('#7 METAL',  LAYERS['METAL'])
        d_texts2 << _get_text('#8 OXIDE',  LAYERS['OXIDE'])
        d_texts3 << _get_text('#80 WAFER', LAYERS['WAFER'])
        d_texts3 << _get_text('#81 AUX',   LAYERS['AUX'])

        d_texts1.distribute(elements='all', direction='x', spacing=2000, separation=True)
        d_texts1.center = (0, -self.wafer_cut_dist-6000)

        d_texts2.distribute(elements='all', direction='x', spacing=2000, separation=True)
        d_texts2.center = (0, -self.wafer_cut_dist-6000-6000)

        d_texts3.distribute(elements='all', direction='x', spacing=2000, separation=True)
        d_texts3.center = (0, -self.wafer_cut_dist-6000-6000-6000)

        d_texts << d_texts1
        d_texts << d_texts2
        d_texts << d_texts3

        return d_texts

    def ReadJson(self, fname):
        with open(fname, "r", encoding="utf-8") as f:
            jdata = json.load(f)
        return jdata

