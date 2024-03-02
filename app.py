import dash
from dash import dcc
from dash import html
from datetime import datetime as dt
import yfinance as yf
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
import datetime
# model
from model import prediction
from sklearn.svm import SVR
global cc 
cc=None

def get_stock_price_fig(df):

    fig = px.line(df,
                  x="Date",
                  y=["Close", "Open"],
                  title="Closing and Openning Price vs Date")

    return fig


def get_more(df):
    df['Price'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                     x="Date",
                     y="Price",
                     title="Price vs Date")
    fig.update_traces(mode='lines+markers')
    return fig


app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Roboto&display=swap",
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css"
        
    ],
    external_scripts=[
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js'
    ],
    )
server = app.server
# html layout of site


app.layout = html.Div(
    [   
                # # Navigation
                html.Nav(className = "navbar navbar-expand-lg bg-success text-white fw-bolder fixed-top", children=[
                #html.A('App1', className="nav-item nav-link btn"),
                html.Div(className = "container-fluid text-center", children=[
                    
                       #html.H4("GROW MORE !" , className ="p-1  font-bold"), 
                       #html.Img(className = "nav-icon", src='assets\stonk-img.png'),
                       html.Img(className = "nav-icon  p-1 font-bold", src='assets\\NAV-LOGO2.PNG'),
                       html.A("ABOUT US!" , className ="p-1  font-bold-ITALIC nav-link active",href="#end-of-the-page"), 
                ])
                ]),


               
                
        

        html.Div(
            [     

                 
                html.Div([
                    # html.P("Input stock code: "),
                    
                    html.Div([
                        html.Img(className = "nav-icon2", src='assets\LOGO1.png'),
                        #html.A(className="nav-link active",aria-current="page" ,href="#">Active),
                        



                        html.Div([
                            html.P("Maximise your", className="start"),
                            html.P("_", className="start2"),
                            html.P("PROFIT !", className="start4"),
                            html.P("_", className="start2"),
                            html.P("Minimise your", className="start"),
                            html.P("_", className="start2"),
                            html.P("RISK !", className="start4"),
                        ],className = "start d-flex flex-row mb-2 d-flex justify-content-center "),
                        
                        dcc.Input(id="dropdown_tickers", placeholder="Input stock code", type="text", className="mt-4 form-control"),
                        html.Button("Submit", id='submit', className="btn btn-success mt-2 text-center",
                        
                        ),
                    ], 
                             className="text-center justify-content-center")
                ],
                         ),
                         
                html.Div([
                    dcc.DatePickerRange(id='my-date-picker-range',
                                        min_date_allowed=dt(1995, 8, 5),
                                        max_date_allowed=dt.now(),
                                        initial_visible_month=dt.now(),
                                        end_date=dt.now().date()),
                       
                ],
                         className="date justify-content-center text-center mt-4"),


                html.Div([
                     html.Button(
                        "Stock Price", className="stock-btn mt-2 mx-2 btn btn-success", id="stock"),
                    html.Button("Indicators",
                                className="indicators-btn mt-2 btn btn-success",
                                id="indicators"),
                    dcc.Input(id="n_days",
                              type="text",
                              placeholder="number of days",
                              className="form-control mt-4"
                              ),
                    html.Button(
                        "Forecast", className="forecast-btn mt-2 btn btn-success", id="forecast")
                ],
                         className="buttons text-center justify-content-center"),
                # here
            ],
          className="mt-4"  ),

        # content
        html.Div(
            [
                html.Div(
                    [  # header
                        html.P(id="ticker"),
                       
                        html.H3(id="cut-price",),
                        
                        #html.P(id="cut-price"),
                    ],
                    className="header"),
                html.Div(id="description", className="decription_ticker"),
                html.Div([], id="graphs-content"),
                html.Div([], id="main-content"),
                html.Div([], id="forecast-content")
            ],
            className="content"),
    #html.P("©️copyrightfireupc",id="end-of-the-page",className="start3"),

    html.Div([
    html.Marquee([
        html.Div([html.Span([html.Img(className="marque-images",src="assets\\apple4.png")]),
            html.H4(["APPLE"]),
            html.P("AAPL"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\microsoft4.png")]),
            html.H4(["MICROSOFT"]),
            html.P("MSFT"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\google4.png")]),
            html.H4(["GOOGLE"]),
            html.P("GOOG"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\\amazon4.png")]),
            html.H4(["AMAZON"]),
            html.P("AMZN"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\\tesla4.png")]),
            html.H4(["TESLA"]),
            html.P("TSLA"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\samsung4.png")]),
            html.H4(["SAMSUNG"]),
            html.P("SMSN.IL"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\sbi4.png")]),
            html.H4(["SBI"]),
            html.P("SBIN.NS"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\hdfc4.png")]),
            html.H4(["HDFC"]),
            html.P("HDFCBANK.NS"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\zomato4.png")]),
            html.H4(["ZOMATO"]),
            html.P("ZOMATO.NS"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\dominos4.png")]),
            html.H4(["DOMINOS"]),
            html.P("DPZ"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\paypal4.png")]),
            html.H4(["PAYPAL"]),
            html.P("PYPL"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\indian-oil4.png")]),
            html.H4(["INDIAN OIL"]),
            html.P("IOC.NS"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\itc4.png")]),
            html.H4(["ITC"]),
            html.P("ITC.NS"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\hp4.png")]),
            html.H4(["HP"]),
            html.P("HPQ"),
        ],className="card"),

        html.Div([html.Span([html.Img(className="marque-images",src="assets\\tata4.png")]),
            html.H4(["TATA MOTORS"]),
            html.P("TATAMOTORS.NS"),
        ],className="card"),

       

        
       
        
    ],),
    ],className="copyright d-flex flex-row mb-2 d-flex justify-content-center"),










    html.Div([
     html.P('©Copyright '), 
     html.P("_", className="start2"),
     #html.SCRIPT(document.write(new Date().getFullYear())),
     html.P(datetime.datetime.now().strftime('%Y')),
     html.P("_", className="start2"),
     html.P("GROW MORE !", className="start5"),
     html.P("_", className="start2"),
     html.P(".Designed and developed by",id="end-of-the-page"),
     html.P("_", className="start2"),
     html.P("FireUpCode.", className="start5"),

    ],className="copyright d-flex flex-row mb-2 d-flex justify-content-center align-content-bottom"),
    ],
    className="container justify-content-center")
    


# callback for company info
@app.callback([
    Output("description", "children"),
    Output("cut-price", "children"),
    Output("ticker", "children"),
    Output("stock", "n_clicks"),
    Output("indicators", "n_clicks"),
    Output("forecast", "n_clicks"),
    #Output("cut-price","n_clicks")
], [Input("submit", "n_clicks")], [State("dropdown_tickers", "value")])
def update_data(n, val):
    global cc  # inpur parameter(s)
    if n == None:
        return "Hey there! Please enter a legitimate stock code to get details.", None, None, None, None, None
        # raise PreventUpdate
    else:
        if val == None:
            raise PreventUpdate
        else:
            ticker = yf.Ticker(val)
            inf = ticker.info
            df = pd.DataFrame().from_dict(inf, orient="index").T
            print(inf)
            cc=inf['currentPrice']
            print("======",cc)
                
            print(df)
            df[[ 'shortName', 'currentPrice','longBusinessSummary']]
            
            return df['longBusinessSummary'].values[0],"Current Price- "+str(cc),  df['shortName'].values[0], None, None, None


# callback for stocks graphs
@app.callback([
    Output("graphs-content", "children"),
], [
    Input("stock", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("dropdown_tickers", "value")])
def stock_price(n, start_date, end_date, val):
    if n == None:
        return [""]
        #raise PreventUpdate
    if val == None:
        raise PreventUpdate
    else:
        if start_date != None:
            df = yf.download(val, str(start_date), str(end_date))
            
        else:
            df = yf.download(val)

    df.reset_index(inplace=True)
    fig = get_stock_price_fig(df)
    return [dcc.Graph(figure=fig)]


# callback for indicators
@app.callback([Output("main-content", "children")], [
    Input("indicators", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("dropdown_tickers", "value")])
def indicators(n, start_date, end_date, val):
    if n == None:
        return [""]
    if val == None:
        return [""]

    if start_date == None:
        df_more = yf.download(val)
    else:
        df_more = yf.download(val, str(start_date), str(end_date))

    df_more.reset_index(inplace=True)
    fig = get_more(df_more)
    return [dcc.Graph(figure=fig)]


# callback for forecast
@app.callback([Output("forecast-content", "children")],
              [Input("forecast", "n_clicks")],
              [State("n_days", "value"),
               State("dropdown_tickers", "value")])
def forecast(n, n_days, val):
    if n == None:
        return [""]
    if val == None:
        raise PreventUpdate
    fig = prediction(val, int(n_days) + 1)
    return [dcc.Graph(figure=fig)]


if __name__ == '__main__':
    app.run_server(debug=False)
