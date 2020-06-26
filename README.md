# PageRank Graph Model

A model for understanding Google's PangeRank algorithm, based upon the concepts of Graph Theory.

PageRank is the algorithm Google uses to sift through the absurd amounts of web pages out there, so that in search results you and I see only the most important and useful information related to our search.

## How Graph Theory Relates to PageRank

If there's two things that the Internet does well, it's:

1. **Storing** Information, and
2. **Connecting** people with that information

As it turns out, graphs are an optimal data structure to model the Web. Why? 

This is because graphs **are also great** at:

- **storing data** in objects called **vertices**,
- and **connecting** vertices together using **edges**

More specifically, here are further details to specify the graph data structure we will use in this project:

- The graph in this case, will be represent all web pages on the Internet. Will be implemented using the ```Internet``` class.
- Individual vertices in the graph are represented by the ```Page``` class.
- **Edges** between the pages **represent hyperlinks** on the Internet.
- **Edges are weighted**, in order to **represent the credibility** that Google assigns to links that come from certain websites, as opposed to others.
- **Edges are directed**. This is because **hyperlinks are one-way connections**. ```Page A``` may link to ```Page B``` for example, but the reverse is not necessarily true.


## Investigation

In this project, we will take a look at several problems that Google uses the PageRank algorithm to solve, and modelling their solutions in code based upon the Graph ADT.

The problems are as follows:

1. ```pass```
2. ```pass```
3. ```pass```

## Resources

For more information explaining how PageRank works, and why you should care (as either a user or web developer), please checkout [this awesome article on Search Engine Land](https://searchengineland.com/what-is-google-pagerank-a-guide-for-searchers-webmasters-11068).
