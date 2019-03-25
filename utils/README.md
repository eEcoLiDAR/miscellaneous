# Utils

## Mounting web-dav server
Since we are using large LiDAR data sets we can't copy all the data to our laptops and computers. The most efficient way to access the data is to mount our `web-dav storage` as local file system. We list here the steps on how to do it in Windows and Linux.

### Windows
To mount eEcolidar web-dav storage in Windows we can use [winfsp](https://github.com/billziss-gh/winfsp), watch [winfsp instructions](https://github.com/billziss-gh/winfsp#winfsp---windows-file-system-proxy) to understand how to do it. The url `https://webdav.grid.surfsara.nl/pnfs/grid.sara.nl/data/projects.nl/eecolidar/` is what needs to be added as `folder` in the `winfsp interface` and for login use your `web-dav` account.

If you prefer a command line approach, you can mount it as a network storage.
```
#To mount it as drive w:
net use w: https://webdav.grid.surfsara.nl/pnfs/grid.sara.nl/data/projects.nl/eecolidar/

#To unmount it
net use w: /delete
```

### Linux

In Linux we use [rclone](https://rclone.org/install/). It is a command line tool which uses `fuse` to mount different type of storages including `web-dav`. After installing `rclone` you need to configure it.
```
eecolidar:~$ rclone config
```

The following menu will appear and you should start the configuration of a new connection, i.e., `n) New remote`.
```
2018/09/07 11:21:45 NOTICE: Config file "/home/eecolidar/.config/rclone/rclone.conf" not found - using defaults
No remotes found - make a new one
n) New remote
s) Set configuration password
q) Quit config
n/s/q>
```
For this example we use `eecolidar_webdav` as the name for the connection to a remote storage, but you can pick a name at your convenience.
```
n/s/q> n
name> eecolidar_webdav
```
For `type of storage` you should pick `Webdav`, i.e., the number `23`.
```
...
20 / Pcloud
   \ "pcloud"
21 / QingCloud Object Storage
   \ "qingstor"
22 / SSH/SFTP Connection
   \ "sftp"
23 / Webdav
   \ "webdav"
24 / Yandex Disk
   \ "yandex"
25 / http Connection
   \ "http"
Storage> 23
```
For storage `url` you should enter `https://webdav.grid.surfsara.nl:2880/pnfs/grid.sara.nl/data/projects.nl/eecolidar/`;
<!--For storage `url` you should enter `https://webdav.grid.surfsara.nl/pnfs/grid.sara.nl/data/projects.nl/eecolidar/`;-->
```
Storage> 23
URL of http host to connect to
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
 1 / Connect to example.com
   \ "https://example.com"
url> https://webdav.grid.surfsara.nl:2880/pnfs/grid.sara.nl/data/projects.nl/eecolidar/
```
For the vendor you should choose `4 / Other site/service or software`.
```
url> https://webdav.grid.surfsara.nl:2880/pnfs/grid.sara.nl/data/projects.nl/eecolidar/
Name of the Webdav site/service/software you are using
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value
 1 / Nextcloud
   \ "nextcloud"
 2 / Owncloud
   \ "owncloud"
 3 / Sharepoint
   \ "sharepoint"
 4 / Other site/service or software
   \ "other"
vendor> 4
```
For log in enter your `user name`, in this example we use `eecolidar` as user name.
```
vendor> 4
User name
Enter a string value. Press Enter for the default ("").
user> eecolidar
```
For automatic login the password can be added to the login information. NOTE: The password will be encrypted and not saved as plain text in the configuration file. It is also the possible to request a `token` and use it instead of `user name` and `password` at login time.
```
user> eecolidar
Password.
y) Yes type in my own password
g) Generate random password
n) No leave this optional password blank
y/g/n> y
Enter the password:
password:
Confirm the password:
password:
Bearer token instead of user/pass (eg a Macaroon)
Enter a string value. Press Enter for the default ("").
bearer_token>
Remote config
```

After inserting the login information, rclone will ask you to confirm the information added.
<!-- prior to dcache maintenance the url was url = https://webdav.grid.surfsara.nl/pnfs/grid.sara.nl/data/projects.nl/eecolidar/ -->
```
--------------------
[eecolidar_webdav]
type = webdav
url = https://webdav.grid.surfsara.nl:2880/pnfs/grid.sara.nl/data/projects.nl/eecolidar/
vendor = other
user = eecolidar
pass = *** ENCRYPTED ***
--------------------
y) Yes this is OK
e) Edit this remote
d) Delete this remote
y/e/d> y
```

If all the information is correct you can quit `rclone config` with option `q`.
```
Name                 Type
====                 ====
eecolidar_webdav     webdav

e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q> q
eecolidar:~$
```

As the menu above shows it is possible to re-configure the setup, you just need to call again `rclone config`. Once it is configured the next step is to mount it. For this example we use the location `/data/local/eecolidar_webdav`. As rclone cache  we use `/data/local/eecolidar/rclone/tmp/`. It is the location used by rclone to cache the files used by the applications. The option `--vfs-cache-mode full` tells rclone to first download the file before it is used.
```
rclone mount eecolidar_webdav: /data/local/eecolidar_webdav/ --allow-other --vfs-cache-mode full --daemon --log-file=/data/local/eecolidar/rclone/rclone_log.out --log-level DEBUG --cache-dir /data/local/eecolidar/rclone/tmp/ --cache-db-purge --vfs-cache-max-age 20m0s --dir-cache-time 15m0s --cache-workers=6
```
When the files are used for a short period of time and many are request in simultaneously, we recommend small time values for `--vfs-cache-max-age` and `--dir-cache-time` (between two and five minutes) to avoid cache overflow, rclone hangs in such situations. If your storage has 128GB free space or more, just use the values given in the example.

To unmount you only need to make sure none of the files or directories under `/data/local/eecolidar_webdav/` are being used.
```
fusermount -u  /data/local/eecolidar_webdav/
```
