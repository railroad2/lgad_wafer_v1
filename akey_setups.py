
akey_setup_org = {
    'AKEY': {
        'ltext'   : ["AKEY", "AKEY", "AKEY", "AKEY", "AKEY", "AKEY", "AKEY"],
        'stext'   : ["JTE", "GAIN", "NPLU", "PSTO", "ILD", "META", "OXID"],
        'text'    : ["AK.JT", "AK.GA", "AK.NP", "AK.PS", "AK.IL", "AK.ME", "AK.OX"],
        'lcoords' : [(0, 0), (0, 2), (0, 4), (0, 6), (1, 0), (1, 4), (2, 2)],
        'scoords' : [(0, 1), (0, 3), (0, 5), (0, 7), (1, 1), (1, 5), (2, 3)],
        'xoffset' : 0
        },
    'JTE': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 0)],
        'scoords' : [(0, 1)],
        'xoffset' : 5
    },
    'GAIN': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 2)],
        'scoords' : [(0, 3)],
        'xoffset' : [5]
    },
    'NPLUS': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 4)],
        'scoords' : [(0, 5)],
        'xoffset' : [5]
    },
    'PSTOP': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 6)],
        'scoords' : [(0, 7)],
        'xoffset' : [5]
    },
    'ILD': {
        'ltext'   : [None, "ILD", "ILD"],
        'stext'   : [None, "META", "OXID"],
        'text'    : [None, "IL.ME", "IL.OX"],
        'lcoords' : [(1, 0), (1, 2), (2, 0)],
        'scoords' : [(1, 1), (1, 3), (2, 1)],
        'xoffset' : [5, 5, 0]
    },
    'METAL': {
        'ltext'    : [None, None, "META"],
        'stext'    : [None, None, "OXID"],
        'lcoords' : [(1, 2), (1, 4), (2, 4)],
        'scoords' : [(1, 3), (1, 5), (2, 5)],
        'npolar'  : -1,
        'xoffset' : [0, -5, -5]
    },
    'OXIDE': {
        'ltext'    : [None, None, None],
        'stext'    : [None, None, None],
        'lcoords' : [(2, 0), (2, 2), (2, 4)],
        'scoords' : [(2, 1), (2, 3), (2, 5)],
        'xoffset' : [0, 5, 5]
    },
}

akey_setup_1_pos = {
    'AKEY': {
        'ltext'   : ["AKEY", "AKEY", "AKEY", "AKEY", "AKEY", "AKEY", "AKEY"],
        'stext'   : ["JTE", "GAIN", "NPLU", "PSTO", "ILD", "META", "OXID"],
        'lcoords' : [(0, 0), (0, 2), (0, 4), (0, 6), (1, 0), (1, 4), (2, 2)],
        'scoords' : [(0, 1), (0, 3), (0, 5), (0, 7), (1, 1), (1, 5), (2, 3)],
        'lx_l'    : 150,
        'sx_l'    : 90,
        },
    'JTE': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 1)],
        'scoords' : [(0, 0)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'GAIN': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 3)],
        'scoords' : [(0, 2)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'NPLUS': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 5)],
        'scoords' : [(0, 4)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'PSTOP': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 7)],
        'scoords' : [(0, 6)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'ILD': {
        'ltext'   : [None, "ILD", "ILD"],
        'stext'   : [None, "META", "OXID"],
        'text'    : [None, "IL.ME", "IL.OX"],
        'lcoords' : [(1, 1), (1, 2), (2, 0)],
        'scoords' : [(1, 0), (1, 3), (2, 1)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'METAL': {
        'ltext'    : [None, None, "META"],
        'stext'    : [None, None, "OXID"],
        'lcoords' : [(1, 3), (1, 5), (2, 4)],
        'scoords' : [(1, 2), (1, 4), (2, 5)],
        'npolar'  : -1,
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'OXIDE': {
        'ltext'    : [None, None, None],
        'stext'    : [None, None, None],
        'lcoords' : [(2, 1), (2, 3), (2, 5)],
        'scoords' : [(2, 0), (2, 2), (2, 4)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
}

akey_setup_2_neg = {
    'AKEY': {
        'ltext'   : ["AKEY", "AKEY", "AKEY", "AKEY", "AKEY", "AKEY", "AKEY"],
        'stext'   : ["JTE", "GAIN", "NPLU", "PSTO", "ILD", "META", "OXID"],
        'text'    : ["AK.JT", "AK.GA", "AK.NP", "AK.PS", "AK.IL", "AK.ME", "AK.OX"],
        'lcoords' : [(0, 0), (0, 2), (0, 4), (0, 6), (1, 0), (1, 4), (2, 2)],
        'scoords' : [(0, 1), (0, 3), (0, 5), (0, 7), (1, 1), (1, 5), (2, 3)],
        'lpolar'  : 1,
        'spolar'  : 1,
        'lx_l'    : 150,
        'sx_l'    : 90,
        'xoffset' : 0
        },
    'JTE': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 1)],
        'scoords' : [(0, 0)],
        'lpolar'  : 1,
        'spolar'  : -1,
        'lx_l'    : 150,
        'sx_l'    : 90,
        'xoffset' : 0
    },
    'GAIN': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 3)],
        'scoords' : [(0, 2)],
        'lpolar'  : 1,
        'spolar'  : -1,
        'lx_l'    : 150,
        'sx_l'    : 90,
        'xoffset' : 0
    },
    'NPLUS': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 5)],
        'scoords' : [(0, 4)],
        'lpolar'  : 1,
        'spolar'  : -1,
        'lx_l'    : 150,
        'sx_l'    : 90,
        'xoffset' : 0
    },
    'PSTOP': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 7)],
        'scoords' : [(0, 6)],
        'lpolar'  : 1,
        'spolar'  : -1,
        'lx_l'    : 150,
        'sx_l'    : 90,
        'xoffset' : 0
    },
    'ILD': {
        'ltext'   : [None, "ILD", "ILD"],
        'stext'   : [None, "META", "OXID"],
        'text'    : [None, "IL.ME", "IL.OX"],
        'lcoords' : [(1, 1), (1, 2), (2, 0)],
        'scoords' : [(1, 0), (1, 3), (2, 1)],
        'lpolar'  : 1,
        'spolar'  : [-1, 1, 1],
        'lx_l'    : 150,
        'sx_l'    : 90,
        'xoffset' : 0
    },
    'METAL': {
        'ltext'    : [None, None, "META"],
        'stext'    : [None, None, "OXID"],
        'lcoords' : [(1, 3), (1, 5), (2, 4)],
        'scoords' : [(1, 2), (1, 4), (2, 5)],
        'lpolar'  : -1,
        'spolar'  : 1,
        'npolar'  : -1,
        'lx_l'    : 150,
        'sx_l'    : 90,
        'xoffset' : 0
    },
    'OXIDE': {
        'ltext'    : [None, None, None],
        'stext'    : [None, None, None],
        'lcoords' : [(2, 1), (2, 3), (2, 5)],
        'scoords' : [(2, 0), (2, 2), (2, 4)],
        'lpolar'  : 1,
        'spolar'  : -1,
        'lx_l'    : 150,
        'sx_l'    : 90,
        'xoffset' : 0
    },
}

akey_setup_3_double_pos = {
    'AKEY': {
        'ltext'   : ["AKEY", "AKEY", "AKEY", "AKEY", "AKEY", "AKEY", "AKEY"],
        'stext'   : ["JTE", "GAIN", "NPLU", "PSTO", "ILD", "META", "OXID"],
        'lcoords' : [(0, 0), (0, 2), (0, 4), (0, 6), (1, 0), (1, 4), (2, 2)],
        'scoords' : [(0, 1), (0, 3), (0, 5), (0, 7), (1, 1), (1, 5), (2, 3)],
        'lx_l'    : 150,
        'sx_l'    : 90,
        },
    'JTE': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 1)],
        'scoords' : [(0, 0)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'GAIN': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 3)],
        'scoords' : [(0, 2)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'NPLUS': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 5)],
        'scoords' : [(0, 4)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'PSTOP': {
        'ltext'   : [None],
        'stext'   : [None],
        'lcoords' : [(0, 7)],
        'scoords' : [(0, 6)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'ILD': {
        'ltext'   : [None, "ILD", "ILD"],
        'stext'   : [None, "META", "OXID"],
        'text'    : [None, "IL.ME", "IL.OX"],
        'lcoords' : [(1, 1), (1, 2), (2, 0)],
        'scoords' : [(1, 0), (1, 3), (2, 1)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'METAL': {
        'ltext'    : [None, None, "META"],
        'stext'    : [None, None, "OXID"],
        'lcoords' : [(1, 3), (1, 5), (2, 4)],
        'scoords' : [(1, 2), (1, 4), (2, 5)],
        'npolar'  : -1,
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
    'OXIDE': {
        'ltext'    : [None, None, None],
        'stext'    : [None, None, None],
        'lcoords' : [(2, 1), (2, 3), (2, 5)],
        'scoords' : [(2, 0), (2, 2), (2, 4)],
        'lx_l'    : 150,
        'sx_l'    : 90,
    },
}
