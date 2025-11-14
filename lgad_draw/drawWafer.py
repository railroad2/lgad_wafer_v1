import json

from phidl import geometry as pg
from phidl import Device

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

        d_reticles = Device('reticles')
        reticles = []
        for i in range(7):
            for j in range(7):
                if (i, j) in [(0, 0), (0, 6), (6, 0), (6, 6)]: 
                    continue

                rect1 = d_reticles.add_ref(rect)
                rect1.center = ((j-3) * (self.reticle_size[0] + 2*self.reticle_margin[0]),
                                (i-3) * (self.reticle_size[1] + 2*self.reticle_margin[1]))


        return d_reticles
        
    def PlaceReticles(self):
        d_reticle_A = pg.import_gds('template.gds')


        d_reticles = Device('reticles')
        reticles = []
        for i in range(7):
            for j in range(7):
                if (i, j) in [(0, 0), (0, 6), (6, 0), (6, 6)]: 
                    continue

                rect1 = d_reticles.add_ref(d_reticle_A)
                rect1.center = ((j-3) * (self.reticle_size[0] + 2*self.reticle_margin[0]),
                                (i-3) * (self.reticle_size[1] + 2*self.reticle_margin[1]))

        return d_reticles

    def DrawLayerNames(self):
        d_texts = Device('texts')

        for k, v in LAYERS.items():
            d_texts << pg.text(text=k, size=5000, layer=v)
            d_texts.distribute(elements='all'
                               direction='x',
                               spacing=2000,
                               separation=True)
        return d_texts

        


