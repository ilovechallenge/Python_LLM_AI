# Decorators

*Variable decorators* offer a simple mechanism to execute custom variable value transformations during the decoding process. They enable custom pre-processing, post-processing or streaming of model output.

## Post-Processing Decorators

The standard use of decorators is to post-process a generated variable value:

```{lmql}
name::decorators

def screaming(value):
    """Decorator to convert a string to uppercase"""
    return value.upper()

"Say 'this is a test':[@screaming TEST]"

model-output::
Say 'this is a test': [TEST THIS IS A TEST]
```

The example above shows a simple decorator that converts the generated variable value to uppercase. By default, decorators are applied to the variable value after the variable has finished decoding.

**Value and Prompt Representation** Next to simple use as shown above, the function signature of a decorator can also be extended to obtain more information about the variable context:

```{lmql}
name::decorators-with-context

from lmql.runtime.program_state import ProgramState
from typing import Any

def aslist(value: Any, prompt_value: str, context: ProgramState):
    """Decorator to convert a comma-separated string into a List[str]"""
    return value.split(", "), prompt_value

"A (comma-separated) list of pancake ingredients: [@aslist ANSWER]"

model-output::
A (comma-separated) list of pancake ingredients: [ANSWER Flour, Eggs, Milk, Baking Powder, Salt, Butter]
```

Here, the decorator `aslist()` has theee arguments:
- `value: any`: the post-processed value of `ANSWER` after it has been fully generated
- `prompt_value: str`, the text representation of `ANSWER` as it was generated by the model
- `context: ProgramState`, the current program state.

The decorator returns a tuple of `(value, prompt_value)`, where `value` is the updated program value for `ANSWER` and `prompt_value` is the updated text representation.

Differentiating between `value` and `prompt_value` allows decorators to modify the program value of `ANSWER` as well as its text representation as used in the prompt. If a decorator does not provide both, `value` and `prompt_value`, as a tuple, the prompt value is assumed to be `str(value)`.

## Streaming Decorators

Another form of decorators are *streaming decorators*. Streaming decorators are applied to the variable value during the decoding process, i.e. the decorator is called for intermediate value of a variable as it is being decoded. This allows for variable-specific streaming of the output:

```{lmql}
name::streaming-decorators
from lmql.runtime.program_state import ProgramState

@lmql.decorators.streaming
def stream(value: str, context: ProgramState):
    """Decorator to stream the variable value"""
    print("VALUE", [value])

"Enumerate the alphabet without spaces:[@stream TEST]"
```

During execution of this query, `stream()` is called for each intermediate value of `TEST`, leading to the output shown above. This allows you to stream output as it is being generated, e.g. to show [partial responses in a chat application](../lib/chat.md) or on the command line.

```bash
VALUE ['']
VALUE ['']
VALUE ['\n']
VALUE ['\n\n']
VALUE ['\n\nABC']
VALUE ['\n\nABCDEF']
...
```

## Pre-Processing Decorators

Lastly, a decorator can also hook into query execution right before the generation of a variable begins. For instance, consider the following caching decorator function:

```{lmql}
name::pre-processing-decorators
from lmql.runtime.program_state import ProgramState
from lmql.language.qstrings import TemplateVariable

cached_values = {
    "ITEM0": "A shopping cart"
}

@lmql.decorators.pre
def cache(variable: TemplateVariable, context: ProgramState):
    """Decorator to cache variable values by name"""
    return cached_values.get(variable.name, variable)

"""A list of things not to forget when going to the supermarket:
-[@cache ITEM0]
-[@cache ITEM1]
-[@cache ITEM0]
""" where STOPS_BEFORE(ITEM0, "\n") and STOPS_BEFORE(ITEM1, "\n")
```

Given a pre-determined list of fixed values per variable name like `ITEM0`, query execution only actually invokes the model for `ITEM1`. For all occurences of `ITEM0`, the cached value is used instead. 

For this, a pre-processing decorator either returns the provided `variable: TemplateVariable` object to indicate that the variable should be generated as usual, or it returns a string value to indicate that the variable should be replaced by a fixed value instead.

## Advanced Decorator Behavior
### Class-Based Decorators

More advanced decorator behavior may require hooking into the query execution process at multiple stages. For this, the `lmql.runtime.decorators.LMQLDecorator` class can be implemented, an instance of which can then act as a decorator function that is invoked at multiple stages of the query execution process.

### Decorator Arguments 

Multiple decorators can also be chained on a single variable, e.g.:
    
```{lmql}
name::decorator-chaining

"Say 'this is a test':[@a @b @c TEST]"
```

During query execution, the pre-stage (if defined), invokes `a()`, `b()` and `c()` in order, passing the result of each decorator to the next one. The post-stage (if defined) then invokes `c()`, `b()` and `a()` in reverse order, passing the result of each decorator to the next one. Streaming-stage decorators do not have a return value, meaning that the order of execution does not have a particular effect.

### Decorator Arguments 

Decorators can also be provided with arguments. The implementation of such operators is achieved similarly to the implementation of decorators in standard Python via local variable capture:

```{lmql}
name::decorator-arguments

def prefix(prefix: str):
    # actual decorator function
    def decorator(value: str):
        return prefix + value.strip()
    
    return decorator

"Say 'this is a test':[@prefix('PREFIX: ') TEST]"

model-output::

Say 'this is a test': [TEST PREFIX: This is a test]
```