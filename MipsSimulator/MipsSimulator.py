def saveJumpLabel(asm,labelIndex, labelName):
    8lineCount = 0
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
    registers = {"$0": 0, "$8":0,"$9": 0, "$10":0,"$11": 0, 
                  "$12":0,"$13": 0, "$14":0,"$15": 0, "$16":0,"$17": 0, 
                  "$18":0,"$19": 0, "$20":0,"$21": 0, "$22":0,"$23": 0, "$lo":0,"hi":0}
	
	memory = [0] *4096 #Remember when ever you get an address in hex subtract 8192 from it then write to it
    
	DIC = 0				#Dynamic Instruction Count
	
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
               op= '001001'
            else:
                op= '001000'
            line = line.split(",")
            imm = int(line[2]) if (int(line[2]) > 0 or op == '001000') else (65536 + int(line[2])) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            result = rs + imm # does the addition operation
            registers[rt]= result # writes the value to the register specified
            pc+= 4# increments pc by 4 
            pcprint=  hex(pc)
            print(registers)# print all the registers and their values (testing purposes to see what is happening)
            print(pc)
            print(pcprint)

           # hexh = (str(op) + str(rs) + str(rt) + str(imm)).split()
           # hexh= hex(int(hexh[0], 2))
           # f.write(hexh + '\n')#str(op) + str(rs) + str(rt) + str(imm) + '\n'+ hexh+ '\n')


        elif(line[0:2] == "lb"): # lb
            line = line.replace("lb","")
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
            hexh = (str('100000') + str(rs) + str(rt) + str(imm)).split()
            hexh= hex(int(hexh[0], 2))
            f.write( hexh + '\n')#str('100000') + str(rs) + str(rt) + str(imm) + '\n'+ hexh+ '\n')
        
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
            hexh = (str('101000') + str(rs) + str(rt) + str(imm)).split()
            hexh= hex(int(hexh[0], 2))
            f.write(hexh + '\n')#str('101000') + str(rs) + str(rt) + str(imm) + '\n'+ hexh+ '\n')        
       
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
            hexh = (str('100011') + str(rs) + str(rt) + str(imm)).split()
            hexh= hex(int(hexh[0], 2))
            f.write( hexh + '\n')#str('100011') + str(rs) + str(rt) + str(imm) + '\n'+ hexh+ '\n')        
       
        elif(line[0:2] == "sw"): # sw
            line = line.replace("sw","")
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
            hexh = (str('101011') + str(rs) + str(rt) + str(imm)).split()
            hexh= hex(int(hexh[0], 2))
            f.write( hexh + '\n')#str('101011') + str(rs) + str(rt) + str(imm) + '\n'+ hexh+ '\n')        
       
        elif(line[0:3] == "beq"): # beq
            line = line.replace("beq","")
            line = line.split(",")
            for i in range(len(labelName)):
                    if(labelName[i] == line[2]):
                       lpos = int(labelIndex[i])- bcount if(bcount < int(labelIndex[i])) else int(labelIndex[i])-bcount
                       imm= format(int(lpos),'016b') if (int(lpos) > 0) else format(65536 + int(lpos),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            hexh = (str('000100') + str(rt)+str(rs) + str(imm)).split()
            hexh= hex(int(hexh[0], 2))
            f.write(hexh + '\n')#str('000100') + str(rs) + str(rt) + str(imm) + '\n'+ hexh+ '\n')
       
        elif(line[0:3] == "bne"): # bne
            line = line.replace("bne","")
            line = line.split(",")
            for i in range(len(labelName)):
                    if(labelName[i] == line[2]):
                       lpos = int(labelIndex[i])- bcount if(bcount < int(labelIndex[i])) else int(labelIndex[i])-bcount
                       imm= format(int(lpos),'016b') if (int(lpos) > 0) else format(65536 + int(lpos),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            hexh = (str('000101') + str(rt)+ str(rs) +  str(imm)).split()
            hexh= hex(int(hexh[0], 2))
            f.write(hexh + '\n')#str('000101') + str(rs) + str(rt) + str(imm) + '\n'+ hexh+ '\n')

        elif(line[0:3] == "add"): # ADD
            line = line.replace("add","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            hexh = (str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000')).split()
            hexh= hex(int(hexh[0], 2))
            hexh= format(int(hexh, 16), '08x' )
            f.write('0x'+ hexh + '\n')#str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000') + '\n' + '0x'+hexh+ '\n')
            
        elif(line[0:3] == "srl"): # SRL
            line = line.replace("srl","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            shamt = format(int(line[2]),'05b')
            hexh = (str('000000') + str('00000') + str(rt) + str(rd) + str(shamt+'000010')).split()
            hexh= hex(int(hexh[0], 2))
            hexh= format(int(hexh, 16), '08x' )
            f.write('0x'+ hexh + '\n')#str('000000') + str('00000') + str(rt) + str(rd) + str(shamt +'000010') + '\n' + '0x'+hexh+ '\n')
                       
        elif(line[0:3] == "slt"): # SLT/U
            line = line.replace("slt","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op= '001001'
            else:
                op= '101010'
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            hexh = (str('000000') + str(rs) + str(rt) + str(rd) + str('00000'+op)).split()
            hexh= hex(int(hexh[0], 2))
            hexh= format(int(hexh, 16), '08x' )
            f.write('0x'+ hexh + '\n')#str('000000') + str(rs) + str(rt) + str(rd) + str('00000'+ op) + '\n' + '0x'+hexh+ '\n')
            
        elif(line[0:4] == "mult"): # MULT/U
            line = line.replace("mult","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op= '011001'
            else:
                op= '011000'
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            hexh = (str('000000') + str(rs) + str(rt) + str('0000000000'+ op)).split()
            hexh= hex(int(hexh[0], 2))
            hexh= format(int(hexh, 16), '08x' )
            f.write('0x'+ hexh + '\n')#str('000000') + str(rs) + str(rt) + str('0000000000'+ op) + '\n' + '0x'+hexh+ '\n')
            
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



    f.close()

if __name__ == "__main__":
    main()
