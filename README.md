# lgad_wafer_v1

## Test - drawing a single sensor

`$ python3 test_sensor.py`

## Drawing a reticle

1. Make a json template

`$ python3 lgad_draw/makeReticleTemplate.py <sensor name prefix (optional)>`

2. Modify the json file as you need.

3. Run

`$ python3 draw_reticle.py <json file name>`

## Drawing a wafer

1. Make a wafer template

`$ python3 lgad_draw/makeWaferTemplate.py`

2. Modify the json file as you need.

3. Run

`$ python3 draw_wafer.py <json file name>`

ex)
`$ python3 draw_wafer.py wafer_json/wafer_template.json`
