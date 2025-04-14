from logging import Logger
from pathlib import Path
from eo4eu_base_utils.typing import Self, Callable, Iterable, Any

from ..drivers import Driver, LocalDriver
from .interface import DataPath, Data, Action, ActionContext
from .actions import (
    Do,
    Log,
    Raw,
    Join,
    Apply,
    Attach,
    Source,
    Filter,
    Switch,
    Branch,
    FileOp,
    Collect,
    TrimNames,
    StatefulAction,
    move_put_func,
    basic_dst_func,
    basic_put_func,
    parent_dst_func,
    unpack_put_func,
)


class Pipeline(Action):
    def __init__(
        self,
        logger: Logger|None = None,
        summary: Logger|None = None,
        selector: Callable[[Path],Any]|None = None,
        context: ActionContext|None = None,
    ):
        if all([
            context is None,
            logger is not None,
            summary is not None
        ]):
            context = ActionContext(
                logger = logger,
                summary = summary,
                selector = selector
            )

        self._context = context
        self._actions = []

    def execute(self, input: Data, context: ActionContext) -> Data:
        if self._context is None and context is not None:
            self._context = context

        result = input.copy()
        for action in self._actions:
            try:
                result = action.execute(result, self._context)
            except Exception as e:
                self._context.summary.error(f"Unexpected pipeline error: {e}")
                return result
        return result

    def exec(self) -> Data:
        return self.execute(Data.empty(), self._context)

    def then(self, action: Action, context: ActionContext|None = None) -> Self:
        if context is None:
            self._actions.append(action)
        else:
            self._actions.append(StatefulAction(action, context))
        return self

    def then_if(
        self,
        predicate: bool,
        action: Action,
        context: ActionContext|None = None
    ) -> Self:
        if predicate:
            return self.then(action = action, context = context)
        else:
            return self

    def apply(self, func: Callable[[Data],Data], context: ActionContext|None = None) -> Self:
        return self.then(
            action = Apply(func = func),
            context = context
        )

    def attach(
        self,
        context: ActionContext|None = None,
        **attrs: Callable[[DataPath],Any],
    ) -> Self:
        return self.then(
            action = Attach(attrs = attrs),
            context = context
        )

    def with_path_selector(
        self,
        selector: Callable[[Path],Any],
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = Attach({"SELECTOR": lambda data_path: selector(data_path.path())}),
            context = context
        )

    def do(self, func: Callable[[],None], context: ActionContext|None = None) -> Self:
        return self.then(
            action = Do(func = func),
            context = context
        )

    def raw(self, paths: Data|list[DataPath|Path|dict], context: ActionContext|None = None) -> Self:
        data = None
        if isinstance(paths, list):
            data_paths = []
            for path in paths:
                if isinstance(path, DataPath):
                    data_paths.append(path)
                elif isinstance(path, Path):
                    data_paths.append(DataPath(
                        driver = LocalDriver(Path.cwd()),
                        cwdir = Path.cwd(),
                        path = path,
                        name = path,
                    ))
                elif "path" in path:
                    data_paths.append(DataPath(
                        driver = path.get("driver", LocalDriver(Path.cwd())),
                        cwdir = Path(path.get("cwdir", Path.cwd())),
                        path = Path(path["path"]),
                        name = Path(path.get("name", path["path"])),
                    ))
            data = Data.ref(data_paths)
        elif isinstance(paths, Data):
            data = paths
        else:
            raise ValueError(f"Variable must be \"Data\" or a list of DataPaths; "
                             f"Is \"{paths.__class__.__name__}\" instead.")

        return self.then(
            action = Raw(data = data),
            context = context
        )


    def source(
        self,
        driver: Driver,
        cwdir: str|Path = "",
        context: ActionContext|None = None,
        **kwargs
    ) -> Self:
        return self.then(
            action = Source(driver = driver, cwdir = Path(cwdir), **kwargs),
            context = context
        )

    def join(
        self,
        actions: Iterable[Action],
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = Join(actions = actions),
            context = context
        )

    def filter(
        self,
        *predicates: Any,
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = Filter(predicates = list(predicates)),
            context = context
        )

    def switch(
        self,
        cases: dict[Any,Action]|list[tuple[Any,Action]],
        otherwise: Action|None = None,
        context: ActionContext|None = None
    ) -> Self:
        case_tuples = cases
        if isinstance(cases, dict):
            case_tuples = [
                (predicate, action) for predicate, action in cases.items()
            ]
        if otherwise is not None:
            case_tuples.append((lambda path: True, otherwise))

        return self.then(
            action = Switch(case_tuples),
            context = context
        )

    def branch(
        self,
        predicate: Any,
        action: Action,
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = Branch(predicate, action),
            context = context
        )

    def collect(
        self,
        name: str,
        consume: bool = False,
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = Collect(name = name, consume = consume),
            context = context
        )

    def consume(
        self,
        name: str,
        context: ActionContext|None = None
    ) -> Self:
        return self.collect(name = name, consume = True, context = context)

    def log(
        self,
        msg: str|Callable[[Logger,Data],None],
        summary: bool = False,
        context: ActionContext|None = None
    ):
        log_func = msg
        if isinstance(msg, str):
            log_func = lambda logger, data: logger.info(msg)
        return self.then(
            action = Log(log_func = log_func, summary = summary),
            context = context
        )

    def announce(
        self,
        msg: str|Callable[[Logger,Data],None],
        context: ActionContext|None = None
    ) -> Self:
        return self.log(msg = msg, summary = True, context = context)

    def trim_names(self, context: ActionContext|None = None):
        return self.then(action = TrimNames(), context = context)

    def put(
        self,
        driver: Driver,
        outdir: str|Path = "",
        context: ActionContext|None = None,
        **kwargs
    ) -> Self:
        return self.then(
            action = FileOp(
                driver = driver,
                outdir = Path(outdir),
                names = ("Put", "Putting", "Put"),
                dst_func = basic_dst_func,
                put_func = basic_put_func,
                **kwargs
            ),
            context = context
        )

    def upload(
        self,
        driver: Driver,
        outdir: str|Path = "",
        context: ActionContext|None = None,
        **kwargs
    ) -> Self:
        return self.then(
            action = FileOp(
                driver = driver,
                outdir = Path(outdir),
                names = ("Upload", "Uploading", "Uploaded"),
                dst_func = basic_dst_func,
                put_func = basic_put_func,
                **kwargs
            ),
            context = context
        )

    def download(
        self,
        outdir: str|Path = "",
        context: ActionContext|None = None,
        **kwargs
    ) -> Self:
        return self.then(
            action = FileOp(
                driver = LocalDriver(Path.cwd()),
                outdir = Path(outdir),
                names = ("Download", "Downloading", "Downloaded"),
                dst_func = basic_dst_func,
                put_func = basic_put_func,
                **kwargs
            ),
            context = context
        )

    def move(
        self,
        outdir: str|Path = "",
        context: ActionContext|None = None,
        **kwargs
    ) -> Self:
        return self.then(
            action = FileOp(
                driver = None,
                outdir = Path(outdir),
                names = ("Move", "Moving", "Moved"),
                dst_func = basic_dst_func,
                put_func = move_put_func,
                **kwargs
            ),
            context = context
        )

    def unpack(
        self,
        outdir: str|Path = "",
        spew: bool = False,  # if false, unpack in dst; if true, in dst.parent
        context: ActionContext|None = None,
        **kwargs
    ) -> Self:
        dst_func = parent_dst_func if spew else basic_dst_func
        return self.then(
            action = FileOp(
                driver = None,
                outdir = Path(outdir),
                names = ("Unpack", "Unpacking", "Unpacked"),
                dst_func = dst_func,
                put_func = unpack_put_func,
                reselect = True,
                **kwargs
            ),
            context = context
        )


def then() -> Pipeline:
    return Pipeline()
