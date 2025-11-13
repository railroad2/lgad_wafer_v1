from phidl import Device

import lgad_draw as lg

from . import layer_default 

class DrawSensor:

    def __new__(self, nx=1, ny=1, center=(0, 0),
                jte_width=20, 
                pstop_gap=10, pstop_width=10, 
                gr_gap=10, gr_width=(65, 105), 
                Nfg=0, fg_gap=(50, 10), fg_width=30,
                edge_gap=80, ild_offset=1,
                gain=True, nplus=True, jte=True, padild=True, padmetal=True, padoxide=True,
                pstop=True, guardring=True, edge=True, 
                rounding=True, tol=0.1, print_progress=False, 
                sensor_name=None, reticle_name=None, layers=None, rotation=0):

        if layers is None:
            LAYERS = layer_default.LAYERNUM
        else:
            LAYERS = layers

        # set dimensions for pad
        dim_pad = lg.DimPad()     
        dim_pad.jte_width = jte_width
        dim_pad.pstop_gap = pstop_gap
        dim_pad.pstop_width = pstop_width
        dim_pad.ild_offset = ild_offset

        # set dimensions for periphery
        dim_per = lg.DimPeriphery(nx, ny, dim_pad)
        dim_per.gr_gap = gr_gap
        dim_per.ild_offset = ild_offset

        if isinstance(gr_width, (list, tuple)):
            dim_per.gr_width, dim_per.gr_widthb = gr_width
        elif isinstance(gr_width, (int, float)):
            dim_per.gr_width = dim_per.gr_widthb = gr_width

        dim_per.Nfg = Nfg
        dim_per.fg_gap = fg_gap
        dim_per.edge_gap = edge_gap

        # finally calculate all the dimensions
        dim_per.set_dims(dim_pad)

        draw_pad = lg.DrawPad(dim_pad)
        draw_per = lg.DrawPeriphery(dim_per)

        draw_pad.tol = tol
        draw_per.tol = tol

        if rounding:
            draw_pad.join = draw_per.join = 'round'
        else:
            draw_pad.join = draw_per.join = 'miter'

        if print_progress: print ('Drawing start')

        sensor = Device(f'sensor_{nx}x{ny}')
        pad0   = Device('pad0')
        per0   = Device('per0')

        if guardring:
            d_gr    = draw_per.DrawGR(layer=LAYERS['GR'], 
                                      layer_metal=LAYERS['METAL'], 
                                      layer_oxide=LAYERS['OXIDE'])
            per0.add(d_gr) 
            if print_progress: print ('Guard-ring is drawn.')
        if Nfg:
            d_fgs   = draw_per.DrawFGs(Nfg, layer=LAYERS['FGR'])
            per0.add(d_fgs) 
            if print_progress: print ('Floating guard-ring is drawn.')
        if edge:
            d_edge  = draw_per.DrawEdge(sensor_name=sensor_name, 
                                        reticle_name=reticle_name,
                                        layer=LAYERS['METAL'],
                                        layer_oxide=LAYERS['OXIDE'])
            per0.add(d_edge) 
            if print_progress: print ('Edge is drawn.')

        if gain: 
            d_gain  = draw_pad.DrawGain(layer=LAYERS['GAIN'])
            pad0.add(d_gain) 
            if print_progress: print ('gain is drawn.')
        if nplus:
            d_nplus = draw_pad.DrawNplus(layer=LAYERS['NPLUS'])
            pad0.add(d_nplus) 
            if print_progress: print ('nplus is drawn.')
        if jte:
            d_jte   = draw_pad.DrawJTE(layer=LAYERS['JTE'])
            pad0.add(d_jte) 
            if print_progress: print ('jte is drawn.')
        if pstop:
            d_pstop1 = draw_pad.DrawPstop(layer=LAYERS['PSTOP'])
            pad0.add(d_pstop1)
            if print_progress: print ('pstop is drawn')

        if padild:
            d_padild = draw_pad.DrawPadILD(layer=LAYERS['ILD'])
            pad0.add(d_padild) 
            if print_progress: print ('pad ild is drawn.')

        if padmetal:
            d_padme = draw_pad.DrawPadMetal(layer=LAYERS['METAL'])
            pad0.add(d_padme) 
            if print_progress: print ('pad metal is drawn.')

        if padoxide:
            d_padox = draw_pad.DrawPadOxide(layer=LAYERS['OXIDE'])
            pad0.add(d_padox) 
            if print_progress: print ('pad oxide is drawn.')

        k = 0
        for i in range(ny):
            for j in range(nx):
                ref = sensor.add_ref(pad0)
                ref.move(dim_per.c_pads[k])
                if print_progress: print (f'Pad {i}, {j} is drawn.')
                k += 1

        per0.center = sensor.center
        sensor << per0
        
        sensor.center = center
        if rotation:
            sensor.rotate(rotation)

        return sensor


