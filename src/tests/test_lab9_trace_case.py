from lab8.trace import Trace
from lab9.trace_case import investigate


def test_seeded_regression_trace_identifies_ticket_override(tmp_path, monkeypatch):
    original_init = Trace.__init__

    def init_in_tmp_path(self, run_id, directory="traces"):
        original_init(self, run_id, tmp_path / "traces")

    monkeypatch.setattr(Trace, "__init__", init_in_tmp_path)

    regression = investigate("seeded_regression", "C-002", 11)
    control = investigate("fixed", "C-002", 11)
    regression_trial = regression["trial"]
    control_trial = control["trial"]

    override = next(event for event in regression_trial["events"] if event["kind"] == "model_override")
    investigator = next(event for event in regression_trial["events"] if event["kind"] == "investigator")

    assert investigator["payload"]["lookup_order"]["order"]["delay_days"] == 2
    assert override["payload"]["delay_days"] == 5
    assert regression_trial["snapshot"]["refund_vnd"] == 20000
    assert regression["label"]["refund_vnd"] == 0
    assert control_trial["result"]["status"] == "denied"
    assert control_trial["snapshot"]["refund_vnd"] == 0
