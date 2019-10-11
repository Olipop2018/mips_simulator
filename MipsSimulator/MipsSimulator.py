memory = [0] *4096 #Remember when ever you get an address in hex subtract 8192 from it then write to it
				#Dynamic Instruction Count
registers = {"$0": 0, "$8":0,"$9": 0, "$10":0,"$11": 0, 
                  "$12":0,"$13": 0, "$14":0,"$15": 0, "$16":0,"$17": 0, 
                  "$18":0,"$19": 0, "$20":0,"$21": 0, "$22":0,"$23": 0, "$lo":0,"$hi":0}
labelIndex = []
labelName = []
pcAssign= []
def HashAndMatch(A,B):
    for i in range(0, 5):
        tmp = A * B
        tmp= format(tmp,'064b')
        hi2=  int(tmp[:32],2)
        lo2=  int(tmp[32:],2)   
        A = hi2 ^ lo2
    A= format(A,'032b')
    C= int(A[16:32],2) ^ int(A[:16],2)
    C= format(C,'016b')
    C=  int(C[8:16],2) ^ int(C[:8],2)
   # now does pattern matachin of C
    C= format(C,'08b')
    if ('11111' in C):
        n=1
    else:
        n=0
    registers["$hi"] = n		#Shift high right 32
    registers["$lo"] = int(C,2)


def instrSimulation(instrs):
   pc = int(0)
   bcount=0
   DIC = int(0)
   j= int(0)
   while True:
        bcount+=1
       # num= len(instrs)
        if (int(pc/4) >= len(instrs)):
            print(DIC)
            return
        line = instrs[int(pc/4)]
        
        DIC+=1
        if(line[0:4] == "addi"): # ADDI/U 
            line = line.replace("addi","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op = '001001'
            else:
                op = '001000'
            line = line.split(",")
            if(line[2][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[2],n) if (int(line[2],n) >= 0 or op == '001000') else (65536 + int(line[2],n)) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
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
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[1],n) if (int(line[1],n) >= 0) else (65536 + int(line[2],n)) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rd = "$" + str(line[0]) # locate the register in which to write to
            imm = imm << 16
            registers[rd] = imm #Write upper imm to rd designation
            pc += 4# increments pc by 4 
             
            pcprint = hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

        elif(line[0:2] == "sw"): # sw
            line = line.replace("sw","")
            line = line.replace(")","")
            line = line.replace("(",",")
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[1],n) if (int(line[1],n) >= 0) else (65536 + int(line[1],n))
            rs = int(registers[("$" + str(line[2]))])
            rt = registers[("$" + str(line[0]))]
            mem = imm + rs
            mem = mem - int('0x2000', 16)
            rt= format(rt,'064b')
            first= rt[:32]
            sec= rt[32:40]
            third= rt[40:48]
            rt= rt[56:64]
            first= int(first,2)
            sec= int(sec,2)
            third= int(third,2)
            rt= int(rt,2)
            memory[mem] = rt
            mem+=1
            memory[mem] = third
            mem+=1
            memory[mem] = sec
            mem+=1
            memory[mem] = first
            pc+= 4# increments pc by 4 
             
            pcprint=  hex(pc)
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
            imm = int(line[1],n) if (int(line[1],n) >= 0) else (65536 + int(line[1],n))
            rs = int(registers[("$" + str(line[2]))])
            rt = registers[("$" + str(line[0]))]
            mem = imm + rs
            mem = mem - int('0x2000', 16)
            rt= format(rt,'08b')
            rt= int(rt,2)
            memory[mem] = rt
            pc+= 4# increments pc by 4 
            pcprint=  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)  
       
        elif(line[0:2] == "lb"): # lbu
            line = line.replace("lb","")
            line = line.replace(")","")
            line = line.replace("(",",")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op = '100100'
            else:
                op = '100000'
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[1],n) if (int(line[1],n) >= 0) else (65536 + int(line[1],n))
            rs = int(registers[("$" + str(line[2]))])
            rt = "$" + str(line[0])
            mem = imm + rs
            mem = mem - int('0x2000', 16)
            temp3 = int(memory[mem]) if (int(memory[mem]) > 0 or op == '100000') else (65536 + int(memory[mem]))
            temp3 = format(temp3, '08b')
            temp3 = int(temp3[:8],2)
            registers[rt] = temp3
            pc += 4# increments pc by 4 
             
            pcprint = hex(pc)
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
                 bcount+=1
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
                       lpos = int(labelIndex[i]-1)
                        
            temp2= (pcAssign[lpos])+4
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[0]))]
            if(rs != rt):
                temp2= temp2-pc
                pc+=temp2
            else:
                pc+= 4
             
            pcprint=  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

        elif(line[0:3] == "srl"): # SRL
            line = line.replace("srl","")
            line = line.split(",")
            rd = "$" + str(line[0])
            rt = registers[("$" + str(line[1]))]
            shamt = int(line[2])
            result = rt >> shamt 
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
            result = format(result,'064b')
            result = int(result[32:],2)
            registers[rd]= result
            pc += 4 # increments pc by 4 
            pcprint =  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)     
            
        elif(line[0:5] == "cfold"): # CFOLD
            line = line.replace("cfold","")
            line = line.split(",")
            rs = registers[("$" + str(line[1]))]	#First register
            rt = registers[("$" + str(line[2]))]	#Second register
            temp = rs * rt	#Multiply
            HashAndMatch(rt, rs)
            pc += 4# increments pc by 4 
            DIC+=1
            pcprint =  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

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
            rs= int(rs) if (int(rs) > 0 or op == '011000') else (65536 + int(rs))
            rt= int(rt) if (int(rt) > 0 or op == '011000') else (65536 + int(rt))
            temp = rs * rt	#Multiply
            temp= format(temp,'064b')
            hi=  int(temp[:32],2)
            lo=  int(temp[32:],2)
            registers["$hi"] = hi		#Shift high right 32
            registers["$lo"] = lo	#Shift low left 32
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
            registers[rs] = registers["$lo"]	#Write value to register
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
            registers[rd] = registers["$hi"]	#Write value to register
            pc += 4# increments pc by 4 
             
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

        elif(line[0:4] == "slti"): # SLTI/U
            line = line.replace("slti","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op = '001011'
            else:
                op= '001010'
            line = line.split(",")
            if(line[2][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[2],n) if (int(line[2],n) > 0 or op == '001010') else (65536 + int(line[2],n)) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to

            if(rs < imm):
                result = 1
            else:
                result = 0
            registers[rt]= result # writes the value to the register specified
            pc += 4 # increments pc by 4 
             
            pcprint = hex(pc)
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
       
        elif(line[0:3] == "add"): # ADD
            line = line.replace("add","")
            line = line.split(",")
            rd = "$" + str(line[0])
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[2]))]
            result = rs + rt # does the addition operation
            registers[rd]= result
            pc+= 4 # increments pc by 4 
             
            pcprint =  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)
        
        elif(line[0:3] == "ori"): # ori
            line = line.replace("ori","")
            line = line.split(",")
            if(line[2][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[2],n) if (int(line[2],n) > 0) else (65536 + int(line[2],n)) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            result = rs | imm # does the addition operation
            registers[rt]= result # writes the value to the register specified
            pc+= 4 # increments pc by 4 
             
            pcprint =  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)
            
        elif(line[0:4] == "andi"): # andi
            line = line.replace("andi","")
            line = line.split(",")
            if(line[2][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[2],n) if (int(line[2],n) >= 0) else (65536 + int(line[2],n)) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            result = rs & imm # does the addition operation
            registers[rt]= result # writes the value to the register specified
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
                pc= int(line[0])
               # hexstr= hex(int(hexstr[0], 2))
               # f.write(hexstr + '\n')#str('000010') + str(format(int(line[0]),'026b')) + '\n'+ hexstr+ '\n')

            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[0]):
                        lpos = int(labelIndex[i]-1)
                        
                pc= (pcAssign[lpos])+4
                        #pc= format(int(labelIndex[i]),'026b')
                        #pc = int(pc,2)
                        #hexstr= hex(int(hexstr[0], 2))
                       # f.write(hexstr+ '\n')#str('000010') + str(format(int(labelIndex[i]),'026b')) + '\n'+ hexstr+ '\n')
  

def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    ppc= 0
    for line in asm:
        line = line.replace(" ","")
        if":" in line:
            pcAssign.append(0)
        else:
            pcAssign.append(ppc)
            ppc+=4
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def main():
   # f = open("mc.txt","w+")
    h = open("testcase.asm","r")
    asm = h.readlines()
    instrs = []
   
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')
       
    saveJumpLabel(asm,labelIndex,labelName) # Save all jump's destinations
    for line in asm:
        #line = line.replace("\t","")
        #line = line.replace('"','')
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
        instrs.append(line)
       
    print(pcAssign)
    instrSimulation(instrs)
    print(memory)
    
   
   


    #f.close()

if __name__ == "__main__":
    main()
