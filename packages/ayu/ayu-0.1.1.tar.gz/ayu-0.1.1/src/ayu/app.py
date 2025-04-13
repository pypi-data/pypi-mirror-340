from pathlib import Path
from textual import work, on
from textual.app import App
from textual.reactive import reactive
from textual.events import Key
from textual.widgets import Log, Header, Footer, Collapsible, Tree
from textual.containers import Horizontal, Vertical
# from textual_slidecontainer import SlideContainer

from ayu.event_dispatcher import EventDispatcher
from ayu.utils import EventType, NodeType, run_all_tests
from ayu.widgets.navigation import TestTree
from ayu.widgets.code_preview import CodePreview
from ayu.widgets.filter import TreeFilter


class AyuApp(App):
    CSS_PATH = Path("assets/ayu.tcss")
    TOOLTIP_DELAY = 0.5

    data_test_tree: reactive[dict] = reactive({}, init=False)
    counter_total_tests: reactive[int] = reactive(0, init=False)

    def __init__(self, *args, **kwargs):
        self.dispatcher = None
        super().__init__(*args, **kwargs)

    def compose(self):
        yield Header()
        yield Footer()
        outcome_log = Log(highlight=True, id="log_outcome")
        outcome_log.border_title = "Outcome"
        report_log = Log(highlight=True, id="log_report")
        report_log.border_title = "Report"
        collection_log = Log(highlight=True, id="log_collection")
        collection_log.border_title = "Collection"
        with Horizontal():
            with Vertical():
                yield TestTree(label="Tests").data_bind(
                    filtered_data_test_tree=AyuApp.data_test_tree,
                    filtered_counter_total_tests=AyuApp.counter_total_tests,
                )
                yield TreeFilter()
            with Vertical():
                yield CodePreview()
                with Collapsible(title="Outcome", collapsed=True):
                    yield outcome_log
                with Collapsible(title="Report", collapsed=True):
                    yield report_log
                with Collapsible(title="Collection", collapsed=True):
                    yield collection_log

    async def on_load(self):
        self.start_socket()

    def on_mount(self):
        self.dispatcher.register_handler(
            event_type=EventType.OUTCOME,
            handler=lambda msg: self.update_outcome_log(msg),
        )
        self.dispatcher.register_handler(
            event_type=EventType.REPORT, handler=lambda msg: self.update_report_log(msg)
        )
        self.app.dispatcher.register_handler(
            event_type=EventType.COLLECTION,
            handler=lambda data: self.update_app_data(data),
        )

    def update_app_data(self, data):
        self.data_test_tree = data["tree"]
        self.counter_total_tests = data["meta"]["test_count"]

    @work(exclusive=True)
    async def start_socket(self):
        self.dispatcher = EventDispatcher()
        self.notify("Websocket Started", timeout=1)
        await self.dispatcher.start()

    def on_key(self, event: Key):
        if event.key == "ctrl+j":
            self.run_test()
        if event.key == "w":
            self.notify(f"{self.workers}")
        if event.key == "s":
            self.query_one(CodePreview).toggle()
            self.query_one(TreeFilter).toggle()
        if event.key == "c":
            self.query_one(TestTree).reset_test_results()
            for log in self.query(Log):
                log.clear()

    @on(Tree.NodeHighlighted)
    def update_test_preview(self, event: Tree.NodeHighlighted):
        self.query_one(CodePreview).file_path_to_preview = Path(event.node.data["path"])
        if event.node.data["type"] in [
            NodeType.FUNCTION,
            NodeType.COROUTINE,
            NodeType.CLASS,
        ]:
            self.query_one(CodePreview).test_start_line_no = event.node.data["lineno"]
        else:
            self.query_one(CodePreview).test_start_line_no = -1

    @work(thread=True)
    def run_test(self):
        run_all_tests(tests_to_run=self.query_one(TestTree).marked_tests)

    def update_outcome_log(self, msg):
        self.query_one("#log_outcome", Log).write_line(f"{msg}")

    def update_report_log(self, msg):
        self.query_one("#log_report", Log).write_line(f"{msg}")

    def watch_data_test_tree(self):
        self.query_one("#log_collection", Log).write_line(f"{self.data_test_tree}")


# https://watchfiles.helpmanual.io
