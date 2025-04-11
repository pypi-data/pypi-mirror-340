# features


## done
+ (2025-04-10) bugfix: Wrong default value of bool argument; Wrong position of opposite arguments (--no-)
+ (2025-02-28) Optimize type annotation resolution via `EasyArg.search_cmdType`, add support for list[str] types
+ (2025-02-26) Split custom argument parser class (also customize `add_argument`), used it from /External/
+ (2025-02-25) Filter functions for showing available functions in CLI-executor mode
+ (2025-02-25) Search for an allowable type hint rather than always using the 1st one
+ (2025-02-22) Support set choices
+ (2025-02-22) resolve type by default/const value, but still restrained to generic python types
+ (2025-02-22) Allow `@ea.command(name="new-name", alias="aa")` for functions with too long name
+ (2025-02-22) Show docstring in help information of specific function
+ (2025-02-22) customized help information with colorful messages
+ (2025-01-16) Add support for completion in shell via **argcomplete**
+ (2025-01-16) Add description content in pypi
+ (2024-11-29) add actions for __main__ entry, that is, run a function even without statement "import easyarg", just run the function
