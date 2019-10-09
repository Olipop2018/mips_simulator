#ECE-366 Project 1
#Author: Joseph Riem, Afeef

#Required commands
	lui $8, 0xFA19
	ori $8, $8, 0xE366	#$8 = B

#Code begins
	#addi $9, $0, 0x21ac	#Origin 
	addi $10, $0, 100	#Counter for 1-100 

loop_Hash:	#Loop mult/fold

HashandMatach $14, $10, $8
#XOR C into Byte 	
	
#Store

	addi $10, $10, -1	#Decrement counter/value
	bne $10, $0, loop_Hash	#If $10 /= 0 loop
#Part B begins
#Part B(ii) anaylsis
	sw $20, 0x2000($0)	#Store pattern matching
© 2019 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
