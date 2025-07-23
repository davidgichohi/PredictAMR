import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from eda import (
    df, plot_top_species, plot_top_countries,
    plot_top_susceptible_antibiotics, generate_country_wordclouds
)

# Header shown on every page
header = html.Div([
    html.Div([
        html.H2("PredictAMR", style={"marginBottom": 0, "fontWeight": "bold"}),
        html.H6("A One Health Dashboard for Surveillance, Interpretation, and Prediction of Antimicrobial Susceptibility",
                style={"marginTop": 0, "fontWeight": "normal"})
    ], style={"padding": "15px", "paddingLeft": "25px"})
], style={"backgroundColor": "#f8f9fa", "borderBottom": "1px solid #ccc", "marginBottom": "10px"})


def create_dashboard(app):
    return html.Div([
        header,
        dcc.Location(id='url', refresh=False),
        dbc.Row([
            dbc.Col([
                dbc.Nav(
                    [
                        dbc.NavLink([html.I(className="bi bi-bar-chart-line me-2"), "EDA"], href="/", active="exact"),
                        dbc.NavLink([html.I(className="bi bi-capsule me-2"), "MIC Interpreter"], href="/mic", active="exact"),
                        dbc.NavLink([html.I(className="bi bi-cpu me-2"), "AMR Predictor"], href="/predictor", active="exact"),
                        dbc.NavLink([html.I(className="bi bi-info-circle me-2"), "About"], href="/about", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                    className="mt-4"
                )
            ], width=2, style={"backgroundColor": "#f8f9fa", "height": "100vh"}),

            dbc.Col([
                html.Div(id='page-content', className="p-4")
            ], width=10)
        ])
    ])


# -------------------------- Layouts --------------------------

layout_eda = dbc.Container([
    html.H3("Exploratory Data Analysis", className="text-center mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Top 10 Isolated Species"),
            dbc.CardBody(dcc.Graph(figure=plot_top_species()))
        ]), md=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Top 10 African Countries by Reported Isolates"),
            dbc.CardBody(dcc.Graph(figure=plot_top_countries()))
        ]), md=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Top 15 Antibiotics with Most Susceptible Outcomes"),
            dbc.CardBody(dcc.Graph(figure=plot_top_susceptible_antibiotics()))
        ]), md=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Resistant Species Word Cloud by Country"),
            dbc.CardBody([
                dcc.Dropdown(
                    id="wordcloud-country",
                    options=[{"label": c, "value": c} for c in sorted(df['Country'].dropna().unique())],
                    value="Kenya"
                ),
                html.Div(id="wordcloud-output")
            ])
        ]), md=12)
    ])
], fluid=True)

layout_mic = html.Div([
    html.H3("MIC Interpreter", className="mt-4"),
    html.Iframe(src="https://amr-mic-1.onrender.com", width="100%", height="800", style={"border": "none"})
])

layout_predictor = html.Div([
    html.H3("AMR Predictor", className="mt-4"),
    html.Iframe(src="https://amr-predictor.onrender.com", width="100%", height="800", style={"border": "none"})
])

layout_about = html.Div([
    html.H3("About PredictAMR", className="mt-4"),
    html.P("This system presents visualizations and models designed to support antimicrobial resistance (AMR) surveillance, empirical treatment decision-making, and research."),
    html.H4("Key Features"),
    html.Ul([
        html.Li("Exploratory Data Analysis: Visual summaries (graphs, charts, word clouds) of AMR trends."),
        html.Li("MIC Interpreter: Rule-based MIC-to-SIR classification for clinical support."),
        html.Li("AMS Predictor: Machine learning tool predicting the most appropriate antibiotic based on patient and isolate profiles."),
    ]),
    html.H4("Data Source"),
    html.P("Pfizer ATLAS dataset (2004–2023) with over 950,000 bacterial isolates from 83 countries."),
    html.H4("Intended Users"),
    html.Ul([
        html.Li("Infectious disease and microbiology researchers"),
        html.Li("AMR surveillance and One Health teams"),
        html.Li("Hospital and clinical personnel"),
        html.Li("Policy planners and global health stakeholders"),
    ]),
    html.H4("Development Team"),
    html.Ul([
        html.Li("Raphael Mutua (KEMRI)"),
        html.Li("David Gichohi (DeKUT)"),
        html.Li("Rahma Golicha (KEMRI)"),
        html.Li("Frida Njeru (KEMRI)"),
        html.Li("Samuel Ndegwa (KEMRI)")
    ])
], className="p-4")


# -------------------------- Callbacks and Routing --------------------------

def get_page_layout(pathname):
    if pathname == "/":
        return layout_eda
    elif pathname == "/mic":
        return layout_mic
    elif pathname == "/predictor":
        return layout_predictor
    elif pathname == "/about":
        return layout_about
    else:
        return html.H3("404 - Page not found")


def register_callbacks(app):
    @app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
    def display_page(pathname):
        return get_page_layout(pathname)

    @app.callback(Output("wordcloud-output", "children"), Input("wordcloud-country", "value"))
    def update_wordcloud(country):
        return generate_country_wordclouds(country)
