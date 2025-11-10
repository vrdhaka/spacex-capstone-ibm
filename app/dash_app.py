import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from pathlib import Path

app = dash.Dash(__name__)

# Load your cleaned data (update the path when ready)
data_path = Path(__file__).resolve().parents[1] / "data" / "cleaned_launches.csv"
if data_path.exists():
    df = pd.read_csv(data_path)
else:
    df = pd.DataFrame(columns=["launch_site","payload_mass","outcome","year"])

app.layout = html.Div([
    html.H2("SpaceX Launch Explorer"),
    dcc.Dropdown(sorted(df["launch_site"].dropna().unique()) if not df.empty else [], id="site", placeholder="Select a launch site"),
    dcc.RangeSlider(id="payload", min=0, max=25000, step=500, value=[0, 25000]),
    dcc.Graph(id="outcome_pie"),
    dcc.Graph(id="payload_scatter")
])

@app.callback(
    [dash.Output("outcome_pie","figure"), dash.Output("payload_scatter","figure")],
    [dash.Input("site","value"), dash.Input("payload","value")]
)
def update(site, payload_range):
    dff = df.copy()
    if site:
        dff = dff[dff["launch_site"]==site]
    lo, hi = payload_range or [0, 25000]
    dff = dff[(dff["payload_mass"].fillna(0)>=lo) & (dff["payload_mass"].fillna(0)<=hi)]
    pie = px.pie(dff, names="outcome", title="Launch Outcomes")
    scatter = px.scatter(dff, x="payload_mass", y="outcome", title="Payload vs Outcome", hover_data=dff.columns)
    return pie, scatter

if __name__ == "__main__":
    app.run_server(debug=True)