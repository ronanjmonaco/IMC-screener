#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

try:
    import streamlit as st
    print("✅ Streamlit imported successfully")
except ImportError as e:
    print(f"❌ Streamlit import failed: {e}")

try:
    import yfinance as yf
    print("✅ yfinance imported successfully")
except ImportError as e:
    print(f"❌ yfinance import failed: {e}")

try:
    import pandas as pd
    print("✅ pandas imported successfully")
except ImportError as e:
    print(f"❌ pandas import failed: {e}")

try:
    import numpy as np
    print("✅ numpy imported successfully")
except ImportError as e:
    print(f"❌ numpy import failed: {e}")

try:
    import plotly.graph_objects as go
    print("✅ plotly.graph_objects imported successfully")
except ImportError as e:
    print(f"❌ plotly.graph_objects import failed: {e}")

try:
    import plotly.express as px
    print("✅ plotly.express imported successfully")
except ImportError as e:
    print(f"❌ plotly.express import failed: {e}")

try:
    from scipy import stats
    print("✅ scipy.stats imported successfully")
except ImportError as e:
    print(f"❌ scipy.stats import failed: {e}")

print("\n🎉 All imports completed!")
