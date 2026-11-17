# Eval card — LogiX-VN refund agent

Card này đi kèm báo cáo và là căn cứ so sánh ở Day 10.

- **Run ID / eval-set SHA:** baseline `E-swarm-20261117-4e77`; PR `E-swarm-20261117-4e77`; eval-set SHA `4e776a9fb3ed`.
- **Phiên bản:** code và graders tại PR head `starter/d09`; eval set v1; metric spec 1.0; MockLLM; Python 3.14.10; seeds 11/22/33/44/55.
- **Eval set:** 14 item × 5 seed, nguồn `lab8_public`; nhãn tách tại `data/eval/labels_v1.json`.
- **Metric & ngưỡng:** `approval_bypass=0`, `secret_leak=0`; `refund_amount_correct≥0.95` và không giảm có ý nghĩa; `reply_amount_correct≥0.95`; `pass_rate≥0.85` và không giảm có ý nghĩa. Theo dõi: `db_fact_kept≥0.95`, `pass_5≥0.80`, `cost_per_success` tăng không quá 10%.
- **Baseline vs PR:** cùng shape `swarm`; `pass_rate=0.9857`, `refund_amount_correct=0.9857`, `reply_amount_correct=1.0`, `approval_bypass=0`, `secret_leak=0`. Paired Δ cho refund/pass rate là `+0.000`, CI 95% `[+0.000, +0.000]`; gate exit 0.
- **Gate demonstration:** `fixed` đạt `pass_rate=1.0`, exit 0. `seeded_regression` đạt `pass_rate=0.7143`, exit 1; bị chặn bởi `refund_amount_correct`, `reply_amount_correct` và `pass_rate`.
- **Judge:** tone đạt κ=0.757, P=0.857, R=0.800; chỉ dùng có giới hạn cho tone. Helpful bị loại: κ=0.375, R=0.300.
- **Trace case:** [trace_case.md](./trace_case.md), sai lệch đầu tiên ở event 3 `model_override`; regression test `test_seeded_regression_trace_identifies_ticket_override`.
- **Gate owner:** người nộp/maintainer của fork `K5-L3A-DAY09-KieuVanThang-2A202603424-EvaluationandFailureAnalysis`; chỉ merge khi job `eval-gate` xanh.
- **Phạm vi pilot:** replay offline bằng MockLLM trên public claim set; không phải triển khai cho khách hàng.
- **Giới hạn / bằng chứng còn thiếu:** 14 item và 5 seed; judge dùng CSV replay công khai; chưa đo trên người dùng hoặc model thật. M5–M7 là phần Advanced/Expert, chưa thuộc phạm vi Core M0–M4.
- **Khi nào tăng eval-set version:** thêm claim/trace hoặc failure mode mới, thay đổi phân phối dữ liệu hay nhãn; tăng phiên bản, chạy lại baseline và ghi provenance trước khi dùng làm gate.
