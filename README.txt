# inidupekeys

** this is inoperable **

Small experiment to subclass something in `configparser` to allow consuming
duplicate options into a list.

Several problems:

* huge loop inside `RawConfigParser._read` method with very few ways of
  hooking into it.
* strict = False is the only way to avoid `DuplicateOptionError` errors in
  that loop.
* other methods raise `DuplicateOptionError` errors.
