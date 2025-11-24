import numpy as np
import pylab as plt

import phidl.geometry as pg
from phidl import Device
from phidl import quickplot as qp
from phidl import routing as pr

import layer_default 

layerset = layer_default.layerset

def draw_X_test(doping_layer, doping_name, width=100, metal_layer=7, oxide_layer=8, ild_layer=6, contact_layer=0):
    D = Device('X_test')
    d_tilt  = Device('X_tilt')
    d_long  = Device('X_long')
    d_short = Device('X_short')
    d_left  = Device('X_left')

    # tilt
    tpad = pg.rectangle(size=(400, width), layer=doping_layer)
    tpad.center = (0, 0)
    d_tilt.add_ref(tpad)

    tline1 = pg.rectangle(size=(30, 220), layer=metal_layer)
    tline1.xmin = tpad.xmin
    tline1.ymax = tpad.ymax
    r_tline1 = d_tilt.add_ref(tline1)

    tline2 = pg.rectangle(size=(30, 180), layer=metal_layer)
    tline2.xmax = tpad.xmax
    tline2.ymax = tpad.ymax
    r_tline2 = d_tilt.add_ref(tline2)

    rect1 = pg.boolean(tpad, tline1, operation='and', layer=contact_layer)
    ild1 = pg.offset(rect1, distance = -5, layer=ild_layer)
    rect2 = pg.boolean(tpad, tline2, operation='and', layer=contact_layer)
    ild2 = pg.offset(rect2, distance = -5, layer=ild_layer)

    r_ild1 = d_tilt.add_ref(ild1)
    r_ild2 = d_tilt.add_ref(ild2)

    if (contact_layer):
        d_tilt.add_ref(rect1)
        d_tilt.add_ref(rect2)
    
    r_tilt = d_left.add_ref(d_tilt)
    r_tilt.rotate(-45)

    mrot = np.array([[np.cos(np.radians(-45)), -np.sin(np.radians(-45))], 
                     [np.sin(np.radians(-45)),  np.cos(np.radians(-45))]])

    tip1 = np.array((r_tline1.xmin, r_tline1.ymin))
    tip2 = np.array((r_tline2.xmin, r_tline2.ymin))
    tip1 = np.matmul(mrot, tip1)
    tip2 = np.matmul(mrot, tip2)

    # long
    lpad  = pg.rectangle(size=(90, 135), layer=metal_layer)
    lline = pg.rectangle(size=(40, 250), layer=metal_layer)

    r_lline = d_long.add_ref(lline)
    r_lpad  = d_long.add_ref(lpad)
    r_lline.xmin = tip1[0]
    r_lline.ymax = tip1[1]

    # short
    sep = tip1[1] - tip2[1]
    sline = pg.rectangle(size=(40, 250 - sep), layer=metal_layer)

    r_sline = d_long.add_ref(sline)
    r_spad  = d_long.add_ref(lpad)
    r_sline.xmin = tip2[0]
    r_sline.ymax = tip2[1]

    # adjust
    r_lpad.xmin = r_lline.xmin
    r_lpad.ymax = r_lline.ymin
    r_spad.xmin = r_sline.xmin
    r_spad.ymax = r_sline.ymin

    r_loxide = d_long.add_ref(pg.offset(r_lpad, distance=-5, layer=oxide_layer))
    r_soxide = d_long.add_ref(pg.offset(r_spad, distance=-5, layer=oxide_layer))
    
    # all
    r_long  = d_left.add_ref(d_long)
    r_short = d_left.add_ref(d_short)

    d_right = pg.copy(d_left)
    d_right.mirror(p1=(0, 0), p2 = (0, 1))

    d_text = pg.text(text=doping_name, size=80, layer=metal_layer)
    d_text1 = pg.text(text=f"L400 W{width}", size=60, layer=metal_layer)
    d_text.center = (0, 360)
    d_text1.center = (0, 260)

    d_text3 = Device('pad_label')
    r_v1 = d_text3.add_ref(pg.text(text="V1", size=50, layer=metal_layer))
    r_v2 = d_text3.add_ref(pg.text(text="V2", size=50, layer=metal_layer))
    r_h1 = d_text3.add_ref(pg.text(text="H1", size=50, layer=metal_layer))
    r_h2 = d_text3.add_ref(pg.text(text="H2", size=50, layer=metal_layer))

    r_v1.center = (r_lpad.center[0], r_lpad.ymin-50)
    r_v2.center = (r_spad.center[0], r_lpad.ymin-50)
    r_h1.center = (-r_spad.center[0], r_lpad.ymin-50)
    r_h2.center = (-r_lpad.center[0], r_lpad.ymin-50)

    D << d_left
    D << d_right
    D << d_text
    D << d_text1
    D << d_text3

    return D


def draw_I_test(doping_layer, doping_name, width=10, metal_layer=7, oxide_layer=8, ild_layer=6, contact_layer=0):
    D = Device('I_test')
    
    metal_left = Device('metal_left')
    pad_v = Device('pad_v')
    pad_i = Device('pad_i')

    length = 400
    doping = pg.rectangle(size=(length + 50*2, width), layer=doping_layer)
    doping.center = (0, 0)

    pad  = pg.rectangle(size=(90, 135), layer=metal_layer)
    pad.add_ref(pg.offset(pad, distance=-5, layer=oxide_layer))
    contact1 = pg.rectangle(size=(20, 24), layer=metal_layer)
    contact2 = pg.rectangle(size=(14, 24), layer=metal_layer)
    line1 = pg.rectangle(size=(20, 50), layer=metal_layer)

    r_pad1 = pad_v.add_ref(pad)
    r_line1 = pad_v.add_ref(line1)  
    r_contact1 = pad_v.add_ref(contact1)

    r_contact1.xmin = doping.xmin
    r_contact1.ymax = doping.ymax+2
    r_line1.xmin = r_contact1.xmin
    r_line1.ymax = r_contact1.ymin
    r_pad1.xmin = r_line1.xmin
    r_pad1.ymax = r_line1.ymin

    d_pad2 = pad_i.add_ref(pad)
    r_contact2 = pad_i.add_ref(contact2)

    r_contact2.xmax = -length/2 + 2
    r_contact2.ymax = doping.ymax + 2
    d_pad2.xmin = doping.xmin + 90 + 40
    d_pad2.ymax = r_pad1.ymax

    port1 = pad_i.add_port(name='p1', midpoint = (r_contact2.x, r_contact2.ymin), width=5, orientation=270)
    port2 = pad_i.add_port(name='p2', midpoint = (d_pad2.xmin+10, d_pad2.ymax),   width=5, orientation=90)
    r_route = pad_i.add_ref(pr.route_smooth(port1, port2, width=(r_contact2.xsize, 20), radius=23, layer=metal_layer))

    rect1 = pg.boolean(doping, r_contact1, operation='and', layer=contact_layer)
    ild1 = pg.rectangle(size=(rect1.xsize-4, rect1.ysize), layer=ild_layer)
    ild1.center = rect1.center
    rect2 = pg.boolean(doping, r_contact2, operation='and', layer=contact_layer)
    ild2 = pg.rectangle(size=(rect2.xsize-4, rect2.ysize), layer=ild_layer)
    ild2.center = rect2.center

    pad_v.add_ref(ild1)
    pad_i.add_ref(ild2)

    pstop1 = pg.rectangle(size=r_contact1.size, layer=contact_layer)
    pstop2 = pg.rectangle(size=r_contact2.size, layer=contact_layer)
    pstop1.center = r_contact1.center
    pstop2.center = r_contact2.center

    if (contact_layer):
        metal_left.add_ref(pstop1)
        metal_left.add_ref(pstop2)

    metal_left.add_ref(pad_v)
    metal_left.add_ref(pad_i)
    metal_right = pg.copy(metal_left)
    metal_right.mirror(p1=(0, 0), p2 = (0, 1))

    d_text = pg.text(text=doping_name, size=80, layer=metal_layer)
    d_text1 = pg.text(text=f"L400 W{width}", size=60, layer=metal_layer)
    d_text.center = (0, 200)
    d_text1.center = (0, 100)

    d_text3 = Device('pad_label')
    r_v1 = d_text3.add_ref(pg.text(text="V1", size=50, layer=metal_layer))
    r_v2 = d_text3.add_ref(pg.text(text="V2", size=50, layer=metal_layer))
    r_i1 = d_text3.add_ref(pg.text(text="I1", size=50, layer=metal_layer))
    r_i2 = d_text3.add_ref(pg.text(text="I2", size=50, layer=metal_layer))

    r_v1.center = (pad_v.center[0], pad_v.ymin-50)
    r_i1.center = (pad_v.center[0]+130, pad_v.ymin-50)
    r_v2.center = (-pad_v.center[0], pad_i.ymin-50)
    r_i2.center = (-pad_v.center[0]-130, pad_i.ymin-50)

    D << metal_left
    D << metal_right
    D << doping
    D << d_text
    D << d_text1
    D << d_text3


    return D


def draw_C_pad(area=2, gain_layer=3, nplus_layer=4, metal_layer=7, oxide_layer=8, ild_layer=6): # area in mm^2
    area_um2 = area * 1e6
    radius = np.sqrt(area_um2 / np.pi)
    D = Device('c-pad')

    ell_gain  = D.add_ref(pg.ellipse(radii=(radius, radius), angle_resolution=1, layer=gain_layer))
    ell_nplus = D.add_ref(pg.ellipse(radii=(radius, radius), angle_resolution=1, layer=nplus_layer))
    ell_metal = D.add_ref(pg.ellipse(radii=(radius, radius), angle_resolution=1, layer=metal_layer))
    ell_oxide = D.add_ref(pg.ellipse(radii=(radius-10, radius-10), angle_resolution=1, layer=oxide_layer))

    ell_gain.center  = (0, 0)
    ell_nplus.center = (0, 0)
    ell_metal.center = (0, 0)
    ell_oxide.center = (0, 0)

    if ild_layer:
        ell_ild   = D.add_ref(pg.ellipse(radii=(radius-5, radius-5), angle_resolution=1, layer=ild_layer))
        ell_ild.center   = (0, 0)

    return D
    

def draw_C_pad_small(doping_layer, doping_name, diameter=400, metal_layer=7, oxide_layer=8, ild_layer=6): # area in mm^2
    radius = diameter/2
    D = Device('c-pad_small')

    if doping_layer:
        ell_dop = D.add_ref(pg.ellipse(radii=(radius, radius), angle_resolution=1, layer=doping_layer))
        ell_dop.center = (0, 0)

    ell_metal = D.add_ref(pg.ellipse(radii=(radius, radius), angle_resolution=1, layer=metal_layer))
    ell_oxide = D.add_ref(pg.ellipse(radii=(radius-5, radius-5), angle_resolution=1, layer=oxide_layer))

    ell_metal.center = (0, 0)
    ell_oxide.center = (0, 0)

    text = D.add_ref(pg.text(text=doping_name, size=80, layer=metal_layer))
    text1 = D.add_ref(pg.text(text=f"D={diameter}", size=60, layer=metal_layer))
    text.center = (0, radius+200)
    text1.center = (0, radius+100)

    return D


def DrawTest_org():
    D = Device('xtest')
    d_vdp = Device('vdp')
    d_res = Device('resitivity')
    d_cap = Device('moscap')

    d_cap1 = Device('big moscap1')
    d_cap2 = Device('big moscap2')

    d_ret1 = Device('ret1')
    d_ret2 = Device('ret2')
    d_ret3 = Device('ret3')

    separation = 650

    r_X_nplus  = d_vdp.add_ref(draw_X_test(layerset['NPLUS'], 'NPLUS'))
    r_X_gain   = d_vdp.add_ref(draw_X_test(layerset['GAIN'], 'GAIN', contact_layer=0))
    r_X_gain_p = d_vdp.add_ref(draw_X_test(layerset['GAIN'], 'GAIN+PSTOP', contact_layer=5))
    r_X_jte    = d_vdp.add_ref(draw_X_test(layerset['JTE'], 'JTE'))
    r_X_pstop  = d_vdp.add_ref(draw_X_test(layerset['PSTOP'], 'PSTOP'))

    r_X_jte.center    = (separation*0, 0)
    r_X_gain.center   = (separation*1, 0)
    r_X_gain_p.center = (separation*2.5, 0)
    r_X_nplus.center  = (separation*3.5, 0)
    r_X_pstop.center  = (separation*4.5, 0)

    r_I_jte10    = d_res.add_ref(draw_I_test(layerset['JTE'], 'JTE', width=10))
    r_I_jte20    = d_res.add_ref(draw_I_test(layerset['JTE'], 'JTE', width=20))
    r_I_gain10   = d_res.add_ref(draw_I_test(layerset['GAIN'], 'GAIN', width=10, contact_layer=0))
    r_I_gain20   = d_res.add_ref(draw_I_test(layerset['GAIN'], 'GAIN', width=20, contact_layer=0))
    r_I_gain10_p = d_res.add_ref(draw_I_test(layerset['GAIN'], 'GAIN+PSTOP', width=10, contact_layer=5))
    r_I_gain20_p = d_res.add_ref(draw_I_test(layerset['GAIN'], 'GAIN+PSTOP', width=20, contact_layer=5))
    r_I_nplus10  = d_res.add_ref(draw_I_test(layerset['NPLUS'], 'NPLUS', width=10))
    r_I_nplus20  = d_res.add_ref(draw_I_test(layerset['NPLUS'], 'NPLUS', width=20))
    r_I_pstop10  = d_res.add_ref(draw_I_test(layerset['PSTOP'], 'PSTOP', width=10))
    r_I_pstop20  = d_res.add_ref(draw_I_test(layerset['PSTOP'], 'PSTOP', width=20))

    r_I_jte10.center    = (separation*0, 0)
    r_I_jte20.center    = (separation*0, r_I_jte10.ymin-r_I_jte20.ysize/2-200)
    r_I_gain10.center   = (separation*1, 0)
    r_I_gain20.center   = (separation*1, r_I_jte20.y)
    r_I_gain10_p.center = (separation*2.5, 0)
    r_I_gain20_p.center = (separation*2.5, r_I_jte20.y)
    r_I_nplus10.center  = (separation*3.5, 0)
    r_I_nplus20.center  = (separation*3.5, r_I_jte20.y)
    r_I_pstop10.center  = (separation*4.5, 0)
    r_I_pstop20.center  = (separation*4.5, r_I_jte20.y)

    diameter = 400
    r_C_jte   = d_cap.add_ref(draw_C_pad_small(layerset['JTE'], 'JTE', diameter))
    r_C_gain  = d_cap.add_ref(draw_C_pad_small(layerset['GAIN'], 'GAIN', diameter))
    r_C_none  = d_cap.add_ref(draw_C_pad_small(None, 'NONE', diameter))
    r_C_nplus = d_cap.add_ref(draw_C_pad_small(layerset['NPLUS'], 'NPLUS', diameter))
    r_C_pstop = d_cap.add_ref(draw_C_pad_small(layerset['PSTOP'], 'PSTOP', diameter))

    r_C_jte.center   = (separation*0, 0)
    r_C_gain.center  = (separation*1, 0)
    r_C_none.center  = (separation*2.5, 0)
    r_C_nplus.center = (separation*3.5, 0)
    r_C_pstop.center = (separation*4.5, 0)

    
    label1 = d_vdp.add_ref(pg.text(text='Van der Pauw', layer=layerset['METAL'], size=100))
    label1.rotate(90)
    label1.center = (separation*-1, 0)

    label2 = d_res.add_ref(pg.text(text='Resistivity', layer=layerset['METAL'], size=100))
    label2.rotate(90)
    label2.center = (separation*-1, (r_I_jte10.center[1] + r_I_jte20.center[1])*0.5)

    label3 = d_cap.add_ref(pg.text(text='MOSCAP', layer=layerset['METAL'], size=100))
    label3.rotate(90)
    label3.center = (separation*-1, 0)


    # reticle 1 : VdP + MOSCAP
    r_vdp = d_ret1.add_ref(d_vdp)
    r_cap = d_ret1.add_ref(d_cap)
    r_cap.ymax = r_vdp.ymin - 100
    d_ret1.center = (0, 0)

    bound = pg.rectangle(size=(4300, 2100), layer=layerset['AUX'])
    bound = pg.offset(bound, distance=-100)
    bound = pg.outline(bound, distance=100, layer=layerset['AUX'])
    r_bound1 = d_ret1.add_ref(bound)
    r_bound1.center = (0, 0)

    # reticle 2 : resistivity
    r_res = d_ret2.add_ref(d_res) 
    d_ret2.center = (0, 0)
    r_bound2 = d_ret2.add_ref(bound)
    r_bound2.center = (0, 0)

    # reticle 3 : big MOSCAP
    r_circle1 = d_cap1.add_ref(draw_C_pad())
    r_circle1.center = (0, 0)

    label4_1 = d_cap1.add_ref(pg.text(text='MOSCAP (NPLUS+GAIN+ILD)', layer=layerset['METAL'], size=100))
    label4_2 = d_cap1.add_ref(pg.text(text='AREA = 2 mm', layer=layerset['METAL'], size=100))
    label4_3 = d_cap1.add_ref(pg.text(text='2', layer=layerset['METAL'], size=50))
    #label4_1.rotate(90)
    label4_2.rotate(90)
    label4_3.rotate(90)
    label4_1.center = (0, r_circle1.ymax + 200) #(r_circle1.xmin-separation*0.7, 0)
    label4_2.center = (r_circle1.xmin-200, 0)
    label4_3.ymin = label4_2.ymax+10
    label4_3.xmin = label4_2.x-50

    r_circle2 = d_cap2.add_ref(draw_C_pad(ild_layer=None))
    r_circle2.center = (0, 0)

    label5_1 = d_cap2.add_ref(pg.text(text='MOSCAP (NPLUS+GAIN)', layer=layerset['METAL'], size=100))
    label5_2 = d_cap2.add_ref(pg.text(text='AREA = 2 mm', layer=layerset['METAL'], size=100))
    label5_3 = d_cap2.add_ref(pg.text(text='2', layer=layerset['METAL'], size=50))
    #label5_1.rotate(90)
    label5_2.rotate(90)
    label5_3.rotate(90)
    label5_1.center = (0, r_circle2.ymax + 200) #(r_circle1.xmin-separation*0.7, 0)
    label5_2.center = (r_circle2.xmin-200, 0)
    label5_3.ymin = label5_2.ymax+10
    label5_3.xmin = label5_2.x-50

    r_cap1 = d_ret3.add_ref(d_cap1)
    r_cap2 = d_ret3.add_ref(d_cap2)
    r_cap2.xmin = r_cap1.xmax + 200
    d_ret3.center = (0, 0)
    r_bound3 = d_ret3.add_ref(bound)
    r_bound3.center = (0, 0)

    r_ret1 = D.add_ref(d_ret1)
    r_ret2 = D.add_ref(d_ret2)
    r_ret3 = D.add_ref(d_ret3)

    r_ret2.ymax = r_ret1.ymin - 100
    r_ret3.ymax = r_ret2.ymin - 100

    return D


def DrawTest():
    D = Device('xtest')
    d_vdp = Device('vdp')
    d_res = Device('resitivity')
    d_cap = Device('moscap')

    d_cap1 = Device('big moscap1')
    d_cap2 = Device('big moscap2')

    d_ret1_1 = Device('test_ret1_1')
    d_ret1_2 = Device('test_ret1_2')
    d_ret2_1 = Device('test_ret2_1')
    d_ret2_2 = Device('test_ret2_2')
    d_ret3_1 = Device('test_ret3_1')
    d_ret3_2 = Device('test_ret3_2')

    separation = 650

    diameter = 400

    bound = pg.rectangle(size=(2100, 2100), layer=layerset['AUX'])
    bound = pg.offset(bound, distance=-20)
    bound = pg.outline(bound, distance=20, layer=layerset['AUX'])

    # reticle 1_1 
    r_X_jte    = d_ret1_1.add_ref(draw_X_test(layerset['JTE'], 'JTE'))
    r_X_gain   = d_ret1_1.add_ref(draw_X_test(layerset['GAIN'], 'GAIN', contact_layer=0))

    label1 = d_ret1_1.add_ref(pg.text(text='Van der Pauw', layer=layerset['METAL'], size=100))
    label1.rotate(90)

    label1.center     = (separation*0, 0)
    r_X_jte.center    = (separation*1, 0)
    r_X_gain.center   = (separation*2, 0)

    label3 = d_ret1_1.add_ref(pg.text(text='MOSCAP', layer=layerset['METAL'], size=100))
    label3.rotate(90)

    r_C_jte   = d_ret1_1.add_ref(draw_C_pad_small(layerset['JTE'], 'JTE', diameter))
    r_C_gain  = d_ret1_1.add_ref(draw_C_pad_small(layerset['GAIN'], 'GAIN', diameter))

    label3.center    = (separation*0, 900)
    r_C_jte.center   = (separation*1, 900)
    r_C_gain.center  = (separation*2, 900)

    d_ret1_1.center = (0, 0)
    r_bound1_1 = d_ret1_1.add_ref(bound)
    r_bound1_1.center = (0, 0)

    # reticle 1_2
    r_X_nplus  = d_ret1_2.add_ref(draw_X_test(layerset['NPLUS'], 'NPLUS'))
    r_X_gain_p = d_ret1_2.add_ref(draw_X_test(layerset['GAIN'], 'GAIN+PSTOP', contact_layer=5))
    r_X_pstop  = d_ret1_2.add_ref(draw_X_test(layerset['PSTOP'], 'PSTOP'))

    r_X_gain_p.center = (separation*0, 0)
    r_X_nplus.center  = (separation*1, 0)
    r_X_pstop.center  = (separation*2, 0)

    r_C_none  = d_ret1_2.add_ref(draw_C_pad_small(None, 'NONE', diameter))
    r_C_nplus = d_ret1_2.add_ref(draw_C_pad_small(layerset['NPLUS'], 'NPLUS', diameter))
    r_C_pstop = d_ret1_2.add_ref(draw_C_pad_small(layerset['PSTOP'], 'PSTOP', diameter))

    r_C_none.center  = (separation*0, 900)
    r_C_nplus.center = (separation*1, 900)
    r_C_pstop.center = (separation*2, 900)

    d_ret1_2.center = (0, 0)
    r_bound1_2 = d_ret1_2.add_ref(bound)
    r_bound1_2.center = (0, 0)


    # reticle 2_1
    r_I_jte10    = d_ret2_1.add_ref(draw_I_test(layerset['JTE'], 'JTE', width=10))
    r_I_jte20    = d_ret2_1.add_ref(draw_I_test(layerset['JTE'], 'JTE', width=20))
    r_I_gain10   = d_ret2_1.add_ref(draw_I_test(layerset['GAIN'], 'GAIN', width=10, contact_layer=0))
    r_I_gain20   = d_ret2_1.add_ref(draw_I_test(layerset['GAIN'], 'GAIN', width=20, contact_layer=0))

    label2 = d_ret2_1.add_ref(pg.text(text='Resistivity', layer=layerset['METAL'], size=100))
    label2.rotate(90)

    r_I_jte10.center    = (separation*1, 0)
    r_I_jte20.center    = (separation*1, r_I_jte10.ymin-r_I_jte20.ysize/2-250)
    r_I_gain10.center   = (separation*2, 0)
    r_I_gain20.center   = (separation*2, r_I_jte20.y)
    label2.center = (separation*0, (r_I_jte10.center[1] + r_I_jte20.center[1])*0.5)

    d_ret2_1.center = (0, 0)
    r_bound2_1 = d_ret2_1.add_ref(bound)
    r_bound2_1.center = (0, 0)

    # reticle 2_2
    r_I_gain10_p = d_ret2_2.add_ref(draw_I_test(layerset['GAIN'], 'GAIN+PSTOP', width=10, contact_layer=5))
    r_I_gain20_p = d_ret2_2.add_ref(draw_I_test(layerset['GAIN'], 'GAIN+PSTOP', width=20, contact_layer=5))
    r_I_nplus10  = d_ret2_2.add_ref(draw_I_test(layerset['NPLUS'], 'NPLUS', width=10))
    r_I_nplus20  = d_ret2_2.add_ref(draw_I_test(layerset['NPLUS'], 'NPLUS', width=20))
    r_I_pstop10  = d_ret2_2.add_ref(draw_I_test(layerset['PSTOP'], 'PSTOP', width=10))
    r_I_pstop20  = d_ret2_2.add_ref(draw_I_test(layerset['PSTOP'], 'PSTOP', width=20))

    r_I_gain10_p.center = (separation*0, 0)
    r_I_gain20_p.center = (separation*0, r_I_gain10_p.ymin-r_I_gain20_p.ysize/2-250)
    r_I_nplus10.center  = (separation*1, 0)
    r_I_nplus20.center  = (separation*1, r_I_gain20_p.y)
    r_I_pstop10.center  = (separation*2, 0)
    r_I_pstop20.center  = (separation*2, r_I_gain20_p.y)

    d_ret2_2.center = (0, 0)
    r_bound2_2 = d_ret2_2.add_ref(bound)
    r_bound2_2.center = (0, 0)

    # reticle 3_1 : big MOSCAP
    r_circle1 = d_ret3_1.add_ref(draw_C_pad())
    r_circle1.center = (0, 0)

    label4_1 = d_ret3_1.add_ref(pg.text(text='MOSCAP (NPLUS+GAIN+ILD)', layer=layerset['METAL'], size=100))
    #label4_2 = d_ret3_1.add_ref(pg.text(text='AREA = 2 mm', layer=layerset['METAL'], size=100))
    #label4_3 = d_ret3_1.add_ref(pg.text(text='2', layer=layerset['METAL'], size=50))
    #label4_2.rotate(90)
    #label4_3.rotate(90)
    label4_1.center = (0, r_circle1.ymax + 200) #(r_circle1.xmin-separation*0.7, 0)
    #label4_2.center = (r_circle1.xmin-200, 0)
    #label4_3.ymin = label4_2.ymax+10
    #label4_3.xmin = label4_2.x-50

    d_ret3_1.center = (0, 0)
    r_bound3_1 = d_ret3_1.add_ref(bound)
    r_bound3_1.center = (0, 0)

    # reticle 3_2 : big MOSCAP
    r_circle2 = d_ret3_2.add_ref(draw_C_pad(ild_layer=None))
    r_circle2.center = (0, 0)

    label5_1 = d_ret3_2.add_ref(pg.text(text='MOSCAP (NPLUS+GAIN)', layer=layerset['METAL'], size=100))
    #label5_2 = d_ret3_2.add_ref(pg.text(text='AREA = 2 mm', layer=layerset['METAL'], size=100))
    #label5_3 = d_ret3_2.add_ref(pg.text(text='2', layer=layerset['METAL'], size=50))
    #label5_2.rotate(90)
    #label5_3.rotate(90)
    label5_1.center = (0, r_circle2.ymax + 200) #(r_circle1.xmin-separation*0.7, 0)
    #label5_2.center = (r_circle2.xmin-200, 0)
    #label5_3.ymin = label5_2.ymax+10
    #label5_3.xmin = label5_2.x-50

    d_ret3_2.center = (0, 0)
    r_bound3_2 = d_ret3_2.add_ref(bound)
    r_bound3_2.center = (0, 0)

    # place the reticles

    r_ret1_1 = D.add_ref(d_ret1_1)
    r_ret1_2 = D.add_ref(d_ret1_2)
    r_ret2_1 = D.add_ref(d_ret2_1)
    r_ret2_2 = D.add_ref(d_ret2_2)
    r_ret3_1 = D.add_ref(d_ret3_1)
    r_ret3_2 = D.add_ref(d_ret3_2)

    r_ret1_2.xmin = r_ret1_1.xmax + 100
    r_ret2_2.xmin = r_ret2_1.xmax + 100
    r_ret2_1.ymax = r_ret1_1.ymin - 100
    r_ret2_2.ymax = r_ret1_1.ymin - 100

    r_ret3_2.xmin = r_ret3_1.xmax + 100
    r_ret3_1.ymax = r_ret2_1.ymin - 100
    r_ret3_2.ymax = r_ret2_1.ymin - 100

    d_ret1_1.write_gds(f'resources/testpattern1_1.gds') 
    d_ret1_2.write_gds(f'resources/testpattern1_2.gds') 
    d_ret2_1.write_gds(f'resources/testpattern2_1.gds') 
    d_ret2_2.write_gds(f'resources/testpattern2_2.gds') 
    d_ret3_1.write_gds(f'resources/testpattern3_1.gds') 
    d_ret3_2.write_gds(f'resources/testpattern3_2.gds') 

    return D

if __name__=="__main__":
    D = DrawTest()
    D.write_gds('test_X.gds')

