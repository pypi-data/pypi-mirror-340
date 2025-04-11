# PalDaQue - PalaestrAI Database Query

This is a small command line tool to get most out of your palaestrAI experiment store.

## Installation

If you're new to Python and/or palaestrAI, have a look at the [Classic ARL Playground](https://gitlab.com/arl2/classic-arl-playground), which contains basic instructions to get a working version of [palaestrAI](https://docs.palaestr.ai/) and a virtual environment.

You can install it from [PyPi](https://pypi.org/) with

```bash
pip install paldaque
```

## Usage

So, you have conducted an experiment (or more) with palaestrAI but don't know how to access the results?
Here we go!

First, lets get an overview of all the experiments in the database:

```bash
paldaque experiment
```

As you might know, each experiment can have one or more runs. 
Lets get all the runs in the database:

```bash
paldaque experiment-run
```

If you already know that you want to look only at the runs of a specific experiment (and you know the experiment ID from the previous command, say it is `1`) you can add the `--experiment-id` (short `-e`) option:

```bash
paldaque experiment-run -e 1
```

Okay, now we know the experiment run ID (say `1`), then lets have a look at all the instances with the `--experiment-run-id` (short `-r`) option:

```bash
paldaque experiment-run-instance -r 1
```

This will give you all the repeated executions of that run (which is the definition of a run instance btw).
We will select one instance (say `1` for the sake of "tradition") and have a look at all the phases with the `--experiment-run-instances` (short `-i`) option:

```bash
paldaque experiment-run-phase -i 1
```

You may recognize the pattern: now we have all the phase IDs of our instance of interest and select one of them (you guess which one, right?) with the `--experiment-run-phases` (short `-p`) option.
Now it will get interesting since we will look at the actual results.
Hrr hrr hrr.

```bash
paldaque muscle-action -p 1
```

Okay. 
But why are there no sensor readings and so on?
Try it out and you know why with the `--full-console-output` (short `-f`) option:

```bash
paldaque muscle-action -p 1 -f
```

Will give you the full output.
My terminal is not wide enough to display everything, but may yours is.

For everyone else, you can export the results to csv with the `--csv` (short `-c`) option:

```bash
paldaque muscle-action -p 1 -c results.csv
```

Now you have them in a csv file. 
Yay!

## Tweaks

### Getting help

Using the `--help` command will give you hints on all possible options for the commands, e.g.,

```bash
paldaque --help
paldaque muscle-action --help
```

### Filtering the results

Maybe you do not only want the results of a single phase, but of an instance/run/experiment?
You can provide the corresponding IDs with `-i` for instance, `-r` for run, and `-e` for experiment.
Providing a "lower" level ID will ignore higher ones (because a phase can only be part of one instance can only be part of one run can only be part of one experiment).

### Batch reading

If you use the `paldaque muscle-action` command, the entries will be read in batches of 100 lines of data.
This allows a "convenient" view of the data in the terminal.
But the actual reason for that is the handling of large datasets. 
If you have ten thousands of data points to query, this can become very slow (or the process could even get killed if you run out of memory).
If you use the `--csv` option, the default limit is set to 10k, which should work even on older machines quite fast. 
Getting a dataset of 100k data points will still take some more seconds, but it should not crash and you can access intermediate results already.

You can control the batch loading behavior with the `--batch-size` (short `-b`) option:

```bash
paldaque muscle-action -b 20
```

This will only show twenty lines in the terminal (for csv export such a low number will likely be not useful but still possible).

Another related option is to use the `--offset` (short `-o`) option to skip the first *n* data points


```bash
paldaque muscle-action -o 5
```

This will skip the first 5 data points and then continue

Finally, there is an option to specify a maximum number of samples to be read with the `--max-read` (short `-m`) option

```bash
paldaque muscle-action -m 110
```

This will stop once 10 data points are read.

You can combine all of the three options.

### Using a different database

You have a different database running somewhere?
You can change the database by providing the `--store-uri` (or short `-s`) option:

```bash
paldaque -s "sqlite:///palaestrai.db" muscle-action
```

Note: there will be no check if the database exists.
You may get errors it that is not the case!

## API

Yes, there is an API so you will be able to integrate `paldaque` directly into your application.

The equivalent code for `paldaque -s "sqlite:///palaestrai.db" muscle-action -p 1 -f -m 100` would be something like this:

```python
from tabulate import tabulate

from paldaque.api_muscle_action import read_muscle_actions
from palaestrai.core import RuntimeConfig

# If you want to use a custom store uri
RuntimeConfig().load({"store_uri": "sqlite:///palaestraid.db"})

results = read_muscle_actions(
    experiment_id=0,
    experiment_run_id=0,
    experiment_run_instance_id=0,
    experiment_run_phase_id=1,
    limit=100,
    offset=0,
    as_dict=True
)

print(tabulate(results, headers="keys", tablefmt="pipe"))
```

This will return the first 100 values.
Increase if you need more and/or change the starting point with `offset`.

If you change `as_dict` to `False`, the `results` object will be a list containing dictionaries for each row.
Otherwise, it will be a dictionary with lists for each column.
