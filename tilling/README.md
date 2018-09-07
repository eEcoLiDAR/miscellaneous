# Tilling LiDAR data sets

When working with large LiDAR data sets we often encountered the data set either fragmented over multiple small tiles or condensed into large tiles. The latter becomes an issue when the decompressed tile size is larger than the available main-memory of a modest server node, 32GB main memory server. Furthermore, the grid formed by the LiDAR tiles is often of different scale and alignment than the one used as basis for spatial and structural studies. To overcome this limitation, we decided to use [Massive-PotreeConverter](https://github.com/NLeSC/Massive-PotreeConverter) to re-grid the LiDAR data set.


## Massive PotreeConverter

The Massive PotreeConverter builds an octree over a LiDAR data set using a divide and conquer approach. To re-grid a LiDAR data set we use its tool called `mpc-tiling`. It takes as parameters the location of the LiDAR data set, location to store the re-gridded data (each grid cell will be a sub-directory at the given path), the number of cells for a square grid, and the extent of the data set. Then it goes over all the LiDAR files in the input directory and using the files bounding box it determines to each grid cell or cells it belongs. If it fits within a single grid cell, the LiDAR file is simply copied otherwise the file is split using [pdal split](https://pdal.io/apps/split.html). Currently `mpc-tiling` does not check if a LiDAR file was already been processed or not. If the user gives the same input and output directory, it will compute again all the LiDAR files stored in the input directory and its sub-directories.

Massive PotreeConverter was designed to process massive point cloud data sets. Due the high data parallelism degree of the tasks, multiple tiles can be processed independently, each of its tools is executed in parallel and across multiple nodes. Distributed processing is not affected by the input tiles size, however, parallelism is since for large tiles a lot main-memory is required. The user should pay attention to that when scheduling the `mpc-tiling` for execution.

### Mpc-tiling

`Mpc-tiling` has two key parameters, number of gird cells and its extent. A drawback of the system is that the number of grid cells must be multiple of 2, an optimization for easy navigation over directories name composing the final result.

For the Netherlands the LiDAR data uses [Amersfoort / RD new](https://epsg.io/28992) projection, i.e., the `EPSG projection 28992`. The center coordinates of `EPSG projection 28992` is `142892.19 470783.87`. To obtain a grid with square cells of 2km length centered with [Amersfoort / RD new](https://epsg.io/28992) we need to create a grid of size `256x256` since a grid of `128x128` (grid size has to be multiple of 2) will not be enough to cover all the Netherlands. Hence, the extent of the grid will be `-113107.8100 214783.8700 398892.1900 726783.87` and it was calculated as follow:
```
X = 142892.19
Y = 470783.87

x_min = X - 128000 = -113107.8100
x_max = X + 128000 = 398892.1900
y_min = Y - 128000 = 214783.8700
y_max = Y + 128000 = 726783.87

Extent = (x_min y_min x_max y_max) 
```

Once we know the grid extent it is easy to re-grid any Dutch LiDAR data set. In the following example we are tiling the LiDAR data set [AHN3](https://www.pdok.nl/nl/ahn3-downloads) downloaded on `2018-08-10` using 2 parallel processes.
```
#-i <input directory>
#-t <temp directory>
#-o <output directory>
#-e <extent>
#-n <number of cells> (in this case 256x256 = 65536
#-p <number of processes>

mpc-tiling -i /data/local/eecolidar_webdav/01_Work/ALS/Netherlands/ahn3_10_08_2018/ -o /data/local/eecolidar_webdav/01_Work/ALS/Netherlands/ahn3_10_08_2018_256x256_2km/ -t /data/local/eecolidar/rclone/tmp/ -e "-107888.7340 203621.0926 404111.2660 715621.0926" -n 65536 -p 2
```
## Tilling validation

After tilling it is necessary to validate the new grid cells. `Massive PotreeConverter` has a tool called `mpc-validate-tiles`. It first compares the total number of points in the input files with the number of points in the output tiles. If they differ, the script will print the name of which input file was not tilled correctly. It uses [SQLite3](https://www.sqlite.org/index.html) to store all meta-data about the files and to perform some `group-by` and `join` operations to obtain the file names which were not tiled correctly.

```
mpc-validate-tiles -h
usage: mpc-validate-tiles [-h] -l DBLOCATION -n DBNAME -i INPUTFILESPATH -t
                          TILESPATH

optional arguments:
  -h, --help            show this help message and exit
  -l DBLOCATION, --dbLocation DBLOCATION
                        Absolute path for the SQLite3 database location
  -n DBNAME, --dbName DBNAME
                        SQLite3 database name
  -i INPUTFILESPATH, --inputFilesPath INPUTFILESPATH
                        Absolute path for the input files
  -t TILESPATH, --tilesPath TILESPATH
                        Absolute path for the tiles
```

Using the `input dir` and `output dir` parameters from `mpc-tiling` example, the call `mpc-validate-tiles` should be as follow:
```
mpc-validate-tiles -l /data/local/home/eecolidar/tmp/ -n ahn3Tiles -i /data/local/eecolidar_webdav/01_Work/ALS/Netherlands/ahn3_10_08_2018/ -t /data/local/eecolidar_webdav/01_Work/ALS/Netherlands/ahn3_10_08_2018_256x256_2km/
```
NOTE: The SQLite3 database, in this case located at `/data/local/home/eecolidar/tmp/ahn3Tiles`, is available for further data inspections and analysis.

## Lasmerge

After all the files are computed by `mpc-tiling` we still need to merge all the files for each grid cell. We use [lasmerge](https://rapidlasso.com/lastools/lasmerge/) to merge them into a single `LAS/LAZ` file. The input files are read directly from `web-dav` mounted directory, however, `lasmerge` is not able to output to a stream. Hence, the `lasmerge` output should be saved into a local `tmp` directory and then moved into `web-dav`. Here is an example for tile `tile_100_100`:

```
lasmerge -i /data/local/eecolidar_webdav/01_Work/ALS/Netherlands/ahn3_10_08_2018_256x256_2km/tile_100_100/*.LAZ -o /data/local/eecolidar/rclone/tmp/tile_100_100.LAZ ; mv /data/local/eecolidar/rclone/tmp/tile_100_100.LAZ /data/local/eecolidar_webdav/01_Work/ALS/Netherlands/ahn3_10_08_2018_256x256_2km/tile_100_100.LAZ
```
