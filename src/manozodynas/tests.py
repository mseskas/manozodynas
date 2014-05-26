# encoding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from manozodynas.testutils import StatefulTesting

import unittest
from django.test import Client
from manozodynas.models import *

# ============== Mindaugas Šeškas tests ===============

class MainPageTest(StatefulTesting):
    def test_InsertTranslation(self):
        self.open(reverse('index'))
        self.selectForm('#insert_translation')
        self.submitForm({
            'key_word': 'test',
            'matches': 'testas ',
        })
        self.assertStatusCode(200)
        
        tran = Translation.objects.all().filter(key_word='test')
        if tran.count() < 1:
            self.fail("Translation insert failed")

    def test_InsertWord(self):
        self.open(reverse('word'))
        self.selectForm('#insert_word')
        self.submitForm({
            'key': 'test',
            'description': 'testas ',
        })
        self.assertStatusCode(200)
        
        word = Words.objects.all().filter(key='test')
        if word.count() < 1:
            self.fail("Word insert failed")

class WordsInsertTest(unittest.TestCase):
    def setUp(self):
        w = Words.objects.create(key="go", description="go sound")
        w.save()

    def test_WordGo(self):
        d = Words.objects.all().filter(key='go')
        if d.count() < 1:
            self.fail("Word insert failed")
        else:
            self.assertEqual(d[0].key, 'go')


class TranslationInsertTest(unittest.TestCase):
    def setUp(self):
        w = Translation.objects.create(key_word="go", matches="eiti keliauti judeti")
        w.save()

    def test_TranslationGo(self):
        d = Translation.objects.all().filter(key_word='go')
        if d.count() < 1:
            self.fail("Translation insert failed")
        else:
            self.assertEqual(d[0].key_word, 'go')


# ============== end of Mindaugas Šeškas tests ===============

class IndexTestCase(StatefulTesting):
    def test_index_page(self):
        self.open(reverse('index'))
        self.assertStatusCode(200)


class LoginTestCase(StatefulTesting):

    fixtures = ['test_fixture.json']

    def test_login_page(self):
        self.open(reverse('login'))
        self.assertStatusCode(200)

    def test_good_login(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'test',
            'password': 'test',
        })
        self.assertStatusCode(302)

    def test_bad_login(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'bad',
            'password': 'bad',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')

    def test_no_input(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': '',
            'password': '',
        })
        self.assertStatusCode(200)
        self.selectMany('.errorlist')

    def test_no_username(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': '',
            'password': 'test',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')

    def test_no_password(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'test',
            'password': '',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')

if __name__ == '__main__':
    unittest.main()
