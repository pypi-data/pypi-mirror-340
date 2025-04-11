A CLI tool to calculate common technical indicators for stock price. Sources the data from Yahoo finance API for the input ticker, period, chooses appropriate parameters for indicators and saves the
added indicators to a CSV file path.

```
What's New:
    - v1.0.0: Upgrade to polars library to support concurrent data processing,
                lazy computations  and support for both CPU and GPU engines. 
    
    - v1.1.0: Added support for asynchronous handling of I/O bound tasks and downloading
              (done by yfinance backend).

    - v1.2.0: Added support for configuration files and downsampling.
```

## Templates
1) **Indicators JSON Config:**
    Enter the values you want to overide for whichever period you are scraping. Each integer value is a certain number of timeframe periods so if your timeframe is "1wk" for the "ytd" period then entering 20 would mean a 20 weeks window. Entering all values is not necessary. The values ommitted will be replaced by default values in this template:
```
    {
        "sma_window": {
            "ytd": 20,"1y": 20,"2y": 20,"5y": 50,"10y": 200,"max": 200
        },
        "ema_window": {
            "ytd": 20,"1y": 20,"2y": 20,"5y": 50,"10y": 200,"max": 200
        },
        "macd_short": {
            "ytd": 12,"1y": 12,"2y": 12,"5y": 12,"10y": 26,"max": 26
        },
        "macd_long": {
            "ytd": 26,"1y": 26,"2y": 26,"5y": 26,"10y": 50,"max": 50
        },
        "macd_signal": {
            "ytd": 9,"1y": 9,"2y": 9,"5y": 9,"10y": 18,"max": 18
        },
        "rsi_window": {
            "ytd": 14,"1y": 14,"2y": 14,"5y": 21,"10y": 30,"max": 30
        },
        "bb_window": {
            "ytd": 20,"1y": 20,"2y": 20,"5y": 50,"10y": 100,"max": 100
        },
        "roc_window": {
            "ytd": 10,"1y": 10,"2y": 10,"5y": 20,"10y": 90,"max": 90
        },
        "atr_window": {
            "ytd": 14,"1y": 14,"2y": 14,"5y": 20,"10y": 50,"max": 50
        },
        "stochastic_window": {
            "ytd": 14,"1y": 14,"2y": 14,"5y": 21,"10y": 30,"max": 30
        }
    }
```

2) **Timeframe Config:**
    Enter the timeframe you would like to choose for each period. Entering a timeframe for each period you mention is necessary if you pass a JSON configuration.
```
    {
        "ytd": "1d",
        "1y": "1d",
        "2y": "1wk",
        "5y": "1mo",
        "10y": "3mo",
        "max": "3mo"
    }
```

Parameters:
- Required:
  1) ticker: ticker of the listed security on Yahoo finance
- Optional:
  1) period (-p, --period; default: 5y): Period of the stock data. One of ["ytd", "1y", "2y", "5y", "max"]
  2) timeframe (-t, --timeframe; default: daily): Time frame of stock data. Can be a string (e.g., "daily", "1d", "1wk") or a JSON file path.
  3) output path (-o, --output): File name for saving the output. If a TXT file is provided, each line is treated as a distinct output file name.
  4) format (-f, --format; default: csv): Output format. One of ["csv", "parquet", "json", "xlsx", "avro"]
  5) directory (-d, --dir): Directory to save the output file.
  6) config JSON file (-c, --config_json): Path to a JSON file for indicator configurations.
  7) engine (-e, --engine; default: cpu): Computation engine to use. One of ["cpu", "gpu"]

Installation:

    pip install indicators-cli

## How to Use

Install the tool:
    pip install indicators

Run the CLI tool:
    indicators TICKER [OPTIONS]

Examples:

    indicators AAPL -p 5y -t 1d -f csv -e cpu -o indicators.csv

    indicators AAPL MSFT NVDA -t 1wk -f parquet -e gpu

    indicators ticker.txt -t timeframe.json -c config.json -f json -e gpu -o outputs.txt

For help:
    indicators --help

## Interpretation

Here are the explanations and interpretations of each of the technical indicators added

1. Moving Averages (MA)

    Simple Moving Average (sma): This is the average of the stock’s closing prices over a specific period (e.g., 20 days). It smoothens out price data to help identify the direction of the trend. A higher SMA generally indicates a longer-term trend.

    Exponential Moving Average (ema): This is similar to SMA but gives more weight to recent prices, making it more responsive to recent price changes. EMAs are useful for identifying short-term trends and can be combined with SMAs to detect trend reversals.

Interpretation:

    When a short-term MA (like a 20-day EMA) crosses above a long-term MA (like a 50-day SMA), it’s often a bullish signal, indicating an upward trend.
    Conversely, when a short-term MA crosses below a long-term MA, it’s considered bearish.

2. Moving Average Convergence Divergence (macd)

    MACD is the difference between a short-term EMA (usually 12-day) and a long-term EMA (usually 26-day). It’s accompanied by a signal line (9-day EMA of the MACD), and their crossover points are used to identify buy or sell signals.
    MACD Histogram: The difference between the MACD line and the signal line, showing the strength of the trend.

Interpretation:

    When the MACD line crosses above the signal line, it’s a bullish signal (suggesting a potential buy).
    When the MACD line crosses below the signal line, it’s a bearish signal (suggesting a potential sell).
    A growing MACD histogram indicates increasing momentum, while a shrinking histogram suggests weakening momentum.

3. Relative Strength Index (rsi)

    RSI is a momentum oscillator that measures the speed and change of price movements on a scale from 0 to 100.
    Typically, values above 70 suggest the stock is overbought (price may decline), while values below 30 indicate the stock is oversold (price may increase).

Interpretation:

    RSI helps identify overbought and oversold conditions. If RSI goes above 70, the stock might be overvalued, which can signal a pullback. Below 30, the stock might be undervalued, signaling a potential buying opportunity.
    RSI divergences (when price moves in the opposite direction of RSI) can indicate a trend reversal.

4. Bollinger Bands (bb_upper/bb_lower)

    Bollinger Bands consist of a middle band (usually a 20-day SMA) and two outer bands, set at two standard deviations above and below the SMA. The bands expand and contract based on price volatility.

Interpretation:

    When prices touch or move outside the bands, they indicate high volatility and potential trend continuation or reversal. For example, if the price touches the upper band, it could be overbought, and if it touches the lower band, it could be oversold.
    Squeeze: When the bands contract significantly, it indicates low volatility and often precedes a sharp price move in either direction.

5. Average True Range (atr)

    ATR measures volatility by calculating the average range between high and low prices over a given period. Higher ATR values indicate higher volatility.

Interpretation:

    ATR does not indicate trend direction but rather the strength of price movements. High ATR values suggest high volatility and potential trend changes, while low ATR values indicate a stable trend or consolidation phase.
    ATR can be used as a trailing stop-loss: if a stock’s ATR is high, setting a wider stop-loss might be necessary to avoid premature exits.

6. Volume

    Volume is the number of shares traded over a certain period. Volume can validate trends: for example, a price move accompanied by high volume is generally more significant and likely to continue than a move with low volume.

Interpretation:

    High volume often accompanies strong moves, such as breakouts or breakdowns, and indicates increased trader interest.
    Low volume can indicate a lack of conviction in a price move, potentially signaling a reversal or a period of consolidation.

7. On-Balance Volume (obv)

    OBV accumulates volume based on the price movement: it adds volume on up days and subtracts volume on down days. This helps measure buying and selling pressure.

Interpretation:

    Rising OBV indicates accumulation (more buying pressure), which often supports upward price moves.
    Falling OBV suggests distribution (more selling pressure), supporting potential downward price moves.
    Divergences between OBV and price can indicate potential reversals.

8. Rate of Change (roc)

    ROC calculates the percentage change in price over a given time period. It’s used to measure the momentum of a stock’s price movement.

Interpretation:

    Positive ROC indicates upward momentum, while negative ROC shows downward momentum.
    Extreme high or low ROC values could indicate overbought or oversold conditions, respectively.
    ROC is also useful for identifying trend reversals when it diverges from the stock price.

9. Stochastic Oscillator (%K and %D)

    This indicator compares the current price to its range over a set period (typically 14 days). It has two lines, %K and %D, and fluctuates between 0 and 100.

Interpretation:

    Like RSI, a value above 80 suggests overbought conditions, while a value below 20 suggests oversold conditions.
    When the %K line crosses above the %D line in the oversold region (below 20), it’s a potential buy signal. Conversely, when it crosses below the %D line in the overbought region (above 80), it’s a potential sell signal.
    Divergences between price and the Stochastic Oscillator can indicate potential trend reversals.

## Build and Publish

The package is automatically built and published to PyPI when a git tag starting with "v" (e.g., v1.1.0) is pushed. This process is managed by the GitHub Actions workflow located at:
    .github/workflows/workflow.yaml
