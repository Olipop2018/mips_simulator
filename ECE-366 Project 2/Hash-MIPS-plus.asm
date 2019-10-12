lui $8, 0xFA19
ori $8, $8, 0xE366
addi $9, $0, 0x21ac 
addi $10, $0, 100
addi $14, $10, 0
addi $20, $0, 0
loop_mult:
cfold $14, $8, $14
mtlo $14
sw $14, 0($9)
mthi $12
add $20, $12, $20
addi $9, $9, -4
addi $10, $10, -1
addi $14, $10, 0
bne $10, $0, loop_mult
sw $20, 0x2008($0)