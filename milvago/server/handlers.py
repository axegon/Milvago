"""The module contains everything that is needed to
create handlers for the Milvago server."""
import logging
import falcon
import jinja2
from rich.console import Console
from rich.table import Table
from milvago.common.exceptions import InvalidMediaType


LOGGER = logging.getLogger('Milvago')


class HttpMlv:
    """Really really basic HTTP server based on the falcon framework.

        Parameters
        ----------
        route : str
            The URI."""
    __slots__ = [
        "__route__",
        "_status",
        "_headers",
        "_req",
        "_resp",
        "_uri_data",
        "_template_loader",
        "get",
        "post",
        "put",
        "delete",
        "head"
    ]

    def __init__(self, route):
        self.__route__ = route
        self._status = falcon.HTTP_200
        self._headers = {}
        self._uri_data = {}
        self._req = None
        self._resp = None
        self._template_loader = None

    def __repr__(self):
        """Printing representation of the class.

        Returns
        -------
        str"""
        return f"<HttpMlv(\n" \
               f"\t__route__= {self.__route__},\n" \
               f"\tstatus = {self.status},\n" \
               f"\theaders = {self.headers},\n" \
               f"\turi_data = {self.uri_data},\n" \
               f"\tstatus = {self.status}\n)>"

    def __getattr__(self, name):
        """Acts as a self-contained wrapper for all the on_*
        methods available in falcon.
        Parameters
        ----------
        name : str
            The function which has been called"""

        def wrapper(*args, **kwargs):
            self._process(*args, **kwargs)

        return wrapper

    def attach_templates(self, template_dir):
        """In the best case scenario this should not be needed
        to develop anything and should only be used if a handler
        needs to render templates from a different directory than
        the default one. Otherwise the Milvago class should take
        care of that."""
        loader = jinja2.FileSystemLoader(
            searchpath=template_dir
        )
        self._template_loader = jinja2.Environment(loader=loader)

    def set_status(self, code):
        """Set the response code of the request.
        Parameters
        ----------
        code : int
            Response code, calling the falcon.HTTP_<code>
        Returns
        -------
        HttpWeb"""
        self._status = getattr(falcon, f"HTTP_{code}")
        return self

    def set_headers(self, **kwargs):
        """Sets the headers in the response.
        Parameters
        ----------
        kwargs : dict
            List all headers as key-value pairs."""
        self._headers.update(kwargs)
        return self

    def _set_request(self, req, resp):
        """Internal method, filling in all the class properties.
        Parameters
        ----------
        req : falcon.Request
            falcon.Request instance.
        resp : falcon.Response
            falcon.Response instance
        Returns
        -------
        HttpWeb"""
        self._req = req
        self._resp = resp
        return self

    @property
    def template_loader(self):
        """For quick access to self._template_loader"""
        return self._template_loader

    @property
    def request(self):
        """For quick access to self._req"""
        return self._req

    @property
    def status(self):
        """For quick access to self._status"""
        return self._status

    @property
    def headers(self):
        """For quick access to self._headers"""
        return self._headers

    @property
    def response(self):
        """For quick access to self._resp"""
        return self._resp

    @property
    def uri(self):
        """For consistency's sake."""
        return self.__route__

    @property
    def uri_data(self) -> dict:
        """In case the uri is composed of named
        arguments, this method will return them as
        a dictionary. For example:
        '/a/{field1}/{field2}' accessed
        via '/a/param1/param2 would retrun:
        {'field1': 'param1', 'field2': 'param2'}

        Returns
        -------
        dict"""
        return self._uri_data

    @property
    def _content_types(self) -> dict:
        """A dict containing all the supported
        content-types.

        Returns
        -------
        dict"""
        return {
            "json": falcon.MEDIA_JSON,
            "msgpack": falcon.MEDIA_MSGPACK,
            "yml": falcon.MEDIA_YAML,
            "xml": falcon.MEDIA_XML,
            "html": falcon.MEDIA_HTML,
            "js": falcon.MEDIA_JS,
            "text": falcon.MEDIA_TEXT,
            "jpg": falcon.MEDIA_JPEG,
            "png": falcon.MEDIA_PNG,
            "gif": falcon.MEDIA_GIF,
        }

    def _get_status(self):
        """Returns the status that has been previously set."""
        return self._status

    def render(self, template_file, **kwargs) -> str:
        """For rendering a template.

        Parameters
        ----------
        template_file : str
            Relative path to the template
            with respect to self._template_loader.
        **kwargs : dict
            Named arguments for the template.

        Returns
        -------
        str"""
        self.set_content_type("html")
        template = self._template_loader.get_template(template_file)
        return template.render(**kwargs)

    def set_content_type(self, content_type: str) -> None:
        if content_type not in self._content_types:
            raise InvalidMediaType(
                f"Invalid media type, you can use one of "
                f"{', '.join(self._content_types.keys())}")
        self._resp.content_type = self._content_types[content_type]

    def set_custom_content_type(self, content_type: str) -> None:
        """In case a non-standard content-type must be used.

        Parameters
        ----------
        content_type : str
            Self-explanatory.

        Returns
        -------
        None"""
        self.response.content_type = content_type

    def _process(self, req, resp, **kwargs):
        """Self contained method for all GET, POST, PUT, DELETE, HEAD,
        etc. methods
        Parameters
        ----------
        req : falcon.Request
            falcon.Request instance.
        resp : falcon.Response
            falcon.Response instance
        Returns
        -------
        HttpWeb"""
        self._uri_data = kwargs
        self._set_request(req, resp)
        resp.status = self._get_status()
        response_method = getattr(self, req.method.lower())
        if response_method.__class__.__name__ == 'function':
            resp.body = response_method(self)
        else:
            resp.body = response_method()


class HttpStaticDir:
    """Wrapper class for directories containing static files,
    ie. css, js, images, fonts, etc.
    IMPORTANT: This is for development purposes only.
    Parameters
    ----------
    uri : str
        The path where the directory should be mounted.
    dir_path : str
        Full path to the directory containing the static
        files."""
    __slots__ = [
        "_uri",
        "_dir_path"
    ]

    def __init__(self, uri: str, dir_path: str):
        self._dir_path = dir_path
        self._uri = uri

    def __repr__(self):
        """Printing representation of the class.

        Returns
        -------
        str"""
        return f"<HttpStaticDir(\n" \
               f"\tfile_path = {self.file_path}," \
               f"\turi = {self.uri}\n)>"

    @property
    def file_path(self) -> str:
        """Getter for the directory path"""
        return self._dir_path

    @property
    def uri(self) -> str:
        """Getter for the URI where the directory
        has been mounted."""
        return self._uri


class API:
    """Fast initialization of the API.
    Parameters
    ----------
    falconapi : falcon.API
        falcon.API instance.
    classes : list
        list of initialized classes inheriting the HttpWeb class
        or HttpStaticDir in development mode."""

    __slots__ = [
        "_mountpoints"
    ]

    def __init__(self, falcon_api, classes):
        self._mountpoints = []
        for handler in classes:
            if isinstance(handler, HttpMlv):
                LOGGER.info(
                    f"Mounting handler {handler.uri} "
                    f"of {str(handler)}"
                )
                falcon_api.add_route(handler.uri, handler)
            elif isinstance(handler, HttpStaticDir):
                LOGGER.info(
                    f"Mounting STATIC handler "
                    f"{handler.file_path} at {handler.uri}")
                LOGGER.warning(
                    f"Mounting static handles isn't advisable "
                    f"in production environments. A web server "
                    f"is a more suitable solution as the "
                    f"interpreter would be slower at reading files."
                )
                falcon_api.add_static_route(
                    handler.uri,
                    handler.file_path
                )
            else:
                LOGGER.error(f"Cannot use class of type "
                             f"{handler.__class__.__name__}")
                continue
            self._append_mountpoint(handler.uri, str(handler))
        self._list_all()

    def __repr__(self):
        """Printing representation of the class.

        Returns
        -------
        str"""
        return f"<API(\n" \
               f"\tmountpoints = {self._mountpoints}\n)>"

    def _append_mountpoint(self, route: str, class_name: str) -> None:
        """Adds all routes and classes to a property.
        For debugging purposes only.
        Parameters
        ----------
        route : str
            Self-explanatory, URI.
        class_name : str
            the __str__ representation of the class
            instance."""
        self._mountpoints.append([route, class_name])

    def _list_all(self):
        """Simply lists all the handlers, will be called
        when the application is initialized."""
        self._mountpoints.sort(key=lambda x: x[0])
        LOGGER.info(self._mountpoints)
        console = Console()
        table = Table(
            show_header=True,
            header_style="bold green"
        )
        table.add_column("Mountpoints")
        table.add_column("Class")
        for mountpoint in self._mountpoints:
            table.add_row(
                *mountpoint
            )
        console.log(table)


def expose_static(route: str, data_dir: str):
    """The simplest way to attach a static directory
    in the application.

    Parameters
    ----------
    route : str
        Route as to where the directory
        should be mounted, i.e. '/images'.
    data_dir : str
        Path to where the actual files are
        located.

    Returns
    -------
    HttpStaticDir"""
    return HttpStaticDir(route, data_dir)


def expose_web(route: str, methods: str = 'get'):
    """Exposes a function to the web-server
    Parameters
    ----------
    route : str
        The URI.
    methods : str
        Comma-separated methods, i.e. 'get,post,put".
    Returns
    -------
    HttpWeb"""

    def decorator(function):
        def wrapper():
            handler = HttpMlv(route)
            for method in methods.split(','):
                setattr(handler, method.strip(), function)
            return handler
        return wrapper
    return decorator
