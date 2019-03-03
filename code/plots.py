

def plot_curves(
        title,
        ylim,
        xlab,
        ylab,
        plotx_1,
        ploty_1,
        plot_lab1,
        plotx_2=None,
        ploty_2=None,
        plot_lab2=None,
        fillrange_1=0,
        fillrange_2=0):
    '''
    plot_curve

    Plot up to two labelled lines with x and y axis specified
    '''
    import matplotlib.pyplot as pl

    pl.figure()
    pl.title(title)

    if ylim is not None:
        pl.ylim(ylim)

    pl.xlabel(xlab)
    pl.ylabel(ylab)

    pl.grid()

    pl.plot(plotx_1, ploty_1, 'o-', color='r', label=plot_lab1)
    if fillrange_1 > 0:
        pl.fill_between(plotx_1, ploty_1 - fillrange_1, ploty_1 + fillrange_1,
                        alpha=0.1, color='r')

    # If we are plotting a second value
    if plotx_2 is not None and ploty_2 is not None and plot_lab2 is not None:
        pl.plot(plotx_2, ploty_2, 'o-', color='b', label=plot_lab2)
        if fillrange_2 > 0:
            pl.fill_between(plotx_2, ploty_2 - fillrange_2, ploty_2 +
                            fillrange_2, alpha=0.1, color='b')

    pl.legend(loc="best")

    return pl


def plot_boxes(
        plot_data,
        title,
        xlabel,
        ylabel,
        xplot_labels=None,
        xplot_label_args=None,
        **kwargs):
    '''
    plot_boxes

    Plot single or multiple box plot using matplotlib
    '''
    import matplotlib.pyplot as pl

    fig, ax = pl.plot()
    box = ax.boxplot(plot_data, **kwargs)
    if xplot_labels is not None:
        ax.set_xticklabels(xplot_labels, **xplot_label_args)

    pl.title(title)
    pl.xlabel(xlabel)
    pl.ylabel(ylabel)

    pl.legend(loc="best")

    return pl, box
