

def prediction(stock, n_days):
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
    # model
    from model import prediction
    from sklearn.model_selection import train_test_split
    from sklearn.model_selection import GridSearchCV
    import numpy as np
    from sklearn.svm import SVR
    from sklearn.metrics import r2_score
    from datetime import date, timedelta
    # load the data
    df = yf.download(stock, period='60d')
    df.reset_index(inplace=True)
    df['Day'] = df.index
    

    days = list()
    for i in range(len(df.Day)):
        days.append([i])

    # Splitting the dataset
    X = days
    Y = df[['Close']]
    print(X)
    print(Y)
    x_train, x_test, y_train, y_test = train_test_split(X,
                                                        Y,
                                                        test_size=0.1,
                                                        shuffle=False)

    gsc = GridSearchCV(
        estimator=SVR(kernel='rbf'),
        param_grid={
            'C': [0.001, 0.01, 0.1, 1, 100, 1000],
            'epsilon': [
                0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10,
                50, 100, 150, 1000
            ],
            'gamma': [0.0001, 0.001, 0.005, 0.1, 1, 3, 5, 8, 40, 100, 1000]
        },
        cv=5,
        scoring='r2',
        verbose=0,
        n_jobs=-1)

    y_train = y_train.values.ravel()
    
  
    grid_result = gsc.fit(x_train, y_train)
    best_params = grid_result.best_params_
    best_svr = SVR(kernel='rbf',
                   C=best_params["C"],
                   epsilon=best_params["epsilon"],
                   gamma=best_params["gamma"],
                   max_iter=-1)

    # Support Vector Regression Models
    rbf_svr = best_svr

    # # Support Vector Regression Models
  
    # rbf_svr.fit(x_train, y_train)

    # # Calculate accuracy percentage
    # test_accuracy = rbf_svr.score(x_test, y_test) * 100
    # print("Testing Accuracy: {:.2f}%".format(test_accuracy))
    # Support Vector Regression Models
  
    rbf_svr.fit(x_train, y_train)

    # Calculate accuracy percentage
    y_test_pred = rbf_svr.predict(x_test)
    percentage_errors = np.abs((y_test_pred - y_test.values.flatten()) / y_test.values.flatten()) * 100
    test_accuracy = 100 - np.mean(percentage_errors)
    print("Model Accuracy: {:.2f}%".format(test_accuracy))




   

    output_days = list()
    for i in range(1, n_days):
        output_days.append([i + x_test[-1][0]])

    dates = []
    current = date.today()
    for i in range(n_days):
        current += timedelta(days=1)
        dates.append(current)

    # plot Results
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=rbf_svr.predict(output_days),
            mode='lines+markers',
            name='data'
        )
    )
    fig.update_layout(
        title="Predicted Close Price of next " + str(n_days - 1) + " days",
        xaxis_title="Date",
        yaxis_title="Closed Price"
    )

    return fig


# prediction("AAPL", 12)
