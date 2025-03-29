package main

import (
	"fmt"
	"encoding/json"
	"github.com/shopspring/decimal"
)

type stockInfo struct {
	StockName string `json:"stockName"`
	Quantity int `json:"qty"`
	Typ string `json:"type"`
	Value decimal.Decimal `json:"value"`
}
type transactionData struct {
	Name string `json:"name"`
	Email string `json:"email"`
	Stocks []stockInfo `json:"stocks"`
}

func ProcessMessage(msg []byte) (error,transactionData) {
	var jsonData transactionData
	err := json.Unmarshal(msg, &jsonData)
	
	if err != nil{
		fmt.Printf("Error unmarshalling json: %v", err)
		return err,jsonData
	}
	return nil,jsonData
}