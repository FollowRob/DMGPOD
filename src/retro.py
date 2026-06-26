import os
import subprocess
import sys

RETROARCH_PATHS = [
    "/Applications/RetroArch.app/Contents/MacOS/RetroArch",
    "/usr/bin/retroarch",
    "/usr/local/bin/retroarch",
]

CORE_SEARCH_DIRS = [
    os.path.expanduser("~/Library/Application Support/RetroArch/cores"),
    "/usr/lib/libretro",
    "/usr/local/lib/libretro",
]

# Preferred core order per system
SYSTEM_CORES = {
    "gb":  ["sameboy", "gambatte", "mgba"],
    "gbc": ["sameboy", "gambatte", "mgba"],
    "gba": ["mgba", "vba_next", "gpsp"],
}

ROM_EXTENSIONS = {".gb", ".gbc", ".gba", ".zip"}


def find_retroarch():
    for p in RETROARCH_PATHS:
        if os.path.isfile(p):
            return p
    return None


def find_core(system):
    preferred = SYSTEM_CORES.get(system, [])
    for core_dir in CORE_SEARCH_DIRS:
        if not os.path.isdir(core_dir):
            continue
        for name in preferred:
            for fname in os.listdir(core_dir):
                if fname.startswith(name) and fname.endswith((".dylib", ".so")):
                    return os.path.join(core_dir, fname)
    return None


def scan_roms(roms_dir):
    """Return dict: {system: [{"name": str, "path": str}]}"""
    result = {}
    for system in ("gb", "gbc", "gba"):
        folder = os.path.join(roms_dir, system)
        if not os.path.isdir(folder):
            continue
        roms = []
        for fname in sorted(os.listdir(folder)):
            if os.path.splitext(fname)[1].lower() in ROM_EXTENSIONS:
                roms.append({
                    "name": os.path.splitext(fname)[0],
                    "path": os.path.join(folder, fname),
                    "system": system,
                })
        if roms:
            result[system] = roms
    return result


def launch(rom_path, system):
    """Launch RetroArch with the correct core. Blocks until RetroArch exits."""
    ra = find_retroarch()
    if not ra:
        return "RetroArch not found"
    core = find_core(system)
    if not core:
        return f"No core found for {system.upper()}"
    cmd = [ra, "-L", core, rom_path, "--fullscreen"]
    try:
        subprocess.run(cmd, check=False)
    except Exception as e:
        return str(e)
    return None
