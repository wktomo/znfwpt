package middleware

import (
	"net/http"
)

// CORSOptions 定义跨域选项
type CORSOptions struct {
	AllowedOrigins   string
	AllowedMethods   string
	AllowedHeaders   string
}

// CORSMiddleware 创建一个跨域处理中间件
func CORSMiddleware(options CORSOptions) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			// 设置允许的头部
			w.Header().Set("Access-Control-Allow-Origin", options.AllowedOrigins)
			w.Header().Set("Access-Control-Allow-Methods", options.AllowedMethods)
			w.Header().Set("Access-Control-Allow-Headers", options.AllowedHeaders)

			// 处理 OPTIONS 预检请求
			if r.Method == "OPTIONS" {
				w.WriteHeader(http.StatusOK)
				return
			}

			// 调用下一个处理程序
			next.ServeHTTP(w, r)
		})
	}
}