import numpy as np

class DimPeriphery:
    # pad center offset
    pad_off_x = 1280
    pad_off_y = 1280

    # single pad edge size
    pad_edge_x = 2100 
    pad_edge_y = 2100 

    # guard-ring
    gr_gap    = 50
    gr_width  = 65
    gr_widthb = 105
    gr_offset = gr_gap + gr_width/2
    gr_size = (0, 0)
    gr_boff = 0
    gr_size_in = (0, 0)
    gr_boff_in = 0

    # floating guard-ring
    fg_gap = 30
    fg_width = 20
    Nfg = 2

    # edge
    edge_size = (0, 0)
    edge_width = 150
    edge_center = (0, 0)
    edge_gap = 60

    def __init__(self, nx=1, ny=1, dim_pads=[], c_pads=[]):
        self.nx = nx
        self.ny = ny

        self.c_pads = c_pads
        self.dim_pads = dim_pads
        self.set_dims(dim_pads)

    # set dimension based on the first pad 
    def set_dims(self, dim_pads=[]): 
        if not isinstance(dim_pads, list):
            dim_pads = [dim_pads]

        self.dim_pads = dim_pads
        pad_size = dim_pads[0].pad_size
        self.pad_offset = self.dim_pads[0].jte_width + self.dim_pads[0].pstop_width + self.dim_pads[0].pstop_gap

        #if self.c_pads == []:
        self.c_pads = []
        for i in range(self.ny):
            for j in range(self.nx):
                c_pad_x =  j * self.pad_off_x
                c_pad_y = -i * self.pad_off_y
                self.c_pads.append( (c_pad_x, c_pad_y) )

        c_pads = np.array(self.c_pads)

        # gr
        self.base_size = (np.max(c_pads[:, 0]) - np.min(c_pads[:, 0]) + dim_pads[0].nplus_size[0],
                          np.max(c_pads[:, 1]) - np.min(c_pads[:, 1]) + dim_pads[0].nplus_size[1])

        self.base_center = (np.average(c_pads[:, 0]), np.average(c_pads[:, 1]))

        self.gr_center = (self.base_center[0], 
                          self.base_center[1] - (self.gr_widthb - self.gr_width)/2)

        # edge
        self.edge_size = (self.pad_off_x*self.nx + (self.pad_edge_x - self.pad_off_x), 
                          self.pad_off_y*self.ny + (self.pad_edge_y - self.pad_off_y))
        self.edge_center = self.base_center
        self.edge_bgap   = (self.edge_size[0] - dim_pads[0].nplus_size[0]*self.nx-180*(self.nx-1))/2

        self.sensor_name = f'KNU LGAD v1-{self.nx}x{self.ny}-{self.Nfg}-{dim_pads[0].jte_width}-{dim_pads[0].pstop_width}'

