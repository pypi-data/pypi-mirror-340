import sys
import time
from datetime import datetime
import requests
from .db_info import *
from .mysql_query_builder import *
from .html_builder import *
from fastapi import FastAPI,Response
import uvicorn
app=FastAPI()
from .lazy_table import LazyTable
from .lazy_tree import LazyTree
from .rich_text_editor import RichTextEditor
from .tabs import Tabs,TabButtons
from .dividers import HorizontalDivider,VerticalDivider
import random
from string import ascii_letters as letters
@app.get('/home')
async def home():
    doc=HtmlDoc()
    css=doc.head.Style()
    css.addCssFile('./lazy_table.css')
    css.addCssFile('./lazy_tree.css')
    css.addCssFile('./rich_text_editor.css')
    css.addCssFile('./tabs.css')
    css.addCssFile('./dividers.css')
    js=doc.head.Script()
    js.addJsFile('./lazy_table_funcs.js')
    js.addJsFile('./lazy_tree_funcs.js')
    js.addJsFile('./rich_text_editor_funcs.js')
    js.addJsFile('./tabs_funcs.js')
    js.addJsFile('./dividers_funcs.js')
    js.addJsFile('./chart_scatter.js')
    js.addJsFile('./chart_scatter_time.js')
    js.addJsFile('./chart_line.js')
    doc.body.P({'text':'ping received (ms)'})
    row0=doc.body.row()
    col=row0.column({'style':{'height':'200px','width':'200px'}})
    col.appendChild(LazyTable({'id':'table','style':{'width':'100%'}},
                              {'checks':True,'headers':['col1','col2']}))
    js=doc.body.Script()
    ls=[[random.randint(0,1000),random.randint(0,1000)] for _ in range(100000)]
    js.addVar('ls',ls)
    js.addLines(
        "LAZYTABLE.resize('table')",
        "LAZYTABLE.setData('table',ls)",
        "LAZYTABLE.populate('table')",
    )
    row0.appendChild(HorizontalDivider())
    row1=row0.row({'style':{'width':'600px'}})
    col=row1.column({'style':{'min-height':'100%','width':'200px'}})
    col.appendChild(LazyTable({'id':'table2'},{'radios':True,'headers':['col1','col2'],
                    'colWidths':[100,100]}))
    js=doc.body.Script()
    ls=[]
    for _ in range(10000):
        a=''.join([letters[random.randint(0,len(letters)-1)] for _ in range(20)])
        b=''.join([letters[random.randint(0,len(letters)-1)] for _ in range(20)])
        ls.append([a,b])
    js.addVar('ls2',ls)
    js.addLines(
        "LAZYTABLE.resize('table2')",
        "LAZYTABLE.setData('table2',ls2)",
        "LAZYTABLE.populate('table2')",
    )
    row1.appendChild(HorizontalDivider())
    col=row1.column({'style':{'height':'300px','width':'calc(100% - 205px)'}})
    col.appendChild(LazyTree({'id':'tree'},{'headers':['firstlayer','secondlayer','thirdLayer'],'colorSelectors':True}))
    js=doc.body.Script()
    js.addVar('data',[
        {'firstlayer':'asdf','secondlayer':'1234','thirdLayer':'asdfsacxz'},
        {'firstlayer':'asdf','secondlayer':'1234','thirdLayer':'asdf'},
        {'firstlayer':'asdf','secondlayer':'1234','thirdLayer':'tyterdh'},
        {'firstlayer':'asdf','secondlayer':'7573','thirdLayer':'dgh'},
        {'firstlayer':'asdf','secondlayer':'7573','thirdLayer':'dfghf'},
        {'firstlayer':'asdf','secondlayer':'7573','thirdLayer':'4yrty'},
        {'firstlayer':'asdf','secondlayer':'7573','thirdLayer':'cvmr'},
        {'firstlayer':'qwer','secondlayer':'7fgd573','thirdLayer':'gdhgh'},
        {'firstlayer':'qwer','secondlayer':'7fgd573','thirdLayer':'xg'},
        {'firstlayer':'qwer','secondlayer':'7fgd573','thirdLayer':'fghg'},
        {'firstlayer':'qwer','secondlayer':'36643fga','thirdLayer':'g'},
        {'firstlayer':'qwer','secondlayer':'36643fga','thirdLayer':'gfh'},
        {'firstlayer':'qwer','secondlayer':'36643fga','thirdLayer':'asdfshfgacxz'},
        {'firstlayer':'qwer','secondlayer':'36643fga','thirdLayer':'ththt'},
        {'firstlayer':'qwer','secondlayer':'36643fga','thirdLayer':'vbrrr'},
        {'firstlayer':'zxcv','secondlayer':'7fgd573','thirdLayer':'bbrhehe'},
        {'firstlayer':'zxcv','secondlayer':'7fgd573','thirdLayer':'htetth'},
        {'firstlayer':'zxcv','secondlayer':'7fgd573','thirdLayer':'hfghg'},
        {'firstlayer':'zxcv','secondlayer':'7fgd573','thirdLayer':'ghgfhd'},
        {'firstlayer':'zxcv','secondlayer':'sdfdsfsf','thirdLayer':'drery'},
        {'firstlayer':'zxcv','secondlayer':'sdfdsfsf','thirdLayer':'eruyhhhj'},
        {'firstlayer':'zxcv','secondlayer':'sdfdsfsf','thirdLayer':'htrtt'},
        {'firstlayer':'zxcv','secondlayer':'sdfdsfsf','thirdLayer':'cghth'},
        {'firstlayer':'tyui','secondlayer':'7fgd573','thirdLayer':'cghgh'},
        {'firstlayer':'tyui','secondlayer':'7fgd573','thirdLayer':'eyqerq'},
        {'firstlayer':'tyui','secondlayer':'7fgd573','thirdLayer':'cghgerrt'},
        {'firstlayer':'tyui','secondlayer':'7fgd573','thirdLayer':'qsgsdh'},
        {'firstlayer':'tyui','secondlayer':'sdfdsfsf','thirdLayer':'dhdhcbv'},
        {'firstlayer':'tyui','secondlayer':'sdfdsfsf','thirdLayer':'cvbrwrrer'},
        {'firstlayer':'tyui','secondlayer':'sdfdsfsf','thirdLayer':'dfghdfh'},
        {'firstlayer':'tyui','secondlayer':'sdfdsfsf','thirdLayer':'rytytyt'},
    ])
    js.addLines(
        f"LAZYTREE.setData('tree',data)",
        f"LAZYTREE.populate('tree')",
    )
    row0=doc.body.row({'style':{'height':'300px'}})
    rte=row0.appendChild(RichTextEditor({'id':'rte','style':{},
         'onmousedown':f"RichTextEditor.onmousedownTable(event,'rte')"}))
    rte.body.attrs['text']=('asldkjflskjfsld<div>zxcvzcxzxcvz</div><table><tbody>'
                            '<tr><td>a</td><td>b</td><td>c</td><td>d</td></tr>'
                            '<tr><td>e</td><td>f</td><td>g</td><td>h</td></tr>'
                            '<tr><td>i</td><td>j</td><td>k</td><td>l</td></tr>'
                            '<tr><td>m</td><td>n</td><td>o</td><td>p</td></tr>'
                            '</tbody></table><div>qwerqwerqwr</div>')
    doc.body.appendChild(VerticalDivider())
    col1=doc.body.column({'style':{'margin-top':'10px','width':'300px','height':'150px'}})
    tabNames=['tab1','tab2','tab3']
    col1.appendChild(TabButtons(tabNames))
    tabCont=col1.appendChild(Tabs(len(tabNames)))
    tabCont.children[0].P({'text':'tab 1 content'})
    button=tabCont.children[0].Button({'text':'dummy button'})
    button.tooltip({'text':'this is a dummy button that has a tooltip'})
    tabCont.children[1].P({'text':'asdlkfjsalkdfasdfasdfseryretyrhrthrrtadfasdfasfsadfasasfds'})
    tabCont.children[2].P({'text':'zzxcvzxcvxzcuio'})
    doc.body.appendChild(VerticalDivider())
    row1=doc.body.row({'style':{'width':'600px','height':'300px'}})
    row1.Canvas({'id':'graph1'})
    js=doc.body.Script()
    numPoints=1000
    rainbow=['red','orange','yellow','green','blue','violet']
    xs=[random.randint(0,10000)/100000 for _ in range(numPoints)]
    ys=[random.randint(0,10000) for _ in range(numPoints)]
    labels=[f'label{c}' for c in range(numPoints)]
    colors={}
    for c,label in enumerate(labels):
        colors[label]=rainbow[c%len(rainbow)]
    js.addVar('xs',xs)
    js.addVar('ys',ys)
    js.addVar('labels',labels)
    js.addVar('colors',colors)
    js.addLines(
        f"let canvas=document.getElementById('graph1')",
        f"let chart=new chartScatter(canvas,{{'title':'GRAPH1','numXTicks':20,'numTooltipPoints':1}})",
        f"chart.setData(xs,ys,labels)",
        f"chart.setColors(colors)",
        f"chart.draw()",
        f"chart.setEvents()",
    )
    doc.body.appendChild(VerticalDivider())
    row1=doc.body.row({'style':{'width':'600px','height':'300px'}})
    row1.Canvas({'id':'graph2'})
    js=doc.body.Script()
    numPoints=10000
    xs=[random.randint(1744209442-3600*24*1,1744209442) for _ in range(numPoints)]
    ys=[random.randint(0,10000) for _ in range(numPoints)]
    labels=[f'label{c}' for c in range(numPoints)]
    colors={}
    for c,label in enumerate(labels):
        colors[label]=rainbow[c%len(rainbow)]
    js.addVar('xs2',xs)
    js.addVar('ys2',ys)
    js.addVar('labels2',labels)
    js.addVar('colors2',colors)
    js.addLines(
        f"canvas=document.getElementById('graph2')",
        f"chart=new chartScatterTime(canvas,{{'title':'GRAPH2','numXTicks':10}})",
        f"chart.setData(xs2,ys2,labels2)",
        f"chart.setColors(colors2)",
        f"chart.draw()",
        f"chart.setEvents()",
    )
    doc.body.appendChild(VerticalDivider())
    row1=doc.body.row({'style':{'width':'600px','height':'300px'}})
    row1.Canvas({'id':'graph3'})
    js=doc.body.Script()
    numPoints=100
    xs=list(range(numPoints))
    ys1=[random.randint(0,numPoints) for _ in range(numPoints)]
    ys2=[random.randint(0,numPoints) for _ in range(numPoints)]
    ys3=[random.randint(0,numPoints) for _ in range(numPoints)]
    labels=[f'label{c}' for c in range(3)]
    colors={}
    for c,label in enumerate(labels):
        colors[label]=rainbow[c%len(rainbow)]
    js.addVar('xs3',xs)
    js.addVar('ys3a',ys1)
    js.addVar('ys3b',ys2)
    js.addVar('ys3c',ys3)
    js.addVar('labels3',labels)
    js.addVar('colors3',colors)
    js.addLines(
        f"canvas=document.getElementById('graph3')",
        f"chart=new chartLine(canvas,{{'title':'GRAPH3'}})",
        f"chart.addDataSet(xs3,ys3a,labels3[0])",
        f"chart.addDataSet(xs3,ys3b,labels3[1])",
        f"chart.addDataSet(xs3,ys3c,labels3[2])",
        f"chart.setColors(colors3)",
        f"chart.draw()",
        f"chart.setEvents()",
    )
    docstr=doc.str().encode(encoding='raw_unicode_escape').replace(b'\\u',b'&#x').replace(b'\\U',b'&#x')
    print(round(len(docstr)/1024/1024,1),'MB')
    return Response(docstr,media_type='text/html')

if __name__=='__main__':
    uvicorn.run(app,port=5001)