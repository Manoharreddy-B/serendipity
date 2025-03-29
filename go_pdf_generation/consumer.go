package main

import (
	"fmt"
	"log"
	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
)

func main() {
	config :=  &kafka.ConfigMap{
		"bootstrap.servers": "localhost:9092", // Kafka broker address
		"group.id":          "my-consumer-group", // Consumer group
		"auto.offset.reset": "earliest",
	}

	consumer, err := kafka.NewConsumer(config)
	if err != nil {
		log.Fatalf("Failed to create consumer: %v", err)
	}

	defer consumer.Close()

	topic := "pdf_gen"
	err = consumer.Subscribe(topic,nil)
	if err != nil {
		log.Fatalf("Failed to subscribe to topic: %v", err)
	}

	fmt.Println("Listening messages on topic:", topic)
	
	var i = 0
	for {
		msg, err := consumer.ReadMessage(-1)
		if err!=nil {
			fmt.Println("Kafka polling error")
		}
		go generatePdf(consumer, msg, i)
		i += 1
	}
	fmt.Println("Consumer is closed")
	
}

func generatePdf(consumer *kafka.Consumer, msg *kafka.Message, userId int) {
	err,jsonData := ProcessMessage(msg.Value)
	if err != nil {
		fmt.Println(err)
	} else {
		err := createPdf(jsonData, userId)
		if err == nil{
			fmt.Println("PDF successfully generated", userId)
		} else {
			fmt.Println("Error occured while generating PDF")
		}
	}
}

