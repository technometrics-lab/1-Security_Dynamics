from pathlib import PurePath, Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle

class GraphicBase:
    """Standard template graphic. It uses LaTeX.

    :param suptitle: Suptitle name of the graphic.
    :type suptitle: str

    :param title: Title name of the graphic.
    :type title: str

    :param xlabel: X-axis name.
    :type xlabel: str

    :param ylabel: Y-axis name.
    :type ylabel: str

    :param date_format: use or not the date formatter on the X-axis.
    :type date_format: bool

    :param figsize: size of the figure.
    :type figsize: (int, int)

    :param fontsize: font size.
    :type fontsize: int"""
    def __init__(self, suptitle, title, xlabel, ylabel, date_format=True,
                 figsize=(30, 15), fontsize=30):
        # Use LaTeX render
        plt.rcParams.update({'text.usetex' : True,
                            'font.family' : 'geometry'})
                            # 'text.latex.preamble': r'\usepackage{siunitx}'})
        # Create the figure
        self.fig, self.ax = plt.subplots(figsize=figsize)

        # Mid point of left and right x-positions
        mid = (self.fig.subplotpars.right + self.fig.subplotpars.left)/2

        # Print title and suptitle
        self.fig.suptitle(suptitle,
                          x=mid,
                          weight='bold',
                          fontsize=fontsize*1.5)
        self.ax.set_title(title,
                          fontsize=fontsize,
                          weight='bold')

        # Activate the grid
        plt.grid(linestyle='dashed',
                 alpha = 0.5)

        # Format the ticks for years
        if date_format:
            years = mdates.YearLocator()   # every year
            years_fmt = mdates.DateFormatter('%Y')

            self.ax.xaxis.set_major_locator(years)
            self.ax.xaxis.set_major_formatter(years_fmt)
        self.ax.xaxis.set_tick_params(rotation=45,
                                      labelsize=fontsize)
        self.ax.yaxis.set_tick_params(labelsize=fontsize)

        # Print axis name
        plt.xlabel(xlabel,
                   fontsize=fontsize,
                   weight='bold')
        plt.ylabel(ylabel,
                   fontsize=fontsize,
                   weight='bold')

        # List which contain legend rectangle
        self.__legend_text = {'Plot': [],
                              'Text': []}


    def add_text_legend(self, text, plot=None) -> None:
        """Adds `text` into the legend box, the `text` can be associated to a
        `plot`. The method :meth:`show_legend` must be call at the end of all
        :meth:`add_text_legend` calling.

        :param text: Text to add into the legend box.
        :type text: str

        :param plot: Return a `plt.plot()`, to associate `text` to this plot.
        """
        if plot is None :
            # Artist object
            plot = Rectangle((0, 0),
                             1,
                             1,
                             fc='w',
                             fill=False,
                             edgecolor='none',
                             linewidth=0)

        self.__legend_text['Plot'].append(plot)
        self.__legend_text['Text'].append(text)

    def show_legend(self, size=15) -> None:
        """Prints the legend box.

        :param size: size of the legend font.
        :type size: int"""
        plt.legend(self.__legend_text['Plot'],
                   self.__legend_text['Text'],
                   loc='upper left',
                   fontsize=size)

    def show_graph(self) -> None:
        """Shows the graphic and close the figure too."""
        plt.show()
        plt.close(self.fig)

    def save_graph(self, result_folder, file_name) -> None:
        """Saves the graphic into `result_folder`, create the path if it
        doesn't exist. Close the figure too.

        :param result_folder: Path to the directory where the file will be
            saved.
        :type result_folder: str or :class:`pathlib.PurePath`

        :param file_name: Name of the saved file.
        :type file_name: str"""
        result_folder = PurePath(result_folder)
        Path(result_folder).mkdir(parents = True, exist_ok = True)
        plt.savefig(result_folder.joinpath(file_name + '.pdf'),
                    format='pdf',
                    transparent=True,
                    dpi=1000,
                    bbox_inches='tight')
        plt.close(self.fig)
