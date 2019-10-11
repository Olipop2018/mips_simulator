lui $8, 0xFA19
ori $8, $8, 0xE366
addi $8, $0, 48
srl $9, $8, 1
bne $9, $0, sec3
sec2:
sll $8, $8, 16
addi $9, $0, 0
sec3:
bne $9, $8, sec2
addi $8, $0, 48
sw $8, 0x2000($0)
sb $8, 0x2001($0)
sb $8, 0x2002($0)
sb $8, 0x2003($0)
lb $9, 0x2002($8)
lbu $9, 0x2002($8)
addi $10, $0, -42
addiu $11, $0, -45
j sec
addi $11, $0, 45
sec:
add $9, $10, $8
sltiu $11, $8, 17
andi $11, $9, 0xFFFF
multu $11, $11
mflo $8
mfhi $9
xor $12, $8, $9
