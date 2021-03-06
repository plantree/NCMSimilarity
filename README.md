# NCMSimilarity（网易云音乐相似度计算）

写着玩，碰巧看到了一个计算文本相似度的公式，恰好网易云音乐有听歌的历史记录，故而想着将二者结合起来，通过采集不同用户的听歌记录，然后计算他们的相似度。

##### 数据部分
网易云音乐有类似REST API的接口，根据用户ID来辨识，如：
>  http://music.163.com/#/user/home?id=xxxxxxxx

但是也有不好的一面，比如都将内容放在一个嵌套的frame里，或许是反爬机制吧，另外数据也基本是通过AJAX生成，因此，毫无疑问，用selenium来实现。

##### 算法部分
协同过滤（CF）作为推荐系统中常用的算法固然很好，但是很难拿到那么大的样本集，就选择简单直白的VSM（Vector Space Model）中的余弦相似度的算法，实现起来相当容易。这里尤其需要注意的是weight的选择，常用的TF-IDF模型无法使用，我的解决策略是：*根据歌曲的排名（这个数据在采集的时候一块获得），重新分成10类，越靠前，权重越大，这其中也起到了归一化的作用。*

[可执行文件](https://github.com/plantree/NCMSimilarity/releases/tag/v1.0-beta)

***
###### References:
1. https://www.jianshu.com/p/edf666d3995f
2. http://www.ruanyifeng.com/blog/2013/03/tf-idf.html
