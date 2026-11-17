# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Case M1 — T02 dùng số ngày trong ticket

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`; cùng claim/seed đối chứng bằng shape `fixed`. |
| Triệu chứng | Agent hoàn 20.000đ dù nhãn yêu cầu `denied`, refund 0đ. |
| Bước sai đầu tiên | Event 3 `model_override`: ghi `delay_days=5`, trong khi event 2 đọc DB `delay_days=2`. |
| Vì sao là bước *đầu tiên* | Handoff và lookup ở event 1–2 giữ đúng claim, principal và dữ kiện đơn hàng. Sai lệch bắt đầu khi ticket thay thế dữ kiện DB. |
| Failure mode | FM-03 `ticket_trust`. |
| Đối chứng | `fixed C-002@11` không có `model_override`, quote 0đ, trạng thái `denied`, ledger 0đ. |
| Regression test | `test_seeded_regression_trace_identifies_ticket_override` trong `tests/test_lab9_trace_case.py`; kiểm tra override và đối chứng `fixed`. |
| Chưa chắc chắn | Trace chứng minh nguyên nhân trong trial này; không khẳng định mọi claim/seed bị lỗi giống nhau. |

Trace chính: event 4 quote 20.000đ; event 6 reply 20.000đ; ledger 20.000đ, nhãn 0đ. Reply khớp ledger nhưng cả hai đều sai so với nhãn.

## Mẫu điền (mỗi nhóm 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `<shape> <claim>@<seed>`, run ID trong report |
| Triệu chứng | Grader nào fail; reply nói gì so với ledger ghi gì |
| Bước sai đầu tiên | Số thứ tự event + kind + trích payload (≤1 dòng) |
| Vì sao là bước *đầu tiên* | Các bước trước đó đúng ra sao (dẫn số event) |
| Failure mode | Mã FM-xx trong `docs/failure_taxonomy.md` |
| Đối chứng | Cùng claim@seed trên shape `fixed`: bước đó khác thế nào |
| Regression test | Tên test + grader/assert nào bắt được; đã thấy fail trên variant lỗi và pass trên `fixed` chưa |
| Chưa chắc chắn | Điều trace không chứng minh được |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
