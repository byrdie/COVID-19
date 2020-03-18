import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.animation
import covid.data

__all__ = ['plot_histogram']


def plot_histogram():

    confirmed = covid.data.read(covid.data.confirmed_filename)

    def calc_hist(index: int):

        sl = [slice(None)] * confirmed.data.ndim
        sl[covid.data.axis.time] = index

        return np.histogram2d(
            y=confirmed.latitudes,
            x=confirmed.longitudes,
            weights=confirmed.data[sl],
            bins=(100, 50),

        )

    hist, x, y = calc_hist(0)

    fig, ax = plt.subplots(figsize=(12, 6))

    img = ax.imshow(
        X=hist.T,
        norm=matplotlib.colors.SymLogNorm(1),
        vmax=np.percentile(confirmed.data, 100),
        vmin=0,
        extent=[x[0], x[~0], y[0], y[~0]],
        origin='lower',
    )

    fig.colorbar(img, fraction=0.02)

    def update(index: int):

        new_hist, _, _ = calc_hist(index)

        ax.set_title(confirmed.dates[index])
        img.set_data(new_hist.T)

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=confirmed.data.shape[covid.data.axis.time])

    with open('histogram.html', 'w') as f:
        f.write(ani.to_jshtml(fps=10))

    plt.show()


def test_plot_histogram():

    plot_histogram()
