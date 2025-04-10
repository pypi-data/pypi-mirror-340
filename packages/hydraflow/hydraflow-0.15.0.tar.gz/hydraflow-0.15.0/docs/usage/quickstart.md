# HydraFlow Quickstart Guide

HydraFlow seamlessly integrates MLflow (for experiment tracking)
with Hydra (for configuration management), creating a powerful
framework for machine learning experimentation.
This quickstart shows you how to get up and running with HydraFlow in minutes.

## Hydra application

The following example demonstrates how to use a Hydraflow application.

```python title="apps/quickstart.py" linenums="1"
--8<-- "apps/quickstart.py"
```

### Hydraflow's `main` decorator

[`hydraflow.main`][] starts a new MLflow run that logs the Hydra
configuration. The decorated function must have two arguments: `run` and
`cfg`. The `run` argument is the current MLflow run with type
`mlflow.entities.Run`. The `cfg` argument is the Hydra configuration
with type `omegaconf.DictConfig`. You can annotate the arguments with
`Run` and `Config` to get type checking and autocompletion in your IDE,
although the `cfg` argument is not actually an instance of `Config`
(duck typing is used).

```python
@hydraflow.main(Config)
def app(run: Run, cfg: Config) -> None:
    pass
```

## Run the application

```bash exec="on"
rm -rf mlruns outputs multirun
```

### Single-run

Run the Hydraflow application as a normal Python script.

```console exec="1" source="console"
$ python apps/quickstart.py
```

Check the MLflow CLI to view the experiment.

```console exec="1" source="console"
$ mlflow experiments search
```

The experiment name comes from the name of the Hydra job.

### Multi-run

Run the Hydraflow application with multiple configurations.

```console exec="1" source="console"
$ python apps/quickstart.py -m width=400,600 height=100,200,300
```

## Use Hydraflow API

### Iterate over run's directory

The [`hydraflow.iter_run_dirs`][] function iterates over the run
directories. The first argument is the path to the MLflow tracking root
directory (in most cases, this is `"mlruns"`).

```pycon exec="1" source="console" session="quickstart"
>>> import hydraflow
>>> for run_dir in hydraflow.iter_run_dirs("mlruns"):
...     print(run_dir)
```

Optionally, you can specify the experiment name(s) to filter the runs.

```python
>>> hydraflow.iter_run_dirs("mlruns", "quickstart")
>>> hydraflow.iter_run_dirs("mlruns", ["quickstart1", "quickstart2"])
```

### Load a run

[`Run`][hydraflow.core.run.Run] is a class that represents a *Hydraflow*
run, not an MLflow run. A `Run` instance is created by passing a
`pathlib.Path` instance that points to the run directory to the `Run`
constructor.

```pycon exec="1" source="console" session="quickstart"
>>> from hydraflow import Run
>>> run_dirs = hydraflow.iter_run_dirs("mlruns", "quickstart")
>>> run_dir = next(run_dirs)  # run_dirs is an iterator
>>> run = Run(run_dir)
>>> print(run)
>>> print(type(run))
```

You can use the [`load`][hydraflow.core.run.Run.load] class method to
load a `Run` instance, which accepts a `str` as well as `pathlib.Path`.

```pycon exec="1" source="console" session="quickstart"
>>> Run.load(str(run_dir))
>>> print(run)
```

!!! note
    The use case of `Run.load` is to load multiple `Run` instances
    from run directories as described below.


The `Run` instance has an `info` attribute that contains information
about the run.

```pycon exec="1" source="console" session="quickstart"
>>> print(run.info.run_dir)
>>> print(run.info.run_id)
>>> print(run.info.job_name)  # Hydra job name = MLflow experiment name
```

The `Run` instance has a `cfg` attribute that contains the Hydra
configuration.

```pycon exec="1" source="console" session="quickstart"
>>> print(run.cfg)
```

### Configuration type of the run

Optionally, you can specify the config type of the run using the
`Run[C]` class.

```pycon exec="1" source="console" session="quickstart"
>>> from dataclasses import dataclass
>>> @dataclass
... class Config:
...     width: int = 1024
...     height: int = 768
>>> run = Run[Config](run_dir)
>>> print(run)
>>> # autocompletion occurs below, for example, run.cfg.height
>>> # run.cfg.[TAB]
```

The `Run[C]` class is a generic class that takes a config type `C` as a
type parameter. The `run.cfg` attribute is recognized as `C` type in
IDEs, which provides autocompletion and type checking.

### Get a run's configuration

The `get` method can be used to get a run's configuration.

```pycon exec="1" source="console" session="quickstart"
>>> print(run.get("width"))
>>> print(run.get("height"))
```

### Implementation of the run

Optionally, you can specify the implementation of the run. Use the
`Run[C, I]` class to specify the implementation type. The second
argument `impl_factory` is the implementation factory, which can be a
class or a function to generate the implementation. The `impl_factory`
is called with the run's artifacts directory as the first and only
argument.

```pycon exec="1" source="console" session="quickstart"
>>> from pathlib import Path
>>> class Impl:
...     root_dir: Path
...     def __init__(self, root_dir: Path):
...         self.root_dir = root_dir
...     def __repr__(self) -> str:
...         return f"Impl({self.root_dir.stem!r})"
>>> run = Run[Config, Impl](run_dir, Impl)
>>> print(run)
```

The representation of the `Run` instance includes the implementation
type as shown above.

If you specify the implementation type, the `run.impl` attribute is
lazily initialized at the first time of the `run.impl` attribute access.
The `run.impl` attribute is recognized as `I` type in IDEs, which
provides autocompletion and type checking.

```pycon exec="1" source="console" session="quickstart"
>>> print(run.impl)
>>> print(run.impl.root_dir)
>>> # autocompletion occurs below, for example, run.impl.root_dir
>>> # run.impl.[TAB]
```

The `impl_factory` can accept two arguments: the run's artifacts
directory and the run's configuration.

```pycon exec="1" source="console" session="quickstart"
>>> from dataclasses import dataclass, field
>>> @dataclass
>>> class Size:
...     root_dir: Path = field(repr=False)
...     cfg: Config
...     size: int = field(init=False)
...     def __post_init__(self):
...         self.size = self.cfg.width * self.cfg.height
>>> run = Run[Config, Size].load(run_dir, Size)
>>> print(run)
>>> print(run.impl)
```

### Collect runs

You can collect multiple `Run` instances from run directories as a
collection of runs [`RunCollection`][hydraflow.RunCollection].

```pycon exec="1" source="console" session="quickstart"
>>> from hydraflow import RunCollection
>>> run_dirs = hydraflow.iter_run_dirs("mlruns", "quickstart")
>>> rc = Run[Config, Size].load(run_dirs, Size)
>>> print(rc)
```

In the above example, the `load` class method is called with an iterable
of run directories and the implementation type. The `load` class method
returns a `RunCollection` instance instead of a single `Run` instance.
The representation of the `RunCollection` instance includes the run
collection type and the number of runs in the collection.

### Handle a run collection

The `RunCollection` instance has a [`first`][hydraflow.RunCollection.first]
and [`last`][hydraflow.RunCollection.last] method that returns the first
and last run in the collection.

```pycon exec="1" source="console" session="quickstart"
>>> print(rc.first())
>>> print(rc.last())
```

The [`filter`][hydraflow.RunCollection.filter] method filters the runs
by the given key-value pairs.

```pycon exec="1" source="console" session="quickstart"
>>> print(rc.filter(width=400))
```

If the value is a list, the run will be included if the value is in the
list.

```pycon exec="1" source="console" session="quickstart"
>>> print(rc.filter(height=[100, 300]))
```

If the value is a tuple, the run will be included if the value is
between the tuple. The start and end of the tuple are inclusive.

```pycon exec="1" source="console" session="quickstart"
>>> print(rc.filter(height=(100, 300)))
```

The [`get`][hydraflow.RunCollection.get] method returns a single `Run`
instance with the given key-value pairs.

```pycon exec="1" source="console" session="quickstart"
>>> run = rc.get(width=(350, 450), height=(150, 250))
>>> print(run)
>>> print(run.impl)
```

The [`to_frame`][hydraflow.RunCollection.to_frame] method returns a
polars DataFrame of the run collection.

```pycon exec="1" source="console" session="quickstart"
>>> print(rc.to_frame("width", "height"))
```

The `to_frame` method can take keyword arguments to customize the
DataFrame. Each keyword argument is a callable that takes a `Run`
instance and returns a value.

```pycon exec="1" source="console" session="quickstart"
>>> print(rc.to_frame("width", size=lambda run: run.impl.size))
```

The callable can return a list.

```pycon exec="1" source="console" session="quickstart"
>>> def to_list(run: Run) -> list[int]:
...     return [2 * run.get("width"), 3 * run.get("height")]
>>> print(rc.to_frame("width", from_list=to_list))
```

The callable can also return a dictionary.

```pycon exec="1" source="console" session="quickstart"
>>> def to_dict(run: Run) -> dict[int, str]:
...     width2 = 2 * run.get("width")
...     name = f"h{run.get('height')}"
...     return {"width2": width2, "name": name}
>>> print(rc.to_frame("width", from_dict=to_dict))
```

### Group runs

The [`group_by`][hydraflow.RunCollection.group_by] method groups the
runs by the given key.

```pycon exec="1" source="console" session="quickstart"
>>> grouped = rc.group_by("width")
>>> for key, group in grouped.items():
...     print(key, group)
```

The `group_by` method can also take multiple keys.

```pycon exec="1" source="console" session="quickstart"
>>> grouped = rc.group_by("width", "height")
>>> for key, group in grouped.items():
...     print(key, group)
```

The `group_by` method can also take a callable which accepts a sequence
of runs and returns a value. In this case, the `group_by` method returns
a polars DataFrame.

```pycon exec="1" source="console" session="quickstart"
>>> df = rc.group_by("width", n=lambda runs: len(runs))
>>> print(df)
```