def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def main():
    labelIndex = []
    labelName = []
    f = open("mc.txt","w+")
    h = open("mips.asm","r")
    asm = h.readlines()
    pc = 0
    memory = [0] *4096 #Remember when ever you get an address in hex subtract 8192 from it then write to it
    DIC = 0				#Dynamic Instruction Count
    registers = {"$0": 0, "$8":0,"$9": 0, "$10":0,"$11": 0, 
                  "$12":0,"$13": 0, "$14":0,"$15": 0, "$16":0,"$17": 0, 
                  "$18":0,"$19": 0, "$20":0,"$21": 0, "$22":0,"$23": 0, "$lo":0,"$hi":0}

    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm,labelIndex,labelName) # Save all jump's destinations
    bcount=0
    for line in asm:
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
        bcount+=1
		
        if(line[0:4] == "addi"): # ADDI/U 
            line = line.replace("addi","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op = '001001'
            else:
                op = '001000'
            line = line.split(",")
            imm = int(line[2]) if (int(line[2]) > 0 or op == '001000') else (65536 + int(line[2])) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            result = rs + imm # does the addition operation
            registers[rt]= result # writes the value to the register specified
            pc += 4# increments pc by 4 
            pcprint = hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

	elif(line[0:3] == "lui"): #lui 
            line = line.replace("lui","")
            op = '001111'
            line = line.split(",")
            imm = int(line[1]) if (int(line[1]) > 0 or op == '001000') else (65536 + int(line[2])) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rd = "$" + str(line[0]) # locate the register in which to write to
			imm = imm << 16
            registers[rd] = immm 		#Write upper imm to rd designation
            pc += 4# increments pc by 4 
            pcprint = hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

        elif(line[0:3] == "lbu"): # lbu
            line = line.replace("lbu","")
            line = line.replace(")","")
            line = line.replace("(",",")
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = format(int(line[1],n),'016b')
            rs = int(registers[("$" + str(line[2]))])
            rt = registers[("$" + str(line[0]))]
			mem = imm + rs
            mem = mem - int('0x2000', 16)
			register[rt] = memory[mem]
            pc += 4# increments pc by 4 
            pcprint = hex(pc)
			print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)
        
        elif(line[0:2] == "sb"): # sb
            line = line.replace("sb","")
            line = line.replace(")","")
            line = line.replace("(",",")
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = format(int(line[1],n),'016b') if (int(line[1],n) > 0) else format(65536 + int(line[1],n),'016b')
            rs = format(int(line[2]),'05b')
            rt = format(int(line[0]),'05b')
            
       
        elif(line[0:2] == "lw"): # lw
            line = line.replace("lw","")
            line = line.replace(")","")
            line = line.replace("(",",")
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = format(int(line[1],n),'016b') if (int(line[1],n) > 0) else format(65536 + int(line[1],n),'016b')
            rs = format(int(line[2]),'05b')
            rt = format(int(line[0]),'05b')
                
       
        elif(line[0:2] == "sw"): # sw
            line = line.replace("sw","")
            line = line.replace(")","")
            line = line.replace("(",",")
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[1],n) if (int(line[1],n) > 0) else 65536 + int(line[1],n)
            rs = int(registers[("$" + str(line[2]))])
            rt = registers[("$" + str(line[0]))]
            mem = imm + rs
            mem = mem - int('0x2000', n)
            memory[mem] = rt
            pc+= 4# increments pc by 4 
            pcprint=  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)  
       
        elif(line[0:3] == "beq"): # beq
            line = line.replace("beq","")
            line = line.split(",")
            for i in range(len(labelName)):
                    if(labelName[i] == line[2]):
                       lpos = int(labelIndex[i])- bcount if(bcount < int(labelIndex[i])) else int(labelIndex[i])-bcount
                       imm= int(lpos)
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[0]))]
            if(rs == rt):
                 pc+= 4
                 pc+= (imm << 2)
            else:
                pc+= 4
            pcprint=  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

        elif(line[0:3] == "bne"): # bne
            line = line.replace("bne","")
            line = line.split(",")
            for i in range(len(labelName)):
                    if(labelName[i] == line[2]):
                       lpos = int(labelIndex[i])- bcount if(bcount < int(labelIndex[i])) else int(labelIndex[i])-bcount
                       imm= int(lpos) 
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[0]))]
            if(rs != rt):
                 pc+= 4
                 pc+= (imm << 2)
            else:
                pc+= 4
            pcprint=  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

        elif(line[0:3] == "add"): # ADD
            line = line.replace("add","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
          
            
        elif(line[0:3] == "srl"): # SRL
            line = line.replace("srl","")
            line = line.split(",")
            rd = "$" + str(line[0])
            rt = registers[("$" + str(line[1]))]
            shamt = int(line[2])
            result = rt >> shamt # does the addition operation
            registers[rd]= result
            pc+= 4# increments pc by 4 
            pcprint=  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)
        
        elif(line[0:3] == "sll"): # SLL
            line = line.replace("sll","")
            line = line.split(",")
            rd = "$" + str(line[0])
            rt = registers[("$" + str(line[1]))]
            shamt = int(line[2])
            result = rt << shamt # does the addition operation
            registers[rd]= result
            pc += 4 # increments pc by 4 
            pcprint =  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)
                       
        elif(line[0:3] == "slt"): # SLT/U
            line = line.replace("slt","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op = '001001'
            else:
                op= '101010'
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            
            
        elif(line[0:4] == "mult"): # MULT/U
            line = line.replace("mult","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op= '011001'
            else:
                op= '011000'
            line = line.split(",")
            rs = registers[("$" + str(line[0]))]	#First register
            rt = registers[("$" + str(line[1]))]	#Second register
			
			temp = rs * rt	#Multiply
			registers[{"$hi"}] = temp << 32		#Shift high right 32
			registers[{"$hi"}] = registers[{"$hi"}] >> 32	#Shift back 32
			registers[{"$lo"}] = temp >> 32	#Shift low left 32
			
			pc += 4# increments pc by 4 
			pcprint =  hex(pc)
			print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)
			
		elif(line[0:4] == "mflo"): #MFLO
            line = line.replace("mflo","")
            op = '001010'
            line = line.split(",")
            rs = "$" + str(line[0])		#Register to write to
			registers[rs] = registers[{"$lo"}]	#Write value to register
			pc += 4# increments pc by 4 
			pcprint =  hex(pc)
			print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)
			
		elif(line[0:4] == "mfhi"): #MFHI
            line = line.replace("mfhi","")
			op = '001000'
            line = line.split(",")
            rd = "$" + str(line[0])		#Register to write to
			registers[rd] = registers[{"$hi"}]	#Write value to register
			pc += 4# increments pc by 4 
			print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

        elif(line[0:3] == "xor"): # XOR
            line = line.replace("xor","")
            line = line.split(",")
            rd = "$" + str(line[0])
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[2]))]
            result = rs ^ rt # does the addition operation
            registers[rd]= result
            pc+= 4 # increments pc by 4 
            pcprint =  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

        elif(line[0:1] == "j"): # JUMP
            line = line.replace("j","")
            line = line.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if(line[0].isdigit()): # First,test to see if it's a label or a integer
                hexstr= (str('000010') + str(format(int(line[0]),'026b'))).split()
                hexstr= hex(int(hexstr[0], 2))
                f.write(hexstr + '\n')#str('000010') + str(format(int(line[0]),'026b')) + '\n'+ hexstr+ '\n')

            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[0]):
                        hexstr= (str('000010') + str(format(int(labelIndex[i]),'026b'))).split()
                        hexstr= hex(int(hexstr[0], 2))
                        f.write(hexstr+ '\n')#str('000010') + str(format(int(labelIndex[i]),'026b')) + '\n'+ hexstr+ '\n')

        elif(line[0:6] == "ori"): # ORI 
            line = line.replace("ori","")
            op = '001101'
            line = line.split(",")
            imm = int(line[2]) if (int(line[2]) > 0 or op == '001000') else (65536 + int(line[2])) # will get the negative or positive inter value. if unsigned and nega			tive will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            result = rs | imm # does the or imm operation
            registers[rt]= result # writes the value to the register specified
            pc += 4# increments pc by 4 
            pcprint = hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

        elif(line[0:6] == "sltiu"): # SLTIU 
            line = line.replace("sltiu","")
            op = '001011'
            line = line.split(",")
            imm = int(line[2]) if (int(line[2]) > 0 or op == '001000') else (65536 + int(line[2])) # will get the negative or positive inter value. if unsigned and nega			tive will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            if(rs < imm): 
                registers[rt]= 1 # writes the value to the register specified
            else:
                registers[rt]= 0
            pc += 4# increments pc by 4 
            pcprint = hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

        elif(line[0:6] == "andi"): # ANDI 
            line = line.replace("andi","")
            op = '001100'
            line = line.split(",")
            imm = int(line[2]) if (int(line[2]) > 0 or op == '001000') else (65536 + int(line[2])) # will get the negative or positive inter value. if unsigned and nega			tive will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            result = rs & imm # does the and operation
            registers[rt]= result # writes the value to the register specified
            pc += 4# increments pc by 4 
            pcprint = hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)



    f.close()

if __name__ == "__main__":
    main()
