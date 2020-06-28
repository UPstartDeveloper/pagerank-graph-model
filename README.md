# PageRank Graph Model

A model for understanding Google's PangeRank algorithm, based upon the concepts of Graph Theory.

PageRank is the algorithm Google uses to sift through the absurd amounts of web pages out there, so that in search results you and I see only the most important and useful information related to our search.

![Google 'G' on a chalkboard with computer science on it](https://i.postimg.cc/FHcdKh7y/Screen-Shot-2020-06-26-at-5-59-40-PM.png)
Credits to Danny Sullivan, on Search Engine Land for the above image ([link to original site](https://searchengineland.com/what-is-google-pagerank-a-guide-for-searchers-webmasters-11068)).

## Table of Contents

1. [How Graph Theory Relates to PageRank](#how-graph-theory-relates-to-pagerank)
2. [How the Model is Structured](#how-the-model-is-structured)
3. [The ```Internet``` Class](#the-internet-class)
4. [The ```Page``` Class](#the-page-class)
5. [Problems To Investigate](#problems-to-investigate)
    - [Calculating the PageRank Rating for each Page in a Network](#calculating-the-pagerank-rating-for-each-page-in-a-network)
    - [Determining Which Pages Can Be Reached After Clicking N links Away from a Starting Page](#determining-which-pages-can-be-reached-after-clicking-n-links-away-from-a-starting-page)
    - [Finding the Shortest Path Required to Get From One Page to Another](#finding-the-shortest-path-required-to-get-from-one-page-to-another)
6. [Resources](#resources)

## How Graph Theory Relates to PageRank

If there's two things that the Internet does really well, it's:

1. **Storing** Information, and
2. **Connecting** people with that information

As it turns out, graphs are an optimal data structure to model the Web. Why?

This is because graphs **are also great** at:

- **storing data** in objects called **vertices**,
- and **connecting** vertices together using **edges**

More specifically, here are further details to specify the graph data structure we will use in this project:

- The graph in this case, will be represent all web pages on the Internet. Will be implemented in Python using the ```Internet``` class.
- Individual vertices in the graph are implemented by the ```Page``` class.
- Not all ```Page``` instances in the graph are necessarily connected.
- **Edges** between the pages **represent hyperlinks** on the Internet.
- **Edges are weighted**, in order to **represent the probability** that a user goes from a certain site to another.
- **Edges are directed**. This is because **hyperlinks are one-way connections**. ```Page A``` may link to ```Page B``` for example, but the reverse is not necessarily true.

## How the Model is Structured

The model is structured using Object-Orientated Programming. The properties and instance methods of the ```Page``` and ```Internet``` classes are below.

### The ```Internet``` Class

A representation of the World Wide Web. This class is a *composition* of many ```Page``` instances.

#### Attributes of ```Internet```

- ```dict: pages```: this dictionary maps the ```id``` attribute of each ```Page``` instance, to the ```Page``` instance itself.

#### Methods of ```Internet```

*This section currently under construction*.

### The ```Page``` Class

A representation of a single web page.

#### Attributes of ```Page```

- ```str: id```: a unique name for the web page
- ```dict: neighbors```: this dictionary represents the other ```Page``` instances that can be reached using hyperlinks from this web page. The dictionary maps the ```id``` attribute of the other ```Page``` instances, to the other ```Page``` object.
- ```float: link_weight``` is the weight that each edge from this ```Page``` instance carries. This attribute of the edge represents the probability a site visitor goes to any one of the neighboring sites linked by this ```Page``` instance. It is calculated as by dividing 100%, by the number of ```neighbors``` that page has. For example, if a ```Page``` has 2 ```neighbors``` that it links *towards* (aka its "outlinks"), then each of the ```weight``` values for those edges will be 0.50.

#### Methods of ```Page```

*This section currently under construction*.

## Problems To Investigate

In this project, we will take a look at several problems that Google uses the PageRank algorithm to solve, and modelling their solutions in code based upon the Graph ADT.

**The problems are as follows:**

### Calculating the PageRank Rating for each Page in a Network

This problem is an application of an algorithm similar to the **Floyd-Warshall** algorithm

We will implement a function that will take one **parameter**:

- an ```Internet``` instance

which will **return** a ```rankings``` array of pages, each element being a tuple of the ```Page.id```; as well as a ranking between 1-10, where 1 is the highest and 10 is the lowest.

The **runtime complexity** of this algorithm is ```O(P^3)```, where P is the number of ```Page``` instances.

### Determining Which Pages Can Be Reached After Clicking N links Away from a Starting Page

This problem is an application of **Breadth-First Search**.

We will implement a function that will take three **parameters**:

- an ```Internet``` instance
- a ```str``` instance ```start_page_id```, representing the id value of the ```Page``` we start from
- and an integer ```pages_away```, representing the number of links we click away from the ```start_page```

which will **return** a ```destinations``` array of page ids which we can reach.

The **runtime complexity** of this algorithm is ```O(P + E)```, where E is the number of links in our ```Internet```, and P is the number of ```Page``` instances.

### Finding the Shortest Path Required to Get From One Page to Another

This problem is an application of **Dijkstra's Shortest Path Algorithm**.

We will implement a function that takes in three **parameters**:

- an ```Internet``` instance
- a ```str``` instance ```starting_page_id```
- and a ```str``` instance ```target_page_id```

which will **return** a ```path``` array of pages to reach from the start to the target.

The **runtime complexity** of this algorithm is ```O(E log P)```, where E is the number of links in our ```Internet```, and P is the number of ```Page``` instances.

## Resources

For more information explaining how PageRank works, and why you should care (as either a businessperson or web developer), please checkout:

1. [This awesome article on Search Engine Land](https://searchengineland.com/what-is-google-pagerank-a-guide-for-searchers-webmasters-11068), explaining PageRank for SEO's.

2. [A 5 minute explanation of PageRank](https://youtu.be/-mUI1g5PZXI) from Matt Cutts, the former Head of the Web Spam team at Google.

3. [Zach Star's explanation of PageRank](https://youtu.be/qxEkY8OScYY) uses adjaceny matrices to explain the algorithm. This explanation most closely resembles what is used in this project.
