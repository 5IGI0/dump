#!/bin/bash
cd /home/pi/binpwnd

/bin/mv ./datas/* ./to_backup

cd ./to_backup

/bin/tar -czvf "../backups/$(date +%Y-%m-%d.tar.gz)" ./

/bin/rm *