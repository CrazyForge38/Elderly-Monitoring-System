import plotly
import plotly.graph_objects as go
import pandas as pd

excel_file = 'excel.ods'
df = pd.read_excel(excel_file, engine='odf')
print(df)

data = [go.Scatter3d( x=df['Date'], y=df['Revenue'], z=df['Profit'])] #selects the title of each column
#data = [go.Scatter( x=df['Date'], y=df['Revenue'])] #selects the title of each colum

fig = go.Figure(data)
fig.show()

