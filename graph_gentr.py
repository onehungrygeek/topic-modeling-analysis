import plotly.plotly as py
import plotly.graph_objs as go
import plotly as plt
import networkx as nx
import random
import json
import time
from pprint import pprint



plt.tools.set_credentials_file(username='akshay1994', api_key='ieUGzhNg4U33RPn74RXi')

users = set()
with open('new.json') as f:
    comments = json.load(f)
    data = {}
    for comment in comments:
        users.add(comment['user'])
#         epochtime =time.mktime(time.strptime(comment['timeCode'],"%B %d, %Y, %I:%M:%S PM"))
#         data[epochtime] = {'user': comment['user'], "keywords": comment['']}
#         
#         
        
vertical_size = 80
cord = range(10, 100*vertical_size*2, vertical_size)
userscord = {user:cord[i]  for i,user in enumerate(users)}


print(len(users)*vertical_size + vertical_size*4,)

G=nx.DiGraph()




nodes = len(comments)
columns = len(users)

stepsize = 50


x = []
y = list(range(1, (nodes + 1)*stepsize*2, stepsize))
topic_list = []

for comment in comments:
    x.append(userscord[comment['user']])
    topic_list.append("<br>".join(comment['keywords'].split()))


print(len(y) , len(set(y)))

G.add_nodes_from(list(range(nodes)))
# If no positions are provided, choose uniformly random vectors in
# Euclidean space of the specified dimension.

#pos = {v: [v/divi if i == 0 else v%divi for i in range(2)] for v in xrange(nodes)}
#nx.set_node_attributes(G, pos, 'pos')



# for i in xrange(1, nodes-1):
#     G.add_edge(i, i+1)
# 
G.add_edges_from( [(1,5) , (2, 4)]) 

# 
edge_trace = go.Scatter(
    x= [],
    y= [],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')


# for edge in G.edges():
#     x0, y0 = G.node[edge[0]]['pos']
#     x1, y1 = G.node[edge[1]]['pos']
#     edge_trace['x'] += tuple([x0, x1, None])
#     edge_trace['y'] += tuple([y0, y1, None])



 


Topic = ["Finance", "Education", "Quality", "Affordability", "HealthCare", "Prevention"] 


cat = []
for i in range(nodes):
    cat.append(random.choice(Topic))
    
  
  
    
# mode='lines+markers+text',
#     name='Lines, Markers and Text',
#     text=['Text A', 'Text B', 'Text C'],
#     textposition='top center'
#Any combination of ['x', 'y', 'z', 'text', 'name'] joined with '+' characters

node_trace = go.Scatter(
    x=x,
    y=y,
    text = cat,
    mode= "markers, text",
    textposition="bottom center",
    hovertext = topic_list,
    hoverinfo="text",
    marker=dict(
        showscale=False,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
#         colorbar=dict(
#             thickness=15,
#             title='Node Connections',
#             xanchor='right',
#             titleside='right'
#         ),
        #textfont = dict(color="white"),
        line=dict(width=2)))

# i = 0
# for node in G.nodes():
#     #x, y = G.node[node]['pos']
#     
#     node_trace['x'] += tuple([x[i]])
#     node_trace['y'] += tuple([y[i]])
#     i += 1


keywords = ["Hello, namaste, aaa", "bbbbb  ccccc", "ddddd ffff"]
i = 0

for node, adjacencies in enumerate(G.adjacency()):
    
    node_trace['marker']['color']+=tuple([random.randint(0,100)])
    node_info = random.choice(Topic)# of connections: '+str(len(adjacencies[1]))
    
    
    #node_trace['text']+=tuple([keywords[i%(len(keywords))]])
    i += 1


 

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                autosize=False,
                width=len(users)*vertical_size + vertical_size*3,
                height=nodes*stepsize + stepsize*4,  
                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
#                 annotations=[ dict(
#                                     x=2,
#                                     y=5,
#                                     xref='x',
#                                     yref='y',
#                                     text='dict Text',
#                                     showarrow=False,
#                                     arrowhead=7,
#                                     ax=0,
#                                     ay=-40
#                                 ), ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))



py.plot(fig, filename='networkx12')
