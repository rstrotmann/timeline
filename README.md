# timeline

A package to create timeline visualizations

The imput is a simple text file. Its format follows a basic domain-specific language:

`SECTION xxx` starts a section with the caption 'xxx'
`THREAD xxx` starts a thread within a section. The thread's caption is 'xxx'

Within a thread, time points can be added, following the below syntax:
`xxx: dd-mm-yy` where 'xxx' is the caption and 'dd-mm-yy' is the date in the specified format.

time intervals can be added following this syntax:
`xxx: dd-mm-yy - dd-mm-yy` where 'xxx' is the interval's caption, and the dates to either side of the dash are the start and the end dates.

That's it.

## Installation

```bash
$ pip install timeline
```

## Usage

```bash
timeline infile.tl -t
```

## License

`timeline` was created by Rainer Strotmann. It is licensed under the terms of the MIT license.

## Credits

`timeline` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
