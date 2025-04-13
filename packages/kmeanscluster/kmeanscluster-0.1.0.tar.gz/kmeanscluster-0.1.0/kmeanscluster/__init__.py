def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
data(iris)
names(iris)
new_data<-subset(iris,select = c(-Species))
new_data
cl<-kmeans(new_data,3)
cl
data<-new_data
wss<-sapply(1:15,function(k){kmeans(data,k)$tot.withinss})
wss
plot(1:15,wss,type="b",pch=19,frame=FALSE,xlab="Number of clustersK",ylab ="Total within-clusters sums of
squares")
library(cluster)
clusplot(new_data,cl$cluster,color=TRUE,shade=TRUE, labels=2,lines=0)
cl$cluster
cl$centers
"agglomarative clustering"
clusters<-hclust(dist(iris[,3:4]))
plot(clusters)
clusterCut<-cutree(clusters,3)
table(clusterCut,iris$Species)

    '''
    print(code)