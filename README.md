# PageRank Graph Model

A model for understanding Google's PangeRank algorithm, based upon the concepts of Graph Theory.

PageRank is the algorithm Google uses to sift through the absurd amounts of web pages out there, so that in search results you and I see only the most important and useful information related to our search.

![Google 'G' on a chalkboard with computer science on it](https://i.postimg.cc/FHcdKh7y/Screen-Shot-2020-06-26-at-5-59-40-PM.png)
Credits to Danny Sullivan, on Search Engine Land for the above image ([link to original site](https://searchengineland.com/what-is-google-pagerank-a-guide-for-searchers-webmasters-11068)).

## Table of Contents

1. [How Graph Theory Relates to PageRank](#how-graph-theory-relates-to-pagerank)
2. [How the Model is Structured](#how-the-model-is-structured)
3. [The ```InternetGraph``` Class](#the-internetgraph-class)
4. [The ```PageVertex``` Class](#the-pagevertex-class)
5. [Problems To Investigate](#problems-to-investigate)
    - [Calculating the PageRank Rating for each Page in a Network](#calculating-the-pagerank-rating-for-each-page-in-a-network)
    - [Determining Which Pages Can Be Reached After Clicking N links Away from a Starting Page](#determining-which-pages-can-be-reached-after-clicking-n-links-away-from-a-starting-page)
    - [Finding the Shortest Path Required to Get From One Page to Another](#finding-the-shortest-path-required-to-get-from-one-page-to-another)
6. [Scale](#scale)
7. [Resources](#resources)

## How Graph Theory Relates to PageRank

If there's two things that the Internet does really well, it's:

1. **Storing** Information, and
2. **Connecting** people with that information

As it turns out, graphs are an optimal data structure to model the Web. Why?

This is because graphs **are also great** at:

- **storing data** in objects called **vertices**,
- and **connecting** vertices together using **edges**

More specifically, here are further details to specify the graph data structure we will use in this project:

- The graph in this case, will be represent all web pages on the Internet. Will be implemented in Python using the ```InternetGraph``` class.
- Individual vertices in the graph are implemented by the ```PageVertex``` class.
- Not all ```PageVertex``` instances in the graph are necessarily connected.
- **Edges** between the pages **represent hyperlinks** on the Internet.
- **Edges are weighted**, in order to **represent the probability** that a user goes from a certain site to another.
- **Edges are directed**. This is because **hyperlinks are one-way connections**. ```PageVertex A``` may link to ```PageVertex B``` for example, but the reverse is not necessarily true.

## How the Model is Structured

The model is structured using Object-Orientated Programming. The properties and instance methods of the ```PageVertex``` and ```InternetGraph``` classes are below.

### The ```InternetGraph``` Class

A representation of the World Wide Web. This class is a *composition* of many ```PageVertex``` instances.

#### Attributes of ```InternetGraph```

- ```dict: pages```: this dictionary maps the ```page_id``` attribute of each ```PageVertex``` instance, to the ```PageVertex``` instance itself.

#### Methods of ```InternetGraph```

*This section currently under construction*.

### The ```PageVertex``` Class

A representation of a single web page.

#### Attributes of ```PageVertex```

- ```str: page_id```: a unique name for the web page
- ```dict: neighbors```: this dictionary represents the other ```PageVertex``` instances that can be reached using hyperlinks from this web page. The dictionary maps the ```page_id``` attribute of the other ```PageVertex``` instances, to the other ```PageVertex``` object.
- ```float: link_weight``` is the weight that each edge from this ```PageVertex``` instance carries. This attribute of the edge represents the probability a site visitor goes to any one of the neighboring sites linked by this ```PageVertex``` instance. It is calculated as by dividing 100%, by the number of ```neighbors``` that page has. For example, if a ```PageVertex``` has 2 ```neighbors``` that it links *towards* (aka its "outlinks"), then each of the ```weight``` values for those edges will be 0.50.

#### Methods of ```PageVertex```

*This section currently under construction*.

## Problems To Investigate

In this project, we will take a look at several problems that Google uses the PageRank algorithm to solve, and modelling their solutions in code based upon the Graph ADT.

**The problems are as follows:**

### Calculating the PageRank Rating for each PageVertex in a Network

This problem is an application of an algorithm similar to the **Floyd-Warshall** algorithm.

We will implement a function that will take one **parameter**:

- an ```InternetGraph``` instance

which will **return** a ```rankings``` array of pages, each element being a tuple of the ```PageVertex.page_id```; as well as a ranking between 1-10, where 1 is the highest and 10 is the lowest.

The **runtime complexity** of this algorithm is ```O(P^3)```, where P is the number of ```PageVertex``` instances.

### Determining Which Pages Can Be Reached After Clicking N links Away from a Starting PageVertex

This problem is an application of **Breadth-First Search**.

We will implement a function that will take three **parameters**:

- an ```InternetGraph``` instance
- a ```str``` instance ```start_page_id```, representing the id value of the ```PageVertex``` we start from
- and an integer ```pages_away```, representing the number of links we click away from the ```start_page```

which will **return** a ```destinations``` array of page ids which we can reach.

The **runtime complexity** of this algorithm is ```O(P + E)```, where E is the number of links in our ```InternetGraph```, and P is the number of ```PageVertex``` instances.

### Finding the Shortest Path Required to Get From One Page to Another

This problem is an application of **Dijkstra's Shortest Path Algorithm**.

We will implement a function that takes in three **parameters**:

- an ```InternetGraph``` instance
- a ```str``` instance ```starting_page_id```
- and a ```str``` instance ```target_page_id```

which will **return** a ```path``` array of pages to reach from the start to the target.

The **runtime complexity** of this algorithm is ```O(E log P)```, where E is the number of links in our ```InternetGraph```, and P is the number of ```PageVertex``` instances.

## Scale

This section will report on *how solvable* the problems in this investigation become, as well as *how efficiently* the algorithms currently being used to solve them become as the size of the input grows asymptotically.

1. PageRank

    PageRank in its full complexity, appears to still work as we add more and more web pages and hyperlinks to the Web. According to [Search Engine Land](https://searchengineland.com/googles-search-indexes-hits-130-trillion-pages-documents-263378), as of 2016 Google has indexed over 130 trillion web pages. Although Google does not publicly announce how PageRank's implementation has changed over the years, [this article on Search Engine Roundtable](https://www.seroundtable.com/google-still-uses-pagerank-29056.html) reports that John Mueller, a Webmaster Trends Analyst at Google, stated in February that the company still uses the algorithm to rank pages *internally* in 2020.

    Currently the method used to perform PageRank, ```InternetGraph.rank_pages```, runs in ```O(P^2 + L)```, where ```P = number of PageVertexs``` and ```L = number of links``` in the InternetGraph. This is mainly due to the runtime used to find the inlinks leading to each ```PageVertex``` - this is performed by a helper function ```InternetGraph.compute_inlink_values```. This is not an efficient algorithm for inputs where ```P + L``` is much greater than 30, perhaps on the scale of 1000s of pages and links.

2. Finding Neighbors n Links Away

    This problem is not solvable as the size of the input scales asymptotically. The InternetGraph as we know it today is simoly too large to get around simply through clicking on links. Be grateful for search engines!

    The function used to solve this problem is ```InternetGraph.find_pages_n_away```. This function implements the Breadth-first Search algorithm for up to n, the number of links specified to traverse in the graph. Therefore in worst case, the runtime of the function is ```O(P + L)```, where ```P = number of PageVertexs``` and ```L = number of links``` in the overall graph. For small inputs and inputs around 30, this is an efficient algorithm. However, on the true scale of the InternetGraph, which is trillions of pages, it is not efficient.

3. Shortest Path-Finding

    This problem is also not solvable as the size of the InternetGraph increases asymptotically, for the same reason as above: when dealing with trillions of web pages, it is simply better to use search engines and applications in order to quickly get between different web pages of interest.

    The function used to solve this problem is ```InternetGraph.find_shortest_path```, which implements Dijkstra's Shortest Path algorithm. This algorithm is usually ```O(P log P)```. However, because an array is used instead of binary min heap in this implementation, the runtime is currently ```O(P^2)```. This would not be an efficient function to use on inputs of size 30 or more.

## Resources

For more information explaining how PageRank works, and why you should care (as either a businessperson or web developer), please checkout:

1. [This awesome article on Search Engine Land](https://searchengineland.com/what-is-google-pagerank-a-guide-for-searchers-webmasters-11068), explaining PageRank for SEO's.

2. [A 5 minute explanation of PageRank](https://youtu.be/-mUI1g5PZXI) from Matt Cutts, the former Head of the Web Spam team at Google.

3. [Zach Star's explanation of PageRank](https://youtu.be/qxEkY8OScYY) uses adjaceny matrices to explain the algorithm. This explanation most closely resembles what is used in this project.

4. [Technical Write-up of this Model](https://medium.com/@zain_raza/what-makes-google-search-work-942e38521348?source=friends_link&sk=a22d26c19f6b11cbd40b3d77afd65baf): in this blog post I go over the conceptual details involving Graph Theory more in detail.
