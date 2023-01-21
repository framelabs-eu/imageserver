# Run this bash file after running any example server with port 8090
# if set brekpoints this will trigger the calls flow so you can to inspect it
curl http://127.0.0.1:8090 -H "Height: 1600" -H "Width: 1200" > /dev/null