import phidl.geometry as pg
from phidl import Device

from .dimPeriphery import DimPeriphery
from . import layer_default

LAYERS = layer_default.LAYERNUM

class DrawPeriphery:
    tol = 0.1
    join='round'

    def __init__(self, dim_per):
        if not isinstance(dim_per, DimPeriphery):
            raise

        self.d_outmost = None
        self.dim_per = dim_per

    def DrawPstop(self, layer=LAYERS['PSTOP']):
        size = self.dim_per.pstop_size
        boff = self.dim_per.pstop_boff
        bsize = (size[0] - 2*boff, size[1] - 2*boff)

        width = self.dim_per.pstop_width
        center = self.dim_per.pstop_center

        boff_in = self.dim_per.pstop_boff_in
        size_in = self.dim_per.pstop_size_in
        bsize_in = (size_in[0] - 2*boff_in, size_in[1] - 2*boff_in)

        nx = self.dim_per.nx
        ny = self.dim_per.ny

        rect_base = pg.rectangle(size=bsize, layer=99)
        rect_out  = pg.offset(rect_base, distance=boff, join=self.join, layer=99, tolerance=self.tol)
        rect_out.simplify(self.tol)

        rect_bin  = pg.rectangle(size=bsize_in, layer=99)
        rect_in   = pg.offset(rect_bin, distance=boff_in, join=self.join, layer=99, tolerance=self.tol)
        rect_in.simplify(self.tol)

        pstop     = rect_out
        pstop.center = center

        k = 0
        for i in range(ny):
            for j in range(nx):
                rect_in.center = self.dim_per.c_pads[k]
                pstop = pg.boolean(pstop, rect_in, operation='not', layer=layer)
                k += 1

        pstop.simplify(self.tol)
        self.d_pstop = pstop
        
        return pstop

    def DrawGR(self, layer=LAYERS['JTE'], layer_metal=LAYERS['METAL'], layer_oxide=LAYERS['OXIDE'], layer_ild=LAYERS['ILD']):
        bsize = self.dim_per.base_size
        bcenter = self.dim_per.base_center
        gap = self.dim_per.gr_gap
        width = self.dim_per.gr_width
        widthb = self.dim_per.gr_widthb
        center = self.dim_per.gr_center
        pad_offset = self.dim_per.pad_offset
        ild_offset = self.dim_per.ild_offset


        # inner rectangle
        rect_base = pg.rectangle(size=bsize, layer=99)
        rect_pads = pg.offset(rect_base, distance=pad_offset, join=self.join, layer=99, tolerance=self.tol)
        rect_pads.center = bcenter
        rect_pads.simplify(self.tol)

        rect_in = pg.offset(rect_pads, distance=gap, join=self.join, layer=99, tolerance=self.tol)
        rect_in.simplify(self.tol)

        # outer rectangle
        rect_base1 = pg.rectangle(size=(bsize[0], bsize[1] + (widthb-width)), layer=99)
        rect_base1.center = center
        rect_out = pg.offset(rect_base1, distance=pad_offset+width+gap, join=self.join, layer=99, tolerance=self.tol)
        rect_out.simplify(self.tol)
        
        gr = pg.boolean(rect_out, rect_in, operation='not', layer=layer)

        # gr ILD
        rect_out_0 = pg.offset(rect_out, distance=-ild_offset , join=self.join, layer=99, tolerance=self.tol)
        rect_in_0  = pg.offset(rect_in,  distance= ild_offset, join=self.join, layer=99, tolerance=self.tol)
        ild = pg.boolean(rect_out_0, rect_in_0, operation='not', layer=layer_ild)
        ild.simplify(self.tol)

        # gr metal
        rect_out_1 = pg.offset(rect_out, distance= 0, join=self.join, layer=99, tolerance=self.tol)
        rect_in_1  = pg.offset(rect_in,  distance= 0, join=self.join, layer=99, tolerance=self.tol)
        metal = pg.boolean(rect_out_1, rect_in_1, operation='not', layer=layer_metal)
        metal.simplify(self.tol)

        # gr oxide open
        rect_out_2 = pg.offset(rect_out_1, distance=-5, join=self.join, layer=99, tolerance=self.tol)
        rect_in_2  = pg.offset(rect_in_1,  distance= 5, join=self.join, layer=99, tolerance=self.tol)
        oxide = pg.boolean(rect_out_2, rect_in_2, operation='not', layer=layer_oxide)
        oxide.simplify(self.tol)

        gr.add(ild)
        gr.add(metal)
        gr.add(oxide)
        #gr.simplify(self.tol)
        self.d_gr = gr

        self.d_outmost = rect_out

        return gr

    def DrawFGs(self, Nfg=2, layer=LAYERS['JTE']):
        d_fgs = Device('fgs')

        if Nfg == 0:
            return 

        base = self.d_outmost
        gap = self.dim_per.fg_gap
        if not isinstance(gap, (list, tuple)):
            gap = [gap, gap] 
        width = self.dim_per.fg_width
        center = self.dim_per.gr_center


        for i in range(Nfg): 
            rect_in   = pg.offset(base, distance=gap[0]+(gap[1]+width)*i, join=self.join, layer=99, tolerance=self.tol)
            rect_out  = pg.offset(base, distance=gap[0]+width+(gap[1]+width)*i, join=self.join, layer=99, tolerance=self.tol)

            fg = pg.boolean(rect_out, rect_in, operation='not', layer=layer)
            d_fgs << fg

        d_fgs.center = center
        d_fgs.simplify(self.tol)

        self.d_fgs = d_fgs
        self.d_outmost = rect_out
        
        return d_fgs

    def DrawEdge(self, sensor_name=None, reticle_name=None, fontsize=60, 
                 layer=LAYERS['METAL'], oxide_open=True, layer_oxide=LAYERS['OXIDE']):
        size = self.dim_per.edge_size
        center = self.dim_per.edge_center
        grcenter = self.dim_per.gr_center
        gap   = self.dim_per.edge_gap
        width = self.dim_per.edge_width
        bgap  = self.dim_per.edge_bgap

        rect_out = pg.rectangle(size, layer=99)
        rect_out.center = center
        rect_base = pg.offset(rect_out, distance=-bgap)
        rect_in = pg.offset(self.d_outmost, distance=gap, join=self.join, tolerance=self.tol)
        rect_in.center = grcenter

        edge = pg.boolean(rect_out, rect_in, operation='not', layer=layer)
        edge.center = center

        if sensor_name is None or sensor_name == "":
            sname = pg.text(text = self.dim_per.sensor_name, size=fontsize, justify='center', layer=layer)
        else:
            sname = pg.text(text = sensor_name, size=fontsize, justify='center', layer=layer)

        sname.center = (edge.x, edge.ymax - width/2)
        edge = pg.boolean(edge, sname, operation='not', layer=layer)

        if reticle_name is None or sensor_name == "":
            pass
        else:
            rname = pg.text(text = reticle_name, size=fontsize, justify='center', layer=layer)
            rname.rotate(90)
            rname.center = (edge.xmin + width/2, edge.y)
            edge = pg.boolean(edge, rname, operation='not', layer=layer)

        if oxide_open:
            oxopen = Device('edge_oxide_open')
            size = (100, 100)
            oxopen1 = pg.rectangle(size, layer=layer_oxide)

            ref1 = oxopen.add_ref(oxopen1)
            ref2 = oxopen.add_ref(oxopen1)
            ref3 = oxopen.add_ref(oxopen1)
            ref4 = oxopen.add_ref(oxopen1)

            ref1.center = (edge.xmin + 10 + size[0]/2, edge.ymin + 10 + size[1]/2)

            ref2.center = (edge.xmin + 10 + size[0]/2, edge.ymax - 10 - size[1]/2)

            ref3.center = (edge.xmax - 10 - size[0]/2, edge.ymax - 10 - size[1]/2)

            ref4.center = (edge.xmax - 10 - size[0]/2, edge.ymin + 10 + size[1]/2)

            edge.add(oxopen)


        edge.simplify(self.tol)
        self.d_edge = edge

        return edge

    def Draw(self):
        d_per = Device('per')
        self.DrawPstop()
        print ('DrawPstop')
        self.DrawGR()
        print ('DrawGR')
        self.DrawFGs()
        print ('DrawFGs')
        self.DrawEdge()

        d_per.add(self.d_pstop)
        d_per.add(self.d_gr)
        d_per.add(self.d_fgs)
        d_per.add(self.d_edge)

        self.d_per = d_per
        return d_per

