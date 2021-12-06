from setuptools import setup

dependencies = [
    "multidict==5.1.0",  # Avoid 5.2.0 due to Avast
    "aiofiles==0.7.0",  # Async IO for files
    "blspy==1.0.8",  # Signature library
    "chiavdf==1.0.3",  # timelord and vdf verification
    "chiabip158==1.0",  # bip158-style wallet filters
    "chiapos==1.0.7",  # proof of space
    "clvm==0.9.7",
    "clvm_rs==0.1.16",
    "clvm_tools==0.4.3",
    "aiohttp==3.7.4",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.9",  # Binary data management library
    "colorama==0.4.4",  # Colorizes terminal output
    "colorlog==5.0.1",  # Adds color to logs
    "concurrent-log-handler==0.9.19",  # Concurrently log and rotate logs
    "cryptography==3.4.7",  # Python cryptography library for TLS - keyring conflict
    "fasteners==0.16.3",  # For interprocess file locking
    "keyring==23.0.1",  # Store keys in MacOS Keychain, Windows Credential Locker
    "keyrings.cryptfile==1.3.4",  # Secure storage for keys on Linux (Will be replaced)
    #  "keyrings.cryptfile==1.3.8",  # Secure storage for keys on Linux (Will be replaced)
    #  See https://github.com/frispete/keyrings.cryptfile/issues/15
    "PyYAML==5.4.1",  # Used for config file format
    "setproctitle==1.2.2",  # Gives the replaceme processes readable names
    "sortedcontainers==2.4.0",  # For maintaining sorted mempools
    "websockets==8.1.0",  # For use in wallet RPC and electron UI
    "click==7.1.2",  # For the CLI
    "dnspythonchia==2.2.0",  # Query DNS seeds
    "watchdog==2.1.6",  # Filesystem event watching - watches keyring.yaml
    "dnslib==0.9.14",  # dns lib
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "pytest",
    "pytest-asyncio",
    "pytest-monitor; sys_platform == 'linux'",
    "pytest-xdist",
    "flake8",
    "mypy",
    "black",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
    "types-aiofiles",
    "types-click",
    "types-cryptography",
    "types-pkg_resources",
    "types-pyyaml",
    "types-setuptools",
]

kwargs = dict(
    name="replaceme-blockchain",
    author="Mariano Sorgente",
    author_email="mariano@replaceme.net",
    description="Replaceme blockchain full node, farmer, timelord, and wallet.",
    url="https://replaceme.net/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="replaceme blockchain node",
    install_requires=dependencies,
    setup_requires=["setuptools_scm"],
    extras_require=dict(
        uvloop=["uvloop"],
        dev=dev_dependencies,
        upnp=upnp_dependencies,
    ),
    packages=[
        "build_scripts",
        "replaceme",
        "replaceme.cmds",
        "replaceme.clvm",
        "replaceme.consensus",
        "replaceme.daemon",
        "replaceme.full_node",
        "replaceme.timelord",
        "replaceme.farmer",
        "replaceme.harvester",
        "replaceme.introducer",
        "replaceme.plotters",
        "replaceme.plotting",
        "replaceme.pools",
        "replaceme.protocols",
        "replaceme.rpc",
        "replaceme.seeder",
        "replaceme.seeder.util",
        "replaceme.server",
        "replaceme.simulator",
        "replaceme.types.blockchain_format",
        "replaceme.types",
        "replaceme.util",
        "replaceme.wallet",
        "replaceme.wallet.puzzles",
        "replaceme.wallet.rl_wallet",
        "replaceme.wallet.cc_wallet",
        "replaceme.wallet.did_wallet",
        "replaceme.wallet.settings",
        "replaceme.wallet.trading",
        "replaceme.wallet.util",
        "replaceme.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "replaceme = replaceme.cmds.replaceme:main",
            "replaceme_wallet = replaceme.server.start_wallet:main",
            "replaceme_full_node = replaceme.server.start_full_node:main",
            "replaceme_harvester = replaceme.server.start_harvester:main",
            "replaceme_farmer = replaceme.server.start_farmer:main",
            "replaceme_introducer = replaceme.server.start_introducer:main",
            "replaceme_seeder = replaceme.cmds.seeder:main",
            "replaceme_seeder_crawler = replaceme.seeder.start_crawler:main",
            "replaceme_seeder_server = replaceme.seeder.dns_server:main",
            "replaceme_timelord = replaceme.server.start_timelord:main",
            "replaceme_timelord_launcher = replaceme.timelord.timelord_launcher:main",
            "replaceme_full_node_simulator = replaceme.simulator.start_simulator:main",
        ]
    },
    package_data={
        "replaceme": ["pyinstaller.spec"],
        "": ["*.clvm", "*.clvm.hex", "*.clib", "*.clinc", "*.clsp", "py.typed"],
        "replaceme.util": ["initial-*.yaml", "english.txt"],
        "replaceme.ssl": ["replaceme_ca.crt", "replaceme_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    # use_scm_version={"fallback_version": "unknown-no-.git-directory"},
    version="1.0.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)


if __name__ == "__main__":
    setup(**kwargs)  # type: ignore
