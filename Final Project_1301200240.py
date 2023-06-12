import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

# Membaca data dari file CSV
data = pd.read_csv('statistik_kependudukan_jakarta.csv')

# Membuat aplikasi Dash
app = dash.Dash(__name__)

# Membuat pilihan tahun unik
tahun_options = [{'label': str(tahun), 'value': tahun} for tahun in data['tahun'].unique()]

# Tata letak tampilan aplikasi
app.layout = html.Div([
    html.H1("Visualisasi Statistik Kependudukan Jakarta"),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='tahun-dropdown',
                options=tahun_options,
                value=data['tahun'].min()
            )
        ], style={'width': '25%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Slider(
                id='kepadatan-slider',
                min=data['kepadatan_penduduk'].min(),
                max=data['kepadatan_penduduk'].max(),
                step=100,
                value=data['kepadatan_penduduk'].min(),
                marks={str(kepadatan): str(kepadatan) for kepadatan in data['kepadatan_penduduk'].unique()}
            )
        ], style={'width': '49%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Slider(
                id='rasio-slider',
                min=data['rasio_jenis_kelamin'].min(),
                max=data['rasio_jenis_kelamin'].max(),
                step=0.1,
                value=data['rasio_jenis_kelamin'].min(),
                marks={str(rasio): str(rasio) for rasio in data['rasio_jenis_kelamin'].unique()}
            )
        ], style={'width': '49%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Slider(
                id='rumah-tangga-slider',
                min=data['jumlah_rumah_tangga'].min(),
                max=data['jumlah_rumah_tangga'].max(),
                step=1000,
                value=data['jumlah_rumah_tangga'].min(),
                marks={str(jumlah): str(jumlah) for jumlah in data['jumlah_rumah_tangga'].unique()}
            )
        ], style={'width': '49%', 'display': 'inline-block'})
    ]),
    
    html.Div([
        dcc.Graph(id='kependudukan-graph')
    ])
])

# Membuat callback untuk mengupdate grafik berdasarkan input interaktif
@app.callback(
    dash.dependencies.Output('kependudukan-graph', 'figure'),
    dash.dependencies.Input('tahun-dropdown', 'value'),
    dash.dependencies.Input('kepadatan-slider', 'value'),
    dash.dependencies.Input('rasio-slider', 'value'),
    dash.dependencies.Input('rumah-tangga-slider', 'value')
)
def update_graph(tahun, kepadatan, rasio, jumlah_rumah_tangga):
    filtered_data = data[(data['tahun'] == tahun) &
                         (data['kepadatan_penduduk'] >= kepadatan) &
                         (data['rasio_jenis_kelamin'] >= rasio) &
                         (data['jumlah_rumah_tangga'] >= jumlah_rumah_tangga)]
    
    fig = px.scatter(filtered_data, x='kepadatan_penduduk', y='rasio_jenis_kelamin',
                     size='jumlah_rumah_tangga', hover_data=['tahun'],
                     labels={'kepadatan_penduduk': 'Kepadatan Penduduk',
                             'rasio_jenis_kelamin': 'Rasio Jenis Kelamin',
                             'jumlah_rumah_tangga': 'Jumlah Rumah Tangga'})
    
    fig.update_layout(title='Visualisasi Kependudukan Jakarta', xaxis_title='Kepadatan Penduduk',
                      yaxis_title='Rasio Jenis Kelamin', showlegend=False)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
