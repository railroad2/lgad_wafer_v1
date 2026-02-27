import numpy as np
import pylab as plt

import phidl.geometry as pg
from phidl import Device

from .dimPad import DimPad
from . import layer_default 


class DrawPad:
    d_gain = None
    d_nplus = None
    d_jte = None
    d_padmetal = None
    d_padoxide = None
    tol = 0.001
    join='round'
    layerset = layer_default.layerset

    def __init__(self, dim_pad): 
        if not isinstance(dim_pad, DimPad):
            raise

        self.dim_pad = dim_pad

    def DrawGain(self, layer=layerset['GAIN'], rounding=3):
        size = self.dim_pad.gain_size
        center = self.dim_pad.gain_center

        gain = pg.rectangle(size=size, layer=layer)
        if rounding:
            gain = pg.offset(gain, distance=-rounding, layer=layer)
            gain = pg.offset(gain, distance=+rounding, layer=layer, join=self.join, tolerance=self.tol)
        gain.center = center
        gain.simplify(self.tol)

        self.d_gain = gain
        return gain

    def DrawNplus(self, layer=layerset['NPLUS'], rounding=None):
        size = self.dim_pad.nplus_size
        center = self.dim_pad.nplus_center

        if rounding is None:
            rounding = (size[0] - self.dim_pad.nplus_sizeb[0] + 10) / 2

        nplus = pg.rectangle(size=size, layer=layer)
        if rounding:
            nplus = pg.offset(nplus, distance=-rounding, layer=layer)
            nplus = pg.offset(nplus, distance=+rounding, layer=layer, join=self.join, tolerance=self.tol)
        nplus.center = center
        nplus.simplify(self.tol)

        self.d_nplus = nplus
        return nplus 
        
    def DrawJTE(self, layer=layerset['JTE'], rounding_in=5):
        size = self.dim_pad.jte_size
        width = self.dim_pad.jte_width
        center = self.dim_pad.jte_center

        rect_in  = pg.rectangle(size=size, layer=99)

        if rounding_in:
            rect_in = pg.offset(rect_in, distance=-rounding_in, layer=99)
            rect_in = pg.offset(rect_in, distance=+rounding_in, layer=99, join=self.join, tolerance=self.tol)

        rect_out = pg.offset(rect_in, distance=width, join=self.join, layer=99, tolerance=self.tol)
        rect_out.simplify(self.tol)

        jte = pg.boolean(rect_out, rect_in, operation='not', layer=layer)
        jte.center = center
        jte.simplify(self.tol)

        self.d_jte = jte
        self.jte_out = rect_out

        return jte

    def DrawPstop(self, layer=layerset['PSTOP']):
        gap = self.dim_pad.pstop_gap
        width = self.dim_pad.pstop_width
        center = self.dim_pad.pstop_center

        rect_in  = pg.offset(self.jte_out, distance=gap, join=self.join, layer=99, tolerance=self.tol)
        rect_in.simplify(self.tol)
        rect_out = pg.offset(rect_in, distance=width, join=self.join, layer=99, tolerance=self.tol)
        rect_out.simplify(self.tol)

        pstop = pg.boolean(rect_out, rect_in, operation='not', layer=layer)
        pstop.center = center
        pstop.simplify(self.tol)

        self.d_pstop = pstop
        return pstop

    def DrawPadMetal(self, layer=layerset['METAL'], rounding=None, rounding_win=3):
        size = self.dim_pad.padmetal_size
        center = self.dim_pad.padmetal_center
        optwin_N = self.dim_pad.optwin_N
        optwin_size = self.dim_pad.optwin_size
        optwin_pos  = self.dim_pad.optwin_pos

        metal = pg.rectangle(size=size, layer=layer)
        metal.center = center

        if rounding is None:
            rounding = (size[0] - self.dim_pad.nplus_sizeb[0] +10 ) / 2

        for i in range(optwin_N):
            rect_win = pg.rectangle(size=optwin_size[i], layer=99)
            rect_win.center = optwin_pos[i]
            if abs(rect_win.xmin - metal.xmin) < 5:
                rect_add = pg.rectangle(size=optwin_size[i], layer=99)
                rect_add.center = optwin_pos[i]
                rect_add.move((-50, 0))
                rect_win.add_ref(rect_add)
            elif abs(rect_win.xmax - metal.xmax) < 5:
                rect_add = pg.rectangle(size=optwin_size[i], layer=99)
                rect_add.center = optwin_pos[i]
                rect_add.move((50, 0))
                rect_win.add_ref(rect_add)

            if rounding_win:
                rect_win = pg.offset(rect_win, distance=-rounding_win)
                rect_win = pg.offset(rect_win, distance=+rounding_win, join=self.join, tolerance=self.tol)
            metal = pg.boolean(metal, rect_win, operation='not', layer=layer)

        if rounding:
            metal = pg.offset(metal, distance=-rounding, layer=layer)
            metal = pg.offset(metal, distance=+rounding, join=self.join, tolerance=self.tol, layer=layer)
            
        metal.simplify(self.tol)

        self.d_padmetal = metal
        return metal

    def DrawPadOxide(self, layer=layerset['OXIDE'], rounding_win=3, offset_win=10):
        size = self.dim_pad.padoxide_size
        width = self.dim_pad.padoxide_width
        center = self.dim_pad.padoxide_center
        optwin_N = self.dim_pad.optwin_N
        optwin_size = self.dim_pad.optwin_size
        optwin_pos  = self.dim_pad.optwin_pos

        oxide   = pg.rectangle(size=size, layer=layer)
        rect_in = pg.offset(oxide, distance=-width, layer=99)
        oxide   = pg.boolean(oxide, rect_in, operation='not', layer=layer)
        oxide.center = center

        for i in range(optwin_N):
            rect_win = pg.rectangle(size=optwin_size[i], layer=99)
            rect_win = pg.offset(rect_win, distance=offset_win, layer=99)
            rect_win.center = optwin_pos[i]
            oxide = pg.boolean(oxide, rect_win, operation='not', layer=layer)

        oxide.simplify(self.tol)

        self.d_padoxide = oxide
        return oxide

    def DrawPadOxide_16x16(self, layer=layerset['OXIDE'], offset_win=10):
        size = self.dim_pad.padoxide_size
        width = self.dim_pad.padoxide_width
        center = self.dim_pad.padoxide_center
        optwin_N = self.dim_pad.optwin_N
        optwin_size = self.dim_pad.optwin_size
        optwin_pos  = self.dim_pad.optwin_pos

        oxide   = Device('padoxide')#pg.rectangle(size=size, layer=layer)
        bumppad = pg.ellipse(radii=(45, 45), layer=99)
        probepad = pg.rectangle(size=(200, 100), layer=99)
        r_bumppad = oxide.add_ref(bumppad)
        r_probepad = oxide.add_ref(probepad)
        r_bumppad.center = (150, 0)
        r_probepad.center = (125, -225)
        #oxide   = pg.boolean(oxide, bumppad, operation='not', layer=layer)
        #oxide   = pg.boolean(oxide, probepad, operation='not', layer=layer)
        #oxide.center = center

        for i in range(optwin_N):
            rect_win = pg.rectangle(size=optwin_size[i], layer=99)
            rect_win = pg.offset(rect_win, distance=offset_win, layer=99)
            rect_win.center = optwin_pos[i]
            oxide = pg.boolean(oxide, rect_win, operation='not', layer=layer)

        oxide.simplify(self.tol)

        self.d_padoxide = oxide
        return oxide

    def DrawPadILD(self, layer=layerset['ILD'], rounding=3):
        size = self.dim_pad.padmetal_size
        center = self.dim_pad.padmetal_center
        optwin_N = self.dim_pad.optwin_N
        optwin_size = self.dim_pad.optwin_size
        optwin_pos  = self.dim_pad.optwin_pos
        ild_offset = self.dim_pad.ild_offset

        #ild = pg.rectangle(size=(size[0]-ild_offset*2, size[1]-ild_offset*2), layer=layer)
        ild = pg.offset(self.d_padmetal, distance=-ild_offset-rounding, layer=layer, join=self.join, tolerance=self.tol)
        ild = pg.offset(ild, distance=rounding, layer=layer, join=self.join, tolerance=self.tol)
        ild.center = center

        """
        for i in range(optwin_N):
            rect_win = pg.rectangle(size=(optwin_size[i][0]+ild_offset*2, optwin_size[i][1]+ild_offset*2), layer=99)
            rect_win.center = optwin_pos[i]
            ild = pg.boolean(ild , rect_win, operation='not', layer=layer)
        """
            
        ild.simplify(self.tol)

        self.d_padild = ild
        return ild 
        

    def Draw(self, center=(0, 0)):
        d_pad = Device('pad')

        self.DrawGain()
        print ('DrawGain')
        self.DrawNplus()
        print ('DrawNplus')
        self.DrawJTE()
        print ('DrawJTE')
        self.DrawPadMetal()
        print ('DrawPadMetal')
        self.DrawPadOxide()
        print ('DrawPadOxide')

        d_pad.add(self.d_gain)
        d_pad.add(self.d_nplus)
        d_pad.add(self.d_jte)
        d_pad.add(self.d_padmetal)
        d_pad.add(self.d_padoxide)
        d_pad.center = center

        self.d_pad = d_pad
        return d_pad


