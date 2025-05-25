package handlers

import (
    "encoding/json"
    "fmt"
    "net/http"
	"github.com/gorilla/mux"
    "go-for-app/app/services" // 导入 services 包
    "go-for-app/utils"        // 导入 utils 包
)

type LoanHandler struct {
    service *services.LoanService
}

// NewLoanHandler 创建一个新的 LoanHandler 实例
func NewLoanHandler(service *services.LoanService) *LoanHandler {
    return &LoanHandler{service: service}
}

// NewLoanService 创建一个新的 LoanService 实例
func NewLoanService() *services.LoanService {
    return services.NewLoanService()
}

// CreateLoanApplication 处理创建贷款申请的 POST 请求
func (lh *LoanHandler) CreateLoanApplication(w http.ResponseWriter, r *http.Request) {
    var loanApp struct {
        FarmerID      string  `json:"farmer_id"`
        FarmerName    string  `json:"farmer_name"`
        FarmerLocation string `json:"farmer_location"`
        CropType      string  `json:"crop_type"`
        LoanAmount    float64 `json:"loan_amount"`
        LoanTerm      int     `json:"loan_term"`
    }

    // 解码请求体中的 JSON 数据
    if err := json.NewDecoder(r.Body).Decode(&loanApp); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    // 生成 UUID 用于贷款申请
    uuidGenerator, err := utils.NewUUID()
    if err != nil {
        http.Error(w, "Failed to generate UUID", http.StatusInternalServerError)
        return
    }
    loanID := uuidGenerator.Generate()

    // 调用服务层处理贷款申请
    if err := lh.service.ProcessLoanApplication(loanApp, loanID); err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusCreated)
    fmt.Fprintf(w, "Loan application created successfully with ID: %s", loanID)
}

// GetLoanApplication 处理获取贷款申请的 GET 请求
func (lh *LoanHandler) GetLoanApplication(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    loanID := vars["id"]

    loanDetails, err := lh.service.GetLoanDetails(loanID)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(loanDetails)
}