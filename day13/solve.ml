open Str

let large_error = 10_000_000_000_000

let extract_coordinates data_str =
  let re = regexp "[0-9]+" in
  let rec extract acc pos =
    try
      let _ = search_forward re data_str pos in
      let num = int_of_string (matched_string data_str) in
      extract (num :: acc) (match_end ())
    with Not_found -> List.rev acc
  in
  let values = extract [] 0 in
  let rec group lst =
    match lst with
    | a :: b :: c :: d :: e :: f :: rest -> ((a, b), (c, d), (e, f)) :: group rest
    | _ -> []
  in
  group values

let find_minimum_cost (ax, ay) (bx, by) (tx, ty) =
  let rec loop b_count lowest_cost =
    if b_count > 100 then lowest_cost
    else
      let x_left = tx - (b_count * bx) in
      let y_left = ty - (b_count * by) in
      if x_left < 0 || y_left < 0 then lowest_cost
      else if x_left mod ax = 0 then
        let a_count = x_left / ax in
        if ay * a_count = y_left then
          loop (b_count + 1) (min (3 * a_count + b_count) lowest_cost)
        else
          loop (b_count + 1) lowest_cost
      else
        loop (b_count + 1) lowest_cost
  in
  let result = loop 1 max_int in
  if result = max_int then 0 else result

let compute_part1 data_str =
  List.fold_left
    (fun acc (point_a, point_b, target) ->
      acc + find_minimum_cost point_a point_b target)
    0
    (extract_coordinates data_str)

let calculate_with_margin (ax, ay) (bx, by) (tx, ty) margin =
  let tx' = tx + margin in
  let ty' = ty + margin in
  let num = ax * bx * ty' - ay * bx * tx' in
  let denom = ax * by - ay * bx in
  let x_cross = num / denom in
  let b_count = x_cross / bx in
  let a_count = (tx' - x_cross) / ax in
  if a_count >= 0 && b_count >= 0 && ay * a_count + by * b_count = ty' && ax * a_count + bx * b_count = tx' then
    b_count + 3 * a_count
  else
    0

let compute_part2 data_str margin =
  List.fold_left
    (fun acc (point_a, point_b, target) ->
      acc + calculate_with_margin point_a point_b target margin)
    0
    (extract_coordinates data_str)

let () =
  try
    let channel = open_in "input" in
    let data_input = really_input_string channel (in_channel_length channel) in
    close_in channel;
    Printf.printf "Part 1: %d\n" (compute_part1 data_input);
    Printf.printf "Part 2: %d\n" (compute_part2 data_input large_error)
  with
  | Sys_error err -> Printf.printf "Error opening file: %s\n" err
  | End_of_file -> Printf.printf "Reached end of file unexpectedly.\n"