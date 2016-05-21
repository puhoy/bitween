#from pycallgraph import PyCallGraph
#from pycallgraph.output import GraphvizOutput

def profile(filename="output.png"):
    """
    decorator to profile functions
    filename is the filename of the output image

    :param filename:
    :return:
    """
    def wrapper(func):
        graphviz = GraphvizOutput()
        graphviz.output_file = filename

        def inner(*args, **kwargs):
            with PyCallGraph(output=graphviz):
                return func(*args, **kwargs)
        return inner
    return wrapper
