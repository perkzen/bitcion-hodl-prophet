import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_values(df: pd.DataFrame, x, y, output_file: str) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(df[x], df[y])

    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f'{y} vs {x}')
    plt.grid(True)

    plt.savefig(output_file, bbox_inches='tight')
    plt.close()


def plot_predictions(df: pd.DataFrame, output_file: str) -> None:
    plt.figure(figsize=(12, 8))
    plt.plot(df['Date'], df["Actual"], label='Actual')
    plt.plot(df['Date'], df['Predicted'], label='Predicted')

    plt.xlabel("Date")
    plt.ylabel("Close price ($)")
    plt.legend()

    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
