def a3a():
    import pandas as pd

    # Create the DataFrame
    data = pd.DataFrame({
        'player': ['A', 'B', 'C', 'D', 'E'],
        'game1': [18, 22, 10, 14, 17],
        'game2': [5, 7, 9, 3, 6],
        'game3': [1, 8, 10, 6, 4],
        'game4': [9, 8, 10, 9, 3]
    })

    print("To create data\n")
    print(data)

    # Save the DataFrame to a CSV file
    data.to_csv('sample.csv', index=False)

    print("\nTo load data\n")
    df = pd.read_csv('sample.csv')
    print(df)



    bar
    temperature<-c(45,56,23,77,99) 
    print(temperature) 
    result<-barplot(temperature) 
    result<-barplot(temperature,main="maximum temperature in a week",xlab="degree 
    celcius",ylab="day") 
    result<-barplot(temperature,main="maximum temperature in a week",xlab="degree 
    celcius",ylab="day",names.arg = c("sunday","monday","tuesday","wednesday","thursday")) 


    scatter

    salary1 <- c(3500, 5400, 1700, 3700, 2500) 
    salary2 <- c(5000, 1500, 5000, 2300, 7000) 
    plot(salary1, salary2, xlab = "Salary of Ahalya", ylab = "Salary of Selvaraj", main = "Comparing Salary 
    of Ahalya and Selvaraj", pch = 19)

    piechart

    expenditure <- c(45,77,8,12,43) 
    result<-pie(expenditure) 
    result<-pie(expenditure,main="expenditure of the 
    week",labels=c("groceries","eb","savings","fees","food")) 
    result<-pie(expenditure,main="expenditure of the 
    week",labels=c("groceries","eb","savings","fees","food"),col=c("Blue","Pink","Red","Yellow","White"
    )) 

