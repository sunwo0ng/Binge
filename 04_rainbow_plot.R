library(readr)
library(data.table)
library(rainbow)

# Load level-up history data
# interval_cum, interval, playtime_side, purchase, ads_total, death
# playtime_dungeon, playtime_tower, 
data <- read_csv("../data/rainbow_plots/interval_cum")

data = transpose(data)
data = data.matrix(data, rownames.force=seq(from=1, by=1, length.out=nrow(data)))
data_rainbow = fts(x=seq(from=1,by=1,length.out=nrow(data)),
                   y=data)

# 1100 x 700
plot(data_rainbow, plot.type="functions", plotlegend=FALSE,
     xlab="Level", ylab="Cumulative hours taken")
     # xlab="Level", ylab="Hours taken")
     # xlab="Level", ylab="In-app purchases made (in KRW)")
     # xlab="Level", ylab="Number of ads watched")
     # xlab="Level", ylab="Number of deaths experienced")
     
     # xlab="Level", ylab="Hours of playing side quests")
     # xlab="Level", ylab="Hours of playing dungeon side quests")
     # xlab="Level", ylab="Hours of playing tower side quests")