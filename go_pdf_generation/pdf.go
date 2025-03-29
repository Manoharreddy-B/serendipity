package main 

import (
	"fmt"
	"strings"
	"io/ioutil"
	"os/exec"
	"bytes"
	"os"
)

func convertTupleToString(stock_info []stockInfo) string{
	var stocksString []string

	for _,stock := range stock_info {
		stockStr := fmt.Sprintf(`("%s", %d, "%s", %s)`, stock.StockName, stock.Quantity, stock.Typ, stock.Value.StringFixed(2))
		stocksString = append(stocksString, stockStr)
	}

	return strings.Join(stocksString, ",\n ")
}

func createPdf(data transactionData, user_id int) error {

	generated_report := "generated_report_" + data.Name + ".ttyp"
	report := "report_" + data.Name + ".pdf"
	typst_template, err := ioutil.ReadFile("report.ttyp")

	if err != nil{
		return fmt.Errorf("There's an error mate!")
	} else {

		typst_content := string(typst_template)
		
		trans := map[string]string{
			"[NAME]" : data.Name,
			"[EMAIL]" : data.Email,
			"[STOCKS]" : convertTupleToString(data.Stocks),
		}
			
		for field, value := range trans {
			typst_content = strings.ReplaceAll(typst_content, field, value)
		}

		err = os.WriteFile(generated_report, []byte(typst_content), 0644)
		if err != nil {
			fmt.Println(err)
			return nil
		}
		
		cmd := exec.Command("typst", "compile", generated_report, report)

		var stdout, stderr bytes.Buffer
		cmd.Stdout = &stdout
		cmd.Stderr = &stderr

		err = cmd.Run()
		if err != nil {
			fmt.Println("Error :", err)
			fmt.Println("Std error :", stderr.String())
			return err

		}
			
	}
	return nil
}

