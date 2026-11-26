import hashlib
import os
import shutil
import tempfile
from pathlib import Path

OLD = "aa3c8d64c79c8e3e45dd095e6dc4b6215cfb30912df50c05a55cd0d5c5f7efa5"
SRC = "fba1ccd9ab7e334ccca2c632ccd3613a3a20274893aa8aaa405b56be4af81835"
NEW = "714d5ba42c2732807220de570ec520f671a30ca7b35837656d47c830ff491c80"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for data in iter(lambda: f.read(1024 * 1024), b""):
            h.update(data)
    return h.hexdigest()


def combine(folder):
    folder = Path(folder)
    target, source = folder / "1126.hip", folder / "tableright.hip"
    if not target.is_file() or not source.is_file():
        raise RuntimeError("没有找到 1126.hip 和 tableright.hip；未修改文件。")
    if sha(source) != SRC:
        raise RuntimeError("tableright 与上传版本不同；未修改文件。")
    current = sha(target)
    if current == NEW:
        print("1126 已经合并完成，不需要重复运行。", flush=True)
        return
    if current != OLD:
        raise RuntimeError("1126 与上传版本不同；未修改文件。")
    backup = folder / "_merge_rollback" / "1126.hip"
    if backup.exists() and sha(backup) != OLD:
        raise RuntimeError("回退文件与上传版本不同；未修改文件。")
    need = 549322663 + (0 if backup.exists() else target.stat().st_size) + 64 * 1024 * 1024
    if shutil.disk_usage(folder).free < need:
        raise RuntimeError("磁盘可用空间不足 1 GB；未修改文件。")
    print("1/3 文件版本核对通过，正在合并；不计算 UV。", flush=True)
    fd, name = tempfile.mkstemp(prefix="1126_merge_", suffix=".tmp", dir=folder)
    os.close(fd)
    temporary = Path(name)
    try:
        with open(target, "rb") as t, open(source, "rb") as s, open(temporary, "wb") as out:
            # These five ranges preserve both native archive dependency blocks.
            ranges = [(t, 0, 1046630), (s, 1046658, 1058973),
                      (t, 1058955, 11025897), (s, 2640892, 540767570),
                      (t, 417317886, 417487984)]
            for stream, begin, end in ranges:
                stream.seek(begin)
                remaining = end - begin
                while remaining:
                    data = stream.read(min(1024 * 1024, remaining))
                    if not data:
                        raise RuntimeError("输入文件读取失败；未替换 1126。")
                    out.write(data)
                    remaining -= len(data)
            out.flush()
            os.fsync(out.fileno())
        if sha(temporary) != NEW or sha(target) != OLD or sha(source) != SRC:
            raise RuntimeError("合并校验失败；未替换 1126。")
        print("2/3 校验通过：教室保留原样，桌椅完整采用 tableright。", flush=True)
        backup.parent.mkdir(exist_ok=True)
        if not backup.exists():
            created = False
            try:
                with open(target, "rb") as src, open(backup, "xb") as dst:
                    created = True
                    shutil.copyfileobj(src, dst, 1024 * 1024)
                    dst.flush()
                    os.fsync(dst.fileno())
            except BaseException:
                if created:
                    backup.unlink(missing_ok=True)
                raise
        if sha(backup) != OLD:
            raise RuntimeError("回退文件校验失败；未替换 1126。")
        if sha(target) != OLD:
            raise RuntimeError("1126 在合并期间被修改；停止替换。")
        os.replace(temporary, target)
        print("3/3 完成：" + str(target), flush=True)
        print("tableright、wallright 未改动。请在 Houdini 中打开这个 1126.hip。", flush=True)
        print("不要把仍显示旧场景的窗口保存覆盖这个文件。", flush=True)
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    combine(r"E:/1126")
