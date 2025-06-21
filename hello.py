import pandas as pd
import plotly.express as px
import preswald as pw
from preswald import selectbox

# from preswald import connect, get_df
# from preswald import query

# # Loading the dataset
# df = get_df("data/f1_circuits.csv")  # Load data for the dashboard
# connect()  # Initialize connection to preswald.toml data sources

# # Filtering the dataset
# sql = """SELECT
#   name,
#   country,
#   location,
#   first_year,
#   last_year,
#   active,
#   last_constructor
# FROM
#   circuits
# WHERE
#   active = TRUE
#   AND first_year < 2000
#   AND last_constructor != 'Red Bull';"""
# df = query(sql, "data/f1_circuits.csv")


pw.text("# F1 through the years")
df = pd.read_csv('data/f1_circuits.csv')
fig_scatter = px.scatter_geo(df,
                             lat="latitude",
                             lon="longitude",
                             hover_name="name",
                             title="F1 Circuit Locations Around the World",
                             projection="natural earth"
                             )
pw.text("F1 as a sport started off in Europe, and over time spread to other nations that could afford to host races, and maintain tracks. We can see the fan base growing over the years as new tracks across the world come into play.")
pw.plotly(fig_scatter)

df = pd.read_csv("data/grid_vs_position_by_decade.csv")
filtered_df = df[df["decade"] == 2020]
fig_violin = px.violin(
    filtered_df,
    x="grid",
    y="positionOrder",
    box=False,
    points=False,
    title=f"Grid vs Final Position",
    labels={"grid": "Grid Position", "positionOrder": "Final Position"}
)
pw.text("Before each race, theres a qualifying session. Driver's are required to drive around the circuit and the faster their lap, the better their starting position is in the actual race. To illustrate this relationship, the upcoming violin plot displays the distribution of finishing positions for each starting spot.")
pw.plotly(fig_violin)

pw.text("While drivers matter, so do the teams that build their cars. There are several constructor teams that develop the cars and hire drivers to race in them. Let's have a look at how drivers have performed throughout their careers under different constructors.")
df = pd.read_csv("data/yearly_stats.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df["year"] = df["year"].astype(int)
df["points"] = pd.to_numeric(df["points"], errors="coerce")
df = df.dropna(subset=["points"])

df_recent = df[df["year"] >= 2015]
driver_options = sorted(df_recent["driver_name"].unique())

selected_drivers = selectbox(
    label="Select a Driver (2015+)",
    options=driver_options,
    multi=False,
    height=100
)

if isinstance(selected_drivers, str):
    selected_drivers = [selected_drivers]

filtered_df = df_recent[df_recent["driver_name"].isin(selected_drivers)]

fig = px.line(
    filtered_df,
    x="year",
    y="points",
    color="driver_name",
    markers=True,
    title="Driver Points Since 2015",
    labels={"year": "Year", "points": "Points",
            "driver_name": "Driver", "constructor": "Constructor"},
    hover_data={"constructor": True}
)

fig.update_layout(height=500)
pw.plotly(fig)
