rm(list=ls())

library(ggplot2)
library(xtable)
library(dplyr)
library(showtext)
library(reshape2)
library(forecast)
len <- length
library(tidyr)
posix.date <- function(str){return(as.Date(as.POSIXct(str, format="%a %b %d %H:%M:%S +0000 %Y", tz="GMT") )) }


plot.dir <- getwd()

#-----------------------------------------------------

#-----------------------------------------------------
bootstrap.sentim <- function(data, R=1000){
  dates.df <- as.data.frame(unique(data$date))
  names(dates.df) <- 'date'  
  n.days <- dim(dates.df)[1]
  samps <- matrix(data=NA, n.days, R)

  for(i in 1:R){
    if(i%%50==0){print(i)}
    set.seed(i)
    samp <- data[sample(nrow(data), replace=T),]
    ag.bl <- aggregate(samp[,c('sent1')], by=list(samp$date), FUN=mean, na.rm=T)
    names(ag.bl) <- c('date','meansent1')
    # merge back to full dates:
    ag.all <- merge(ag.bl, dates.df, all=T)
    ag.all <- ag.all[order(ag.all$date),] %>% fill(meansent1) # fill forward
    ag.all <- ag.all %>% fill(meansent1, .direction='up') # back fill in case NAs at start.
    fit_ses <- ses(ag.all$meansent1, h = 6)
    samps[,i] <- fit_ses$fitted
  }
  
  pctile.stats <- matrix(data=NA, n.days, 3)
  # percentile bootstrap:
  for(i in 1:n.days){
    pctile.stats[i,] <- quantile(samps[i,], c(.05, .5, .95))
  }
  
  p.df <- as.data.frame(ag.all$date)
  p.df$p05 <- pctile.stats[,1]
  p.df$median <- pctile.stats[,2]
  p.df$p95 <- pctile.stats[,3]
  
  names(p.df) <- c("date",'95% lower bound','median','95% upper bound')
  return(p.df)
}
#-----------------------------------------------------

#-----------------------------------------------------

data.names <- c("pedagogique") # "ecolemaison"


file_in <- paste0("notext_sentiment_", data.names, ".csv") # file with estimated sentiment column

df <- read.csv(file_in)
dim(df)

# pedagogique: 1.02M
# ecole-maison 375k

names(df)[12] <- "sent1"  # need cols named 'date', "sent1"
df$date <- sapply(df$created_at, substring, 1, 10)
df$date <- as.Date(df$date)


R <- 1000 # number of replications
p.df <- bootstrap.sentim(df, R=R)

plot(p.df$date, p.df$median, type='l')
lines(p.df$date, p.df$`95% lower bound`, col='grey')
lines(p.df$date, p.df$`95% upper bound`, col='grey')

out.folder <- getwd()
write.csv(p.df, file=paste0(out.folder, "bootstrap_", which.data, ".csv"))