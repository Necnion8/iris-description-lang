import sys
import json
from pathlib import Path


def json_to_lang(src_dir, dst_json):
    src_dir = Path(src_dir)
    lang = {}

    def proc_nest(parent, keys: list, obj):
        if isinstance(obj, list):
            for idx, item in enumerate(obj):
                proc_nest(parent, [*keys, str(idx)], item)

        elif isinstance(obj, dict):
            if "description" in obj:
                lang[parent + ".".join(keys)] = obj["description"]

            for key, value in obj.items():
                proc_nest(parent, [*keys, key], value)

    for child in src_dir.glob("**/*"):
        if not child.is_file() or child.suffix != ".json":
            continue

        file_key = ".".join(child.relative_to(src_dir).with_suffix("").parts)
        with open(child, "r", encoding="utf8") as f:
            proc_nest(file_key + "/", [], json.load(f))

    with open(dst_json, "w", encoding="utf8") as f:
        json.dump(lang, f, indent=2, ensure_ascii=False)


def lang_to_json(src_dir, dst_dir, src_json):
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    src_json = Path(src_json)

    with open(src_json, "r", encoding="utf8") as f:
        lang = json.load(f)

    def proc_nest(parent, keys: list, obj):
        if isinstance(obj, list):
            for idx, item in enumerate(obj):
                proc_nest(parent, [*keys, str(idx)], item)

        elif isinstance(obj, dict):
            if "description" in obj:
                _key = parent + ".".join(keys)
                if _key in lang:
                    obj["description"] = lang[_key]

            for key, value in obj.items():
                proc_nest(parent, [*keys, key], value)

    for child in src_dir.glob("**/*"):
        if not child.is_file() or child.suffix != ".json":
            continue

        child_path = child.relative_to(src_dir)
        file_key = ".".join(child_path.with_suffix("").parts)
        with open(child, "r", encoding="utf8") as f:
            fd = json.load(f)
            proc_nest(file_key + "/", [], fd)

        (dst_dir / child_path).parent.mkdir(parents=True, exist_ok=True)
        with open(dst_dir / child_path, "w", encoding="utf8") as f:
            json.dump(fd, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    try:
        mode = sys.argv[1]
    except IndexError:
        mode = None

    if mode == "genlang":
        json_to_lang("./schema", "description_lang.json")

    elif mode == "apply":
        lang_to_json("./schema", "./schema_result", "description_lang.json")

    else:
        print("mode を指定してください")
        print("  genlang    -> ./schema を読み込んで description_lang.json を出力します")
        print("  apply      -> ./schema と description_lang.json を読み込んで ./schema_result に出力します")
