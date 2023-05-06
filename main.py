# Import tkinter, mapview, math, sys, and data
import tkinter as tk
import tkintermapview as tkmap
import math
import airportsdata

# Create array of airports to use for listboxes
# * Only used for listboxes
airports = []

airports_data = airportsdata.load()
for airport in airports_data:
	airports.append([airports_data[airport]['icao'], airports_data[airport]["name"]])

airports = sorted(airports)

# Function to calculate nautical miles between two points using haversine formula
def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    distance_km = c * r
    distance_nm = distance_km / 1.852 # Convert kilometers to nautical miles
    return distance_nm

# Function to get the two airports and put the markers on the screen
# TODO Make this function also show a label with distance and other estimated
# TODO items like time, fuel burn, etc.
def get_distance():
    global marker1, marker2
    icao1 = listbox.get(listbox.curselection())[:4]
    icao2 = listbox2.get(listbox2.curselection())[:4]
    lat1, lon1 = airports_data[icao1]["lat"], airports_data[icao1]["lon"]
    lat2, lon2 = airports_data[icao2]["lat"], airports_data[icao2]["lon"]
    marker1.set_position(lat1, lon1)
    marker2.set_position(lat2, lon2)
    marker1.set_text(icao1)
    marker2.set_text(icao2)
    print(round(haversine(lat1, lon1, lat2, lon2), 2), "nm")

# * Main window and widgets setup
root = tk.Tk()
root.title("Flight Calculator")
root.grid_columnconfigure(weight=1, index=0)
root.grid_columnconfigure(weight=1, index=1)
root.grid_rowconfigure(weight=1, index=0)
root.minsize(width=850, height=450)

side_frame = tk.Frame(root)

main_frame = tk.Frame(root)

map_view = tkmap.TkinterMapView(main_frame, width=800, height=600, corner_radius=2)
map_view.set_zoom(1)

ok = tk.Button(side_frame, text="Calculate", command=get_distance)

marker1 = map_view.set_marker(0, 0)
marker2 = map_view.set_marker(0, 0)

# * Listboxes

# Listbox 1 -=-=-=-=-=-=-=-=-=-=-=-=-
listbox = tk.Listbox(side_frame)

# Populate the Listbox with data
for item in airports:
    listbox.insert(tk.END, f"{item[0]}-{item[1]}")

# Create a search field
search_var = tk.StringVar()
search_entry = tk.Entry(side_frame, textvariable=search_var)

# Define the search function
def search_listbox(event):
    search_term = search_var.get()
    for i in range(listbox.size()):
        if search_term.lower() in listbox.get(i).lower():
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(i)
            listbox.activate(i)
            listbox.see(i)
            break

# Bind the search function to the Entry field
search_entry.bind("<KeyRelease>", search_listbox)

# Listbox 2 -=-=-=-=-=-=-=-=-=-=-=-
listbox2 = tk.Listbox(side_frame)

# Populate the Listbox with data
for item in airports:
    listbox2.insert(tk.END, f"{item[0]}-{item[1]}")

# Create a search field
search_var2 = tk.StringVar()
search_entry2 = tk.Entry(side_frame, textvariable=search_var2)

# Define the search function
def search_listbox2(event):
    search_term = search_var2.get()
    for i in range(listbox.size()):
        if search_term.lower() in listbox2.get(i).lower():
            listbox2.selection_clear(0, tk.END)
            listbox2.selection_set(i)
            listbox2.activate(i)
            listbox2.see(i)
            break

# Bind the search function to the Entry field
search_entry2.bind("<KeyRelease>", search_listbox2)

# * END OF LISTBOXES

# Pack/Grid all widgets #*(For proper ordering on GUI)
side_frame.grid(row=0, column=0, sticky=tk.NSEW)
main_frame.grid(row=0, column=1, sticky=tk.NSEW)

map_view.pack(expand=True, fill=tk.BOTH)

listbox.pack(expand=True, fill=tk.BOTH)
search_entry.pack(expand=True, fill=tk.X)

listbox2.pack(expand=True, fill=tk.BOTH)
search_entry2.pack(expand=True, fill=tk.X)

ok.pack()

# Config listboxes to allow two listboxes two have a selection at once
listbox.configure(takefocus=False, exportselection=False)
listbox2.configure(takefocus=False, exportselection=False)

root.mainloop()
