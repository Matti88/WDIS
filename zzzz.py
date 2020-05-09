import numpy as np
from flask import Flask, jsonify, make_response, request

from bokeh.models import AjaxDataSource, CustomJS
from bokeh.plotting import figure, show

# Bokeh related code

adapter = CustomJS(code="""
    const result = {x: [], y: []}
    const pts = cb_data.response.points
    for (let i=0; i<pts.length; i++) {
        result.x.push(pts[i][0])
        result.y.push(pts[i][1])
    }
    return result
""")

source = AjaxDataSource(data_url='http://127.0.0.1:5000/advantages', polling_interval=0, adapter=adapter)

p = figure(plot_height=300, plot_width=800, background_fill_color="white",
           title="ScatterPlot")
p.circle('x', 'y', source=source)

p.x_range.follow = "end"
p.x_range.follow_interval = 100000000

show(p)