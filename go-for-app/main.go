package main

import (
	"fmt"
	"net/http"
	"github.com/gorilla/mux"
	"go-for-app/app/handlers"
	"go-for-app/app/middleware"
	"go-for-app/utils" // 引入 utils 包
)

func main() {
	// 创建 UUID 生成器
	uuidGenerator, err := utils.NewUUID()
	if err != nil {
		fmt.Printf("Error creating UUID generator: %v\n", err)
		return
	}

	// 生成一个 UUID 并打印
	loanID := uuidGenerator.Generate()
	fmt.Printf("Generated UUID for loan: %s\n", loanID)

	// 初始化路由器
	router := mux.NewRouter()

	// 初始化服务
	loanService, err := initializeLoanService()
	if err != nil {
		fmt.Printf("Error initializing loan service: %v\n", err)
		return
	}

	// 定义跨域选项
	corsOptions := middleware.CORSOptions{
		AllowedOrigins:   "*", // 允许所有来源，实际应用中应限制为信任的域
		AllowedMethods:   "GET, POST, OPTIONS",
		AllowedHeaders:   "Origin, Content-Type, Accept",
	}

	// 创建跨域中间件
	corsMiddleware := middleware.CORSMiddleware(corsOptions)

	// 包装路由器
	handler := corsMiddleware(router)

	// 注册路由
	registerRoutes(router, loanService)

	// 启动服务器
	fmt.Println("Starting server on :8080")
	if err := http.ListenAndServe(":8080", handler); err != nil {
		fmt.Printf("Server startup failed: %v\n", err)
	}
}

// registerRoutes 注册所有路由
func registerRoutes(router *mux.Router, loanService *handlers.LoanHandler) {
    // 贷款申请相关路由
    router.HandleFunc("/api/loans", loanService.CreateLoanApplication).Methods("POST")
    router.HandleFunc("/api/loans/{id}", loanService.GetLoanApplication).Methods("GET")

    // 智能问答路由
    router.HandleFunc("/api/questions", handlers.AnswerQuestion).Methods("POST")

    // 语音辅助路由
    router.HandleFunc("/api/voice_assistant", handlers.VoiceAssistant).Methods("POST")
}

// initializeLoanService 初始化贷款服务
func initializeLoanService() (*handlers.LoanHandler, error) {
	// 创建贷款服务
	loanService := handlers.NewLoanService()

	// 创建贷款处理器
	loanHandler := handlers.NewLoanHandler(loanService)

	return loanHandler, nil
}