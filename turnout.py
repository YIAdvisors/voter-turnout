import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_daq as daq

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import heroku3
from dash.dependencies import Input, Output

#Ensure dash capabilities are enabled.
#This allows the code to be deployed on an online server.
app = dash.Dash(__name__)
server = app.server


################################################################################
#This code creates a data visualization of the uninsured rate by state.
#The plotly package is used to create the visualization.
#The dash package is used to create an interactive web app.
#If the app is put on a website, use an iframe of height 800 and width 925.
#################################################################################


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("ya_voter_turnout.csv")
dfExpanded = pd.read_csv("voter_turnout_cleaned.csv")
df35up = pd.read_csv("non_ya_voter_turnout.csv")
state_map = {"Alabama":"AL", "Alaska":"AK", "Arizona":"AZ", "Arkansas":"AR", "California":"CA", "Colorado":"CO", "Connecticut":"CT","District of Columbia":"DC", "Delaware":"DE", "Florida":"FL","Georgia":"GA",
          "Hawaii":"HI", "Idaho":"ID", "Illinois":"IL", "Indiana":"IN", "Iowa":"IA", "Kansas":"KS", "Kentucky":"KY", "Louisiana":"LA", "Maine":"ME", "Maryland":"MD",
          "Massachusetts":"MA", "Michigan":"MI", "Minnesota":"MN", "Mississippi":"MS", "Missouri":"MO", "Montana":"MT", "Nebraska":"NE", "Nevada":"NV", "New Hampshire":"NH", "New Jersey":"NJ",
          "New Mexico":"NM", "New York":"NY", "North Carolina":"NC", "North Dakota":"ND", "Ohio":"OH", "Oklahoma":"OK", "Oregon":"OR", "Pennsylvania":"PA", "Rhode Island":"RI", "South Carolina":"SC",
          "South Dakota":"SD", "Tennessee":"TN", "Texas":"TX", "Utah":"UT", "Vermont":"VT", "Virginia":"VA", "Washington":"WA", "West Virginia":"WV", "Wisconsin":"WI", "Wyoming":"WY"}
df['state_code'] = df['State:'].map(state_map)
dfExpanded['state_code'] = dfExpanded['State:'].map(state_map)
df35up['state_code'] = df35up['State:'].map(state_map)

fnameDict = {"heat map" :["Ages 35+ Turnout - Young Adult Turnout"],
            "education": ["Less than High School", "High School Grad", "Some College","Associate's Degree","Bachelor's Degree","Post-Graduate Degree"],
            "race": ["White", "Hispanic","Black","American Indian","Asian or PI"],
            "employment": ["At Work", "Unemployed","NILF"],
            "age": ["Under 18", "18-23","24-34","35-59","Over 60"],
            }
names = list(fnameDict.keys())
nestedOptions = fnameDict[names[0]]

print(df[:3])
print(dfExpanded[:3])

# ------------------------------------------------------------------------------
# App layout (create app layout for the web app)
app.layout = html.Div([
    #Create title.
    html.H1("Voter Turnout Rate for Young Adults Ages 18-34", style={ 'text-align': 'Center','fontFamily':'Arial, serif'}),

    #Display the option from the slider the user selected. (It is currently disabeled. to enable, change the code in the app.callback so that container = "option_slctd")
    html.Div(id='output_container', children=[],style={'text-align': 'Center', 'fontFamily':'Arial, serif'}),
    html.Br(),
    html.Div(children='''Statistic of Interest:''', style={'text-align': 'left', 'margin-left': '2%', 'fontFamily':'Arial, serif', 'padding-bottom':'1%'}),
    dcc.Dropdown(id="slct_statistic",
            options=[{'label':name, 'value':name} for name in names],
            value = list(fnameDict.keys())[0],
            multi=False,
            style={'width': "45%", 'margin-left': '2%'}
            ),
    dcc.Dropdown(id="slct_val",
                 multi=False,
                 value="Ages 35+ Turnout - Young Adult Turnout",
                 style={'width': "45%", 'margin-left': '2%'}
                 ),
    #Creates a Plotly choropleth map graph.
    dcc.Graph(id='uninsured_map', config={
                'displayModeBar': False}),

    #Creates a slider, enabling the user to choose the year displayed.
    html.Div(children=[
        daq.Slider(id="slct_year",
            updatemode='drag',
            min=2000,
            max=2016,
            size=750,
            className='slider',
            marks={
                2000: {'label': '2000','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}}, #creates a list with the options
                2004: {'label': "2004",'style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2008: {'label': '2008','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2012: {'label': '2012','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                2016: {'label': '2016','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                #2002: {'label': '2002','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                #2006: {'label': '2006','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                #2010: {'label': '2010','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                #2014: {'label': '2014','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
                #2018: {'label': '2018','style':{'text-align': 'center', 'fontFamily':'Arial, serif','color':'#3D3D3D'}},
            },
            handleLabel={"showCurrentValue": True,
                        'color':'#3D3D3D',
                        'style':{'text-align': 'center', 'fontFamily':'Arial, serif'},
                        'label':'Year:',
                        },
            step=4,
            color={"gradient":True,"ranges":{"gray":[0,6],"gray":[6,8],"gray":[8,10]}},
            value=2016
            )
    ], style={'width': '100%','padding-left':'20%', 'padding-right':'20%'}),



            #style={'width':'800px','height': '100vh', 'justify':'center', 'align':'center','text-align': 'Center','margin:':'auto'}),
            #style="width:800px; margin:0 auto;"
            #style={'width': '100%','text-align':'center','justify-content':'center','margin':'0 auto','margin-left':'auto', 'margin-right':'auto','padding-left':'10%'}
])

    #style={'width': '95%','padding-left':'0%', 'padding-right':'0%'}

@app.callback(
    dash.dependencies.Output('slct_val', 'options'),
    [dash.dependencies.Input('slct_statistic', 'value')]
)
def update_date_dropdown(name):
    return [{'label': i, 'value': i} for i in fnameDict[name]]



# ------------------------------------------------------------------------------
# Connect the Plotly graph with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='uninsured_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'), #Note the second input used here. This is so the graph can update both the year and the statistic displayed.
    Input(component_id='slct_statistic', component_property='value'),
    Input(component_id='slct_val', component_property='value')]
    )
def update_graph(option_slctd,slct_statistic,slct_val):
    print(option_slctd)

    #Code to dynamically display the selected option is in the comment below:
    #container = "The year chosen by user was: {}".format(option_slctd)
    container = ""

    #Create a new dataframe that only includes the selected year's values
    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff['voterturnout'] = dff['voterturnout']*100
    dff['voterturnoutStr'] = "percent voted"
    dff = dff.round(decimals=2)

    if(slct_val == "Ages 35+ Turnout - Young Adult Turnout"):
        dfCopy = df35up.copy()
        dfCopy = dfCopy[dfCopy["Year"] == option_slctd]
        dfCopy['voterturnout'] = (dfCopy['voterturnout']*100) - dff['voterturnout']
        dfCopy = dfCopy.round(decimals=2)
        hoverVal = dfCopy['voterturnout'].astype(str)+"% more people ages 35+ voted in "+dff['state_code']
    else:
        dfCopy = dfExpanded.copy()
        dfCopy = dfCopy[dfCopy["Year"] == option_slctd]
        dfCopy = dfCopy[dfCopy["stat_type"]== slct_statistic]
        dfCopy = dfCopy[dfCopy["stat_val"]== slct_val]
        dfCopy = dfCopy[dfCopy["YA"]== False]
        dfCopy['voterturnout'] = dfCopy['voterturnout']*100
        dfCopy['voterturnoutStr'] = "percent voted"
        dfCopy = dfCopy.round(decimals=2)
        hoverVal = dfCopy['voterturnout'].astype(str)+"% voted in "+dfCopy['state_code']
        print(hoverVal)
        print(dfCopy[:5])




    # Plotly Express
    # Creates choropleth map of the US with the selected year

    fig = make_subplots(rows=1, cols=2,
        specs=[[{'type': 'choropleth'},{'type': 'choropleth'}]],
        subplot_titles=('Young Adults', 'Comparison'))

    map1 = go.Choropleth(
        locations=dff['state_code'],
        z=dff['voterturnout'],
        locationmode='USA-states',
        colorbar_showticklabels=False,
        #colorscale='Reds', (this is another option)
        colorscale = ["#e9ebef","#d4d8e0","#959eb2","#6b7793","#415174","#2c3e65"], #Creates a custom color scale for the map, using YI's colors.
        autocolorscale=False,
        colorbar_ticksuffix = '%',
        name="",
        zmax = 100,
        zmin = 0,
        hovertemplate = dff['voterturnout'].astype(str)+"% voted in "+dff['state_code'],
        marker_line_color='white', # line markers between states
        colorbar_title="Voter Turnout Percentage"
    )

    map2 = go.Choropleth(
        locations=dfCopy['state_code'],
        z=dfCopy['voterturnout'],
        locationmode='USA-states',
        colorscale = ["#e9ebef","#d4d8e0","#959eb2","#6b7793","#415174","#2c3e65"], #Creates a custom color scale for the map, using YI's colors.
        autocolorscale=False,
        colorbar_ticksuffix = '%',
        geo = "geo",
        name="",
        hovertemplate = hoverVal,
        zmax = 100,
        zmin = 0,
        marker_line_color='white', # line markers between states
        colorbar_title="Voter Turnout Percentage"
    )

    fig.add_trace(
        map1,
        row=1, col=1
    )


    fig.update_layout(
        geo = dict(scope='usa', projection=go.layout.geo.Projection(type = 'albers usa'))
        )

    fig.add_trace(
        map2,
        row=1, col=2
    )


#Adds custom styling to the choropleth maps of the US.
    fig.update_layout(
        geo = dict(scope='usa', projection=go.layout.geo.Projection(type = 'albers usa')),
        geo2 = dict(scope='usa', projection=go.layout.geo.Projection(type = 'albers usa')),
        #annotations = [dict(
        #    x=0.55,
        #    y=-.1,
        #    xref='paper',
        #    yref='paper',
        #    text='Source: <a href="https://usa.ipums.org/usa/" style="color:#dd3430">American Community Survey</a>',
        #    showarrow = False
        #    )]
        )


    #Returns the selected value and the figure to be displayed in the web app.
    return container, fig


#Command that ensures dash capabilities are enabled.
#This allows the code to be deployed on an online server.
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
