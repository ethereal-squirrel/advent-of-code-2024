#!/bin/bash

input_file="input"
rules=()
updates=()

while IFS= read -r line; do
    if [[ "$line" == *"|"* ]]; then
        rules+=("$line")
    elif [[ -n "$line" ]]; then
        updates+=("$line")
    fi
done < "$input_file"

is_correctly_ordered() {
    local update=("$@")
    local -A index_map

    for i in "${!update[@]}"; do
        index_map[${update[i]}]=$i
    done

    for rule in "${rules[@]}"; do
        IFS='|' read -r x y <<< "$rule"
        if [[ -n "${index_map[$x]}" && -n "${index_map[$y]}" ]]; then
            if (( index_map[$x] >= index_map[$y] )); then
                return 1
            fi
        fi
    done
    return 0
}

middle_pages_sum=0
for update in "${updates[@]}"; do
    IFS=',' read -r -a update_array <<< "$update"
    if is_correctly_ordered "${update_array[@]}"; then
        middle_index=$(( ${#update_array[@]} / 2 ))
        middle_pages_sum=$(( middle_pages_sum + update_array[middle_index] ))
    fi
done

echo "Correctly ordered updates: $middle_pages_sum"