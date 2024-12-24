block_cipher = None

a = Analysis(
    ['src/app.py'],
    pathex=['N:\\Doct\\Codes\\World_Wines'],
    binaries=[],
    datas=[
        ('src/templates', 'templates'),
        ('src/data', 'data'),
        ('src/static', 'static')
    ],
    hiddenimports=[
        'folium',
        'flask',
        'pandas'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'data_processing',
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
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WineMap',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True
)