from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont as font, QFont
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QApplication, QFileDialog, QWidget, QCheckBox, QLabel, QTextEdit
from PyQt5.uic import loadUi
import sys
import tweepy
import fileinput
import networkx as nx
import matplotlib.pyplot as plt
import operator
import codecs
import matplotlib.pyplot as plti


class Main(QWidget):

    def __init__(self):
        ##tweepy stuff:
        auth = tweepy.OAuthHandler("SECRET","SECRET")
        auth.set_access_token("SECRET","SECRET")

        self.api = tweepy.API(auth,wait_on_rate_limit=True)

        super(Main, self).__init__()
        loadUi('s.ui', self)
        self.pushButton.clicked.connect(self.makeOutPut)
        self.networkButton.clicked.connect(self.showGraph)
        self.comapreButton.clicked.connect(self.showCompare)
        #show the two graphs button
        self.hashtag = ""
        self.list = []
        self.sdegree = {}
        self.sbetweennes = {}
        self.sclosennes = {}
        self.hDeg = 0
        self.hBetw = 0
        self.hClos = 0
        self.realNames = {}



        #make the degrees public too


    def makeOutPut(self):
        s = self.scrollArea
        txtEdit = QTextEdit()

        self.hashtag = self.input.text()
        self.getEffectedList()


        for line in open("naming.txt","r",encoding='utf-8'):
            split = line.split("$")
            split[1] = split[1].strip("\n")
            print(split)
            self.realNames[split[0]] = split[1]


        i = 1
        for org in self.list:
            print(org)
            line = str(i) + ") " + self.realNames[org]
            txtEdit.append(line)
            i = i + 1

        s.setWidget(txtEdit)


    def getEffectedList(self):
        self.list = []
        file = open("allValidAccounts.txt", "r")
        counter = 0
        for account in file:

            account = account.strip("\n")
            if account != "N/A":
                search = "("+self.hashtag+") "+"("+account+")"
                # tweets = api.search_full_archive(q=search,query="has:hashtags",label="try",maxResults=10)
                tweets = self.api.search_tweets(q=search,count=1)
                results = 0
                for tweet in tweets:
                    results = results + 1
                    break
                if results >= 1:
                    self.list.append(account)
                    print("Found:"+account)
                    counter = counter + 1

    def showGraph(self):
        ##showing the data:
        graph = nx.Graph()

        for line in open("networkData.txt", "r"):
            line = line.strip("\n")
            split = line.split("$")
            graph.add_edge(split[0], split[1])
            # print(split)
            # kite.com
            # sorting the values
            degree = {}
            betweennes = {}
            closennes = {}
            for node in graph.nodes:
                degree[node] = nx.degree_centrality(graph).get(node)
                betweennes[node] = nx.betweenness_centrality(graph).get(node)
                closennes[node] = nx.closeness_centrality(graph).get(node)
            temdegree = sorted(degree.items(), key=operator.itemgetter(1), reverse=True)
            self.sdegree = dict(temdegree)

            tembetweennes = sorted(betweennes.items(), key=operator.itemgetter(1), reverse=True)
            self.sbetweennes = dict(tembetweennes)

            temclosennes = sorted(closennes.items(), key=operator.itemgetter(1), reverse=True)
            self.sclosennes = dict(temclosennes)

        # Getting the # centrality
        for efName in self.list:
            graph.add_edge(efName, "#")


        hashtagDegree = 0
        for node in graph.nodes:
            if node == "#":
                hashtagDegree = nx.degree_centrality(graph).get(node)
                self.hDeg = nx.degree_centrality(graph).get(node)
                self.hBetw = nx.betweenness_centrality(graph).get(node)
                self.hClos = nx.closeness_centrality(graph).get(node)

        self.dlabel.setText(str(self.hDeg))
        self.dlabel_2.setText(str(self.hBetw))
        self.dlabel_3.setText(str(self.hClos))



        # for efName in self.list:
        #     graph.remove_edge(efName, self.hashtag)
        # if len(self.list) > 0:
        #     graph.remove_node(self.hashtag)


        arrayOfNames = list(graph.nodes)
        colors = []

        # colors would be longer than arrayof names
        for name in arrayOfNames:
            name = name.strip("\n")
            colors.append("grey")
        i = 0;
        for name in arrayOfNames:
            name = name.strip("\n")
            for efName in self.list:
                if efName == name:
                    colors[i] = "red"
            if name == "#":
                colors[i] = "blue"
            i = i + 1


        pos = nx.spring_layout(graph)
        nx.draw_networkx(graph, pos=pos, node_color=colors, with_labels=True)
        plt.show()

    def showCompare(self):
        ##https://www.tutorialspoint.com/matplotlib/matplotlib_bar_plot.htm
        fig = plti.figure()
        ax = fig.add_subplot(111)
        orgs = []
        values = []
        orgs.append("#")
        values.append(self.hClos)
        i =0
        for one in self.sclosennes:
            if i == 5:
                break
            orgs.append(one)
            values.append(self.sclosennes[one])
            i = i + 1

        ax.bar(orgs, values)
        plti.show()


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.setStyleSheet("background-color: rgb(255, 255, 255);")
start = Main()
widget.addWidget(start)
widget.show()
sys.exit(app.exec_())