import sublime
import sublime_plugin
import re

#For the unicode files
def chinese_wordcount(text):
    words = 0
    chinesewords = 0
    chars = 0
    sections = 1
    newlines = 0
    charsFlag = 0
    sectionsFlag = 0

    textString = text
    for i in range(0,len(textString)):
    	#count the chinese words
        if 0x2000 <= ord(textString[i]) <= 0xffff :
            words += 1
            chars += 1
            chinesewords += 1
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
            newlines += 1
            sectionsFlag = 1
        else:
            if sectionsFlag == 1:
                sections += 1
                sectionsFlag = 0

    return words, chinesewords, chars, sections, (len(textString) - newlines)

class  ChineseWordCountCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selected = self.view.sel()
        lines = len(self.view.lines(selected[0]))

        scope = "selected region"
        if len(selected) == 1 and selected[0].empty():
            selected = [sublime.Region(0, self.view.size())]
            lines = self.view.rowcol(self.view.size())[0] + 1
            scope = "entire file"

        words = 0
        chinesewords = 0
        chars = 0
        total_chars = 0
        sections = 0
        language = "plain text"

        for region in selected:
            (rwords, rchinesewords, rchars, rsections, rtotal) = chinese_wordcount(self.view.substr(region))
            words += rwords
            chinesewords += rchinesewords
            chars += rchars
            sections += rsections
            total_chars += rtotal

        sublime.message_dialog('''\
Word count for %s

words:\t\t\t\t\t\t%d
chinese words:\t\t\t\t\t%d
Characters (ignoring whitespace):\t%d
Characters (with whitespace):\t%d
sections:\t\t\t\t\t\t%d

%s''' % (scope, words, chinesewords, chars, total_chars, sections, language))	