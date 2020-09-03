"""The module creates the server and starts the application
on a given host and port."""
import typing
from werkzeug.serving import run_simple
import falcon
from milvago.server.handlers import HttpMlv, API
from milvago.common.exceptions import InvalidMilvagoClassException


class Milvago:
    """The class handles the initialization of the
    application, attaching a template directory for jinja2
    and starting the server.

    Parameters
    ----------
    handlers : list
        A list of handlers of type HttpMlv.
    debug : bool
        Run the application in debug mode,
        without gunicorn.
    host : str
        Self-explanatory, on which host to respond.
    port : int
        Self-explanatory again.
    template_dir : str
        Full path to where the directory containing
        the templates."""
    __slots__ = [
        "_handler_list",
        "_app",
        "_debug",
        "_host",
        "_port",
        "_templates"
    ]

    def __init__(
            self,
            handlers: list,
            debug: bool = False,
            host: str = '0.0.0.0',
            port: int = 8000,
            template_dir: str = None
    ):
        self._handler_list = handlers
        self._app = falcon.API()
        self._debug = debug
        self._host = host
        self._port = port
        self._templates = template_dir

    def attach_handler(self, handler: HttpMlv) -> None:
        """In case a handler needs to be added before
        initializing the app.

        Parameters
        ----------
        handler : HttpMlv
            A valid http handler.

        Returns
        -------
        None

        Raises
        ------
        InvalidMilvagoClassException
            In case the handler parameter isn't an instance
            of HttpMlv."""
        if not isinstance(handler, HttpMlv):
            raise InvalidMilvagoClassException(
                f"{handler} is not an instance of "
                f"HttpMlv, but {handler.__class__.__name__}"
            )
        self._handler_list.append(handler)

    @property
    def app(self):
        """Public property returning self._app."""
        return self._app

    @property
    def host(self):
        """Public property returning self._host."""
        return self._host

    @property
    def port(self):
        """Public property returning self._port."""
        return self._port

    def __repr__(self) -> str:
        """Printing representation of the class.

        Returns
        -------
        str"""
        return f"<{self.__class__.__name__}(\n" \
               f"\thandlers = {self._handler_list},\n" \
               f"\thost = {self.host},\n" \
               f"\tport = {self.port},\n" \
               f"\tdebug = {self._debug},\n" \
               f"\ttemplate_dir = {self._templates}"

    def modfy_props(self, prop_name: str, prop_value: typing.Any) -> None:
        """For modifying properties of Milvago.app.

        Returns
        -------
        None"""
        self._app.__dict__[prop_name] = prop_value

    def __call__(self):
        """Starts the application in either development
        mode or in production through gunicorn.

        Returns
        -------
        falcon.API"""
        self._app.req_options.auto_parse_form_urlencoded = True
        for handler in self._handler_list:
            if isinstance(handler, HttpMlv) \
                    and not handler.template_loader\
                    and self._templates:
                handler.attach_templates(self._templates)
        API(
            self.app,
            self._handler_list
        )
        if self._debug:
            run_simple(
                self.host,
                self.port,
                self.app,
                use_reloader=True
            )
        else:
            return self.app
