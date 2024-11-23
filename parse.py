import sys
import json
from pathlib import Path


def json_to_lang(src, dst):
    src = Path(src)
    dst = Path(dst)

    with open(src, "r", encoding="utf8") as f:
        fd = json.load(f)

    def parse(keys: list, obj):
        if isinstance(obj, list):
            for idx, item in enumerate(obj):
                parse([*keys, str(idx)], item)

        elif isinstance(obj, dict):
            if "description" in obj:
                lang[".".join(keys)] = obj["description"]

            for key, value in obj.items():
                parse([*keys, key], value)

    lang = {}
    parse([], fd)

    with open(dst, "w", encoding="utf8") as f:
        json.dump(lang, f, indent=2)


def lang_to_json(lang_p, src):
    lang_p = Path(lang_p)
    src = Path(src)

    with open(lang_p, "r", encoding="utf8") as f:
        lang = json.load(f)

    with open(src, "r", encoding="utf8") as f:
        fd = json.load(f)

    def parse(keys: list, obj):
        if isinstance(obj, list):
            for idx, item in enumerate(obj):
                parse([*keys, str(idx)], item)

        elif isinstance(obj, dict):
            if "description" in obj:
                _key = ".".join(keys)
                if _key in lang:
                    obj["description"] = lang[_key]

            for key, value in obj.items():
                parse([*keys, key], value)

    parse([], fd)

    with open(src, "w", encoding="utf8") as f:
        json.dump(fd, f, indent=2)


if __name__ == '__main__':
    try:
        mode = sys.argv[1]
    except IndexError:
        mode = None

    if mode == "json2lang":
        src = Path("./schema/biomes-schema.json")
        json_to_lang(src, src.with_stem(src.stem + ".lang"))

    elif mode == "lang2json":
        src = Path("./schema/biomes-schema.json")
        lang_p = src.with_stem(src.stem + ".lang")
        json_to_lang(lang_p, src)
