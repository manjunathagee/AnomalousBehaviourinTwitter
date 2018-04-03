#------------------Library Imports--------------------------------------------------#
library(dplyr)
library(lubridate)
#-----------------------------------------------------------------------------------#

#------------------Functions Declartions------------------------------------------------#

computeUserTotalTweets <- function(){
  processedTwitterDS <<- mutate(df, totalTweets = count(df, 'screen_name'))
}

computeFriendShipRatio <- function(){
  
}

computeFavoriteCountRatio <- function(){
  
}

computeTweetRatio <- function(){
  
}

computeLanguageRatio <- function(){
  
}


#-----------------------------------------------------------------------------------#

#------------------Utility Functions------------------------------------------------#

#Utility function which will look for any null/Empty values for mandatory columns and removes the corresponding row 
preprocesssTwitterDS <- function(){
  
  if(any(is.na(df[, "created_at"]))){
    df <- df[!(is.na(df$created_at) | df$created_at == ""), ]
  }
  
  if(any(is.na(df[, "text"]))){
    df <- df[!(is.na(df$text) | df$text==""), ]
  }
  
  if(any(is.na(df[, "favorite_count"]))){
    df <- df[!(is.na(df$favorite_count) | df$favorite_count == ""), ]
  }
  
  if(any(is.na(df[, "followers_count"]))){
    df <- df[!(is.na(df$followers_count) | df$followers_count==""), ]
  }
  
  if(any(is.na(df[, "friends_count"]))){
    df <- df[!(is.na(df$friends_count) | df$friends_count==""), ]
  }
  
  if(any(is.na(df[, "user_created_at"]))){
    df <- df[!(is.na(df$user_created_at) | df$user_created_at==""), ]
  }
  
  if(any(is.na(df[, "tweet_language"]))){
    df <- df[!(is.na(df$tweet_language) | df$tweet_language==""), ]
  }
  
  #compute user longevity
  computeUserLongevity()
  
}

#Utility function returns the difference in days between two date objects
# @param1 - date object one
# @param2 - date object two
# @return - differnce between two date objects in terms of days
dateDifference <- function(date1, date2=Sys.Date()){
  as.numeric(difftime(date2,date1,units="days"))
}

#Utility function which will compute user longevity for each user and adds it as new column
computeUserLongevity <- function(){
  processedTwitterDS <<- mutate(df, userLongevity = round(dateDifference(ymd_hms(user_created_at))))
}

#-----------------------------------------------------------------------------------#

#------------------Main Function--------------------------------------------------#

main <- function(){
  originalTwitterDS <- read.csv('tweets.csv')
  
  #make a copy of original data, not recommended to work on raw dataset
  df <- originalTwitterDS
  
  preprocesssTwitterDS()
  
  
  computeUserTotalTweets()
  computeFriendShipRatio()
  computeFavoriteCountRatio()
  computeTweetRatio()
  computeLanguageRatio()
  
}

main()

#-----------------------------------------------------------------------------------#

