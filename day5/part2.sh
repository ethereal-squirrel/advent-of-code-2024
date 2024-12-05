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

order_update() {
    local update=("$@")
    local ordered_update=()
    local -A dependencies

    for page in "${update[@]}"; do
        dependencies[$page]=0
    done

    for rule in "${rules[@]}"; do
        IFS='|' read -r x y <<< "$rule"
        if [[ " ${update[*]} " == *" $x "* && " ${update[*]} " == *" $y "* ]]; then
            ((dependencies[$y]++))
        fi
    done

    while [[ ${#ordered_update[@]} -lt ${#update[@]} ]]; do
        for page in "${update[@]}"; do
            if [[ ${dependencies[$page]} -eq 0 ]]; then
                ordered_update+=("$page")
                dependencies[$page]=-1
                for rule in "${rules[@]}"; do
                    IFS='|' read -r x y <<< "$rule"
                    if [[ $x -eq $page && " ${update[*]} " == *" $y "* ]]; then
                        ((dependencies[$y]--))
                    fi
                done
            fi
        done
    done

    echo "${ordered_update[@]}"
}

middle_pages_sum=0
for update in "${updates[@]}"; do
    IFS=',' read -r -a update_array <<< "$update"
    if ! is_correctly_ordered "${update_array[@]}"; then
        ordered_update=($(order_update "${update_array[@]}"))
        middle_index=$(( ${#ordered_update[@]} / 2 ))
        middle_pages_sum=$(( middle_pages_sum + ordered_update[middle_index] ))
    fi
done

echo "Incorrectly ordered updates: $middle_pages_sum"