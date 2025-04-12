"""
A module for building HTML/XML documents using context managers, with
improved organization and a sum-type approach for mutation events.
"""

import random
import logging
import pathlib
import functools
import xml.etree.ElementTree as ET
import re

from io import StringIO
from typing import (
    Any,
    List,
    Union,
    Literal,
    Callable,
    Optional,
)
from contextlib import contextmanager, asynccontextmanager
from contextvars import ContextVar

import anyio
from anyio.abc import TaskGroup
from anyio.streams.memory import (
    MemoryObjectSendStream,
    MemoryObjectReceiveStream,
)

from fastapi import (
    FastAPI,
    Request,
    Response,
    WebSocket,
    WebSocketDisconnect,
)
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

logger = logging.getLogger(__name__)


def mint() -> str:
    """Generate a concise unique ID using base62 encoding (A-Z, a-z, 0-9)."""
    # Use 48 bits of randomness encoded in base62
    # This gives us ~281 trillion unique IDs
    n = random.getrandbits(48)
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    result = ""
    while n:
        n, remainder = divmod(n, 62)
        result = chars[remainder] + result
    # Pad to ensure consistent length
    return result.zfill(8)


# -----------------------------------------------------------------------------
# 1. Mutation Event Sum-Type
# -----------------------------------------------------------------------------


class OpenTagEvent(BaseModel):
    target: str  # parent element ID
    id: str  # new element ID
    tag: str  # HTML tag name
    attrs: dict[str, str]  # initial attributes
    type: Literal["openTag"] = "openTag"


class CloseTagEvent(BaseModel):
    target: str  # element ID to close
    type: Literal["closeTag"] = "closeTag"


class SetAttributeEvent(BaseModel):
    target: str  # element ID
    name: str  # attribute name
    value: str  # attribute value
    type: Literal["setAttribute"] = "setAttribute"


class SetTextEvent(BaseModel):
    target: str  # element ID
    value: str  # new text
    type: Literal["setText"] = "setText"


class ClearEvent(BaseModel):
    target: str  # element ID
    type: Literal["clear"] = "clear"


# A discriminated union of the possible events
MutationEvent = Union[
    OpenTagEvent, CloseTagEvent, SetAttributeEvent, SetTextEvent, ClearEvent
]


class Transaction(BaseModel):
    """Holds a list of mutations which can be sent in a single atomic update."""

    mutations: list[MutationEvent]
    type: Literal["update"] = "update"


# -----------------------------------------------------------------------------
# 2. Fragment: The root of a Tagflow context
# -----------------------------------------------------------------------------


class Fragment:
    """
    Represents a collection of HTML/XML elements that can be rendered
    as a complete document or XML fragment.
    """

    live_session: Optional["Session"]

    def __init__(self):
        self.element = ET.Element("fragment")
        self.live_session = None

    def __str__(self) -> str:
        return self.to_html()

    @property
    def live(self) -> bool:
        """Whether this fragment is connected to a live session."""
        return self.live_session is not None

    def to_html(self, compact: bool = True) -> str:
        """
        Renders the fragment as HTML. By default, it concatenates the
        top-level elements without indentation or line breaks.
        """
        if len(self.element) == 0:
            return ""
        elif len(self.element) > 1 and not compact:
            raise ValueError("Pretty printing requires exactly one root element")

        if compact:
            return "".join(
                ET.tostring(child, encoding="unicode", method="html")
                for child in self.element
            )

        # For pretty printing, we can rely on BeautifulSoup or your preferred tool
        from bs4 import BeautifulSoup

        element = self.element[0] if len(self.element) == 1 else self.element
        rough_string = ET.tostring(element, encoding="unicode", method="html")
        soup = BeautifulSoup(rough_string, "html.parser")
        return soup.prettify()

    def to_xml(self) -> str:
        """
        Renders the fragment as XML. If there's more than one top-level
        element, we raise an error, since XML requires a single root.
        """
        if len(self.element) > 1:
            raise ValueError("Fragment has more than one root element.")

        tree = ET.ElementTree(self.element[0])
        s = StringIO()
        tree.write(s, encoding="unicode", method="xml")
        return s.getvalue()


# -----------------------------------------------------------------------------
# 3. Context Variables and Transaction Recording
# -----------------------------------------------------------------------------

# The current node in the document to which we are appending content
node: ContextVar[ET.Element] = ContextVar("node")

# The current document fragment (root)
root_fragment: ContextVar[Fragment] = ContextVar("root")

# The current transaction, if any
tx: ContextVar[Optional[Transaction]] = ContextVar("tx", default=None)


@contextmanager
def enter(element: ET.Element):
    """
    Context manager for entering an element.
    """
    token = node.set(element)
    try:
        yield element
    finally:
        node.reset(token)


def _get_or_create_id(element: ET.Element) -> str:
    """
    Get or create a unique 'id' attribute for an element. If the root
    document is in 'live' mode, we must ensure elements have IDs so
    they can be tracked for incremental updates.
    """
    current_id = element.attrib.get("id")

    if not current_id and root_fragment.get().live:
        new_id = mint()
        element.attrib["id"] = new_id
        return new_id
    return current_id or ""


def record_mutation(event: MutationEvent):
    """
    Records a mutation if there's an active transaction. The transaction
    is then responsible for bundling these changes and sending them to
    the client via WebSocket (if in live mode).
    """
    transaction = tx.get()
    if transaction is not None:
        transaction.mutations.append(event)


# -----------------------------------------------------------------------------
# 4. Public API Context Managers
# -----------------------------------------------------------------------------


@contextmanager
def document():
    """
    Creates a new document context for building HTML/XML content. The
    returned value is a Fragment, which can be rendered to HTML or XML.
    """
    doc = Fragment()
    token_root = root_fragment.set(doc)
    token_node = node.set(doc.element)
    try:
        yield doc
    finally:
        root_fragment.reset(token_root)
        node.reset(token_node)


# -----------------------------------------------------------------------------
# 5. Core Tag Building
# -----------------------------------------------------------------------------


def attr_name_to_xml(name: str) -> str:
    """
    Convert Pythonic attribute names to valid HTML/XML attribute names.
    If 'classes' or 'class_' is passed in, that maps to the 'class' attribute.
    Otherwise, replace underscores between word characters with hyphens.
    """
    if name == "classes" or name == "class_":
        return "class"
    return re.sub(r"(\w)_(\w)", r"\1-\2", name)


# Type for class names that can be arbitrarily nested lists of strings
ClassValue = Union[str, None, List["ClassValue"]]

# Type for any HTML attribute value
AttrValue = Union[str, int, float, bool, ClassValue]


def attr_value_to_str(value: AttrValue, attr_name: str) -> str:
    """Convert an attribute value to its string representation for HTML output."""
    if value is True:
        return ""
    if isinstance(value, (str, list)):
        return strs(value)
    if isinstance(value, (int, float)):
        return str(value)
    raise TypeError(
        f"Attribute values must be strings, numbers, booleans, or lists. "
        f"Got {type(value)} for attribute '{attr_name}'"
    )


def strs(value: Union[str, ClassValue]) -> str:
    """
    Helper to convert a string or nested list of strings to a single space-
    separated string. Handles arbitrarily nested lists of strings.
    """
    if isinstance(value, str):
        return value
    elif isinstance(value, list):
        return " ".join(strs(v) for v in value if v)
    return ""


class HTMLTagBuilder:
    """
    Provides a convenient API for creating HTML elements:
      with tag.div(class="container"):
          ...
    or:
      with tag("div", id="something"):
          ...
    """

    def __call__(
        self,
        tagname: str,
        *klasses: ClassValue,
        **kwargs: AttrValue,
    ):
        """
        Creates a new HTML/XML element with the given tag name and
        attributes. Returns a context manager for adding child elements.
        """
        # Convert kwargs to element attributes
        attrs = {}
        for k, v in kwargs.items():
            if v is None or v is False:
                # skip falsey attributes
                continue
            xml_name = attr_name_to_xml(k)
            attrs[xml_name] = attr_value_to_str(v, k)

        # Now merge any klasses with the class attribute if present
        if klasses:
            class_attr = attrs.get("class")
            class_values = list(klasses)
            if class_attr:
                class_values.append(class_attr)
            attrs["class"] = strs(class_values)

        # Create the element
        element = ET.Element(tagname, attrib=attrs)

        # If the document is live, ensure we have an ID
        if root_fragment.get().live and "id" not in attrs:
            _get_or_create_id(element)

        # Append to parent
        parent = node.get()
        parent.append(element)

        # Record the open tag mutation
        record_mutation(
            OpenTagEvent(
                target=_get_or_create_id(parent),
                id=_get_or_create_id(element),
                tag=tagname,
                attrs=attrs,
            )
        )

        @contextmanager
        def context():
            token = node.set(element)
            try:
                yield element
            finally:
                node.reset(token)
                # Record the close tag mutation when the context exits
                record_mutation(CloseTagEvent(target=_get_or_create_id(element)))

        return context()

    def __getattr__(self, name: str) -> Callable[..., Any]:
        """
        Fallback for dot-access style creation:
            tag.div(id="test")  -> tag("div", id="test")
        """
        return lambda *args, **kw: self.__call__(name, *args, **kw)


tag = HTMLTagBuilder()


def tag_decorator(tag_name: str, *klasses: ClassValue, **kwargs: AttrValue):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs2):
            with tag(tag_name, *klasses, **kwargs):
                return func(*args, **kwargs2)

        return wrapper

    return decorator


class HTMLDecorators:
    """
    Provides a convenient API for creating HTML elements as decorators.
    Usage: @html.div(class="container") or @html("div", class="container")
    """

    def __getattr__(self, name: str) -> Callable[..., Any]:
        return lambda *args, **kwargs: tag_decorator(name, *args, **kwargs)

    def __call__(
        self, name: str, *klasses: ClassValue, **kwargs: AttrValue
    ) -> Callable[[Any], Any]:
        return tag_decorator(name, *klasses, **kwargs)


html = HTMLDecorators()


# -----------------------------------------------------------------------------
# 6. Convenience Functions
# -----------------------------------------------------------------------------


def text(content: str):
    """
    Appends text to the current element. If the current element already
    has children, the text is appended to the tail of the last child.
    """
    current_el = node.get()
    if len(current_el) > 0:
        last_child = current_el[-1]
        old_tail = last_child.tail or ""
        new_tail = old_tail + content
        last_child.tail = new_tail

        record_mutation(
            SetTextEvent(
                target=_get_or_create_id(last_child),
                value=new_tail,
            )
        )
    else:
        old_text = current_el.text or ""
        new_text = old_text + content
        current_el.text = new_text

        record_mutation(
            SetTextEvent(
                target=_get_or_create_id(current_el),
                value=new_text,
            )
        )


def attr(name: str, value: AttrValue):
    """
    Sets or removes an attribute on the current element. If `value`
    is None or False, the attribute is removed. If `value` is True,
    the empty string is used.
    """
    current_el = node.get()
    xml_name = attr_name_to_xml(name)

    if value is None or value is False:
        if xml_name in current_el.attrib:
            current_el.attrib.pop(xml_name)
    elif value is True:
        current_el.set(xml_name, "")
    else:
        current_el.set(xml_name, str(value))

    # Record the mutation
    current_val = current_el.get(xml_name)
    if current_val is not None:
        record_mutation(
            SetAttributeEvent(
                target=_get_or_create_id(current_el),
                name=xml_name,
                value=current_val,
            )
        )


def classes(*names: ClassValue):
    """
    Appends the given class names to the current element's 'class' attribute.
    Handles arbitrarily nested lists of strings.
    """
    el = node.get()
    current_classes = el.get("class", "").strip()
    if current_classes and names:
        current_classes += " "
    new_value = current_classes + strs(list(names))
    el.set("class", new_value)

    record_mutation(
        SetAttributeEvent(
            target=_get_or_create_id(el),
            name="class",
            value=new_value,
        )
    )


def dataset(data: dict[str, str]):
    """
    Sets data-* attributes from a dict. E.g. dataset({"foo": "bar"})
    sets the attribute data-foo="bar".
    """
    for k, v in data.items():
        attr(f"data-{k}", v)


def clear():
    """
    Removes all children of the current element. This also records a
    clear mutation for live updates.
    """
    current_el = node.get()
    for child in current_el:
        current_el.remove(child)
    current_el.text = None
    current_el.tail = None
    record_mutation(ClearEvent(target=_get_or_create_id(current_el)))


# -----------------------------------------------------------------------------
# 7. Rendering Helper
# -----------------------------------------------------------------------------


def document_html() -> str:
    """
    Returns the entire document as an HTML string, prefixed by the
    doctype declaration.
    """
    doc = root_fragment.get()
    if not doc:
        return "<!doctype html><html><body>Error: No root document</body></html>"
    return f"<!doctype html>\n{doc.to_html()}"


# -----------------------------------------------------------------------------
# 8. FastAPI Response Classes
# -----------------------------------------------------------------------------


class TagResponse(HTMLResponse):
    """
    A FastAPI-compatible response class that captures the Tagflow
    document context and renders it as HTML.
    """

    def render(self, content: Optional[str] = None) -> bytes:
        doc = root_fragment.get()
        if doc is not None:
            return document_html().encode("utf-8")
        else:
            # If not in a Tagflow context, fallback
            return super().render(content or "")


class XMLResponse(Response):
    """
    A FastAPI-compatible response class that captures the Tagflow
    document context and renders it as XML.
    """

    media_type = "application/xml"

    def render(self, content: Any) -> bytes:
        doc = root_fragment.get()
        if doc is not None:
            return doc.to_xml().encode("utf-8")
        else:
            return str(content).encode("utf-8")


# -----------------------------------------------------------------------------
# 9. Document Middleware
# -----------------------------------------------------------------------------


class DocumentMiddleware(BaseHTTPMiddleware):
    """
    Middleware that sets up a fresh document context for each request.

    Usage in FastAPI:
        app = FastAPI()
        app.add_middleware(DocumentMiddleware)
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        with document():
            response = await call_next(request)
            return response


# -----------------------------------------------------------------------------
# 10. Live Document Support
# -----------------------------------------------------------------------------


class Session(BaseModel):
    """
    A live session that manages WebSocket connections and updates.
    Each session is intended to coordinate a single "live" view.
    """

    id: str
    taskgroup: TaskGroup
    send_channel: MemoryObjectSendStream[Transaction]
    transaction_receiver: MemoryObjectReceiveStream[Transaction]

    class Config:
        arbitrary_types_allowed = True

    @asynccontextmanager
    async def transition(self):
        """
        Context manager for atomic document updates. Mutations in this
        context are collected into a Transaction and sent when the
        block exits. If no mutations are recorded, the transaction is not
        sent.
        """
        transaction = Transaction(mutations=[])
        token = tx.set(transaction)
        try:
            yield
            if transaction.mutations:
                await self.send_channel.send(transaction)
        finally:
            tx.reset(token)

    def spawn(self, fn: Callable[..., Any]) -> None:
        """
        Spawn a new task in the session's task group. This is helpful
        if your UI needs to do background polling, timers, etc.
        """
        self.taskgroup.start_soon(fn)

    def cancel(self):
        """
        Cancel the session. This will close the WebSocket connection and
        stop the task group.
        """
        self.taskgroup.cancel_scope.cancel()

    def client_tag(self):
        """
        Insert a live document client element with this session's ID.
        This element will automatically connect to the server and apply
        mutations to the DOM as they are received.
        """
        with tag("tagflow-client", session_id=self.id):
            pass

    async def run(self):
        """
        Main loop for the session.
        """
        async with self.send_channel:
            while True:
                await anyio.sleep(1)


class FutureValue:
    """
    A small wrapper around a memory channel used to produce/consume a single
    value exactly once. This can be used to return a Session from a background
    task.
    """

    def __init__(self):
        self.send_channel, self.receive_channel = anyio.create_memory_object_stream(1)

    async def provide(self, value: Any):
        await self.send_channel.send(value)
        await self.send_channel.aclose()

    async def consume(self) -> Any:
        return await self.receive_channel.receive()


@asynccontextmanager
async def future():
    """
    Produces a context manager that yields a FutureValue. The context manager
    handles the lifetime of the channels.
    """
    f = FutureValue()
    try:
        yield f
    finally:
        # Ensure channels get closed
        await f.send_channel.aclose()
        await f.receive_channel.aclose()


class Live:
    """
    Manages live document sessions and their WebSocket connections.
    To use:
       live = Live()
       async with live.run(app):
           # The server is now set up to handle WS at `/.well-known/tagflow/live.ws`
    """

    def __init__(self):
        self._taskgroup: Optional[TaskGroup] = None
        self._sessions: dict[str, Session] = {}

    @asynccontextmanager
    async def run(self, app: FastAPI):
        """
        Start the live document manager, hooking the default
        WebSocket route to handle live updates.
        """
        async with anyio.create_task_group() as taskgroup:
            self._taskgroup = taskgroup

            # Mount static files directory
            static_dir = pathlib.Path(__file__).parent / "static"
            app.mount(
                "/.well-known/tagflow/static",
                StaticFiles(directory=str(static_dir)),
                name="tagflow_static",
            )

            # Register the default live WS endpoint
            app.websocket("/.well-known/tagflow/live.ws")(self.handle_websocket)
            yield

            # Exiting the context cancels the task group

    async def session(self) -> Session:
        """
        Creates a new live session. The session's background task is managed
        by the Live manager's task group. The calling code can then yield within
        a Tagflow context to produce dynamic content.
        """
        if not self._taskgroup:
            raise RuntimeError("Live.run() must be called before creating a session.")

        # Get the current root fragment
        doc = root_fragment.get()

        # Create a session ID, memory channels, and a future
        session_id = mint()
        send_channel, receive_channel = anyio.create_memory_object_stream(8)

        async with future() as session_future:

            async def session_task():
                async with anyio.create_task_group() as session_taskgroup:
                    sess = Session(
                        id=session_id,
                        taskgroup=session_taskgroup,
                        send_channel=send_channel,
                        transaction_receiver=receive_channel,
                    )
                    self._sessions[session_id] = sess
                    await session_future.provide(sess)
                    try:
                        logger.info("Session %s running", session_id)
                        await sess.run()
                    finally:
                        logger.info("Session %s disconnected", session_id)
                        del self._sessions[session_id]

            # Start the session task in the manager's task group
            self._taskgroup.start_soon(session_task)

            # The consumer side: wait to get the Session from the future
            sess = await session_future.consume()

            # Set the live session on the document
            doc.live_session = sess

            return sess

    def script_tag(self) -> None:
        """
        Insert the live document JavaScript code and custom element into the current element.
        """
        with tag.script(src="/.well-known/tagflow/static/tagflow.js"):
            pass

    def client_tag(self, session_id: str):
        """
        Insert a live document client element with a given session ID.
        This element will automatically connect to the server and apply
        mutations to the DOM as they are received.
        """
        with tag("tagflow-client", session_id=session_id):
            pass

    async def handle_websocket(self, websocket: WebSocket):
        """
        Default WebSocket route for receiving live updates from the browser
        and sending out mutation events.
        """
        await websocket.accept()

        # For simplicity, assume the first message from the client is the session ID
        hello = await websocket.receive_json()
        session_id = hello.get("id")
        if session_id not in self._sessions:
            await websocket.close(code=1008)
            return

        session = self._sessions[session_id]
        # We'll clone the session's recv channel to read from it locally

        async def recv_loop():
            while True:
                try:
                    await websocket.receive_json()
                except WebSocketDisconnect:
                    session.taskgroup.cancel_scope.cancel()
                    return

        async def send_loop():
            txs = session.transaction_receiver.clone()
            async with txs:
                # Continuously push updates from the session to the browser
                while True:
                    try:
                        msg = await txs.receive()
                        await websocket.send_json(msg.model_dump())
                    except anyio.EndOfStream:
                        break

        async with anyio.create_task_group() as nursery:
            nursery.start_soon(recv_loop)
            nursery.start_soon(send_loop)


async def spawn(fn: Callable[..., Any]) -> None:
    """
    Spawn a new task in the current document's live session task group.
    This is helpful if your UI needs to do background polling, timers, etc.
    """
    doc = root_fragment.get()
    if not doc.live_session:
        raise RuntimeError("Cannot spawn task: document is not live")
    doc.live_session.spawn(fn)


@asynccontextmanager
async def transition():
    """
    Context manager for atomic document updates. Mutations in this
    context are collected into a Transaction and sent when the
    block exits.
    """
    doc = root_fragment.get()
    if not doc.live_session:
        raise RuntimeError("Cannot transition: document is not live")
    async with doc.live_session.transition():
        yield
