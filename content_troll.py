#! /usr/bin/python
# Requires wikipedia.py, wiki2plain.py, and python yaml
import wikipedia
import os
import unicodedata
import random


class Face:
    def __init__(self, topic):
        self.content = ''
        self.topic = topic

        if self.topic:
            self.content = self.get_text()

    def set_topic(self, new_topic):
        self.topic = new_topic
        topic_path = os.path.join("content", "{}.txt".format(new_topic))
        if os.path.exists(topic_path):
            with open(topic_path, "r") as f:
                self.content = f.read()
        else:
            self.content = self.get_text()

    def get_text(self):
        print('get_text: {}'.format(self.topic))
        assert self.topic
        queries = [self.topic, self.topic[:len(self.topic) // 2]]
        tokens = self.topic.split()
        if len(tokens) > 1:
            queries.append(tokens[0])
            queries.append(tokens[-1])

        topic_results = list()
        for query in queries:
            topic_results.extend(wikipedia.search(query))
        print('topic_results size:', len(topic_results))
        try:
            topic_results = wikipedia.search(self.topic)
            for query in random.sample(topic_results, 9):
                self.content += wikipedia.page(query).content
        except wikipedia.exceptions.DisambiguationError:
            self.content += self.topic + ' can mean many things but to me it is'
        except wikipedia.exceptions.PageError:
            self.content += self.topic + ' is sometimes hard to find'
        return self.content

    def research_topic(self, topic, logger):
        content = ""

        # do a wikipedia search for the topic
        topic_results = wikipedia.search(topic)

        logger("  Search returned %d articles on %s" % (len(topic_results), topic))
        for i in range(len(topic_results)):
            try:
                data = wikipedia.page(topic_results[i]).content
                if type(data) is str:
                    content += data
                elif type(data) is unicode:
                    content += unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')
            except:
                pass

        return content

    def fully_research_topic(self, topic, logger):
        content = ""

        content += self.research_topic(topic, logger)

        topic_split = topic.split()
        if len(topic_split) > 1:
            for i in range(len(topic_split)):
                try:
                    # Skip words that are less than five characters
                    if len(topic_split[i]) < 3:
                        continue

                    content += self.research_topic(topic_split[i], logger)

                except wikipedia.exceptions.DisambiguationError:
                    content += topic + ' can mean many things but to me it is'
                except wikipedia.exceptions.PageError:
                    content += topic + ' is sometimes hard to find'

        return content

    def parse_text(self):
        phrases = []
        words = self.content.split()
        # function to take a blob and parse out apropriately sized snippets
        for index in range(0, len(words) - 1):
            if self.topic.lower()[:len(self.topic) // 4] in words[index].lower() or self.topic.split()[-1].lower() in \
                    words[index].lower():
                cur_word = words[index]
                phrase = ''
                if index > 5:
                    i = index - random.randint(0, 5)
                else:
                    i = index
                counter = 0
                while cur_word.isalpha() and counter < 6:
                    try:
                        phrase = phrase + words[i].lower() + ' '
                        i += 1
                        cur_word = words[i]
                    except:
                        cur_word = '...'
                    counter += 1
                if len(phrase.split()) > 3:
                    temp = ''
                    for char in phrase:
                        if char.isalpha() or char.isspace():
                            temp += char
                    phrase = temp
                    other_words = [
                            'using only my', 'forever!', 'because', 'for once in your life', 'until',
                            'Great Job!', ', but in reality', 'is wrong!', 'is #1', 'never dies', 'is really',
                            'might be', 'or not', 'better known as', 'the worst', 'kinda feels like',
                            ', right?', '', ', WTF!', ', for realz', ', tru fact', 'in the feels',
                            'probably the best', '?']
                    phrase += random.choice(other_words)
                    phrases.append(phrase)
        phrases = list(set(phrases))
        return phrases

    def parse_bullets(self):
        bullets = []
        sentences = self.content.split('.')
        for ea in sentences:
            if len(ea) in range(50, 75) and "\n" not in ea and "=" not in ea:
                bullets.append(ea)
        return bullets

    def get_bullets(self, min_count):
        final_bullets = []
        while len(final_bullets) < min_count:
            self.content += self.get_text()
            bullets = self.parse_bullets()
            for b in bullets:
                final_bullets.append(b.strip())
        return final_bullets

    def get_titles(self, min_count):
        # function to choose short headlines for the top of slides
        headlines = []
        while len(headlines) < min_count:
            self.content += self.get_text()
            phrases = self.parse_text()
            for p in phrases:
                headlines.append(p.strip())
        return headlines
