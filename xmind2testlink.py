#-*- coding: utf-8 -*-
import xmind
from xml.etree import ElementTree
import argparse
import os

#备注
# print sheets[0].getRootTopic().getNotes().getContent()
#标签
# print sheets[0].getRootTopic().getFirstChildNodeByTagName(u'labels').getElementsByTagName('label')[0].childNodes[0].data
# subTopics = sheets[0].getRootTopic().getSubTopics()

def create_testcase(xml_root, top_topic):
    if top_topic.getSubTopics():
        for topic in top_topic.getSubTopics():
            note = topic.getNotes()
            if not topic.getSubTopics():
                testcase = ElementTree.Element(u'testcase')
                if note:
                    summary = ElementTree.Element(u'summary')
                    summary.text = note.getContent()
                    testcase.append(summary)
            else:
                testcase = ElementTree.Element(u'testsuite')
                if note:
                    details = ElementTree.Element(u'details')
                    details.text = note.getContent()
                    testcase.append(details)
            title = topic.getTitle()
            testcase.attrib = {u'name': title}
            keywords = generate_keyword(topic)
            if keywords is not None:
                testcase.append(keywords)
            print u'%s ,note is %s' % (title, note.getContent() if note else u'')
            xml_root.append(testcase)
            create_testcase(testcase, topic)


def creat_root_testcase(root_topic):
    root = ElementTree.Element(u'testsuite')
    title = root_topic.getTitle()
    root.attrib = {u'name': title}
    note = root_topic.getNotes()
    if note:
        details = ElementTree.Element(u'details')
        details.text = note.getContent()
        root.append(details)
    keywords = generate_keyword(root_topic)
    if keywords is not None:
        root.append(keywords)
    print u'%s ,note is %s' % (title, note.getContent() if note else u'')
    return root

def generate_keyword(topic):
    keywords = ElementTree.Element(u'keywords')
    if topic.getMarkers():
        for marker in topic.getMarkers():
            if marker.getMarkerId().name == u'flag-red':
                keyword = ElementTree.Element(u'keyword')
                keyword.attrib = {u'name': u'冒烟用例'}
                keywords.append(keyword)
            if marker.getMarkerId().name  == u'priority-1':
                keyword = ElementTree.Element(u'keyword')
                keyword.attrib = {u'name': u'P1'}
                keywords.append(keyword)
            if marker.getMarkerId().name  == u'priority-2':
                keyword = ElementTree.Element(u'keyword')
                keyword.attrib = {u'name': u'P2'}
                keywords.append(keyword)
            if marker.getMarkerId().name  == u'priority-3':
                keyword = ElementTree.Element(u'keyword')
                keyword.attrib = {u'name': u'P3'}
                keywords.append(keyword)
    if len(list(keywords)) > 0:
        return keywords
    else:
        return None

def parse_args():
    parser = argparse.ArgumentParser(description=u'convert xmind to testlink\'s xml')
    parser.add_argument(u'src', help=u'the path of xmind')
    parser.add_argument(u'dest', help=u'the write path of xml')
    return parser.parse_args()

if __name__ == u'__main__':
    args = parse_args()
    xmind_path = os.path.normpath(args.src)
    xml_path = os.path.normpath(args.dest)
    if not os.path.isfile(xmind_path):
        print u'%s dose not exist!' % xmind_path
        exit(-1)
    work = xmind.load(xmind_path)
    sheets = work.getSheets()
    for sheet in sheets:
        root = creat_root_testcase(sheet.getRootTopic())
        create_testcase(root, sheet.getRootTopic())
        tree = ElementTree.ElementTree(root)
        tree.write(xml_path, u'UTF-8')
