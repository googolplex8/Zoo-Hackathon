import gmplot

gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)
map_styles = [
        {
            'featureType': 'all',
            'stylers': [
                {'saturation': -80 },
                {'lightness': 60 },
            ]
        }
    ]

gmap.draw("mymap.html")