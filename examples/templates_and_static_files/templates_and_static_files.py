"""Diving into templates and static files.

Milvago uses jinja2 as a templating engine so most people
will feel right at home from the start. It also supports
serving static files like images, css and js files, but
this isn't recommended and you should be using nginx, apache
or a CDN for those purposes because that way, they wouldn't be
going through the python interpreter and will dramatically
ease the load.

In addition, here we'll mix up function and class-based
views for the sake of the example."""
import os
from milvago import Milvago, HttpMlv, HttpStaticDir, expose_web


@expose_web('/')
def index(web):
    """Let's explore the web parameter. What is it?
    Well, in essence, it's an entire instance of
    the HttpMlv class and you can access all the properties
    and methods from it. One of which, is render().
    render() the name of the html template you intend
    to use and any number of named arguments to be passed
    on to the view. In this case, the view uses a variable
    called 'name' and we set it to 'Milvago'."""
    return web.render('index.html', name="Milvago")


class SecondView(HttpMlv):
    """Now this is a class based view where we add some
    static variables but naturally those can be coming
    from a database, REST api, cache or some other source,
    it really doesn't matter."""
    __slots__ = [
        "name",
        "picture"
    ]

    def __init__(self):
        HttpMlv.__init__(self, "/intro")
        self.name = "Linus"
        self.picture = "/static/Linus.jpg"

    def get(self):
        """Much like the index function we declared
        above, we have a view and named arguments."""
        return self.render(
            'second_view.html',
            name=self.name,
            picture=self.picture
        )


class StaticFiles(HttpStaticDir):
    """And here is how we define a directory from
    which we can serve static files. You simply
    need to create a class, which extends HttpStaticDir
    and call it's constructor with two arguments:
    The first one (uri) is the mount-point,
    and the second one (dir_path) is a full path to
    the location on your disk where the files are stored."""
    def __init__(self):
        HttpStaticDir.__init__(
            self,
            '/static',
            f"{os.path.dirname(os.path.abspath(__file__))}/static"
        )


"""This is where things change: the Milvago class needs a
template_dir parameter, which is a full path to the location
where the html templates are stored. In this example, it's in
a subdirectory called 'templates, sitting right next to this script.
The Milvago class is responsible for telling all the views, function
or class-based where to look for them, so you don't need to worry
about it.'"""
milvago = Milvago(
    [
        index(),
        SecondView(),
        StaticFiles()
    ],
    debug=True,
    template_dir=f"{os.path.dirname(os.path.abspath(__file__))}/templates")
views = milvago()
