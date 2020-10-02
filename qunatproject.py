import pandas as pd
import dash
from dash.dependencies import Input, Output,State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame

df = pd.read_csv('BQ-Assignment-Data-Analytics.csv')


global Item
Item = [i  for i in ( df['Item'].unique().tolist() ) ]


global Date
Date = [i  for i in ( df['Date'].unique().tolist() ) ]


global Item_Sort_Order
Item_Sort_Order= [i  for i in ( df['Item Sort Order'].unique().tolist() ) ]
global fd

fd=pd.DataFrame()



for i in Date:
    fd[i]=None


    


fd['Item']=Item



fd['Item Sort Order']=Item_Sort_Order




dfj=df[df['Date']=='Jan-20']
Salesj=[i  for i in ( dfj['Sales'].unique().tolist() ) ]
fd['Jan-20']=Salesj
fd


dff=df[df['Date']=='Feb-20']
Salesf=[i  for i in ( dff['Sales'].unique().tolist() ) ]
fd['Feb-20']=Salesf



dfm=df[df['Date']=='Mar-20']
Salesm=[i  for i in ( dfm['Sales'].unique().tolist() ) ]
fd['Mar-20']=Salesm

dfa=df[df['Date']=='Apr-20']
Salesa=[i  for i in ( dfa['Sales'].unique().tolist() ) ]
fd['Apr-20']=Salesa



dfma=df[df['Date']=='May-20']
Salesma=[i  for i in ( dfma['Sales'].unique().tolist() ) ]
fd['May-20']=Salesma




fd = fd[['Item', 'Item Sort Order', 'Jan-20', 'Feb-20','Mar-20','Apr-20','May-20']]
for i in range(len(fd['Item'])):
    if fd.iloc[i][0] in ['Strawberry','Apple','Lychee','Cherries']:
        fd.loc[i,'Item Type']='Fruit'
    else:
        fd.loc[i,'Item Type']='Vegitable'
fd = fd[['Item Type','Item', 'Item Sort Order', 'Jan-20', 'Feb-20','Mar-20','Apr-20','May-20']]

app = dash.Dash(__name__)
app = dash.Dash(prevent_initial_callbacks=True)
app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        data=fd.to_dict('records'),
        columns=[
            {"name": i, "id": i, "selectable": True} for i in fd.columns[1:]
        ],
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        column_selectable="multi",
        row_selectable='multi',
        
        #row_deletable=True,
        selected_columns=[],
        selected_rows=[],
       

    ),
    dcc.RadioItems(id='radioitem',
           options=[
               {'label':'Select All','value':'Select All'},
               {'label':'Fruit','value':'Fruit'},
               {'label':'Vegitable','value':'Vegitable'},
           ],
           value='Select All'
       ),
    
    html.Div(id='datatable-interactivity-container'),
    html.Br(),
    html.Button("Download csv File Of Data", id="btn"), Download(id="download"),
    html.Td(),
    html.Br(),
    html.Button("Download xlsx File Of Data", id="btn1"), Download(id="download1")
])
@app.callback(
    Output('datatable-interactivity', 'data'),
    [Input('radioitem', 'value')]
) 
def update_data_table(radio_value):
    global fd
    if radio_value=='Fruit':
        fd1=fd[fd['Item Type']=='Fruit']
        data=fd1.to_dict('records')
        columns=[
                {"name": i, "id": i, "selectable": True} for i in fd.columns
            ]
        print(data)
        return data
    elif radio_value=='Vegitable':
        fd2=fd[fd['Item Type']=='Vegitable']
        data=fd2.to_dict('records')
        columns=[
                {"name": i, "id": i, "selectable": True} for i in fd.columns
            ]
        print(data)
        return data
    else:
        data=fd.to_dict('records')
        return data
    
@app.callback(
    Output('datatable-interactivity', "style_data_conditional"),
    [Input('datatable-interactivity', "derived_virtual_selected_rows"),
    Input('datatable-interactivity', 'selected_columns')])


def update_graphs(derived_virtual_selected_rows,selected_columns):
    print(derived_virtual_selected_rows)
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []    
    row1=[{
    "if": {"row_index": i},
    "backgroundColor": "#7FDBFF",
    'color': 'white'
}for i in derived_virtual_selected_rows]  
    column1= [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF',
        
    } for i in selected_columns]

    return row1 + column1
@app.callback(Output("download", "data"),
            [Input("btn", "n_clicks")],
            [State('radioitem', 'value')])
def func(n_nlicks,radio_value):
    if radio_value=='Fruit':
        fd1=fd[fd['Item Type']=='Fruit']
        return send_data_frame(fd1.to_csv, "Fruit.csv", index=False)
    elif radio_value=='Vegitable':
        fd2=fd[fd['Item Type']=='Vegitable']
        return send_data_frame(fd2.to_csv, "Vegitable.csv", index=False)
    else:
        return send_data_frame(fd.to_csv, "All_Data.csv", index=False)
@app.callback(Output("download1", "data"),
            [Input("btn1", "n_clicks")],
            [State('radioitem', 'value')])
def func(n_nlicks,radio_value):
    if radio_value=='Fruit':
        fd1=fd[fd['Item Type']=='Fruit']
        return send_data_frame(fd1.to_excel, "Fruit.xlsx", index=False)
    elif radio_value=='Vegitable':
        fd2=fd[fd['Item Type']=='Vegitable']
        return send_data_frame(fd2.to_excel, "Vegitable.xlsx", index=False)
    else:
        return send_data_frame(fd.to_excel, "All_Data.xlsx", index=False)


     
if __name__ == '__main__':
    app.run_server(debug=True)