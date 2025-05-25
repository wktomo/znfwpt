package ai

import (
	"go-for-app/models" // 引入模型库代码
)

type VoiceModel struct {
	model *models.VoiceModel
}

func NewVoiceModel() *VoiceModel {
	return &VoiceModel{
		model: models.NewVoiceModel(),
	}
}

func (vm *VoiceModel) LoadModel(modelFile string) error {
	return vm.model.LoadModel(modelFile)
}

func (vm *VoiceModel) TextToSpeech(text string) string {
	return vm.model.TextToSpeech(text)
}

func (vm *VoiceModel) SpeechToText(audioBase64 string) string {
	return vm.model.SpeechToText(audioBase64)
}