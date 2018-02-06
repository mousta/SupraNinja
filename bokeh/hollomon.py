''' 
Hollomon law & Bokeh 
'''
import numpy as np

from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HBox, VBoxForm
from bokeh.models.widgets import Slider, TextInput
from bokeh.io import curdoc

def Hollomon(eps, E = 1., sy = .01, n = 0.2):
  """
  Hollomon law
  """
  ey = sy/E
  sigma_e = E * eps
  sigma_p = sy * (eps/ey)**n
  return np.where(sigma_p < sigma_e, sigma_p, sigma_e) 
  
# Set up data
N = 200
eps = np.linspace(0, 1., N)
sigma = Hollomon(eps)
source = ColumnDataSource(data=dict(x=eps, y=sigma))


# Set up plot
plot = Figure(plot_height=400, plot_width=400, title="Hollomon",
              tools="crosshair,pan,reset,resize,save,wheel_zoom",
              x_range=[0., eps.max()], y_range=[0., sigma.max()])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="title", value='my sine wave')
eps_max = Slider(title="max strain", 
                 value=.1, 
                 start=0., 
                 end=1.0, 
                 step=0.1)
modulus = Slider(title="Young's modulus $E$", 
                 value=1.0, 
                 start=0., 
                 end=10.0)
yield_stress = Slider(title="yield stress", 
                      value=.01, 
                      start=0.0, 
                      end=.1, 
                      step = 0.01)
hard_exp = Slider(title="hardening exp.", 
                  value=.2, 
                  start=0., 
                  end=1.,
                  step = 0.05)


# Set up callbacks
def update_title(attrname, old, new):
    plot.title = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    emax = eps_max.value
    E = modulus.value
    sy = yield_stress.value
    n = hard_exp.value
    
    # Generate the new curve
    eps = np.linspace(0, emax, N)
    sigma = Hollomon(eps, E = E, sy=sy, n=n)

    source.data = dict(x=eps, y=sigma)
    plot.x_range.end = eps.max()
    plot.y_range.end = sigma.max()
    

for w in [eps_max, modulus, yield_stress, hard_exp]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = VBoxForm(children=[text, eps_max, modulus, yield_stress, hard_exp])

curdoc().add_root(HBox(children=[inputs, plot], width=800))

from bokeh.embed import file_html

html = file_html(plot, "CDN", "my plot")
