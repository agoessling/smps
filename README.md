# smps 

Switch-Mode Power Supply design.

## Usage

### WORKSPACE

To incorporate `smps` into your project copy the following into your `WORKSPACE` file.

```Starlark
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "smps",
    # See release page for latest version url and sha.
)
```
