citydata = read.csv('/users/Sydney/CityData.csv')

library(ggplot2)
require(ggplot2)

citydata$Date = as.Date(citydata$Date, format='%m/%d/%y')

citydata2 = subset(citydata, OfficialBoolean==TRUE)

ggplot() + geom_histogram(data=citydata2, aes(x=Date))

ggplot() + geom_point(data=citydata, aes(x=BlockNS, y=BlockEW))

citydata2[29] = 

citydata$BlockNS[1]
test= toString(citydata$BlockNS[1])
test[1:(length(test)-2)]
length(test)-1

length(citydata2)

ggplot() + 
  geom_histogram(data=citydata3, aes(x=NeighborhoodWatchSigns), fill='red') + 
  geom_histogram(data=citydata2, aes(x=VacantLots), fill='blue', alpha=0.7)

ggplot() + geom_point(data=citydata, aes(x=NeighborhoodWatchSigns, y=VacantLots, color=Zipcode))
ggplot() + geom_point(data=citydata, aes(x=NeighborhoodWatchSigns, y=BoardedUp, color=Zipcode))


citydata2 = subset(citydata2, VacantLots>0)

citydata3 = subset(citydata, (OfficialBoolean==TRUE & NeighborhoodWatchSigns>0))



