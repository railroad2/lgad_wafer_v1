from phidl import Device, Layer
import phidl.geometry as pg
import pylab as plt


yo = yoffset = 3000
positions = [ (0, yo), (600, yo), (1200, yo), (1800, yo), (2400, yo),
              (0, 0), (600, 0), (1200, 0), (1800, 0), (2400, 0), ]
textoffset =100

def innercal(layer, name, invert=False):
    d_cal = Device('cal')
    d_calh = Device('hcal')
    d_calv = Device('vcal')
    cal = pg.litho_calipers(notch_size = [10, 30], 
                            notch_spacing=10, 
                            num_notches = 11,
                            offset_per_notch = 0.2,
                            row_spacing = 0,
                            layer1 = layer, 
                            layer2 = 99)

    box = pg.rectangle(size=(600, 700), layer=81)
    box.center = (0, 0)
    pin = pg.rectangle(size=(10, 10), layer=99)

    r_hor = d_calh.add_ref(cal)
    r_hor.center = (0, 0)
    r_pinh1 = d_calh.add_ref(pin)
    r_pinh2 = d_calh.add_ref(pin)
    r_pinh3 = d_calh.add_ref(pin)
    r_pinh4 = d_calh.add_ref(pin)
    r_pinh1.center = (-198, -35)
    r_pinh2.center = ( -99, -35)
    r_pinh3.center = (  99, -35)
    r_pinh4.center = ( 198, -35)
    
    r_ver = d_calv.add_ref(cal)
    r_ver.center = (0, 0)
    r_ver.rotate(90)
    r_pinv1 = d_calv.add_ref(pin)
    r_pinv2 = d_calv.add_ref(pin)
    r_pinv3 = d_calv.add_ref(pin)
    r_pinv4 = d_calv.add_ref(pin)
    r_pinv1.center = (35, -198)
    r_pinv2.center = (35, -99)
    r_pinv3.center = (35, 99)
    r_pinv4.center = (35, 198)

    r_calh = d_cal.add_ref(d_calh)
    r_calv = d_cal.add_ref(d_calv)
    
    r_calv.xmax = r_calh.xmax + 30
    r_calv.ymin = r_calh.ymax 

    r_text1h = d_cal.add_ref(pg.text(text=name, size=50, layer=layer))
    r_text1v = d_cal.add_ref(pg.text(text=name, size=50, layer=layer))
    r_text1v.rotate(90)
    r_text1h.center = (r_calh.center[0], r_calh.center[1]+textoffset)
    r_text1v.center = (r_calv.center[0]-textoffset, r_calv.center[1])
    r_text2h = d_cal.add_ref(pg.text(text='DUMMY', size=50, layer=99))
    r_text2v = d_cal.add_ref(pg.text(text='DUMMY', size=50, layer=99))
    r_text2v.rotate(90)
    r_text2h.center = (r_calh.center[0], r_calh.center[1]-textoffset)
    r_text2v.center = (r_calv.center[0]+textoffset, r_calv.center[1])
    
    d_cal.center = (0, 0)
    d_clean = pg.extract(d_cal, layers=[layer])
    
    if invert:
        d_clean = pg.boolean(box, d_clean, operation='not', layer=layer)
    d_clean.add_ref(box)

    return d_clean

def outercal(layer, name, invert=False):
    d_cal = Device('cal')
    d_calh = Device('hcal')
    d_calv = Device('vcal')
    cal = pg.litho_calipers(notch_size = [10, 30], 
                            notch_spacing = 10, 
                            num_notches = 11,
                            offset_per_notch = 0.2,
                            row_spacing = 0,
                            layer1 = 99, 
                            layer2 = layer)

    box = pg.rectangle(size=(600, 700), layer=81)
    box.center = (0, 0)
    pin = pg.rectangle(size=(10, 10), layer=layer)

    r_hor = d_calh.add_ref(cal)
    r_hor.center = (0, 0)
    r_pinh1 = d_calh.add_ref(pin)
    r_pinh2 = d_calh.add_ref(pin)
    r_pinh3 = d_calh.add_ref(pin)
    r_pinh4 = d_calh.add_ref(pin)
    r_pinh1.center = (-198, -35)
    r_pinh2.center = ( -99, -35)
    r_pinh3.center = (  99, -35)
    r_pinh4.center = ( 198, -35)
    
    r_ver = d_calv.add_ref(cal)
    r_ver.center = (0, 0)
    r_ver.rotate(90)
    r_pinv1 = d_calv.add_ref(pin)
    r_pinv2 = d_calv.add_ref(pin)
    r_pinv3 = d_calv.add_ref(pin)
    r_pinv4 = d_calv.add_ref(pin)
    r_pinv1.center = (35, -198)
    r_pinv2.center = (35, -99)
    r_pinv3.center = (35, 99)
    r_pinv4.center = (35, 198)

    r_calh = d_cal.add_ref(d_calh)
    r_calv = d_cal.add_ref(d_calv)

    r_calv.xmax = r_calh.xmax + 30
    r_calv.ymin = r_calh.ymax 

    r_text1h = d_cal.add_ref(pg.text(text='DUMMY', size=50, layer=99))
    r_text1v = d_cal.add_ref(pg.text(text='DUMMY', size=50, layer=99))
    r_text1v.rotate(90)
    r_text1h.center = (r_calh.center[0], r_calh.center[1]+textoffset)
    r_text1v.center = (r_calv.center[0]-textoffset, r_calv.center[1])
    r_text2h = d_cal.add_ref(pg.text(text=name, size=50, layer=layer))
    r_text2v = d_cal.add_ref(pg.text(text=name, size=50, layer=layer))
    r_text2v.rotate(90)
    r_text2h.center = (r_calh.center[0], r_calh.center[1]-textoffset)
    r_text2v.center = (r_calv.center[0]+textoffset, r_calv.center[1])

    d_cal.center = (0, 0)
    d_clean = pg.extract(d_cal, layers=[layer])
    if invert:
        d_clean = pg.boolean(box, d_clean, operation='not', layer=layer)
    
    d_clean.add_ref(box)
    return d_clean


def place(layer, name, poslst, inout, invert=False):
    if inout=='in':
        fnc = innercal
    elif inout=='out':
        fnc = outercal

    D = Device('cal')
    for pos in poslst:
        r_1 = D.add_ref(fnc(layer, name, invert=invert))
        r_1.center = positions[pos]

    return D


def draw_all():
    pos_akey_in = [0, 1, 2, 3, 4, 6, 8]
    pos_jte_out = [0]
    pos_gain_out = [1]
    pos_nplus_out = [2]
    pos_pstop_out = [3]
    pos_ild_out = [4]
    pos_ild_in = [5, 7]
    pos_metal_out = [5, 6]
    pos_metal_in = [9]
    pos_oxide_out = [7, 8, 9]

    D = Device('cal')

    D.add_ref(place(1, 'AKEY', pos_akey_in, 'in', invert=False))
    D.add_ref(place(2, 'JTE', pos_jte_out, 'out', invert=True))
    D.add_ref(place(3, 'GAIN', pos_gain_out, 'out', invert=True))
    D.add_ref(place(4, 'NPLUS', pos_nplus_out, 'out', invert=True))
    D.add_ref(place(5, 'PSTOP', pos_pstop_out, 'out', invert=True))
    D.add_ref(place(6, 'ILD', pos_ild_out, 'out', invert=True))
    D.add_ref(place(6, 'ILD', pos_ild_in, 'in', invert=False))
    D.add_ref(place(7, 'METAL', pos_metal_out, 'out'))
    D.add_ref(place(7, 'METAL', pos_metal_in, 'in'))
    D.add_ref(place(8, 'OXIDE', pos_oxide_out, 'out', invert=True))

    
    D.write_gds('vernier.gds')

draw_all()
#qp(D) # quickplot the geometry

