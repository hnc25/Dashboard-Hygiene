import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# ----------------------------
# Data Preparation
# ----------------------------
def get_data(time_range):
    if time_range == "1 Month":
        return {
            "contact_complete": {
                "Email": [100000, 95000, 90000, 85000],
                "Phone": [100000, 97000, 92000, 90000],
                "ZIP/Name": [100000, 90000, 85000, 80000],
                "TAC": [100000, 85000, 80000, 75000],
            },
            "corrections": {
                "NCOA": 5000,
                "PCOA": 2000,
                "PCA": 1000,
            },
            "email_standardization": {
                "Valid": 90000,
                "Invalid": 4000,
            }
        }
    elif time_range == "3 Months":
        return {
            "contact_complete": {
                "Email": [200000, 180000, 170000, 160000],
                "Phone": [200000, 190000, 180000, 170000],
                "ZIP/Name": [200000, 180000, 170000, 160000],
                "TAC": [200000, 170000, 160000, 150000],
            },
            "corrections": {
                "NCOA": 10000,
                "PCOA": 4000,
                "PCA": 2000,
            },
            "email_standardization": {
                "Valid": 180000,
                "Invalid": 8000,
            }
        }
    else:  # 6 Months
        return {
            "contact_complete": {
                "Email": [300000, 270000, 250000, 240000],
                "Phone": [300000, 290000, 270000, 260000],
                "ZIP/Name": [300000, 270000, 250000, 240000],
                "TAC": [300000, 260000, 240000, 230000],
            },
            "corrections": {
                "NCOA": 15000,
                "PCOA": 6000,
                "PCA": 3000,
            },
            "email_standardization": {
                "Valid": 270000,
                "Invalid": 12000,
            }
        }

# ----------------------------
# Layout of the Dashboard
# ----------------------------
app.layout = html.Div([
    # Title and Description
    html.H1("Hygiene Summary", style={"textAlign": "center", "marginBottom": "20px"}),
    html.P(
        "The Hygiene Summary dashboard evaluates the validation, enrichment, and standardization of customer contact data, "
        "including email, phone, ZIP/Name, and address records.",
        style={"textAlign": "center", "fontWeight": "bold"}
    ),

    # Time Range Selector
    html.Div([
        html.Label("Time Range:", style={"fontWeight": "bold", "textAlign": "center"}),
        dcc.Dropdown(
            id="time-range-dropdown",
            options=[
                {"label": "1 Month", "value": "1 Month"},
                {"label": "3 Months", "value": "3 Months"},
                {"label": "6 Months", "value": "6 Months"},
            ],
            value="1 Month",
            style={"width": "50%", "margin": "0 auto"}
        )
    ], style={"textAlign": "center", "marginBottom": "20px"}),

    # Contact Complete Section
    html.H2("Contact Complete", style={"marginTop": "30px"}),
    html.P(
        "Business Goal: How many records were completed using address, email, and phone from my customer profiles?",
        style={"fontWeight": "bold", "marginLeft": "10px"}
    ),
    html.Div(id="contact-complete-blocks", style={"display": "flex", "justifyContent": "space-around", "marginBottom": "20px"}),
    dcc.Graph(id="contact-complete-bar"),

    # Standardization and Corrections Section
    html.H2("Standardization and Corrections", style={"marginTop": "30px"}),
    html.P(
        "Business Goal: What is the total number of records that were standardized, corrected, or moved?",
        style={"fontWeight": "bold", "marginLeft": "10px"}
    ),
    html.Div(id="corrections-blocks", style={"display": "flex", "justifyContent": "space-around", "marginBottom": "20px"}),
    dcc.Graph(id="corrections-doughnut"),

    # Email Validation Section
    html.H2("Email Validation Status", style={"marginTop": "30px"}),
    html.P(
        "Business Goal: What is the total number of email records that were validated?",
        style={"fontWeight": "bold", "marginLeft": "10px"}
    ),
    html.Div(id="email-validation-blocks", style={"display": "flex", "justifyContent": "space-around", "marginBottom": "20px"}),
    dcc.Graph(id="email-validation-pie"),
])

# ----------------------------
# Callbacks for Dynamic Updates
# ----------------------------
@app.callback(
    [
        Output("contact-complete-blocks", "children"),
        Output("contact-complete-bar", "figure"),
        Output("corrections-blocks", "children"),
        Output("corrections-doughnut", "figure"),
        Output("email-validation-blocks", "children"),
        Output("email-validation-pie", "figure"),
    ],
    [Input("time-range-dropdown", "value")]
)
def update_dashboard(time_range):
    data = get_data(time_range)

    # Contact Complete Blocks
    contact_data = data["contact_complete"]
    contact_blocks = [
        html.Div([
            html.H4(f"{key} Appends", style={"textAlign": "center", "marginBottom": "10px"}),
            html.Div([
                html.Div(f"{sum(value):,}", style={
                    "padding": "10px",
                    "width": "45%",
                    "textAlign": "center"
                }),
                html.Div(style={
                    "borderLeft": "3px solid lightgray",  # Divider line
                    "height": "30px",  # Adjust height
                    "margin": "auto 5px"  # Center line with spacing
                }),
                html.Div(f"{round(sum(value) / sum(sum(v) for v in contact_data.values()) * 100, 1)}%", style={
                    "padding": "10px",
                    "width": "45%",
                    "textAlign": "center"
                })
            ], style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"})
        ], style={"width": "23%", "backgroundColor": "#f9f9f9", "padding": "20px", "borderRadius": "5px", "margin": "10px"})
        for key, value in contact_data.items()
    ]

    # Contact Complete Bar Chart
    contact_complete_fig = px.bar(
        pd.DataFrame({
            "Type": list(contact_data.keys()),
            "Total": [sum(contact_data[k]) for k in contact_data.keys()],
            "Percentage": [sum(contact_data[k]) / sum(sum(v) for v in contact_data.values()) * 100 for k in contact_data.keys()]
        }),
        x="Type", y="Total", text="Percentage",
        title="Records Completed by Type",
        labels={"Total": "Count", "Type": "Category"},
        color="Type",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    contact_complete_fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    contact_complete_fig.update_layout(showlegend=True, legend_title="Category")

    # Standardization and Corrections Blocks
    corrections_data = data["corrections"]
    corrections_blocks = [
        html.Div([
            html.H4(key, style={"textAlign": "center", "marginBottom": "10px"}),
            html.Div([
                html.Div(f"{value:,}", style={
                    "padding": "10px",
                    "width": "45%",
                    "textAlign": "center"
                }),
                html.Div(style={
                    "borderLeft": "3px solid lightgray",  # Divider line
                    "height": "30px",  # Adjust height
                    "margin": "auto 5px"
                }),
                html.Div(f"{round(value / sum(corrections_data.values()) * 100, 1)}%", style={
                    "padding": "10px",
                    "width": "45%",
                    "textAlign": "center"
                })
            ], style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"})
        ], style={"width": "30%", "backgroundColor": "#f9f9f9", "padding": "20px", "borderRadius": "5px", "margin": "10px"})
        for key, value in corrections_data.items()
    ]

    # Standardization and Corrections Doughnut Chart
    corrections_fig = px.pie(
        names=list(corrections_data.keys()),
        values=list(corrections_data.values()),
        hole=0.4,
        title="Standardization and Corrections"
    )

    # Email Validation Blocks
    email_data = data["email_standardization"]
    email_blocks = [
        html.Div([
            html.H4(key, style={"textAlign": "center", "marginBottom": "10px"}),
            html.Div([
                html.Div(f"{value:,}", style={
                    "padding": "10px",
                    "width": "45%",
                    "textAlign": "center"
                }),
                html.Div(style={
                    "borderLeft": "3px solid lightgray",  # Divider line
                    "height": "30px",  # Adjust height
                    "margin": "auto 5px"
                }),
                html.Div(f"{round(value / sum(email_data.values()) * 100, 1)}%", style={
                    "padding": "10px",
                    "width": "45%",
                    "textAlign": "center"
                })
            ], style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"})
        ], style={"width": "30%", "backgroundColor": "#f9f9f9", "padding": "20px", "borderRadius": "5px", "margin": "10px"})
        for key, value in email_data.items()
    ]

    # Email Validation Pie Chart
    email_fig = px.pie(
        names=["Valid", "Invalid"],
        values=[email_data["Valid"], email_data["Invalid"]],
        title="Email Validation Status"
    )
    email_fig.update_traces(textinfo='percent+label')

    return contact_blocks, contact_complete_fig, corrections_blocks, corrections_fig, email_blocks, email_fig

# ----------------------------
# Run the Server
# ----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
