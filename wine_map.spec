block_cipher = None

a = Analysis(
    ['src/app.py'],  # Entry point to your application
    pathex=['World_Wines'],  # Base path of your project
    binaries=[],  # No binary files
    datas=[
        ('src/templates', 'templates'),  # Include templates folder
        ('src/static', 'static'),        # Include static folder
        ('src/data', 'data'),            # Include data folder
    ],
    hiddenimports=[
        'folium',
        'flask',
        'pandas',
        'jinja2',
        'werkzeug',
        'flask.templating',
        'folium.plugins'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'src/data_processing.py',  # Exclude the script you don't need
        '.git',
        '.gitignore',
        'README.md'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,  # Use the scripts automatically found by Analysis
    [],
    exclude_binaries=True,  # Don't duplicate binaries in EXE
    name='WineMap',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,  # Collect all the data files specified earlier
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WineMap'
)
