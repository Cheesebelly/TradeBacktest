# Trade Logger

## Description
Trade Logger is a Python application that allows users to log and analyze their trading activities. The application provides a graphical user interface (GUI) to add trading pairs, log trades, view trades, and visualize statistics. The statistics include win/loss ratios, confluence win/loss, map color win/loss, and bias followed vs. not followed.

## Features
- Add trading pairs
- Log trades with details such as result, confluences, bias followed, and map color
- View all trades for a selected pair
- Visualize statistics for all trades or specific pairs
- Reset all data
- Refresh the application

## Requirements
- Python 3.x
- matplotlib library
- tkinter library (comes with Python standard library)

## Installation

### Download and Install Python:
1. Go to the [Python website](https://www.python.org/) and download the latest version of Python.
2. Run the installer and make sure to check the box that says "Add Python to PATH".
3. Follow the installation instructions.

### Download the Repository:
1. Click on the green "Code" button on the top right of the repository page.
2. Select "Download ZIP".
3. Extract the downloaded ZIP file to a folder on your computer.

### Install Required Libraries:
Open a command prompt or terminal. Navigate to the folder where you extracted the ZIP file. Run the following command to install the required libraries:

bash
```pip install matplotlib```
Run the Application:
In the same command prompt or terminal, run the following command:

bash:
```python TradeData.py```


Usage
- Add Pair: Click on "Add Pair" to add a new trading pair.
- Log Trade: Select a pair from the dropdown, fill in the trade details, and click "Add Trade".
- View Trades: Click on "View Trades" to view all trades for the selected pair.
- View Statistics: Select a pair from the statistics dropdown and click "Show Statistics" to visualize the statistics.
- Reset Data: Click on "Reset Data" to clear all data.
- Refresh: Click on "Refresh" to restart the application.
