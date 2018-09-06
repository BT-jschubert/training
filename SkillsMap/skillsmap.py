from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, CDSView, GroupFilter
import csv

output_file("skillsmap.html")
input_file = 'survey.user_input_demo.csv'

my_data = open(input_file, 'r')
csvreader = csv.reader(my_data, delimiter=',', quotechar='"')

levels = [ 'No knowledge',
           'Basic knowledge (not applied in projects so far)',
           'Good knowledge (applied in at least 1 project)',
           'Expert knowledge (applied in several projects)',
]

data_in_cols = []

for l in csvreader:
    data_in_cols.append(l)

data_in_cols = list(zip(*data_in_cols))

data_dict = {}

for d in data_in_cols:
    data_dict[d[0]] = list(d[1:])

# Fill in the names
for index, name in enumerate(data_dict['name']):
    if not name:
        data_dict['name'][index] = data_dict['name'][index - 1]

# Fill in the location
for index, location in enumerate(data_dict['location']):
    if not location:
        data_dict['location'][index] = data_dict['location'][index - 1]

cds_data = ColumnDataSource(data_dict)

# Get unique values.
skills = list(set(data_dict['skill']))
locations = list(set(data_dict['location']))

location_views = {}

# Build the CDSViews for every location
for loc in locations:
    location_views[loc] = CDSView(source=cds_data, filters=[GroupFilter(column_name='location', group=loc)])

TOOLTIPS = [
    ("Name", "@name"),
    ("Location", "@location"),
]
# Base plot
p = figure(title="brain-tec: Skills Map by location", plot_width=1400, plot_height=1600,
           x_range=levels, y_range=skills,
           tools="hover", toolbar_location=None, tooltips=TOOLTIPS)

# Plot the data for every location
for name, l_view in location_views.items():
    p.rect(x="level", y="skill", width=1, height=1, source=cds_data, view=l_view, fill_alpha=0.6,
           legend=name, color=factor_cmap("location", palette=Spectral6, factors=locations))

p.outline_line_color = None
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_standoff = 0
p.legend.orientation = "vertical"
p.legend.location ="top_right"
p.legend.click_policy="hide"

show(p)
