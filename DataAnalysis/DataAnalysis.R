getwd()

#default setting
#install.packages("ggplot2", repos="http://cran.nexr.com/")
library(ggplot2)
#install.packages("dplyr")
library(dplyr)
#install.packages("tidyr")
library(tidyr)
#install.packages("jsonlite)
library(jsonlite)
#install.packages("NbClust")
library(NbClust)


#key : 서버에서 사용자마다 주는 key값
key <- "7bded40948c00c1e951a773b4b70c687"
#https://sandbox-api.brewerydb.com/v2/
base_url <- "http://api.brewerydb.com/v2"
key_preface <- "/?key="

get_beer <- function(id) {
  fromJSON(paste0(base_url, "/beer/", id, "/", key_preface, key))
}

#모든 페이지의 값 불러오기

paginated_request <- function(trace_progress = TRUE) {
  full_request <- NULL
  first_page <- fromJSON(paste0(base_url, "/beers", key_preface, key, "&p=",1))
  number_of_pages <- ifelse(!(is.null(first_page$numberOfPages)), first_page$numberOfPages)      
  
  for (page in 1:number_of_pages) {                               
    this_request <- fromJSON(paste0(base_url, "/beers", key_preface, key, "&p=", page),flatten = TRUE) 
    full_request <- bind_rows(full_request, this_request$data)
  }
  bind_rows(full_request, this_request$data)
  return(full_request)
}

brewery_raw<-paginated_request()

write.csv(
  brewery_raw,              # 파일에 저장할 데이터 프레임 또는 행렬
  file="brewery_raw.csv",        # 데이터를 저장할 파일명
  row.names=TRUE  # TRUE면 행 이름을 CSV 파일에 포함하여 저장한다.
)

brewery_raw<-read.csv(
  file="brewery_raw.csv",          # 파일명
  header=TRUE,  # 파일의 첫 행을 헤더로 처리할 것인지 여부
  # 데이터에 결측치가 포함되어 있을 경우 R의 NA에 대응시킬 값을 지정한다.
  # 기본값은 "NA"로, "NA"로 저장된 문자열들은 R의 NA로 저장된다.
  na.strings="NA",
  # 문자열을 팩터로 저장할지 또는 문자열로 저장할지 여부를 지정하는 데 사용한다. 별다른
  # 설정을 하지 않았다면 기본값은 보통 TRUE다.
  stringsAsFactors=default.stringsAsFactors()
)
brewery_raw<-brewery_raw[,c(2:59)]

#clustering
names(brewery_raw)
#id,ibu,ibv,srm,icon
brewery_numeric<-brewery_raw[,c(1,2,36:41,22:24)]
#delete NA
brewery_numeric2<-brewery_numeric[complete.cases(brewery_numeric),]

write.csv(
  brewery_numeric2,              # 파일에 저장할 데이터 프레임 또는 행렬
  file="brewery_numeric.csv",        # 데이터를 저장할 파일명
  row.names=TRUE  # TRUE면 행 이름을 CSV 파일에 포함하여 저장한다.
)


brewery_numeric2<-read.csv(
  file="brewery_numeric.csv",          # 파일명
  header=TRUE,  # 파일의 첫 행을 헤더로 처리할 것인지 여부
  # 데이터에 결측치가 포함되어 있을 경우 R의 NA에 대응시킬 값을 지정한다.
  # 기본값은 "NA"로, "NA"로 저장된 문자열들은 R의 NA로 저장된다.
  na.strings="NA",
  # 문자열을 팩터로 저장할지 또는 문자열로 저장할지 여부를 지정하는 데 사용한다. 별다른
  # 설정을 하지 않았다면 기본값은 보통 TRUE다.
  stringsAsFactors=default.stringsAsFactors()
)
brewery_numeric2<-brewery_numeric2[,c(2:12)]

brewery_numeric3<-brewery_numeric2

IBU<-(brewery_numeric3$style.ibuMin+brewery_numeric3$style.ibuMax)/2
ABV<-(brewery_numeric3$style.abvMin+brewery_numeric3$style.abvMax)/2
SRM<-(brewery_numeric3$style.srmMin+brewery_numeric3$style.srmMax)/2

brewery_3comp<-data.frame(brewery_numeric3[,c(2)],IBU,ABV,SRM,brewery_numeric3[,c(9:11)])

#new data
brewery_new<-read.csv(
  file="brew_add.csv",          # 파일명
  header=TRUE,  # 파일의 첫 행을 헤더로 처리할 것인지 여부
  # 데이터에 결측치가 포함되어 있을 경우 R의 NA에 대응시킬 값을 지정한다.
  # 기본값은 "NA"로, "NA"로 저장된 문자열들은 R의 NA로 저장된다.
  na.strings="NA",
  # 문자열을 팩터로 저장할지 또는 문자열로 저장할지 여부를 지정하는 데 사용한다. 별다른
  # 설정을 하지 않았다면 기본값은 보통 TRUE다.
  stringsAsFactors=default.stringsAsFactors()
)


brewery_new<-brewery_new[,c(2,10,9,11,12:14)]
names(brewery_new)<-names(brewery_3comp)
brewery_3comp<-rbind(brewery_3comp,brewery_new)

#scaling
brewery_scale<-scale(brewery_3comp[,c(2:4)],center=TRUE,scale=TRUE)
summary(brewery_scale)

#validation_1
nc <- NbClust(brewery_scale, min.nc=2, max.nc=20, method="kmeans")
par(mfrow=c(1,1))
barplot(table(nc$Best.n[1,]),
        xlab="Numer of Clusters", ylab="Number of Criteria",
        main="Number of Clusters Chosen")

#validation_2

wssplot <- function(data, nc=20, seed=1234){
  wss <- (nrow(data)-1)*sum(apply(data,2,var))
  for (i in 2:nc){
    set.seed(seed)
    wss[i] <- sum(kmeans(data, centers=i)$withinss)}
  plot(1:nc, wss, type="b", xlab="Number of Clusters",
       ylab="Within groups sum of squares")}

wssplot(brewery_scale)

#cluster
clusters_out <- kmeans(x = brewery_scale, centers = 19)
cluster_b19<-cbind(cluster_assignment=factor(clusters_out$cluster),brewery_3comp)
qplot(IBU, ABV, colour = cluster_assignment, data = cluster_b19)


write.csv(
  cluster_b19,              # 파일에 저장할 데이터 프레임 또는 행렬
  file="cluster_b19.csv",        # 데이터를 저장할 파일명
  row.names=TRUE  # TRUE면 행 이름을 CSV 파일에 포함하여 저장한다.
)




clusters_raw<-read.csv(
  file="brewery_raw.csv",          # 파일명
  header=TRUE,  # 파일의 첫 행을 헤더로 처리할 것인지 여부
  # 데이터에 결측치가 포함되어 있을 경우 R의 NA에 대응시킬 값을 지정한다.
  # 기본값은 "NA"로, "NA"로 저장된 문자열들은 R의 NA로 저장된다.
  na.strings="NA",
  # 문자열을 팩터로 저장할지 또는 문자열로 저장할지 여부를 지정하는 데 사용한다. 별다른
  # 설정을 하지 않았다면 기본값은 보통 TRUE다.
  stringsAsFactors=default.stringsAsFactors()
)



