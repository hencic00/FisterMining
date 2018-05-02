#!/usr/bin/python
import http.client

conn = http.client.HTTPSConnection("min-api.cryptocompare.com")
# conn.request("GET","/data/pricehistorical?fsym=ETH&tsyms=BTC,USD,EUR&ts=1452680400")
conn.request("GET", "/data/price?fsym=ETH&tsyms=BTC,USD,EUR")
response = conn.getresponse()

print(response.read())
