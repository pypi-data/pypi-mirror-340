def a5a():
    import pandas as pd 
    df=pd.DataFrame({'player':['A','B','C','D','E'], 
                    'game1':[18,22,19,14,14], 
                    'game2':[23,21,22,33,11], 
                    'game3':[1,22,31,23,4], 
    'game4':[1,6,3,7,6]}) 
    print(df) 
    print("\nmean\n") 
    print(df.mean(numeric_only=True)) 
    print("\nmedian\n") 
    print(df.median(numeric_only=True)) 
    print("\nmode\n") 
    print(df.mode(numeric_only=True)) 
    data=[[10,12,14],[34,53,23],[54,16,16]] 
    print("Standard Deviation\n") 
    df=pd.DataFrame(data) 
    print(df.std()) 
    print("variance\n") 
    print(df.var)



    def greet(bot_name, birth_year):    
        print("Hello! My name is {0}.".format(bot_name))   
        print("I was created in {0}.".format(birth_year))  
    def remind_name():     
        print('Please, remind me your name.')   
        name = input()     
        print("What a great name you have, {0}!".format(name))   
    def guess_age():     
        print('Let me guess your age.')    
        print('Enter remainders of dividing your age by 3, 5 and 7.')   
        rem3 = int(input())   
        rem5 = int(input())    
        rem7 = int(input())     
        age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105      
        print('Will I  Guess your Age ?')   
        print("Your age is {0}; that's a good time to start programming!".format(age))   
    def count():     
        print('Now I will prove to you that I can count to any number you want.')   
        num = int(input())       
        counter = 0      
        while counter <= num:       
            print("{0} !".format(counter))        
            counter += 1  
    def test():      
        print("Let's test your programming knowledge.") 
        print("Why do we use methods?") 
        print("1. To repeat a statement multiple times.")   
        print("2. To decompose a program into several small subroutines.")    
        print("3. To determine the execution time of a program.")     
        print("4. To interrupt the execution of a program.") 
        answer = 2    
        guess = int(input()) 
        while guess != answer:   
            print("Please, try again.")      
            guess = int(input())  
            print('Completed, have a nice day!')  
            print('.................................')  
        print('.................................')   
    def end():     
        print('Congratulations, have a nice day!')   
        print('.................................')   
        print('.................................')  
        input()     
        greet('Sbot', '2025-January')  
        remind_name()  
        guess_age()  
        count() 
        test() 
        end()
