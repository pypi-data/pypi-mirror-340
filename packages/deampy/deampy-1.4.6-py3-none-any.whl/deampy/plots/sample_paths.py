import matplotlib.pyplot as plt

from deampy.plots.plot_support import output_figure
from deampy.sample_path import *


def plot_sample_path(sample_path,
                     title=None, x_label=None, y_label=None,
                     x_range=None, y_range=None,
                     figure_size=None, file_name=None,
                     legend=None, color=None, transparency=0.75, connect='step'):
    """
    plot a sample path
    :param sample_path: a sample path
    :param title: (string) title of the figure
    :param x_label: (string) x-axis label
    :param y_label: (string) y-axis label
    :param x_range: (list) [x_min, x_max]
    :param y_range: (list) [y_min, y_max]
    :param figure_size: (tuple) figure size
    :param file_name: (string) filename to save the histogram as (e.g. 'fig.png')
    :param legend: (string) the legend
    :param color: (string) for example: 'b' blue 'g' green 'r' red 'c' cyan 'm' magenta 'y' yellow 'k' black
    :param transparency: (float) between 0 and 1 for the transparency of curves
    :param connect: (string) set to 'step' to produce a step graph and to 'line' to produce a line graph
    """

    if not (isinstance(sample_path, IncidenceSamplePath) or isinstance(sample_path, PrevalenceSamplePath)):
        raise ValueError(
            'sample_path should be an instance of PrevalenceSamplePath or PrevalencePathBatchUpdate.')

    fig, ax = plt.subplots(figsize=figure_size)

    # add a sample path to this ax
    add_sample_path_to_ax(sample_path=sample_path,
                          ax=ax,
                          color=color, transparency=transparency,
                          legend=legend,
                          connect=connect,
                          x_label=x_label, y_label=y_label, title=title)
    ax.set_ylim(bottom=0)  # the minimum has to be set after plotting the values

    if x_range is not None:
        ax.set_xlim(x_range)
    else:
        if isinstance(sample_path, PrevalenceSamplePath):
            ax.set_xlim(left=0)
        elif isinstance(sample_path, IncidenceSamplePath):
            ax.set_xlim(left=0.5)

    if y_range is not None:
        ax.set_ylim(y_range)

    # output figure
    output_figure(fig, file_name)


def plot_sample_paths(sample_paths,
                      title=None, x_label=None, y_label=None,
                      x_range=None, y_range=None,
                      figure_size=None, file_name=None,
                      legends=None, legend_fontsize=8, transparency=1,
                      color_codes=None,
                      common_color_code=None, connect='step'):
    """ graphs multiple sample paths
    :param sample_paths: a list of sample paths
    :param title: (string) title of the figure
    :param x_label: (string) x-axis label
    :param y_label: (string) y-axis label
    :param x_range: (list) [x_min, x_max]
    :param y_range: (list) [y_min, y_max]
    :param figure_size: (tuple) figure size
    :param file_name: (string) filename to save the histogram as (e.g. 'fig.png')
    :param legends: (list) of strings for legend
    :param legend_fontsize: (float) legend font size
    :param transparency: (float) 0.0 transparent through 1.0 opaque
    :param color_codes: (list) of color code for sample paths
    :param common_color_code: (string) color code if all sample paths should have the same color
        'b'	blue 'g' green 'r' red 'c' cyan 'm' magenta 'y' yellow 'k' black
    :param connect: (string) set to 'step' to produce an step graph and to 'line' to produce a line graph
    """

    if len(sample_paths) == 1:
        raise ValueError('Only one sample path is provided. Use graph_sample_path instead.')

    fig, ax = plt.subplots(figsize=figure_size)
    ax.set_title(title)  # title
    ax.set_xlabel(x_label)  # x-axis label
    ax.set_ylabel(y_label)  # y-axis label
    if x_range is not None:
        ax.set_xlim(x_range)
    if y_range is not None:
        ax.set_ylim(y_range)

    # add all sample paths
    add_sample_paths_to_ax(sample_paths=sample_paths,
                           ax=ax,
                           color_codes=color_codes,
                           common_color_code=common_color_code,
                           transparency=transparency,
                           connect=connect)

    # add legend if provided
    if legends is not None:
        if common_color_code is None:
            ax.legend(legends, fontsize=legend_fontsize)
        else:
            ax.legend([legends], fontsize=legend_fontsize)

    # set the minimum of y-axis to zero
    if y_range is None:
        ax.set_ylim(bottom=0)  # the minimum has to be set after plotting the values

    # output figure
    output_figure(fig, file_name)


def plot_sets_of_sample_paths(sets_of_sample_paths,
                              title=None, x_label=None, y_label=None,
                              x_range=None, y_range=None,
                              figure_size=None, file_name=None,
                              legends=None, transparency=1, color_codes=None, connect='step'):
    """ graphs multiple sample paths
    :param sets_of_sample_paths: (list) of list of sample paths
    :param title: (string) title of the figure
    :param x_label: (string) x-axis label
    :param y_label: (string) y-axis label
    :param x_range: (list) [x_min, x_max]
    :param y_range: (list) [y_min, y_max]
    :param figure_size: (tuple) figure size
    :param file_name: (string) filename to to save the histogram as (e.g. 'fig.png')
    :param legends: (list of strings) for legends
    :param transparency: float (0.0 transparent through 1.0 opaque)
    :param color_codes: (list of strings) color code of sample path sets
            e.g. 'b' blue 'g' green 'r' red 'c' cyan 'm' magenta 'y' yellow 'k' black
    :param connect: (string) set to 'step' to produce an step graph and to 'line' to produce a line graph
    """

    if len(sets_of_sample_paths) == 1:
        raise ValueError('Only one set of sample paths is provided. Use plot_sample_paths instead.')

    fig, ax = plt.subplots(figsize=figure_size)
    if x_range is not None:
        ax.set_xlim(x_range)
    if y_range is not None:
        ax.set_ylim(y_range)

    # add all sample paths
    add_sets_of_sample_paths_to_ax(sets_of_sample_paths=sets_of_sample_paths,
                                   ax=ax,
                                   color_codes=color_codes,
                                   legends=legends,
                                   transparency=transparency,
                                   connect=connect)

    ax.set_title(title)  # title
    ax.set_xlabel(x_label)  # x-axis label
    ax.set_ylabel(y_label)  # y-axis label
    # # set the minimum of y-axis to zero
    # ax.set_ylim(bottom=0)  # the minimum has to be set after plotting the values
    # output figure
    output_figure(fig, file_name)


def add_sample_path_to_ax(sample_path, ax, legend=None, color=None, transparency=1.0, connect='step',
                          title=None, x_label=None, y_label=None,
                          x_range=None, y_range=None, legend_fontsize=8
                          ):

    # x and y values
    if isinstance(sample_path, PrevalenceSamplePath):
        x_values = sample_path.get_times()
    elif isinstance(sample_path, IncidenceSamplePath):
        x_values = sample_path.get_period_numbers()

    y_values = sample_path.get_values()

    # plot the sample path
    if connect == 'step':
        ax.step(x=x_values, y=y_values, where='post', color=color,
                linewidth=0.75, label=legend, alpha=transparency)
    else:
        ax.plot(x_values, y_values, color=color,
                linewidth=0.75, label=legend, alpha=transparency)

    if title is not None:
        ax.set_title(title)
    if x_label is not None:
        ax.set_xlabel(x_label)
    if y_label is not None:
        ax.set_ylabel(y_label)
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)

    # add legend if provided
    if legend is not None:
        ax.legend(fontsize=legend_fontsize)


def add_sample_paths_to_ax(sample_paths, ax, color_codes=None, common_color_code=None, transparency=0.5,
                           connect='step', legends=None, legend_fontsize=8,
                           title=None, x_label=None, y_label=None,
                           x_range=None, y_range=None):

    # add every path
    for i, path in enumerate(sample_paths):
        if color_codes is not None:
            color = color_codes[i]
        elif common_color_code is not None:
            color = common_color_code
        else:
            color = None

        legend = None if legends is None else legends[i]

        add_sample_path_to_ax(sample_path=path,
                              ax=ax,
                              color=color,
                              legend=legend,
                              legend_fontsize=legend_fontsize,
                              transparency=transparency,
                              connect=connect)

    if title is not None:
        ax.set_title(title)
    if x_label is not None:
        ax.set_xlabel(x_label)
    if y_label is not None:
        ax.set_ylabel(y_label)
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)


def add_sets_of_sample_paths_to_ax(
        sets_of_sample_paths, ax, color_codes, legends, transparency, connect='step',
        title=None, x_label=None, y_label=None,
        x_range=None, y_range=None):

    # add every path
    for i, sample_paths in enumerate(sets_of_sample_paths):
        for j, path in enumerate(sample_paths):
            if j == 0:
                legend = legends[i]
            else:
                legend = None
            if color_codes is None:
                this_color_code = None
            else:
                this_color_code = color_codes[i]
            add_sample_path_to_ax(sample_path=path,
                                  ax=ax,
                                  color=this_color_code,
                                  legend=legend,
                                  transparency=transparency,
                                  connect=connect)

    if title is not None:
        ax.set_title(title)
    if x_label is not None:
        ax.set_xlabel(x_label)
    if y_label is not None:
        ax.set_ylabel(y_label)
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)