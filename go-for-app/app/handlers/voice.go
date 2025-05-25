package handlers

import (
    "encoding/json"
    "net/http"
    "go-for-app/ai"
	"fmt"
)

var voiceModel *ai.VoiceModel

func init() {
    // 初始化模型
    voiceModel = ai.NewVoiceModel()
    if err := voiceModel.LoadModel("models/voice_model.h5"); err != nil {
        panic(fmt.Sprintf("Failed to load Voice model: %v", err))
    }
}

// VoiceAssistant 处理语音助手的 POST 请求
func VoiceAssistant(w http.ResponseWriter, r *http.Request) {
    var request struct {
        Text string `json:"text"`
    }

    if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    // 使用语音合成模型来生成语音数据
    speechData := voiceModel.TextToSpeech(request.Text)

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"speech_data": speechData})
}