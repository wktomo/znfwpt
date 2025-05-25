package ai

import (
	"go-for-app/models" // 引入模型库代码
)

type QAModel struct {
	model *models.QAModel
}

func NewQAModel() *QAModel {
	return &QAModel{
		model: models.NewQAModel(),
	}
}

func (qa *QAModel) LoadModel(modelFile string) error {
	return qa.model.LoadModel(modelFile)
}

func (qa *QAModel) AnswerQuestion(question string) string {
	return qa.model.Predict(question)
}