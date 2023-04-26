# HOLON ETM service module

Welcome to the little ETM input module. This repo contains the ETM service module of the HOLON project. This repo and other repos are licensed under the [MIT license](LICENSE.md). Other repos are:

1. [AnyLogic](https://github.com/ZEnMo/HOLON)
2. [Webapp](https://github.com/ZEnMo/HOLON-webapp)
3. [cloudclient](https://github.com/ZEnMo/HOLON-cloudclient) (legacy)

### Example

Running an example of the module via `hatch`:

```
hatch run etm_to_csv
```

And running the tests:

```
hatch run cov
```

If you're not interested in `hatch`, the used dependencies are very straightforward, and can be found in the `pyproject.toml`. So you should be fine by just running the examples in the `scripts` folder in your own way.

### Using the packaged version

You can also install the lastest realease as a package with `pip`.

```
pip install dist/etm_service-0.1.tar.gz
```

And then import it into your own project with `import etm_service`. Check out some
examples in the scripts folder, like `get_etm_results.py`.

## Configuring the module

The main action for modelers here is in the config folder. The `config` file allows you to specify where the data comes from and goes to. You can specify which ETM engine you want to connect to, with which scenario you want to communicate, and where the data should be written to.

The `etm_service` file contains _what_ information should be pulled from the ETM and if any conversions should be done on it. There is a description at the top of the file telling you what is expected for each field, and some dummy data.

## Adding new conversions

Currently only 'divide' is supported as a conversion, but it's relatively easy to add more different types. Here's a little guide if any of you wants to try.

**Step 1** Create a new file/class in the `converters` module. It requires an init, a method called `calculation` and a method called `required_for_calculation`. Draw some inspiration from the `DivideBy` converter. Don't forget to import your new converter in the converter modules init!

**Step 2** Add suitable methods to `Curve`, `Value` and `NodeProperty` if you want these data types to act on your new conversion (e.g arithmatic operations). Again you can draw inpsiration from the `divide_by` method on `Curve`.

**Step 3** Think of a good keyword for your converter to use in the config file (like `divide` for the `DivideBy` converter). Add this keyword for your converter to the method `_create_converter` in `single_request.converter`.

Good luck!
