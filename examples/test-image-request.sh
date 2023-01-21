# Run this bash file after running any example server with port 8090 and setting breakpoints
# this will trigger the calls flow so you can inspect and debug
curl http://127.0.0.1:8090 -H "Height: 1600" -H "Width: 1200" > /dev/null