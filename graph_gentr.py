import plotly.plotly as py
import plotly.graph_objs as go
import plotly as plt
import networkx as nx
import random
import json
import time
import os

from pprint import pprint
from collections import defaultdict


def fullJustify(words, maxWidth):
    res, cur, num_of_letters = [], [], 0
    for w in words:
        if num_of_letters + len(w) + len(cur) > maxWidth:
            for i in range(maxWidth - num_of_letters):
                cur[i % (len(cur)-1 or 1)] += ' '
            res.append(''.join(cur))
            cur, num_of_letters = [], 0
        cur += [w]
        num_of_letters += len(w)
    return res + [' '.join(cur).ljust(maxWidth)]


fakenames = ["Austin", "Jessica", "Noah", "David", "Bill", "James"]

def graph_gen(filename):
    plt.tools.set_credentials_file(
        username='akshay1994', api_key='ieUGzhNg4U33RPn74RXi')

    users = set()
    with open(filename) as f:
        comments = json.load(f)
        data = {}
        for comment in comments:
            users.add(comment['user'])
    colors = ["magenta", 'blue', "green", "cyan", "yellow", "red"]
    vertical_size = 80
    cord = range(10, 100*vertical_size*2, vertical_size)
    userscord = {user: cord[i] for i, user in enumerate(users)}
    usercolor = {user: colors[i] for i, user in enumerate(users)}
    username = {user: fakenames[i] for i, user in enumerate(users)}


    G = nx.DiGraph()


    nodes = len(comments)
    columns = len(users)

    stepsize = 50


    x = []
    y = list(range(1, (nodes + 1)*stepsize*2, stepsize))
    topic_list = []


    prevdata = defaultdict(int)
    cat = []
    for idx, comment in enumerate(comments):
        x.append(userscord[comment['user']])

        info = "User : " + username[comment['user']] + "<br>"
        info += "Content  : "
        data = fullJustify(comment['content'].split(" "), 100)
        for d in data:
            info += d + "<br>"

        info += "Detail : "
        for key, value in prevdata.items():
            info += key + " : " + str(value) + " , "
        info += " <br>"

        info += "Topic probabilities : "

        for key, value in comment['topic_probablities'].items():
            info += key + " : " + value + " , "
        info += " <br>"
        prevdata[comment['dominant_topic'].capitalize()] += 1

        info += "Keywords : " + comment['keywords'] + "<br>"
        info += "Time : " + comment['timeCode'] + "<br>"

        topic_list.append(info)

        tp = [[label, float(value.split(" ")[0])]
            for label, value in comment['topic_probablities'].items()]

        tp.sort(key=lambda x: x[1], reverse=True)

        cat.append(comment['dominant_topic'].capitalize() + ", " + tp[1][0])
        if comment['reply'] != -1:
            G.add_edge(idx, comment['reply'])


    G.add_nodes_from(list(range(nodes)))

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=1.5, color='#f13'),
        hoverinfo='none',
        mode='lines')


    for edge in G.edges():
        x0, y0 = x[edge[0]], y[edge[0]]
        x1, y1 = x[edge[1]], y[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])
        edge_trace['marker']['color'] = random.choice(colors)

    Topic = ["Finance", "Education", "Quality",
            "Affordability", "HealthCare", "Prevention"]


    node_trace = go.Scatter(
        x=x,
        y=y,
        text=cat,
        mode="markers, text",
        textposition="bottom center",
        hovertext=topic_list,
        hoverinfo="text",
        marker=dict(
            showscale=False,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,

            line=dict(width=2)))


    i = 0

    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'] += tuple([usercolor[comments[i]['user']]])
        i += 1


    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                    autosize=False,
                    width=len(users)*vertical_size + vertical_size*6,
                    height=nodes*stepsize + stepsize*5,
                    title='<br>Network graph made with Python',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=10, r=10, t=40),
                    xaxis=dict(showgrid=False, zeroline=False,
                            showticklabels=False),
                    yaxis=dict(autorange="reversed", showgrid=False, zeroline=False, showticklabels=False)))


    py.plot(fig, filename=os.path.basename(filename))

if __name__ == "__main__":
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "Output_Files/JSON")):
        for file in files:
            if "new" in file and ".json" in file:
                print(os.path.join(root, file))
                graph_gen(os.path.join(root, file))    
