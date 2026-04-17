# 3ds Max Known Patterns

This file is intentionally small. Add tested snippets as the adapter is used.

## Context

Use `examples/context.py`.

## MAXScript From Python

```python
import MaxPlus

value = MaxPlus.Core.EvalMAXScript("objects.count")
result = value.Get()
```

## Create Objects

```python
import MaxPlus

script = r'''
undo "Add box" on
(
    obj = box name:"Named Box" length:40 width:40 height:40 pos:[0,0,20]
    select obj
    obj.name
)
'''
created = MaxPlus.Core.EvalMAXScript(script).Get()
```

## Undo

Prefer MAXScript `undo "<label>" on (...)` around bounded directed edits.

## Python Version

3ds Max 2020 embeds Python 2.7. In-app bridge code must avoid Python 3-only
syntax. User scripts sent through the bridge should also be compatible with the
embedded Python version.
