from swankit.callback.models import key as K
from swankit.core import ChartType


def test_column_info():
    c = K.ColumnInfo(
        key="a/1",
        key_id="b",
        key_name="c",
        key_class="SYSTEM",
        section_name="e",
        section_sort=1,
        chart_type=ChartType.TEXT,
        chart_reference="step",
        error=None,
        config=None,
    )
    assert c.got is None
    assert c.key == "a/1"
    assert c.key_id == "b"
    assert c.key_name == "c"
    assert c.key_class == "SYSTEM"
    assert c.section_name == "e"
    assert c.section_sort == 1
    assert c.chart_type == ChartType.TEXT
    assert c.chart_reference == "step"
    assert c.error is None
    assert c.config == {}
    assert c.key_encode == "a%2F1"


def test_metric_info():
    c = K.ColumnInfo(
        key="a/1",
        key_id="b",
        key_name="c",
        key_class="SYSTEM",
        section_name="e",
        section_sort=1,
        chart_type=ChartType.TEXT,
        chart_reference="step",
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
    assert m.column_info.key_id == "b"
    assert m.column_info.key_name == "c"
    assert m.column_info.key_class == "SYSTEM"
    assert m.column_info.section_name == "e"
    assert m.column_info.section_sort == 1
    assert m.column_info.chart_type == ChartType.TEXT
    assert m.column_info.chart_reference == "step"
    assert m.column_info.error is None
    assert m.column_info.config == {}
    assert m.column_info.key_encode == "a%2F1"
    assert m.column_info.got is None
    assert m.column_info.expected is None
    assert m.column_info.key_encode == "a%2F1"
    assert m.column_info.key == "a/1"
    assert m.column_info.key_id == "b"
    assert m.metric == {"data": 1}
    assert m.metric_buffers is None
    assert m.metric_summary == {"data": 1}
    assert m.metric_step == 1
    assert m.metric_epoch == 1
    assert m.swanlab_media_dir == "."
    assert m.metric_file_path == f"./{c.key_id}/1.log"
