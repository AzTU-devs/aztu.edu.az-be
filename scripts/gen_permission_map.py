"""Emit ROUTE_PERMISSIONS skeleton lines for routes that are not mapped yet.

The map in app/core/permission_map.py is hand-maintained — this only saves typing
when new routes land. Run it, paste the output into the right section, replace
every TODO.TODO with a real catalogue key, then add the key to
app/core/permissions.py.

    python -m scripts.gen_permission_map
"""

import re
import sys

sys.path.insert(0, ".")

from app.core.permission_map import ROUTE_PERMISSIONS, _SKIP_METHODS, _SKIP_PATHS  # noqa: E402

_PARAM = re.compile(r"\{([^}]+)\}")


def _guess(path: str):
    params = _PARAM.findall(path)
    if not params:
        return None, None
    param = params[-1]
    return param, param[:-3] if param.endswith("_id") else param


def main() -> int:
    from app.main import app

    lines = []
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", None)
        if not path or not methods or path in _SKIP_PATHS:
            continue
        for method in sorted(set(methods) - _SKIP_METHODS):
            if (method, path) in ROUTE_PERMISSIONS:
                continue
            param, target = _guess(path)
            args = ['"TODO.TODO"']
            if target:
                args.append(f'target_type="{target}"')
            if param:
                args.append(f'target_param="{param}"')
            lines.append(f'    ("{method}", "{path}"): RouteRule({", ".join(args)}),')

    if not lines:
        print("# permission_map is complete — nothing to generate.")
        return 0

    print(f"# {len(lines)} unmapped mutating route(s):")
    print("\n".join(sorted(lines)))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
