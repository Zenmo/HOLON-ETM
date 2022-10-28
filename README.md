# The etm_service module

Welcome to the little ETM input module.

Running an example of the module via `hatch`:
```
hatch run etm_to_csv
```

And running the tests:
```
hatch run cov
```

If you're not interested in `hatch`, the used dependencies are very straightforward, and can be found in the `pyproject.toml`. So you should be fine by just running the examples in the `scripts` folder in your own way.

## Configuring the module
The main action for modelers here is in the config folder. The `config` file allows you to specify where the data comes from and goes to. You can specify which ETM engine you want to connect to, with which scenario you want to communicate, and where the data should be written to.

The `etm_service` file contains _what_ information should be pulled from the ETM and if any conversions should be done on it. There is a description at the top of the file telling you what is expected for each field, and some dummy data.

## Adding new conversions
Currently only 'divide' is supported as a conversion, but it's relatively easy to add more different types. Here's a little guide if any of you wants to try.

**Step 1** Create a new file/class in the `converters` module. It requires an init, a method called `calculation` and a method called `required_for_calculation`. Draw some inspiration from the `DivideBy` converter. Don't forget to import your new converter in the converter modules init!

**Step 2** Add suitable methods to `Curve`, `Value` and `NodeProperty` if you want these data types to act on your new conversion (e.g arithmatic operations). Again you can draw inpsiration from the `divide_by` method on `Curve`.

**Step 3** Think of a good keyword for your converter to use in the config file (like `divide` for the `DivideBy` converter). Add this keyword for your converter to the method `_create_converter` in `single_request.converter`.

Good luck!
