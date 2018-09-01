# Generate a georeferenced map from an image dataset

In order to generate a georeferenced map, your dataset must meet the following requirements:

- All images should be in JPG format
- All images must have latitude, longitude, and altitude in the GPS EXIF data
- All images should be facing the area of interest
- All images should have significant overlap (more than 70% side and front overlap, 80% for agricultural or homogeneous imagery)
- At least 5 images for reliable map processing.

First, make sure you have [Docker](https://www.docker.com/get-started) and [Python 3](https://www.python.org/downloads/) installed on your machine.

## Generate a georeferenced map

```bash
# Clone WebODM repository
$ git clone https://github.com/OpenDroneMap/WebODM --config core.autocrlf=input --depth 1 ~/Repos/WebODM

# Run WebODM
$ cd ~/Repos/WebODM
$ ./webodm.sh start

# Install Python dependencies
$ pip install -r requirements.txt

# Run script
$ python generate_map.py
```

The script takes about 15 minutes to run on my MBP.

## Viewing generated georeferenced map

```bash
# Add OSGeo's Homebrew repository
$ brew tap osgeo/osgeo4mac

# Install QGis 3
$ brew install osgeo/osgeo4mac/qgis3

# Launch QGis
$ qgis3
```

You can now open `./output/ortophoto.tif` and measure distances and areas.
