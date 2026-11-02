"""Localiza el texto fijo del buscador emergente de los sitios Zensical indicados."""

from pathlib import Path
import sys


site_roots = [Path(argument) for argument in sys.argv[1:]] or [Path("sites/1dam-djk/site")]

original = 'placeholder:"Search"'
localized = 'placeholder:"Buscar"'

for site_root in site_roots:
    bundle_dir = site_root / "assets/javascripts"
    bundles = list(bundle_dir.glob("bundle.*.min.js"))
    if len(bundles) != 1:
        raise SystemExit(
            f"Se esperaba un único bundle de Zensical en {bundle_dir}; encontrados: {len(bundles)}"
        )

    bundle = bundles[0]
    content = bundle.read_text(encoding="utf-8")
    occurrences = content.count(original)
    if occurrences != 1:
        raise SystemExit(f"Se esperaba una única etiqueta de búsqueda en {bundle}; encontradas: {occurrences}")

    bundle.write_text(content.replace(original, localized), encoding="utf-8")
