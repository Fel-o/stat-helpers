import matplotlib.pyplot as plt
import seaborn as sns


def prop_plot(x, data, value, hue1=None, hue2=None, **kwargs):
    """Create a plot with the size of the proportion of the target value.
    Subgroups can be specified by hue1, hue2.
    """
    hues = [hue for hue in [hue1, hue2] if hue]
    groups = data.groupby([*hues, x]).size()
    if hue1:
        prop_groups = groups.groupby(hues).apply(lambda x: 100 * x / float(x.sum()))
        prop_groups = prop_groups[prop_groups.index.get_level_values(x) == value]
        return (prop_groups
                .unstack(x)
                .rename(columns={value:f"{x} proportion [%]"})
                .reset_index()
                .pipe((sns.barplot, "data"), x=hue1, y=f"{x} proportion [%]", hue=hue2, **kwargs))
    return sns.barplot(x=[value], y=[(100 * groups / float(groups.sum()))[value]], **kwargs)


def plot_std(ax, x, y, std, marker_width, **kwargs):
    """Plot std marker at specified x and y. Return top y of marker."""
    x2 = x - marker_width * 0.5
    x3 = x + marker_width * 0.5
    y2 = y + std
    ax.plot([x, x, x2, x3], [y, y2, y2, y2], **kwargs)
    return y2

def add_std_to_bar(ax, bar, std, rel_marker_width=0.5, **kwargs):
    """Plot std marker on bar. Return top y of marker."""
    barwidth = bar.get_width()
    x = bar.get_x() + barwidth * 0.5
    y = bar.get_height()
    marker_width = barwidth * rel_marker_width
    return plot_std(ax, x, y, std, marker_width=marker_width, **kwargs)

def plot_p_between_patches(ax, patches, p, height=0.8, marker_height=0.05, label_marker_space=0.01):
    # sort bars by x_value and split into chunks of pairs
    assert len(patches) == 2
    patches = sorted(patches, key=lambda p: p.get_x())

    axis_to_data = ax.transAxes + ax.transData.inverted()
    data_to_axis = axis_to_data.inverted()
    x1 = data_to_axis.transform([patches[0].get_x() + 0.5 * patches[0].get_width(), 0])[0]
    x2 = data_to_axis.transform([patches[1].get_x() + 0.5 * patches[1].get_width(), 0])[0]
    y1 = height
    y2 = height + marker_height

    label_y = y2 + label_marker_space

    ax.plot([x1,x1,x2,x2], [y1, y2, y2, y1], lw=1, c="k", transform=ax.transAxes)
    ax.text((x1 + x2) / 2, label_y, p, ha='center', va='bottom', transform=ax.transAxes)


def patchesborder(ax, lw=1, color="k"):
    """Add border arount ax patches"""
    plt.setp(ax.patches, linewidth=lw, edgecolor=color)


def change_barwidth(ax, width):
    """Change width of ax patches."""
    for patch in ax.patches:
        current_width = patch.get_width()
        diff = current_width - width
        patch.set_width(width)  # change the bar width
        patch.set_x(patch.get_x() + diff * .5)  # recenter the bar
