import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import requests
from datetime import datetime
import pandas as pd
from dash_bootstrap_templates import load_figure_template

# Cargar template oscuro
load_figure_template("darkly")

# Inicializar la app
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

# Paleta de colores mejorada
COLORS = {
    'background': '#000000',
    'card': '#1a1a1a',
    'text': '#ffffff',
    'accent1': '#0A84FF',  # Azul iOS
    'accent2': '#5E5CE6',  # Violeta iOS
    'accent3': '#FF375F',  # Rosa iOS
    'success': '#30D158',  # Verde iOS
    'warning': '#FF9F0A',  # Naranja iOS
    'charts': ['#0A84FF', '#5E5CE6', '#FF375F', '#30D158', '#FF9F0A']
}

# Estilos de tarjetas
CARD_STYLE = {
    'backgroundColor': COLORS['card'],
    'borderRadius': '20px',
    'boxShadow': '0 8px 32px rgba(0, 0, 0, 0.12)',
    'margin': '12px',
    'padding': '20px',
    'border': f'1px solid {COLORS["card"]}'
}

METRIC_CARD_STYLE = {
    **CARD_STYLE,
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'space-between',
    'padding': '25px'
}

def fetch_data(endpoint):
    try:
        response = requests.get(f"http://localhost:8000{endpoint}")
        return response.json()
    except Exception as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Sales Analytics", 
                        className="display-3 text-center",
                        style={
                            'fontWeight': '200',
                            'letterSpacing': '-1.5px',
                            'color': COLORS['text'],
                            'fontFamily': 'SF Pro Display, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif'
                        }),
                html.P("Real-time business insights",
                      className="text-center mb-4",
                      style={
                          'fontSize': '1.3rem',
                          'color': '#8E8E93',
                          'fontWeight': '300'
                      })
            ], style={'padding': '40px 0 20px 0'})
        ])
    ]),

    # Métricas principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-3x",
                              style={'color': COLORS['accent1']}),
                    ], style={'marginRight': '20px'}),
                    html.Div([
                        html.H3("Total Revenue", 
                               style={'color': '#8E8E93', 'fontSize': '1rem', 'marginBottom': '8px'}),
                        html.H2(id="total-revenue", 
                               style={'color': COLORS['accent1'], 'fontSize': '2.2rem', 'margin': 0})
                    ])
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], style=METRIC_CARD_STYLE)
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-shopping-cart fa-3x",
                              style={'color': COLORS['accent2']}),
                    ], style={'marginRight': '20px'}),
                    html.Div([
                        html.H3("Average Order", 
                               style={'color': '#8E8E93', 'fontSize': '1rem', 'marginBottom': '8px'}),
                        html.H2(id="avg-order", 
                               style={'color': COLORS['accent2'], 'fontSize': '2.2rem', 'margin': 0})
                    ])
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], style=METRIC_CARD_STYLE)
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-trophy fa-3x",
                              style={'color': COLORS['accent3']}),
                    ], style={'marginRight': '20px'}),
                    html.Div([
                        html.H3("Top Category", 
                               style={'color': '#8E8E93', 'fontSize': '1rem', 'marginBottom': '8px'}),
                        html.H2(id="top-category", 
                               style={'color': COLORS['accent3'], 'fontSize': '2.2rem', 'margin': 0})
                    ])
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], style=METRIC_CARD_STYLE)
        ], width=4),
    ], className="mb-4"),

    # Gráficos principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-chart-area fa-2x",
                              style={'color': COLORS['accent1'], 'marginRight': '15px'}),
                        html.H4("Sales Trend", 
                               style={'color': '#8E8E93', 'margin': '0'}),
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),
                    dcc.Graph(id='daily-sales-chart',
                             config={'displayModeBar': False})
                ])
            ], style=CARD_STYLE)
        ], width=8),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-chart-pie fa-2x",
                              style={'color': COLORS['accent2'], 'marginRight': '15px'}),
                        html.H4("Category Distribution", 
                               style={'color': '#8E8E93', 'margin': '0'}),
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),
                    dcc.Graph(id='category-pie-chart',
                             config={'displayModeBar': False})
                ])
            ], style=CARD_STYLE)
        ], width=4),
    ], className="mb-4"),

    # Gráfico de barras y detalles
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-chart-bar fa-2x",
                              style={'color': COLORS['accent3'], 'marginRight': '15px'}),
                        html.H4("Product Performance", 
                               style={'color': '#8E8E93', 'margin': '0'}),
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),
                    dcc.Graph(id='product-performance-chart',
                             config={'displayModeBar': False})
                ])
            ], style=CARD_STYLE)
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-info-circle fa-2x",
                              style={'color': COLORS['warning'], 'marginRight': '15px'}),
                        html.H4("Category Details", 
                               style={'color': '#8E8E93', 'margin': '0'}),
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),
                    html.Div(id='category-details')
                ])
            ], style=CARD_STYLE)
        ], width=6),
    ]),

], fluid=True, style={'backgroundColor': COLORS['background'], 'minHeight': '100vh', 'padding': '20px'})

@app.callback(
    [Output('total-revenue', 'children'),
     Output('avg-order', 'children'),
     Output('top-category', 'children'),
     Output('daily-sales-chart', 'figure'),
     Output('category-pie-chart', 'figure'),
     Output('product-performance-chart', 'figure'),
     Output('category-details', 'children')],
    Input('daily-sales-chart', 'id')  # Dummy input para la actualización inicial
)
def update_dashboard(dummy):
    # Obtener datos
    sales_by_day = fetch_data("/sales/day")
    sales_by_category = fetch_data("/sales/category")
    sales_by_product = fetch_data("/sales/product")
    
    # Procesar datos para las métricas
    df_daily = pd.DataFrame(sales_by_day['sales'])
    total_revenue = df_daily['total_sales'].sum()
    avg_order = total_revenue / len(df_daily) if len(df_daily) > 0 else 0
    top_cat = max(sales_by_category['categories'], key=lambda x: x['total_revenue'])['category']

    # Gráfico de ventas diarias
    daily_fig = go.Figure()
    daily_fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['total_sales'],
        mode='lines+markers',
        line=dict(color=COLORS['accent1'], width=3, shape='spline'),
        marker=dict(size=8, color=COLORS['accent1']),
        name='Daily Sales'
    ))
    daily_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color=COLORS['text'],
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(l=40, r=40, t=40, b=40),
        height=400
    )

    # Gráfico de categorías
    df_category = pd.DataFrame(sales_by_category['categories'])
    pie_fig = go.Figure(data=[go.Pie(
        labels=df_category['category'],
        values=df_category['total_revenue'],
        hole=.6,
        marker=dict(colors=COLORS['charts']),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(color=COLORS['text'])
    )])
    pie_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color=COLORS['text'],
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=400
    )

    # Gráfico de productos
    df_product = pd.DataFrame(sales_by_product['products'])
    product_fig = go.Figure()
    product_fig.add_trace(go.Bar(
        x=df_product['total_sales'],
        y=df_product['product'],
        orientation='h',
        marker=dict(color=COLORS['accent2']),
        text=df_product['total_sales'].apply(lambda x: f'${x:,.2f}'),
        textposition='auto',
    ))
    product_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color=COLORS['text'],
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=20, r=20, t=20, b=20),
        height=400
    )

    # Detalles de categoría
    category_details = []
    for cat in sales_by_category['categories']:
        category_details.append(
            html.Div([
                html.Div([
                    html.H5(cat['category'], 
                           style={'color': COLORS['text'], 'marginBottom': '15px', 'fontSize': '1.2rem'}),
                    html.Div([
                        html.Span("Revenue: ", style={'color': '#8E8E93'}),
                        html.Span(f"${cat['total_revenue']:,.2f}", 
                                style={'color': COLORS['accent1'], 'fontWeight': 'bold'})
                    ], style={'marginBottom': '8px'}),
                    html.Div([
                        html.Span("Avg Price: ", style={'color': '#8E8E93'}),
                        html.Span(f"${cat['average_price']:,.2f}",
                                style={'color': COLORS['accent2'], 'fontWeight': 'bold'})
                    ], style={'marginBottom': '8px'}),
                    html.Div([
                        html.Span("Best Day: ", style={'color': '#8E8E93'}),
                        html.Span(cat['day_with_highest_sales'],
                                style={'color': COLORS['accent3'], 'fontWeight': 'bold'})
                    ])
                ], style={
                    'backgroundColor': 'rgba(255,255,255,0.05)',
                    'borderRadius': '15px',
                    'padding': '20px',
                    'marginBottom': '10px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'transition': 'all 0.3s ease',
                    'cursor': 'pointer'
                })
            ], className="category-detail-card")
        )

    return (
        f"${total_revenue:,.2f}",
        f"${avg_order:,.2f}",
        top_cat,
        daily_fig,
        pie_fig,
        product_fig,
        html.Div(category_details, style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
            'gap': '15px',
            'padding': '10px'
        })
    )

if __name__ == '__main__':
    app.run_server(debug=True)