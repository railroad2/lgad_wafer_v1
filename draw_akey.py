import numpy as np
import pylab as plt

from phidl import geometry as pg
from phidl import Device

import lgad_draw as lg

class DrawAlignkey:
    layerset = lg.layer_default.layerset

    center_size = (1800, 800)
    center_width = -10

    sidewin_size = (1800, 400)
    sidewin_offset = 20

    posrect_size = (220, 250)
    posrect_array = (3, 8)

    lx_l = 150 
    lx_w = lx_l/3
    sx_l = 90
    sx_w = sx_l/3

    d_posrect = None
    r_posrect = []


    akey_setup = {
        'AKEY': {
            'text'    : "AKE",
            'lcoords' : [(0, 0), (0, 2), (0, 4), (0, 6), (1, 0), (1, 4), (2, 2)],
            'scoords' : [(0, 1), (0, 3), (0, 5), (0, 7), (1, 1), (1, 5), (2, 3)],
            'xoffset' : 0
            },
        'JTE': {
            'text'    : "JTE",
            'lcoords' : [(0, 0)],
            'scoords' : [(0, 1)],
            'xoffset' : 5
        },
        'GAIN': {
            'text'    : "GAI",
            'lcoords' : [(0, 2)],
            'scoords' : [(0, 3)],
            'xoffset' : [5]
        },
        'NPLUS': {
            'text'    : "NPL",
            'lcoords' : [(0, 4)],
            'scoords' : [(0, 5)],
            'xoffset' : [5]
        },
        'PSTOP': {
            'text'    : "PST",
            'lcoords' : [(0, 6)],
            'scoords' : [(0, 7)],
            'xoffset' : [5]
        },
        'ILD': {
            'text'    : "ILD",
            'lcoords' : [(1, 0), (1, 2), (2, 0)],
            'scoords' : [(1, 1), (1, 3), (2, 1)],
            'xoffset' : [5, 5, 5]
        },
        'METAL': {
            'text'    : "MET",
            'lcoords' : [(1, 2), (1, 4), (2, 4)],
            'scoords' : [(1, 3), (1, 5), (2, 5)],
            'xoffset' : [0, -5, -5]
        },
        'OXIDE': {
            'text'    : "OXI",
            'lcoords' : [(2, 0), (2, 2), (2, 4)],
            'scoords' : [(2, 1), (2, 3), (2, 5)],
            'xoffset' : [0, 5, 0]
        },
    }

    def __init__(self):
        pass

    def draw_frame(self, layer=layerset):
        rect_out = pg.rectangle(size=(10100, 15700))
        rect_in  = pg.rectangle(size=(9000, 9000))
        rect_out.center = (0, 0)
        rect_in.center = (0, 0)
        frame = pg.boolean(rect_out, rect_in, operation='not', layer=1)

        return frame

    def draw_cross(self, length, layer):
        recth = pg.rectangle(size=(length, length/3), layer=layer)
        recth.center = (0, 0)
        rectv = pg.rectangle(size=(length/3, length), layer=layer)
        rectv.center = (0, 0)
        cross = pg.boolean(recth, rectv, operation='or', layer=layer)
        return cross
        
    def draw_window(self, size, layer, width=0, arrows=False):
        d_arrow = Device('arrow')
        d_arrows= Device('arrows')

        pts_arrow = [
                (0, 0), 
                (-50*np.cos(np.pi/4), -50*np.sin(np.pi/4)),
                (-15, -50*np.sin(np.pi/4)), 
                (-15, -50*np.sin(np.pi/4)-40), 
                (15, -50*np.sin(np.pi/4)-40), 
                (15, -50*np.sin(np.pi/4)), 
                (50*np.cos(np.pi/4), -50*np.sin(np.pi/4)),
            ]

        d_arrow.add_polygon(points=pts_arrow, layer=layer)
         
        rect = pg.rectangle(size=size, layer=layer) 
        if width:
            rect = pg.outline(rect, distance=width, layer=layer)

        rect.center = (0, 0)

        if arrows:
            d_arrow1 = d_arrows.add_ref(d_arrow)
            d_arrow2 = d_arrows.add_ref(d_arrow)
            d_arrow3 = d_arrows.add_ref(d_arrow)
            d_arrow4 = d_arrows.add_ref(d_arrow)

            d_arrow1.rotate(-45)
            d_arrow2.rotate(45)
            d_arrow3.rotate(135)
            d_arrow4.rotate(225)

            d_arrow1.xmax =  size[0]/2-10
            d_arrow1.ymax =  size[1]/2-10
            d_arrow2.xmin = -size[0]/2+10
            d_arrow2.ymax =  size[1]/2-10
            d_arrow3.xmin = -size[0]/2+10
            d_arrow3.ymin = -size[1]/2+10
            d_arrow4.xmax =  size[0]/2-10
            d_arrow4.ymin = -size[1]/2+10

            rect = pg.boolean(rect, d_arrows, operation='not', layer=layer)

        return rect

    def draw_posrect(self, layer=layerset['AUX']):
        d_posrect = Device('posrect')
        
        r_posrect = []
        for i in range(self.posrect_array[0]):
            r_tmps = []
            for j in range(self.posrect_array[1]):
                d_rect = pg.rectangle(size=self.posrect_size, layer=layer)
                r_tmp = d_posrect.add_ref(d_rect)
                r_tmp.center = (j*self.posrect_size[0], - i*self.posrect_size[1])
                r_tmps.append(r_tmp)

            r_posrect.append(r_tmps)
        
        d_posrect.center = (0, 0)
        self.d_posrect = d_posrect
        self.r_posrect = r_posrect

        return d_posrect

    def place_large_crosses(self, coords, layer, offset=0):
        if self.r_posrect == []:
            self.draw_posrect()

        if isinstance(offset, (int, float)):
            offset = [offset] * len(coords)

        d_lx = Device('large_x')
        large_cross = self.draw_cross(length=self.lx_l, layer=layer)

        for coord, off in zip(coords, offset):
            if off:
                large_cross1 = pg.offset(large_cross, distance=off, layer=layer)
            else:
                large_cross1 = large_cross

            r_lx = d_lx.add_ref(large_cross1)
            r_lx.center = self.r_posrect[coord[0]][coord[1]].center
            
        return d_lx

    def place_small_crosses(self, coords, layer, offset=0):
        if self.r_posrect == []:
            self.draw_posrect()

        if isinstance(offset, (int, float)):
            offset = [offset] * len(coords)

        d_sx = Device('small_x')
        small_cross = self.draw_cross(length=self.sx_l, layer=layer)

        for coord, off in zip(coords, offset):
            if off:
                small_cross1 = pg.offset(small_cross, distance=off, layer=layer)
            else:
                small_cross1 = small_cross
            r_sx = d_sx.add_ref(small_cross1)
            r_sx.center = self.r_posrect[coord[0]][coord[1]].center
            
        return d_sx

    def draw_keys(self):
        d_keys = Device('keys')
        for k, v in self.akey_setup.items():
            if 'xoffset' in v.keys():
                xoffset = v['xoffset']
            else:
                xoffset = 0

            d_keys.add_ref(self.place_large_crosses(v['lcoords'], layer=self.layerset[k], offset=xoffset))
            d_keys.add_ref(self.place_small_crosses(v['scoords'], layer=self.layerset[k], offset=xoffset))

        return d_keys

    def load_align_key(self, fname):   
        d_alignkey = pg.import_gds(fname, cellname='toplevel')
        d_alignkey.center = (0, 0)

        return d_alignkey

    def draw_centerframe(self, ):
        d_cf = Device('center_frame')
        for i in range(1, 9):
            d_cf.add_ref(self.draw_window(size=self.center_size, width=self.center_width, layer=i))

        return d_cf

    def draw_sidewindow(self, ):
        d_win = Device('window')

        d_win.add_ref(self.draw_window(size=np.array(self.sidewin_size)-20, 
                                  layer=self.layerset['AKEY'], arrows=True))

        for i in [2, 3, 4, 5, 6, 8]:
            d_win.add_ref(self.draw_window(size=self.sidewin_size, layer=i))

        d_win.add_ref(self.draw_window(size=np.array(self.sidewin_size)-20, width=-10, layer=7))

        d_win.center=(0, 0)
        return d_win

    def draw_all(self):
        D = Device('alignkey')

        # align keys
        r_key = D.add_ref(self.load_align_key('align_keys/akey.gds'))
        r_key.center = (2000, 0)

        # center frame
        r_cf = D.add_ref(self.draw_centerframe())
        r_cf.center = (0, 0)
        
        # upper window
        r_upper = D.add_ref(self.draw_sidewindow())
        r_upper.center = (0, (self.center_size[1] + self.sidewin_size[1])/2 + self.sidewin_offset)

        r_lower = D.add_ref(self.draw_sidewindow())
        r_lower.center = (0, -(self.center_size[1] + self.sidewin_size[1])/2 - self.sidewin_offset)

        r_posrect = D.add_ref(self.draw_posrect())

        # keys
        r_keys = D.add_ref(self.draw_keys())

        D.write_gds('akey1.gds')

        return D

if __name__=="__main__":
    da = DrawAlignkey()
    d = da.draw_all()
    
    lg.qp(d)
    plt.show()


