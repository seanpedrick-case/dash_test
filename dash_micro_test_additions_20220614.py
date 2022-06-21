# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# Minimum required
import dash
import dash_core_components as dcc
import pandas as pd
import plotly.express as px

# Additional stuff
import dash_html_components as html
import dash_table
from dash_table import DataTable, FormatTemplate
import pandas as pd
from dash.dependencies import Input, Output

import plotly.graph_objects as go

data = pd.read_csv("A1a - KS2 standard RWM.csv")
#data = data.groupby(['Year-Month','Country'])['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')

# +
#tc_lookup_fold = "../../../../../Lambeth Council/Data, Analytics & Insight - Analytics Team - Private - Data Science Team - Private/IBD/IBD/data/external/area_lookups"

tc_lookup = pd.read_csv("town_centre_ward_lookup.csv")
# -

data = data.merge(tc_lookup, left_on = "Ward name", right_on = "Ward", how = "left").drop("Ward", axis = 1)

data['value_perc'] = (round(data['A1a - % KS2 students achieving expected standard in reading, writing, and maths in town centre areas']*100)).astype(str) + '%'

data.head()

# ## Create a table

large_tb = data

# + tags=[]
perc_format = FormatTemplate.percentage(2)
perc_cols = ['A1a - % KS2 students achieving expected standard in reading, writing, and maths in town centre areas']
d_columns = [{'name':x, 'id':x} for x in large_tb.columns if x not in perc_cols]
d_columns += [
    {'name':'A1a - % KS2 students achieving expected standard in reading, writing, and maths in town centre areas', 'id':'A1a - % KS2 students achieving expected standard in reading, writing, and maths in town centre areas', 
    'type':'numeric', 
    'format':perc_format
     # Allow columns to be selected
    , 'selectable':True
    }#,
    #{'name':'Ward rank', 'id':'Ward rank', 
    #'type':'numeric', 
    #'format':money_format
     # Allow columns to be selected
    #, 'selectable':True
    #}
]
# -

# ## Create dropdown and categories for dropdown

major_categories = list(data['Town centre'].dropna().unique())
minor_categories = list(data['Ward name'].unique())

major_categories

minor_categories

# #### Making a bar using the 'Figure'command. Doesn't seem to work well, and I can't get customdata to work

# data_bar = data.copy()
#
# bar_graph = go.Figure(data=go.Bar(x=data_bar['Ward name'], 
#                                       y=data_bar['A1a - % KS2 students achieving expected standard in reading, writing, and maths in town centre areas']))#, 
#                       #customdata = ['Town centre', "Ward name", "value_perc"])#,
#                          #width=1200, height=600, 
#                          #title=f'% KS2 students achieving expected standard in\nreading, writing, and maths in town centre areas:', 
#                          #custom_data=['Town centre'], color='Ward name', template='simple_white', text_auto=True, textposition ='auto', 
#                          #text=data_bar['A1a - % KS2 students achieving expected standard in reading, writing, and maths in town centre areas'])#
#     
# bar_graph.update_traces(marker_line_color='rgb(8,48,107)',# marker_color='rgb(158,202,225)', 
#                   marker_line_width=1.5, opacity=0.6)
#
# bar_graph.update_layout(title_text='KS2 students achieving expected standard in\nreading, writing, and maths in town centre areas')
#     
#     
# #### hover popup options
# bar_graph.update_traces(
#     hovertemplate="<br>".join([
#             "Ward: %{customdata[1]}",
#             "Town centre area: %{customdata[0]}",
#             "Value: %{customdata[2]}"]
# ))

# major_cat_title = "All"
#
# data_bar = data.copy()
#
# bar_graph = px.bar(data_bar, x='Ward name', 
#                        y='A1a - % KS2 students achieving expected standard in reading, writing, and maths in town centre areas',
#     width=800, height=600, 
#     title=f'% KS2 students achieving expected standard in<br>reading, writing, and maths in town centre areas: {major_cat_title}', 
#     custom_data=['Town centre', "Ward name", "value_perc"], color='Ward name', template='simple_white', text='value_perc'
#                   )# text_auto=True,
#     
# #### Bar appearance
# bar_graph.update_traces(marker_line_color='rgb(8,48,107)',# marker_color='rgb(158,202,225)', 
# marker_line_width=1.5, opacity=0.6)
#     
# #### Text label appearance
# bar_graph.update_traces(textfont_size=12,
#                         textangle=0,
#                         textposition="outside"
#                        )        
#
# #### Title options  
# bar_graph.update_layout(#{title:{'x':0.5}},
#                         title={
#                         'y':0.9,
#                         'x':0.5,
#                         'xanchor': 'center',
#                         'yanchor': 'top'},
#                         xaxis_title=None,
#                         yaxis_title="A1a - % KS2 students achieving expected standard<br>in reading, writing, and maths (%)")
#
# #### xaxis label options
# bar_graph.update_layout(
#                         xaxis_tickangle=-45
# )
#
# #### hover popup options
# bar_graph.update_traces(
#     hovertemplate="<br>".join([
#             "Ward: %{customdata[1]}",
#             "Town centre: %{customdata[0]}",
#             "Value: %{customdata[2]}"]
# ))
#                         

# ## Create the Dash app

# ### Setup the layout

# +
app = dash.Dash(__name__)

# Set up the layout with a single graph
app.layout = html.Div([
    
    # Title and break
    html.H1('KS2 students achieving expected standard in\nreading, writing, and maths'),
    html.Br(),
        
    # Dropdown and title
    html.Div( 
        children=[
            html.H3('Town centre selection'),
            
            dcc.Dropdown(id='major_cat_dd',
                options=[{'label':category, 'value':category} for category in major_categories], multi = True),
        #    
            html.Br(),
            
            html.H3('Ward selection'),
            
            dcc.Dropdown(id='minor_cat_dd',
                options=[{'label':categori, 'value':categori} for categori in minor_categories], multi = True)
               
        ],
    style={'width':'350px', 'display':'block', 'vertical-align':'top', 'border':'1px solid black', 'padding':'10px', 'margin':'auto'}
    ),
    
    html.Div(
        children=[
        # Bar graph
        dcc.Graph(
          id='my-bar-graph')#,
          # Insert the bar graph
          #figure=bar_fig)
        ]    
    ,style={'text-align':'center', 'display':'inline-block', 'width':'100%'} 
    )
])
    
# -

# ## Create callback for category filter interaction with graph

# +
@app.callback(
   Output('my-bar-graph', 'figure'),
   #Output('chosen_major_cat_title', 'children'),
   Input('major_cat_dd', 'value'),
   Input('minor_cat_dd', 'value'))

#def update_dd(major_cat_dd):
 #   major_minor = data[['Town centre', 'Ward name']].drop_duplicates()
  #  relevant_minor = major_minor[major_minor['Town centre'] == major_cat_dd]['Ward name'].values.tolist()
   # minor_options = [dict(label=x, value=x) for x in relevant_minor]

    #if not major_cat_dd:
     #   major_cat_dd = 'ALL'
    
    #major_cat_title = f'This is in the Major Category of : {major_cat_dd}'

    #return minor_options, major_cat_title

def update_bar(major_cat_dd, minor_cat_dd):
    major_cat_title = 'All'
    data_bar = data.copy()
    
    if major_cat_dd:
        major_cat_title = major_cat_dd
        data_bar = data_bar[data_bar['Town centre'].isin(major_cat_dd)]
        
    if minor_cat_dd:
        data_bar = data_bar[data_bar['Ward name'].isin(minor_cat_dd)]
        
    #data_bar = data_bar.groupby('Year-Month')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
    
    bar_graph = px.bar(data_bar, x='Ward name', 
                       y='A1a - % KS2 students achieving expected standard in reading, writing, and maths in town centre areas',
    height=600, # width=1000, , 
    title=f'% KS2 students achieving expected standard in<br>reading, writing, and maths in town centre areas: {major_cat_title}', 
    custom_data=['Town centre', "Ward name", "value_perc"], color='Ward name', template='simple_white', text='value_perc'
                  )# text_auto=True,
    
    # Bar appearance
    bar_graph.update_traces(marker_line_color='rgb(8,48,107)',# marker_color='rgb(158,202,225)', 
    marker_line_width=1.5, opacity=0.6)
    
    # Text label appearance
    bar_graph.update_traces(textfont_size=12,
                        textangle=0,
                        textposition="outside"
                       )        

    # Title options  
    bar_graph.update_layout(#{title:{'x':0.5}},
                        title={
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                        xaxis_title=None,
                        yaxis_title="A1a - % KS2 students achieving expected standard<br>in reading, writing, and maths (%)")

    # xaxis label options
    bar_graph.update_layout(
                        xaxis_tickangle=-45
    )

    # hover popup options
    bar_graph.update_traces(
        hovertemplate="<br>".join([
            "Ward: %{customdata[1]}",
            "Town centre: %{customdata[0]}",
            "Value: %{customdata[2]}"]
    ))
    
    return bar_graph


# -

# ## Major category dropdown interaction with minor category dropdown

# +
@app.callback(
   Output('minor_cat_dd', 'options'),
   #Output('chosen_major_cat_title', 'children'),
   Input('major_cat_dd', 'value'))

def update_dd(major_cat_dd):
    
    major_minor = data[['Town centre', 'Ward name']].drop_duplicates()
    
    minor_options = [dict(label=x, value=x) for x in major_minor['Ward name'].values.tolist()]
     
    if major_cat_dd:        
        relevant_minor = major_minor[major_minor['Town centre'].isin(major_cat_dd)]['Ward name'].values.tolist()
        minor_options = [dict(label=x, value=x) for x in relevant_minor]

    #if not major_cat_dd:
        #major_cat_dd = 'ALL'
    
   # major_cat_title = f'This is in the Major Category of : {major_cat_dd}'

    return minor_options#, major_cat_title


# -

# ### Run the app

# Set the app to run in development mode
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

# +
# Following is if you need to debug
# # %tb
# -


