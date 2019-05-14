def analysis(av):
##1.+ Г-1 Гипертимые хЗ (умножить значение на 3) + 1, 11, 23, 33, 45, 55, 67, 77, -: нет 
##2.+ Г-2 Застревание х2 + : 2,15,24,34,37,56,68,78,81, -: 12,46, 59 
##3.+ Г-3 Эмотивные х3 + : 3, 13, 35, 47, 57, 69, 79, -: 25 
##4.+ Г-4 Педантичные х2+:4,14,17,26,39,48,58,61,70,80,83,- :36 
##5.+ Г-5 Тревожные х3 +: 16, 27, 38, 49, 60, 71, 82, -: 5 
##6.+ Г-6 Циклотивные х3 + : 6, 18, 28, 40, 50, 62, 72, 84, -: нет
##7.+ 1.Демонстративность: +:7, 19, 22, 29, 41, 44, 63, 66, 73, 85, 88. -:51
##8.+ Г-8 Возбудимость х3 +: 8,20,30,42,52,64,74,86, -: нет 
##9.+ Г-9 Дистимные х3 + : 9, 21, 43, 75, 87, - : 31, 53, 65 
##10.+ Г-10 Экзальтированные х6 + : 10, 32, 54, 76, -: нет
    results={}
    hyperthymic_p=av[0]+av[10]+av[22]+av[32]+av[44]+av[54]+av[66]+av[76]
    hyperthymic=hyperthymic_p*3
    results['Z73.1.hyperthymic']=hyperthymic
    
    stuck_p=av[1]+av[14]+av[23]+av[33]+av[36]+av[55]+av[67]+av[77]+av[80]
    stuck_n= 3-(av[11]+av[45]+av[58])
    stuck=(stuck_p+stuck_n)*2
    results['Z73.1.stuck']=stuck
    
    emotive_p=av[2]+av[12]+av[34]+av[46]+av[56]+av[68]+av[78]
    emotive_n=1-av[24]
    emotive = (emotive_p+emotive_n)*3
    results['Z73.1.emotive']=emotive
    
    pedantic_p=av[3]+av[13]+av[16]+av[25]+av[38]+av[47]+av[57]+av[60]+av[69]+av[79]+av[82]
    pedantic_n=1-av[35]
    pedantic = (pedantic_p+pedantic_n)*2
    results['Z73.1.pedantic']=pedantic
    
    disturbing_p=av[15]+av[26]+av[37]+av[48]+av[59]+av[70]+av[81]
    disturbing_n=1-av[4]
    disturbing=(disturbing_p+disturbing_n)*3
    results['Z73.1.disturbing']=disturbing
    
    cyclic_p=av[5]+av[17]+av[27]+av[39]+av[49]+av[61]+av[71]+av[83]
    cyclic=cyclic_p*3
    results['Z73.1.cyclic']=cyclic
    
    demonstrative_p=av[6]+av[18]+av[21]+av[28]+av[40]+av[43]+av[62]+av[65]+av[72]+av[84]+av[87]
    demonstrative_n=av[50]
    demonstrative=(demonstrative_p+demonstrative_n)*2
    results['Z73.1.demonstrative']=demonstrative
    
    excitable_p=av[7]+av[19]+av[29]+av[41]+av[51]+av[63]+av[73]+av[85]
    excitable =excitable_p*3
    results['Z73.1.excitable']=excitable
    
    distimal_p=av[8]+av[20]+av[42]+av[74]+av[86]
    distimal_n=3-(av[30]+av[52]+av[64])
    distimal=(distimal_p+distimal_n)*3
    results['Z73.1.distimal']=distimal
    
    exalted_p=av[9]+av[31]+av[53]+av[75]
    exalted=exalted_p*6
    results['Z73.1.exalted']=exalted

    accentuations=[]
    for key in results.keys():
        if results[key]>19:
            accentuations.append(key)
    if len(accentuations)<=0:
        accentuations.append(max(results, key=results.get))
    return accentuations

