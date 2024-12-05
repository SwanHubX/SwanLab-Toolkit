from swankit.callback.models import key as K
from swankit.core import ChartType


def test_column_info():
    c = K.ColumnInfo(
        key="a/1",
        kid="b",
        name="c",
        cls="SYSTEM",
        section_name="e",
        section_sort=1,
        section_type="PUBLIC",
        chart_type=ChartType.TEXT,
        chart_reference="STEP",
        error=None,
        config=None,
    )
    assert c.got is None
    assert c.key == "a/1"
    assert c.kid == "b"
    assert c.name == "c"
    assert c.cls == "SYSTEM"
    assert c.section_name == "e"
    assert c.section_sort == 1
    assert c.chart_type == ChartType.TEXT
    assert c.chart_reference == "STEP"
    assert c.section_type == "PUBLIC"
    assert c.error is None
    assert c.config is None
    assert c.key_encode == "a%2F1"


def test_metric_info():
    c = K.ColumnInfo(
        key="a/1",
        kid="b",
        name="c",
        cls="SYSTEM",
        section_name="e",
        section_sort=1,
        chart_type=ChartType.TEXT,
        section_type="PUBLIC",
        chart_reference="STEP",
        error=None,
        config=None,
    )

    m = K.MetricInfo(
        column_info=c,
        metric={"data": 1},
        metric_buffers=None,
        metric_summary={"data": 1},
        metric_file_name="1.log",
        metric_step=1,
        metric_epoch=1,
        swanlab_logdir=".",
        swanlab_media_dir=".",
    )
    assert m.column_info.got is None
    assert m.column_info.key == "a/1"
    assert m.column_info.kid == "b"
    assert m.column_info.name == "c"
    assert m.column_info.cls == "SYSTEM"
    assert m.column_info.section_name == "e"
    assert m.column_info.section_sort == 1
    assert m.column_info.chart_type == ChartType.TEXT
    assert m.column_info.chart_reference == "STEP"
    assert m.column_info.section_type == "PUBLIC"
    assert m.column_info.error is None
    assert m.column_info.config is None
    assert m.column_info.key_encode == "a%2F1"
    assert m.column_info.got is None
    assert m.column_info.expected is None
    assert m.column_info.key_encode == "a%2F1"
    assert m.column_info.key == "a/1"
    assert m.column_info.kid == "b"
    assert m.metric == {"data": 1}
    assert m.metric_buffers is None
    assert m.metric_summary == {"data": 1}
    assert m.metric_step == 1
    assert m.metric_epoch == 1
    assert m.swanlab_media_dir == "."
    assert m.metric_file_path == f"./{c.kid}/1.log"
