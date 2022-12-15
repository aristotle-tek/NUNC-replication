
# ---
#  based on code from: "Predicting Initial Unemployment Insurance Claims Using Google Trends"
# author: "Paul Goldsmith-Pinkham + Aaron Sojourner" - "4/1/2020"

# -- basic approach is to compare each region to a high-traffic region (e.g. CA) to have a standardized level.

# --- Note can look at youtube searches specifically

# --- NB: The gtrends.r setup changed Sept 12, 2020 - date format changed.


rm(list=ls(all=T))


library(gtrendsR)
library(tidyverse)
library(ggrepel)
library(RApiDatetime)
library(lubridate)
library(zoo)
library(knitr)
library(kableExtra)
library(patchwork)


#--------------------------
# for simple exp smooth
#--------------------------
library(forecast)
simple.exp.smooth <- function(time.series, h=6){
  fit_ses <- ses(time.series, h=h)
  return(fit_ses$fitted)
}

#----------------------

# can also do by cities - Mulhouse, Strasbourg - but only if sufficient volume.

# by region - alphabetical code.
# Alsace - 'FR-A'

library(xlsx)
cds <- read.xlsx("/Users/andrew/Dropbox/0_Poitiers/data/Fr_regions_google.xlsx", 1, stringsAsFactors=F)
regions <- cds$google
regions


pull_data = function(loc, time_window, keyword.vect, panel=FALSE) {
  if (panel==TRUE) {
    geo = c("FR-J",loc)
    res_post = gtrends(keyword=keyword.vect,  geo = geo, 
                       time = time_window, hl='fr', onlyInterest = TRUE, low_search_volume=T)
    state_data = res_post$interest_over_time %>%
      mutate(hits = as.numeric(hits)) %>%
      mutate(hits = replace_na(hits, 0))
    cutoff = dim(res_post$interest_over_time)[1]/length(geo)
    CA_max = state_data %>% filter(row_number() <= cutoff) 
    ## We do the filter thing to drop the comparison state out. 
    state_data = state_data %>% filter(row_number() > cutoff) %>% 
      group_by(geo) %>% 
      mutate(max_geo = max(hits), 
             scale = max_geo / max(CA_max$hits),
             hits = scale*hits)
    return(list(state_data = state_data))
  }
  else {
    geo = loc
    res_post = gtrends(keyword=keyword.vect,  geo = geo, 
                       time = time_window, hl='fr', onlyInterest=T, low_search_volume=T)
    state_data = res_post$interest_over_time %>%
      mutate(hits = as.numeric(hits))
    return(list(state_data = state_data))    
  }
}


# # Loop multiple times and average, following Seth's paper
num.for.avgs <- 3


keyword.vect <- c("pédagogique")


year <- '2022'

if(year=='2022'){
  time.window <- "2022-01-01 2022-12-15"
}else{
  time.window <- paste0(year, "-01-01 ", year, "-12-31")
}

print(time.window)


data_full = tibble()
for (j in seq(1,num.for.avgs)) {
  panel_data = list()
  for (i in c(1,5,9,13,16,19)) {
    print(i)
    if (i < 10) {
      panel_data[[i]] = pull_data(loc =regions[i:(i+3)], time_window=time.window, keyword.vect=keyword.vect, panel=TRUE)
    }
    else {
      panel_data[[i]] = pull_data(loc =regions[i:(i+2)], time_window=time.window, keyword.vect=keyword.vect, panel=TRUE)
    }
    Sys.sleep(3.1)
  }
  panel_data_states = list()
  for (i in seq(1,length(panel_data))) {
    panel_data_states[[i]] = panel_data[[i]]$state_data
  }
  
  # Parse data
  data_states_short = bind_rows(panel_data_states) %>%
    mutate(location = substr(geo, 4,6)) %>%
    ungroup() %>%
    select(location, hits, date) %>%
    mutate(date = ymd(date)) %>%
    group_by(location, date) %>%
    arrange(location, date)
  
  data_full = data_full %>% bind_rows(data_states_short)
  Sys.sleep(10)
}  

data_states_short = data_full %>% group_by(location, date) %>% summarize(hits = mean(hits))


file.out.pref <- ""
filename <- paste0(file.out.pref, 'gtrends_', year, '_', gsub(' ', '_', keyword.vect[1]), ".csv")
data_states_short %>% write_csv(filename)

data <- read.csv(filename, stringsAsFactors=F)

head(data)
df <-data #_states_short

cds$g.letters<- substring(cds$google, 4, 5)

g.key <- cds[,c('g.letters','nom')]

mg <- merge(df, g.key, by.x='location', by.y='g.letters', all.x=T)
head(mg)
table(mg$nom)

mg$date <- as.Date(mg$date)



library(reshape2)
c.df <- dcast(mg[,c('date','hits','nom')], date~ nom, value.var='hits')
head(c.df)
names(c.df) <- gsub(' ', '-', names(c.df))
names(c.df) <- gsub('\'', '', names(c.df))


write.csv(c.df, paste0(file.out.pref, "gtrends_", year, "_", keyword.vect[1], "_regions.csv"))

