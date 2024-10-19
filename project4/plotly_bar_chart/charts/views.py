from django.shortcuts import render

# Create your views here.
# charts/views.py
from django.shortcuts import render
import plotly.graph_objs as go

def bar_chart(request):
    # Data for the bar chart (example: sales data)
    categories = ['Product A', 'Product B', 'Product C', 'Product D']
    values = [500, 700, 300, 400]
    
    # Create a bar chart
    bar_trace = go.Bar(
        x=categories,
        y=values,
        marker=dict(color='blue')
    )
    
    # Create a layout for the chart
    layout = go.Layout(
        title='Sales Data',
        xaxis=dict(title='Products'),
        yaxis=dict(title='Sales (in units)')
    )
    
    # Create the figure and convert it to HTML
    fig = go.Figure(data=[bar_trace], layout=layout)
    chart_html = fig.to_html(full_html=False)
    
    # Render the chart in the template
    return render(request, 'charts/bar_chart.html', {'chart_html': chart_html})
