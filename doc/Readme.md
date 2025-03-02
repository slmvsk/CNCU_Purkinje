
## Getting started with NEURON

### Installation

Install python pacakge manager [uv](https://astral.sh/blog/uv).

```console
> brew install uv
```

For a working environment, create a virtual environment with `uv`.

```console
> mkdir good_job
> cd good_job
> uv venv
```

Activate the virtual environment.

```console
> source .venv/bin/activate
```

or automatically source it using [direnv](https://direnv.net/) with a `.envrc`:

```shell
if [[ -f .venv/bin/activate ]]; then
  source .venv/bin/activate
fi
```


Install [NEURON](https://nrn.readthedocs.io/en/latest/install/install_instructions.html) using `uv`.

```console
> uv pip install neuron
```

Make sure that `XQuartz` is installed.
If it is installed, `DISPLAY` environment variable should be set.

```console
❯ echo $DISPLAY
/private/tmp/com.apple.launchd.V3Qx1TFced/org.xquartz:0
```

If `DISPLAY` is empty, install `XQuartz` with the following command:

```console
> brew install --cask xquartz
```

and re-login to let the system set `DISPLAY`.


Launch NEURON GUI by:

```console
> nrngui
```

then you will see a `NEURON Main Menu` window appeared.


### Import a `.swc` 3D model

Follow the menu of: [Tools] -> [Miscellaneous] -> [Import 3D].

Click "choose a file" and choose a desired file.

"Show Points" is recommended to be unselected for a better rendering performance.


### Export a `.hoc` file

In the window of "Import3d_GUI[x]", follow [Export] -> [CellBuilder] and open a "CellBuild[x]" window.

### Open a `.hoc` file

```console
> nrngui xxx.hoc
```

Follow the menu of [Tools] -> [Distributed Mechanisms] -> [Viewers] -> [Shape Name].
