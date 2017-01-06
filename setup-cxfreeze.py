from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    includes = ['atexit'],
    excludes = [])

executables = [
    Executable(
        'xldigest/main.py',
        base = None,
        targetName = 'xldigest',
    )
]

setup(name='xldigest-cxfreeze',
      version = '1.0',
      description = 'An application',
      options = dict(build_exe = buildOptions),
      executables = executables)
