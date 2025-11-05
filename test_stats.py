"""
Test historical stats API
"""

import os
from fubon_neo.sdk import FubonSDK

# Load env vars
username = os.getenv("FUBON_USERNAME")
password = os.getenv("FUBON_PASSWORD")
pfx_path = os.getenv("FUBON_PFX_PATH")
pfx_password = os.getenv("FUBON_PFX_PASSWORD")

if not all([username, password, pfx_path]):
    print("Missing env vars")
    exit(1)

print("Initializing SDK...")
sdk = FubonSDK()
accounts = sdk.login(username, password, pfx_path, pfx_password or "")
sdk.init_realtime()
reststock = sdk.marketdata.rest_client.stock

print("Testing historical.stats()...")

# Test 1: no args
try:
    print("1. reststock.historical.stats()")
    result = reststock.historical.stats()
    print(f"Success! {type(result)}")
    print(result)
except Exception as e:
    print(f"Error: {e}")

# Test 2: with symbol
try:
    print("2. reststock.historical.stats(symbol='0050')")
    result = reststock.historical.stats(symbol='0050')
    print(f"Success! {type(result)}")
    print(result)
except Exception as e:
    print(f"Error: {e}")

# Test 3: positional
try:
    print("3. reststock.historical.stats('0050')")
    result = reststock.historical.stats('0050')
    print(f"Success! {type(result)}")
    print(result)
except Exception as e:
    print(f"Error: {e}")

print("Available methods in historical:")
for attr in dir(reststock.historical):
    if not attr.startswith('_'):
        print(f" - {attr}")