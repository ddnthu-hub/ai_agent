# HỆ THỐNG HỖ TRỢ RA QUYẾT ĐỊNH KHUYẾN NGHỊ ĐẦU TƯ AI AGENT TRONG LĨNH VỰC KHOA HỌC MÁY TÍNH

## 1. Giới thiệu

Dự án xây dựng một **Hệ thống hỗ trợ ra quyết định (Decision Support System - DSS)** nhằm phân tích và khuyến nghị đầu tư AI Agent cho doanh nghiệp trong lĩnh vực Khoa học Máy tính.

Thay vì lựa chọn AI Agent theo cảm tính, hệ thống sử dụng dữ liệu từ bộ **WORKBank Dataset** kết hợp với hồ sơ doanh nghiệp để đánh giá, xếp hạng và đề xuất AI Agent phù hợp nhất với từng trường hợp cụ thể.

Hệ thống không tạo ra AI Agent mới mà tập trung vào việc hỗ trợ doanh nghiệp trả lời câu hỏi:

> **"Nên đầu tư AI Agent nào trước để đạt hiệu quả cao nhất?"**

---

## 2. Mục tiêu

Mục tiêu của dự án bao gồm:

- Phân tích đặc trưng của các tác vụ trong bộ dữ liệu WORKBank.
- Ánh xạ các tác vụ thành các nhóm AI Agent chức năng.
- Xây dựng mô hình Decision Support System hỗ trợ ra quyết định.
- Tính toán Decision Score, Confidence và ROI cho từng AI Agent.
- Xếp hạng và khuyến nghị AI Agent phù hợp với từng doanh nghiệp.
- Giải thích rõ lý do khuyến nghị nhằm tăng tính minh bạch của hệ thống.

---

## 3. Bộ dữ liệu

Nguồn dữ liệu sử dụng:

**WORKBank Dataset – Stanford University**

Các thuộc tính chính được sử dụng:

- Automation Capability
- Automation Desire
- Human Agency
- Communication Requirement
- Domain Expertise Requirement
- Involved Uncertainty

Những thuộc tính này phản ánh mức độ phù hợp của từng tác vụ đối với việc ứng dụng AI.

---

## 4. Ý tưởng của hệ thống

Trong thực tế, doanh nghiệp không lựa chọn AI theo từng tác vụ riêng lẻ mà lựa chọn theo các nhóm chức năng.

Vì vậy, dự án thực hiện quy trình:

```
WORKBank Dataset

↓

Task Feature Extraction

↓

AI Agent Mapping

↓

Business Profile

↓

Weight Generator

↓

Decision Engine

↓

Decision Score + ROI + Confidence

↓

AI Agent Ranking

↓

Final Recommendation
```

Sau bước AI Agent Mapping, các tác vụ trong WORKBank được gom thành các nhóm AI Agent có cùng chức năng nhằm phù hợp với nhu cầu triển khai thực tế của doanh nghiệp.

---

## 5. Các nhóm AI Agent

Hệ thống hiện hỗ trợ các nhóm AI Agent sau:

- Backup Agent
- Documentation Agent
- Testing Agent
- Monitoring Agent
- Database Agent
- Analytics Agent
- Code Review Copilot
- DevOps Agent
- Planning Agent
- Security Agent

---

## 6. Hồ sơ doanh nghiệp

Để cá nhân hóa kết quả, người dùng cấu hình các thông tin doanh nghiệp trước khi đánh giá.

Bao gồm:

- Mục tiêu doanh nghiệp (Business Goal)
- Chiến lược triển khai AI (AI Adoption Strategy)
- Quy mô doanh nghiệp (Company Size)
- Ngân sách đầu tư (Budget)

Các thông tin này sẽ làm thay đổi trọng số trong quá trình tính Decision Score.

---

## 7. Decision Engine

Decision Engine là thành phần trung tâm của hệ thống.

Nó có nhiệm vụ:

- Sinh trọng số dựa trên hồ sơ doanh nghiệp.
- Tính Decision Score.
- Hiệu chỉnh bằng Confidence Factor.
- Ước lượng ROI.
- Xếp hạng AI Agent.
- Đưa ra khuyến nghị đầu tư.

---

## 8. Decision Score

Decision Score được tính từ nhiều thành phần:

### Các đặc trưng từ WORKBank

- Automation Capability
- Automation Desire
- Human Agency
- Communication Requirement
- Domain Expertise Requirement
- Involved Uncertainty

### Các đặc trưng từ doanh nghiệp

- Company Size
- Budget

Sau khi tính điểm ban đầu, hệ thống nhân thêm hệ số Confidence để tạo ra Final Decision Score.

---

## 9. Confidence Factor

Do mỗi AI Agent được hình thành từ số lượng Task khác nhau nên nhóm bổ sung hệ số Confidence nhằm giảm thiên lệch thống kê.

Ví dụ:

|Số lượng Task|Confidence|
|-------------|----------|
|≥30|100%|
|20–29|98%|
|10–19|96%|
|5–9|94%|
|<5|92%|

Confidence phản ánh độ ổn định của dữ liệu chứ không phản ánh chất lượng AI Agent.

---

## 10. Estimated ROI

ROI được sử dụng như một chỉ số ước lượng hiệu quả đầu tư tương đối giữa các AI Agent.

ROI được tính dựa trên:

- Final Decision Score
- Budget Modifier
- Company Size Modifier

ROI trong dự án không đại diện cho tỷ suất lợi nhuận tài chính thực tế mà chỉ phục vụ mục đích hỗ trợ so sánh và ra quyết định.

---

## 11. Cấu trúc Dashboard

### Trang 1 – Tổng quan dữ liệu

Hiển thị:

- Thống kê bộ dữ liệu
- Danh sách AI Agent
- Phân bố các đặc trưng của Task

---

### Trang 2 – Thiết lập hệ thống

Cho phép cấu hình:

- Business Goal
- AI Adoption Strategy
- Company Size
- Budget

Đồng thời giới thiệu:

- Weight Generator
- Confidence
- Decision Score
- ROI
- Decision Flow

---

### Trang 3 – Decision Engine

Trình bày quá trình hệ thống tính toán:

- Radar Chart
- Decision Score
- Feature Contribution
- ROI Analysis

Giúp người dùng hiểu nguyên nhân điểm số thay đổi.

---

### Trang 4 – AI Agent Ranking

Hiển thị:

- Decision Score
- Estimated ROI
- Confidence
- Deployment Model
- Investment Decision

Toàn bộ AI Agent được xếp hạng theo mức độ phù hợp.

---

### Trang 5 – Final Recommendation

Tổng hợp:

- Danh sách AI Agent
- Thứ hạng
- Lý do khuyến nghị
- Lợi ích kỳ vọng
- Lưu ý triển khai

Nhằm hỗ trợ doanh nghiệp đưa ra quyết định đầu tư.

---

## 12. Công nghệ sử dụng

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

---

## 13. Cấu trúc thư mục

```
AI_AGENT_DSS/

│

├── app.py
├── dashboard.py
├── utils.py
├── requirements.txt

├── data/
│   ├── domain_worker_desires.csv
│   ├── expert_rated_technological_capability.csv
│   ├── task_statement_with_metadata.csv
│   └── domain_worker_metadata.csv

├── assets/

├── screenshots/

└── README.md
```

---

## 14. Hướng dẫn cài đặt

Clone dự án

```bash
git clone https://github.com/ddnthu-hub/ai_agent.git
```

Di chuyển vào thư mục

```bash
cd ai_agent
```

Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Chạy hệ thống

```bash
streamlit run app.py
```

---

## 15. Kết quả đạt được

Hệ thống có khả năng:

- Phân tích dữ liệu WORKBank.
- Ánh xạ Task thành AI Agent.
- Cá nhân hóa kết quả theo doanh nghiệp.
- Tính Decision Score, ROI và Confidence.
- Xếp hạng AI Agent.
- Hỗ trợ doanh nghiệp lựa chọn AI Agent ưu tiên đầu tư.
- Giải thích nguyên nhân khuyến nghị một cách minh bạch.

---

## 16. Hạn chế

- Confidence được xây dựng theo quy tắc thay vì ước lượng thống kê thực nghiệm.
- ROI chỉ là chỉ số tương đối, chưa phản ánh lợi nhuận tài chính thực tế.
- Các bảng trọng số được thiết kế dựa trên mô hình DSS và có thể tiếp tục hiệu chỉnh khi có dữ liệu doanh nghiệp thực tế.

---

## 17. Hướng phát triển

Trong tương lai, hệ thống có thể mở rộng theo các hướng:

- Học trọng số tự động bằng Machine Learning.
- Kết nối với dữ liệu doanh nghiệp thực tế.
- Tích hợp mô hình tối ưu đa mục tiêu.
- Kết hợp LLM để sinh giải thích khuyến nghị.
- Mở rộng danh mục AI Agent và lĩnh vực ứng dụng.

---

## Tác giả

Họ và tên: Võ Thị Vân Thư

Đề tài: **Hệ thống hỗ trợ ra quyết định khuyến nghị đầu tư AI Agent trong lĩnh vực Khoa học Máy tính**
