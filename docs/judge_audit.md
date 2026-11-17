# Judge audit

Chạy:
```bash
python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5
python -m lab9.judge --csv data/eval/judge_helpful_public.csv --audit 5
```

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có | Dùng có giới hạn cho tone trên replay; tính đúng tiền/chính sách cần grader code. |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không | Loại: bỏ sót 21/30 lỗi (recall 0.30), dù không có false positive. |

Judge lấy FAIL làm lớp dương tính. Tone có TP=24, FP=4, FN=6, TN=66; tỷ lệ lỗi quan sát 0.28, hiệu chỉnh Rogan–Gladen khoảng 0.30 (sensitivity=0.80, specificity=66/70). Helpful có TP=9, FP=0, FN=21, TN=70; tỷ lệ quan sát 0.09 nhưng hiệu chỉnh thành 0.30 (sensitivity=0.30, specificity=1.00). Kappa không xác định phải được xem là FAIL; trường hợp đó không xuất hiện trong hai bộ replay này.

## Audit bất đồng và hành động sửa rubric
| # | Bộ / case | Human | Judge | Phân tích | Hành động |
|---|---|---|---|---|---|
| 1 | tone / H-008 | FAIL | PASS | Xưng “em”, “nha” quá suồng sã trong ngữ cảnh CS. | Nêu tiêu chí xưng hô chuyên nghiệp; thêm ví dụ xưng hô không phù hợp. |
| 2 | tone / H-029 | FAIL | PASS | “Không cần nhắn thêm” mang giọng ra lệnh dù mở đầu lịch sự. | Đánh giá toàn câu; thêm tiêu chí cấm mệnh lệnh/đổ lỗi. |
| 3 | tone / H-042 | PASS | FAIL | Câu đủ thông tin nhưng judge phạt vì không xin lỗi. | Không bắt buộc xin lỗi ở mọi câu; chỉ yêu cầu khi ngữ cảnh cần. |
| 4 | tone / H-051 | PASS | FAIL | Judge phạt từ “refund” dù từ này được LogiX cho phép. | Ghi rõ từ vay mượn được duyệt không tự động làm câu thất bại. |
| 5 | tone / H-063 | FAIL | PASS | Hứa “sẽ hoàn thêm” ngoài kết quả hệ thống. | Cấm hứa khoản tiền/hành động chưa được xác nhận. |
| 6 | tone / H-081 | Nhãn cần sửa | FAIL | Ghi chú CSV cho biết nhãn human đọc nhầm ticket; judge đúng. | Đối chiếu transcript và sửa nhãn gold, không đổi judge để khớp nhãn sai. |
| 7 | helpful / HL-015 | FAIL | PASS | Reply báo 55.000đ nhưng ledger chỉ ghi 40.000đ. | Đưa số tiền ledger/nhãn vào đầu vào chấm; dùng so khớp số tiền bằng code. |
| 8 | helpful / HL-016 | FAIL | PASS | Reply báo 55.000đ, ledger 35.000đ; lời xin lỗi dài không bù lỗi tiền. | Tách kiểm tra tính đúng tiền khỏi điểm văn phong; sai tiền phải FAIL. |
| 9 | helpful / HL-020 | FAIL | PASS | Reply báo 90.000đ trong khi ledger là 120.000đ. | Bắt cả trường hợp báo thiếu tiền, không chỉ báo thừa. |
| 10 | helpful / HL-028 | FAIL | PASS | Reply báo 50.000đ nhưng ledger 35.000đ, dù câu lịch sự. | Không để độ lịch sự che lấp sai kết quả nghiệp vụ. |
| 11 | helpful / HL-047 | FAIL | PASS | “Ok bạn … nhé” sai xưng hô nhưng judge vẫn PASS. | Bổ sung tiêu chí xưng hô theo ngữ cảnh vào rubric helpful. |

## Kết luận
- **Tone: dùng có giới hạn** vì đạt cả ba sàn; các bất đồng cho thấy cần bổ sung ví dụ cho giọng ra lệnh, lời hứa và từ ngữ được phép.
- **Helpful: loại** vì recall 0.30 và κ=0.375, dù precision=1.00; judge hiện bỏ sót phần lớn câu sai tiền.
- Rủi ro còn lại: đây là replay công khai, không phải held-out độc lập. Cần nhãn người mới và đánh giá lại rubric trước khi dùng ngoài lab.
