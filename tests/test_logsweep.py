import logsweep
from logsweep import main, sweep


def test_log_total_error(tmp_log_dir):
    total_error = sweep(tmp_log_dir)

    assert total_error == 4


def test_log_total_with_empty_logs(tmp_log_dir_with_empty_logs):
    total_error = sweep(tmp_log_dir_with_empty_logs)

    assert total_error == 0


def test_log_dir_with_no_files(tmp_path, capsys):
    sweep(tmp_path)

    printed = capsys.readouterr()

    assert "no log files here" in printed.out


def test_sweep_reading_logs(tmp_log_dir, capsys):
    sweep(tmp_log_dir)

    printed = capsys.readouterr()

    assert "log-1.log" in printed.out
    assert "log-2.log" in printed.out
    assert "log-3.log" in printed.out


def test_sweep_prints_correct_counts_per_file(tmp_log_dir, capsys):
    sweep(tmp_log_dir)
    printed = capsys.readouterr()

    log_1_expected_line = "  %-16s %3d info %3d warn %3d error" % (
        "log-1.log", 4, 1, 1)
    log_2_expected_line = "  %-16s %3d info %3d warn %3d error" % (
        "log-2.log", 4, 0, 0)
    log_3_expected_line = "  %-16s %3d info %3d warn %3d error" % (
        "log-3.log", 2, 1, 3)

    assert log_1_expected_line in printed.out
    assert log_2_expected_line in printed.out
    assert log_3_expected_line in printed.out


def test_sweep_everything_should_be_ignored_except_logs(tmp_log_dir_with_non_log_file, capsys):
    total = sweep(tmp_log_dir_with_non_log_file)
    printed = capsys.readouterr()

    # means the those files are not read
    assert "log-4.txt" not in printed.out
    assert "log-5.md" not in printed.out
    assert total == 4


def test_sweep_prints_worst_file_correctly(tmp_log_dir, capsys):
    sweep(tmp_log_dir)
    printed = capsys.readouterr()

    assert "worst file: log-3.log" in printed.out


def test_sweep_prints_worst_file_that_comes_first_when_tied(tmp_log_dir_with_tie_error, capsys):
    sweep(tmp_log_dir_with_tie_error)
    printed = capsys.readouterr()

    assert "worst file: log-1.log" in printed.out


def test_sweep_total_errors_and_files_read(tmp_log_dir, capsys):
    sweep(tmp_log_dir)
    printed = capsys.readouterr()

    assert "4 errors across 3 files" in printed.out


def test_entry_point_message_if_missing_directory():
    exit_code = main(["logsweep.py"])

    assert exit_code == 2


def test_entry_point_if_arg_is_not_a_directory(tmp_path, capsys):
    exit_code = main(["logsweep.py", str(tmp_path / "nosuchthing")])
    printed = capsys.readouterr()

    assert exit_code == 1
    assert "not a directory: " in printed.out


def test_entry_point_returns_1_if_sweep_has_errors(tmp_path, monkeypatch):
    def fake_sweep(directory):
        return 4  # simulating sweep using tmp_log_dir fixture

    monkeypatch.setattr(logsweep, "sweep", fake_sweep)

    exit_code = logsweep.main(["logsweep.py", str(tmp_path)])
    assert exit_code == 1


def test_entry_point_returns_0_if_sweep_has_no_errors(tmp_path, monkeypatch):
    def fake_sweep(directory):
        return 0  # simulating sweep that has no error

    monkeypatch.setattr(logsweep, "sweep", fake_sweep)

    exit_code = logsweep.main(["logsweep.py", str(tmp_path)])
    assert exit_code == 0
