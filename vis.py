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
