# Firepup650
Package containing various shorthand things I use, and a few imports I almost always use
### Change log:
#### v.1.1.0:
BREAKING: due to breaking changes in fkeycapture 1.3.0, this package is now only compatible with that version and above.
#### v.1.0.48:
pylint
#### v.1.0.47:
Typo fix in safety check
#### v.1.0.46:
Project metadata update
#### v.1.0.45:
Added an explode function (dangerous!!)
#### v.1.0.44:
Added a getRandomNumber function (xkcd 221)
#### v.1.0.43:
Called the error the wrong thing
#### v.1.0.42:
Small typo fix (`stackLevel` -> `stacklevel`)
#### v.1.0.41:
Windows "Support"
#### v.1.0.40:
Add offset mapping all the way up to 10 Billion, which exceeds the integer limit.
#### v.1.0.39:
Add offset mappings for exceeding 1 Million options, new limit is 10 Million options
#### v.1.0.38:
Mappings for much larger menu sizes, hopefully no one should ever hit that limit.
#### v.1.0.37:
Upgrades to gp and gh, they now function as stand-alone prompts, and allow deletion of characters as well (`allowDelete` must be set to `True`)
#### v.1.0.36:
Fix an old annoying bug with menus having an incorrect size calculation if the width of the menu was an even number
#### v.1.0.35:
Adds a few missing docstrings and fixes a bug with the menu function
#### v.1.0.34:
Adds methods to hide/show the cursor and a menu system
#### v.1.0.33:
Finally fixes `clear`'s ascii option, and adds windows compatibility to the same
#### v.1.0.32 (Breaking change!):
BREAKING CHANGE: `input` -> `inputCast`

Adds the `makeError` function, and fixes some mypy complaints
#### v.1.0.31:
Adds the `isMath` function provided by @python660 on Replit Ask
#### v.1.0.30:
Fix all mypy stub issues
#### v.1.0.29:
Provide a mypy stub file
#### v.1.0.28:
Updates `Color` to flush print by default.
#### v.1.0.27:
Renames many methods, old names are still avalible for backwards compatiblity however. Also, SQL was moved to it's own package entirely.
#### v.1.0.26:
Adds `remove_prefix` and `remove_suffix`, name mangles internal variables in `sql`, fixes a bug in `console.warn`, adds `__VERSION__`, `__NEW__`, and `__LICENSE__`, adds many aliases for `help()`.
#### v.1.0.25:
Fix all bugs related to version `1.0.24`'s patch.
#### v.1.0.24:
Fixes a bug in `sql`'s `addTable` function.
#### v.1.0.23:
Adds `sql` (class) and all it's functions
#### v.1.0.22:
Adds `flush_print`.
#### v.1.0.21:
Adds `bad_cast_message` to `input` and `replit_input`.
#### v.1.0.20:
Fixes a bug where `replit_input` didn't cast to `cast`.
#### v.1.0.19:
Updates `replit_input` to call (new) custom `input` that supports type casting under the hood.
#### v.1.0.18:
Adds Ease Of Use stuff to `bcolors`.
#### v.1.0.17:
Adds `cprint`.
#### v.1.0.16:
Same as `v.1.0.15`. Should be fixed now.
#### v.1.0.15:
Same as `v.1.0.14`, but I can't use the same number
#### v.1.0.14:
Hopefully fixes poetry not showing certain project info.
#### v.1.0.13:
Adds `replit_input`
#### v.1.0.12:
Description fix for `gp`, add `gh`.
#### v.1.0.11:
Fix a bug in the `gp` method.
#### v.1.0.10:
Add the `REPLIT` color to `bcolors`, and add `replit_cursor` to the module.
#### v.1.0.9:
Small tweaks, nothing major.
#### v.1.0.8:
Cat install collections. This better fix it.
###### v.1.0.7:
Adds `console` (class), `bcolors` (class), and `Color` (function). Fixes type hinting on various things (Lots of thanks to [@bigminiboss](https://pypi.org/user/bigminiboss/)!).
#### v.1.0.6:
Hopefully, fixes an issue where the package doesn't install it's dependencies (Again. Hopefully.)
#### v.1.0.5:
Hopefully, fixes an issue where the package doesn't install it's dependencies
#### v.1.0.4:
Subscript errors
#### v.1.0.3:
Dependant errors
#### v.1.0.2:
Random shorthand (literally)
#### v.1.0.1:
Added animated typing function, sleep shorthand
#### v.1.0.0:
Initial Release!
