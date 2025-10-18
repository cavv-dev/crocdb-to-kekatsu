# crocdb-to-kekatsu
Crocdb database porting to Kekatsu app

This project makes use of the [Crocdb API](https://github.com/cavv-dev/crocdb-api) to create an updated working database for [Kekatsu](https://github.com/cavv-dev/Kekatsu-DS).

## Setup
### Nintendo DS(i)
- Follow the [Quick setup instructions](https://github.com/cavv-dev/Kekatsu-DS?tab=readme-ov-file#quick-setup-instructions) to install and configure Kekatsu
- Add these lines to `databases.txt` based on your ROMs selection preference:
#### DSi and DSiWare
```
Crocdb (dsi)=https://crocdb.net/kekatsu/dsi
```
#### DS, DSi and DSiWare
```
Crocdb (nds, dsi)=https://crocdb.net/kekatsu/ds
```
#### DS
```
Crocdb (nds)=https://crocdb.net/kekatsu/nds
```

Smaller selection = Faster loading time
