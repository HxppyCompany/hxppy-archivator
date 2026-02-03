from pathlib import Path
from src.hxppy import pack_files, unpack_files


def test_pack_unpack_cycle(tmp_path: Path):
    # 1. Создаем временную структуру файлов
    test_dir = tmp_path / "project"
    test_dir.mkdir()
    file1 = test_dir / "hello.py"
    file1.write_text("print('hello')", encoding="utf-8")

    archive = tmp_path / "backup.txt"

    # Меняем рабочую директорию на временную (имитируем запуск в папке)
    import os

    old_cwd = os.getcwd()
    os.chdir(test_dir)

    try:
        # 2. Упаковываем
        pack_files(archive)
        assert archive.exists()

        # 3. Удаляем исходный файл и распаковываем
        file1.unlink()
        unpack_files(archive)

        # 4. Проверяем, что файл вернулся в исходном виде
        assert file1.exists()
        assert file1.read_text(encoding="utf-8") == "print('hello')"
    finally:
        os.chdir(old_cwd)
