import numpy as np
import pylab as plt

import phidl.geometry as pg
from phidl import Device

from .dimPad import DimPad
from . import layer_default 

LAYERS = layer_default.LAYERNUM

class DrawPad:
    d_gain = None
    d_nplus = None
    d_jte = None
    d_padmetal = None
    d_padoxide = None
    tol = 0.1
    join='round'

    def __init__(self, dim_pad): 
        if not isinstance(dim_pad, DimPad):
            raise

        self.dim_pad = dim_pad

    def DrawGain(self, layer=LAYERS['GAIN']):
        size = self.dim_pad.gain_size
        center = self.dim_pad.gain_center

        gain = pg.rectangle(size=size, layer=layer)
        gain.center = center
        gain.simplify(self.tol)

        self.d_gain = gain
        return gain

    def DrawNplus(self, layer=LAYERS['NPLUS']):
        size = self.dim_pad.nplus_size
        center = self.dim_pad.nplus_center

        nplus = pg.rectangle(size=size, layer=layer)
        nplus.center = center
        nplus.simplify(self.tol)

        self.d_nplus = nplus
        return nplus 
        
    def DrawJTE(self, layer=LAYERS['JTE']):
        size = self.dim_pad.jte_size
        width = self.dim_pad.jte_width
        center = self.dim_pad.jte_center

        rect_in  = pg.rectangle(size=size, layer=99)
        rect_out = pg.offset(rect_in, distance=width, join=self.join, layer=99, tolerance=self.tol)
        rect_out.simplify(self.tol)

        jte = pg.boolean(rect_out, rect_in, operation='not', layer=layer)
        jte.center = center
        jte.simplify(self.tol)

        self.jte_out = rect_out

        self.d_jte = jte
        return jte

    def DrawPstop(self, layer=LAYERS['PSTOP']):
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

    def DrawPadMetal(self, layer=LAYERS['METAL']):
        size = self.dim_pad.padmetal_size
        center = self.dim_pad.padmetal_center
        optwin_N = self.dim_pad.optwin_N
        optwin_size = self.dim_pad.optwin_size
        optwin_pos  = self.dim_pad.optwin_pos

        metal = pg.rectangle(size=size, layer=layer)
        metal.center = center

        for i in range(optwin_N):
            rect_win = pg.rectangle(size=optwin_size[i], layer=99)
            rect_win.center = optwin_pos[i]
            metal = pg.boolean(metal, rect_win, operation='not', layer=layer)
            
        metal.simplify(self.tol)

        self.d_padmetal = metal
        return metal

    def DrawPadOxide(self, layer=LAYERS['OXIDE']):
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
            rect_win.center = optwin_pos[i]
            oxide = pg.boolean(oxide, rect_win, operation='not', layer=layer)

        oxide.simplify(self.tol)

        self.d_padoxide = oxide
        return oxide

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


