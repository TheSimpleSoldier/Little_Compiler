# This program converts IR to tiny 

IRCode = [[ 'LABEL', 'main'],
          [ 'LINK' ],
          [ 'STOREI', '20', '$T1' ],
          [ 'STOREI', '$T1', 'a'  ],
          [ 'STOREI', '30', '$T2' ],
          [ 'STOREI', '$T2', 'b'  ],
          [ 'STOREI', '40', '$T3' ],
          [ 'STOREI', '$T3', 'c'  ],
          [ 'MULTI', 'a', 'b', '$T4' ],
          [ 'MULTI', 'a', 'b', '$T5' ],
          [ 'ADDI',  '$T5', 'c', '$T6' ],
          [ 'DIVI', '$T6', 'a', '$T7' ],
          [ 'STOREI', '20', '$T8' ],
          [ 'ADDI', 'c', '$T4', '$T9' ],
          [ 'ADDI', '$T9', '$T7', '$T10' ],
          [ 'ADDI', '$T10', '$T8', '$T11' ],
          [ 'STOREI', '$T11', 'c' ],
          [ 'MULTI', 'b', 'b', '$T12' ],
          [ 'ADDI', '$T12', 'a', '$T13' ],
          [ 'STOREI', '$T13', 'b' ],
          [ 'MULTI', 'b', 'a', '$T14' ],
          [ 'DIVI', '$T14', 'a', '$T15' ],
          [ 'STOREI', '$T15', 'a' ],
          [ 'WRITEI', 'c' ],
          [ 'WRITEI', 'b' ],
          [ 'WRITEI', 'a' ],
          [ 'RET' ],
          ]


        

def converter(IRCode):
    instructions = []
    count = 0
    varList = []
    varCount = 0
    for v in IRCode:
        if v[0] == 'MULTI':
            var1 = v[1]
            if "$" in var1:
                var1 = "r" + str(int(var1[2:]) - 1)
            var2 = v[2]
            if "$" in var2:
                var2 = "r" + str(int(var2[2:]) - 1)
            
            instructions.append("move " + var1 + " " + "r" + str(count))
            instructions.append("muli " + var2 + " " + "r" + str(count))
            count += 1

        if v[0] == 'ADDI':
            var1 = v[1]
            if "$" in var1:
                var1 = "r" + str(int(var1[2:]) - 1)
            var2 = v[2]
            if "$" in var2:
                var2 = "r" + str(int(var2[2:]) - 1)

            instructions.append("move " + var1 + " " + "r" + str(count))
            instructions.append("addi " + var2 + " " + "r" + str(count))
            count += 1

        if v[0] == 'DIVI':
            var1 = v[1]
            if "$" in var1:
                var1 = "r" + str(int(var1[2:]) - 1)
            var2 = v[2]
            if "$" in var2:
                var2 = "r" + str(int(var2[2:]) - 1)
            instructions.append("move " + var1 + " " + "r" + str(count))
            instructions.append("divi " + var2 + " " + "r" + str(count))
            count += 1

        if v[0] == 'WRITEI':
            instructions.append("sys writei " + v[1])

        if v[0] == 'RET':
            instructions.append("sys halt")

        if v[0] == 'STOREI': 
            if "$" in v[2]:
                instructions.append("move " + v[1] + " " + "r" + str(count))
                count += 1
            else:
                if v[2] in varList:
                    value = v[1]
                    if "$T" in value:
                        value = "r" + str(int(value[2:]) - 1)
                    instructions.append("move " + value + " " + v[2])
                
                else:
                    varList.append(v[2])
                    instructions.insert(varCount, "var " + v[2])
                    varCount += 1
                    value = v[1]

                    if "$T" in value:
                        value = "r" + str(int(value[2:]) - 1)

                    instructions.append("move " + value + " " + v[2])
                    
    for i in instructions:
        print i

converter(IRCode)            


