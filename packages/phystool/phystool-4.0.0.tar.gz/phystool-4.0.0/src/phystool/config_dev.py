from configparser import ConfigParser
from pathlib import Path
from uuid import uuid4
from PySide6.QtCore import QProcessEnvironment


class MyConfig:
    def __init__(self, dev_mode: bool = True):
        config_dir = _ensure_exists(
            Path.cwd().parent / "dev"
            if dev_mode
            else Path.home() / ".phystool"
        )

        self._data = ConfigParser()
        self._config_file = config_dir / "phystool.conf"
        if self._config_file.exists():
            self._data.read(self._config_file)
        else:
            if dev_mode:
                self._data['phystool'] = {"db": str(config_dir / "physdb_dev")}
            else:
                self._data['phystool'] = {"db": str(Path.home() / "physdb")}
            self._data['physnoob'] = {'editor': 'kile'}
            self._data['latex'] = {
                "auto": "physauto_dev",
                "tikz": "phystikz_dev",
            }
            self._data['git'] = {"theme": ""}
            with self._config_file.open('w') as out:
                self._data.write(out)

        self.DB_DIR = Path(self._data['phystool']['db']).expanduser()
        if not self.DB_DIR.exists():
            from shutil import copytree
            copytree(self.get_static_path() / "physdb_dev", self.DB_DIR)

        self.METADATA_DIR = _ensure_exists(self.DB_DIR / "metadata")

        self.LOGFILE_PATH = config_dir / 'phystool.log'
        self.METADATA_PATH = self.METADATA_DIR / '0_metadata.pkl'
        self.TAGS_PATH = self.METADATA_DIR / '1_tags.json'
        self.EVALUATION_PATH = self.METADATA_DIR / '2_evaluations.json'
        self.LATEX = LaTeXConf(
            config_dir=config_dir,
            db_dir=self.DB_DIR,
            conf=self._data['latex']
        )
        self.EDITOR_CMD: tuple[str, list[str]] = (self._data['physnoob']['editor'], [])
        if self.EDITOR_CMD[0] == "vim":
            self.EDITOR_CMD = ("rxvt-unicode", ["-e", "vim"])

        self.DELTA_THEME = self._data['git']['theme']
        self.BITBUCKET_API_KEY = "ATCTT3xFfGN0uBgFqH_ksSRPMDAtwwcykz_4uMw5nD6Q97bgYKAcRqn9L0DXte6e6QZ_0uSxfSTb0ovyt3RcPEi3mOKdDLIwrwjSFhlUsfxOx7EAbnS00uVa-OHTKVopBojiFThl3Ton7bsJJkjUdpEG2PXolDjCvI5i4DmoPTinj3HBdIqyEzs=A220AF8E"  # noqa
        self.BITBUCKET_API_URL = "https://api.bitbucket.org/2.0/repositories/jdufour/phystool/src/master/CHANGELOG.md"  # noqa

    def get_static_path(self) -> Path:
        if not hasattr(self, '_static_path'):
            from site import getsitepackages
            for site_package in getsitepackages():
                tmp = Path(site_package) / "phystool/static/"
                if tmp.exists():
                    self._static_path = tmp
                    return self._static_path
            raise FileNotFoundError("Static path not found")
        return self._static_path

    def new_pdb_filename(self) -> Path:
        return (self.DB_DIR / str(uuid4())).with_suffix(".tex")

    def save_config(self, section: str, key: str, val: str) -> None:
        try:
            self._data[section][key] = val
        except KeyError:
            self._data.add_section(section)
            self._data[section][key] = val
        with self._config_file.open('w') as out:
            self._data.write(out)


class LaTeXConf:
    def __init__(self, config_dir: Path, db_dir: Path, conf: dict[str, str]):
        self._env: dict[bool, QProcessEnvironment | dict] = {}
        self._template = (
            f"\\documentclass{{{{{conf['auto']}}}}}\n"
            f"\\PdbSetDBPath{{{{{db_dir}/}}}}\n"
            "\\begin{{document}}\n"
            "    \\PdbPrint{{{tex_file}}}\n"
            "\\end{{document}}"
        )
        self.source = _ensure_exists(db_dir / "phystex")
        self.tikz_pattern = fr"^\\documentclass.*{{{conf['tikz']}}}"
        self.aux = _ensure_exists(config_dir / "texaux")

    def env(self, qrocess: bool) -> dict[str, str] | QProcessEnvironment:
        if not self._env:
            tmp = QProcessEnvironment.systemEnvironment()
            tmp.insert("TEXINPUTS", f":{self.source}:")
            self._env = {
                True: tmp,
                False: {
                    key: tmp.value(key)
                    for key in tmp.keys()
                }
            }
        return self._env[qrocess]

    def template(self, tex_file: Path) -> str:
        return self._template.format(tex_file=tex_file)


def _ensure_exists(path: Path) -> Path:
    if not path.exists():
        path.mkdir()
    return path
