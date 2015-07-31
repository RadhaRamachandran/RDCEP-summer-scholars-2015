## read a csv
crime = read.csv('/users/annablinderman/downloads/Past_Year.csv')

## plotting in R: http://docs.ggplot2.org/current/
library(ggplot2)
require(ggplot2)

## basic histogram
ggplot(data=crime, aes(x=District)) + geom_histogram(binwidth=2) 

## basic scatterplot
ggplot(data=crime, aes(x=District, y=Beat)) + geom_point() 

## best fit lines and their slopes
  + geom_smooth(method='lm', se=FALSE, formula = y~x) 
lm(Beat ~ District, crime14)

## subsets 
crime14 = subset(crime, Year == 2014)
crime15 = subset(crime, Year == 2015)
crime_theft = subset(crime, Primary.Type == 'THEFT')

## overplotting
ggplot() +
  geom_point(data=crime14, aes(x=District, y=Beat)) +
  geom_point(data=crime15, aes(x=District, y=BeatY))

## show frequency of each variable in a column
test = as.data.frame(table(crime$Primary.Type))
View(test)

## convert to datetime: https://www.stat.berkeley.edu/~s133/dates.html
as.Date(crime$Date, format='%m/%d/%y h:m')


## examples of writing functions (remember globals!)

addNumbers <<- function(oneNumber, anotherNumber) {
  myAnswer <<- oneNumber + anotherNumber
}

doubleNumber <<- function(myNumber) {
  answer <<- 2*myNumber
}

addNumbers(2, 3)
doubleNumber(4)
answer


## HI SETH (pie charts): http://www.statmethods.net/graphs/pie.html
