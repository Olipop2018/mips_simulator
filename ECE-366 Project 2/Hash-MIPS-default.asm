lui $8, 0xFA19
ori $8, $8, 0xE366
addi $9, $0, 0x21ac
addi $10, $0, 100
addi $11, $0, 5
addi $14, $10, 0
addi $18, $0, 4
addi $19, $0, 0
addi $20, $0, 0
addi $21, $0, 0
addi $23, $0, 1
loop_mult:
multu $14, $8
mflo $12
mfhi $13
xor $14, $13, $12
addi $11, $11, -1
bne $11, $0, loop_mult
addi $11, $0, 5
addi $15, $0, 0x2000
srl $16, $14, 16
andi $14, $14, 0xFFFF
xor $14, $16, $14
srl $16, $14, 8
andi $14, $14, 0xFF
xor $14, $16, $14
addi $19, $14, 0
loop_pm:
sltiu $21, $19, 0xf8
addi $18, $18, -1
sll $19, $19, 1
sw $19, 0x201c($0)
lbu $19, 0x201c($0)
bne $21, $23, skip_s
bne $18, $0, loop_pm
bne $18, $23, skip_fr
skip_s: 
addi $20, $20, 1
skip_fr: 
sw $14, 0($9)
addi $9, $9, -4
addi $10, $10, -1
addi $14, $10, 0
addi $18, $0, 4
bne $10, $0, loop_mult
sw $20, 0x2008($0)