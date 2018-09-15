from gmplot import gmplot
lats = []
lngs = []
gmap = gmplot.GoogleMapPlotter.heatmap(lats, lngs)
gmap.draw("my_map.html")