location_x = 0x7b
count_variable = 0x0
flag_address = 0x201020


while(count_variable < 0x7e4):
    location_x = ((location_x +1) * location_x) % 0x7f
    count_variable += 1

location_x = location_x * 0x40
flag_address += location_x

print(hex(flag_address))
