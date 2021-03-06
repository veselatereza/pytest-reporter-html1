import re

from bs4 import BeautifulSoup


pytest_plugins = ["pytester"]


def test_sample_report(testdir, pytestconfig):
    testdir.makeini([
        "[pytest]",
        "python_files=sample_*.py",
        "markers =",
        "   static_mark",
        "   dynamic_mark",
        "   mark_with_args",
    ])
    testdir.copy_example("samples")
    testdir.copy_example("../screenshot.png")

    report = "{}/report/report.html".format(pytestconfig.rootdir)
    result = testdir.runpytest(
        "--log-level=DEBUG",
        "--template=html1/index.html",
        "--report=" + report
    )
    testdir.runpytest(
        "--template=html1/index.html",
        "--split-report",
        "--report={}/report/split_report.html".format(pytestconfig.rootdir)
    )
    assert result.ret == 1
    with open(report) as fp:
        soup = BeautifulSoup(fp, "html.parser")

    sample_outcomes = soup.find(
        string=re.compile(r"sample_outcomes\.py")
    ).find_parent("details")
    counts = sample_outcomes.find_all(class_="count")
    # failed, passed, error, xfailed, xpassed, skipped
    assert len(counts) == 6
    # 1 test of each
    for count in counts:
        assert count.string == "1"
