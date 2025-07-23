import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from dash import html

df = pd.read_csv("data/atlas-data.csv", low_memory=False)

def plot_top_species():
    top_species = df['Species'].value_counts().nlargest(10)
    fig = px.bar(
        x=top_species.values,
        y=top_species.index,
        orientation='h',
        title="Top 10 Most Frequent Isolated Species",
        labels={'x': 'Count', 'y': 'Species'},
        color=top_species.values,
        color_continuous_scale='Blues'
    )
    fig.update_layout(template="plotly_white")
    return fig

def plot_top_countries():
    top_countries = df['Country'].value_counts().nlargest(10)
    fig = px.bar(
        x=top_countries.values,
        y=top_countries.index,
        orientation='h',
        title="Top 10 African Countries by Number of Reported Isolates",
        labels={'x': 'Count', 'y': 'Country'},
        color=top_countries.values,
        color_continuous_scale='Greens'
    )
    fig.update_layout(template="plotly_white")
    return fig

def plot_top_susceptible_antibiotics():
    antibiotic_cols = [col for col in df.columns if col.endswith("_I")]

    counts = {}
    for col in antibiotic_cols:
        count_s = (df[col] == "Susceptible").sum()
        if count_s > 0:
            counts[col.replace("_I", "")] = count_s

    if not counts:
        return px.bar(title="No susceptible antibiotic data found.")

    top_antibiotics = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:15]
    df_top = pd.DataFrame(top_antibiotics, columns=["Antibiotic", "Susceptible Count"])

    fig = px.bar(
        df_top,
        x="Antibiotic",
        y="Susceptible Count",
        title="Top 15 Antibiotics with Most Susceptible Outcomes",
        color="Susceptible Count",
        color_continuous_scale="Oranges"
    )
    fig.update_layout(xaxis_tickangle=-45, template="plotly_white")
    return fig

def generate_country_wordclouds(country):
    # Filter rows by selected country
    country_df = df[df["Country"] == country]

    # Count species frequency
    species_counts = country_df["Species"].value_counts().to_dict()

    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(species_counts)

    # Convert plot to base64 image
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format='PNG')
    encoded_image = base64.b64encode(buffer.getvalue()).decode()

    return html.Img(src=f'data:image/png;base64,{encoded_image}', style={"width": "100%", "height": "auto"})