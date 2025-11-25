import phidl.geometry as pg
from phidl import Device

from .dimPeriphery import DimPeriphery
from . import layer_default


class DrawPeriphery:
    tol = 0.1
    join='round'
    layerset = layer_default.layerset

    def __init__(self, dim_per):
        if not isinstance(dim_per, DimPeriphery):
            raise

        self.dim_per = dim_per
        self.d_outmost = None


    # ---------------------------------------------------------
    # PSTOP 
    # ---------------------------------------------------------
    def DrawPstop(self, layer=layerset['PSTOP']):
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
        rect_out  = pg.offset(rect_base, distance=boff, join=self.join, tolerance=self.tol)
        rect_out.simplify(self.tol)

        rect_bin  = pg.rectangle(size=bsize_in, layer=99)
        rect_in   = pg.offset(rect_bin, distance=boff_in, join=self.join, tolerance=self.tol)
        rect_in.simplify(self.tol)

        pstop = rect_out
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


    # ---------------------------------------------------------
    # MAIN GUARD RING (JTE)
    # ---------------------------------------------------------
    def DrawGR(self,
               layer=layerset['JTE'],
               layer_metal=layerset['METAL'],
               layer_oxide=layerset['OXIDE'],
               layer_ild=layerset['ILD']):
        
        bsize = self.dim_per.base_size
        bcenter = self.dim_per.base_center
        gap = self.dim_per.gr_gap
        width = self.dim_per.gr_width
        widthb = self.dim_per.gr_widthb
        center = self.dim_per.gr_center
        pad_offset = self.dim_per.pad_offset
        ild_offset = self.dim_per.ild_offset

        # inner boundary
        rect_base = pg.rectangle(size=bsize, layer=99)
        rect_pads = pg.offset(rect_base, distance=pad_offset,
                              join=self.join, tolerance=self.tol)
        rect_pads.center = bcenter
        rect_pads.simplify(self.tol)

        rect_in = pg.offset(rect_pads, distance=gap, join=self.join, tolerance=self.tol)
        rect_in.simplify(self.tol)

        # outer boundary
        rect_base1 = pg.rectangle(size=(bsize[0], bsize[1] + (widthb-width)), layer=99)
        rect_base1.center = center
        rect_out = pg.offset(rect_base1,
                             distance=pad_offset+width+gap,
                             join=self.join, tolerance=self.tol)
        rect_out.simplify(self.tol)

        # JTE ring
        gr = pg.boolean(rect_out, rect_in, operation='not', layer=layer)

        # -----------------------------------------------------
        # ADD ILD (±1 µm shrink) + metal (same width) 
        # -----------------------------------------------------
        # ILD
        rect_out_i = pg.offset(rect_out, distance=-ild_offset,
                               join=self.join, tolerance=self.tol)
        rect_in_i  = pg.offset(rect_in,  distance= ild_offset,
                               join=self.join, tolerance=self.tol)
        ild = pg.boolean(rect_out_i, rect_in_i, operation='not', layer=layer_ild)
        ild.simplify(self.tol)

        # metal (same width)
        metal = pg.boolean(rect_out, rect_in, operation='not', layer=layer_metal)
        metal.simplify(self.tol)

        # oxide opening
        rect_out_o = pg.offset(rect_out, distance=-5,
                               join=self.join, tolerance=self.tol)
        rect_in_o  = pg.offset(rect_in,  distance= 5,
                               join=self.join, tolerance=self.tol)
        oxide = pg.boolean(rect_out_o, rect_in_o, operation='not', layer=layer_oxide)
        oxide.simplify(self.tol)

        gr.add(ild)
        gr.add(metal)
        gr.add(oxide)

        self.d_gr = gr
        self.d_outmost = rect_out
        return gr


    # ---------------------------------------------------------
    # FLOATING GUARD RINGS
    # (ILD + metal ONLY, NO oxide)
    # ---------------------------------------------------------
    def DrawFGs(self, Nfg=2, layer=layerset['JTE']):
        d_fgs = Device('fgs')

        if Nfg == 0:
            self.d_fgs = d_fgs
            return d_fgs

        base = self.d_outmost
        gap = self.dim_per.fg_gap

        if not isinstance(gap, (list, tuple)):
            gap = [gap, gap]

        width = self.dim_per.fg_width
        ild_offset = self.dim_per.ild_offset
        center = self.dim_per.gr_center

        for i in range(Nfg):
            rect_in = pg.offset(base,
                                distance=gap[0] + (gap[1] + width)*i,
                                join=self.join, tolerance=self.tol)
            rect_out = pg.offset(base,
                                 distance=gap[0] + width + (gap[1] + width)*i,
                                 join=self.join, tolerance=self.tol)

            fg = pg.boolean(rect_out, rect_in, operation='not', layer=layer)
            fg.simplify(self.tol)

            # ILD (±1 µm)
            #rect_out_i = pg.offset(rect_out, distance=-ild_offset,
            #                       join=self.join, tolerance=self.tol)
            #rect_in_i  = pg.offset(rect_in,  distance= ild_offset,
            #                       join=self.join, tolerance=self.tol)
            #ild = pg.boolean(rect_out_i, rect_in_i, operation='not',
            #                 layer=self.layerset['ILD'])
            ild = pg.offset(fg, distance=-ild_offset, tolerance=self.tol, layer=self.layerset['ILD'])
            ild.simplify(self.tol)

            # metal (same width)
            metal = pg.boolean(rect_out, rect_in, operation='not',
                               layer=self.layerset['METAL'])
            metal.simplify(self.tol)

            # **FG에는 oxide 없음**
            fg.add(ild)
            fg.add(metal)

            d_fgs.add(fg)

        d_fgs.center = center
        d_fgs.simplify(self.tol)

        self.d_fgs = d_fgs
        self.d_outmost = rect_out
        return d_fgs


    # ---------------------------------------------------------
    # EDGE (unchanged)
    # ---------------------------------------------------------
    def DrawEdge(self, sensor_name=None, reticle_name=None,
                 reticle_name_blank=False, blank_size=None,
                 fontsize=60, layer=layerset['METAL'],
                 oxide_open=True, layer_oxide=layerset['OXIDE']):

        size = self.dim_per.edge_size
        center = self.dim_per.edge_center
        grcenter = self.dim_per.gr_center
        gap   = self.dim_per.edge_gap
        width = self.dim_per.edge_width
        bgap  = self.dim_per.edge_bgap

        rect_out = pg.rectangle(size, layer=99)
        rect_out.center = center

        rect_base = pg.offset(rect_out, distance=-bgap)
        rect_in = pg.offset(self.d_outmost, distance=gap,
                            join=self.join, tolerance=self.tol)
        rect_in.center = self.d_outmost.center

        edge = pg.boolean(rect_out, rect_in, operation='not', layer=layer)
        edge.center = center

        if sensor_name:
            sname = pg.text(text=sensor_name, size=fontsize,
                            justify='center', layer=layer)
            sname.center = (edge.x, edge.ymax - width/2)
            edge = pg.boolean(edge, sname, operation='not', layer=layer)

        if reticle_name:
            rname = pg.text(text=reticle_name, size=fontsize,
                            justify='center', layer=layer)
            rname.rotate(90)
            rname.center = (edge.xmin + width/2, edge.y)
            edge = pg.boolean(edge, rname, operation='not', layer=layer)

        if reticle_name_blank:
            if blank_size is None:
                blank_size = self.dim_per.blank_size
            rname_rect = pg.rectangle(size=blank_size, layer=layer)
            rname_rect.rotate(90)
            rname_rect.center = (edge.xmin + blank_size[1]/2, edge.y)
            edge = pg.boolean(edge, rname_rect, operation='not', layer=layer)

        if oxide_open:
            ox = Device('edge_oxide_open')
            size_o = (100, 100)
            o = pg.rectangle(size_o, layer=layer_oxide)

            ref1 = ox.add_ref(o); ref2 = ox.add_ref(o)
            ref3 = ox.add_ref(o); ref4 = ox.add_ref(o)

            ref1.center = (edge.xmin + 10 + size_o[0]/2, edge.ymin + 10 + size_o[1]/2)
            ref2.center = (edge.xmin + 10 + size_o[0]/2, edge.ymax - 10 - size_o[1]/2)
            ref3.center = (edge.xmax - 10 - size_o[0]/2, edge.ymax - 10 - size_o[1]/2)
            ref4.center = (edge.xmax - 10 - size_o[0]/2, edge.ymin + 10 + size_o[1]/2)

            edge.add(ox)

        edge.simplify(self.tol)
        self.d_edge = edge
        return edge


    # ---------------------------------------------------------
    # MAIN DRAW
    # ---------------------------------------------------------
    def Draw(self):
        d_per = Device('per')

        self.DrawPstop()
        self.DrawGR()
        self.DrawFGs(self.dim_per.Nfg)
        self.DrawEdge()

        d_per.add_ref(self.d_pstop)
        d_per.add_ref(self.d_gr)
        d_per.add_ref(self.d_fgs)
        d_per.add_ref(self.d_edge)

        self.d_per = d_per
        return d_per
