import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import io
import base64
import plotly.express as px
import dash_bootstrap_components as dbc

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Upload Data and Visualize")),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False  # Do not allow multiple files
            ),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='output-graph'), width=12)
    ])
])

# Helper function to parse the uploaded file
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an Excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None, "Unsupported file type"
        
        return df, None
    except Exception as e:
        return None, str(e)

# Callback to handle file upload and generate visualizations
@app.callback(
    Output('output-graph', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is None:
        # If no file is uploaded, display an empty graph
        return {}

    # Parse the uploaded file
    df, error = parse_contents(contents, filename)
    
    if error:
        return {}  # Return an empty graph in case of error

    # Check if the file has the expected structure (for example, check column names)
    required_columns = ['Entity', 'Year', 'Renewable energy share in the total final energy consumption (%)']
    if not all(col in df.columns for col in required_columns):
        return {}  # If the required structure is not met, return an empty graph

    # Generate a simple plot (scatter plot with lines) for visualization
    fig = px.line(df, x='Year', y='Renewable energy share in the total final energy consumption (%)', color='Entity',
                  title="Renewable Energy Share Over Time")

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
 