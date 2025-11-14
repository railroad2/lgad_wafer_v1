import os
import json

from phidl import geometry as pg
from phidl import Device

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
        js = self.ReadJson(jsonname)
        self.wafername = js['WAFERNAME']
        self.jsonpath = js['JSONPATH']
        self.gdspath = js['GDSPATH']
        reticles = js['RETICLES']

        D_reticles = Device('reticles')

        for i, ret in enumerate(reticles):
            rname = ret['NAME']
            rtype = ret['TYPE']
            center = ret['CENTER']
            srcfile = ret['SRCFILE']
            nfg = ret['NFG']

            rtname = f'{rtype}-FG{nfg}'
            d_ret = D_reticles.add_ref(self.LoadSrc(srcfile, rtname))
            d_ret.center = center

            print (f'[DrawWafer] {i:02} {rname}-{rtype}-FG{nfg} is placed at {center}')

        return D_reticles

    def LoadSrc(self, srcfile, rtname=None):
        if srcfile in self.d_loaded.keys():
            return self.d_loaded[srcfile]

        if os.path.exists(srcfile):
            if os.path.splitext(srcfile)[-1] == 'gds':
                ret = self.LoadSrc_gds(srcfile, rtname)
            elif os.path.splitext(srcfile)[-1] == 'json':
                ret = self.LoadSrc_json(srcfile, rtname)
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

        ret.name = srcfile
        self.d_loaded[srcfile] = ret

        return ret

    def LoadSrc_gds(self, fname, rtname=None):
        d_reticle = pg.import_gds(fname)
        if rtname:
            d_reticle.name = rtname
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

    def DrawLayerNames(self):
        d_texts = Device('texts')
        d_texts1 = Device('texts1')
        d_texts2 = Device('texts2')
        d_texts3 = Device('texts3')

        def _get_text(name, layer, font='Arial'):
            d_txt = pg.text(text=name, size=4000, font=font, layer=layer)
            return d_txt

        d_texts1 << _get_text('#1 AKEY',   LAYERS['AKEY'])
        d_texts1 << _get_text('#2 JTE/GR', LAYERS['JTE'])
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

