# %%
import pandas as pd
import datetime
import numpy as np
import plotly.express as px
import dash
from dash import html,dcc,no_update
from dash.dash_table import DataTable
from dash.dependencies import Output,Input,State
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# %%
df = []
for i in range(1,5):
    frame = pd.read_excel('Thống kê Margin.xlsx',sheet_name = f"{i}")
    df.append(frame)

# %%
ctck = df[1].copy()
ctck['AseanSC']=ctck['Danh mục lọc bằng Tool']
ctck =ctck.drop(columns=ctck.columns[1:4])
melted = ctck.melt(id_vars = 'Tỷ lệ cho vay(%)',var_name = 'CTCK',value_name = 'Số mã')

# %%
p_v = pd.read_excel('Price and Volume.xlsx')

# %%
def my_table(i,df,id='',active_cell=None):
    df[i]['id']=df[i].index
    table=DataTable(id=id,
                    columns=[{'name':x,'id':x} for x in df[i].columns if x!='id'],
                    data=df[i].to_dict('records'),
                    sort_action='native',
                    filter_action='native',
                    active_cell=active_cell,
                    fill_width=False,
                    )
    return table

# %%
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div(
        dcc.Tabs(id="tabs", value='tabs-values', 
            children=[
            dcc.Tab(label='Danh mục Margin', value='one-table',
                    children=[
                        html.Div(children=[
                                html.H1('DANH MỤC MARGIN QUÝ 3 - 2023',style={'color':'magneta','textAlign':'center'}),
                                my_table(i=3,df=df,id='table_1',active_cell={'row':0,'column':0,'column_id':'Mã CK','row_id':0}),
                                html.Div(children=[
                                        dcc.DatePickerRange(id='input_date'),
                                        dcc.Graph(id='graph_1')])
                                        ],
                                style={'border':'dotted'})
                                ]
                ),
            dcc.Tab(label='Thống kê Margin', value='many-tables',
                    children=[
                        html.Div(children=[
                                html.Div(children=[
                                html.H1('THỐNG KÊ THAY ĐỔI MARGIN',style={'color':'magneta','textAlign':'center'}),
                                html.Div(my_table(2,df),style={'padding':'0px 0px 0px 435px'}),
                                html.Br(),
                                html.Div(my_table(0,df),style={'padding':'0px 0px 0px 250px'})],
                                style={'border':'dotted','width':'100%'}),
                        html.Div(children=[
                            html.H1('SO SÁNH VỚI CÁC CTCK KHÁC',style={'color':'magneta','textAlign':'center'}),
                            dcc.Graph(figure=px.bar(data_frame=melted,
                                                    x='Tỷ lệ cho vay(%)',
                                                    y='Số mã',
                                                    color = 'CTCK',
                                                    barmode='group'))],
                                        style={'border':'dotted','width':'100%'})]
                        ,style={'border':'dotted'})   
                    ])
                ]
        )
)

@app.callback(
    Output('graph_1','figure'),
    [Input('table_1','active_cell'),
     Input('input_date','start_date'),
     Input('input_date','end_date')]
)
def get_figure(active_cell,start_date,end_date):
        price_volume = p_v.copy(deep=True)
        if active_cell is None:
              return no_update
        elif active_cell is not None:
                if(start_date)and(end_date):
                        ticker = df[3].at[active_cell['row_id'],'Mã CK']
                        price_volume['TRADE_DATE']=pd.to_datetime(price_volume['TRADE_DATE'])
                        price_volume = price_volume.sort_values('TRADE_DATE')
                        start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
                        end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
                        price_volume = price_volume[price_volume['SECURITY_CODE'] == ticker]
                        price_volume = price_volume.loc[(price_volume['TRADE_DATE']>=start_date)&(price_volume['TRADE_DATE']<=end_date)]
                        fig = make_subplots(specs=[[{"secondary_y": True}]])
                        fig.add_trace(go.Scatter(x=price_volume['TRADE_DATE'], y=price_volume['CLOSE_PRICE'], name="Giá(VND)",mode='lines'),secondary_y=False)
                        fig.add_trace(go.Bar(x=price_volume['TRADE_DATE'], y=price_volume['TOTAL_VOLUME'], name="Khối lượng(CP)"),secondary_y=True)
                        # Add figure title
                        fig.update_layout(title_text="DỮ LIỆU GIÁ VÀ KHỐI LƯỢNG")
                        # Set x-axis title
                        fig.update_xaxes(title_text="Ngày giao dịch(Date)")
                        # Set y-axes titles
                        fig.update_yaxes(title_text="Giá(VND)", secondary_y=False)
                        fig.update_yaxes(title_text="Khối lượng(CP)", secondary_y=True,range=[0,35000000])
                        return fig
                else:
                        ticker = df[3].at[active_cell['row_id'],'Mã CK']
                        price_volume['TRADE_DATE']=pd.to_datetime(price_volume['TRADE_DATE'])
                        price_volume = price_volume.sort_values('TRADE_DATE')
                        price_volume = price_volume[price_volume['SECURITY_CODE'] == ticker]
                        fig = make_subplots(specs=[[{"secondary_y": True}]])
                        fig.add_trace(go.Scatter(x=price_volume['TRADE_DATE'], y=price_volume['CLOSE_PRICE'], name="Giá(VND)",mode='lines'),secondary_y=False)
                        fig.add_trace(go.Bar(x=price_volume['TRADE_DATE'], y=price_volume['TOTAL_VOLUME'], name="Khối lượng(CP)"),secondary_y=True)
                        # Add figure title
                        fig.update_layout(title_text="DỮ LIỆU GIÁ VÀ KHỐI LƯỢNG")
                        # Set x-axis title
                        fig.update_xaxes(title_text="Ngày giao dịch(Date)")
                        # Set y-axes titles
                        fig.update_yaxes(title_text="Giá(VND)", secondary_y=False)
                        fig.update_yaxes(title_text="Khối lượng(CP)", secondary_y=True,range=[0,35000000])
                        return fig
if __name__ == '__main__':
    app.run_server(debug=True)
        

# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%



