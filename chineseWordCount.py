import sublime
import sublime_plugin
import re

def basic_wordcount(text):
    words = 0
    chars = 0
    sections = 1
    charsFlag = 0
    sectionsFlag = 0

    textString = text
    for i in range(0,len(textString)):
    	#count the chinese words
        if 0x4e00 <= ord(textString[i]) <= 0x9fa5 :
            words += 1
            chars += 1
        #count the english chars and words
        if 0x20 <= ord(textString[i]) <= 0xff and ord(textString[i]) != 0x20 :
            chars += 1
            charsFlag = 1
            if i == (len(textString) - 1):
                words += 1
        else :
            if charsFlag == 1:
                words += 1
                charsFlag = 0
        #count the sections
        if ord(textString[i]) == 0x0A:
            sectionsFlag = 1
        else:
            if sectionsFlag == 1:
                sections += 1
                sectionsFlag = 0

    return words, chars, sections, len(textString)

class  ChineseWordCountCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		scope = "selected region"
		words = 0
		chars = 0
		total_chars = 0
		sections = 0
		lines = 0
		language = "plain text"
		sublime.message_dialog('''\
Word count for %s

words:\t\t\t\t\t\t%d
Characters (ignoring whitespace):\t%d
Characters (with whitespace):\t%d
sections:\t\t\t\t\t\t%d
Lines:\t\t\t\t\t\t%d

%s''' % (scope, words, chars, total_chars, sections, lines, language))
		