## all dimensions in micrometer (um)

class DimPad:
    gain_size    = (1000, 1000)
    gain_center  = (0, 0)

    nplus_sizeb  = (1100, 1100)
    nplus_center = (0, 0)

    jte_size     = nplus_sizeb
    jte_width    = 20
    jte_center   = (0, 0)

    pstop_gap_   = 20
    pstop_width  = 10
    pstop_center = (0, 0)

    padmetal_extend = 5
    #padmetal_size   = (1100, 1100)
    padmetal_center = (0, 0)

    padoxide_size   = (990, 990)
    padoxide_width  = 200
    padoxide_center = (0, 0)

    optwin_N = 3
    optwin_size = [(100, 100), 
                   (100, 100), 
                   (100, 100)]
    optwin_pos  = [(0, 0), 
                   (-400, 0), 
                   (400, 0)]

    #pad_size   = (jte_size[0]+jte_width, jte_size[1]+jte_width)
    #pad_size   = (jte_size[0]+jte_width+pstop_gap+pstop_width, jte_size[1]+jte_width+pstop_gap+pstop_width)
    pad_size   = (1300, 1300)
    pad_center = (0, 0)

    ild_offset = 1

    @property
    def pstop_gap(self):
        return 0.5 * (
            (self.pad_size[0] - self.jte_size[0]) / 2
            - (self.jte_width + self.pstop_width))
    @property
    def gr_gap(self):
        return self.pstop_gap

    @property
    def nplus_extend(self):
        return self.jte_width - 2

    @property
    def nplus_size(self):
        return (self.nplus_sizeb[0] + self.nplus_extend * 2, self.nplus_sizeb[1] + self.nplus_extend * 2)

    @property
    def padmetal_size(self):
        return (self.nplus_size[0] + self.padmetal_extend * 2, self.nplus_size[1] + self.padmetal_extend * 2)

