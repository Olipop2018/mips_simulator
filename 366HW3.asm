addi $8, $0, 0x2000
addi $9, $0, 1
addi $10, $0, 255

loop_sb:
sb $9, 0($8)
addi $9, $9, 1

addi $8, $8, 1
addi $10, $10, -1 
bne $10, $0, loop_sb


subi $9,$9, 1
sb $9, 0($8)



second part starts here

addi $10, $0, 255
addi $8, $0, 0x2000
addi $9, $0, 0

loop_lb:
lb   $12, 0($8)
lb   $16, 0($8)
addi $14, $0, 0
addi $15, $0, 0
addi $11, $0, 8
loop_shft:
andi $13, $12, 1
bne $13, 0, count_1
addi $14, $14, 1
j cont
count_1:
addi $15, $15, 1
cont:
srl $12, $12, 1
addi $11, $11, -1 
bne $11, $0, loop_shft
bne $14,$15, next
addi $9, $9, 1
next:
addi $8, $8, 1
addi $10, $10, -1 
bne $10, $0, loop_lb














