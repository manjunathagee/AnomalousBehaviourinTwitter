#system('python twitterFriendsList.py')
library(lubridate)

dateDifference <- function(date1, date2=Sys.Date()){
 as.numeric(difftime(date2,date1,units="days"))
}


df <- read.csv('tweets.csv')


print(as.numeric(dateDifference("2018-01-02")))