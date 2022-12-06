INPUT_FILE = "input.txt"

function get_filename() 
    for i, _ in pairs(arg) do
        if i == 1 then
            return arg[1]
        end
    end
    
    return INPUT_FILE
end

filename = get_filename()
file = io.open(filename, "r")

calories, max_calories = 0, 0
for line in io.lines(filename) do
    if line == '' then
        if calories > max_calories then
            max_calories = calories
        end
        calories = 0
    else
        calories = calories + tonumber(line)
    end
end
io.close(file)
if calories > max_calories then
    max_calories = calories
end

print("ANSWER:\nPart 1: " .. max_calories)
