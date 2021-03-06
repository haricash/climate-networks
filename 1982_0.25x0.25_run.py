import numpy as np
import matplotlib.pyplot as plt
from pyunicorn import climate
#import xarray as xr

DATA_FILENAME = 'data/_Clim_Pred_LRF_New_RF25_IMD0p251982.nc'
#DATA_FILENAME = xr.open_mfdataset(PATH)

#  Type of data file ("NetCDF" indicates a NetCDF file with data on a regular
#  lat-lon grid, "iNetCDF" allows for arbitrary grids - > see documentation).
#  For example, the "NetCDF" FILE_TYPE is compatible with data from the IPCC
#  AR4 model ensemble or the reanalysis data provided by NCEP/NCAR.
FILE_TYPE = "NetCDF"

#  Indicate data source (optional)
DATA_SOURCE = "Rajeevan_Dataset_1999"

#  Name of observable in NetCDF file ("air" indicates surface air temperature)
#  in NCEP/NCAR reanalysis data)
OBSERVABLE_NAME = "RAINFALL"

#  Select a subset in time and space from the data (e.g., a particular region
#  or a particular time window, or both)
#WINDOW = {"time_min": 0., "time_max": 0., "lat_min": 0, "lon_min": 0,
 #         "lat_max": 30, "lon_max": 0}  # selects the whole data set

#  Indicate the length of the annual cycle in the data (e.g., 12 for monthly
#  data). This is used for calculating climatological anomaly values
#  correctly.
TIME_CYCLE = 12

#  Related to climate network construction

#  For setting fixed threshold
THRESHOLD = 0.5

#  For setting fixed link density
LINK_DENSITY = 0.005

#  Indicates whether to use only data from winter months (DJF) for calculating
#  correlations
WINTER_ONLY = False

#
#  Print script title
#

print("\n")
print("Tutorial on how to use climate")
print("-------------------------------")
print("\n")

#
#  Create a ClimateData object containing the data and print information
#

data = climate.ClimateData.Load(
    file_name=DATA_FILENAME, observable_name=OBSERVABLE_NAME,
    data_source=DATA_SOURCE, file_type=FILE_TYPE,
    window=None, time_cycle=TIME_CYCLE)

#  Print some information on the data set
print(data)


map_plots = climate.MapPlots(data.grid, DATA_SOURCE)

#build network using mutual information
net = climate.MutualInfoClimateNetwork(
   data, threshold=THRESHOLD, winter_only=WINTER_ONLY)


 
print("Link density:", net.link_density)

#  Get degree
degree = net.degree()
#  Get closeness
closeness = net.closeness()
#  Get betweenness
betweenness = net.betweenness()
#  Get local clustering coefficient
clustering = net.local_clustering()
#  Get average link distance
ald = net.average_link_distance()
#  Get maximum link distance
mld = net.max_link_distance()

#
#  Save results to text file
#

#  Save the grid (mainly vertex coordinates) to text files
data.grid.save_txt(filename="1982_0.25x0.25_grid.txt")

#  Save the degree sequence. Other measures may be saved similarly.
np.savetxt("1982_0.25x0.25_degree.txt", degree)

#
#  Plotting
#

#  Comment everything below if you are not using pyngl for plotting!

#  Add network measures to the plotting queue
map_plots.add_dataset("Degree", degree)
map_plots.add_dataset("Closeness", closeness)
map_plots.add_dataset("Betweenness (log10)", np.log10(betweenness + 1))
map_plots.add_dataset("Clustering", clustering)
map_plots.add_dataset("Average link distance", ald)
map_plots.add_dataset("Maximum link distance", mld)

#  Change the map projection
map_plots.resources.mpProjection = "Robinson"
map_plots.resources.mpCenterLonF = 0

#  Change the levels of contouring
map_plots.resources.cnLevelSelectionMode = "EqualSpacedLevels"
map_plots.resources.cnMaxLevelCount = 20

# map_plots.resources.cnRasterSmoothingOn = True
# map_plots.resources.cnFillMode = "AreaFill"

map_plots.generate_map_plots(file_name="1982_0.25x0.25_climate_network_measures",
                             title_on=False, labels_on=True)

