
## all dimensions in micrometer (um)

class DimPad:
    gain_size   = (1000, 1000)
    gain_center = (0, 0)

    nplus_size   = (1100, 1100)
    nplus_center = (0, 0)

    jte_size   = nplus_size
    jte_width  = 20
    jte_center = (0, 0)

    pstop_gap   = 20
    pstop_width = 10
    pstop_center = (0, 0)

    padmetal_size   = (1100, 1100)
    padmetal_center = (0, 0)

    padoxide_size   = (990, 990)
    padoxide_width  = 200
    padoxide_center = (0, 0)

    optwin_N = 3
    optwin_size = [(100, 100), 
                   (100, 100), 
                   (100, 100)]
    optwin_pos  = [(0, 0), 
                   (-450, 0), 
                   (450, 0)]

    #pad_size   = (jte_size[0]+jte_width, jte_size[1]+jte_width)
    pad_size   = (jte_size[0]+jte_width+pstop_gap+pstop_width, jte_size[1]+jte_width+pstop_gap+pstop_width)
    pad_center = (0, 0)

    ild_offset = 1
