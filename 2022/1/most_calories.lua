INPUT_FILE = "input.txt"


function get_filename() 
    for i, _ in ipairs(arg) do
        if i == 1 then
            return arg[1]
        end
    end
    
    return INPUT_FILE
end


META_ELF = {
    __tostring = function(mytable)
        res, sep = "Elf(", ""
        for k, v in pairs(mytable) do
            res = res .. sep .. k .. "=" ..v
            sep = ", "
        end
        return res .. ")"
    end, 

    __lt = function(mytable, othertable)
        return mytable.calories < othertable.calories
    end
}


function new_elf(id, calories)
    elf = {id=id, calories=calories}
    return setmetatable(elf, META_ELF)
end

filename = get_filename()
file = io.open(filename, "r")

elf = new_elf(1, 0)
elfs = {elf}
for line in io.lines(filename) do
    if line == '' then
        table.insert(elfs, elf)
        elf = new_elf(elf.id + 1, 0)
    else
        elf.calories = elf.calories + tonumber(line)
    end
end
io.close(file)
table.insert(elfs, elf)
table.sort(elfs)
max3 = {elfs[#elfs], elfs[#elfs-1], elfs[#elfs-2]}
sum_of_max_3 = 0
for _, v in ipairs(max3) do
    sum_of_max_3 = sum_of_max_3 + v.calories
end

print("ANSWER:\nPart 1: " .. elfs[#elfs].calories)
print("Part 2: " .. sum_of_max_3)
-- print("(" .. tostring(elfs[#elfs]) .. ")")
