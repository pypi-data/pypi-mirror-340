# pip-build-standalone

pip-build-standalone builds a standalone, relocatable Python installation with the given
pips installed.

Typically, Python installations are not relocatable or transferable between machines, in
particular because scripts and libraries contain absolute file paths (such as your home
folder at the time Python or the venv was installed).

[uv](https://github.com/jlevy/uv) already uses
[standalone Python distributions](https://github.com/astral-sh/python-build-standalone)
and offers [relocatable venvs](https://github.com/astral-sh/uv/pull/5515). But the
actual Python installations created by uv can still have absolute paths that can leak
into libs and scripts.

This tool takes a bit of a brute-force approach to get a fully self-contained
installation. We have to do slightly different things on macOS, Linux, and Windows to
make the installation relocatable, but it now seems to work on all three platforms.

It uses a true (not venv) Python installation with the given pips installed, with zero
absolute paths encoded in any of the Python scripts or libraries.
So *in theory*, the resulting binary folder should be installable as at any location on
a machine with compatible architecture.

The idea is this pre-built binary build for a given platform can now packaged for use
without any external dependencies on Python or uv.

Warning: Experimental!
No promises this works or is even a good idea.

It is lightly tested on macOS, ubuntu, and Windows, but obviously there are lots of
possibilities for subtle incompatibilities within a given platform.

## Usage

This tool requires uv to run.
Do a `uv self update` to make sure you have a recent uv (I'm currently testing on
v0.6.14).

As an example, to create a full standalone Python 3.13 environment with the `cowsay`
package:

```sh
uvx pip-build-standalone cowsay
```

Now the `./py-standalone` directory will work without being tied to a specific machine,
your home folder, or any other system-specific paths.

Binaries can now be put wherever and run:

```
./py-standalone/cpython-3.13.2-macos-aarch64-none/bin/cowsay -t moo
mv ./py-standalone /tmp
/tmp/py-standalone/cpython-3.13.2-macos-aarch64-none/bin/cowsay -t moo
```

```log
$ uvx pip-build-standalone cowsay

❯ uv python install --managed-python --install-dir /Users/levy/wrk/github/pip-build-standalone/py-standalone 3.13
Installed Python 3.13.3 in 1.78s
 + cpython-3.13.3-macos-aarch64-none

⏱ Call to run took 1.79s

❯ uv pip install cowsay --python py-standalone/cpython-3.13.3-macos-aarch64-none --break-system-packages
Using Python 3.13.3 environment at: py-standalone/cpython-3.13.3-macos-aarch64-none
Resolved 1 package in 0.85ms
Installed 1 package in 2ms
 + cowsay==6.1

⏱ Call to run took 655ms
Removed: py-standalone/cpython-3.13.3-macos-aarch64-none/lib/python3.13/encodings/__pycache__
Found macos dylib, will update its id to remove any absolute paths: py-standalone/cpython-3.13.3-macos-aarch64-none/lib/libpython3.13.dylib

❯ install_name_tool -id @executable_path/../lib/libpython3.13.dylib py-standalone/cpython-3.13.3-macos-aarch64-none/lib/libpython3.13.dylib

⏱ Call to run took 31.71ms

Inserting relocatable shebangs on scripts in:
    ', '.join(glob_patterns)}
Replaced shebang in: py-standalone/cpython-3.13.3-macos-aarch64-none/bin/cowsay
Replaced shebang in: py-standalone/cpython-3.13.3-macos-aarch64-none/bin/pydoc3.13
Replaced shebang in: py-standalone/cpython-3.13.3-macos-aarch64-none/bin/pip3.13
Replaced shebang in: py-standalone/cpython-3.13.3-macos-aarch64-none/bin/pip3
Replaced shebang in: py-standalone/cpython-3.13.3-macos-aarch64-none/bin/idle3
Replaced shebang in: py-standalone/cpython-3.13.3-macos-aarch64-none/bin/python3-config
Replaced shebang in: py-standalone/cpython-3.13.3-macos-aarch64-none/bin/pip
Replaced shebang in: py-standalone/cpython-3.13.3-macos-aarch64-none/bin/idle3.13
Replaced shebang in: py-standalone/cpython-3.13.3-macos-aarch64-none/bin/python3.13-config
Replaced shebang in: py-standalone/cpython-3.13.3-macos-aarch64-none/bin/pydoc3

Replacing all absolute paths in:
    py-standalone/cpython-3.13.3-macos-aarch64-none/bin/* py-standalone/cpython-3.13.3-macos-aarch64-none/lib/**/*.py:
    `/Users/levy/wrk/github/pip-build-standalone/py-standalone` -> `py-standalone`
Replaced 27 occurrences in: py-standalone/cpython-3.13.3-macos-aarch64-none/lib/python3.13/_sysconfigdata__darwin_darwin.py
Replaced 27 total occurrences in 1 files total

Sanity checking if any absolute paths remain...
Great! No absolute paths found in the installed files.

✔️ Success: Created standalone Python environment for packages ['cowsay'] at: py-standalone

$ ./py-standalone/cpython-3.13.3-macos-aarch64-none/bin/cowsay -t 'im moobile'
  __________
| im moobile |
  ==========
          \
           \
             ^__^
             (oo)\_______
             (__)\       )\/\
                 ||----w |
                 ||     ||
$ /tmp/py-standalone/cpython-3.13.3-macos-aarch64-none/bin/cowsay -t 'udderly moobile'
  _______________
| udderly moobile |
  ===============
               \
                \
                  ^__^
                  (oo)\_______
                  (__)\       )\/\
                      ||----w |
                      ||     ||
$
```

* * *

*This project was built from
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*
