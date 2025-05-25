package handlers

import (
    "encoding/json"
    "net/http"
    "bytes"
)

// AnswerQuestion 处理智能问答的 POST 请求
func AnswerQuestion(w http.ResponseWriter, r *http.Request) {
    var question struct {
        Text string `json:"text"`
    }

    if err := json.NewDecoder(r.Body).Decode(&question); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    // 准备输入数据
    input := map[string]interface{}{"input": []int{1, 2, 3, 4, 5}} // 示例输入数据

    // 将输入数据编码为 JSON
    inputJSON, err := json.Marshal(input)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    // 调用 Python Flask API
    resp, err := http.Post("http://localhost:5000/predict", "application/json", bytes.NewBuffer(inputJSON))
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    defer resp.Body.Close()

    // 解析响应
    var result map[string]interface{}
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]interface{}{"answer": result["output"]})
}