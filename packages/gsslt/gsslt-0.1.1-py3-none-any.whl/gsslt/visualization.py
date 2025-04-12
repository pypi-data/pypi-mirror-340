from altair import Scale, theme

@theme.register('gessulat', enable=False)
def gessulat():
    font = "Georgia"
    return {
        'config': {
            "title": {
                'font': font,
                'fontSize': 20
            },
            "background": None,
            'view': {
                'width': 300,
                'height': 300,
                'stroke': None,
            },
            'mark': {
                'filled': True,
                'color': 'black',
                'opacity': 0.75,
            },
            'axis': {
                'labelFontSize': 14,
                'titleFontSize': 18,
                'offset': 10,
                'grid': False,
                'ticks': False,
                'labelFont': font,
                'titleFont': font
            },
            'legend': { 
                'titleFont': font,
                'labelFont': font,
                'titleFontSize': 14,
                'labelFontSize': 12
            },
            'range': {
                'category': {'scheme': 'observable10'}
            },
            'scale': {
                'nice': True
            }
        }
    }

def min_max_scale(df, col):
    return Scale(domain=[df[col].min(), df[col].max()])