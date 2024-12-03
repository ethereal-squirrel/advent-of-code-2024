package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func main() {
	file, err := os.Open("../input")
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var corruptedMemory string
	for scanner.Scan() {
		corruptedMemory += scanner.Text()
	}
	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	mulRegex := regexp.MustCompile(`mul\((\d+),(\d+)\)`)
	doRegex := regexp.MustCompile(`do\(\)`)
	dontRegex := regexp.MustCompile(`don't\(\)`)

	matches := mulRegex.FindAllStringSubmatchIndex(corruptedMemory, -1)
	doMatches := doRegex.FindAllStringIndex(corruptedMemory, -1)
	dontMatches := dontRegex.FindAllStringIndex(corruptedMemory, -1)
	enabled := true
	totalSum := 0
	nextDo := 0
	nextDont := 0

	for _, match := range matches {
		for nextDo < len(doMatches) && doMatches[nextDo][0] < match[0] {
			enabled = true
			nextDo++
		}
		for nextDont < len(dontMatches) && dontMatches[nextDont][0] < match[0] {
			enabled = false
			nextDont++
		}

		if enabled {
			x, _ := strconv.Atoi(corruptedMemory[match[2]:match[3]])
			y, _ := strconv.Atoi(corruptedMemory[match[4]:match[5]])
			totalSum += x * y
		}
	}

	fmt.Printf("Total sum: %d\n", totalSum)
}
